---
name: app-review-mining
description: Mines App Store and Google Play data via the Crawlora API — app details, reviews, ratings, store rankings, and similar apps — as clean JSON. Use when the user wants mobile-app reviews, ratings, store charts/rankings, or competitive ASO (app store optimization) research without scraping store pages.
---

# App review mining & ASO

Pull App Store (iOS) and Google Play (Android) app details, reviews, ratings,
rankings, and similar-app lists as normalized JSON from the Crawlora API.

## When to use this skill

- "What are the reviews / ratings for <app>?"
- "How is <app> ranked?" / "top apps in <category>."
- "Find apps similar to <app>" / competitive ASO research.
- "Pull this app's details / privacy / version history."
- Building an app-review sentiment or competitor-tracking pipeline.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Choose the store (both have parallel endpoints), then the job:

1. **Find the app** — `/appstore/search?term=...` or `/googleplay/search?q=...`
   to resolve the app id / bundle id.
2. **Details** — `/appstore/app`, `/googleplay/app` for metadata, rating summary,
   description, and developer.
3. **Reviews** — `/appstore/reviews`, `/googleplay/reviews` (paginate) for the
   review text, score, and date to mine sentiment and themes.
4. **Rankings** — `/appstore/list`, `/googleplay/list` for store charts by category.
5. **Competitors** — `/appstore/similar`, `/googleplay/similar` for similar apps.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Find an app, then pull its reviews (GET, key=value params):
scripts/crawlora.sh /appstore/search term="notion" | jq '.'
scripts/crawlora.sh /appstore/reviews id=1232780281 country=us | jq '.data'

scripts/crawlora.sh /googleplay/search term="notion" | jq '.'
scripts/crawlora.sh /googleplay/reviews app_id="notion.id" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every App Store and
Google Play endpoint this skill uses (method, path, params, description).

## Examples

- **Review sentiment:** resolve the app id via search → `/appstore/reviews`
  (paginate) → classify each review's sentiment and summarize top complaints/praise.
- **Cross-store compare:** pull `/appstore/app` and `/googleplay/app` for the same
  product to compare ratings and review volume across platforms.
- **Category ranking watch:** `/googleplay/list` for a category to track where an
  app sits in the charts over time.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public store pages; respect Apple's and Google's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Reviews are paginated and locale-specific — pass `country`/`page` to widen coverage.
