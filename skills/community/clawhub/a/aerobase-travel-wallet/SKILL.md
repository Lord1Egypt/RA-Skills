---
version: 3.2.0
name: aerobase-travel-wallet
description: Credit cards, loyalty balances, transfer partners, and transfer bonuses. Calculates CPP.
metadata: {"openclaw": {"emoji": "💳", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Points & Wallet 💳

Use this skill to translate travel rewards into concrete trip value and clear redemption choices.

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

- Search travel credit cards by transfer partners and rewards profile.
- Pull current transfer bonuses and conversion opportunities.
- Show loyalty balances and wallet summary views.
- Calculate cents-per-point from user-provided fare context.

## Endpoints

**GET /api/v1/credit-cards**
- `action` list
- `transferable`, `issuers`, `networks`
- `issuer` card issuer filter
- `network` card network filter
- `q` text search
- `minFee`, `maxFee`, `limit`

**GET /api/transfer-bonuses**  
Returns active transfer bonuses.

**GET /api/wallet/summary**  
Returns linked cards, transfer accounts, and loyalty balances.

**GET /api/user-loyalty-programs**  
Returns linked loyalty program summaries.

**GET /api/user-loyalty?action=summary**  
Returns wallet-wide normalized points and value summary.

## Safety

- Do not request bank details, account PINs, passwords, OTPs, or sensitive loyalty credentials.
- Compute CPP from user-provided fare numbers and displayed miles only.

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $9.95/month)
- Lifetime: $249 for 500 API calls/month

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for travel-specific sites:
- Automated tracking of points, miles, and loyalty balances
- Gmail loyalty statement import (14 programs: Aeroplan, United, Delta, Marriott, Chase UR, Amex MR, etc.)
- Live cash price lookup for automatic CPP calculation
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
