# technical-analyst

> Compute 12+ technical indicators (SMA/EMA, MACD, RSI, Stochastic, Bollinger Bands, ATR, OBV), identify chart patterns, map support/resistance levels, and generate a structured trade setup with entry/stop/target — powered by [Finskills API](https://finskills.net) historical OHLCV data.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro%20%2B%20Free-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-technical-analysis-blue.svg)]()

---

## What This Skill Does

1. Fetches 1-year daily + 2-year weekly OHLCV data for the requested symbol
2. Computes all standard indicators: SMA/EMA, MACD, RSI (14), Stochastic, Bollinger Bands, ATR (14), OBV
3. Performs multi-timeframe trend alignment (daily vs. weekly)
4. Maps 3 support levels and 3 resistance levels from price structure
5. Detects common chart patterns (Cup/Handle, H&S, Double Top/Bottom, Flags, Triangles)
6. Synthesizes a weighted signal scorecard (9 indicators, bull vs. bear tally)
7. Generates a full trade setup: Bias, Entry Zone, Stop-Loss (ATR-based), Target 1/2, R:R ratio

## Install

```bash
npx skills add https://github.com/finskills/technical-analyst --skill technical-analyst
```

## Quick Start

```
You: Do a technical analysis on NVDA
Claude: [Fetches 1Y daily + 2Y weekly data, computes all indicators, maps levels, outputs trade setup]
```

## Example Triggers

- `"Give me a technical analysis on AAPL"`
- `"What's the RSI and MACD on Tesla?"`
- `"Is SPY overbought right now?"`
- `"Where's the support level for MSFT?"`
- `"Is there a bullish chart pattern forming on AMD?"`
- `"Set up a trade on QQQ with entry, stop, and target"`

## Indicators Computed

| Type | Indicators |
|------|-----------|
| **Trend** | SMA 20/50/200, EMA 12/26, Golden/Death Cross |
| **Momentum** | RSI (14), MACD + Signal, Stochastic %K/%D |
| **Volatility** | Bollinger Bands (20, 2σ), ATR (14) |
| **Volume** | Volume vs. 20-day avg, On-Balance Volume (OBV) |

## API Endpoints Used

| Endpoint | Plan | Data |
|----------|------|------|
| `GET /v1/stocks/history/{symbol}?period=1y&interval=1d` | Pro | Daily OHLCV |
| `GET /v1/stocks/history/{symbol}?period=2y&interval=1wk` | Pro | Weekly OHLCV |
| `GET /v1/free/market/breadth` | Free | Macro breadth context |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **Pro plan required** for historical OHLCV data
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
