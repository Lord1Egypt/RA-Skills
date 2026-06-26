# us-stock-analyzer

> Institutional-grade US equity analysis powered by [Finskills API](https://finskills.net). Delivers comprehensive fundamental, valuation, and analyst consensus analysis in a structured investment report.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-stock--analysis-green.svg)]()

---

## What This Skill Does

When you ask Claude to analyze a stock (e.g., "analyze NVDA" or "give me a bull/bear case on AAPL"), this skill:

1. Fetches real-time price, company profile, 3–5 year financials, analyst ratings, earnings history, and institutional holders — all via the Finskills API
2. Scores the business on four quality dimensions (moat, management, revenue, growth)
3. Computes 7 financial health metrics with benchmarks
4. Performs multi-method valuation (P/E, EV/EBITDA, P/FCF, PEG)
5. Summarizes analyst consensus and earnings beat rate
6. Delivers a verdict with price target and confidence rating

## Install

```bash
npx skills add https://github.com/finskills/us-stock-analyzer
```

## Quick Start

```
You: Analyze MSFT — give me a full fundamental report
Claude: [Fetches data via Finskills API and generates structured report]
```

## Example Triggers

- `"Deep dive on NVDA"`
- `"Is AMZN overvalued right now?"`
- `"Give me a buy/sell rating on META"`
- `"Analyze Apple's financial health"`
- `"What do analysts think about Tesla?"`

## API Endpoints Used

| Endpoint | Data |
|----------|------|
| `GET /v1/stocks/quote/{symbol}` | Real-time price, 52-week range, volume |
| `GET /v1/stocks/profile/{symbol}` | Company description, sector, industry |
| `GET /v1/stocks/financials/{symbol}` | Income statement, balance sheet, cash flow |
| `GET /v1/stocks/recommendations/{symbol}` | Analyst ratings, price targets |
| `GET /v1/stocks/earnings/{symbol}` | Earnings history, EPS estimates |
| `GET /v1/stocks/holders/{symbol}` | Institutional ownership |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) — free tier available; Pro plan required for full access (historical data, financials, batch quotes)
- **Claude** with skill support (Claude.ai, Claude Desktop, or compatible client)

## Output Example

```
═══════════════════════════════════════════════════
  US STOCK ANALYSIS REPORT — NVDA (2025-04-18)
═══════════════════════════════════════════════════

📌 COMPANY SNAPSHOT
  NVIDIA Corporation | Technology | Semiconductors
  Price: $875.40  Change: +2.1%  Market Cap: $2.15T

📊 BUSINESS QUALITY SCORE: 4.75/5
  ◦ Competitive Moat:   5/5 — CUDA ecosystem lock-in, dominant AI training share
  ◦ Management Quality: 5/5 — 35%+ FCF margin consistently; disciplined capex
  ...

🎯 INVESTMENT VERDICT
  Rating:     BUY
  12M Target: $1,050  (Bull: $1,300 | Bear: $700)
  Confidence: HIGH
═══════════════════════════════════════════════════
```

## License

MIT — see [LICENSE](../LICENSE)
