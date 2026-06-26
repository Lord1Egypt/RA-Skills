#!/usr/bin/env python3
"""RSS/Atom feed fetcher with filtering and summarization."""
import feedparser
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

def parse_date(entry):
    """Extract publication date from entry."""
    for field in ('published_parsed', 'updated_parsed', 'created_parsed'):
        if hasattr(entry, field) and entry.get(field):
            return datetime(*entry[field][:6])
    return None

def fetch_feed(url, max_age_days=None, keyword_filter=None):
    """Fetch and filter feed entries."""
    feed = feedparser.parse(url)
    entries = feed.entries

    # Filter by age
    if max_age_days:
        cutoff = datetime.now() - timedelta(days=max_age_days)
        entries = [e for e in entries if parse_date(e) and parse_date(e) >= cutoff]

    # Filter by keyword
    if keyword_filter:
        kw_lower = keyword_filter.lower()
        entries = [e for e in entries if kw_lower in (e.get('title', '') + e.get('summary', '')).lower()]

    return {
        'title': feed.feed.get('title', url),
        'url': url,
        'entries': [
            {
                'title': e.get('title', 'No title'),
                'link': e.get('link', ''),
                'published': parse_date(e).isoformat() if parse_date(e) else None,
                'summary': e.get('summary', e.get('description', ''))[:500]
            }
            for e in entries
        ]
    }

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    max_age = int(sys.argv[2]) if len(sys.argv) > 2 else None
    keyword = sys.argv[3] if len(sys.argv) > 3 else None

    if not url:
        print(json.dumps({'error': 'URL required'}))
        sys.exit(1)

    result = fetch_feed(url, max_age, keyword)
    print(json.dumps(result, indent=2))