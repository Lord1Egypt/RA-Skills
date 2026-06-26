# portfolio-manager

> Real-time portfolio analysis and rebalancing advisor for US equity portfolios — powered by [Finskills API](https://finskills.net) batch quotes, sector data, and market summary.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-portfolio-blue.svg)]()

---

## What This Skill Does

Provide your holdings list and this skill fetches live prices for every position, then:

1. Computes current value, daily P&L, and total return for each position
2. Calculates portfolio-level daily return vs. S&P 500
3. Maps sector allocation and flags overweight/underweight vs. benchmark
4. Estimates portfolio Beta and flags concentration risk
5. Generates rebalancing recommendations with specific share quantities

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/finskills-portfolio-manager):

1. Visit **[https://clawhub.ai/finskills/finskills-portfolio-manager](https://clawhub.ai/finskills/finskills-portfolio-manager)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: Here's my portfolio: AAPL 50 shares, MSFT 30 shares, NVDA 20 shares, GOOGL 15 shares.
     Cost basis: AAPL $150, MSFT $280, NVDA $400, GOOGL $120. Analyze it.
Claude: [Fetches live quotes, calculates P&L, sectors, risk metrics, rebalancing suggestions]
```

## Example Triggers

- `"Analyze my portfolio: AAPL 100sh, TSLA 50sh, META 30sh"`
- `"How is my portfolio doing today vs the market?"`
- `"What sectors am I overweight in?"`
- `"Should I rebalance? I want 60% tech, 20% healthcare, 20% financials"`
- `"What's my portfolio's estimated beta?"`

## API Endpoints Used

| Endpoint | Data |
|----------|------|
| `GET /v1/stocks/quotes` | Batch real-time prices for all holdings |
| `GET /v1/market/summary` | S&P 500/Nasdaq/Dow benchmark data |
| `GET /v1/market/sectors` | 11 GICS sector performance |
| `GET /v1/stocks/profile/{symbol}` | Sector/industry classification |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — Pro plan for batch quotes and market data
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
