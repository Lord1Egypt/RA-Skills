# FMP Endpoints & MCP Tools Reference

Base URL: `https://financialmodelingprep.com/stable/`
Auth: append `apikey=YOUR_FMP_API_KEY` to every request (never the real value in output).
Method: **GET only.** Responses are JSON, usually a JSON array of objects.

The `financialmodelingprep-mcp` server is **complete and live-tested**. It exposes **12 tools**:
eleven dedicated tools for common workflows plus one generic passthrough (`fmp_request`) that reaches
**all 263 `/stable` endpoints**. Prefer the dedicated MCP tools; fall back to direct GET or
`fmp_request` for the long tail.

> Verification needed: paths, params, and response shapes evolve. Confirm against
> https://site.financialmodelingprep.com/developer/docs.

---

## The 12 MCP tools

| # | MCP tool | Purpose | HTTP endpoint (`/stable/...`) |
|---|----------|---------|-------------------------------|
| 1 | `fmp_search` | Resolve a symbol by ticker or company name (auto symbol→name fallback) | `/search-symbol?query=`, then `/search-name?query=` |
| 2 | `fmp_quote` | Current (delayed) quote | `/quote?symbol=` |
| 3 | `fmp_company_profile` | Company overview / identity | `/profile?symbol=` |
| 4 | `fmp_income_statement` | Income statement | `/income-statement?symbol=&period=&limit=` |
| 5 | `fmp_balance_sheet` | Balance sheet | `/balance-sheet-statement?symbol=&period=&limit=` |
| 6 | `fmp_cash_flow` | Cash-flow statement | `/cash-flow-statement?symbol=&period=&limit=` |
| 7 | `fmp_ratios` | Pre-computed ratios | `/ratios?symbol=&period=&limit=` |
| 8 | `fmp_key_metrics` | Per-share & valuation metrics | `/key-metrics?symbol=&period=&limit=` |
| 9 | `fmp_dcf` | DCF model estimate (not advice) | `/discounted-cash-flow?symbol=` |
| 10 | `fmp_historical_prices` | EOD OHLCV history | `/historical-price-eod/full?symbol=&from=&to=` |
| 11 | `fmp_screener` | Company screener by fundamentals | `/company-screener?...` |
| 12 | `fmp_request` | **Generic passthrough to all 263 endpoints** | any `/stable/<endpoint>` |

Common params: `period` ∈ `annual | quarter`; `limit` = number of periods/rows; `from`/`to` =
`YYYY-MM-DD`. Inputs are validated server-side; the key is injected and redacted; typed errors are
`auth`, `validation`, `rate_limit`, `plan_restricted` (HTTP 402 — do not retry), `timeout`, `server`.

---

## Symbol search — `fmp_search`

- **Purpose:** resolve a ticker by partial symbol or company name. The tool tries `/search-symbol`
  and **automatically falls back** to `/search-name`, so one call handles either.
- **Params:** `query` (required), optional `limit`.
- **Response shape:** array of `{ symbol, name, currency, exchange, exchangeFullName }`.
- **Cost note:** cheap; use **first** before pulling any data.

---

## Quote — `fmp_quote`

- **Endpoint:** `/quote?symbol=`
- **Params:** `symbol` (required).
- **Response shape:** `{ symbol, name, price, change, changePercentage, volume, dayLow, dayHigh,
  yearHigh, yearLow, marketCap, priceAvg50, priceAvg200, exchange, open, previousClose, timestamp }`.
- **Cost note:** one call. Cite the `timestamp` (delayed quote).

---

## Company profile — `fmp_company_profile`

- **Endpoint:** `/profile?symbol=`
- **Params:** `symbol` (required).
- **Response shape:** array (usually one) `{ symbol, companyName, currency, exchange, sector,
  industry, country, description, ceo, fullTimeEmployees, marketCap, price, website, ipoDate,
  isActivelyTrading, ... }`.
- **Cost note:** one call; use to confirm the resolved symbol matches user intent (exchange,
  currency).

---

## Financial statements

### Income statement — `fmp_income_statement`
- **Endpoint:** `/income-statement?symbol=&period=&limit=`
- **Params:** `symbol`, `period=annual|quarter`, `limit`.
- **Response shape:** per period `{ symbol, date, period, fiscalYear, reportedCurrency, revenue,
  costOfRevenue, grossProfit, operatingIncome, netIncome, eps, epsDiluted, ... }`.

### Balance sheet — `fmp_balance_sheet`
- **Endpoint:** `/balance-sheet-statement?symbol=&period=&limit=`
- **Params:** same as income statement.
- **Response shape:** per period `{ symbol, date, period, fiscalYear, reportedCurrency, totalAssets,
  totalCurrentAssets, cashAndCashEquivalents, totalLiabilities, totalCurrentLiabilities, totalDebt,
  totalEquity, retainedEarnings, ... }`.

### Cash flow — `fmp_cash_flow`
- **Endpoint:** `/cash-flow-statement?symbol=&period=&limit=`
- **Params:** same as income statement.
- **Response shape:** per period `{ symbol, date, period, fiscalYear, reportedCurrency, netIncome,
  operatingCashFlow, capitalExpenditure, freeCashFlow, dividendsPaid, commonStockRepurchased,
  netChangeInCash, ... }`.

> Choose `period` deliberately: `annual` for year-over-year trends and "last N years"; `quarter` for
> recent momentum, seasonality, or building TTM from four quarters. Never label an annual figure
> "TTM". Cost note: one call each; larger `limit` may exceed plan history.

---

## Ratios & metrics

### Ratios — `fmp_ratios`
- **Endpoint:** `/ratios?symbol=&period=&limit=`
- **Response shape:** per period `{ symbol, date, period, currentRatio, quickRatio,
  grossProfitMargin, operatingProfitMargin, netProfitMargin, returnOnEquity, returnOnAssets,
  debtToEquityRatio, priceToEarningsRatio, ... }`.
- **Cost note:** prefer these over hand-computing ratios.

### Key metrics — `fmp_key_metrics`
- **Endpoint:** `/key-metrics?symbol=&period=&limit=`
- **Response shape:** per period `{ symbol, date, period, marketCap, enterpriseValue, peRatio,
  priceToSalesRatio, returnOnEquity, returnOnInvestedCapital, currentRatio, debtToEquity,
  freeCashFlowPerShare, revenuePerShare, ... }`.

> Verification needed: whether a TTM variant (e.g. `key-metrics-ttm`, `ratios-ttm`) exists; if so,
> reach it via `fmp_request`.

---

## Valuation — `fmp_dcf`

- **Endpoint:** `/discounted-cash-flow?symbol=`
- **Params:** `symbol` (required).
- **Response shape:** array (usually one) `{ symbol, date, dcf, "Stock Price" }`.
- **Cost note:** one call. **Model estimate only** — always caveat; never a recommendation.

---

## Price history — `fmp_historical_prices`

- **Endpoint:** `/historical-price-eod/full?symbol=&from=&to=`
- **Params:** `symbol` (required), `from=YYYY-MM-DD`, `to=YYYY-MM-DD`.
- **Response shape:** array of `{ symbol, date, open, high, low, close, adjClose, volume }` (the tool
  normalizes a possible `{ symbol, historical[] }` wrapper to a flat array).
- **Cost note:** wide ranges return large payloads / may time out — narrow `from`/`to`.

---

## Company screener — `fmp_screener`

- **Endpoint:** `/company-screener?...`
- **Params (all optional):** `marketCapMoreThan`, `marketCapLowerThan`, `priceMoreThan`,
  `priceLowerThan`, `betaMoreThan`, `betaLowerThan`, `volumeMoreThan`, `volumeLowerThan`,
  `dividendMoreThan`, `dividendLowerThan`, `sector`, `industry`, `exchange`, `country`, `isEtf`,
  `isFund`, `isActivelyTrading`, `includeAllShareClasses`, `limit`.
- **Response shape:** array of `{ symbol, companyName, marketCap, sector, industry, beta, price,
  volume, exchange, country, isEtf, isFund, isActivelyTrading }`.
- **Cost note / plan:** often **plan-restricted**. On lower tiers it returns `plan_restricted`
  (HTTP 402) — **do not retry**; tell the user a higher plan is required.

---

## Generic passthrough — `fmp_request` (all 263 endpoints)

Use `fmp_request` for any endpoint without a dedicated tool. Supply `endpoint` (the path after
`/stable/`, validated to a safe path shape) and an optional `params` object.

```json
{ "endpoint": "treasury-rates", "params": { "from": "2025-01-01", "to": "2025-03-31" } }
{ "endpoint": "dividends",      "params": { "symbol": "AAPL" } }
{ "endpoint": "senate-trading", "params": { "symbol": "AAPL" } }
{ "endpoint": "news/stock-latest", "params": { "limit": 20 } }
```

- **Generic endpoint pattern:** `GET /stable/<endpoint>?<params>&apikey=YOUR_FMP_API_KEY` where
  `<endpoint>` matches a safe path shape (lowercase letters, digits, hyphens, `/`).
- **Prefer a dedicated tool** when one exists (quote, profile, statements, ratios, key metrics, DCF,
  history, screener, search) — dedicated tools add validation, normalization, and clearer errors.
- Same retry/timeout/redaction/typed-error behavior as the dedicated tools applies. A `402` from a
  plan-restricted endpoint is **not** retried.

### Full 263-endpoint catalog

The complete list of `/stable` endpoints — with parameters and response shapes — lives in the API
docs, organized by domain:

- [`api-docs/09-all-endpoints/01-search-and-directory.md`](../../api-docs/09-all-endpoints/01-search-and-directory.md)
- [`api-docs/09-all-endpoints/02-company-and-profile.md`](../../api-docs/09-all-endpoints/02-company-and-profile.md)
- [`api-docs/09-all-endpoints/03-quotes.md`](../../api-docs/09-all-endpoints/03-quotes.md)
- [`api-docs/09-all-endpoints/04-prices-and-history.md`](../../api-docs/09-all-endpoints/04-prices-and-history.md)
- [`api-docs/09-all-endpoints/06-metrics-valuation-analyst.md`](../../api-docs/09-all-endpoints/06-metrics-valuation-analyst.md)
- [`api-docs/09-all-endpoints/09-ownership-sec-government.md`](../../api-docs/09-all-endpoints/09-ownership-sec-government.md)
- [`api-docs/09-all-endpoints/10-etfs-and-funds.md`](../../api-docs/09-all-endpoints/10-etfs-and-funds.md)
- [`api-docs/09-all-endpoints/12-screeners-and-movers.md`](../../api-docs/09-all-endpoints/12-screeners-and-movers.md)

Consult the catalog to pick the right `endpoint`/`params` for `fmp_request` rather than guessing.
