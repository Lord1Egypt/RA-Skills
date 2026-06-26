---
name: finnhub-skill
description: Read-only market data skill for Finnhub. Use when the user wants stock, forex, crypto, company profile, candles/K-lines, news, earnings, or economic calendar data from Finnhub; also use when the user mentions Finnhub API, Finnhub token, or wants to package Finnhub market data access into an OpenClaw workflow.
---

# Finnhub Skill

Use Finnhub as a **read-only market data source**.

## Core Rules

1. Treat this skill as **data retrieval only**.
2. Never place trades or modify accounts through this skill.
3. Require a valid `FINNHUB_API_KEY` before making live requests.
4. If the API key is missing, explain how to configure it instead of guessing.
5. Prefer concise outputs: summary first, raw fields second.

## Supported Use Cases

- Real-time quote lookup
- K-line / candle retrieval
- Company profile lookup
- Symbol/company news lookup
- Earnings calendar / earnings history lookup
- Economic calendar lookup
- Crypto and forex reference data (if supported by the user plan)
- Structured daily stock news report (price + news + trader-style interpretation)

## Configuration

Expect the user to provide:

```bash
export FINNHUB_API_KEY=your_api_key
```

Optional base URL override is supported only for the official Finnhub domain:

```bash
export FINNHUB_BASE_URL=https://finnhub.io/api/v1
```

Default base URL:

```text
https://finnhub.io/api/v1
```

Security rule:
- Only allow `https://finnhub.io/...`
- Do not point this skill to arbitrary hosts or proxies that could capture the API key

## Execution Layer

Use the bundled script:

```bash
python3 scripts/finnhub.py <command> [flags]
```

Supported commands:
- `quote --symbol AAPL [--raw]`
- `candles --symbol AAPL --resolution D --from-ts 1711584000 --to-ts 1712188800 [--raw]`
- `profile --symbol AAPL [--raw]`
- `company-news --symbol AAPL --date-from 2026-03-01 --date-to 2026-03-30 [--raw]`
- `market-news --category general [--raw]`
- `earnings --date-from 2026-03-30 --date-to 2026-04-06 [--symbol AAPL] [--raw]`
- `economic --date-from 2026-03-30 --date-to 2026-04-06 [--raw]`

Default output is human-readable. Use `--raw` when the user explicitly wants JSON.

## Recommended Request Pattern

Use the bundled Python script for live calls instead of rebuilding requests from scratch.

When constructing requests:
- URL-encode symbol and other parameters
- Validate time range inputs before sending
- Keep requests read-only
- If the user asks for a very broad request, narrow the scope first

## Output Style

### Quote
Return:
- symbol
- current price
- absolute change
- percent change
- high / low / open / previous close
- timestamp if available

### Candles
Summarize:
- symbol
- resolution
- start/end window
- number of candles returned
- latest OHLCV row

Only dump the full array when the user explicitly asks.

### Company Profile
Return:
- company name
- ticker
- exchange
- currency
- country
- market cap
- industry / IPO date if available
- website

### News
Return:
- headline
- source
- published time
- URL
- short summary if available

Prefer 3-5 most relevant items unless the user asks for more.

## Common Tasks

### 1. Real-time quote
Use Finnhub quote endpoint for stocks or supported symbols.
If the user gives a bare ticker like `AAPL`, use it directly.
If the user gives crypto/forex, confirm Finnhub symbol format if needed.

### 2. Candles / K-lines
Ask for or infer:
- symbol
- resolution (`1`, `5`, `15`, `30`, `60`, `D`, `W`, `M`)
- from timestamp
- to timestamp

If the user asks loosely (e.g. “last week”), convert it into a concrete range.

### 3. Company profile
Use the company profile endpoint when the user asks “what is this company”, “profile”, “market cap”, “which exchange”, etc.

### 4. News
Use company or market news endpoints depending on the request:
- company-specific → company news
- broad market / macro → market news

### 5. Earnings / calendar
Use earnings calendar for upcoming results and earnings history if the user asks what already happened.

### 6. Daily stock report
When the user asks for a daily report like:
- “发我 TSLA 昨天的新闻总结”
- “做一个 NVDA 昨日新闻日报”
- “给我 AAPL 的价格+新闻日报”

Build the report in this order:
1. quote / price summary first
2. most important 3-5 news items
3. market narrative and trader interpretation
4. final rating

For the report format, read:
- `references/daily-report-template.md`

If candle/volume endpoints are unavailable due to Finnhub plan limits:
- still produce the report
- explicitly say that detailed candles/volume are unavailable under current access
- avoid inventing volume comparison or trend detail

## Error Handling

If Finnhub returns auth or quota errors:
- State the likely cause clearly
- Do not fabricate fallback data
- Suggest checking API key, plan limits, or symbol format

If symbol format is ambiguous:
- Ask one clarifying question
- Do not assume unsupported exchange suffixes

## Reference File

For endpoint patterns and parameter hints, read:
- `references/api.md`
