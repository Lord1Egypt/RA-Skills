#!/usr/bin/env python3
"""Fetch recent AI news articles.
Returns JSON list to stdout: [{"title":..., "link":..., "source":..., "date":...}]
Uses a hard‑coded list of RSS feeds; for production replace with proper API.
"""
import sys, json, datetime, feedparser, os

# RSS sources (public)
RSS_FEEDS = [
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/ai/rss/index.xml",  # The Verge AI 专题
    "https://syncedreview.com/feed/",
    "https://www.jiqizhixin.com/rss",  # 机器之心中文 AI 新闻
    "https://www.ithome.com/rss",       # IT 之家科技资讯（部分 AI）
]

# Only keep items from last 24h
now = datetime.datetime.utcnow()
cutoff = now - datetime.timedelta(days=1)

articles = []
for url in RSS_FEEDS:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # parse date
            if hasattr(entry, 'published_parsed'):
                entry_dt = datetime.datetime(*entry.published_parsed[:6])
            else:
                continue
            if entry_dt < cutoff:
                continue
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "source": feed.feed.get('title', 'Unknown'),
                "date": entry_dt.isoformat() + 'Z',
            })
    except Exception as e:
        sys.stderr.write(f"Failed to parse {url}: {e}\n")

# limit to 5 newest
articles = sorted(articles, key=lambda x: x['date'], reverse=True)[:5]
print(json.dumps(articles, ensure_ascii=False, indent=2))
