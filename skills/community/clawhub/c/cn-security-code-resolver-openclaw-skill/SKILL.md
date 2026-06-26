---
name: cn-security-code-resolver
description: Resolve A-share stocks, ETFs, funds, and other mainland China securities from Chinese names into tradable codes using Eastmoney search. This skill should be used when a user asks for a security code, ticker, exchange suffix, or wants a portfolio file enriched with Chinese market instrument codes.
---

# CN Security Code Resolver

## Overview

Resolve Chinese security names into exchange-tradable codes with a deterministic first pass and a verifiable fallback. Use the bundled script to query Eastmoney's public suggest API, then return the best match with enough metadata for confirmation.

## When to use

Use this skill when the task involves any of the following:
- Find the code for a Chinese stock, ETF, LOF, REIT, or fund from its Chinese name
- Convert a portfolio/watchlist from names into tradable codes
- Confirm whether an instrument is A-share, ETF/fund, or another mainland market type
- Add exchange-aware identifiers such as `600938.SH`, `510880.SH`, or Eastmoney `QuoteID`

Do not use this skill for:
- Real-time pricing or chart analysis
- Hong Kong, US, futures, or crypto symbols unless the user explicitly wants cross-market results
- Fundamental analysis beyond basic instrument identification

## Workflow

### 1) Prefer the script first

Run the bundled resolver script:

```bash
python3 skills/cn-security-code-resolver/scripts/resolve_cn_security.py "中国海油"
```

Batch mode:

```bash
python3 skills/cn-security-code-resolver/scripts/resolve_cn_security.py "红利ETF华泰柏瑞" "苏美达" "中国海油" "海油发展" "中海油服"
```

### 2) Read the best match carefully

Prefer rows where:
- `Name` exactly matches the queried Chinese name
- `SecurityTypeName` matches user intent (`沪A`, `深A`, `基金`, etc.)
- `MarketType` / `QuoteID` indicate mainland trading venue

For mainland cash equities and ETFs, map exchange suffixes as:
- codes starting with `6`, `5`, or `9` → usually `SH`
- codes starting with `0`, `1`, `2`, or `3` → usually `SZ`

If the returned result is ambiguous, show the top 3 candidates and ask for confirmation instead of guessing.

### 3) Return a concise confirmation

Use this output shape when replying:

```text
标的：中海油服
A股代码：601808
交易所：上交所
类型：沪A
标准代码：601808.SH
QuoteID：1.601808
```

### 4) When updating files

When writing portfolio JSON or other structured files, prefer storing both:
- `code`: raw numeric code, e.g. `601808`
- `exchangeSuffix`: `SH` or `SZ` when it can be derived confidently

Optional enriched fields:
- `quoteId`
- `securityTypeName`
- `marketType`
- `source: "eastmoney_suggest"`

## Verification guidance

If the first result looks suspicious:
- Re-run with the exact full Chinese name from the broker/app
- Inspect the top candidate list from the script
- Cross-check with a browser search only when necessary

Good verification signals:
- Exact Chinese name match
- Expected category (for example ETF vs stock)
- Price range and portfolio context are consistent with the instrument type

## Bundled resources

### Script
- `scripts/resolve_cn_security.py`
  - Queries Eastmoney suggest API
  - Supports one or many names
  - Returns ranked JSON results with exchange hints

### Reference
- `references/eastmoney-api.md`
  - Documents the API endpoint, returned fields, and matching heuristics

## Examples

```bash
python3 skills/cn-security-code-resolver/scripts/resolve_cn_security.py "苏美达"
```

Expected top result:
- `600710` / `苏美达` / `沪A`

```bash
python3 skills/cn-security-code-resolver/scripts/resolve_cn_security.py "红利ETF华泰柏瑞"
```

Expected top result:
- `510880` / `红利ETF华泰柏瑞` / `基金`

```bash
python3 skills/cn-security-code-resolver/scripts/resolve_cn_security.py "中海油服"
```

Expected top result:
- `601808` / `中海油服` / `沪A`
- If other markets also appear elsewhere, prefer A-share unless the user asks otherwise
