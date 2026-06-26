#!/usr/bin/env python3
"""
Generic RSS/Atom feed source for podcast topic discovery.
Works with any valid RSS or Atom feed URL.
"""
import re
import html
import urllib.request
import urllib.error
from typing import List, Dict
from datetime import datetime
from .base import TopicSource


class RSSSource(TopicSource):
    """Generic RSS feed source"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.url = config.get("url")
        if not self.url:
            raise ValueError("RSS source requires 'url' in config")
        self.category = config.get("category", "")
        
    def fetch(self) -> List[Dict]:
        """Fetch and parse RSS feed"""
        try:
            content = self._fetch_url(self.url)
            if not content:
                return []
            
            # Parse both RSS and Atom formats
            items = self._parse_feed(content)
            return [self.normalize_topic(item) for item in items]
            
        except Exception as e:
            print(f"ERROR: RSS fetch failed for {self.name}: {e}")
            return []
    
    def _fetch_url(self, url: str, timeout: int = 10) -> str:
        """Fetch URL content"""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  WARNING: Failed to fetch {url}: {e}")
            return ""
    
    def _parse_feed(self, content: str) -> List[Dict]:
        """Parse RSS/Atom XML content"""
        items = []
        
        # Extract titles - handle both CDATA and plain text
        titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', content)
        if not titles:
            titles = re.findall(r'<title>(.*?)</title>', content)
        
        # Extract links
        links = re.findall(r'<link[^>]*>(.*?)</link>', content)
        if not links:
            # Try href attribute (Atom format)
            links = re.findall(r'<link[^>]*href=["\']([^"\']+)["\']', content)
        
        # Clean up: first title/link is often the feed itself, not an item
        if titles and links:
            # Check if first link is just the homepage
            if links[0].strip().rstrip('/') == self.url.strip().rstrip('/'):
                links = links[1:]
            if titles[0].lower() in [self.name.lower(), 'feed', 'rss']:
                titles = titles[1:]
        
        # Extract descriptions (optional)
        descriptions = re.findall(r'<description><!\[CDATA\[(.*?)\]\]></description>', content)
        if not descriptions:
            descriptions = re.findall(r'<description>(.*?)</description>', content)
        
        # Pair up titles and links
        for i, title in enumerate(titles[:20]):  # Limit to 20 items
            clean_title = self._clean_html(title)
            if len(clean_title) < 10:
                continue
                
            item = {
                "title": clean_title,
                "url": links[i] if i < len(links) else "",
                "category": self.category,
                "description": self._clean_html(descriptions[i]) if i < len(descriptions) else "",
                "source": self.name,
            }
            items.append(item)
        
        return items
    
    def _clean_html(self, text: str) -> str:
        """Strip HTML tags and decode entities"""
        text = re.sub(r'<[^>]+>', '', text)
        return html.unescape(text).strip()
