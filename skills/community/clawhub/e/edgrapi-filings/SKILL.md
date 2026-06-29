---
name: edgrapi-filings
version: 1.0.0
description: Company profiles and recent SEC filings from EDGAR via Edgrapi.com. Resolve a US-listed ticker to its CIK, industry, fiscal-year end, and exchange, and list its recent 10-K / 10-Q / 8-K filings with document links.
license: MIT-0
author: Edgrapi
homepage: https://edgrapi.com
repository: https://github.com/paperandbeyond23-gif/edgrapi-skills
tags:
  - edgrapi
  - sec-edgar
  - filings
  - 10-k
  - 10-q
  - 8-k
  - company-profile
  - api
metadata:
  openclaw:
    primaryEnv: EDGRAPI_KEY
    homepage: https://edgrapi.com
    requires:
      env:
        - EDGRAPI_KEY
---

# edgrapi-filings

Company profiles and recent SEC filings from EDGAR via [Edgrapi.com](https://edgrapi.com). The focused two-tool variant of `edgrapi-full` — install this when you need filer metadata and disclosure history, not financial statements.

Use when the user **explicitly asks** who/what a filer is (CIK, industry, fiscal-year end, exchange) or for a company's recent SEC filings.

## When to use this skill

Each call spends one Edgrapi credit (1 credit = 1 request). Activate only for a genuine lookup about a specific company — not when a ticker appears in passing.

## Tools

### `get_company`
CIK, legal name, SIC industry, fiscal-year end, exchanges, and website, resolved from EDGAR submissions. Args: `ticker` (required).

### `get_filings`
Recent filings with filing/report dates and document links. Args: `ticker` (required), `limit` (1–100, default 20), `form` (optional filter, e.g. `10-K`, `10-Q`, `8-K`).

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
