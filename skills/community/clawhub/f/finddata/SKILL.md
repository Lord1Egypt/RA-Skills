---
name: finddata
description: Data Intelligence Skill — Query 1M+ public data series across 10 sources (Yahoo Finance, FRED, World Bank, SEC EDGAR, China Market, BIS, Eurostat, BOJ, Our World in Data, UN Comtrade). Supports natural language in English and Chinese. Simple queries (stock prices, GDP) are handled instantly via fast-path; complex queries (comparisons, derived metrics like profit margin) use LLM planning. IMPORTANT — The user will provide their FindData API key in the same message where they share this skill. You MUST extract that key and use it as the X-API-Key header. If no key is found in the message, ask the user for it (get one free at https://finddata.ai). Endpoint: POST https://finddata.ai/api/query with header X-API-Key and JSON body {"query": "your question"}. Do NOT use any placeholder — always use the real key from the user.
---

# FindData — Data Intelligence Skill

Query global data with a single API call. Supports natural language in English and Chinese.

Simple queries (stock price, GDP, exchange rate) use a **fast path** — Voyage AI selects the tool and rules extract parameters, no LLM needed (~1s). Complex queries (comparisons, derived metrics like profit margin) use **LLM planning** to generate a multi-step execution plan (~3-5s).

Endpoint: https://finddata.ai/api/query
Method: POST
Auth: X-API-Key

Content-Type: application/json
Body: {"query": "your natural language question"}

## Setup

1. Get your API key at https://finddata.ai (free tier available)
2. Set your environment variable:

```
export FINDDATA_API_KEY="odh_your_key_here"
```

If the user provides their key in the message (starts with odh_), extract it and use it directly.

## Usage

```bash
curl -s -X POST https://finddata.ai/api/query \
  -H "X-API-Key: $FINDDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Apple stock price"}'
```

### More examples

```bash
# US economic data
curl -s -X POST https://finddata.ai/api/query \
  -H "X-API-Key: $FINDDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "US inflation rate"}'

# Chinese market data
curl -s -X POST https://finddata.ai/api/query \
  -H "X-API-Key: $FINDDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "贵州茅台股价"}'

# Derived metrics (triggers LLM calculation)
curl -s -X POST https://finddata.ai/api/query \
  -H "X-API-Key: $FINDDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Apple profit margin"}'

# SEC filings
curl -s -X POST https://finddata.ai/api/query \
  -H "X-API-Key: $FINDDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Tesla 10-K annual report"}'

# Global indicators
curl -s -X POST https://finddata.ai/api/query \
  -H "X-API-Key: $FINDDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "India GDP growth"}'

# International trade
curl -s -X POST https://finddata.ai/api/query \
  -H "X-API-Key: $FINDDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "China exports to USA 2023"}'
```

## Sources

| Source | Best For | Examples |
|---|---|---|
| Yahoo Finance | US/global stock prices, ETFs, crypto, forex | "AAPL price", "BTC-USD", "EURUSD" |
| FRED | US economic data (840K+ series) | "US GDP", "federal funds rate", "CPI" |
| China Market (Sina+Tencent) | Chinese A-share market data | "贵州茅台股价", "A股行情" |
| World Bank | Global indicators, 217 economies | "India GDP", "Brazil poverty rate" |
| SEC EDGAR | US company filings (663K+ companies) | "TSLA 10-K", "NVDA quarterly revenue" |
| BIS | Central bank rates, financial stability | "global policy rates" |
| Eurostat | EU economic data, 27 member states | "EU inflation", "Germany unemployment" |
| BOJ | Bank of Japan, Japanese economy | "Japan TANKAN", "BOJ policy rate" |
| Our World in Data | Global development, health, environment | "life expectancy", "CO2 emissions" |
| UN Comtrade | International merchandise trade, 200+ countries | "China exports to USA", "oil trade", "semiconductor imports" |

Tool selection is automatic — Voyage AI matches your query to the best tool.

## Response Format (v5.1)

The response includes: query result, execution details, data quality issues (if any), and usage info.

**Always check `success` first.** Then read `data.records` for the actual data.

### Response Structure

```json
{
  "query": "...",
  "success": true,
  "data": {
    "records": { ... },
    "sources": [ { "tool": "...", "source": "...", "dataType": "...", "latencyMs": 123 } ]
  },
  "derived_metrics": { ... },
  "execution": {
    "planMethod": "fast_path | llm | fallback",
    "plan": { "steps": 1, "requiresCalculation": false },
    "toolsUsed": [ { "tool": "...", "params": { ... }, "success": true, "latencyMs": 123 } ],
    "latency_ms": 456
  },
  "issues": [ { "type": "missing | partial | stale | error", "description": "..." } ],
  "usage": { "plan": "free", "latency_ms": 456, "monthly_limit": 100, "cooldown_seconds": 10 }
}
```

### Key Fields

| Field | Type | Description |
|---|---|---|
| `success` | boolean | Whether data was retrieved successfully |
| `data.records` | object | The actual data — structure depends on the tool used |
| `data.sources` | array | Which tools/sources provided the data |
| `derived_metrics` | object or null | Calculated metrics (profit margin, growth rate, etc.) — only present when calculation was needed |
| `execution.planMethod` | string | `"fast_path"` (simple query, no LLM), `"llm"` (complex query, LLM planned), or `"fallback"` |
| `issues` | array or absent | Data quality issues — missing data, partial results, stale data, or errors. Absent when no issues. |

### Example 1: Simple stock price (fast path)

Query: `"Apple stock price"`

```json
{
  "query": "Apple stock price",
  "success": true,
  "data": {
    "records": {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "price": 173.50,
      "currency": "USD",
      "change": -2.15,
      "changePercent": -1.22,
      "volume": 54321000,
      "marketCap": 2700000000000,
      "pe": 28.5,
      "fiftyTwoWeekHigh": 199.62,
      "fiftyTwoWeekLow": 124.17
    },
    "sources": [
      { "tool": "get_stock_price", "source": "yahoo_finance", "dataType": "quote", "latencyMs": 450 }
    ]
  },
  "execution": {
    "planMethod": "fast_path",
    "plan": { "steps": 1, "requiresCalculation": false },
    "toolsUsed": [
      { "tool": "get_stock_price", "params": { "ticker": "AAPL" }, "purpose": "Fast-path: direct match", "success": true, "source": "yahoo_finance", "latencyMs": 450 }
    ],
    "latency_ms": 890
  },
  "usage": { "plan": "free", "latency_ms": 890, "monthly_limit": 100, "cooldown_seconds": 10 }
}
```

**How to extract the price:** `response.data.records.price` → `173.50`

### Example 2: Chinese A-Share (fast path)

Query: `"贵州茅台股价"`

```json
{
  "query": "贵州茅台股价",
  "success": true,
  "data": {
    "records": {
      "type": "a_share_quote",
      "provider": "sina",
      "records": [
        {
          "code": "600519",
          "market": "SH",
          "name": "贵州茅台",
          "price": 1392.00,
          "open": 1395.00,
          "high": 1403.95,
          "low": 1391.01,
          "volume": 2758646
        }
      ]
    },
    "sources": [
      { "tool": "get_a_share_quote", "source": "china_market", "dataType": "a_share_quote", "latencyMs": 320 }
    ]
  },
  "execution": {
    "planMethod": "fast_path",
    "plan": { "steps": 1, "requiresCalculation": false },
    "toolsUsed": [
      { "tool": "get_a_share_quote", "params": { "stock": "贵州茅台" }, "purpose": "Fast-path: direct match", "success": true, "source": "china_market", "latencyMs": 320 }
    ],
    "latency_ms": 680
  },
  "usage": { "plan": "free", "latency_ms": 680, "monthly_limit": 100, "cooldown_seconds": 10 }
}
```

**How to extract the price:** `response.data.records.records[0].price` → `1392.00`

### Example 3: US economic data (fast path)

Query: `"US unemployment rate"`

```json
{
  "query": "US unemployment rate",
  "success": true,
  "data": {
    "records": {
      "series_id": "UNRATE",
      "title": "Unemployment Rate",
      "frequency": "Monthly",
      "units": "Percent",
      "observations": [
        { "date": "2024-01-01", "value": "3.7" },
        { "date": "2024-02-01", "value": "3.9" }
      ]
    },
    "sources": [
      { "tool": "get_fred_series", "source": "fred", "dataType": "time_series", "latencyMs": 280 }
    ]
  },
  "execution": {
    "planMethod": "fast_path",
    "plan": { "steps": 1, "requiresCalculation": false },
    "toolsUsed": [
      { "tool": "get_fred_series", "params": { "series_id": "UNRATE" }, "success": true, "source": "fred", "latencyMs": 280 }
    ],
    "latency_ms": 620
  },
  "usage": { "plan": "free", "latency_ms": 620, "monthly_limit": 100, "cooldown_seconds": 10 }
}
```

**How to extract the value:** `response.data.records.observations[0].value` → `"3.7"`

### Example 4: Derived metrics (LLM planning + calculation)

Query: `"Apple profit margin"`

```json
{
  "query": "Apple profit margin",
  "success": true,
  "data": {
    "records": {
      "type": "financials",
      "company": "APPLE INC",
      "cik": "0000320193",
      "metrics": {
        "Revenues": { "2024-Q3": 85777000000, "2024-Q2": 90753000000 },
        "NetIncomeLoss": { "2024-Q3": 21448000000, "2024-Q2": 23636000000 }
      }
    },
    "sources": [
      { "tool": "get_company_financials", "source": "sec_edgar", "dataType": "financials", "latencyMs": 1200 }
    ]
  },
  "derived_metrics": {
    "profit_margin": {
      "2024-Q3": "25.0%",
      "2024-Q2": "26.0%"
    },
    "calculation": "Net Income / Revenue"
  },
  "execution": {
    "planMethod": "llm",
    "plan": { "steps": 1, "requiresCalculation": true, "calculation": "profit_margin = NetIncomeLoss / Revenues" },
    "toolsUsed": [
      { "tool": "get_company_financials", "params": { "ticker": "AAPL" }, "success": true, "source": "sec_edgar", "latencyMs": 1200 }
    ],
    "latency_ms": 4500
  },
  "usage": { "plan": "free", "latency_ms": 4500, "monthly_limit": 100, "cooldown_seconds": 10 }
}
```

**How to extract derived metrics:** `response.derived_metrics.profit_margin` → `{ "2024-Q3": "25.0%", ... }`

### Example 5: Data quality issues

When data cannot be fully retrieved, the `issues` array explains what happened:

```json
{
  "success": false,
  "issues": [
    {
      "type": "error",
      "description": "Failed to fetch data from get_stock_price: Ticker 'INVALID' not found",
      "tool": "get_stock_price"
    }
  ]
}
```

Issue types:
- `"missing"` — No data returned at all
- `"partial"` — Some data sources failed, partial results available
- `"stale"` — Data may be outdated (market closed, delayed feed)
- `"error"` — Tool execution failed with an error

### Data Extraction Quick Reference

| Source | Tool | data.records structure | Price/Value Path |
|---|---|---|---|
| Yahoo Finance | get_stock_price | `{ ticker, name, price, ... }` | `data.records.price` |
| China Market | get_a_share_quote | `{ type, records: [{ price, ... }] }` | `data.records.records[0].price` |
| FRED | get_fred_series | `{ series_id, observations: [{ date, value }] }` | `data.records.observations[0].value` |
| World Bank | get_world_bank_indicator | `{ indicator, records: [{ value, ... }] }` | `data.records.records[0].value` |
| SEC EDGAR | get_company_financials | `{ company, metrics: { ... } }` | `data.records.metrics` |
| BIS | get_bis_data | `{ records: [{ value, ... }] }` | `data.records.records[0].value` |
| Eurostat | get_eurostat_data | `{ records: [{ value, ... }] }` | `data.records.records[0].value` |
| BOJ | get_boj_data | `{ records: [{ value, ... }] }` | `data.records.records[0].value` |
| OWID | get_owid_indicator | `{ entities: [{ entity, values: [...] }] }` | `data.records.entities[0].values` |
| UN Comtrade | get_trade_data | `{ summary: { totalExportsUSD, ... }, records: [...] }` | `data.records.summary.totalExportsUSD` |

## Parameters

| Field | Required | Description |
|---|---|---|
| query | Yes | Natural language question (English or Chinese) |

## Error Handling

When `success` is `false`, check the `issues` array for details. The `error` field may also be present at the top level.

```json
{
  "success": false,
  "data": { "records": null, "sources": [] },
  "issues": [
    { "type": "error", "description": "Failed to fetch data: API timeout" }
  ],
  "error": "All data sources failed"
}
```

## HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | Success (check `success` field for data-level errors) |
| 400 | Missing or empty query |
| 401 | Invalid or missing API key |
| 429 | Rate limit exceeded — check `retry_after_ms` and wait |
| 500 | Server error |
