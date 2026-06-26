---
name: Google News Scraper
description: |
  This skill should be used when the user asks to
  "scrape Google News", "get news articles",
  "search for news", "extract news data",
  "monitor news topics", "get latest headlines",
  or needs to collect news articles from Google News.
version: 0.1.0
---

# Google News Scraper with Apify

Search and extract news articles from Google News with full article content, enriched descriptions, and metadata. Supports region and language filtering.

Actor: `futurizerush/google-news-scraper`

## Prerequisites

Set `APIFY_API_TOKEN` in environment. Get a token at [console.apify.com/account/integrations](https://console.apify.com/account/integrations?fpr=rush).

## Execution Flow

Apify runs are asynchronous. Every request follows 3 steps:

1. **Start a run** -- POST to the actor API, receive a run ID and dataset ID
2. **Poll until done** -- GET the run status, wait for `SUCCEEDED`
3. **Fetch results** -- GET the dataset items (returns a JSON array)

Typical run time: 30-90 seconds depending on query count and article enrichment.

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `searchQueries` | array of strings | **Yes** | Search queries (e.g. `["AI"]`, `["climate change"]`) |
| `region` | string | No | Region code. Default: `"us"`. Examples: `"us"`, `"tw"`, `"jp"` |
| `language` | string | No | Language code. Default: `"en"`. Examples: `"en"`, `"zh-TW"`, `"ja"` |
| `dateFilter` | string | No | Time range: `"1h"`, `"1d"`, `"1w"`, `"1m"`, or `""` (any time). Default: `""` |
| `maxResults` | integer | No | Max articles per query. Default: 20. Min: 10 |

## Complete Example (Python)

```python
import requests, os, time

TOKEN = os.environ["APIFY_API_TOKEN"]
BASE = "https://api.apify.com/v2"

# Step 1: Start the run
response = requests.post(
    f"{BASE}/acts/futurizerush~google-news-scraper/runs?token={TOKEN}",
    json={
        "searchQueries": ["AI"],
        "region": "us",
        "language": "en",
        "dateFilter": "1d",
        "maxResults": 10,
    },
)
response.raise_for_status()
run = response.json()["data"]
run_id = run["id"]
dataset_id = run["defaultDatasetId"]

# Step 2: Poll until done
while True:
    status = requests.get(
        f"{BASE}/actor-runs/{run_id}?token={TOKEN}"
    ).json()["data"]["status"]
    if status == "SUCCEEDED":
        break
    if status in ("FAILED", "ABORTED", "TIMED-OUT"):
        raise RuntimeError(f"Run failed: {status}")
    time.sleep(5)

# Step 3: Fetch results (JSON array)
items = requests.get(
    f"{BASE}/datasets/{dataset_id}/items?token={TOKEN}"
).json()
for article in items:
    print(f"[{article['source']}] {article['title']}")
    print(f"  URL: {article['articleUrl']}")
    print(f"  Published: {article['pubDate']}")
    if article.get("enrichedDescription"):
        print(f"  Summary: {article['enrichedDescription'][:100]}")
```

### Taiwan news in Chinese

```python
requests.post(
    f"{BASE}/acts/futurizerush~google-news-scraper/runs?token={TOKEN}",
    json={
        "searchQueries": ["台灣"],
        "region": "tw",
        "language": "zh-TW",
        "dateFilter": "1d",
        "maxResults": 10,
    },
)
```

### Multiple queries

```python
requests.post(
    f"{BASE}/acts/futurizerush~google-news-scraper/runs?token={TOKEN}",
    json={
        "searchQueries": ["AI", "climate", "crypto"],
        "region": "us",
        "dateFilter": "1w",
        "maxResults": 10,
    },
)
```

## Complete Example (bash)

```bash
# Step 1: Start the run
RUN_RESPONSE=$(curl -s -X POST \
  "https://api.apify.com/v2/acts/futurizerush~google-news-scraper/runs?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchQueries": ["AI"], "region": "us", "language": "en", "dateFilter": "1d", "maxResults": 10}')

RUN_ID=$(echo "$RUN_RESPONSE" | jq -r '.data.id')
DATASET_ID=$(echo "$RUN_RESPONSE" | jq -r '.data.defaultDatasetId')

# Step 2: Poll until done
while true; do
  STATUS=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_API_TOKEN" \
    | jq -r '.data.status')
  [ "$STATUS" = "SUCCEEDED" ] && break
  [ "$STATUS" = "FAILED" ] || [ "$STATUS" = "ABORTED" ] && echo "Failed: $STATUS" && exit 1
  sleep 5
done

# Step 3: Fetch results
curl -s "https://api.apify.com/v2/datasets/$DATASET_ID/items?token=$APIFY_API_TOKEN" | jq '.'
```

## Output Format

Each item in the results array (field names verified from real API output on 2026-04-11):

```json
{
  "title": "Vance, Bessent questioned tech giants on AI security...",
  "articleUrl": "https://www.cnbc.com/2026/04/10/...",
  "googleNewsUrl": "https://news.google.com/rss/articles/...",
  "pubDate": "Fri, 10 Apr 2026 20:06:08 GMT",
  "timestamp": "2026-04-10T20:06:08.000Z",
  "source": "CNBC",
  "websiteName": "CNBC",
  "websiteUrl": "https://www.cnbc.com",
  "imageUrl": "https://image.cnbcfm.com/...",
  "description": "Raw RSS description with related headlines...",
  "enrichedDescription": "Bessent and Fed Chair Jerome Powell separately met with...",
  "excerpt": "Bessent and Fed Chair Jerome Powell separately met with...",
  "articleContent": {
    "content": "Full article text (truncated to ~2000 chars)...",
    "characterCount": 2000,
    "tokenCount": 325
  },
  "enrichmentTime": 9848,
  "guid": "unique-article-id",
  "searchQuery": "AI",
  "region": "us",
  "language": "en",
  "scrapedAt": "2026-04-11T06:06:59.618Z"
}
```

**Note:** Field names use camelCase. The `articleContent` object contains the full article text (up to ~2000 characters), character count, and token count. Use `enrichedDescription` or `excerpt` for summaries.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API token | Check `APIFY_API_TOKEN` |
| `invalid-input`: "must be >= 10" | `maxResults` below minimum | Set `maxResults` to at least 10 |
| No results | Query too specific or region has no news | Broaden the query or try a different region |

## Tips

- Use `dateFilter: "1h"` for real-time news monitoring and alerting.
- Use `dateFilter: "1d"` for daily news digests.
- `articleContent.content` provides the full article text (up to ~2000 chars) -- useful for summarization.
- `enrichedDescription` is a cleaner summary than `description` (which contains raw RSS data with related headlines).
- `timestamp` is ISO 8601 format, easier to parse than `pubDate`.
- Multiple search queries run in a single actor execution.
- No login or API key for Google News required.

## Links

- [Actor page](https://apify.com/futurizerush/google-news-scraper?fpr=rush)
- [Apify API docs](https://docs.apify.com/api/v2)
