---
name: apify-bluesky-scraper
description: Scrape Bluesky social posts via AT Protocol. Use when user asks to search Bluesky, find Bluesky posts, monitor Bluesky discussions, or extract Bluesky data. Requires APIFY_TOKEN environment variable.
metadata: {"openclaw":{"emoji":"🦋","requires":{"env":["APIFY_TOKEN"],"bins":["curl","jq"]},"primaryEnv":"APIFY_TOKEN"}}
---

# Bluesky Scraper

Scrape Bluesky posts using an Apify Actor via the REST API.

## Actor ID
`WAJfBnZBYR9mJrk5d`

## Prerequisites
- `APIFY_TOKEN` environment variable must be set
- `curl` and `jq` must be available

## Workflow

### Step 1: Confirm search parameters with user
Ask what they want to search for. Supported input fields:
- `searchTerms` (array of strings) - keywords to search
- `maxResults` (integer) - max posts to return (default: 50)
- `sortBy` (string) - "relevance" or "latest"

### Step 2: Run the Actor (synchronous)
```bash
RESULT=$(curl -s -X POST "https://api.apify.com/v2/acts/WAJfBnZBYR9mJrk5d/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["SEARCH_TERM"], "maxResults": 50, "sortBy": "relevance"}')
echo "$RESULT" | jq '.'
```

For larger jobs (async):
```bash
RUN_ID=$(curl -s -X POST "https://api.apify.com/v2/acts/WAJfBnZBYR9mJrk5d/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["TERM"], "maxResults": 50}' | jq -r '.data.id')
```

### Step 3: Poll and fetch (if async)
```bash
STATUS=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | jq -r '.data.status')
# Poll every 5s until SUCCEEDED or FAILED
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN" | jq '.'
```

### Step 4: Present results
Summarize: total posts, top by engagement, common themes. Offer JSON/CSV export.

## Error Handling
- If APIFY_TOKEN not set: `export APIFY_TOKEN=your_token`
- If run FAILS: `curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/log?token=$APIFY_TOKEN"`
- Rate limited (429): wait 60s, retry
