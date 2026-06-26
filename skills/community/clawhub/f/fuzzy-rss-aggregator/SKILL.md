---
name: rss-aggregator
description: "Monitor, filter, and summarize RSS/Atom feeds on a schedule. Use when: (1) tracking industry news or competitor blogs, (2) setting up keyword alerts across multiple feeds, (3) getting daily/periodic digest of new articles, (4) routing interesting articles to Discord/email/webhook, (5) building a personal news pipeline. Triggers on: rss feed, atom, feed monitor, news aggregator, track this blog, keyword alert, feed digest, subscribe to feed, monitor this site."
---

# RSS Aggregator

Monitor RSS/Atom feeds on a schedule, filter by keywords or date, and route summaries to your preferred channel.

## Setup

Requires the `feedparser` Python package:

```bash
pip install feedparser
```

## Core Script

Save as `scripts/fetch_feeds.py`:

```python
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
```

## Recipes

### Recipe 1: Daily News Digest

```json
cron_add(
  name="Tech news digest",
  schedule={"kind": "cron", "expr": "0 8 * * 1-5", "tz": "Africa/Johannesburg"},
  payload={
    "kind": "agentTurn",
    "message": "Run: python scripts/fetch_feeds.py https://news.ycombinator.com/rss 7. Then summarize the top 5 stories as a clean bullet list with titles and links."
  },
  delivery={"mode": "announce"},
  sessionTarget="isolated"
)
```

### Recipe 2: Multi-Feed Monitoring

```json
// First, create scripts/multi_fetch.py:
"""
import feedparser, json, sys
from scripts.fetch_feeds import fetch_feed

feeds = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.feedburner.com/TechCrunch/"
]

results = [fetch_feed(url, max_age_days=1) for url in feeds]
print(json.dumps(results, indent=2))
"""
```

Then schedule:
```json
cron_add(
  name="Industry pulse",
  schedule={"kind": "cron", "expr": "0 */6 * * *", "tz": "UTC"},
  payload={
    "kind": "agentTurn",
    "message": "Run: python scripts/multi_fetch.py. Filter entries from last 6 hours. Post new articles to #news channel on Discord with title + link."
  },
  delivery={"mode": "announce"},
  sessionTarget="isolated"
)
```

### Recipe 3: Keyword Alert

```json
cron_add(
  name="AI keyword alert",
  schedule={"kind": "cron", "expr": "0 */4 * * *", "tz": "UTC"},
  payload={
    "kind": "agentTurn",
    "message": "Run: python scripts/fetch_feeds.py https://feeds.feedburner.com/venturebeat/Settings 1 \"AI OR machine learning OR LLM\". If results have entries, format as: **Alert** [Article Title](URL). Send to Discord #alerts channel."
  },
  delivery={"mode": "webhook", "to": "https://discord.com/api/webhooks/..."},
  sessionTarget="isolated"
)
```

### Recipe 4: Feed Status Health Check

```json
cron_add(
  name="Feed health check",
  schedule={"kind": "cron", "expr": "0 9 * * *", "tz": "UTC"},
  payload={
    "kind": "agentTurn",
    "message": "Check if these feeds are still live: Hacker News (https://news.ycombinator.com/rss), TechCrunch (https://techcrunch.com/feed/). Run fetch without filters. If any feed returns 0 entries or error, alert via webhook."
  },
  delivery={"mode": "announce"},
  sessionTarget="isolated",
  failureAlert={"after": 3, "mode": "announce", "cooldownMs": 86400000}
)
```

### Recipe 5: Feed to Read Later (Notion)

```json
cron_add(
  name="RSS to Notion",
  schedule={"kind": "cron", "expr": "0 7 * * *", "tz": "Africa/Johannesburg"},
  payload={
    "kind": "agentTurn",
    "message": "Run: python scripts/fetch_feeds.py https://example.com/rss 1. Create Notion page for each entry in your Reading List database with title, link, and summary as page content."
  },
  delivery={"mode": "none"},
  sessionTarget="isolated"
)
```

## Managing Feeds

```bash
# Test a feed directly
python scripts/fetch_feeds.py <feed-url> [max-age-days] [keyword-filter]

# Example
python scripts/fetch_feeds.py https://news.ycombinator.com/rss 7
python scripts/fetch_feeds.py https://techcrunch.com/feed/ 1 "AI"
```

## Feed Discovery

Find RSS feeds on any website by:
- Adding `/feed` or `/rss` to the URL
- Checking the page source for `<link rel="alternate" type="application/rss+xml">`
- Using `site:rss` search on Google

Common feed URLs:
- YouTube: `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID`
- Twitter/X: No native RSS — use替他 (Nitter for Twitter lists)
- Reddit: `https://www.reddit.com/r/SUBREDDIT.rss` (requires auth for full content)

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Empty entries list | Feed may require auth or be XML-only | Try curl to inspect raw feed |
| `decode error` in feed | Malformed encoding | Add `, encoding='utf-8'` to `feedparser.parse()` |
| Unicode errors | Non-UTF8 characters | Add `, response_encoding='utf-8'` to parse call |
| Old entries only | `max_age_days` too restrictive | Increase or remove the filter |
| Missing summaries | Site blocks feed scrapers | Use `e.get('content', [{}])[0].get('value', '')` for full content |

## See Also

- `fuzzy-cron-scheduler` skill — scheduling recurring feed checks
- `notion-integration` skill — storing articles in Notion
- `discord` skill — routing articles to Discord channels
- `webhook-automation` skill — HTTP delivery to any endpoint