---
version: 3.3.1
name: aerobase-travel-flights
description: Search, compare, and score flights with jetlag optimization
metadata: {"openclaw": {"emoji": "🛫", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Travel Flights 🛫

Use this when users want the fastest, highest-confidence way to compare flights with jetlag awareness.

## Setup

Use this skill by getting a free API key at https://aerobase.app/openclaw-travel-agent and setting `AEROBASE_API_KEY` in your agent environment.
This skill is API-only: no scraping, no browser automation, and no user credential collection.

Usage is capped at 5 requests/day for free users.
Upgrade to Pro ($9.95/month) at https://aerobase.app/openclaw-travel-agent for 500 API calls/month.

## Agent API Key Protocol

- Base URL: `https://aerobase.app`
- Required env var: `AEROBASE_API_KEY`
- Auth header (preferred): `Authorization: Bearer ${AEROBASE_API_KEY}`
- Never ask users for passwords, OTPs, cookies, or third-party logins.
- Never print raw API keys in output; redact as `sk_live_***`.

### Request rules

- Use only Aerobase endpoints documented in this skill.
- Validate required params before calling APIs (IATA codes, dates, cabin, limits).
- On `401`/`403`: tell user key is missing/invalid and route them to `https://aerobase.app/openclaw-travel-agent`.
- On `429`: explain free-tier quota (`5 requests/day`) and suggest Pro (`$9.95/month`, 500 API calls/month) or Lifetime ($249, 500 API calls/month).
- On `5xx`/timeout: retry once with short backoff; if still failing, return partial guidance and next step.
- Use concise responses: top options first, then 1-2 follow-up actions.

## What this skill does

- Search flights by route/date with canonical jetlag scoring context.
- Compare alternatives and highlight better accelerated recovery options.
- Validate fare offers before user booking action.

## Search API

**POST /api/v1/flights/search**

Body: `{ from, to, date, return_date?, max_stops?, sort?, limit? }`  
Accepted sort values:
- `price`
- `duration`

Free tier: 5 results. Concierge mode: 50 results.

**POST /api/flights/search/agent** — multi-provider parallel search.

## Booking support

- **POST /api/v1/flights/validate** — pre-booking price and seatability check.
  Body: `{ bookingToken, provider? }`
  Returns: `{ available, currentPrice, priceChanged }`

- **POST /api/v1/flights/book** — place booking request (zooz credit card flow).
  Body: `{ bookingToken, passengers: [{firstName, lastName, email, phone, birthday, title, nationality?, documentNumber?, documentExpiry?}], payment?: {cardNumber, expiry, cvv, holderName, currency?} }`
  Returns: `{ action, bookingId, providerReference, totalPrice, message }`
  Actions: `booked`, `redirect`, `re-search`, `confirm_price_change`, `failed`

- **GET /api/v1/flights/bookings** — list your bookings with status.
  Query: `?limit=20&offset=0`

- **GET /api/v1/flights/bookings/{id}** — booking detail with webhook history.

- Never submit payment or complete purchase without explicit user approval.

## Compare & score

- **POST /api/v1/flights/compare** — compare multiple flight options.
- **POST /api/v1/flights/score** — score any single flight with canonical `jetlagScore` (`0-100`) and accelerated recovery impact.

For `0-2h` shifts, treat results as minimal/negligible circadian disruption rather than a full jetlag reset problem.

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $9.95/month)
- Lifetime: $249 for 500 API calls/month

## Safety

- Do not request user account passwords, OTPs, or payment credentials.
- Ask before any booking-related action.

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for air travel sites:
- Live Google Flights and Kayak price comparison
- Concurrent multi-source search for comprehensive results
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
