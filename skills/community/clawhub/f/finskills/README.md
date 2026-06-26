# Finskills — Stock Quantitative Investment Skill

> An AI skill that gives Claude and other assistants real-time access to stock quotes, OHLCV history, company fundamentals, earnings data, analyst recommendations, macroeconomic indicators, commodity signals, SEC filings, and financial news — purpose-built for systematic investment analysis.

[![Anthropic Skills](https://img.shields.io/badge/Anthropic-Skills-blueviolet)](https://github.com/anthropics/skills)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

## Why Finskills?

| Feature | Description |
|---------|-------------|
| **Real-time Data** | Live market quotes and OHLCV, not static training data |
| **9 Data Categories** | Stocks · Fundamentals · Options · Macro · Commodities · Forex · News · Filings · Crypto |
| **Quantitative Focus** | Designed for factor analysis, screening, and systematic research workflows |
| **Free Tier** | Most endpoints work with any valid API key at no cost |
| **Standard Format** | Follows [Anthropic SKILL.md](https://github.com/anthropics/skills) specification |

## Quick Start

### 1. Get an API Key

Register at [finskills.net/register](https://finskills.net/register) — free tier available.

### 2. Install the Skill

Choose one of the methods below:

#### Claude Code (npx)

```bash
npx skills add finskills/finskills
```

#### Claude.ai (Project Knowledge)

1. Open [claude.ai](https://claude.ai) → select or create a Project
2. Go to **Project Knowledge** → click **Add content**
3. Download [`SKILL.md`](skills/finskills/SKILL.md) and upload it as project knowledge

#### Cursor

```bash
# Download into Cursor rules directory
mkdir -p .cursor/rules
curl -o .cursor/rules/finskills.mdc https://finskills.net/SKILL.md
```

#### VS Code Copilot

```bash
# Add to project-level Copilot instructions
mkdir -p .github
curl -o .github/copilot-instructions.md https://finskills.net/SKILL.md
```

#### Manual Download

```bash
curl -O https://finskills.net/SKILL.md
```

### 3. Set Your API Key

When prompted, provide your API key. It will be sent as the `X-API-Key` header on all requests.

### 4. Start Querying

Ask natural language questions — no special commands needed.

## Example Prompts

| You ask | Endpoints called |
|---------|-----------------|
| "Screen the Magnificent 7 for momentum and valuation" | `/v1/stocks/quotes?symbols=AAPL,MSFT,GOOGL,META,NVDA,AMZN,TSLA` + history per stock |
| "Analyze Apple's financial quality: ROE, margins, FCF" | `/v1/stocks/financials/AAPL?freq=yearly` |
| "Has Microsoft been consistently beating earnings?" | `/v1/stocks/earnings/MSFT` |
| "Is the yield curve inverted? Show the full curve." | `/v1/free/macro/treasury-rates` + `/v1/macro/indicator/T10Y2Y` |
| "Which sectors are outperforming? What does macro say?" | `/v1/market/sectors` + `/v1/macro/interest-rates` + `/v1/macro/inflation` |
| "What is the current gold price and trend?" | `/v1/free/commodity/price/GC=F` + `/v1/free/commodity/history/GC=F?range=3mo` |
| "Is copper signaling economic expansion?" | `/v1/free/commodity/history/HG=F?range=1y&interval=1wk` |
| "Find Tesla's latest 10-K SEC filing" | `/v1/free/sec/filings/0001318605` |
| "What is Nvidia's implied volatility before earnings?" | `/v1/stocks/options/NVDA` |
| "Show macro risk dashboard: VIX, credit spreads, curve" | `/v1/macro/indicator/VIXCLS` + `/v1/macro/indicator/T10Y2Y` + `/v1/free/macro/treasury-rates` |

## Supported Data Categories

- **Stocks** — Real-time quotes, batch pricing, historical OHLCV, company profiles, search
- **Fundamentals** — Income statement, balance sheet, cash flow, earnings history, dividends
- **Market Intelligence** — Analyst recommendations, institutional holders, options chains
- **Market Overview** — Major indices, sector performance, trending tickers, top movers
- **Macroeconomics** — US GDP/CPI/Fed Funds rate, full Treasury yield curve, 50+ FRED series, World Bank global indicators
- **Commodities** — Real-time futures for 27 instruments (energy, precious metals, industrial metals, agriculture, livestock); FRED daily series; IMF monthly price indicators
- **Forex** — Live exchange rates (150+ currencies), historical rate series
- **News** — Financial headlines, stock-specific news articles
- **SEC Filings** — 10-K, 10-Q, 8-K filings; XBRL structured financial data via EDGAR
- **Cryptocurrency** — Prices, market rankings, historical data (bitcoin, ethereum, solana…)

## Quantitative Workflows

### Momentum Strategy
Rank stocks by 12-1 month return (skip recent month to avoid reversal).
```
GET /v1/stocks/quotes?symbols=...         → Universe pricing
GET /v1/stocks/history/{symbol}?interval=1mo  → Monthly returns for ranking
GET /v1/market/sectors                    → Sector momentum confirmation
```

### Value / Quality Screening
```
GET /v1/stocks/quote/{symbol}             → P/E, P/B, market cap
GET /v1/stocks/financials/{symbol}        → ROE, FCF yield, Debt/Equity, margins
GET /v1/stocks/recommendations/{symbol}   → Analyst consensus check
```

### Risk Environment Assessment
```
GET /v1/free/macro/treasury-rates         → Yield curve shape
GET /v1/macro/indicator/T10Y2Y            → Inversion signal (recession risk)
GET /v1/macro/indicator/VIXCLS            → Market fear gauge
GET /v1/macro/indicator/BAMLH0A0HYM2      → High-yield credit spreads
GET /v1/macro/interest-rates + inflation  → Rate/inflation regime
```

### Sector Rotation (Macro-driven)
```
Rising rates + high inflation → Energy, Financials, Materials, Industrials
Low rates + low inflation     → Tech, Consumer Discretionary, Real Estate
GET /v1/market/sectors        → Confirm which sectors are actually leading
```

## How It Works

```
You ask a question
        ↓
SKILL.md tells Claude which endpoint to call
        ↓
Claude sends HTTP request to Finskills API (with X-API-Key header)
        ↓
Finskills returns real-time JSON data
        ↓
Claude formats a contextualized, data-driven answer
```

## Project Structure

```
finskills/
├── LICENSE
├── README.md
└── skills/
    └── finskills/
        └── SKILL.md          ← The skill definition file
```

## MCP Support

Finskills also supports the **Model Context Protocol (MCP)** for direct tool-based integration.
See the [MCP documentation](https://finskills.net/documentation) on the website for setup details.

## Links

- **Website**: [finskills.net](https://finskills.net)
- **API Docs**: [finskills.net/documentation](https://finskills.net/documentation)
- **Skill Page**: [finskills.net/skill](https://finskills.net/skill)
- **Register**: [finskills.net/register](https://finskills.net/register)
- **Anthropic Skills Spec**: [github.com/anthropics/skills](https://github.com/anthropics/skills)

## License

[Apache License 2.0](LICENSE)
