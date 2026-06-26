# Trading Knowledge Base

> Beta's accumulated trading research.

## Core Skills Available

| Skill | Path | Description |
|-------|------|-------------|
| `trading-bot-framework` | skills/trading-bot-framework | Build automated trading bots |
| `ta-quant-pipeline` | skills/ta-quant-pipeline | Technical analysis signal pipeline |
| `signal-alert-system` | skills/signal-alert-system | Real-time trading alerts |
| `spx-analysis` | skills/spx-analysis | SPX/market direction analysis |
| `options-chains` | skills/options-chains | Options chain analysis |
| `portfolio-monitor` | skills/portfolio-monitor | Portfolio tracking |
| `risk-management` | skills/risk-management | Position sizing, drawdown protection |
| `backtester` | skills/backtester | Strategy backtesting |

## Trading Gig Services Offered

1. **Pre-Market Trading Plan** — SPX key levels, direction bias, entry/exit zones
2. **Quantitative Trading Research** — Backtest any strategy, discover alpha
3. **Options Trading Strategy Analysis** — Greeks decomposition, optimal setups
4. **AI Trading Bot Development** — Pine Script, Python, TradingView automation
5. **Risk Management System** — Position sizing, drawdown protection
6. **Portfolio Analysis & Rebalancing** — Allocation optimization
7. **TradingView Indicator Development** — Custom Pinescript

## Market Analysis Framework

### Pre-Market Checklist

1. **SPX/ES futures** — direction and overnight gap
2. **VIX** — fear gauge, above 20 = caution
3. **Sector rotation** — who's leading/lagging
4. **Options flow** — unusual call/put activity
5. **Economic data** — calendar events
6. **Support/Resistance** — key levels from previous session

### Technical Indicators Used

- SMA 20/50/200 (trend)
- RSI (momentum, overbought >70, oversold <30)
- MACD (trend momentum)
- Bollinger Bands (volatility)
- Volume profile
- VWAP

## Key Trading Rules

1. **Never risk more than 1-2% per trade**
2. **Always have an exit plan before entry**
3. **Trend is your friend** — trade with trend
4. **Cut losses quickly, let winners run**
5. **Respect the daily chart direction**
6. **Pre-market determines the day's bias**

## Platforms & Tools

- **TradingView** — Charting, Pine Script
- **Tiger API** — Market data
- **Alpaca** — Brokerage for paper/live trading
- **CCXT** — Crypto exchange aggregation

## Research Findings

### CoinMarketCap Data (from previous research)

- CMC API is free for basic data
- Good for: price, market cap, volume, OHLCV
- Rate limit: ~10-30 requests/minute
- Python library: `python-coinmarketcap`

### Trading Bot Architecture

```
Data Feed → Signal Generation → Risk Check → Order Execution → Portfolio Management
    ↓              ↓                  ↓              ↓              ↓
 CCXT/Tiger   TA indicators    Position sizing   Exchange API    P&L tracking
```

## Market Research Topics Done

- [x] SPX futures and market bias
- [x] Options flow analysis basics
- [x] Risk management frameworks
- [x] Backtesting methodology
- [x] MEV and DeFi trading opportunities
- [x] Sentiment analysis sources
