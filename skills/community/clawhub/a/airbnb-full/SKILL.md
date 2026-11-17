---
name: airbnb-full
description: "Complete Airbnb toolkit — search, availability, listing detail, price, cross-OTA price comparison and reviews, all in one unified schema. Install this when an agent needs broad Airbnb coverage. Powered by StayingAPI."
version: "1.0.0"
license: MIT-0
author: StayingAPI
homepage: https://stayingapi.com
repository: https://github.com/stayingapi/airbnb-skills
user-invocable: true
compatibility: Requires internet access to reach api.stayingapi.com. No additional runtimes or dependencies needed.
required_environment_variables:
  - name: STAYINGAPI_KEY
    prompt: Your StayingAPI key (starts with stay_)
    help: Free key at https://stayingapi.com/signup — no card. A stay_test_ sandbox key returns fixtures at zero cost.
    required_for: all API requests
tags: ["airbnb", "airbnb-api", "search", "availability", "reviews", "price-comparison", "travel", "accommodation"]
metadata: {"openclaw":{"emoji":"🧰","requires":{"env":["STAYINGAPI_KEY"]},"primaryEnv":"STAYINGAPI_KEY","homepage":"https://stayingapi.com"},"hermes":{"tags":["airbnb","airbnb-api","search","availability","reviews","price-comparison","travel","accommodation"],"category":"integrations"}}
---

# Airbnb — complete toolkit

The everything skill for Airbnb: search, availability, listing detail, price, cross-OTA price comparison and reviews — one key, one schema. Install the focused skills instead when you want a minimal tool surface.

## Setup

If `$STAYINGAPI_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md) and follow it to get and store the key. A `stay_test_` sandbox key works for evaluation at zero cost.

## When to use this skill

**DO use when the user asks:**

- Any Airbnb data task — the agent picks the right call

**Do NOT use when:**

- You want the smallest possible tool surface — install a focused skill

## Required headers

Every request needs:

- **Authorization:** `Bearer $STAYINGAPI_KEY`
- **User-Agent:** your agent's name (e.g. `ClaudeCode/1.0`).

Base URL: `https://api.stayingapi.com/v1`.

## Tools

### `GET /v1/search`

Discover properties matching a location, dates, occupancy and filters across one or more platforms. Results from every requested platform are normalized to the same Property shape and merged into a single, cursor-paginated list. This is the breadth / funnel endpoint — and the clearest demonstration of "one schema, every platform".

Key parameters:
- `location` — **Required.** Place name ("Split, HR") or "lat,lng".
- `checkIn` — YYYY-MM-DD; required if checkOut given; not in the past.
- `checkOut` — YYYY-MM-DD; required if checkIn given; must be after checkIn.
- `adults` — ≥ 1.
- `children` — ≥ 0.
- `childAges[]` — Length must equal children. Coarsened for Vrbo/Airbnb.
- `platforms[]` — Drives fan-out + per-platform billing.

### `GET /v1/availability`

Get day-by-day availability for a known listing (or a batch of listings) on one platform over a date window. Each day reports whether it is available, its minimum-night requirement, and whether check-in / check-out / booking is allowed.

Key parameters:
- `platform` — **Required.** vrbo | booking | airbnb | google. Single platform (not a fan-out endpoint). Use the API value, not the brand name — "booking", not "booking-com"; "google", not "google-hotels".
- `listingId` — A single listing id on platform.
- `listingIds[]` — A batch of listing ids on platform.
- `url` — Full listing URL (alternative to an id).
- `startDate` — **Required.** YYYY-MM-DD; not in the past.
- `endDate` — **Required.** After startDate; window ≤ 365 days.

### `GET /v1/listing/{platform}/{id}`

Full normalized detail for one listing: amenities (canonical taxonomy), photos, host, geo, ratings, and — when you pass dates — an embedded live price. The detail body is cached 24 h; any embedded live price is cached at the 1 h price TTL and composed at read time, so a stale price never rides on fresh detail.

Key parameters:
- `platform` — **Required.** vrbo | booking | airbnb | google.
- `id` — **Required.** Platform-native listing id (case-sensitive, verbatim from source). A bare booking.com slug needs a country — without one it returns 400 needs_country (booking slugs are not globally unique).
- `country` — ISO-3166 alpha-2 (booking). Disambiguates a bare booking slug without the %2F-encoded /hotel/{cc}/{slug} id — e.g. ?country=co.
- `checkIn` — Pairs with checkOut; presence embeds a best-effort live price (may be null; the call still bills).
- `checkOut` — Must be after checkIn.
- `adults` — ≥ 1 (only used with dates).

### `GET /v1/price`

Quote one listing for specific dates and occupancy. Pass the platform-native platformListingId returned by /v1/search — numeric on Airbnb and Vrbo, a slug string on Booking.com and Google (e.g. "abramovic2") — or a full listing URL. On a live key the response is always a real numeric price or a typed error — never a wrong property's price. Note this guarantee covers live calls: sandbox (stay_test_) responses are canned fixtures and may echo a different listing, dates or occupancy than you requested, so do not assert identity against a sandbox response.

Key parameters:
- `platform` — **Required.** vrbo | booking | airbnb | google.
- `listingId` — **Required.** Platform-native id from /v1/search platformListingId — numeric (Airbnb/Vrbo) or a slug string (Booking.com/Google). Or pass a url.
- `checkIn` — **Required.** YYYY-MM-DD; not in the past.
- `checkOut` — **Required.** Must be after checkIn.
- `adults` — ≥ 1.
- `children` — ≥ 0.

### `GET /v1/price-compare`

Rate-shop one property in a single call, resolved through the Google Hotels backbone. The response carries the offers the backbone exposes for that property plus StayingAPI-computed min and median over those offers as first-class fields, so you can read the cheapest rate without re-deriving it. Coverage varies by property: some resolve to several OTA offers, others to a single aggregated-lowest offer (then offers has one entry, min equals median, and the entry may be a direct-supplier rate rather than an OTA). Read offers.length before presenting a result as a multi-platform comparison — the schema does not guarantee more than one.

Key parameters:
- `name` — Property name to resolve.
- `googleHotelId` — Precise Google Hotels id.
- `location` — Disambiguating place / "lat,lng".
- `checkIn` — **Required.** YYYY-MM-DD; not in the past.
- `checkOut` — **Required.** Must be after checkIn.
- `adults` — ≥ 1.

### `GET /v1/reviews`

Normalized, paginated reviews for one listing on one platform. Native rating scales are preserved and echoed alongside each rating (TripAdvisor/Airbnb/Vrbo use 5; Booking.com/Expedia/Hotels.com use 10) — never silently rescaled.

Key parameters:
- `platform` — **Required.** vrbo | booking | airbnb. Note google is NOT enabled for reviews (400 platform_not_enabled). Use the API value, not the brand name — "booking", not "booking-com".
- `listingId` — Listing id on platform.
- `url` — Full listing URL.
- `limit` — 1–100.
- `cursor` — Opaque base64 cursor.
- `language` — ISO-639-1 filter.


> Filter results to Airbnb by passing `platforms=airbnb` to the search call.

## MCP (no key pasted into the agent)

On an MCP-capable runtime, connect `https://mcp.stayingapi.com/mcp` (OAuth 2.1 + PKCE) and use: `search_stays`, `check_availability`, `get_listing`, `get_price`, `compare_prices`, `get_reviews`.

## Platform × endpoint support

Not every endpoint supports every platform. Verified:

| platform | search | availability | price | price-compare | listing | reviews |
|---|---|---|---|---|---|---|
| `airbnb` | yes | yes | yes | yes | yes | yes |
| `booking` | yes | yes | yes | yes | yes | yes |
| `vrbo` | yes | yes | yes | yes | yes | yes |
| `google` | yes | yes | yes | yes | **no** | **no** |

`GET /v1/listing/google/…` and `GET /v1/reviews?platform=google` return
`400 platform_not_enabled` ("google is not enabled for this endpoint"). Use `booking`,
`airbnb` or `vrbo` for listing detail and reviews; use `google` for search, price and
cross-OTA price-compare.

## The cross-OTA advantage

StayingAPI is **cross-platform**: Airbnb data comes back in the *same unified schema* as Booking.com, Vrbo and Google Hotels, so one integration covers them all. `/v1/price-compare` resolves a property through the Google Hotels backbone and returns the offers it exposes plus a StayingAPI-computed **min** and **median** over those offers, as first-class fields.

> Coverage varies by property and by what the backbone returns: some properties come back with several OTA offers, others with a single aggregated-lowest offer (in which case `min` equals `median` and `offers` has one entry, sometimes a direct-supplier rate rather than an OTA). Read `offers.length` before describing a result as a multi-platform comparison.

## Async & partial failures

A live call that has to scrape returns `202` with `data.jobId`, `data.pollUrl` and
`data.estimatedSeconds` (the `202` itself charges 0). Poll `GET /v1/jobs/{jobId}` (free)
until `data.status` is TERMINAL — `completed` **or** `failed`.

- **`completed`** → the payload is at `data.result` (the same schema the sync call returns;
  `data` itself is just `{jobId, result, status}`). `meta` carries `partial`,
  `platformResults[]` and `warnings[]`. A completed job may still return an **empty**
  result (`data.result: []`) — the reason is in `meta.warnings[]` (e.g. `no_results`), and
  empty results charge 0.
- **`failed`** → HTTP is still **200**, not an HTTP error. The failure is nested at
  `data.error` (`code`, `type`, `message`, `retryable`). Detect it with
  `data.status === "failed"`, **not** a top-level `error`. `creditsCharged` is 0, and `meta`
  carries only `{requestId, creditsCharged, platforms}` — do **not** read `partial`,
  `platformResults` or `warnings` on a failed job.

Pace your polling: honour the `Retry-After` header, back off between attempts, and cap the
number of attempts. A tight loop hits `429 rate_limit_exceeded` (120 requests/minute).

## Known limitations

- **Pagination:** `limit`/`cursor` are accepted where documented, but availability depends on the endpoint and the upstream source — treat `meta.pagination` as authoritative and stop when `hasMore` is false or `nextCursor` is null.
- **Externally-sourced ids:** a Vrbo id obtained somewhere other than `/v1/search` may not resolve upstream and can produce a failed job (`all_actors_failed`). Prefer ids from `/v1/search` (`platformListingId`).
- **Platform gaps:** see the support matrix above — `google` has no listing or reviews endpoint.

## Credits

Number-free by design — **failed, empty and blocked calls are never billed**, and `stay_test_` sandbox calls are always free. Current costs: <https://stayingapi.com/pricing> · full contract: <https://api.stayingapi.com/openapi.json>.

## Trademark

StayingAPI is an independent service and is not affiliated with, endorsed by, or sponsored by Airbnb. Airbnb is a trademark of its respective owner.

---

**Get your free key → https://stayingapi.com/signup** · Docs: https://stayingapi.com/docs
