---
name: aerobase-travel
description: Jetlag-aware flight intelligence for AI travel agents
version: 1.0.0
author: Aerobase
tier: free
api_base: https://aerobase.app/api
---

# Aerobase Travel Intelligence

You have access to the Aerobase travel API for jetlag-scored flight search and analysis.

## Setup

Set your API key:

```bash
export AEROBASE_API_KEY="ak_..."
```

All requests use `https://aerobase.app/api` as the base URL.

## Response Envelope

Every response wraps data in a standard envelope:

```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "tier": "free",
    "calls_remaining": 7,
    "latency_ms": 142
  }
}
```

Errors return:

```json
{
  "error": { "code": "VALIDATION_ERROR", "message": "..." },
  "meta": { "request_id": "...", "tier": "free", "calls_remaining": 9, "latency_ms": 12 }
}
```

## Rate Limits

Free tier: 10 requests per hour. When `calls_remaining` reaches 0, wait until the hour resets.

---

## Available Tools

### 1. Score a Flight

When the user describes a specific flight with departure and arrival times, score it for jetlag impact.

```bash
curl -s -X POST "https://aerobase.app/api/v1/flights/score" \
  -H "Authorization: Bearer $AEROBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "LAX",
    "to": "NRT",
    "departure": "2026-04-15T13:25:00-07:00",
    "arrival": "2026-04-16T15:40:00+09:00",
    "cabin": "economy"
  }'
```

**Required fields:** `from`, `to` (3-letter IATA), `departure`, `arrival` (ISO 8601 with timezone offset).

**Optional:** `cabin` (economy | business | first | premium_economy).

**Response data:**

| Field | Type | Description |
|-------|------|-------------|
| `score` | number | 0-100, higher is better for jetlag |
| `tier` | string | excellent / good / moderate / poor / severe |
| `recovery_days` | number | Estimated days to fully recover |
| `direction` | string | east / west / same |
| `timezone_shift_hours` | number | Hours of timezone crossing |
| `breakdown` | object | Sub-scores (circadian, duration, arrival) |
| `insight` | string | Human-readable summary |
| `strategies.departure` | string | Pre-departure advice |
| `strategies.arrival` | string | Post-arrival advice |
| `strategies.shift` | string | Circadian shift approach |
| `strategies.recovery` | string | Recovery timeline estimate |
| `tips` | string[] | Actionable tips list |
| `origin` | object | Airport details (code, name, city, timezone) |
| `destination` | object | Airport details (code, name, city, timezone) |

**Present to user:** "This flight scores **X/100** for jetlag (tier). You'd need ~Y days to recover. [strategies.arrival summary]"

---

### 2. Search Flights

Search for flights on a route and date, ranked by jetlag score.

```bash
curl -s -X POST "https://aerobase.app/api/v1/flights/search" \
  -H "Authorization: Bearer $AEROBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "SFO",
    "to": "LHR",
    "date": "2026-05-20",
    "max_stops": 1,
    "sort": "jetlag",
    "limit": 5
  }'
```

**Required:** `from`, `to` (IATA), `date` (YYYY-MM-DD).

**Optional:** `return_date`, `max_stops` (default 2), `sort` (jetlag | price | duration), `limit` (max 5 on free tier).

**Response data** is an array of flights:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Flight identifier |
| `price` | number/null | Price in USD (null for database results) |
| `duration_minutes` | number | Total trip duration |
| `stops` | number | Number of stops |
| `jetlag_score` | number | 0-100 composite score |
| `tier` | string | Jetlag tier |
| `recovery_days` | number | Recovery estimate |
| `direction` | string | east / west / same |
| `booking_url` | string/null | Booking link when available |
| `segments` | array | Flight legs with from, to, airline, departure, arrival |
| `source` | string | "live" or "database" |

**Present to user:** Show as a ranked list. Lead with the best jetlag score. Mention price if available. Highlight the score difference between best and worst option.

---

### 3. Airport Info

Get airport details including jetlag-relevant facilities, lounges, and transit options.

```bash
curl -s "https://aerobase.app/api/v1/airports/NRT" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

**Response data:**

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | IATA code |
| `name` | string | Airport name |
| `city` | string | City |
| `country` | string | Country |
| `timezone` | string | IANA timezone |
| `latitude` | number | Latitude |
| `longitude` | number | Longitude |
| `facilities` | array | Jetlag facilities (sleep pods, showers, etc.) |
| `lounges` | array | Available lounges with amenities and ratings |
| `transit` | array | Ground transport options with time and cost |

**Present to user:** Highlight facilities that help with jetlag recovery (sleep pods, showers, daylight rooms). Mention lounge access options for layovers.

---

### 4. Route Intelligence

Get comprehensive route analysis between two airports including direct and connecting options.

```bash
curl -s "https://aerobase.app/api/v1/routes/LAX/NRT" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

**Response data:**

| Field | Type | Description |
|-------|------|-------------|
| `origin` | object | Airport info (code, name, city, country, timezone) |
| `destination` | object | Airport info |
| `timezone_shift` | object | hours, direction, actual_shift_hours, UTC offsets |
| `direct_routes` | array | Nonstop options with jetlag_score, airlines, distance |
| `connecting_routes` | array | 1-2 stop options with connection airports |
| `route_count` | number | Total routes found |

Each route includes: `jetlag_score` (0-100), `stops`, `connections`, `total_distance_km`, `total_duration_minutes`, `recovery_days`, `segments`.

**Present to user:** Start with timezone shift context ("This route crosses X hours"). Compare direct vs connecting options. Note that connecting flights sometimes score better when the layover breaks the circadian disruption.

---

### 5. Travel Deals

Browse jetlag-scored travel deals. Free tier returns up to 3 results.

```bash
curl -s "https://aerobase.app/api/v1/deals?departure=LAX&sort=value_score&limit=3" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

**Query parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `departure` | string | Origin IATA (optional) |
| `destination` | string | Destination IATA (optional) |
| `max_price` | number | Maximum price USD (optional) |
| `sort` | string | value_score / price / jetlag_score / newest |
| `limit` | number | Max results (3 on free tier) |

**Response data.deals** array:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Deal headline |
| `source` | string | Deal source |
| `price_usd` | number | Price |
| `cabin_class` | string | Cabin |
| `is_error_fare` | boolean | Error fare flag |
| `origin` | object | {iata, city} |
| `destination` | object | {iata, city} |
| `jetlag` | object | score, recovery_days, direction, recommendation |
| `value_score` | number | Combined value metric |
| `travel_dates` | object | start, end, specificity |
| `booking_deadline` | string | Expiration |
| `source_url` | string | Booking link |

**Present to user:** Lead with value_score. Mention jetlag impact alongside price. Flag error fares prominently (they disappear fast).

---

## Presentation Guidelines

1. **Always mention jetlag score and recovery days** - these are the primary differentiators.
2. **Compare scores** when showing multiple options. "Flight A scores 82/100 vs Flight B at 61/100 - that's a full day less recovery."
3. **Highlight departure/arrival strategy** - users want actionable advice, not just numbers.
4. **Convert technical data to natural language** - say "you'll cross 9 time zones heading east" not "timezone_shift_hours: 9, direction: east".
5. **Context matters** - a score of 70 on a 2-hour flight is unremarkable, but 70 on a transpacific route is excellent.
6. **Use tier labels** - "excellent", "good", "moderate", "poor", "severe" are immediately understandable.

## Score Interpretation

| Score | Tier | Recovery | Meaning |
|-------|------|----------|---------|
| 80-100 | Excellent | 0-1 days | Minimal jetlag, well-timed flight |
| 65-79 | Good | 1-2 days | Manageable with basic strategies |
| 50-64 | Moderate | 2-3 days | Noticeable jetlag, follow recovery plan |
| 35-49 | Poor | 3-5 days | Significant disruption expected |
| 0-34 | Severe | 5+ days | Consider alternative flight times |
