---
name: aerobase-travel-pro
description: Full jetlag intelligence suite with award search, comparison, recovery plans, and itinerary analysis
version: 1.0.0
author: Aerobase
tier: pro
api_base: https://aerobase.app/api
---

# Aerobase Travel Intelligence Pro

You have access to the full Aerobase travel API. This includes everything in the free tier plus award flight search, side-by-side comparison, personalized recovery plans, itinerary analysis, and flight lookup.

## Setup

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
    "tier": "pro",
    "calls_remaining": 38,
    "latency_ms": 142
  }
}
```

Errors return:

```json
{
  "error": { "code": "VALIDATION_ERROR", "message": "..." },
  "meta": { "request_id": "...", "tier": "pro", "calls_remaining": 41, "latency_ms": 12 }
}
```

## Rate Limits

Pro tier: 42 requests per hour. Monitor `calls_remaining` in response meta.

---

## Tools 1-5: Core (Free Tier)

### 1. Score a Flight

Score a specific flight for jetlag impact given exact departure and arrival times.

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

**Required:** `from`, `to` (3-letter IATA), `departure`, `arrival` (ISO 8601 with tz offset).
**Optional:** `cabin` (economy | business | first | premium_economy).

**Response data:** `score` (0-100), `tier`, `recovery_days`, `direction`, `timezone_shift_hours`, `breakdown`, `insight`, `strategies` (departure, arrival, shift, recovery), `tips[]`, `origin`, `destination`.

**Present:** "This flight scores **X/100** (tier). ~Y days recovery. [strategy summary]"

---

### 2. Search Flights

Search flights on a route ranked by jetlag score. Pro tier returns up to 50 results.

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
    "limit": 10
  }'
```

**Required:** `from`, `to`, `date` (YYYY-MM-DD).
**Optional:** `return_date`, `max_stops` (default 2), `sort` (jetlag | price | duration), `limit` (max 50).

**Response:** Array of flights with `id`, `price`, `duration_minutes`, `stops`, `jetlag_score` (0-100), `tier`, `recovery_days`, `direction`, `booking_url`, `segments[]`, `source`.

---

### 3. Airport Info

Airport details with jetlag facilities, lounges, and ground transit.

```bash
curl -s "https://aerobase.app/api/v1/airports/NRT" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

**Response:** `code`, `name`, `city`, `country`, `timezone`, `latitude`, `longitude`, `facilities[]`, `lounges[]`, `transit[]`.

---

### 4. Route Intelligence

Comprehensive route analysis with direct and connecting options.

```bash
curl -s "https://aerobase.app/api/v1/routes/LAX/NRT" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

**Response:** `origin`, `destination`, `timezone_shift` (hours, direction, offsets), `direct_routes[]`, `connecting_routes[]`, `route_count`. Each route has `jetlag_score`, `stops`, `connections`, `total_distance_km`, `recovery_days`, `segments[]`.

---

### 5. Travel Deals

Jetlag-scored travel deals. Pro tier returns up to 50 results.

```bash
curl -s "https://aerobase.app/api/v1/deals?departure=LAX&sort=value_score&limit=20" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

**Params:** `departure`, `destination`, `max_price`, `sort` (value_score | price | jetlag_score | newest), `limit`.

**Response:** `deals[]` with `title`, `price_usd`, `cabin_class`, `is_error_fare`, `origin`, `destination`, `jetlag` (score, recovery_days, direction, recommendation), `value_score`, `travel_dates`, `booking_deadline`, `source_url`.

---

## Tools 6-10: Pro Exclusive

### 6. Award Search

Search award flight availability across 24 loyalty programs with jetlag scoring.

```bash
curl -s -X POST "https://aerobase.app/api/v1/awards/search" \
  -H "Authorization: Bearer $AEROBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "SFO",
    "to": "NRT",
    "cabin": "business",
    "date_from": "2026-06-01",
    "date_to": "2026-06-15",
    "limit": 20
  }'
```

**Required:** `from`, `to` (IATA).
**Optional:** `cabin` (economy | business | premium | first), `date` (single date), `date_from`/`date_to` (range), `limit` (max 100).

**Response data** is an array:

| Field | Type | Description |
|-------|------|-------------|
| `origin` | string | Origin IATA |
| `destination` | string | Destination IATA |
| `date` | string | Travel date |
| `cabin` | string | Cabin class |
| `miles` | number | Miles/points cost |
| `seats_remaining` | number/null | Seats available |
| `program` | string | Loyalty program (e.g., "united", "aeroplan") |
| `jetlag_score_k2` | number/null | K2 score 0-100 (higher = better) |
| `departure_time` | string/null | Local departure time |
| `arrival_time` | string/null | Local arrival time |

**Present to user:** Rank by jetlag_score_k2. Mention miles cost, program, and available seats. "ANA business via United MileagePlus: 88,000 miles, scores 76/100 for jetlag with 2 seats left."

---

### 7. Flight Compare

Compare 2-10 flights side by side with a recommendation.

```bash
curl -s -X POST "https://aerobase.app/api/v1/flights/compare" \
  -H "Authorization: Bearer $AEROBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "flights": [
      {
        "from": "SFO",
        "to": "LHR",
        "departure": "2026-05-20T16:30:00-07:00",
        "arrival": "2026-05-21T10:45:00+01:00",
        "cabin": "economy",
        "label": "United afternoon"
      },
      {
        "from": "SFO",
        "to": "LHR",
        "departure": "2026-05-20T21:15:00-07:00",
        "arrival": "2026-05-21T15:10:00+01:00",
        "cabin": "economy",
        "label": "BA red-eye"
      }
    ]
  }'
```

**Required:** `flights` array (2-10 items). Each flight needs `from`, `to`, `departure`, `arrival`.
**Optional per flight:** `cabin`, `label`.

**Response data:**

| Field | Type | Description |
|-------|------|-------------|
| `flights` | array | Scored flights with full breakdown and per-flight strategies |
| `recommendation.pick` | number | Index of best option |
| `recommendation.label` | string | Label of recommended flight |
| `recommendation.reason` | string | Explanation of why it wins |
| `deltas.score_range` | number | Score spread across options |
| `deltas.recovery_range` | number | Recovery days spread |
| `deltas.duration_range` | number | Duration spread in minutes |

Each flight in the array includes: `score` (composite, tier, recovery_days, direction, breakdown), `explanation` (summary, departure_strategy, arrival_strategy, shift_approach, recovery_estimate, tips[]).

**Present to user:** Lead with the recommendation. Show a comparison table. Highlight the key differentiator (arrival time, duration, recovery). "I recommend **[label]** - it scores X vs Y, saving you ~Z days of recovery because [reason]."

---

### 8. Recovery Plan

Generate a personalized jetlag recovery plan with pre-flight, in-flight, and post-arrival schedules. Optionally assess risk against arrival commitments.

```bash
curl -s -X POST "https://aerobase.app/api/v1/recovery/plan" \
  -H "Authorization: Bearer $AEROBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "SFO",
    "to": "TYO",
    "departure": "2026-06-10T11:00:00-07:00",
    "arrival": "2026-06-11T14:30:00+09:00",
    "cabin": "business",
    "arrival_commitments": [
      { "event": "Client meeting", "time": "2026-06-12T09:00:00+09:00" },
      { "event": "Team dinner", "time": "2026-06-12T19:00:00+09:00" }
    ]
  }'
```

**Required:** `from`, `to`, `departure`, `arrival`.
**Optional:** `cabin`, `arrival_commitments[]` (event name + time).

**Response data:**

| Field | Type | Description |
|-------|------|-------------|
| `score` | object | Composite score, tier, recovery_days, breakdown |
| `recovery_plan.pre_flight_schedule` | array | Days before departure - light exposure, sleep timing |
| `recovery_plan.during_flight` | object | In-flight strategy - when to sleep, eat, hydrate |
| `recovery_plan.post_arrival_schedule` | array | Day-by-day recovery schedule |
| `recovery_plan.recovery_timeline` | array | Hourly adaptation milestones |
| `recovery_plan.personalized_insights` | array | Tailored advice |
| `commitment_risks` | array | Per-commitment risk assessment |
| `timezone_shift` | object | Hours, direction |

Each commitment risk includes: `event`, `scheduled_time`, `body_clock_time` (what your body thinks the time is), `misalignment_hours`, `risk_level` (low | moderate | high), `warning`.

**Present to user:** Start with the score. Walk through the plan chronologically: "**3 days before**: Start shifting sleep 30 min earlier each night. **On the flight**: Sleep from [time] to [time]. **Day 1**: Get morning sunlight before 10am..." If commitments exist, flag any high-risk ones prominently.

---

### 9. Itinerary Analyze

Analyze a multi-leg itinerary for cumulative jetlag fatigue, compounding effects, and recovery gaps.

```bash
curl -s -X POST "https://aerobase.app/api/v1/itinerary/analyze" \
  -H "Authorization: Bearer $AEROBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "legs": [
      {
        "from": "SFO",
        "to": "LHR",
        "departure": "2026-06-01T17:00:00-07:00",
        "arrival": "2026-06-02T11:00:00+01:00",
        "cabin": "business"
      },
      {
        "from": "LHR",
        "to": "DXB",
        "departure": "2026-06-05T09:00:00+01:00",
        "arrival": "2026-06-05T19:30:00+04:00"
      },
      {
        "from": "DXB",
        "to": "SIN",
        "departure": "2026-06-08T02:00:00+04:00",
        "arrival": "2026-06-08T14:00:00+08:00"
      },
      {
        "from": "SIN",
        "to": "SFO",
        "departure": "2026-06-12T23:30:00+08:00",
        "arrival": "2026-06-12T20:00:00-07:00"
      }
    ]
  }'
```

**Required:** `legs` array (2-20 legs). Each leg needs `from`, `to`, `departure`, `arrival`.
**Optional per leg:** `cabin`.

**Response data:**

| Field | Type | Description |
|-------|------|-------------|
| `legs` | array | Per-leg analysis with adjusted scores |
| `summary.total_legs` | number | Number of legs |
| `summary.total_timezone_shifts` | number | Cumulative hours shifted |
| `summary.net_offset` | number | Net timezone offset at end |
| `summary.worst_leg` | object | Leg with lowest adjusted score |
| `summary.cumulative_recovery_days` | number | Total recovery days needed |
| `summary.average_adjusted_score` | number | Average score accounting for fatigue |
| `summary.fatigue_risk` | string | low / moderate / high / severe |
| `summary.incomplete_recoveries` | number | Legs where recovery was insufficient |
| `recommendation` | string | Actionable advice |

Each leg includes: `score`, `adjusted_score` (fatigue-weighted), `cumulative_offset`, `days_since_previous`, `recovery_factor` (0-1, how recovered you were), `fatigue_multiplier`, `carryover_benefit` (same-direction bonus).

**Present to user:** Give the overall fatigue risk first. Walk through each leg noting whether recovery time was adequate. Highlight the worst leg. "Your **DXB-SIN leg** is the weak point - only 3 days after your LHR-DXB flight, your body clock is still catching up. Consider adding 1-2 days in Dubai."

---

### 10. Flight Lookup

Look up a specific flight by carrier and number. Includes jetlag scoring when schedule data is available.

```bash
curl -s "https://aerobase.app/api/v1/flights/lookup/NH/7/\?date=2026-06-10" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

**Path:** `/v1/flights/lookup/{carrier}/{number}` where carrier is the 2-letter IATA airline code and number is the flight number.
**Optional query:** `date` (YYYY-MM-DD) for date-specific schedule lookup.

**Response data:**

| Field | Type | Description |
|-------|------|-------------|
| `flight_number` | string | Full flight designator (e.g., "NH7") |
| `airline` | string | Carrier code |
| `origin` | string | Departure IATA |
| `destination` | string | Arrival IATA |
| `departure_time` | string | Departure time |
| `arrival_time` | string | Arrival time |
| `duration_minutes` | number/null | Flight duration |
| `stops` | number | Number of stops |
| `segments` | array/null | Multi-segment details (codeshares) |
| `jetlag` | object/null | score (0-100), tier, recovery_days, direction, timezone_shift |

**Present to user:** "**NH7** (ANA) SFO-NRT departs 11:00, arrives 14:30+1. Duration: 11h30m. Jetlag score: X/100 (tier), ~Y days recovery heading [direction]."

---

## Heartbeat: Deal Monitoring

Periodically check deals for the user's home airport. Run this every few hours or at the start of each session.

```bash
curl -s "https://aerobase.app/api/v1/deals?departure=SFO&sort=value_score&limit=5" \
  -H "Authorization: Bearer $AEROBASE_API_KEY"
```

If a deal has `value_score > 80` or `is_error_fare: true`, proactively mention it:

"New deal alert: **$312 SFO-Barcelona** in economy, scores 71/100 for jetlag. Error fare - may disappear soon. [source_url]"

Only surface deals that score above 50 for jetlag - a cheap flight that wrecks your sleep for a week is not a good deal.

---

## Presentation Guidelines

1. **Always mention jetlag score and recovery days** - the primary differentiators.
2. **Compare scores** when showing multiple options. Quantify the difference: "that's a full day less recovery."
3. **Highlight strategies** - users want actionable advice, not just numbers.
4. **Convert data to language** - "9 time zones heading east" not "timezone_shift_hours: 9".
5. **Context matters** - a 70 on a 2-hour domestic flight is unremarkable; 70 on transpacific is excellent.
6. **Use tier labels** - excellent, good, moderate, poor, severe.
7. **For awards** - always mention the program, miles cost, and seats remaining together.
8. **For itineraries** - focus on the weakest link and what to do about it.

## Score Interpretation

| Score | Tier | Recovery | Meaning |
|-------|------|----------|---------|
| 80-100 | Excellent | 0-1 days | Minimal jetlag, well-timed flight |
| 65-79 | Good | 1-2 days | Manageable with basic strategies |
| 50-64 | Moderate | 2-3 days | Noticeable jetlag, follow recovery plan |
| 35-49 | Poor | 3-5 days | Significant disruption expected |
| 0-34 | Severe | 5+ days | Consider alternative flight times |
