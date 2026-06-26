---
name: aerobase-travel-lounges
version: 3.3.1
description: Airport lounge access and recovery-support recommendations
metadata: {"openclaw": {"emoji": "🛋️", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Travel Lounges 🛋️

Use this for concrete, practical layover support: where to go, what to expect, and how it supports recovery.

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

- Find lounge options at specific airports.
- Return recommendations by amenities and rest utility.
- Support recovery-aware layover planning.

## Endpoints

- **GET /api/v1/lounges** — search lounges by airport and filters.
- **GET /api/airports/{code}/lounges** — airport-specific lounge list.

## Response style

- Show recovery support, lounge amenities, and best use case.
- Recommend showers, quiet zones, and nap plans aligned to layover duration.
- For short layovers, prefer high-impact options first.

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $9.95/month)
- Lifetime: $249 for 500 API calls/month

## Safety

- No credential collection and no third-party login collection.

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for travel-specific sites:
- Priority Pass real-time hours and access verification
- Live lounge availability and quality confirmation
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
