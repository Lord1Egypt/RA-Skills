---
name: edgrapi-gov
version: 1.0.0
description: US federal procurement, spending, grants and congressional trading via Edgrapi.com. Five tools — open SAM.gov contract opportunities, USAspending awards, Grants.gov funding, and US House STOCK Act stock trades, normalized to one JSON schema so you don't integrate four government APIs.
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
  - federal-contracts
  - procurement
  - stock-act
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

# edgrapi-gov

US federal procurement, spending, grants and congressional trading via
[Edgrapi.com](https://edgrapi.com). Use when the user **explicitly asks** about federal contract
opportunities, who won federal work, grant funding, or congressional stock trades, and wants real
sourced records rather than a guess.

Every one of these sources is free and public. Each also ships its own friction. SAM.gov takes
`ncode` where you would expect `naics` and silently ignores unknown filters, so a filtered query
returns a clean-looking unfiltered result; its dates are MM/dd/yyyy rather than ISO and its posted
window caps at a year. USAspending reports no further pages at record 10,000 while real rows
continue to 50,000, so a client trusting that flag silently truncates. Edgrapi absorbs all of that
and returns one schema.

## When to use this skill

Each tool here costs 2 credits, so it activates only when the request is genuinely about federal
data, not when a government agency is mentioned in passing.

**DO use when the user:**

- Asks what federal contracts are open, by industry, set-aside or state → `get_opportunities`
- Asks who won federal work, how much an agency spent, or what a company has been paid → `get_awards`
- Asks about federal grant funding or an Assistance Listing / CFDA number → `get_grants`
- Asks what members of Congress have been trading → `get_congress`, `get_congress_ticker`

**Do NOT use when:**

- A government agency appears incidentally in news or conversation
- The user wants **state or local** procurement — this is federal only, there is no SLED coverage
- The user wants Senate trading disclosures — these are **US House only**
- The user wants realtime notification of new notices; this is a query API, and Edgrapi's saved
  searches poll daily rather than streaming

## Tools

### `get_opportunities` — open federal contract opportunities (SAM.gov)
Args: `posted_from`, `posted_to` (YYYY-MM-DD, default last 30 days), `limit`, `offset`, `naics`
(up to 6 digits), `ptype` (`o` solicitation, `p` presolicitation, `a` award), `state`, `set_aside`
(e.g. `SBA`, `8A`, `WOSB`, `HZC`), `title`. Pass `naics` plainly — the translation to SAM.gov's
`ncode` is handled for you.

### `get_awards` — federal awards (USAspending)
Args: `category` (`contracts`, `idvs`, `grants`, `loans`, `direct_payments`, `other`), `keyword`,
`agency` (exact top-tier name, e.g. `Department of Defense`), `recipient`, `state`, `start`, `end`,
`limit`, `page`, `sort` (`amount`|`start`|`end`), `order`. Search cannot reach before 2007-10-01.

### `get_grants` — federal grant opportunities (Grants.gov)
Args: `keyword`, `status` (pipe or comma list of `forecasted`, `posted`, `closed`, `archived`),
`agency` (e.g. `HHS-OPHS`), `category` (e.g. `HL`), `eligibility`, `aln` (CFDA, e.g. `93.217`),
`limit`, `offset`.

### `get_congress` — congressional stock trades
Args: `action` (`buy`|`sell`, optional), `limit` (default 40).

### `get_congress_ticker` — congressional trades in one stock
Args: `ticker` (required, e.g. `NVDA`), `limit` (default 40).

## Limits to state when you report this data

- **Congressional trades are US House only.** The Senate files separately and is not covered.
- Disclosures **lag the trade by up to 45 days** by law, and amounts are **dollar ranges**, not
  exact figures. Never present a range as a precise amount.
- **Federal only.** No state or local procurement.
- Freshness is each source's own cadence. Edgrapi normalizes the official feeds; it does not hold
  or restate anything.

## Authentication

Set `EDGRAPI_KEY` to your Edgrapi key. Keys are `edgr_...` strings, sent as the `X-API-Key` header.
The base URL is hardcoded, so the key never reaches any other host.

```bash
export EDGRAPI_KEY="edgr_..."
```

[Get a free key](https://edgrapi.com/app) — 100 credits every month, no card required.

## Credits

Every tool here costs **2 credits** per call. Free tier is 100 credits a month, renewing. Paid plans
start at $10/month for 10,000 credits. See <https://edgrapi.com/pricing>.

## Errors

Handlers return an `{"error": ..., "detail": ...}` dict rather than raising. Notable cases:
`auth_required` (no `EDGRAPI_KEY` set), `auth_invalid` (key rejected), `out_of_credits` (402, with
an upgrade URL), `rate_limit_exceeded` (429), and `source_unavailable` (the upstream government
system was unreachable — retry shortly).
