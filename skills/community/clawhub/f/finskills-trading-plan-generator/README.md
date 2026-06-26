# trading-plan-generator

> Convert any stock idea into a complete, professional trading plan: entry trigger, ATR-based stop-loss, risk-based position sizing, multi-target exits, time stop, and thesis validation — powered by live data from [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-trading-red.svg)]()

---

## What This Skill Does

1. Fetches live quote, 6-month OHLCV history, and analyst recommendations
2. Identifies 3 support and 3 resistance levels from price structure
3. Computes ATR (14) for volatility-based stop placement
4. Sizes position using Fixed Risk method: `Shares = (Account × Risk%) / Stop_Distance`
5. Sets Target 1 (2:1 R:R), Target 2 (3:1), Target 3 (analyst target)
6. Creates a formal 3-part thesis: Catalyst, Invalidation, Monitoring
7. Outputs a complete trading plan in structured format

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/finskills-trading-plan-generator):

1. Visit **[https://clawhub.ai/finskills/finskills-trading-plan-generator](https://clawhub.ai/finskills/finskills-trading-plan-generator)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: I want to trade NVDA long, I have a $50K account and can risk 2% per trade
Claude: [Fetches NVDA quote + history + analyst targets, computes ATR, sizes position, generates full plan]
```

## Example Triggers

- `"Create a trade plan for going long on MSFT"`
- `"Help me size a position in Tesla with a 1.5% risk on a $200K account"`
- `"Generate entry, stop, and targets for a QQQ swing trade"`
- `"I think AAPL breaks out — how should I structure the trade?"`
- `"Plan a short trade on XLF with proper risk management"`

## Position Sizing Formula

```
Dollar Risk    = Account Size × Max Risk %
Stop Distance  = Entry Price − Stop Loss Price  (for longs)
Shares         = Dollar Risk ÷ Stop Distance
Position Value = Shares × Entry Price
```

## API Endpoints Used

| Endpoint | Plan | Data |
|----------|------|------|
| `GET /v1/stocks/quote/{symbol}` | Pro | Live price, 52-week range, beta |
| `GET /v1/stocks/history/{symbol}?period=6mo&interval=1d` | Pro | OHLCV for ATR, S/R levels |
| `GET /v1/stocks/recommendations/{symbol}` | Pro | Analyst targets + consensus |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **Pro plan required**
- **Claude** with skill support
- User should provide: account size, max risk % per trade (default: 1–2%), direction (long/short), time horizon

## License

MIT — see [LICENSE](../LICENSE)
