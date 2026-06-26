import requests

# 获取科技/物流新闻
try:
    tech_news = requests.get('https://ai.6551.io/open/free_hot?category=tech', timeout=15).json()
    print(tech_news)
except Exception as e:
    print(f"Error: {e}")
