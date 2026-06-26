# crypto-market-analyst

> Analyze Bitcoin, Ethereum, and altcoins with market cap/dominance, BTC halving cycle positioning, altcoin season detection, and risk assessment — all via free-tier [Finskills API](https://finskills.net) crypto endpoints.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Free-brightgreen.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-crypto-yellow.svg)]()

---

## What This Skill Does

1. Fetches the full crypto market overview: top 20+ coins by market cap with 24h/7D performance
2. Computes Bitcoin and Ethereum dominance percentages, plus altcoin dominance
3. Analyzes BTC halving cycle position (last halving: April 2024)
4. Calculates 30-day annualized volatility and ATH drawdown for key coins
5. Detects **Altcoin Season** vs. **Bitcoin Season** (what % of top 20 beat BTC in 7D)
6. Estimates market sentiment (Extreme Greed / Fear) from price data
7. Maps macro context (equity correlation, Fed policy, gold comparison)
8. Outputs structured regime classification with positioning guidance

**All API endpoints used are on the free tier — no Pro plan required.**

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/crypto-market-analyst):

1. Visit **[https://clawhub.ai/finskills/crypto-market-analyst](https://clawhub.ai/finskills/crypto-market-analyst)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: Give me a crypto market analysis
Claude: [Fetches top 20 market data + BTC/ETH history, computes dominance, cycle, alts vs BTC, outputs report]
```

## Example Triggers

- `"What's the current state of the crypto market?"`
- `"Is Bitcoin in a bull market right now?"`
- `"Are we in altcoin season?"`
- `"Compare Solana, Ethereum, and Avalanche performance"`
- `"What does BTC dominance tell us right now?"`
- `"How far are we from the last Bitcoin halving?"`

## Key Signals Generated

| Signal | Description |
|--------|-------------|
| BTC Dominance | > 55% = Bitcoin Season; < 45% = Altcoin Season |
| Cycle Phase | Position relative to April 2024 halving |
| ATH Distance | % below all-time high (bear market proxy) |
| Altcoin Season | % of top 20 coins outperforming BTC in 7D |
| Sentiment | Extreme Greed → Extreme Fear from data proxies |

## API Endpoints Used (All Free)

| Endpoint | Data |
|----------|------|
| `GET /v1/free/crypto/markets` | Top 20+ coins, market caps, 24h/7D performance |
| `GET /v1/free/crypto/price/{coinId}` | Single coin details |
| `GET /v1/free/crypto/history/{coinId}` | Historical prices for BTC, ETH, altcoins |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **free plan is sufficient**
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
