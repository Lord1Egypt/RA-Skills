---
version: 3.3.1
name: aerobase-jetlag
description: Jetlag recovery optimization - score flights, generate recovery plans, optimize travel timing
metadata: {"openclaw": {"emoji": "😴", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Jetlag Recovery 😴

This skill makes jetlag decisions actionable: score fatigue impact, then return an easy recovery plan users can execute the same day.

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

- Score any flight for jetlag impact (`0-100`).
- Generate personalized recovery plans.
- Suggest timing, sleep adjustments, and in-flight routines.
- Estimate accelerated functional recovery days.
- Treat `0` recovery days as negligible circadian disruption, not missing data.

## Endpoints

- **POST /api/v1/flights/score** — score a flight for jetlag impact with canonical `jetlagScore` (`0-100`).
- **POST /api/v1/recovery/plan** — generate a personalized accelerated recovery plan.

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $9.95/month)
- Lifetime: $249 for 500 API calls/month

## Example usage pattern

- User asks: "How hard is LHR → JFK on this option?"  
  Use `/api/v1/flights/score`.
- User asks: "Help me recover better"  
  Use `/api/v1/recovery/plan` with their likely sleep window and timezone context.
- For `0-2h` shifts, frame results as minimal/negligible circadian disruption rather than a full jetlag reset problem.

## Safety

- Never infer or request secrets.
- Keep the plan practical: clear action list, no unsafe medical or dosing recommendations.
- Offer alternatives when recovery burden is high (later departure, longer stay buffer, airport adjustments).

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for travel-specific sites:
- Calendar sync with body clock conflict detection at destination
- Gmail import auto-extracts flights for recovery plan generation
- Day-by-day itinerary planning with jetlag-phased scheduling
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
