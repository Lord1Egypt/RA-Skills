# tradingviewapi Structured Data Reference

This document lists every `tradingviewapi` (TradingView proxy service) endpoint and maps its response fields to equity research report sections. Shared by all skills in the `equity-research` plugin. **Prefer the structured API for numeric data**; use Web Search only for narrative content (MD&A, forward guidance, earnings call transcripts, segment breakdowns, risk factors).

## Quick Navigation

1. [Authentication](#authentication)
2. [Symbol Format](#symbol-format)
3. [Scenario A: Quarterly Earnings Analysis](#scenario-a-quarterly-earnings-analysis-earnings-analysis-earnings-preview)
4. [Scenario B: Initiation Report](#scenario-b-initiation-report-initiating-coverage)
5. [Scenario C: Catalyst Calendar](#scenario-c-catalyst-calendar-catalyst-calendar)
6. [Scenario D: Morning Note](#scenario-d-morning-note-morning-note)
7. [Scenario E: Screening / Idea Generation](#scenario-e-screening--idea-generation-idea-generation)
8. [Scenario F: Sector Overview](#scenario-f-sector-overview-sector-overview)
9. [Scenario G: Model Update](#scenario-g-model-update-model-update)
10. [Scenario H: Thesis Tracker](#scenario-h-thesis-tracker-thesis-tracker)
11. [Ticker Resolution](#ticker-resolution-generic-preflight)
12. [Full Endpoint Catalog](#full-endpoint-catalog-60-endpoints)
13. [Citation Convention](#citation-convention-aligned-with-earnings-analysisskillmd-lines-50-107)
14. [Fallback Strategy](#fallback-strategy)

## Lookup Tips

`references/tradingviewapi.md` is the workflow-facing index and field-mapping guide.
For exact endpoint behavior, downloaded API docs, and real executed example payloads, always refer to `references/tradingviewapi-docs/` first.
In case of any mismatch, treat `references/tradingviewapi-docs/` as the source of truth and update this file to match it.

### Reference priority

Use the bundled references in this order:

1. `tradingviewapi-docs/openapi.json` — source of truth for parameter names, required fields, defaults, and enum constraints
2. `tradingviewapi-docs/examples/` — request / response examples and payload-shape hints
3. `tradingviewapi.md` — workflow routing and report-field mapping

If sources disagree:

- Trust `openapi.json` for how to build the request.
- Use `examples/` to understand the returned payload shape after the request has been validated against the spec.
- Treat `examples/` as potentially illustrative rather than universally valid for every asset class or symbol family.

### Parameter discipline

- Match the endpoint family to the symbol family. Example: `/api/news/crypto` should use crypto symbols such as `BINANCE:BTCUSDT`, not stock tickers.
- For `/api/search/market/{query}`, set `filter` to the actual asset class you want (`stock`, `crypto`, `forex`, `futures`, `index`, `funds`, `bond`, `options`, or `undefined`) instead of relying on a reused stock example.
- For `/api/quote/{symbol}`, prefer `?session=regular&fields=all` unless the workflow explicitly needs a different session or a reduced field set.
- When an example appears to conflict with endpoint semantics, verify the allowed parameters in `openapi.json` before using the example verbatim.

### Common pitfalls

- `GET /api/news/crypto`
  Use crypto symbols such as `BINANCE:BTCUSDT` when passing `symbol`. Do not reuse stock placeholders from unrelated examples.
- `GET /api/search/market/{query}`
  The `filter` value materially changes results. Use `filter=stock` for equities, `filter=crypto` for crypto, `filter=forex` for FX, and so on.
- `GET /api/quote/{symbol}`
  Prefer `?session=regular&fields=all` for analysis workflows. The returned quote fields are nested under `data.data`, not flat at the top level.
- `GET /api/market-data/{symbol}/analyst-recommendations`
  The payload is a single object at `data.analyst_recommendations`, not an array. Do not parse it as `data[0]`.
- `GET /api/market-data/{symbol}`
  Treat the request symbol or preflight search result as canonical. Do not rely on `data.company.ticker` or `data.company.exchange` to reconstruct the primary listing.

- Read this file before opening `tradingviewapi-docs/openapi.json` or any file in `tradingviewapi-docs/examples/`.
- Search `tradingviewapi-docs/examples/` by endpoint path or JSON field name, not by workflow name.
- Treat `tradingviewapi-docs/examples/` as the real executed sample set, not just illustrative pseudodata.
- Most common files:
  - `examples/10-market-data.md` for company, TTM, current-period, and analyst data
  - `examples/08-calendar.md` for earnings and macro events
  - `examples/01-price-data.md`, `02-quote-data.md`, `04-technical-analysis.md` for chart inputs
  - `examples/06-news.md` for narrative news sourcing

- OpenAPI source (bundled): `./tradingviewapi-docs/openapi.json`
- RapidAPI call examples (bundled, grouped by endpoint): `./tradingviewapi-docs/examples/`
- Base URL (RapidAPI hosted): `https://tradingview-data1.p.rapidapi.com`

> 📦 **Self-contained note**: `tradingviewapi-docs/` is the bundled local copy of the downloaded `tradingviewapi` documentation set for this skill, including real request examples and sample payloads captured from execution. If the contents look stale, refresh the affected files manually from the published API materials and re-align this file to those downloaded docs.

---

## Authentication

**RapidAPI (recommended for external users):**

```bash
curl -H "x-rapidapi-host: tradingview-data1.p.rapidapi.com" \
     -H "x-rapidapi-key: $RAPIDAPI_KEY" \
     "https://tradingview-data1.p.rapidapi.com/api/market-data/NASDAQ:AAPL"
```

**Self-hosted:**

```bash
curl "https://tradingview-data1.p.rapidapi.com/api/market-data/NASDAQ:AAPL"
```

Environment variables: `RAPIDAPI_KEY`, optional `TRADINGS_API_BASE`.

For persistent user setup guidance, prefer the user-level shell configuration described in `./tradingviewapi-docs/README.md` and avoid storing real secrets inside the skill folder or packaged `.skill` artifact.

---

## Symbol Format

All `{symbol}` parameters use `EXCHANGE:TICKER` format:

- Stocks: `NASDAQ:AAPL`, `NYSE:JPM`, `NASDAQ:TSLA`
- ETFs: `NYSE:SPY`, `NASDAQ:QQQ`
- Crypto: `BINANCE:BTCUSDT`
- Indices: `SP:SPX`, `NASDAQ:NDX`
- Forex: `FX:EURUSD`
- Futures: `CME_MINI:ES1!`

If the ticker is ambiguous, resolve it first via `/api/search/market/{query}?filter=stock`.

Pick the `filter` that matches the asset class you are researching:

- Equities / ETFs for this skill's default workflows: `filter=stock`
- Crypto pairs: `filter=crypto`
- FX pairs: `filter=forex`
- Futures: `filter=futures`
- Indices: `filter=index`

**Observed response shape (verified 2026-04-26):**

```bash
curl -H "x-rapidapi-host: tradingview-data1.p.rapidapi.com" \
     -H "x-rapidapi-key: $RAPIDAPI_KEY" \
     "https://tradingview-data1.p.rapidapi.com/api/search/market/NVIDIA?filter=stock"
```

Use `data.markets[]`, not `data[]`.

| Needed field | JSON path |
|---|---|
| First resolved symbol | `data.markets[0].id` |
| Short ticker | `data.markets[0].symbol` |
| Exchange | `data.markets[0].exchange` |
| Description | `data.markets[0].description` |

---

## Scenario A: Quarterly Earnings Analysis (`earnings-analysis`, `earnings-preview`)

### One-shot fetch (highest information density)

```bash
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/market-data/NASDAQ:AAPL"
```

**Observed symbol / fiscal-label caveats (verified 2026-04-26):**

- Treat the request symbol (for example `NASDAQ:NVDA`) or the preflight search result from `/api/search/market/{query}` as canonical.
- Do not rely on `data.company.ticker` or `data.company.exchange` as the canonical listing fields; they may be null or may show a quote venue such as `Cboe One`.
- Treat `data.current.fiscal_period_current` as a provider-side structured label. If it conflicts with the company's own IR / SEC quarter naming, use the latest primary-source quarter label in narrative output and keep the API label only as a structured-data citation detail.

Returns 5 blocks that populate the following report fields:

| Report field | JSON path |
|---|---|
| Company description | `data.company.business_description` |
| CEO | `data.company.ceo` |
| Employee count | `data.company.number_of_employees` |
| Sector / industry | `data.company.sector`, `data.company.industry` |
| Market cap | `data.indicators.market_cap_basic` |
| P/E TTM | `data.indicators.price_earnings` |
| 52-week high / low | `data.indicators.price_52_week_high`, `price_52_week_low` |
| Beta (1y / 3y / 5y) | `data.indicators.beta_1_year`, `beta_3_year`, `beta_5_year` |
| Latest earnings date | `data.indicators.earnings_release_date` (Unix seconds) |
| Next earnings date | `data.indicators.earnings_release_next_date` |
| **Past 8 earnings-release timestamps** | `data.indicators.earnings_release_date_h[]` |
| TTM revenue | `data.ttm.total_revenue_ttm` |
| **Past 8 quarters TTM revenue (for charts)** | `data.ttm.total_revenue_ttm_h[]` |
| TTM net income | `data.ttm.net_income_ttm` |
| **Past 8 quarters net income** | `data.ttm.net_income_ttm_h[]` |
| TTM EBITDA | `data.ttm.ebitda_ttm` |
| **Past 8 quarters EBITDA** | `data.ttm.ebitda_ttm_h[]` |
| TTM gross profit | `data.ttm.gross_profit_ttm`, `gross_profit_ttm_h[]` |
| TTM free cash flow | `data.ttm.free_cash_flow_ttm`, `free_cash_flow_ttm_h[]` |
| TTM diluted EPS | `data.ttm.earnings_per_share_diluted_ttm`, `earnings_per_share_diluted_ttm_h[]` |
| TTM gross margin | `data.ttm.gross_margin_ttm` |
| TTM operating margin | `data.ttm.operating_margin_ttm` |
| TTM net margin | `data.ttm.net_margin_ttm` |
| TTM EBITDA margin | `data.ttm.ebitda_margin_ttm` |
| TTM ROE | `data.ttm.return_on_common_equity_ttm` |
| TTM ROIC | `data.ttm.return_of_invested_capital_percent_ttm` |
| TTM R&D expense | `data.ttm.research_and_dev_ttm` |
| TTM capex | `data.ttm.capital_expenditures_ttm`, `capital_expenditures_unchanged_ttm_h[]` |
| Current fiscal period | `data.current.fiscal_period_current` (e.g. `"2026-Q1"`) |
| Current P/E, P/B, P/S | `data.current.price_earnings_current`, `price_book_current`, `price_sales_current` |
| Current EV | `data.current.enterprise_value_current` |
| Current EV/EBITDA | `data.current.enterprise_value_ebitda_current` |
| Current dividend yield | `data.current.dividends_yield_current` |
| Current D/E | `data.current.debt_to_equity_current` |
| Current-quarter EPS actual | `data.financials_quarterly.earnings_per_share_fq` |
| **Next-quarter EPS consensus** ⭐ | `data.financials_quarterly.earnings_per_share_forecast_next_fq` |

**Key insight**: The 8-element `*_ttm_h[]` arrays are the direct data source for earnings-analysis-required charts like "quarterly revenue progression", "quarterly EPS progression", and "quarterly margin trends".

### Beat / miss analysis

```bash
# Analyst ratings, price targets, buy/hold/sell distribution
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/market-data/NASDAQ:AAPL/analyst-recommendations"

# Quarterly three-statement data (balance sheet / income / cash flow)
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/market-data/NASDAQ:AAPL/financials-quarterly"
```

**Observed analyst payload shape (verified 2026-04-26):**

The endpoint returns a single object under `data.analyst_recommendations`, not an array.

| Needed field | JSON path |
|---|---|
| Recommendation score | `data.analyst_recommendations.recommendation_mark` |
| Total analysts | `data.analyst_recommendations.recommendation_total` |
| Buy / overweight / hold / underweight / sell | `data.analyst_recommendations.recommendation_buy`, `recommendation_over`, `recommendation_hold`, `recommendation_under`, `recommendation_sell` |
| Average / median / high / low target price | `data.analyst_recommendations.price_target_average`, `price_target_median`, `price_target_high`, `price_target_low` |
| Price-target snapshot date | `data.analyst_recommendations.price_target_date` |

### Price chart and technicals

```bash
# Daily 252 bars (~1 year) for stock price chart
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/price/NASDAQ:AAPL?timeframe=D&range=252"

# Real-time quote (pre/post-market, daily change, volume)
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/quote/NASDAQ:AAPL?session=regular&fields=all"

# Multi-timeframe technical signals (for the technical section)
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/ta/NASDAQ:AAPL"

# 50+ individual indicators (RSI / MACD / moving averages / pivots)
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/ta/NASDAQ:AAPL/indicators"
```

**Observed quote payload shape (verified 2026-04-26):**

The quote endpoint returns metadata at `data.symbol` and quote fields under nested `data.data`.

| Needed field | JSON path |
|---|---|
| Symbol | `data.symbol` |
| Last price | `data.data.lp` |
| Daily change | `data.data.ch` |
| Daily change % | `data.data.chp` |
| Volume | `data.data.volume` |
| Market cap | `data.data.market_cap_basic` |
| Session status | `data.data.current_session` |

---

## Scenario B: Initiation Report (`initiating-coverage`)

**Task 1 — Company Research:**

```bash
curl ".../api/market-data/NASDAQ:AAPL/company"          # Company basic info
curl ".../api/market-data/NASDAQ:AAPL/ipo"              # IPO info
curl ".../api/market-data/NASDAQ:AAPL/credit-ratings"   # S&P / Moody's / Fitch ratings
```

**Task 2 — Financial Modeling:**

```bash
curl ".../api/market-data/NASDAQ:AAPL/financials-annual"   # Annual three statements
curl ".../api/market-data/NASDAQ:AAPL/history-annual"      # Multi-year history arrays
curl ".../api/market-data/NASDAQ:AAPL/cash-flow"           # Cash flow breakdown
```

**Task 3 — Valuation:**

```bash
curl ".../api/market-data/NASDAQ:AAPL/enterprise-value"         # EV / EV/EBITDA
curl ".../api/market-data/NASDAQ:AAPL/ttm"                      # Full TTM ratios
curl ".../api/market-data/NASDAQ:AAPL/analyst-recommendations"  # Target-price consensus
curl ".../api/market-data/NASDAQ:AAPL/dividend"                 # Dividend history
```

**Task 4 — Chart Generation:**

Use `/api/price/` plus the `*_h[]` arrays from `/api/market-data/`. No external data needed.

**Sections still requiring Web Search (~10%):**

- Deep business description, product-line detail → company website + 10-K Item 1
- Management bios → LinkedIn + Proxy Statement (DEF 14A)
- Risk factors → 10-K Item 1A
- Segment breakdown (segment revenue) → 10-K / 10-Q footnotes
- Industry research → Gartner / Forrester / IDC

---

## Scenario C: Catalyst Calendar (`catalyst-calendar`)

```bash
# Ranges must be ≤ 40 days, Unix seconds
FROM=$(date -v+0d +%s)
TO=$(date -v+30d +%s)

# Next 30 days of US earnings releases
curl -H "x-rapidapi-key: $RAPIDAPI_KEY" \
  "https://tradingview-data1.p.rapidapi.com/api/calendar/earnings?from=$FROM&to=$TO&market=america"

# Dividend calendar
curl ".../api/calendar/revenue?from=$FROM&to=$TO&market=america"

# IPO calendar
curl ".../api/calendar/ipo?from=$FROM&to=$TO&market=america"

# Macro economic events (CPI, NFP, FOMC)
curl ".../api/calendar/economic?from=$FROM&to=$TO&market=america,china"
```

---

## Scenario D: Morning Note (`morning-note`)

```bash
curl ".../api/news/stock?lang=en&market_country=US"                      # US equity news tape
curl ".../api/news/economic?lang=en"                                     # Macro news tape
curl ".../api/news?symbol=NASDAQ:AAPL&lang=en&market=stock&market_country=US"  # Single-stock news
curl ".../api/quote/NASDAQ:AAPL?session=regular&fields=all"              # Pre/post-market quote
curl ".../api/calendar/economic?from=$FROM&to=$TO&market=america"        # Today's macro releases
curl ".../api/calendar/earnings?from=$FROM&to=$TO&market=america"        # Today's / tomorrow's earnings
```

For multi-name coverage universes, use `POST /api/quote/batch` to pull the same quote fields across the watchlist in one request.

---

## Scenario E: Screening / Idea Generation (`idea-generation`)

```bash
# Top US gainers / losers / high dividend / 52-week highs
curl ".../api/leaderboard/stocks?tab=gainers&market_code=america&count=50"
curl ".../api/leaderboard/stocks?tab=losers&market_code=america&count=50"
curl ".../api/leaderboard/stocks?tab=high_dividend&market_code=america&count=50"

# Hot investment ideas (TradingView community)
curl ".../api/ideas/hot?lang=en&page=1"

# Community views on a specific stock
curl ".../api/ideas/list/NASDAQ:AAPL?lang=en"
curl ".../api/ideas/NASDAQ:AAPL/minds?lang=en"

# Follow-up diligence on screened candidates
curl ".../api/market-data/NASDAQ:AAPL"
curl ".../api/quote/NASDAQ:AAPL?session=regular&fields=all"
curl ".../api/ta/NASDAQ:AAPL"
```

Full list of `tab` values: `/api/metadata/tabs?type=stocks`. Common picks: `gainers`, `losers`, `large_cap`, `high_dividend`, `most_volatile`, `52wk_high`, `overbought`, `oversold`, `penny_stocks`.

---

## Scenario F: Sector Overview (`sector-overview`)

```bash
# Sector categorization + columnset metadata (which columns are selectable)
curl ".../api/metadata/columnsets"
curl ".../api/metadata/tabs?type=stocks"

# Filter by sector (using leaderboard with columnset=valuation/profitability/etc.)
curl ".../api/leaderboard/stocks?tab=all_stocks&market_code=america&columnset=valuation&count=100"

# Drill into representative companies after the screen
curl ".../api/market-data/NASDAQ:AAPL"
curl ".../api/market-data/NASDAQ:MSFT/analyst-recommendations"

# Add macro context for global / cyclical sectors
curl ".../api/world-economy/indicators/full-year-gdp-growth?region=g20"
```

---

## Scenario G: Model Update (`model-update`)

```bash
# Reported quarter actuals + rolling baselines
curl ".../api/market-data/NASDAQ:AAPL"
curl ".../api/market-data/NASDAQ:AAPL/financials-quarterly"

# Consensus and current market context
curl ".../api/market-data/NASDAQ:AAPL/analyst-recommendations"
curl ".../api/quote/NASDAQ:AAPL?session=regular&fields=all"
curl ".../api/market-data/NASDAQ:AAPL/enterprise-value"
```

Use Web Search only for updated guidance wording, transcript commentary, and one-off disclosures that are not represented in the structured payload.

---

## Scenario H: Thesis Tracker (`thesis-tracker`)

```bash
# Baseline thesis scorecard metrics
curl ".../api/market-data/NASDAQ:AAPL"
curl ".../api/market-data/NASDAQ:AAPL/ttm"
curl ".../api/market-data/NASDAQ:AAPL/analyst-recommendations"

# Upcoming catalysts and recent evidence
curl ".../api/calendar/earnings?from=$FROM&to=$TO&market=america"
curl ".../api/news?symbol=NASDAQ:AAPL&lang=en&market=stock&market_country=US"
curl ".../api/news/stock?symbol=NASDAQ:AAPL&lang=en&market_country=US"
```

This scenario is best for maintaining a structured thesis scorecard: earnings cadence, valuation anchor, estimate dispersion, and fresh confirming/disconfirming data points.

---

## Ticker Resolution (generic preflight)

If the user supplies only a company name (e.g. "Apple"), resolve it to `EXCHANGE:TICKER` first:

```bash
curl ".../api/search/market/Apple?filter=stock"
# Returns: { data: { markets: [ { id: "NASDAQ:AAPL", symbol: "AAPL", description: "Apple Inc.", ... } ] } }
```

---

## Full Endpoint Catalog (60 endpoints)

| Category | Endpoints |
|---|---|
| **Market Data (14)** | `/api/market-data/{symbol}` (full), `/company`, `/ipo`, `/current`, `/ttm`, `/indicators`, `/financials-quarterly`, `/financials-annual`, `/history-quarterly`, `/history-annual`, `/dividend`, `/analyst-recommendations`, `/enterprise-value`, `/credit-ratings`, `/cash-flow` |
| **Quote** | `/api/quote/{symbol}`, `/api/quote/batch` (POST) |
| **Price (OHLCV)** | `/api/price/{symbol}`, `/api/price/batch` (POST) |
| **Technical** | `/api/ta/{symbol}`, `/api/ta/{symbol}/indicators` |
| **Calendar** | `/api/calendar/earnings`, `/revenue`, `/ipo`, `/economic` |
| **News (10)** | `/api/news`, `/news/stock`, `/news/crypto`, `/news/forex`, `/news/futures`, `/news/etf`, `/news/bond`, `/news/index`, `/news/economic`, `/news/{newsId}` |
| **Leaderboard** | `/api/leaderboard/stocks`, `/indices`, `/crypto`, `/futures`, `/forex`, `/bonds`, `/corporate-bonds`, `/etfs`, `/data` |
| **Ideas** | `/api/ideas/hot`, `/editors-picks`, `/list/{symbol}`, `/{symbol}/minds`, `/{imageUrl}` |
| **Search** | `/api/search/market/{query}?filter=stock\|etf\|crypto\|forex` |
| **Metadata** | `/api/metadata/markets`, `/exchanges`, `/tabs`, `/columnsets`, `/languages`, `/world-economy/indicators` |
| **World Economy** | `/api/world-economy/indicators/{indicator}` |
| **Realtime** | `/sse/stream` (JWT required), `/api/token/generate`, `/api/mcp/generate` |
| **Health** | `/health` |

---

## Citation Convention (aligned with `earnings-analysis/SKILL.md` lines 50-107)

When citing data obtained from this API in a report:

```
Source: Structured data via tradingviewapi (TradingView); fetched [YYYY-MM-DD]
        Endpoint: /api/market-data/NASDAQ:AAPL
        Fiscal Period: data.current.fiscal_period_current = "2026-Q1"
```

SEC filings (10-Q / 10-K) must still be cited separately with EDGAR hyperlinks. When consensus data comes from this API, cite the `analyst-recommendations` endpoint explicitly instead of a generic terminal label.

---

## Fallback Strategy

1. **API unavailable** → fall back to the skill's original Web Search flow
2. **Missing field** (company has no such metric) → keep field as "N/A"; do not fabricate
3. **Stale data** (`fiscal_period_current` > 90 days behind current quarter) → mark as "last reported" and Web Search to confirm whether a newer release exists
4. **Ticker resolution fails** → ask the user to specify `EXCHANGE:TICKER` explicitly
