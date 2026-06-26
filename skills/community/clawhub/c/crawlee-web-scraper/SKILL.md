---
name: crawlee-web-scraper
description: Resilient web scraper with bot-detection evasion using the Crawlee library. Use when web_fetch is blocked by rate limits or bot detection. Supports single URLs, bulk file input, and automatic fallback from requests to Crawlee on 403/429 responses.
---

# crawlee-web-scraper

Drop-in replacement for `web_fetch` when sites block automated requests. Crawlee handles session management, retry logic, and bot-detection evasion automatically.

## Scripts

- **`crawlee_fetch.py`** — main scraper; accepts a single URL or a file of URLs; returns JSON
- **`crawlee_http.py`** — library helper; tries `requests` first, falls back to Crawlee on 403/429/503

## Usage

```bash
# Single URL, return HTML preview
python3 scripts/crawlee_fetch.py --url "https://example.com"

# Single URL, extract text (strips HTML tags)
python3 scripts/crawlee_fetch.py --url "https://example.com" --extract-text

# Bulk scrape from file
python3 scripts/crawlee_fetch.py --urls-file urls.txt --output results.json
```

### Library usage

```python
from crawlee_http import fetch_with_fallback

resp = fetch_with_fallback("https://example.com")
print(resp.status_code, resp.text[:500])
```

## Output

JSON array with one object per URL:

```json
[
  {
    "url": "https://example.com",
    "status": 200,
    "fetched_at": "2026-01-01T00:00:00Z",
    "length": 12345,
    "text": "Page content..."
  }
]
```

## Installation

```bash
pip install crawlee requests
```

## When to use

- `web_fetch` returns 403 / 429 / empty
- Bulk scraping 10+ URLs
- Sites using Cloudflare or similar bot protection
