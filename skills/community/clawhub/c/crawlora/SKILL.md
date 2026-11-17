---
name: crawlora
description: Fetches structured public web data through Crawlora's hosted REST API, including broad search, bounded web crawls, and durable cross-corpus research jobs. Calls require a user-provided API key and successful requests may consume credits. Use for public prices, listings, reviews, transcripts, SERPs, trends, financials, and places.
---

# Crawlora — structured public web data

Crawlora is a hosted API that turns public websites into clean, normalized JSON.
The current public-data catalog contains **3,509 tools across 467 platform
groups**, and the repository ships 169 installable research skills. One API key gives
you the endpoints in the bundled [catalog](reference/catalog.md) — search engines,
marketplaces, social and video, finance and crypto, maps, app stores, media, and
reviews — so an agent can fetch real data without running a browser, proxies, or
HTML parsers.

## Scope, billing, and job side effects

This skill calls Crawlora's hosted third-party API. Its catalog includes broad
public-web search and bounded crawl routes as well as ordinary one-shot data
lookups. Some routes start durable research or bounded web-crawl jobs that
continue after the initial request and retain owner-scoped job status, events,
and results. Successful requests may consume credits; `POST /web/crawl` requires
a `max_credits` limit. Before starting one of these jobs, make the source scope,
credit limit, and continuing job behavior clear to the user. Do not start
recurring or unbounded work. Use only the API key the user supplied through
`CRAWLORA_API_KEY`, and never print, store, or commit it.

Account usage, recent-IP, website-monitor management, generic URL scraping, APK
analysis, and bulk profile-dataset endpoints are intentionally excluded from
this skill. Dedicated skills cover the specialized workflows, and this helper
rejects those paths as well.

## When to use this skill

Use Crawlora when the user asks for live data that lives on a public website, e.g.:

- "What's the price of X on Amazon / eBay / Shopify?"
- "Pull the transcript / comments of this YouTube video."
- "Get the latest Google / Bing results for …" or "what's trending on Google Trends?"
- "Reviews and ratings for this iOS / Android app."
- "Yahoo Finance quote / financials for NVDA", "top CoinGecko gainers".
- "TikTok / Instagram / Reddit posts about …", "Trustpilot reviews for …".
- Any task where the alternative would be scraping HTML or maintaining a crawler.

Prefer a more specific Crawlora skill if one is installed (e.g.
`product-price-research`, `youtube-research`, `app-review-mining`,
`serp-keyword-research`). This umbrella skill covers everything else.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Export it so the helper and any `curl` calls can read it:

  ```sh
  export CRAWLORA_API_KEY
  ```

  Set `CRAWLORA_API_KEY` to the key you received before running the helper.

- All requests go to `https://api.crawlora.net/api/v1` with the header
  `CRAWLORA_API_KEY` from the environment. A missing/invalid key returns `401`.

## How it works

1. **Pick the endpoint.** Open [`reference/catalog.md`](reference/catalog.md) — it
   lists every endpoint grouped by platform, with method, path, and parameters.
   Match the user's job to a platform group, then to an endpoint.
2. **Call it** with `scripts/crawlora.sh` (see below). It handles auth and prints JSON.
3. **Parse** the JSON with `jq` and answer. Most endpoints return paginated lists;
   pass `page`/`count` params where documented.

## Calling the API

```sh
# GET with query params (key=value):
scripts/crawlora.sh /amazon/search k=laptop | jq '.'
scripts/crawlora.sh /google/suggest q="web scraping" | jq '.'
scripts/crawlora.sh /youtube/transcript/dQw4w9WgXcQ | jq '.'

# POST endpoints take a JSON body (note the -X POST):
scripts/crawlora.sh -X POST /google/search '{"keyword":"web scraping api","language":"en","country":"us"}' | jq '.'
scripts/crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["bitcoin"]}' | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


The catalog marks each endpoint's HTTP method. Path params like `{id}` are
substituted into the URL; `GET` params go in the query string; `POST` params go
in the JSON body.

## Endpoint reference

See [`reference/catalog.md`](reference/catalog.md) for the complete list of
endpoints (method, path, params, description) grouped by platform.

## Examples

- **Product price:** `scripts/crawlora.sh /amazon/search k="standing desk"` →
  read `.data[].price` to compare listings.
- **YouTube transcript:** resolve the video id from the URL, then
  `scripts/crawlora.sh /youtube/transcript/<id>` and summarize.
- **Trend check:** `scripts/crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["electric bikes"]}'`.
- **Finance:** `scripts/crawlora.sh /yahoo-finance/ticker/NVDA/quote` (see the
  Yahoo Finance group in the catalog for the exact path/params).

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx` responses; failures aren't charged.
  Free tier is 2,000 credits/mo. Get a key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Long-running jobs:** `/research/jobs` and `/web/crawl` create durable work.
  Bound crawl credits with `max_credits`, poll only as needed, and cancel a job
  when the user no longer needs it.
- **Public data only.** Crawlora returns publicly available web data; no third-party
  account credentials are involved. Respect each source's terms and rate limits.
- **Security:** keep the key in `CRAWLORA_API_KEY` only — never hardcode it, never put
  it in a URL query param, never commit it.
- Some search endpoints return `503` when the upstream serves a challenge page; retry
  or fall back to another search provider (Google ↔ Bing ↔ Brave).
