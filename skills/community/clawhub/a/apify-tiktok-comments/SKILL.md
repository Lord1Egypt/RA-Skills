---
name: TikTok Comment Scraper
description: |
  This skill should be used when the user asks to
  "scrape TikTok comments", "get TikTok post comments",
  "extract comments from a TikTok video",
  "get TikTok replies", "analyze TikTok engagement",
  or needs to collect comments and replies from TikTok posts.
version: 0.1.0
---

# TikTok Comment Scraper with Apify

Extract comments and replies from TikTok video and photo posts. Supports both top-level comments and threaded replies. No login required.

Actor: `futurizerush/tiktok-comment-scraper`

## Prerequisites

Set `APIFY_API_TOKEN` in environment. Get a token at [console.apify.com/account/integrations](https://console.apify.com/account/integrations?fpr=rush).

## Execution Flow

Apify runs are asynchronous. Every request follows 3 steps:

1. **Start a run** -- POST to the actor API, receive a run ID and dataset ID
2. **Poll until done** -- GET the run status, wait for `SUCCEEDED`
3. **Fetch results** -- GET the dataset items (returns a JSON array)

Typical run time: 15-60 seconds depending on comment count.

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `videoUrls` | array of strings | **Yes** | TikTok post URLs (video, photo, or short links). Max 50, must be unique. |
| `maxCommentsPerVideo` | integer | No | Max top-level comments per post. Default: 100. Min: 1, Max: 5000 |
| `includeReplies` | boolean | No | Collect threaded replies. Default: true |
| `maxRepliesPerComment` | integer | No | Max replies per comment. Default: 50. Min: 1, Max: 500 |

## Complete Example (Python)

```python
import requests, os, time

TOKEN = os.environ["APIFY_API_TOKEN"]
BASE = "https://api.apify.com/v2"

# Step 1: Start the run
response = requests.post(
    f"{BASE}/acts/futurizerush~tiktok-comment-scraper/runs?token={TOKEN}",
    json={
        "videoUrls": [
            "https://www.tiktok.com/@bellapoarch/video/6862153058223197445"
        ],
        "maxCommentsPerVideo": 20,
        "includeReplies": True,
        "maxRepliesPerComment": 10,
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

# Separate comments from replies
for item in items:
    prefix = "  Reply" if item["isReply"] else "Comment"
    print(f"{prefix} by @{item['username']}: {item['text'][:80]}")
    print(f"  likes={item['likeCount']} replies={item['replyCount']}")
```

### Multiple videos

```python
requests.post(
    f"{BASE}/acts/futurizerush~tiktok-comment-scraper/runs?token={TOKEN}",
    json={
        "videoUrls": [
            "https://www.tiktok.com/@bellapoarch/video/6862153058223197445",
            "https://www.tiktok.com/@charlidamelio/video/EXAMPLE123",
        ],
        "maxCommentsPerVideo": 50,
    },
)
```

## Complete Example (bash)

```bash
# Step 1: Start the run
RUN_RESPONSE=$(curl -s -X POST \
  "https://api.apify.com/v2/acts/futurizerush~tiktok-comment-scraper/runs?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"videoUrls": ["https://www.tiktok.com/@bellapoarch/video/6862153058223197445"], "maxCommentsPerVideo": 20, "includeReplies": true}')

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

### Comment item:

```json
{
  "commentId": "7604380245148189453",
  "text": "It happened, Leah Healton got more likes.",
  "createTime": "2026-02-08T06:39:49.000Z",
  "likeCount": 160671,
  "replyCount": 0,
  "isPinned": false,
  "isAuthorLiked": false,
  "userId": "7189081523688309806",
  "username": "kdarr1013",
  "nickname": "レイヴン",
  "avatarUrl": "https://p16-common-sign.tiktokcdn-us.com/...",
  "profileUrl": "https://www.tiktok.com/@kdarr1013",
  "isVerified": false,
  "parentCommentId": null,
  "isReply": false,
  "videoId": "6862153058223197445",
  "videoUrl": "https://www.tiktok.com/@bellapoarch/video/6862153058223197445",
  "collectedAt": "2026-04-11T06:07:23.985Z"
}
```

### Reply item (same fields, different values):

```json
{
  "commentId": "7192662943740297989",
  "text": "Hi! I'm from 2023",
  "parentCommentId": "6941063376386686982",
  "isReply": true,
  "likeCount": 1182,
  "replyCount": 0
}
```

**Note:** Field names use camelCase. Distinguish comments from replies using `isReply`. Replies have a non-null `parentCommentId` linking them to the parent comment.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API token | Check `APIFY_API_TOKEN` |
| `FAILED`: "post(s) appear unavailable or private" | Video is private or deleted | Verify the video URL is public |
| No results | Video has comments disabled | Try a different video |

## Tips

- Use `isReply: false` to filter top-level comments only.
- Use `parentCommentId` to reconstruct comment threads.
- Use `isPinned: true` to find creator-pinned comments.
- Use `isAuthorLiked: true` to find comments the creator liked.
- Supports video posts, photo posts, and short links (vm.tiktok.com).
- URLs must be unique (no duplicates allowed).
- No login or session ID required.

## Links

- [Actor page](https://apify.com/futurizerush/tiktok-comment-scraper?fpr=rush)
- [Apify API docs](https://docs.apify.com/api/v2)
