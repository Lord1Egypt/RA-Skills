---
name: brickeconomy
description: Use the BrickEconomy API through the included CLI for LEGO set/minifig valuation, collection performance, and sales-ledger analysis from verified Brick Directory references.
version: 1.0.0
---

# BrickEconomy AFOL skill

Use this skill when the user asks about LEGO set values, minifig values, BrickEconomy collection valuation, collection growth, investment performance, forecasts, ROI, or sales-ledger profit/loss.

Primary interface: `scripts/brickeconomy`.

The skill is self-contained for archive distribution and wraps the BrickEconomy API directly using checked-in references inside this skill directory:
- OpenAPI reference: `references/openapi/brickeconomy.yaml`
- Domain guidance: `references/prompts/brickeconomy-tools.txt`
- CLI source: `scripts/brickeconomy_cli.py`

Do not scrape vendor docs or invent parameters when the checked-in OpenAPI reference covers the endpoint. If the reference is insufficient, say what is missing.

## Authentication

Required environment variable:

```bash
export BRICKECONOMY_API_KEY=...
```

Optional override:

```bash
export BRICKECONOMY_BASE_URL=https://www.brickeconomy.com/api/v1
```

Never print, commit, log, or paste the real API key. Commands should reference `$BRICKECONOMY_API_KEY` only indirectly through the CLI.

BrickEconomy auth placement matters: every API call sends the key as the `x-apikey` HTTP header, not as a query parameter or form field. The CLI handles that, which is the main reason to use it instead of ad-hoc curl.

## CLI quick reference

Run commands from this skill directory:

```bash
scripts/brickeconomy --help
scripts/brickeconomy set --set-number 10236-1 --currency EUR
scripts/brickeconomy minifig --minifig-number sw0509 --currency USD
scripts/brickeconomy collection-sets --currency EUR
scripts/brickeconomy collection-minifigs --currency EUR
scripts/brickeconomy sales-ledger
```

All commands are read-only. Use `--dry-run` to inspect request shape without requiring an API key or calling BrickEconomy:

```bash
scripts/brickeconomy set --dry-run --set-number 10236-1 --currency EUR
scripts/brickeconomy sales-ledger --dry-run
```

## Safety rules

The checked-in BrickEconomy spec for this skill contains only read-only `GET` endpoints:
- `set`
- `minifig`
- `collection-sets`
- `collection-minifigs`
- `sales-ledger`

There are no collection mutation, marketplace listing, order update, wishlist, delete, or bulk-update endpoints in this skill archive.

Still be careful:
- Treat returned collection and sales-ledger data as private financial/account data.
- Do not call personal collection or sales-ledger endpoints unless the user asked for personal collection, ROI, or sales analysis.
- Do not fan out across many set/minifig lookups unless the user asked for bulk analysis and the 100 requests/day, 4 requests/minute limit budget is acceptable.
- If a future BrickEconomy reference adds mutating endpoints, require explicit user confirmation in the current conversation and a mechanical guard such as `--yes`; keep `--dry-run` available.

## Endpoint coverage

| Workflow | CLI command | Method/path | Operation | Notes |
|---|---|---|---|---|
| Set value | `set --set-number 10236-1 --currency EUR` | `GET /set/{setNumber}` | `getSet` | Accepts set numbers with or without variant suffix, for example `10236` or `10236-1`. Supports optional `currency`. |
| Minifig value | `minifig --minifig-number sw0509 --currency USD` | `GET /minifig/{minifigNumber}` | `getMinifig` | Accepts BrickEconomy minifig numbers such as `sw0509`. Supports optional `currency`. |
| Collection sets | `collection-sets --currency EUR` | `GET /collection/sets` | `getCollectionSets` | Returns all authenticated set collection entries with paid price, current value, growth, acquisition, condition, and collection fields. |
| Collection minifigs | `collection-minifigs --currency EUR` | `GET /collection/minifigs` | `getCollectionMinifigs` | Returns all authenticated minifig collection entries with paid price, current value, growth, acquisition, and collection fields. |
| Sales ledger | `sales-ledger` | `GET /salesledger` | `getSalesLedger` | Returns set and minifig sale records with sale price, fees/shipping, quantity, buy price, dates, condition, and notes. No `currency` parameter is defined for this endpoint in the spec. |

Supported currency codes from the spec: `USD`, `GBP`, `CAD`, `AUD`, `CNY`, `KRW`, `EUR`, `JPY`, `CHF`, `INR`, `BRL`, `RUB`, `ZAR`, `MXN`, `SGD`, `HKD`, `SEK`, `NZD`, `NOK`, `TRY`, `DKK`, `PLN`. API default is `USD`.

Known BrickEconomy limits from `references/prompts/brickeconomy-tools.txt`: 100 requests/day and 4 requests/minute. Be stingy: one collection call is better than N individual set calls when analyzing a user's portfolio.

## Analysis rules

All analysis must be grounded in API response fields. Do not fill missing values from memory, web search, BrickLink, or another provider unless the user explicitly asks for multi-provider fallback and you name the source.

For set value responses, use fields such as:
- `current_value_new`, `current_value_used`, `current_value_used_low`, `current_value_used_high`
- `forecast_value_new_2_years`, `forecast_value_new_5_years`
- `rolling_growth_lastyear`, `rolling_growth_12months`
- `price_events_new`, `price_events_used`
- `retired`, `released_date`, `retired_date`, `retail_price_*`, `currency`

For minifig value responses, use fields such as:
- current value fields
- forecast and growth fields when present
- `set_count`, `sets`, `theme`, `subtheme`, `year`, `currency`

For collection analysis:
- Prefer `collection-sets` or `collection-minifigs` over repeated individual lookups.
- Calculate ROI only from returned paid/acquisition value and current value fields.
- Sort best performers by explicit growth percentage or absolute gain from the response; say which metric you used.
- Do not hide low-confidence or missing paid-price rows inside totals; call out missing data.

For sales-ledger analysis:
- Compute profit/loss only from returned sale price, fees, shipping, buy price, quantity, and dates.
- Mention whether totals include fees/shipping based on fields present in the ledger response.
- Keep buyer/order/note details private unless the user specifically needs them.

## Read-only smoke checks

Local, no-network checks:

```bash
python3 -m py_compile scripts/brickeconomy_cli.py
scripts/brickeconomy set --dry-run --set-number 10236-1 --currency EUR
scripts/brickeconomy sales-ledger --dry-run
```

Live smoke checks, only when `BRICKECONOMY_API_KEY` is configured:

```bash
scripts/brickeconomy set --set-number 10236-1 --currency USD
scripts/brickeconomy minifig --minifig-number sw0509 --currency USD
```

Summarize only response shape, for example top-level keys and whether `data` is an object/list. Do not paste full collection or sales-ledger data into reports.

## BrickEconomy limitations and routing

BrickEconomy is appropriate for:
- set and minifig valuation
- forecasts and growth-rate analysis
- authenticated collection valuation and performance
- authenticated sales-ledger profit/loss analysis

BrickEconomy is not appropriate for:
- individual part pricing
- current marketplace offers/listings from sellers
- collection mutation or marketplace inventory writes
- BrickOwl/BrickLink catalog identifier lookup

If the user asks for part prices, seller availability, or buy/sell marketplace actions, route to the relevant BrickLink or BrickOwl skill instead of forcing BrickEconomy.

## Verification

Before committing changes to this skill:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
scripts/validate-skills.sh
git diff --check
```
