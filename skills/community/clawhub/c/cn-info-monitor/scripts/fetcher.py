"""
内容采集器 - 支持RSS/网页/微信公众号链接三种采集方式
依赖: requests, feedparser (可选，RSS模式需要)
"""

import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class Article:
    def __init__(self, title, url, content, source_name, published_at=None):
        self.title = title
        self.url = url
        self.content = content
        self.source_name = source_name
        self.published_at = published_at or datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content[:500],
            "source_name": self.source_name,
            "published_at": self.published_at
        }


def fetch_rss(source_config, proxy=None):
    """采集RSS feed源
    
    Args:
        source_config: dict with 'url', 'name' keys
        proxy: optional HTTP proxy string like 'http://proxy:port'
    
    Returns:
        list[Article]
    """
    if not HAS_FEEDPARSER:
        print("[WARN] feedparser未安装，跳过RSS源: {}".format(source_config.get("name")))
        return []
    
    try:
        kwargs = {}
        if proxy:
            kwargs["request_headers"] = {"Proxy": proxy}
        
        feed = feedparser.parse(source_config["url"])
        articles = []
        for entry in feed.entries[:20]:
            content = ""
            if hasattr(entry, "content") and entry.content:
                content = entry.content[0].get("value", "")
            elif hasattr(entry, "summary"):
                content = entry.summary
            elif hasattr(entry, "description"):
                content = entry.description
            
            articles.append(Article(
                title=entry.get("title", "无标题"),
                url=entry.get("link", ""),
                content=_strip_html(content),
                source_name=source_config.get("name", "unknown"),
                published_at=entry.get("published", "")
            ))
        return articles
    except Exception as e:
        print("[ERROR] RSS采集失败 [{}]: {}".format(source_config.get("name"), e))
        return []


def fetch_webpage(source_config, proxy=None):
    """采集普通网页（提取正文）
    
    使用简单的正则提取正文内容，不需要额外依赖。
    如果有 readability 或 newspaper3k 会更好，但不强制要求。
    """
    if not HAS_REQUESTS:
        print("[WARN] requests未安装，跳过网页源: {}".format(source_config.get("name")))
        return []
    
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        resp = requests.get(
            source_config["url"],
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (compatible; InfoMonitor/1.0)"},
            proxies=proxies
        )
        resp.raise_for_status()
        html = resp.text
        
        title = _extract_title(html)
        content = _extract_content(html)
        
        if content:
            return [Article(
                title=title or source_config.get("name"),
                url=source_config["url"],
                content=content[:3000],
                source_name=source_config.get("name", "unknown")
            )]
        return []
    except Exception as e:
        print("[ERROR] 网页采集失败 [{}]: {}".format(source_config.get("name"), e))
        return []


def fetch_wechat(source_config, proxy=None):
    """采集微信公众号文章
    
    微信公众号文章URL格式: https://mp.weixin.qq.com/s/xxxxx
    需要处理反爬：建议用户使用代理或官方API模式
    """
    if not HAS_REQUESTS:
        print("[WARN] requests未安装，跳过微信源: {}".format(source_config.get("name")))
        return []
    
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        resp = requests.get(
            source_config["url"],
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
                "Referer": "https://mp.weixin.qq.com/"
            },
            proxies=proxies
        )
        resp.raise_for_status()
        html = resp.text
        
        title = _extract_title(html) or "微信文章"
        content = _extract_wechat_content(html)
        
        if content:
            return [Article(
                title=title,
                url=source_config["url"],
                content=content[:3000],
                source_name=source_config.get("name", "wechat")
            )]
        return []
    except Exception as e:
        print("[ERROR] 微信采集失败 [{}]: {} (可能需要配置代理)".format(source_config.get("name"), e))
        return []


def fetch_all(sources_config, proxy=None):
    """采集所有已启用的信息源
    
    Args:
        sources_config: list of source config dicts
        proxy: optional proxy string
    
    Returns:
        list[Article]
    """
    all_articles = []
    for source in sources_config:
        if not source.get("enabled", True):
            continue
        
        source_type = source.get("type", "rss")
        if source_type == "rss":
            articles = fetch_rss(source, proxy)
        elif source_type == "webpage":
            articles = fetch_webpage(source, proxy)
        elif source_type == "wechat":
            articles = fetch_wechat(source, proxy)
        else:
            print("[WARN] 未知类型: {}, 跳过".format(source_type))
            continue
        
        all_articles.extend(articles)
        print("[OK] [{}] 采集到 {} 篇文章".format(source.get("name"), len(articles)))
    
    return all_articles


# --- 内部工具函数 ---

def _strip_html(html):
    if not html:
        return ""
    text = re.sub(r'<[^>]+>', '', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
    return m.group(1).strip() if m else ""


def _extract_content(html):
    patterns = [
        r'<article[^>]*>(.*?)</article>',
        r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>',
    ]
    for p in patterns:
        m = re.search(p, html, re.S)
        if m:
            return _strip_html(m.group(1))
    return ""


def _extract_wechat_content(html):
    patterns = [
        r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*</div>',
        r'<div[^>]*class="[^"]*rich_media_content[^"]*"[^>]*>(.*?)</div>',
    ]
    for p in patterns:
        m = re.search(p, html, re.S)
        if m:
            return _strip_html(m.group(1))
    return _extract_content(html)


if __name__ == "__main__":
    test_sources = [
        {"name": "36氪测试", "type": "rss", "url": "https://36kr.com/feed", "enabled": True}
    ]
    articles = fetch_all(test_sources)
    for a in articles:
        print("- {}: {}".format(a.title, a.url))
