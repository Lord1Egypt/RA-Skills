import sys
import requests
from bs4 import BeautifulSoup
import feedparser
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')


def get_bbc_news(url, limit=10):
    now = datetime.datetime.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    hour = now.hour
    
    feed = feedparser.parse(url)
    
    # Kiểm tra xem có lấy được dữ liệu không
    if not feed.entries:
        logging.error("Không thể lấy dữ liệu hoặc URL sai.")
        return []
    
    logging.info(f"--- Đang lấy {limit} tin mới nhất từ: {feed.feed.title} ---\n")

    news_list = []
    for entry in feed.entries[:limit]:
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if hasattr(entry, "published") else None,
            "summary": entry.summary if 'summary' in entry else "Không có tóm tắt"
        }
        news_list.append(news_item)
    
    # Format the output
    # Output show the URL of the news and its title
    # To be safe, let's explicitly mention "Current Time"
    
    greeting = f"Here are hot and trendy news at {current_time_str}"
    news_info = ""
    for i, news_item in enumerate(news_list, 1):
        item_string = f"""{{
            'title': {news_item['title']}, 
            'link': {news_item['link']}, 
            'summary': {news_item['summary']}, 
            'published': {news_item['published']} 
        }} \n"""
        news_info += item_string
        
    return f"{greeting}\n{news_info}"

if __name__ == "__main__":
    url = "https://feeds.bbci.co.uk/vietnamese/rss.xml"
    print(get_bbc_news(url))


