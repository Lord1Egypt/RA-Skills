---
name: Google Maps Scraper
description: |
  This skill should be used when the user asks to
  "scrape Google Maps", "find businesses on Google Maps",
  "get business listings", "extract business data",
  "find restaurants near me", "get local business info",
  "scrape business emails from Google Maps",
  or needs to collect business data from Google Maps.
version: 0.1.0
---

# Google Maps Scraper with Apify

Search and extract business listings from Google Maps including name, address, phone, website, email, ratings, and opening hours. Supports email extraction from business websites.

Actor: `futurizerush/google-maps-scraper`

## Prerequisites

Set `APIFY_API_TOKEN` in environment. Get a token at [console.apify.com/account/integrations](https://console.apify.com/account/integrations?fpr=rush).

## Execution Flow

Apify runs are asynchronous. Every request follows 3 steps:

1. **Start a run** -- POST to the actor API, receive a run ID and dataset ID
2. **Poll until done** -- GET the run status, wait for `SUCCEEDED`
3. **Fetch results** -- GET the dataset items (returns a JSON array)

Typical run time: 1-5 minutes depending on result count and email scraping.

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `searchQueries` | array of strings | **Yes** (or `startUrls`) | Search queries (e.g. `["coffee shop taipei"]`, `["dentist new york"]`) |
| `startUrls` | array of objects | **Yes** (or `searchQueries`) | Direct Google Maps URLs in `[{"url": "..."}]` format |
| `maxResults` | integer | No | Max results per query. Default: 50. Min: 50 |
| `language` | string | No | Language for results. Options: `"en"`, `"zh-TW"`. Default: varies |
| `scrapeEmails` | boolean | No | Extract emails from business websites. Default: true |

## Complete Example (Python)

```python
import requests, os, time

TOKEN = os.environ["APIFY_API_TOKEN"]
BASE = "https://api.apify.com/v2"

# Step 1: Start the run
response = requests.post(
    f"{BASE}/acts/futurizerush~google-maps-scraper/runs?token={TOKEN}",
    json={
        "searchQueries": ["coffee shop taipei"],
        "maxResults": 50,
        "language": "en",
        "scrapeEmails": True,
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
for biz in items:
    print(f"{biz['name']} ({biz['businessType']})")
    print(f"  Rating: {biz['rating']} ({biz['reviews']} reviews)")
    print(f"  Address: {biz['address']}")
    print(f"  Phone: {biz['phone']}")
    if biz.get("emails"):
        print(f"  Emails: {', '.join(biz['emails'])}")
```

### Search with direct Google Maps URL

```python
requests.post(
    f"{BASE}/acts/futurizerush~google-maps-scraper/runs?token={TOKEN}",
    json={
        "startUrls": [
            {"url": "https://www.google.com/maps/search/sushi+restaurant+tokyo"}
        ],
        "maxResults": 50,
        "scrapeEmails": True,
    },
)
```

### Multiple queries

```python
requests.post(
    f"{BASE}/acts/futurizerush~google-maps-scraper/runs?token={TOKEN}",
    json={
        "searchQueries": ["dentist new york", "lawyer new york", "accountant new york"],
        "maxResults": 50,
        "scrapeEmails": True,
    },
)
```

## Complete Example (bash)

```bash
# Step 1: Start the run
RUN_RESPONSE=$(curl -s -X POST \
  "https://api.apify.com/v2/acts/futurizerush~google-maps-scraper/runs?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchQueries": ["coffee shop taipei"], "maxResults": 50, "language": "en", "scrapeEmails": true}')

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
  "name": "RUFOUS COFFEE",
  "placeId": "ChIJW03Z2y6qQjQRkIeeuqF3-mU",
  "latitude": 25.0235003,
  "longitude": 121.5436548,
  "rating": 4.6,
  "reviews": 1756,
  "address": "No. 339號, Section 2, Fuxing S Rd, Da'an District, Taipei City, Taiwan 106",
  "businessType": "Coffee shop",
  "phone": "+886 2 2736 6880",
  "website": "https://www.rufous.com.tw/",
  "email": null,
  "emails": [],
  "url": "https://www.google.com/maps/place/RUFOUS+COFFEE/data=...",
  "hours": [
    "Monday: 12 to 8 PM",
    "Tuesday: 12 to 8 PM",
    "Wednesday: 12 to 8 PM",
    "Thursday: Closed",
    "Friday: 12 to 8 PM",
    "Saturday: 12 to 8 PM",
    "Sunday: 12 to 8 PM"
  ],
  "hoursDetail": {
    "Monday": "12 to 8 PM",
    "Tuesday": "12 to 8 PM",
    "Thursday": "Closed"
  },
  "sourceUrl": "https://www.google.com/maps/search/coffee%20shop%20taipei?hl=en",
  "query": "coffee shop taipei",
  "timestamp": "2026-04-11T06:10:14.294Z",
  "scrapeDuration": 233
}
```

**Note:** Field names use camelCase. `email` is a single string (or null), `emails` is an array (may be empty even with `scrapeEmails: true` if no email is found on the website). `hours` is an ordered array; `hoursDetail` is a keyed object.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API token | Check `APIFY_API_TOKEN` |
| `invalid-input`: "must be >= 50" | `maxResults` below minimum | Set `maxResults` to at least 50 |
| No results | Query too specific or no businesses match | Broaden the search query |

## Tips

- Use `scrapeEmails: true` for lead generation -- the actor visits each business website to find emails.
- Email scraping adds time (visiting each website), so runs take longer with it enabled.
- `placeId` is a stable Google Maps identifier -- use it for deduplication across queries.
- `hours` is an ordered array (Monday-Sunday), `hoursDetail` is a keyed object -- use whichever is more convenient.
- `latitude` and `longitude` can be used for distance calculations or map visualizations.
- Multiple search queries run in a single actor execution.
- No Google Maps API key required.

## Links

- [Actor page](https://apify.com/futurizerush/google-maps-scraper?fpr=rush)
- [Apify API docs](https://docs.apify.com/api/v2)
