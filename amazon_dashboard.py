import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Amazon Products Dashboard",layout ='wide')
st.title("Amazon Products Dashboard")
df = pd.read_csv('amazon.csv')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = df['rating_count'].str.replace(',', '').astype(float)
df['discounted_price'] = df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)
df['actual_price'] = df['actual_price'].str.replace('₹', '').str.replace(',', '').astype(float)
st.markdown("---")
st.subheader("Search & Filter Products")
col1,col2 = st.columns(2)
col3,col4 = st.columns(2)
col5,col6 = st.columns(2)
with col1:
    search = st.text_input("search by product name")
with col2:
    category = st.multiselect("select categories", df['category'].unique())
with col3:
     min_price = st.number_input("Min Price (₹)", value=0)
with col4:
    max_price = st.number_input("Max Price (₹)", value=100000)
with col5:
    min_rating = st.slider("Min Rating", 0.0, 5.0, 0.0)
with col6:
    min_reviews = st.number_input("min review count",value=0)
filtered_df = df.copy()
if search:
    filtered_df=filtered_df[filtered_df['product_name'].str.contains(search, case=False,na=False)]
if category:
    filtered_df=filtered_df[filtered_df['category'].isin(category)]

filtered_df = filtered_df[(filtered_df['rating'] >= min_rating) &  (filtered_df['rating_count'] >= min_reviews)]
filtered_df = filtered_df[(filtered_df['discounted_price'] >= min_price)&(filtered_df['discounted_price'] <= max_price)]
st.write(f"Found {len(filtered_df)} products")
st.dataframe(filtered_df[['product_name','category','discounted_price','rating','rating_count']])
st.markdown("---")
# ... all your filters ...

st.write(f"Found {len(filtered_df)} products")

st.markdown("---")

st.subheader("Sort Results")
sort_by = st.selectbox("Sort by", ['product_name', 'discounted_price', 'rating', 'rating_count'])
sort_order = st.radio("Order", ['Ascending', 'Descending'])

ascending = sort_order == 'Ascending'
filtered_df_sorted = filtered_df.sort_values(sort_by, ascending=ascending)

st.subheader("Results")
st.dataframe(filtered_df_sorted[['product_name', 'category', 'discounted_price', 'rating', 'rating_count']])

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Products by Rating")
    top_10 = filtered_df.nlargest(10, 'rating')[['product_name', 'rating']]
    st.bar_chart(data=top_10.set_index('product_name')['rating'])

with col2:
    st.subheader("Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(filtered_df['discounted_price'], bins=30, color='steelblue', edgecolor='black')
    ax.set_xlabel('Price (₹)')
    ax.set_ylabel('Number of Products')
    st.pyplot(fig)