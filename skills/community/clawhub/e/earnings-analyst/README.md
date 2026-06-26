# earnings-analyst

> Track earnings calendars, analyze EPS beat/miss history, measure implied earnings moves, and monitor estimate revision momentum — powered by [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Free%2FPro-yellow.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-event--driven-orange.svg)]()

---

## What This Skill Does

Supports two modes:

**Mode A — Market Earnings Calendar**: Shows all major companies reporting this week, grouped by day with BMO/AMC timing and consensus EPS estimates.

**Mode B — Per-Stock Earnings Deep Dive**: For a specific ticker, delivers EPS/revenue beat rate history, estimate revision trend, options-implied earnings move, and pre-earnings catalyst analysis.

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/earnings-analyst):

1. Visit **[https://clawhub.ai/finskills/earnings-analyst](https://clawhub.ai/finskills/earnings-analyst)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: Who's reporting earnings this week?
Claude: [Fetches earnings calendar, groups by day, flags mega-caps]

You: Deep dive on NVDA earnings — what should I expect?
Claude: [Fetches earnings history, estimates, implied move, news, outputs full report]
```

## Example Triggers

- `"What companies report earnings this week?"`
- `"What's Apple's earnings beat rate?"`
- `"Analyze Microsoft's upcoming earnings"`
- `"What move is the market pricing in for Tesla earnings?"`
- `"Are analyst estimates for NVDA going up or down?"`
- `"Set up a pre-earnings research on META"`

## API Endpoints Used

| Endpoint | Plan | Data |
|----------|------|------|
| `GET /v1/free/market/earnings-calendar` | Free | Weekly earnings schedule |
| `GET /v1/stocks/earnings/{symbol}` | Pro | EPS history + estimates |
| `GET /v1/free/stocks/estimates/{symbol}` | Free | Analyst estimate revisions |
| `GET /v1/news/by-symbol/{symbol}` | Pro | Pre-earnings news |
| `GET /v1/stocks/options/{symbol}` | Pro | Implied move calculation |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available)
- Calendar-only mode works on **free plan**; full per-stock analysis requires **Pro**

## License

MIT — see [LICENSE](../LICENSE)
