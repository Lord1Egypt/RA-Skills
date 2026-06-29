---
name: edgrapi-full
version: 1.0.0
description: Clean company financials from SEC EDGAR via Edgrapi.com. Four tools — pull normalized income/balance/cash-flow fundamentals, computed ratios, company profiles, and recent SEC filings for any US-listed ticker, parsed from EDGAR XBRL so you don't have to.
license: MIT-0
author: Edgrapi
homepage: https://edgrapi.com
repository: https://github.com/paperandbeyond23-gif/edgrapi-skills
tags:
  - edgrapi
  - sec-edgar
  - financial-data
  - fundamentals
  - financial-statements
  - xbrl
  - stocks
  - equity-research
  - api
  - mcp
metadata:
  openclaw:
    primaryEnv: EDGRAPI_KEY
    homepage: https://edgrapi.com
    requires:
      env:
        - EDGRAPI_KEY
---

# edgrapi-full

Clean company financials from SEC EDGAR via [Edgrapi.com](https://edgrapi.com). Use when the user **explicitly asks** for a US-listed company's financial statements, fundamentals, ratios, profile, or recent SEC filings — and wants real, sourced numbers rather than a guess.

EDGAR is free but its XBRL company-facts payloads are brutal to parse (tag drift, mixed periods, trailing-twelve-month windows hiding inside 10-Qs). Edgrapi normalizes all of that into clean JSON, keyed by fiscal period.

## When to use this skill

Each tool call spends one Edgrapi credit (1 credit = 1 request), so this skill activates only when the request is genuinely about a company's financials — not when a ticker merely appears in passing.

**DO use when the user:**

- Asks for revenue, net income, assets, debt, cash flow, EPS, etc. for a company → `get_fundamentals`
- Asks for margins, returns (ROE/ROA), leverage, or liquidity ratios → `get_ratios`
- Asks who/what a filer is — CIK, industry, fiscal-year end, exchange → `get_company`
- Asks for a company's recent 10-K / 10-Q / 8-K filings → `get_filings`

**Do NOT use when:**

- A ticker or company name appears incidentally (news, a portfolio list, small talk)
- The user wants a live stock **price** or market cap — Edgrapi is fundamentals from filings, not a price feed
- The user is discussing markets abstractly without a specific company

When intent is ambiguous, confirm the ticker before calling.

## Tools

### `get_fundamentals` — income, balance sheet, cash flow
Normalized financial statements for a ticker, parsed from EDGAR XBRL companyfacts. Args: `ticker` (required), `period` (`annual` | `quarterly`, default `annual`), `limit` (1–20 periods, default 5). Returns statements periodized by fiscal period end, in USD.

### `get_ratios` — computed ratios
Margins, returns, leverage, and liquidity ratios derived from the fundamentals. Args: `ticker` (required). Price-based ratios (P/E, P/B) are **not** included — EDGAR carries no market price.

### `get_company` — filer profile
CIK, legal name, SIC industry, fiscal-year end, exchanges, and website, resolved from EDGAR submissions. Args: `ticker` (required).

### `get_filings` — recent SEC filings
Recent filings with filing/report dates and document links. Args: `ticker` (required), `limit` (1–100, default 20), `form` (optional filter, e.g. `10-K`, `10-Q`, `8-K`).

## Authentication

Set `EDGRAPI_KEY` to your Edgrapi key. Keys are `edgr_...` strings, sent as the `X-API-Key` header.

```bash
export EDGRAPI_KEY="edgr_..."
```

Get a free key (100 free credits, no card required) at <https://edgrapi.com/app>.

## Pricing

1 credit = 1 request. Credits never expire. All data is from public SEC EDGAR.

| Plan | Price | Credits |
|---|---|---|
| Free | $0 | 100 one-time |
| Pro (monthly) | $29/mo | 60,000 / mo |
| Pro (annual) | $290/yr | 720,000 up front |

Top-up packs (one-time, never expire): 10,000 / $7 · 30,000 / $18 · 100,000 / $55.

Manage plans at <https://edgrapi.com/pricing>. Also available metered on RapidAPI.

## Errors

All functions return a Python dict. On success it's the API response; on failure it has an `error` key:

- `{"error": "auth_required", ...}` — `EDGRAPI_KEY` not set (includes `signup_url`)
- `{"error": "auth_invalid", ...}` — key rejected; mint a new one at `/app`
- `{"error": "ticker_not_found", ...}` — no SEC filer matches that ticker
- `{"error": "out_of_credits", ...}` — credit balance exhausted; includes `upgrade_url` to top up or subscribe
- `{"error": "rapidapi_only", ...}` — origin locked to RapidAPI subscribers
- `{"error": "edgar_unavailable", ...}` — SEC EDGAR was unreachable upstream; retry
- `{"error": "network" | "HTTP <code>" | "unexpected", ...}` — transport / other failures

## API reference

- Docs: <https://edgrapi.com/docs>
- OpenAPI spec: <https://edgrapi.com/openapi.json>
- Pricing: <https://edgrapi.com/pricing>

## Independence

Edgrapi is an independent service and is not affiliated with, endorsed by, or sponsored by the U.S. Securities and Exchange Commission. All data originates from the SEC's public EDGAR system. "EDGAR" is a system operated by the U.S. SEC.
