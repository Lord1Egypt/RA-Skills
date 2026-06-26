#!/usr/bin/env python3
"""
News Fetcher - RSS/Atom feed aggregator for Newsman skill.

Usage:
    python fetch_news.py [options]

Options:
    --source NAME       Fetch specific source only
    --category CAT      Filter by category (tech, finance, world, science, sports)
    --search QUERY      Search for keywords in title/description
    --hours N           Only fetch items published within last N hours
    --max-items N       Max items per source (default: 10)
    --output FILE       Output JSON file (default: stdout)
    --cache-dir DIR     Cache directory (default: ./.cache/newsman)
    --no-cache          Disable caching
    --verbose, -v       Verbose output
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

# Try to import feedparser, fallback to simple XML parsing
try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False
    import xml.etree.ElementTree as ET

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse various date formats to datetime."""
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",  # RFC 2822
        "%Y-%m-%dT%H:%M:%S%z",       # ISO 8601
        "%Y-%m-%dT%H:%M:%SZ",        # ISO 8601 UTC
        "%Y-%m-%d %H:%M:%S",         # Simple format
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


def fetch_feed_requests(url: str, timeout: int = 30) -> str:
    """Fetch feed content using requests."""
    headers = {
        'User-Agent': 'Newsman/1.0 (OpenClaw News Aggregator)'
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def fetch_feed_urllib(url: str, timeout: int = 30) -> str:
    """Fetch feed content using urllib."""
    headers = {
        'User-Agent': 'Newsman/1.0 (OpenClaw News Aggregator)'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode('utf-8')


def fetch_feed(url: str) -> str:
    """Fetch feed content with fallback methods."""
    if HAS_REQUESTS:
        return fetch_feed_requests(url)
    return fetch_feed_urllib(url)


def parse_feed_feedparser(content: str) -> List[Dict]:
    """Parse feed using feedparser."""
    feed = feedparser.parse(content)
    items = []
    
    for entry in feed.entries:
        item = {
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'summary': entry.get('summary', entry.get('description', '')),
            'published': entry.get('published', entry.get('updated', '')),
            'author': entry.get('author', ''),
        }
        items.append(item)
    
    return items


def parse_feed_xml(content: str) -> List[Dict]:
    """Parse RSS/Atom feed using ElementTree."""
    items = []
    
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        return items
    
    # Determine feed type
    if root.tag == 'rss' or root.tag.endswith('rss'):
        channel = root.find('.//channel')
        if channel is None:
            return items
        entries = channel.findall('item')
    else:  # Atom
        entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        if not entries:
            entries = root.findall('.//entry')
    
    for entry in entries:
        item = {}
        
        title_elem = entry.find('title')
        item['title'] = title_elem.text if title_elem is not None else ''
        
        link_elem = entry.find('link')
        if link_elem is not None:
            item['link'] = link_elem.get('href', link_elem.text or '')
        else:
            item['link'] = ''
        
        desc_elem = entry.find('description')
        if desc_elem is None:
            desc_elem = entry.find('summary')
        item['summary'] = desc_elem.text if desc_elem is not None else ''
        
        date_elem = entry.find('pubDate')
        if date_elem is None:
            date_elem = entry.find('published')
        if date_elem is None:
            date_elem = entry.find('updated')
        item['published'] = date_elem.text if date_elem is not None else ''
        
        author_elem = entry.find('author')
        if author_elem is None:
            author_elem = entry.find('name')
        item['author'] = author_elem.text if author_elem is not None else ''
        
        items.append(item)
    
    return items


def parse_feed(content: str) -> List[Dict]:
    """Parse feed with fallback methods."""
    if HAS_FEEDPARSER:
        return parse_feed_feedparser(content)
    return parse_feed_xml(content)


def get_default_sources() -> List[Dict]:
    """Get default news sources."""
    return [
        {'name': 'techcrunch', 'url': 'https://techcrunch.com/feed/', 'category': 'tech', 'language': 'en'},
        {'name': 'the-verge', 'url': 'https://www.theverge.com/rss/index.xml', 'category': 'tech', 'language': 'en'},
        {'name': 'ars-technica', 'url': 'http://feeds.arstechnica.com/arstechnica/index', 'category': 'tech', 'language': 'en'},
        {'name': 'bbc-tech', 'url': 'http://feeds.bbci.co.uk/news/technology/rss.xml', 'category': 'tech', 'language': 'en'},
        {'name': 'bbc-world', 'url': 'http://feeds.bbci.co.uk/news/world/rss.xml', 'category': 'world', 'language': 'en'},
        {'name': 'scientific-american', 'url': 'https://www.scientificamerican.com/rss/news.cfm', 'category': 'science', 'language': 'en'},
        {'name': 'espn', 'url': 'https://www.espn.com/espn/rss/news', 'category': 'sports', 'language': 'en'},
    ]


def load_cache(cache_file: Path) -> List[Dict]:
    """Load cached news items."""
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_cache(cache_file: Path, items: List[Dict]):
    """Save news items to cache."""
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def clean_html(html: str) -> str:
    """Remove HTML tags from text."""
    # Simple HTML tag removal
    clean = re.sub(r'<[^>]+>', '', html)
    # Decode common HTML entities
    clean = clean.replace('&nbsp;', ' ')
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&lt;', '<')
    clean = clean.replace('&gt;', '>')
    clean = clean.replace('&quot;', '"')
    return clean.strip()


def main():
    parser = argparse.ArgumentParser(description='Fetch news from RSS/Atom feeds')
    parser.add_argument('--source', help='Fetch specific source only')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--search', help='Search for keywords')
    parser.add_argument('--hours', type=int, help='Only items from last N hours')
    parser.add_argument('--max-items', type=int, default=10, help='Max items per source')
    parser.add_argument('--output', help='Output JSON file (default: stdout)')
    parser.add_argument('--cache-dir', default='./.cache/newsman', help='Cache directory')
    parser.add_argument('--no-cache', action='store_true', help='Disable caching')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Setup cache
    cache_file = None
    if not args.no_cache:
        cache_path = Path(args.cache_dir)
        cache_file = cache_path / 'fetched_news.json'
    
    # Load cached items
    cached_items = []
    if cache_file:
        cached_items = load_cache(cache_file)
    
    # Get sources
    sources = get_default_sources()
    
    if args.source:
        sources = [s for s in sources if s['name'] == args.source]
        if not sources:
            print(f"Source not found: {args.source}", file=sys.stderr)
            sys.exit(1)
    
    if args.category:
        sources = [s for s in sources if s['category'] == args.category]
    
    all_items = []
    cutoff_time = None
    if args.hours:
        cutoff_time = datetime.now() - timedelta(hours=args.hours)
    
    # Fetch from each source
    for source in sources:
        if args.verbose:
            print(f"Fetching: {source['name']} ({source['url']})", file=sys.stderr)
        
        try:
            content = fetch_feed(source['url'])
            items = parse_feed(content)
            
            # Add metadata
            for item in items[:args.max_items]:
                item['source'] = source['name']
                item['category'] = source['category']
                item['language'] = source.get('language', 'en')
                item['fetched_at'] = datetime.now().isoformat()
                
                # Clean HTML in summary
                if item.get('summary'):
                    item['summary'] = clean_html(item['summary'])
                
                # Check time filter
                if cutoff_time and item.get('published'):
                    pub_date = parse_date(item['published'])
                    if pub_date and pub_date < cutoff_time:
                        continue
                
                # Check search filter
                if args.search:
                    search_lower = args.search.lower()
                    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
                    if search_lower not in text:
                        continue
                
                all_items.append(item)
            
            if args.verbose:
                print(f"  -> Got {len(items[:args.max_items])} items", file=sys.stderr)
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            if args.verbose:
                print(f"  -> Error: {e}", file=sys.stderr)
            continue
    
    # Merge with cache (deduplicate by link)
    seen_links = {item['link'] for item in all_items}
    for cached in cached_items:
        if cached['link'] not in seen_links:
            all_items.append(cached)
            seen_links.add(cached['link'])
    
    # Sort by published date (newest first)
    all_items.sort(key=lambda x: x.get('published', ''), reverse=True)
    
    # Save cache
    if cache_file:
        save_cache(cache_file, all_items)
    
    # Output
    output = {
        'fetched_at': datetime.now().isoformat(),
        'total_items': len(all_items),
        'sources': len(sources),
        'items': all_items
    }
    
    json_output = json.dumps(output, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        if args.verbose:
            print(f"Output written to: {args.output}", file=sys.stderr)
    else:
        print(json_output)


if __name__ == '__main__':
    main()
