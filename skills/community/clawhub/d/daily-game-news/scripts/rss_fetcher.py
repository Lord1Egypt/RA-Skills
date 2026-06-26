#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS Feed Fetcher
用于抓取 RSS 订阅源的文章
"""

import sys
import json
import time
from html import unescape
import re

# 尝试导入 requests，如果失败则使用 urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    HAS_REQUESTS = False

import feedparser


def clean_html(text):
    """清理 HTML 标签"""
    if not text:
        return ''
    # 移除 HTML 标签
    clean = re.sub(r'<[^>]+>', '', text)
    # 解码 HTML 实体
    clean = unescape(clean)
    return clean.strip()


def fetch_rss(url):
    """抓取 RSS 源"""
    try:
        # 使用 requests 或 urllib 获取 RSS 内容
        if HAS_REQUESTS:
            response = requests.get(url, timeout=30, verify=False, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            rss_content = response.text
        else:
            import ssl
            context = ssl._create_unverified_context()
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, context=context, timeout=30) as f:
                rss_content = f.read().decode('utf-8')
        
        # 解析 RSS
        feed = feedparser.parse(rss_content)
        
        entries = []
        for entry in feed.entries:
            # 获取发布时间
            published = ''
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published = time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed)
                except:
                    published = entry.get('published', '')
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                try:
                    published = time.strftime('%Y-%m-%d %H:%M:%S', entry.updated_parsed)
                except:
                    published = entry.get('updated', '')
            else:
                published = entry.get('published', '') or entry.get('updated', '')
            
            entries.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': published,
                'summary': clean_html(entry.get('summary', '') or entry.get('description', ''))[:200],
                'author': entry.get('author', '')
            })
        
        return {
            'feed_title': feed.feed.get('title', ''),
            'entries': entries
        }
    except Exception as e:
        return {
            'feed_title': '',
            'entries': [],
            'error': str(e)
        }


if __name__ == '__main__':
    import time
    
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Missing URL argument'}))
        sys.exit(1)
    
    url = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'json'
    
    result = fetch_rss(url)
    
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Feed: {result['feed_title']}")
        print(f"Entries: {len(result['entries'])}")
        for entry in result['entries']:
            print(f"\n- {entry['title']}")
            print(f"  Link: {entry['link']}")
            print(f"  Published: {entry['published']}")
