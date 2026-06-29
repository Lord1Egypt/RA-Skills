---
name: airbnb-full
version: 1.0.1
description: Complete Airbnb stay data toolkit via StayingAPI.com — id/URL/address lookup, sub-resources, listing search with presets, async batch jobs, job polling, webhook management, and account/usage. Plus the hosted MCP server's five tools.
license: MIT-0
author: Staying API
homepage: https://stayingapi.com
repository: https://github.com/nikhonit/airbnb-skills
tags:
  - airbnb
  - short-term-rental
  - vacation-rental
  - listings
  - reviews
  - batch
  - webhooks
  - api
  - mcp
metadata:
  openclaw:
    primaryEnv: STAYINGAPI_KEY
    homepage: https://stayingapi.com
    requires:
      env:
        - STAYINGAPI_KEY
---

# airbnb-full

Complete Airbnb stay data toolkit via StayingAPI.com. Use when the user **explicitly asks** about an Airbnb listing, its price, reviews or availability, listings to book in a place, or bulk/automated stay-data jobs.

## When to use this skill

Each tool call consumes Staying API credits, so this skill activates only when the user's request is genuinely about Airbnb stay data — not when a listing link or place name merely appears in passing.

**DO use when the user:**

- Pastes an Airbnb URL and asks about that listing → `lookup_stay_by_url`
- Gives a listing id or address and asks about the place, its reviews, or availability → `lookup_stay_by_id` / `lookup_stay_by_address`
- Asks for a specific facet (photos, reviews, host, amenities, availability, pricing, location, rating) → `get_stay_*`
- Asks to find stays matching criteria (location, dates, price, beds, capacity) → `search_stays` (or `search_superhost` / `search_instant_book` / `search_luxury`)
- Wants to resolve many listings at once → `batch_stays`
- Wants to be notified when an async job finishes → `create_webhook`
- Asks about their credit balance or usage → `get_account` / `get_usage`

**Do NOT use when:**

- An Airbnb link or address appears incidentally (email signatures, news articles, unrelated content)
- The user is discussing travel abstractly without asking for data on a specific listing or search
- The user has not signaled they want a lookup

When intent is ambiguous, ask the user to confirm before calling a tool. These tools cost credits and return large records.

## Tools

All tools return a Python dict — the API response on success, or `{"error": ..., "detail": ...}` on failure. The `get_stay_*` sub-resource tools accept `stay_id` (cheapest), `url`, or `address`.

### Lookup

- **`lookup_stay_by_id(stay_id, fields=None)`** — 1 credit. Full canonical `Stay` record.
- **`lookup_stay_by_url(url, fields=None)`** — 1 credit. Same, from an `airbnb.com/rooms/<id>` URL.
- **`lookup_stay_by_address(address, fields=None)`** — 3 credits. Resolve from a street address.

### Sub-resources (1 credit each)

- **`get_stay_photos(...)`** — photo gallery
- **`get_stay_reviews(...)`** — reviews + rating breakdown
- **`get_stay_host(...)`** — host profile
- **`get_stay_amenities(...)`** — amenities by category
- **`get_stay_availability(...)`** — 12-month availability calendar
- **`get_stay_pricing(...)`** — nightly rate, fees, currency
- **`get_stay_location(...)`** — coordinates and address
- **`get_stay_rating(...)`** — star rating and review-count summary

### Search

- **`search_stays(location=None, search_urls=None, check_in=None, check_out=None, price_min=None, price_max=None, min_beds=None, min_bedrooms=None, min_bathrooms=None, adults=None, children=None, infants=None, pets=None, currency=None, locale=None, max_items=50, fields=None)`** — 1 credit per result, `max_items` up to 240.
- **`search_superhost(...)` / `search_instant_book(...)` / `search_luxury(...)`** — same filters, preset segments.
- **`search_stays_with_details(...)`** — async; returns a job envelope (poll with `get_job` / `get_job_results`).

### Batch + jobs

- **`batch_stays(targets, webhook_id=None)`** — async. `targets` is a list of ids, URLs, and/or addresses (up to 500). Returns a job envelope.
- **`list_jobs(status=None, type=None, since=None, limit=50, offset=0)`** — list async jobs.
- **`get_job(job_id)`** — job status.
- **`get_job_results(job_id, limit=50, offset=0, format="json")`** — paginated results (`json` | `csv` | `ndjson`).

### Webhooks

- **`create_webhook(url, events, description=None)`** — `events` from: `job.queued`, `job.running`, `job.succeeded`, `job.failed`, `stay.cached`. Deliveries are HMAC-signed.
- **`list_webhooks()`** · **`get_webhook(webhook_id)`** · **`delete_webhook(webhook_id)`** · **`get_webhook_deliveries(webhook_id)`**

### Account

- **`get_account()`** — account, plan, and credit balance (`GET /v1/me`).
- **`get_usage(since=None, limit=50)`** — recent metered calls.

## Equivalent MCP tools

The hosted MCP server (`https://api.stayingapi.com/mcp`, streamable-HTTP, Bearer `sk_...` or OAuth 2.1 PKCE scope `mcp:access`) exposes five tools — an alternative to this skill: `lookup_stay_by_id`, `lookup_stay_by_url`, `search_stays`, `get_stay_photos`, `get_stay_reviews`.

## Authentication

Set `STAYINGAPI_KEY` to your Staying API key. Keys are `sk_...` strings.

```bash
export STAYINGAPI_KEY="sk_..."
```

Get a free key with 100 credits at <https://stayingapi.com/app/keys> — no card required.

## Pricing

| Plan | Price | Credits | Rate limit |
|---|---|---|---|
| Free | $0 | 100 (one-time) | 20/min |
| Monthly | $5/mo | 400/month | 200/min |
| Annual | $54/yr | 5,000/year | 300/min |
| Enterprise | Custom | Custom | 1,500/min |

One credit per stay record returned. Search bills 1 credit per result; `by-address` and address batch entries weigh 3. Failed calls (`4xx`/`5xx`) do not consume credits. Credits roll forward and don't expire.

## Errors

All functions return a Python dict. On success it contains the API response. On failure it contains an `error` key:

- `{"error": "auth", ...}` — `STAYINGAPI_KEY` is missing or invalid
- `{"error": "HTTP 404", ...}` — listing or job not found
- `{"error": "HTTP 429", ...}` — rate-limited; back off and retry
- `{"error": "network", ...}` — DNS/connection failure

## API reference

- OpenAPI spec: <https://stayingapi.com/openapi.json>
- Hosted MCP server (alternative to this skill): <https://api.stayingapi.com/mcp>
- MCP server card: <https://stayingapi.com/.well-known/mcp/server-card.json>
- Quickstart: <https://stayingapi.com/quickstart/>

## Trademark

Staying API is an independent service and is not affiliated with, endorsed by, or sponsored by Airbnb, Inc. "Airbnb" is a registered trademark of Airbnb, Inc.
