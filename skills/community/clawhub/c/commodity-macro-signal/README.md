# commodity-macro-signal

> Analyze energy, metals, and agricultural commodity prices to extract macro signals for inflation, growth, and sector rotation — all via free-tier [Finskills API](https://finskills.net) commodity endpoints.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Free-brightgreen.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-macro-commodities-brown.svg)]()

---

## What This Skill Does

1. Fetches a full commodity price dashboard: energy (WTI/Brent, NatGas), metals (Gold, Silver, Copper), agricultural (Wheat, Corn, Soybeans)
2. Computes 1M/3M/YTD trends per commodity
3. Calculates macro signal ratios: Gold/Silver ratio, Copper/Gold ratio ("Dr. Copper")
4. Fetches FRED and IMF commodity indices for broader cycle context
5. Classifies current commodity super-cycle phase (Early Bull → Late Bear)
6. Maps commodity signals to sector and asset class implications (OW/N/UW)

**All API endpoints used are on the free tier — no Pro plan required.**

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/commodity-macro-signal):

1. Visit **[https://clawhub.ai/finskills/commodity-macro-signal](https://clawhub.ai/finskills/commodity-macro-signal)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: What are commodity prices telling us about the macro environment?
Claude: [Fetches all commodity prices + history + FRED series, computes ratios, outputs macro signal report]
```

## Example Triggers

- `"What's the signal from oil prices right now?"`
- `"Is gold rising for good or bad reasons?"`
- `"What is Dr. Copper saying about the economy?"`
- `"Give me a commodities macro panel"`
- `"Should I overweight energy or materials based on commodities?"`

## Key Signal Ratios

| Ratio | Interpretation |
|-------|---------------|
| Gold/Silver > 80 | Risk-off, economic uncertainty |
| Gold/Silver < 60 | Risk-on, industrial expansion |
| Copper/Gold rising | Growth regime, yields following |
| Copper/Gold falling | Deflationary / slowdown signal |
| WTI > $90 | High inflation pressure or supply shock |
| WTI < $60 | Disinflation, consumer spending tailwind |

## API Endpoints Used (All Free)

| Endpoint | Data |
|----------|------|
| `GET /v1/free/commodity/prices` | All commodity spot prices |
| `GET /v1/free/commodity/history/{symbol}` | 1Y history for WTI, Gold, Copper |
| `GET /v1/free/commodity/fred/{seriesId}` | FRED commodity series (DCOILWTICO, etc.) |
| `GET /v1/free/commodity/imf` | IMF all-commodity + sub-indices |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **free plan is sufficient**
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
