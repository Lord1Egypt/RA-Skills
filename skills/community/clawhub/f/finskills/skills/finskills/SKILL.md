---
name: finskills
display_name: Finskills — Stock Quantitative Investment
description: Real-time financial data API for systematic stock analysis and quantitative investment research. Access stock quotes, historical OHLCV, batch screening, company fundamentals (income statement, balance sheet, cash flow), earnings estimates, analyst recommendations, options chains, institutional holders, macroeconomic indicators (GDP, CPI, Fed Funds rate, Treasury yields, FRED series), commodity price signals, SEC filings, and financial news. Use this skill for momentum screening, value/quality factor analysis, earnings event research, portfolio risk assessment, sector rotation, macro factor overlays, and multi-asset market research.
homepage: https://finskills.net
---

# Finskills — Stock Quantitative Investment

Use the Finskills REST API at `https://finskills.net` to perform systematic stock analysis and quantitative investment research in real time.

## Authentication

All requests require the `X-API-Key` header. Ask the user for their key if not provided.
Get a key at: https://finskills.net/register

```
X-API-Key: YOUR_API_KEY_HERE
```

Base URL: `https://finskills.net`

## Quick Start

1. Ask the user for their Finskills API key if not already provided.
2. Make HTTP requests to `https://finskills.net/v1/...` with the `X-API-Key` header.
3. Use `/v1/free/...` endpoints whenever available — they work with any valid API key.
4. For universe-level analysis, always start with the **batch quote** endpoint to minimize API calls.

---

## Endpoint Reference

### 1. Stock Screening & Universe Pricing

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/stocks/quote/{symbol}` | Real-time price, change%, volume, market cap, P/E, 52-week range | symbol e.g. `AAPL` |
| `GET /v1/stocks/quotes?symbols=` | Batch quotes for a stock universe (up to 50 symbols) | `symbols=AAPL,MSFT,GOOGL` (CSV) |
| `GET /v1/stocks/search?q=` | Find stocks by company name or ticker | `q=apple` |
| `GET /v1/market/summary` | Major indices (S&P 500, Dow, Nasdaq), trending tickers, top movers | — |
| `GET /v1/market/sectors` | S&P 500 sector performance — all 11 GICS sectors with daily returns | — |

### 2. Historical Price & OHLCV Data

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/stocks/history/{symbol}` | Historical OHLCV candlestick data | `interval`: 1d / 1wk / 1mo · `from`: YYYY-MM-DD · `to`: YYYY-MM-DD |

**Interval selection guide:**
- `1d` — Daily close prices: momentum signals, moving averages (SMA/EMA), daily returns, volatility (σ)
- `1wk` — Weekly: medium-term trends, 52-week return calculation, relative strength
- `1mo` — Monthly: long-term factor models, Fama-French style analysis

**Derived metrics from history data:**
- **Simple return**: `(Pt / P0) - 1`
- **Annualized volatility**: `std(daily_returns) × √252`
- **12-1 month momentum**: `(P[t-1] / P[t-12]) - 1` (skip most recent month)
- **Max drawdown**: `max((P_peak - P_trough) / P_peak)` over a period

### 3. Company Fundamentals

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/stocks/profile/{symbol}` | Company description, sector, industry, employee count, country, exchange | — |
| `GET /v1/stocks/financials/{symbol}` | Income statement, balance sheet, cash flow statements | `freq`: `yearly` (default) / `quarterly` |
| `GET /v1/stocks/earnings/{symbol}` | EPS history, actuals vs. estimates, surprise%, next earnings date | — |
| `GET /v1/stocks/dividends/{symbol}` | Full dividend payment history and yield | — |

**Key metrics available from `/v1/stocks/financials`:**
| Metric | Statement | Formula / Field |
|--------|-----------|-----------------|
| Revenue growth | Income | `revenue[t] / revenue[t-1] - 1` |
| Gross margin | Income | `grossProfit / revenue` |
| EBITDA margin | Income | `ebitda / revenue` |
| Net margin | Income | `netIncome / revenue` |
| ROE | Income + Balance | `netIncome / shareholdersEquity` |
| ROA | Income + Balance | `netIncome / totalAssets` |
| Debt/Equity | Balance | `totalDebt / shareholdersEquity` |
| Current ratio | Balance | `currentAssets / currentLiabilities` |
| FCF yield | Cash Flow + Quote | `freeCashFlow / marketCap` |
| CapEx intensity | Cash Flow | `capitalExpenditure / revenue` |

### 4. Market Intelligence & Analyst Data

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/stocks/recommendations/{symbol}` | Analyst buy/hold/sell counts with trend over recent periods | — |
| `GET /v1/stocks/holders/{symbol}` | Top institutional holders, insider ownership %, 13F data | — |
| `GET /v1/stocks/options/{symbol}` | Full options chain: strikes, expiries, IV, bid/ask, open interest, Greeks | `date`: YYYY-MM-DD (expiry filter) |

**Options-derived signals:**
- **Implied Volatility (IV)**: measure of market-priced uncertainty before earnings
- **Put/Call ratio**: `put_open_interest / call_open_interest` — elevated ratio signals bearish positioning
- **IV Rank**: compare current IV to 52-week range to assess richness of options premiums

### 5. Macroeconomic & Risk Context

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/macro/inflation` | US CPI monthly series (YoY and MoM) | — |
| `GET /v1/macro/interest-rates` | US Federal Funds effective rate history | — |
| `GET /v1/macro/gdp` | US GDP time series | — |
| `GET /v1/macro/indicator/{series}` | Any FRED series by ID | `series`: CPIAUCSL, FEDFUNDS, UNRATE, T10Y2Y … |
| `GET /v1/free/macro/gdp` | World Bank GDP by country | `countryCode`: US / CN / JP / DE / GB |
| `GET /v1/free/macro/indicator/{indicator}` | World Bank macro indicator | `indicator`: CPI / GDP / UNEMPLOYMENT · `country`: US |
| `GET /v1/free/macro/treasury-rates` | Full US Treasury yield curve (1-month to 30-year) | — |
| `GET /v1/free/forex/rates` | Live exchange rates (150+ currencies) | `base`: USD / EUR / GBP / JPY / CNY |
| `GET /v1/free/forex/history` | Historical forex rate series | `base`, `target`, `startDate`, `endDate` (YYYY-MM-DD) |

**Essential FRED series for quantitative research:**

| Series ID | Description | Signal Use |
|-----------|-------------|------------|
| `CPIAUCSL` | US CPI All Items (inflation) | Inflation regime classification |
| `FEDFUNDS` | Federal Funds Effective Rate | Rate cycle position |
| `UNRATE` | US Unemployment Rate | Economic cycle indicator |
| `T10Y2Y` | 10Y minus 2Y Treasury spread | Yield curve inversion warning |
| `T10YIE` | 10-Year Breakeven Inflation Rate | Real rate expectations |
| `BAMLH0A0HYM2` | US High-Yield OAS credit spread | Risk appetite / stress indicator |
| `VIXCLS` | CBOE VIX Volatility Index | Market fear gauge |
| `MORTGAGE30US` | 30-Year Fixed Mortgage Rate | Housing sector pressure |
| `DGS10` | 10-Year Treasury Constant Maturity | Risk-free rate benchmark |

### 6. Commodity Price Signals

Use commodity prices as macro signals for sector analysis and portfolio risk.

**Categories:** `energy` · `metals_precious` · `metals_industrial` · `agriculture` · `livestock`

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/free/commodity/prices` | Real-time prices for all or one category | `category`: energy / metals_precious / agriculture |
| `GET /v1/free/commodity/price/{symbol}` | Single commodity real-time quote | symbol: `CL=F`, `GC=F`, `HG=F` |
| `GET /v1/free/commodity/history/{symbol}` | Commodity OHLCV history | `range`: 1d/5d/1mo/3mo/6mo/1y/2y/5y · `interval`: 1d/1wk/1mo |
| `GET /v1/free/commodity/fred/{seriesId}` | FRED daily commodity historical series | `limit`: 365 · `startDate`: YYYY-MM-DD |
| `GET /v1/free/commodity/imf/batch` | IMF monthly data for multiple commodities | `indicators`: POILAPSP,PGOLD,PCOPP (CSV) |
| `GET /v1/free/commodity/imf/{indicator}` | IMF single commodity monthly series | `periods`: 60 (default) |

**Key commodity instruments:**

| Symbol | Commodity | Macro Signal |
|--------|-----------|--------------|
| `CL=F` | WTI Crude Oil | Energy sector costs, inflation driver |
| `BZ=F` | Brent Crude | Global oil benchmark |
| `NG=F` | Natural Gas | Utilities, industrial energy costs |
| `GC=F` | Gold | Safe-haven demand, real rate proxy |
| `SI=F` | Silver | Industrial + monetary demand |
| `HG=F` | Copper | "Dr. Copper" — leading economic growth indicator |
| `ZC=F` | Corn | Agriculture input costs, ethanol |
| `ZW=F` | Wheat | Food inflation signal |
| `ZS=F` | Soybeans | Global protein demand, China trade |

**FRED commodity series:** `DCOILWTICO` (WTI daily), `DCOILBRENTEU` (Brent daily), `DHHNGSP` (Natural Gas), `GOLDAMGBD228NLBM` (Gold AM Fix)

**IMF indicators:** `POILAPSP` (crude avg), `PGOLD`, `PSILVER`, `PCOPP`, `PWHEAMT`, `PMAIZMT`, `PSOYBEAN`, `PNICK`

### 7. Alternative Data: News & SEC Filings

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/news/by-symbol/{symbol}` | News articles linked to a specific stock | symbol |
| `GET /v1/free/news/finance` | Latest financial news headlines | — |
| `GET /v1/free/sec/filings/{cik}` | SEC filings: 10-K (annual), 10-Q (quarterly), 8-K (events) | `cik`: company CIK |
| `GET /v1/free/sec/company-facts/{cik}` | XBRL-structured financial facts from SEC EDGAR | `cik` |

**Common CIK numbers:**
Apple `0000320193` · Microsoft `0000789019` · Tesla `0001318605` · Amazon `0001018724`
Alphabet `0001652044` · Meta `0001326801` · Nvidia `0001045810` · Berkshire `0001067983`

### 8. Cryptocurrency & Crypto Macro

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/free/crypto/price/{coinId}` | Current price, market cap, 24h change, volume | `coinId`: bitcoin, ethereum, solana |
| `GET /v1/free/crypto/markets` | Top coins ranked by market cap | `perPage`: 100 (max 250) |
| `GET /v1/free/crypto/history/{coinId}` | Historical prices (daily) | `days`: 7 / 30 / 90 / 365 |

Use CoinGecko IDs (bitcoin, ethereum, solana) — not ticker symbols (BTC, ETH).

---

## Quantitative Analysis Workflows

### Momentum Strategy (Price-based)
Rank stocks by 12-1 month return (skip the most recent month to avoid short-term reversal).

```
Step 1: GET /v1/stocks/quotes?symbols=AAPL,MSFT,GOOGL,META,NVDA,...
        → Get current prices for universe

Step 2: GET /v1/stocks/history/{symbol}?interval=1mo
        → Compute momentum = (P[t-1] / P[t-12]) - 1 for each stock

Step 3: Rank by momentum score; long top quintile, underweight bottom quintile

Step 4: GET /v1/market/sectors → Confirm sector-level momentum alignment
```

### Value / Quality Screening (Fundamental)

```
Step 1: GET /v1/stocks/quote/{symbol}
        → trailingPE, priceToBook, marketCap

Step 2: GET /v1/stocks/financials/{symbol}?freq=yearly
        → Compute: ROE = netIncome / shareholdersEquity
        → Compute: FCF yield = freeCashFlow / marketCap
        → Compute: Debt/Equity = totalDebt / shareholdersEquity
        → Compute: Revenue growth (YoY)

Step 3: Quality filter: ROE > 15%, Debt/Equity < 1.5, FCF yield > 3%
        Value filter: PE < sector median, PB < 3

Step 4: GET /v1/stocks/recommendations/{symbol}
        → Confirm analyst consensus is not broadly negative
```

### Earnings Event-Driven (PEAD)

```
Step 1: GET /v1/stocks/earnings/{symbol}
        → Find quarters with EPS surprise > 5%
        → Look for consecutive beats as quality/momentum signal

Step 2: GET /v1/stocks/history/{symbol}?from={reportDate}&interval=1d
        → Measure post-earnings price drift (PEAD) over 60 days

Step 3: GET /v1/news/by-symbol/{symbol}
        → Verify fundamental catalyst vs. transient market noise

Step 4: GET /v1/stocks/options/{symbol}
        → Check pre-earnings IV spike to assess market expectations
```

### Risk Environment Dashboard

```
Step 1: GET /v1/free/macro/treasury-rates
        → Check full yield curve shape (normal / flat / inverted)

Step 2: GET /v1/macro/indicator/T10Y2Y
        → Spread < 0: yield curve inverted → recession risk elevated

Step 3: GET /v1/macro/indicator/VIXCLS
        → VIX > 25: elevated fear; VIX > 30: stress conditions

Step 4: GET /v1/macro/indicator/BAMLH0A0HYM2
        → Credit spreads widening → risk-off, reduce beta exposure

Step 5: GET /v1/macro/interest-rates + GET /v1/macro/inflation
        → Rate/inflation quadrant: determines sector rotation bias

Step 6: GET /v1/free/commodity/price/GC=F
        → Gold rising = safe-haven demand increasing
```

### Sector Rotation (Macro-driven)

```
Step 1: GET /v1/market/sectors → Identify leading and lagging sectors (by 1-day and YTD return)

Step 2: GET /v1/macro/interest-rates + GET /v1/macro/inflation
        Regime mapping:
        - High inflation + rising rates → Energy, Financials, Materials, Industrials
        - Low inflation + falling rates  → Tech, Consumer Discretionary, Real Estate
        - Stagflation                    → Energy, Gold, Consumer Staples, Healthcare
        - Goldilocks (low rates, growth) → Tech, Small Cap Growth, Discretionary

Step 3: GET /v1/stocks/quotes?symbols=XLE,XLF,XLK,XLV,XLI,XLP,XLRE,XLU,XLY,XLB,XLC
        → Confirm sector ETF momentum aligns with macro regime

Step 4: GET /v1/free/commodity/prices?category=energy
        → Energy commodity trend confirms / contradicts sector call
```

### Multi-Factor Portfolio Overlay

```
Step 1: GET /v1/macro/gdp + GET /v1/macro/inflation + GET /v1/macro/interest-rates
        → Establish macro regime (growth/inflation quadrant)

Step 2: GET /v1/free/macro/treasury-rates
        → Full yield curve + duration risk assessment

Step 3: GET /v1/free/forex/rates?base=USD
        → Dollar strength (DXY proxy): strong USD headwind for multinationals

Step 4: GET /v1/free/commodity/prices → Energy, copper as economic leading indicators

Step 5: GET /v1/market/sectors → Top-down sector allocation
        → Apply bottom-up stock screening within target sectors
```

---

## Example Interactions

**Batch screening:**
> "Screen the Magnificent 7 stocks for momentum and valuation"
→ `GET /v1/stocks/quotes?symbols=AAPL,MSFT,GOOGL,META,NVDA,AMZN,TSLA` for pricing/PE, then `/v1/stocks/history/{symbol}?interval=1mo` per stock for momentum

**Deep fundamental analysis:**
> "Analyze Apple's financial quality: margins, ROE, free cash flow"
→ `GET /v1/stocks/financials/AAPL?freq=yearly` (multi-year), compute ROE, margins, FCF yield; also `GET /v1/stocks/earnings/AAPL` for EPS trend

**Earnings research:**
> "Has Microsoft been consistently beating estimates?"
→ `GET /v1/stocks/earnings/MSFT` — show EPS actuals vs. estimates, surprise% per quarter

**Analyst sentiment:**
> "What is the analyst consensus on Nvidia?"
→ `GET /v1/stocks/recommendations/NVDA` — show buy/hold/sell count trend

**Institutional ownership:**
> "Who are the major institutional holders of Tesla?"
→ `GET /v1/stocks/holders/TSLA`

**Options volatility:**
> "What is the implied volatility on NVIDIA before earnings?"
→ `GET /v1/stocks/options/NVDA` — show front-month IV, put/call ratio

**Yield curve:**
> "Is the yield curve currently inverted? Show me the full curve."
→ `GET /v1/free/macro/treasury-rates`, then `GET /v1/macro/indicator/T10Y2Y` for spread history

**Macro inflation:**
> "How has US inflation been trending over the past 2 years?"
→ `GET /v1/macro/inflation` or `GET /v1/macro/indicator/CPIAUCSL`

**Rate environment:**
> "Where is the Fed Funds rate relative to historical levels?"
→ `GET /v1/macro/interest-rates` — show rate history and current level

**Sector rotation:**
> "Which sectors are outperforming today? What does it signal?"
→ `GET /v1/market/sectors`, cross-reference with `GET /v1/macro/interest-rates`

**Copper as economic signal:**
> "Is Dr. Copper signaling economic expansion or contraction?"
→ `GET /v1/free/commodity/history/HG=F?range=1y&interval=1wk` — trend + recent momentum

**Gold safe haven:**
> "Is gold rising? Is there safe-haven demand?"
→ `GET /v1/free/commodity/price/GC=F` + `GET /v1/free/commodity/history/GC=F?range=3mo`

**Oil macro impact:**
> "How does the current WTI crude price compare to last year?"
→ `GET /v1/free/commodity/fred/DCOILWTICO?startDate=2024-01-01`

**SEC filing research:**
> "Find Tesla's latest 10-K annual report"
→ `GET /v1/free/sec/filings/0001318605` (filter for `form: 10-K`)

**Company dividend history:**
> "Does Microsoft pay dividends? Show history."
→ `GET /v1/stocks/dividends/MSFT`

**News catalyst:**
> "What news is driving Amazon's stock move today?"
→ `GET /v1/news/by-symbol/AMZN`

---

## Data & Presentation Guidelines

- **Batch first**: For >3 stocks, use `/v1/stocks/quotes?symbols=` rather than individual calls.
- **Cite freshness**: Always note "as of [date]" and data source (Yahoo Finance, FRED, World Bank, SEC EDGAR).
- **Units always**: USD, %, bps, × (multiple), $ millions/billions as appropriate.
- **No investment advice**: Present data and derived metrics factually. Say "the data shows…" not "you should buy/sell".
- **Large number formatting**: `$1.23B`, `$456.7M`, `2.4×` — never raw 9-digit numbers.
- **Rate limiting**: Free plan = 30 requests/min. Paid plans vary. Use batch endpoints to stay within limits.
- **Historical depth**: `/v1/stocks/history` supports `from` / `to` date range; `interval=1wk` for longer series with fewer data points.
