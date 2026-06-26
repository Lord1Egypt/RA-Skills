---
name: apify-substack-scraper
description: Scrape Substack newsletters and articles. Use when user asks to search Substack, find newsletter posts, extract Substack content, or monitor Substack publications. Requires APIFY_TOKEN environment variable.
metadata: {"openclaw":{"emoji":"📰","requires":{"env":["APIFY_TOKEN"],"bins":["curl","jq"]},"primaryEnv":"APIFY_TOKEN"}}
---

# Substack Scraper

Scrape Substack newsletters using an Apify Actor via the REST API.

## Actor ID
`BULaGFURBV7WG3K81`

## Prerequisites
- `APIFY_TOKEN` environment variable must be set
- `curl` and `jq` must be available

## Workflow

### Step 1: Confirm parameters with user
Ask what they want to scrape. Supported input fields:
- `urls` (array of strings) - Substack publication URLs to scrape
- `maxArticles` (integer) - max articles per publication
- `includeContent` (boolean) - include full article text

### Step 2: Run the Actor
```bash
RESULT=$(curl -s -X POST "https://api.apify.com/v2/acts/BULaGFURBV7WG3K81/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.substack.com"], "maxArticles": 20}')
echo "$RESULT" | jq '.'
```

### Step 3: Poll and fetch (if async)
```bash
RUN_ID=$(curl -s -X POST "https://api.apify.com/v2/acts/BULaGFURBV7WG3K81/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.substack.com"], "maxArticles": 100}' | jq -r '.data.id')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | jq -r '.data.status'
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN" | jq '.'
```

### Step 4: Present results
Summarize articles: titles, authors, dates, engagement. Offer JSON/CSV export.

## Error Handling
- If APIFY_TOKEN not set: `export APIFY_TOKEN=your_token`
- If run FAILS: check log endpoint
