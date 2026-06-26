---
name: Threads Scraper
description: |
  This skill should be used when the user asks to
  "scrape Threads posts", "get Threads data",
  "extract Threads content", "search Threads",
  "monitor Threads hashtags", "analyze Threads engagement",
  "get posts from a Threads user",
  or needs to collect data from Meta Threads.
version: 0.2.0
---

# Threads Scraper with Apify

Scrape Meta Threads posts, search by keyword or hashtag, and extract engagement metrics. No login required.

Actor: `futurizerush/meta-threads-scraper`

## Prerequisites

Set `APIFY_API_TOKEN` in environment. Get a token at [console.apify.com/account/integrations](https://console.apify.com/account/integrations?fpr=rush).

## Execution Flow

Apify runs are asynchronous. Every request follows 3 steps:

1. **Start a run** -- POST to the actor API, receive a run ID and dataset ID
2. **Poll until done** -- GET the run status, wait for `SUCCEEDED`
3. **Fetch results** -- GET the dataset items (returns a JSON array)

Typical run time: 30 seconds to 2 minutes depending on `max_posts`.

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `mode` | enum | **Yes** | `"user"` (user posts), `"keyword"` (hashtag/tag), `"search"` (full-text keyword search) |
| `usernames` | array of strings | For `user` mode | Usernames without @ (e.g. `["zuck"]`) |
| `keywords` | array of strings | For `keyword`/`search` mode | Single-word keywords or hashtags (e.g. `["AI"]`, `["fashion"]`) |
| `search_filter` | `"top"` / `"recent"` | No | Sort order. `search` mode only. Default: `"top"` |
| `max_posts` | integer | No | Max posts per user/keyword. Default: 200 |
| `start_date` | string | No | Start date (YYYY-MM-DD). `search` mode only |
| `end_date` | string | No | End date (YYYY-MM-DD). `search` mode only |

### Mode differences

- **`user`** -- Scrape a user's timeline. Requires `usernames`.
- **`keyword`** -- Search by hashtag/tag. Requires `keywords`.
- **`search`** -- Full-text keyword search with sort and date filtering. Requires `keywords`. Supports `search_filter`, `start_date`, `end_date`.

## Complete Example (Python)

```python
import requests, os, time

TOKEN = os.environ["APIFY_API_TOKEN"]
BASE = "https://api.apify.com/v2"

# Step 1: Start the run
response = requests.post(
    f"{BASE}/acts/futurizerush~meta-threads-scraper/runs?token={TOKEN}",
    json={"mode": "user", "usernames": ["futurizerush"], "max_posts": 5},
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
for post in items:
    print(f"@{post['username']}: {post['text_content'][:80]}")
    print(f"  likes={post['like_count']} replies={post['reply_count']} views={post['view_count']}")
```

### Search recent posts by keyword

```python
requests.post(
    f"{BASE}/acts/futurizerush~meta-threads-scraper/runs?token={TOKEN}",
    json={
        "mode": "search",
        "keywords": ["AI"],
        "search_filter": "recent",
        "max_posts": 10,
    },
)
```

### Search by hashtag

```python
requests.post(
    f"{BASE}/acts/futurizerush~meta-threads-scraper/runs?token={TOKEN}",
    json={"mode": "keyword", "keywords": ["automation"], "max_posts": 20},
)
```

## Complete Example (bash)

```bash
# Step 1: Start the run
RUN_RESPONSE=$(curl -s -X POST \
  "https://api.apify.com/v2/acts/futurizerush~meta-threads-scraper/runs?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mode": "user", "usernames": ["futurizerush"], "max_posts": 5}')

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
  "text_content": "Post text here...",
  "username": "lucky_dilkhush7970",
  "display_name": "Lucky Dilkhush",
  "profile_url": "https://www.threads.com/@lucky_dilkhush7970",
  "profile_pic_url": "https://scontent-iad6-1.cdninstagram.com/...",
  "is_verified": false,
  "followers_count": 11,
  "bio": "",
  "like_count": 19,
  "reply_count": 7,
  "repost_count": 0,
  "quote_count": 0,
  "share_count": 1,
  "view_count": 602,
  "post_code": "DRyBIddEjav",
  "post_url": "https://www.threads.com/@lucky_dilkhush7970/post/DRyBIddEjav",
  "created_at": "2025-12-03T00:40:19+00:00",
  "created_at_timestamp": 1764722419,
  "has_media": true,
  "media_type": "photo",
  "media_url": "https://scontent-iad6-1.cdninstagram.com/...",
  "media_urls": [],
  "hashtags": [],
  "mentions": [],
  "urls": [],
  "emails": [],
  "phones": [],
  "bio_links": [],
  "external_links": [],
  "is_pinned": false,
  "is_edited": false,
  "search_keyword": "AI",
  "scraped_at": "2026-04-11T05:24:26.152274+00:00"
}
```

**Note:** Field names use snake_case. Access with `post['like_count']` not `post['likeCount']`.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API token | Check `APIFY_API_TOKEN` |
| `FAILED`: "At least one username is required" | `mode` is `"user"` but `usernames` is missing or empty | Add `"usernames": ["name"]` |
| `FAILED`: "No posts found" | User has no public posts or Threads rate limit | Try a different user or wait and retry |

## Tips

- Use `mode: "search"` with `search_filter: "recent"` for real-time monitoring and alerting.
- Use `mode: "keyword"` for hashtag-based discovery.
- Use single-word keywords for best results (e.g. `"AI"`, `"fashion"`, `"tech"`).
- No login or session ID required.
- Results are a JSON array, not a single object.
- All field names use snake_case (e.g. `text_content`, `like_count`, `view_count`).
- For reply/comment extraction, use the separate Threads Replies Scraper actor (`futurizerush/threads-replies-scraper`).

## Links

- [Actor page](https://apify.com/futurizerush/meta-threads-scraper?fpr=rush)
- [Apify API docs](https://docs.apify.com/api/v2)
