---
name: trading-signals
description: Generate trading signals for stocks, indices, crypto, and commodities using TradingView data. Use when user asks for trading signals, technical analysis, buy/sell recommendations, market indicators (RSI, MACD, SMA), or automated market monitoring. Supports real-time data from TradingView and CoinGecko.
---

# Trading Signals

Generate technical trading signals using TradingView real-time data.

## Capabilities

- **Technical Indicators**: RSI, SMA (20/50), MACD, Bollinger Bands
- **Signal Generation**: Buy/Sell signals based on indicator combinations
- **Asset Coverage**: Indices, stocks, crypto, commodities, forex
- **Timeframes**: 15m, 60m, 240m, 1D
- **Alerting**: Email notifications for strong signals

## Quick Start

```bash
# Analyze default assets
node scripts/analyze.js

# Analyze specific asset
node scripts/analyze.js --symbol BINANCE:BTCUSDT --name Bitcoin

# Continuous monitoring (15min intervals)
node scripts/monitor.js --interval 15
```

## Signal Types

| Signal | Indicator | Strength |
|--------|-----------|----------|
| 🟢 BUY | RSI < 30 (oversold) | Strong |
| 🟢 BUY | Golden Cross (SMA20 > SMA50) | Medium |
| 🟢 BUY | Price near SMA20 bounce | Weak |
| 🔴 SELL | RSI > 70 (overbought) | Strong |
| 🔴 SELL | Death Cross (SMA20 < SMA50) | Medium |
| 🔴 SELL | Price below SMA20 resistance | Weak |

## Configuration

Edit `references/assets.json` to customize monitored assets:

```json
{
  "assets": [
    { "symbol": "XETR:DAX", "name": "DAX", "category": "Index", "timeframe": "60" },
    { "symbol": "BINANCE:BTCUSDT", "name": "Bitcoin", "category": "Crypto", "timeframe": "60" }
  ],
  "alerts": {
    "email": "ai.escher.bot@gmail.com",
    "minStrength": "medium",
    "rsiThresholds": { "oversold": 30, "overbought": 70 }
  }
}
```

## Scripts

- `scripts/analyze.js` - Single analysis run
- `scripts/monitor.js` - Continuous monitoring with alerts
- `scripts/lib/tradingview.js` - TradingView API wrapper
- `scripts/lib/indicators.js` - Technical indicator calculations
- `scripts/lib/email.js` - Email alert sender

## Dependencies

- `@mathieuc/tradingview` - TradingView WebSocket API
- Node.js built-in `https` for CoinGecko API
