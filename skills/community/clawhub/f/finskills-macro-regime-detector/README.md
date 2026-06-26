# macro-regime-detector

> Identify the current US macroeconomic regime using real-time treasury yields, GDP, inflation, and Fed policy data from the [Finskills API](https://finskills.net). Delivers regime classification with asset allocation implications.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Free-brightgreen.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-macro-purple.svg)]()

---

## What This Skill Does

Classifies the current US macro environment into one of six regimes — **Goldilocks**, **Reflation**, **Overheating**, **Stagflation**, **Slowdown**, or **Recession** — based on live data for:

- US Treasury yield curve (2y10y spread, 3m10y spread)
- GDP growth and Industrial Production
- CPI, Core CPI, and PCE inflation trend
- Federal Funds Rate and policy direction
- Commodity cross-checks (Gold, Oil, Copper)

Then maps the regime to an asset allocation framework (OW / N / UW across equities, bonds, commodities, and cash).

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/finskills-macro-regime-detector):

1. Visit **[https://clawhub.ai/finskills/finskills-macro-regime-detector](https://clawhub.ai/finskills/finskills-macro-regime-detector)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: What macro regime are we in right now?
Claude: [Fetches treasury rates, GDP, inflation, Fed policy, commodity data — outputs regime report]
```

## Example Triggers

- `"What's the current macro environment?"`
- `"Are we heading into recession or recovery?"`
- `"How should I position my portfolio given current macro?"`
- `"Is the yield curve inverted?"`
- `"What does the Fed's last move mean for stocks?"`

## API Endpoints Used (All Free Tier)

| Endpoint | Data |
|----------|------|
| `GET /v1/free/macro/treasury-rates` | Full yield curve |
| `GET /v1/free/macro/gdp/US` | GDP growth rate |
| `GET /v1/macro/inflation` | CPI, Core CPI, PCE |
| `GET /v1/macro/interest-rates` | Fed Funds Rate history |
| `GET /v1/free/macro/indicator/UNRATE` | Unemployment rate |
| `GET /v1/free/macro/indicator/INDPRO` | Industrial Production |
| `GET /v1/free/commodity/prices` | Gold, WTI, Copper |

## Regime Framework

| Regime | Growth | Inflation | Best Assets |
|--------|--------|-----------|------------|
| Goldilocks | Expanding | 2–3% | Equities, REITs |
| Reflation | Expanding | Rising | Cyclicals, Energy |
| Overheating | Strong | > 5% | Commodities |
| Stagflation | Slowing | High | Gold, Cash |
| Slowdown | Decelerating | Falling | Defensives, Bonds |
| Recession | Contracting | Low | Cash, Long Bonds |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — all endpoints used are on the free tier
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
