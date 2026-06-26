---
name: apify-hn-scraper
description: Scrape Hacker News stories, comments, and discussions. Use when user asks to search HN, find Hacker News posts, monitor tech discussions, or extract HN data. Requires APIFY_TOKEN environment variable.
metadata: {"openclaw":{"emoji":"🟧","requires":{"env":["APIFY_TOKEN"],"bins":["curl","jq"]},"primaryEnv":"APIFY_TOKEN"}}
---

# Hacker News Scraper

Scrape Hacker News using an Apify Actor via the REST API.

## Actor ID
`0UDODOnpTkxY3Oc90`

## Prerequisites
- `APIFY_TOKEN` environment variable must be set
- `curl` and `jq` must be available

## Workflow

### Step 1: Confirm parameters with user
Ask what they want to scrape. Supported input fields:
- `searchTerms` (array of strings) - keywords to search
- `maxResults` (integer) - max stories to return
- `sortBy` (string) - "points", "date", or "relevance"
- `includeComments` (boolean) - include comment threads

### Step 2: Run the Actor
```bash
RESULT=$(curl -s -X POST "https://api.apify.com/v2/acts/0UDODOnpTkxY3Oc90/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["TERM"], "maxResults": 30}')
echo "$RESULT" | jq '.'
```

### Step 3: Poll and fetch (if async)
```bash
RUN_ID=$(curl -s -X POST "https://api.apify.com/v2/acts/0UDODOnpTkxY3Oc90/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["TERM"], "maxResults": 100}' | jq -r '.data.id')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | jq -r '.data.status'
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN" | jq '.'
```

### Step 4: Present results
Summarize: top stories by points, comment counts, domains, trends. Offer JSON/CSV export.

## Error Handling
- If APIFY_TOKEN not set: `export APIFY_TOKEN=your_token`
- If run FAILS: check log endpoint
