#!/usr/bin/env python3
"""东方财富秒想新闻搜索"""
import requests
import json
import sys

API_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"
API_KEY = "mkt_o2fBS-Dkbt11c7vSNnlXjESgfybI8EXzzzX2XkOQVuE"

def search_news(query, size=10):
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY
    }
    data = {
        "query": query,
        "variables": 0,
        "size": size
    }
    
    resp = requests.post(API_URL, headers=headers, json=data, timeout=30)
    result = resp.json()
    
    if result.get("status") != 0:
        return {"error": result.get("message", "API Error")}
    
    articles = result.get("data", {}).get("data", [])
    return [{"title": a.get("title", ""),
             "content": a.get("content", "")[:200],
             "source": a.get("source", ""),
             "date": a.get("date", "")} for a in articles]

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "今日A股市场"
    news = search_news(query)
    print(json.dumps(news, ensure_ascii=False, indent=2))
