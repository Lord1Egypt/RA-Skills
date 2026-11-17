---
name: edgrapi-full
version: 1.1.0
description: All five US government sources via Edgrapi.com. Nine tools — SAM.gov contract opportunities, USAspending awards, Grants.gov funding and US House STOCK Act trades, plus normalized SEC EDGAR fundamentals, ratios, company profiles and filings, on one key and one JSON schema.
license: MIT-0
author: Edgrapi
homepage: https://edgrapi.com
repository: https://github.com/paperandbeyond23-gif/edgrapi-skills
tags:
  - edgrapi
  - government-data
  - sam-gov
  - usaspending
  - grants-gov
  - govcon
  - stock-act
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

All five US government sources via [Edgrapi.com](https://edgrapi.com) on one key: federal contract
opportunities, awards, grants, congressional trades, and SEC EDGAR financials. Use when the user
**explicitly asks** for any of those and wants real, sourced records rather than a guess.

For government data only, the focused [`edgrapi-gov`](../edgrapi-gov) skill has the same five
government tools with a smaller surface.

EDGAR is free but its XBRL company-facts payloads are brutal to parse (tag drift, mixed periods, trailing-twelve-month windows hiding inside 10-Qs). Edgrapi normalizes all of that into clean JSON, keyed by fiscal period.

## When to use this skill

Credits are weighted by endpoint rather than one per request, so this skill activates only when the request is genuinely about a company's financials — not when a ticker merely appears in passing.

**DO use when the user:**

- Asks what federal contracts are open, by industry, set-aside or state → `get_opportunities`
- Asks who won federal work, or what an agency or company has been paid → `get_awards`
- Asks about federal grant funding or a CFDA / Assistance Listing number → `get_grants`
- Asks what members of Congress have been trading → `get_congress`, `get_congress_ticker`
- Asks for revenue, net income, assets, debt, cash flow, EPS, etc. for a company → `get_fundamentals`
- Asks for margins, returns (ROE/ROA), leverage, or liquidity ratios → `get_ratios`
- Asks who/what a filer is — CIK, industry, fiscal-year end, exchange → `get_company`
- Asks for a company's recent 10-K / 10-Q / 8-K filings → `get_filings`

**Do NOT use when:**

- A ticker or company name appears incidentally (news, a portfolio list, small talk)
- The user wants a live stock **price** or market cap — Edgrapi is fundamentals from filings, not a price feed
- The user wants **state or local** procurement — this is federal only, there is no SLED coverage
- The user wants **Senate** trading disclosures — congressional data here is US House only
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

### `get_opportunities` — open federal contract opportunities (SAM.gov)
Args: `posted_from`, `posted_to` (YYYY-MM-DD, default last 30 days), `limit`, `offset`, `naics`, `ptype` (`o`|`p`|`a`), `state`, `set_aside` (e.g. `SBA`, `8A`, `WOSB`), `title`. Pass `naics` plainly — SAM.gov's own API wants `ncode` and silently ignores `naics`; that translation is handled for you.

### `get_awards` — federal awards (USAspending)
Args: `category` (`contracts`|`idvs`|`grants`|`loans`|`direct_payments`|`other`), `keyword`, `agency`, `recipient`, `state`, `start`, `end`, `limit`, `page`, `sort`, `order`. Search cannot reach before 2007-10-01.

### `get_grants` — federal grant opportunities (Grants.gov)
Args: `keyword`, `status` (`forecasted`|`posted`|`closed`|`archived`, pipe or comma separated), `agency`, `category`, `eligibility`, `aln` (CFDA, e.g. `93.217`), `limit`, `offset`.

### `get_congress` / `get_congress_ticker` — congressional stock trades
Args: `action` (`buy`|`sell`, optional), `limit`; or `ticker` (required) and `limit`. **US House only**, up to 45 days behind by law, amounts as dollar ranges rather than exact figures — state those limits whenever you report this data.

## Authentication

Set `EDGRAPI_KEY` to your Edgrapi key. Keys are `edgr_...` strings, sent as the `X-API-Key` header.

```bash
export EDGRAPI_KEY="edgr_..."
```

Get a free key (100 credits every month, no card required) at <https://edgrapi.com/app>.

## Pricing

Credits are weighted by endpoint, not one per request: company, filings, events, entity resolution
and full-text search cost 1; fundamentals, ratios and XBRL cost 3; sections, insider, holdings and
activist cost 5. Credits never expire. All data is from public SEC EDGAR.

| Plan | Price | Credits |
|---|---|---|
| Free | $0 | 100 / month |
| Starter | $10/mo | 10,000 / month |
| Pro (monthly) | $29/mo | 30,000 / month |
| Pro (annual) | $290/yr | 360,000 up front |

Top-up packs (one-time, never expire): 5,000 / $7 · 15,000 / $18 · 50,000 / $55.

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
