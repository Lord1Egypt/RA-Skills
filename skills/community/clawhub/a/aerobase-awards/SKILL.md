---
name: aerobase-awards
description: Search 24+ airline loyalty programs for award space with miles cost, seat availability, and jetlag scores
metadata: {"openclaw": {"emoji": "✈️", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true}}
---

# Award Flight Intelligence

## Search

**POST /api/v1/awards/search** — search seats.aero cache (286K+ rows, 24 programs)
Body: `{ origin?, destination?, program?, cabin?, dateFrom?, dateTo?, minScore? }`
Returns: jetlagScore (0-10 raw, multiply by 10 for K2), k2CabinScore, k2BaseScore,
milesCost, remaining_seats, transfer_options.
Cabin values: economy, business, premium, first (full names, NOT codes).

## Saved Award Trips

**GET /api/v1/awards/trips** — retrieve saved award trip search results
Returns previously searched award itineraries with segments, pricing, and jetlag scores.

## Alerts

- POST /api/awards/alerts — create alert
- GET /api/awards/alerts — list user's alerts
- Continuous alerts require Pro tier

## Program Intelligence

24 programs: Copa, Aeromexico, Ethiopian, United, Delta, American, BA, Lufthansa, AF/KLM, etc.
Cross-reference user's credit card portfolio with transfer partner map.

## Always

- Present prices in miles/points, not cash
- Include jetlag score alongside every result
- Warn about fuel surcharges on BA, LH, AF awards
- Calculate cents-per-point value: "Business to Tokyo is 75K Aeroplan. Cash price is $3,200.
  That's 4.3 cents/point — excellent value, your points are worth more here than average."
- When comparing cash vs. points: "The economy option saves 50K miles but the 11 PM departure
  scores 7.8 — four days of zombie mode. The business seat literally buys you three productive days."

## Rate Limits

- Award search: max 20/hr. Alert create: max 10 alerts per user total.
- Award monitoring cron: every 4 hours (do not increase). Batch route queries where possible.

## Scrapling — Cash Price Lookup for CPP Calculation

Use Scrapling `/search` to get cash prices from Google Flights for cents-per-point value:

Reference: [Scrapling Documentation](https://scrapling.readthedocs.io/en/latest/overview.html)

```
POST {SCRAPLING_URL}/search
{"site":"google-flights","origin":"JFK","destination":"LHR","departure":"2026-04-01","return":"2026-04-08"}
```
Returns: `{"results": [{"price":"€488","duration":"6 hr 50 min","stops":"Nonstop"}], "count": 48}`

### CPP Calculation Workflow
1. Get award price from seats.aero API (e.g., 60K Aeroplan)
2. Fire Scrapling Google Flights search for same route
3. Extract cash price (EUR from Helsinki — convert to USD if needed)
4. Calculate: `cash_price_usd / miles_required * 100 = cents_per_point`
5. Present: "Business to London is 60K Aeroplan. Cash price is $543. That's 0.9 cpp."

### seats.aero (API preferred, browser fallback with PROXY)
Cloudflare protected. Use API cache first. Browser via proxy only for logged-in users.

### Airline Award Search (PROXY required)
- Navigate to airline's FFP booking page (behind login wall)
- User must provide credentials for their account
- NEVER store or log FFP credentials

### When to SKIP browser entirely
- General award search → seats.aero API cache is comprehensive
- Award alerts → API handles this automatically
- Program comparisons → API data is sufficient
- Only use browser for visual verification or cash-price lookup
