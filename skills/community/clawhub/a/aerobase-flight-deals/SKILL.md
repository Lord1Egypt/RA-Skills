---
version: 3.2.0
name: aerobase-flight-deals
description: Find cheap flights, monitor prices, and alert on price drops
metadata: {"openclaw": {"emoji": "💰", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Flight Deals 💰

Use this skill for shopping, ranking, and tracking fare movement so users get the right flight value at the right moment.

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

- Search live and saved-route deals from Aerobase deal data.
- Compare options by price, value score, and jetlag recovery impact.
- Create, list, and manage watch alerts for meaningful price drops.

## Deal search

**GET /api/v1/deals**  
Query params:
- `origin` departure IATA code
- `destination` destination IATA code
- `max_price` maximum price in USD
- `min_score` minimum value score
- `max_recovery_days` max recovery window
- `date_from` travel date start
- `date_to` travel date end
- `sort` (`value_score`, `price`, `jetlag_score`, `newest`)
- `limit` up to 50

## Deal alerts

- **POST /api/deals/alerts** — create a watch alert for a route/date strategy
- **GET /api/deals/alerts** — list active user alerts

## Output pattern

- Show route + travel window + fare + airline first.
- Add `jetlag_score` and recovery recommendations inline.
- For long layover routes, call out whether price gain comes with recovery burden.

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $9.95/month)
- Lifetime: $249 for 500 API calls/month

Monitoring checks remain triggered based on route watch setup.

## Safety

- Do not request credentials, account numbers, or saved logins.
- Do not instruct users to provide private account details or one-time tokens.

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for travel deal sites:
- Real-time deal feeds from SecretFlying, TheFlightDeal, TravelPirates, and Going.com
- Google Flights price verification for deal confirmation
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
