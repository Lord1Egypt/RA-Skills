# Frankfurter API v2 — Full Endpoint Reference

Base URL: `https://api.frankfurter.dev`. All examples below were verified
against the live API. No authentication required.

## Contents

1. [GET /v2/rates](#get-v2rates) — latest, historical, and time-series rates
2. [GET /v2/rate/{BASE}/{QUOTE}](#get-v2ratebasequote) — single pair
3. [GET /v2/currencies](#get-v2currencies) — list currencies
4. [GET /v2/currency/{CODE}](#get-v2currencycode) — currency details
5. [GET /v2/providers](#get-v2providers) — data sources
6. [Output formats](#output-formats)
7. [Errors](#errors)

---

## GET /v2/rates

The workhorse endpoint. Returns a JSON array of rate rows.

### Query parameters

| Param | Meaning | Example |
|---|---|---|
| `base` | Base currency (default `EUR`) | `base=USD` |
| `quotes` | Comma-separated target currencies (default: all) | `quotes=USD,GBP` |
| `date` | Rates for one specific date | `date=1999-01-04` |
| `from` / `to` | Time series over a date range (`to` defaults to today) | `from=2026-01-01&to=2026-03-31` |
| `group` | Downsample a series: `week` or `month` | `group=month` |
| `providers` | Restrict to specific provider keys | `providers=ECB` |
| `expand` | `expand=providers` adds per-provider attribution | `expand=providers` |

### Latest rates

```
GET /v2/rates?base=USD&quotes=EUR,TWD
```
```json
[
  {"date": "2026-07-03", "base": "USD", "quote": "EUR", "rate": 0.87598},
  {"date": "2026-07-03", "base": "USD", "quote": "TWD", "rate": 31.913}
]
```

### Historical date

```
GET /v2/rates?date=1999-01-04&quotes=USD
```
```json
[{"date": "1999-01-04", "base": "EUR", "quote": "USD", "rate": 1.1757}]
```

### Time series (with grouping)

```
GET /v2/rates?from=2026-01-01&to=2026-03-31&quotes=USD&group=month
```
```json
[
  {"date": "2026-01-01", "base": "EUR", "quote": "USD", "rate": 1.1737},
  {"date": "2026-02-01", "base": "EUR", "quote": "USD", "rate": 1.1829},
  {"date": "2026-03-01", "base": "EUR", "quote": "USD", "rate": 1.157}
]
```

Without `group`, you get one row per business day per quote currency. For large
ranges, narrow `quotes` and consider NDJSON output (see below).

### Provider attribution

```
GET /v2/rates?quotes=USD&expand=providers
```
```json
[
  {
    "date": "2026-07-03", "base": "EUR", "quote": "USD", "rate": 1.1416,
    "providers": [
      {"key": "ECB", "rate": 1.1399},
      {"key": "BOE", "rate": 1.1395},
      {"key": "FRED", "rate": 1.1403}
    ]
  }
]
```
(The real array lists every contributing central bank — often 50+ for major
pairs.) Rows for pegged currencies omit `providers`; those rates come from the
peg itself.

---

## GET /v2/rate/{BASE}/{QUOTE}

Single currency pair, single object. Optional `date` and `providers` params.

```
GET /v2/rate/USD/JPY?date=2020-03-16
```
```json
{"date": "2020-03-16", "base": "USD", "quote": "JPY", "rate": 106.45}
```

This is the cheapest call for currency conversion: multiply your amount by
`rate`.

---

## GET /v2/currencies

Lists available currencies. Add `scope=all` to include legacy/discontinued
currencies (DEM, FRF, ...).

```
GET /v2/currencies
```
```json
[
  {
    "iso_code": "AED",
    "iso_numeric": "784",
    "name": "United Arab Emirates Dirham",
    "symbol": "د.إ",
    "start_date": "1996-04-11",
    "end_date": "2026-07-03"
  }
]
```

`start_date`/`end_date` tell you the date range for which rates exist — check
`start_date` before requesting old historical data.

---

## GET /v2/currency/{CODE}

One currency's details plus which providers cover it.

```
GET /v2/currency/TWD
```
```json
{
  "iso_code": "TWD",
  "iso_numeric": "901",
  "name": "New Taiwan Dollar",
  "symbol": "$",
  "start_date": "1981-01-02",
  "end_date": "2026-07-03",
  "providers": ["AMCM", "BOC", "BOE", "CBC", "ECB", "FRED", "MAS", "..."]
}
```

---

## GET /v2/providers

Lists the central banks / data sources behind the API. Useful for finding the
`providers=` key for compliance-grade official rates.

```
GET /v2/providers
```
```json
[
  {
    "key": "AMCM",
    "name": "Autoridade Monetária de Macau",
    "country_code": "MO",
    "rate_type": "interbank middle rate",
    "pivot_currency": "MOP",
    "data_url": "https://www.amcm.gov.mo/en/financial-information/interbank-midpoint",
    "terms_url": null,
    "start_date": "1986-01-02",
    "end_date": "2026-07-03",
    "publish_cadence": "daily",
    "currencies": ["AUD", "CAD", "CHF", "CNY", "EUR", "GBP", "JPY", "USD", "..."]
  }
]
```

Common provider keys: `ECB` (European Central Bank), `BOE` (Bank of England),
`FRED` (US Federal Reserve data), `BOJ` (Bank of Japan), `CBC` (Central Bank of
the Republic of China, Taiwan), `MAS` (Monetary Authority of Singapore).

---

## Output formats

| Format | How to request | Notes |
|---|---|---|
| JSON | default | |
| CSV | append `.csv` to path, or `Accept: text/csv` | header row: `date,base,quote,rate` |
| NDJSON | `Accept: application/x-ndjson` | one JSON object per line; stream large series |

```
GET /v2/rates.csv?quotes=USD,GBP
```
```csv
date,base,quote,rate
2026-07-03,EUR,GBP,0.85788
2026-07-03,EUR,USD,1.1416
```

---

## Errors

Standard HTTP status codes with a JSON body:

```json
{"status": 404, "message": "not found"}
```

| Status | Meaning | Typical cause |
|---|---|---|
| 400 | Invalid parameter or malformed request | bad date format, unknown query param value |
| 404 | Resource not found | wrong ISO code, no data for that date/currency |
| 422 | Understood but not processable | logically invalid combination |

## Other facts worth knowing

- No GraphQL — use query params (`base`, `quotes`, `from`/`to`) to shape data.
- No call quotas; rate limiting exists only to prevent abuse. For high volume:
  cache, self-host (Docker), or use the published datasets directly.
- The API itself collects no personal data (public instance sits behind
  Cloudflare).
- An official MCP server for AI assistants and integrations for Excel, Google
  Sheets, and pandas exist — see https://frankfurter.dev/ under "Integrations".
- The name: the European Central Bank is in Frankfurt.
