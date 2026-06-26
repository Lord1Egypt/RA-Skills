---
name: YouTube Email Scraper
description: |
  This skill should be used when the user asks to
  "find YouTube channel emails", "scrape YouTube contacts",
  "get YouTuber email addresses", "extract YouTube channel info",
  "find influencer emails", "search YouTube channels",
  or needs to collect contact information from YouTube channels.
version: 0.1.0
---

# YouTube Email Scraper with Apify

Find email addresses and contact information from YouTube channels. Search by keyword or provide channel URLs directly. Useful for influencer outreach, sponsorship, and lead generation.

Actor: `futurizerush/youtube-email-scraper`

## Prerequisites

Set `APIFY_API_TOKEN` in environment. Get a token at [console.apify.com/account/integrations](https://console.apify.com/account/integrations?fpr=rush).

## Execution Flow

Apify runs are asynchronous. Every request follows 3 steps:

1. **Start a run** -- POST to the actor API, receive a run ID and dataset ID
2. **Poll until done** -- GET the run status, wait for `SUCCEEDED`
3. **Fetch results** -- GET the dataset items (returns a JSON array)

Typical run time: 30-120 seconds depending on channel count.

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `inputMode` | string | **Yes** | `"directUrls"` or `"keywordSearch"` |
| `channelUrls` | array of strings | For `directUrls` mode | YouTube channel URLs |
| `searchKeywords` | array of strings | For `keywordSearch` mode | Keywords to search channels |
| `maxChannelsPerKeyword` | integer | No | Max channels per keyword. Default: 50 |
| `maxResults` | integer | No | Max total results. Default: 100 |
| `locale` | string | No | Locale for search. Default: `"US"` |

### Mode differences

- **`directUrls`** -- Scrape specific channels. Requires `channelUrls`.
- **`keywordSearch`** -- Find channels by keyword, then extract contacts. Requires `searchKeywords`.

## Complete Example (Python)

```python
import requests, os, time

TOKEN = os.environ["APIFY_API_TOKEN"]
BASE = "https://api.apify.com/v2"

# Step 1: Start the run
response = requests.post(
    f"{BASE}/acts/futurizerush~youtube-email-scraper/runs?token={TOKEN}",
    json={
        "inputMode": "keywordSearch",
        "searchKeywords": ["AI automation"],
        "maxChannelsPerKeyword": 10,
        "maxResults": 10,
        "locale": "US",
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

# Filter channels with emails
for channel in items:
    if channel["hasEmails"]:
        print(f"{channel['channelName']} ({channel['subscriberCount']} subs)")
        print(f"  Emails: {', '.join(channel['emails'])}")
        print(f"  URL: {channel['channelUrl']}")
```

### Direct channel URLs

```python
requests.post(
    f"{BASE}/acts/futurizerush~youtube-email-scraper/runs?token={TOKEN}",
    json={
        "inputMode": "directUrls",
        "channelUrls": [
            "https://www.youtube.com/@mkbhd",
            "https://www.youtube.com/@nateherk",
        ],
    },
)
```

## Complete Example (bash)

```bash
# Step 1: Start the run
RUN_RESPONSE=$(curl -s -X POST \
  "https://api.apify.com/v2/acts/futurizerush~youtube-email-scraper/runs?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputMode": "keywordSearch", "searchKeywords": ["AI automation"], "maxChannelsPerKeyword": 10, "maxResults": 10}')

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
  "channelName": "Nate Herk | AI Automation",
  "subscriberCount": "645.0K",
  "channelUrl": "https://www.youtube.com/@nateherk",
  "channelDescription": "Hi, I'm Nate Herk. I'm passionate about...",
  "joinDate": "Nov 17, 2013",
  "viewCount": 405328,
  "videoCount": 383,
  "location": null,
  "contactInfo": {
    "emails": ["sponsorships@nateherk.com"],
    "websites": ["https://nateherk.com/"],
    "socialMedia": {}
  },
  "emails": ["sponsorships@nateherk.com"],
  "websites": ["https://nateherk.com/"],
  "socialMedia": {},
  "emailCount": 1,
  "hasEmails": true,
  "descriptionUrls": [],
  "extractedAt": "2026-04-11T06:07:13.204Z",
  "processingSuccess": true,
  "searchKeyword": "AI automation"
}
```

**Note:** Field names use camelCase. The `emails` array is a flat convenience field; the same data is also in `contactInfo.emails`. Use `hasEmails` to quickly filter channels that have contact emails.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API token | Check `APIFY_API_TOKEN` |
| `invalid-input`: "must be equal to one of the allowed values" | Wrong `inputMode` value | Use `"directUrls"` or `"keywordSearch"` (exact strings) |
| No emails found | Channel doesn't list email publicly | Try more channels or different keywords |

## Tips

- Use `hasEmails: true` to quickly filter channels with public emails.
- `subscriberCount` is a string (e.g. `"645.0K"`) not a number.
- `contactInfo` contains structured data; `emails` and `websites` at root level are flat convenience arrays.
- For influencer outreach, search by niche keyword to find relevant channels with emails.
- `searchKeyword` in output tells you which query found each channel (useful with multiple keywords).
- No login or YouTube API key required.

## Links

- [Actor page](https://apify.com/futurizerush/youtube-email-scraper?fpr=rush)
- [Apify API docs](https://docs.apify.com/api/v2)
