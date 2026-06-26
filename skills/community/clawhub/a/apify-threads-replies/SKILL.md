---
name: Threads Replies Scraper
description: |
  This skill should be used when the user asks to
  "scrape Threads replies", "get Threads comments",
  "extract replies from a Threads post",
  "get comments on a Threads post",
  "analyze Threads conversations",
  or needs to collect replies/comments from Meta Threads posts.
version: 0.1.0
---

# Threads Replies Scraper with Apify

Extract replies and comments from public Threads posts. Each post typically yields ~20 replies. No login required.

Actor: `futurizerush/threads-replies-scraper`

## Prerequisites

Set `APIFY_API_TOKEN` in environment. Get a token at [console.apify.com/account/integrations](https://console.apify.com/account/integrations?fpr=rush).

## Execution Flow

Apify runs are asynchronous. Every request follows 3 steps:

1. **Start a run** -- POST to the actor API, receive a run ID and dataset ID
2. **Poll until done** -- GET the run status, wait for `SUCCEEDED`
3. **Fetch results** -- GET the dataset items (returns a JSON array)

Typical run time: 10-30 seconds per post.

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `post_urls` | array of objects | **Yes** | Post URLs in `[{"url": "..."}]` format (requestListSources) |
| `max_replies` | integer | No | Max replies per post. Default: 50. Min: 10, Max: 50 |

**Important:** `post_urls` uses requestListSources format. Each item must be an object with a `url` key, not a plain string.

## Complete Example (Python)

```python
import requests, os, time

TOKEN = os.environ["APIFY_API_TOKEN"]
BASE = "https://api.apify.com/v2"

# Step 1: Start the run
response = requests.post(
    f"{BASE}/acts/futurizerush~threads-replies-scraper/runs?token={TOKEN}",
    json={
        "post_urls": [
            {"url": "https://www.threads.com/@zuck/post/DIffiWcJnob"}
        ],
        "max_replies": 20,
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

# Separate original post from replies
for item in items:
    if item["item_type"] == "original_post":
        print(f"Original post by @{item['author_username']}: {item['text_content'][:80]}")
        print(f"  likes={item['like_count']} replies={item['reply_count']} views={item['view_count']}")
    else:
        print(f"  Reply by @{item['author_username']}: {item['text_content'][:80]}")
        print(f"    likes={item['like_count']}")
```

### Multiple posts

```python
requests.post(
    f"{BASE}/acts/futurizerush~threads-replies-scraper/runs?token={TOKEN}",
    json={
        "post_urls": [
            {"url": "https://www.threads.com/@zuck/post/DIffiWcJnob"},
            {"url": "https://www.threads.com/@mosseri/post/EXAMPLE123"},
        ],
        "max_replies": 50,
    },
)
```

## Complete Example (bash)

```bash
# Step 1: Start the run
RUN_RESPONSE=$(curl -s -X POST \
  "https://api.apify.com/v2/acts/futurizerush~threads-replies-scraper/runs?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"post_urls": [{"url": "https://www.threads.com/@zuck/post/DIffiWcJnob"}], "max_replies": 20}')

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

Results include two item types: `original_post` and `reply`.

### Original post item (field names verified from real API output on 2026-04-11):

```json
{
  "post_code": "DS3sTIYAFaj",
  "post_url": "https://www.threads.com/@futurizerush/post/DS3sTIYAFaj",
  "author_username": "futurizerush",
  "author_display_name": "Rush in the loop｜AI 自動化",
  "author_is_verified": false,
  "author_profile_pic_url": "https://scontent-iad3-2.cdninstagram.com/...",
  "author_profile_url": "https://www.threads.com/@futurizerush",
  "text_content": "Post text here...",
  "like_count": 529,
  "reply_count": 10,
  "repost_count": 24,
  "quote_count": 0,
  "view_count": 42507,
  "created_at": "2025-12-30T02:05:14.000Z",
  "scraped_at": "2026-04-11T06:07:37.970849Z",
  "item_type": "original_post",
  "source_post_url": "https://www.threads.com/@futurizerush/post/DS3sTIYAFaj"
}
```

### Reply item (additional fields):

```json
{
  "reply_id": "DS3sVeegK8h",
  "author_username": "futurizerush",
  "author_display_name": "Rush in the loop｜AI 自動化",
  "author_is_verified": false,
  "author_profile_pic_url": "https://scontent-iad3-2.cdninstagram.com/...",
  "author_profile_url": "https://www.threads.com/@futurizerush",
  "text_content": "Reply text here...",
  "created_at": "2025-12-30T02:05:35.000Z",
  "created_at_timestamp": 1767060335,
  "like_count": 14,
  "reply_count": 0,
  "repost_count": 1,
  "quote_count": 0,
  "is_liked_by_author": false,
  "reply_to_username": "futurizerush",
  "media_type": 1,
  "has_audio": false,
  "mentions": [],
  "hashtags": [],
  "reply_url": "https://www.threads.com/@futurizerush/post/DS3sVeegK8h",
  "scraped_at": "2026-04-11T06:07:40.030190Z",
  "item_type": "reply",
  "source_post_url": "https://www.threads.com/@futurizerush/post/DS3sTIYAFaj"
}
```

**Note:** All field names use snake_case. Distinguish between `original_post` and `reply` using the `item_type` field. Reply items have extra fields: `reply_id`, `reply_to_username`, `is_liked_by_author`, `reply_url`, `has_audio`, `media_type`, `mentions`, `hashtags`.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API token | Check `APIFY_API_TOKEN` |
| `invalid-input`: "do not contain valid URLs" | Wrong URL format -- must use `[{"url": "..."}]` not `["..."]` | Use requestListSources format |
| `invalid-input`: "must be >= 10" | `max_replies` below minimum | Set `max_replies` to at least 10 |
| `FAILED`: "post(s) appear unavailable or private" | Post doesn't exist or is private | Verify the post URL is public |

## Tips

- Results include the original post as the first item (`item_type: "original_post"`), followed by replies (`item_type: "reply"`).
- Use `reply_to_username` to identify who the reply is directed at.
- Use `is_liked_by_author` to find replies the post author engaged with.
- `source_post_url` links each reply back to its parent post (useful when scraping multiple posts).
- Threads typically provides ~20 replies per post.
- No login or session ID required.
- All field names use snake_case (e.g. `text_content`, `like_count`, `reply_count`).

## Related Skills

- For scraping a user's timeline or searching posts by keyword, use the [Threads Scraper](../threads-scraper/) actor (`futurizerush/meta-threads-scraper`).

## Links

- [Actor page](https://apify.com/futurizerush/threads-replies-scraper?fpr=rush)
- [Apify API docs](https://docs.apify.com/api/v2)
