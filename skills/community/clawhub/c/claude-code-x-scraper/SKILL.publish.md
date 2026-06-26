---
name: claude-code-x-scraper
description: X (Twitter) data extraction and analysis. Use when user asks to "get tweets from @username", "search X for", "analyze Twitter data", "fetch tweets about [topic]", or "scrape X posts". Supports user timelines, keyword search, tweet details, and social media research workflows.
---

# X (Twitter) Data Scraper

Extract and analyze X/Twitter data programmatically.

## When to Use

- Fetch tweets from a specific user
- Search X for keywords/topics
- Analyze Twitter data and sentiment
- Monitor social media trends

## Quick Start

```bash
# Get user tweets
python3 scripts/get_user_tweets.py elonmusk 20

# Search for topic
python3 scripts/search_tweets.py "machine learning" 30
```

## Setup

**Credentials:** Create `~/.openclaw/credentials/x_api_tokens.env`:
```
X_BEARER_TOKEN=Bearer YOUR_TOKEN_HERE
```

Get token: https://developer.twitter.com/en/portal/dashboard

## Scripts

| Script | Purpose |
|--------|---------|
| `get_user_tweets.py` | Fetch user timeline |
| `search_tweets.py` | Search by keyword |
| `fetch_x_playwright.py` | Browser-based scraping |
| `x_api_client.py` | API client module |

## Advanced Search

```bash
# Exclude replies/retweets
python3 scripts/get_user_tweets.py elonmusk 20 --no-replies --no-retweets

# Complex search
python3 scripts/search_tweets.py "(AI OR ML) from:elonmusk lang:en" 20
```

## Troubleshooting

- **401 Unauthorized:** Check Bearer token format
- **403 Forbidden:** Search API needs Elevated access
- **429 Rate Limited:** Wait 15 minutes

## License

MIT
