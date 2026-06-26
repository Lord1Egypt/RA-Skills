---
name: find-rss
description: Discover RSS and Atom feeds for any website. Use when the user wants to find RSS feeds, subscribe to website updates, or locate syndication feeds for news aggregation. Triggers on phrases like "find RSS", "RSS feed", "get feed URL", "subscribe to updates", or when working with news aggregation, feed readers, or content monitoring.
---

# Find RSS Skill

Discover RSS and Atom feeds for websites to enable news aggregation and content monitoring.

## Quick Start

Run the find-rss script with a website URL:

```bash
~/.openclaw/skills/find-rss/scripts/find-rss.sh <website_url>
```

Example:
```bash
~/.openclaw/skills/find-rss/scripts/find-rss.sh https://techcrunch.com/
```

## What This Skill Does

1. **Checks HTML link tags** - Searches for `<link rel="alternate" type="application/rss+xml">` tags
2. **Tests common RSS paths** - Tries standard feed locations like `/feed`, `/rss`, `/atom`
3. **Validates feeds** - Confirms discovered URLs return valid RSS/Atom content

## How It Works

The script performs two main checks:

### 1. HTML Link Tag Discovery
Most websites with RSS feeds include a link tag in their HTML:
```html
<link rel="alternate" type="application/rss+xml" href="https://example.com/feed/">
```

The script extracts all such links from the page source.

### 2. Common Path Testing
If no link tags are found, the script tests common RSS paths:
- `/feed` and `/feed/`
- `/rss` and `/rss/`
- `/atom` and `/atom/`
- `/index.xml`, `/feed.xml`, `/rss.xml`
- `/blog/feed`, `/news/feed`

## Interpreting Results

- **✅ Found in HTML**: RSS link was discovered in the page's HTML source
- **✅ Common path**: RSS feed exists at a standard location
- **❌ Not found**: No RSS feed detected (website may not offer one)

## Tips for Users

If no RSS feed is found:
1. Check the website's footer for an "RSS" or "Subscribe" link
2. Search Google for "[sitename] RSS feed"
3. Use feed discovery services like Feedly or Inoreader
4. Some sites use JSON Feeds or proprietary APIs instead of RSS

## Common RSS Feed Patterns

| Platform | Typical Feed URL |
|----------|-----------------|
| WordPress | `https://site.com/feed/` |
| Medium | `https://medium.com/feed/@username` |
| Substack | `https://newsletter.substack.com/feed` |
| Ghost | `https://site.com/rss/` |
| YouTube | `https://www.youtube.com/feeds/videos.xml?channel_id=...` |

## Limitations

- Some websites block automated requests (may return 403)
- JavaScript-rendered sites may hide RSS links
- Relative URLs are resolved but may not always be accurate
- Rate limiting may apply for multiple rapid requests
