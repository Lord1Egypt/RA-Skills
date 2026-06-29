---
name: airbnb-stay
version: 1.0.1
description: Single Airbnb listing lookups via StayingAPI.com — fetch one stay by id, airbnb.com/rooms URL, or street address, plus photos, reviews, host, amenities, availability, pricing, location, and rating.
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

# airbnb-stay

Focused single-listing skill. Use when the user **explicitly asks** about one known Airbnb property — its details, price, reviews, availability, photos, or host — given a listing id, an `airbnb.com/rooms/...` URL, or a street address.

## When to use this skill

**DO use when the user asks:**

- "What's this place? https://www.airbnb.com/rooms/12345678"
- "How much per night is listing 12345678?"
- "What are the reviews like on this Airbnb?"
- "Is this place available in July?"
- "Who's the host / is it a superhost?"
- "Show me the photos for this listing."

**Do NOT use when:**

- An Airbnb link or address appears incidentally in context (email signatures, unrelated documents)
- The user wants to *find* listings by criteria — use [`airbnb-search`](https://github.com/nikhonit/airbnb-skills/tree/main/skills/airbnb-search) instead
- The user has not signaled they want a property lookup

If you also need batch resolution, search, or webhooks, use [`airbnb-full`](https://github.com/nikhonit/airbnb-skills/tree/main/skills/airbnb-full) — it bundles everything in one install.

## Tools

Every tool returns a Python dict — the API response on success, or `{"error": ..., "detail": ...}` on failure. Sub-resource tools accept `stay_id` (cheapest), `url`, or `address`.

### `lookup_stay_by_id(stay_id, fields=None)` — 1 credit
Full canonical `Stay` record: title, property/room type, capacity, star rating, location, host, pricing, reviews count, rating breakdown, photos, reviews, amenities, and availability. `fields` is an optional comma-separated projection.

### `lookup_stay_by_url(url, fields=None)` — 1 credit
Same record, resolved from an `airbnb.com/rooms/<id>` URL.

### `lookup_stay_by_address(address, fields=None)` — 3 credits
Resolve a listing from a street address. Weighted higher; prefer id or URL when you have one.

### `get_stay_photos(...)` — 1 credit
Photo gallery (responsive image URLs).

### `get_stay_reviews(...)` — 1 credit
Reviews plus the rating breakdown (cleanliness, accuracy, check-in, communication, location, value).

### `get_stay_host(...)` — 1 credit
Host profile (name, superhost status, response data).

### `get_stay_amenities(...)` — 1 credit
Amenities grouped by category.

### `get_stay_availability(...)` — 1 credit
Per-date availability calendar (up to 12 months).

### `get_stay_pricing(...)` — 1 credit
Pricing block: nightly rate, fees, currency.

### `get_stay_location(...)` — 1 credit
Coordinates and address.

### `get_stay_rating(...)` — 1 credit
Star rating and review-count summary.

## Equivalent MCP tools

The Staying API hosts a streamable-HTTP MCP server at `https://api.stayingapi.com/mcp`. If your agent speaks MCP, you can skip this skill and call: `lookup_stay_by_id`, `lookup_stay_by_url`, `get_stay_photos`, `get_stay_reviews`.

## Authentication

Set `STAYINGAPI_KEY` to your Staying API key (format `sk_...`).

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

One credit per successful call (`by-address` is 3). Failed calls (`4xx`/`5xx`) do not consume credits. Credits roll forward and don't expire.

## Errors

Functions return a dict. On failure it carries an `error` key:

- `{"error": "auth", ...}` — `STAYINGAPI_KEY` is missing or invalid
- `{"error": "HTTP 404", ...}` — listing not found
- `{"error": "HTTP 429", ...}` — rate-limited; back off and retry
- `{"error": "network", ...}` — DNS/connection failure

## API reference

- OpenAPI spec: <https://stayingapi.com/openapi.json>
- Hosted MCP server: <https://api.stayingapi.com/mcp>
- Quickstart: <https://stayingapi.com/quickstart/>

## Trademark

Staying API is an independent service and is not affiliated with, endorsed by, or sponsored by Airbnb, Inc. "Airbnb" is a registered trademark of Airbnb, Inc.
