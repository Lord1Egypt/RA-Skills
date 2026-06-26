#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
import requests
import re
from bs4 import BeautifulSoup
import feedparser
import argparse
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure UTF-8 output
import sys
sys.stdout.reconfigure(encoding='utf-8')


def summary_preprocessing(text):
    clean_text = re.sub(r'<[^>]+>', '', str(text))
    return clean_text


def get_vnexpress_news(url, topic, limit=10):
    now = datetime.datetime.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    hour = now.hour
    
    feed = feedparser.parse(url)
    
    # Kiểm tra xem có lấy được dữ liệu không
    if not feed.entries:
        logging.error(f"Cannot load data or wrong URL: {url}")
        return []
    
    news_list = []
    for entry in feed.entries[:limit]:
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if hasattr(entry, "published") else None,
            "summary": bs(entry.summary, 'html.parser')
        }
        news_list.append(news_item)
    
    # Format the output
    # Output show the URL of the news and its title
    # To be safe, let's explicitly mention "Current Time"
    
    greeting = f"Here are hot and trendy news for topic {topic} at {current_time_str}"
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
    #-- Parser
    parser = argparse.ArgumentParser(description='Fetch latest news from BBC')
    parser.add_argument('--count_str', type=str, default=10, help='Number of news want to retrieve per topic')
    parser.add_argument('--topics', type=str, default="tin-moi-nhat, tin-xem-nhieu", help='Topics that user want to search')
    args = parser.parse_args()

    #-- Get arguments
    rss_path_template = "https://vnexpress.net/rss/{topic}.rss"
    count_str = args.count_str
    available_topics = [
        "tin-moi-nhat",
        "the-gioi",
        "thoi-su",
        "kinh-doanh",
        "giai-tri",
        "the-thao",
        "phap-luat",
        "giao-duc",
        "tin-noi-bat",
        "suc-khoe",
        "doi-song",
        "du-lich",
        "khoa-hoc-cong-nghe",
        "oto-xe-may",
        "y-kien",
        "tam-su",
        "cuoi",
        "tin-xem-nhieu"
    ]
    topics = list(set([
        topic.strip()
        if topic.strip() in available_topics
        else "tin-moi-nhat"
        for topic in args.topics.split(",")
    ]))
    counts = [int(count) for count in count_str.split(",")]
    if len(topics) > len(counts):
        counts = counts * len(topics)

    #-- Split topic count
    all_news_information = ""
    for topic, count in zip(topics, counts):
        url = rss_path_template.format(topic=topic)
        news = get_vnexpress_news(url, topic=topic, limit=count)
        if isinstance(news, str):
            all_news_information += news + "\n"

    print(all_news_information)


