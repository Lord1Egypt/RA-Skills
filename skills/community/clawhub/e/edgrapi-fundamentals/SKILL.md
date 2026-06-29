---
name: edgrapi-fundamentals
version: 1.0.0
description: Normalized company financial statements and computed ratios from SEC EDGAR via Edgrapi.com. Pull clean income/balance/cash-flow figures and margin/return/leverage/liquidity ratios for any US-listed ticker, parsed from EDGAR XBRL.
license: MIT-0
author: Edgrapi
homepage: https://edgrapi.com
repository: https://github.com/paperandbeyond23-gif/edgrapi-skills
tags:
  - edgrapi
  - sec-edgar
  - fundamentals
  - financial-statements
  - ratios
  - xbrl
  - equity-research
  - api
metadata:
  openclaw:
    primaryEnv: EDGRAPI_KEY
    homepage: https://edgrapi.com
    requires:
      env:
        - EDGRAPI_KEY
---

# edgrapi-fundamentals

Clean financial statements and ratios from SEC EDGAR via [Edgrapi.com](https://edgrapi.com). The focused two-tool variant of `edgrapi-full` — install this when you only need the numbers, not filings/profile lookups.

Use when the user **explicitly asks** for a US-listed company's financials: revenue, net income, assets, debt, cash flow, EPS, margins, ROE/ROA, leverage, or liquidity.

## When to use this skill

Each call spends one Edgrapi credit (1 credit = 1 request). Activate only for a genuine financials request about a specific company — not when a ticker appears in passing, and not for live stock **prices** (Edgrapi is filings-derived fundamentals, not a price feed).

## Tools

### `get_fundamentals`
Normalized income-statement, balance-sheet, and cash-flow figures, parsed from EDGAR XBRL companyfacts. Args: `ticker` (required), `period` (`annual` | `quarterly`, default `annual`), `limit` (1–20, default 5). Periodized by fiscal period end, in USD.

### `get_ratios`
Margins, returns, leverage, and liquidity ratios derived from the fundamentals. Args: `ticker` (required). Price-based ratios (P/E, P/B) are **not** included — EDGAR carries no market price.

## Authentication

Set `EDGRAPI_KEY` to your Edgrapi key (`edgr_...`), sent as the `X-API-Key` header.

```bash
export EDGRAPI_KEY="edgr_..."
```

Free key (100 free credits, no card) at <https://edgrapi.com/app>.

## Pricing

Free 100 one-time · Pro $29/mo (60k credits) or $290/yr (720k) · top-up packs from $7. 1 credit = 1 call. See <https://edgrapi.com/pricing>.

## Errors

Functions return a dict; on failure it has an `error` key: `auth_required`, `auth_invalid`, `ticker_not_found`, `out_of_credits`, `rapidapi_only`, `edgar_unavailable`, `network`, `HTTP <code>`, `unexpected`.

## Independence

Edgrapi is an independent service, not affiliated with or endorsed by the U.S. SEC. All data originates from the SEC's public EDGAR system.
