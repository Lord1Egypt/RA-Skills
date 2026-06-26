---
name: baidu-search-free
description: Free Baidu web search, no API key required, supports time range filtering
author: OpenClaw Community
version: 1.0.1
license: MIT
tags: ["search", "baidu", "free", "web-search", "chinese"]
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["python3"]
---

# Baidu Search (Free)
Free Baidu web search tool, no API key or authentication required, ready to use out of box.

## Features
✅ No API key required, completely free
✅ Supports Chinese/English search queries
✅ Time range filtering: 1 day/1 week/1 month/1 year/custom date range
✅ Customizable result count (up to 50 results)
✅ Automatic anti-scraping handling with retry mechanism
✅ Returns title, snippet, real URL, and publish time

## Usage
```bash
python scripts/search.py '{"query": "your search keywords", "count": 10, "freshness": "pd/pw/pm/py/YYYY-MM-DDtoYYYY-MM-DD"}'
```

> ⚠️ Note: If you encounter anti-scraping verification errors, this is likely due to Baidu blocking your server's IP. This is a known limitation when scraping Baidu from cloud servers. Consider using a proxy or VPN if needed.

## Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | yes | - | Search keywords |
| count | int | no | 10 | Number of results to return, max 50 |
| freshness | string | no | null | Time range filter: pd(past 24h), pw(past week), pm(past month), py(past year), or custom date range in format YYYY-MM-DDtoYYYY-MM-DD |

## Example
```bash
python scripts/search.py '{"query": "Linzhi Tibet travel guide", "count": 3, "freshness": "pm"}'
```
