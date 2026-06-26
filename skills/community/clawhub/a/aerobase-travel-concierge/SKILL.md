---
version: 3.3.1
name: aerobase-travel-concierge
description: Complete AI travel concierge covering flights, hotels, lounges, awards, activities, deals, wallet, and recovery
metadata: {"openclaw": {"emoji": "⭐", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Travel Concierge ⭐ ALL-IN-ONE

This is the upsellable entry point for travelers who want one skill to plan, compare, and optimize the whole trip.

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

- Run one coordinated trip workflow: flights, hotel stays, lounge planning, awards, deals, wallet value, and accelerated jetlag recovery.
- Keep outputs brief and prioritizing “next best action” for the traveler.

## API-first capability map

### Flight Search & Scoring
- POST `/api/v1/flights/search`
- POST `/api/v1/flights/compare`
- POST `/api/v1/flights/score`
- POST `/api/flights/search/agent`

### Award Search
- POST `/api/v1/awards/search`
- GET `/api/v1/awards/trips`
- GET `/api/awards/alerts`
- POST `/api/awards/alerts`

### Airport Lounges
- GET `/api/v1/lounges`
- GET `/api/airports/{code}/lounges`

### Hotels & Booking
- GET `/api/v1/hotels` — search with filters
- GET `/api/v1/hotels/near-airport/{code}` — airport-adjacent hotels
- POST `/api/v1/hotels/rates` — live rates (hotelIds or airportCode)
- POST `/api/v1/hotels/prebook` → `POST /api/v1/hotels/book` — full booking flow
- GET `/api/v1/hotels/bookings/{id}`, DELETE to cancel
- GET `/api/dayuse?airport={code}` — day-use hotels

### Activities
- GET `/api/attractions`
- GET `/api/attractions/{slug}/tours`
- GET `/api/tours`

### Deals
- GET `/api/v1/deals`
- POST `/api/deals/alerts`
- GET `/api/deals/alerts`

### Wallet & Cards
- GET `/api/v1/credit-cards`
- GET `/api/transfer-bonuses`
- GET `/api/wallet/summary`
- GET `/api/user-loyalty-programs`

### Jetlag Recovery
- POST `/api/v1/recovery/plan`

Use canonical `jetlagScore` on a `0-100` scale across flight and award decisions, and treat `recoveryDays` as accelerated functional recovery. A value of `0` means negligible circadian disruption.

## Safety and tone

- Do not collect passwords, OTPs, loyalty logins, or any account secrets.
- Never expose internal keys in responses.
- Keep recommendations concise, reversible, and safe: suggest alternatives when confidence is low.

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for air travel and travel-specific sites:
- Automated airline check-in before flights (Delta, BA, Southwest)
- Automated tracking of awards, points, miles, and loyalty balances
- Live Google Flights/Kayak price comparison
- Real-time deal feeds from SecretFlying, TheFlightDeal, TravelPirates
- Booking.com and Google Hotels price comparison
- Priority Pass real-time lounge verification
- TripAdvisor activity discovery
- SeatGuru seat quality lookup
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
