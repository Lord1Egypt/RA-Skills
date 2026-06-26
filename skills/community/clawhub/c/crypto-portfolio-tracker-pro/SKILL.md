---
name: crypto-portfolio-tracker
description: Real-time cryptocurrency portfolio tracking and analysis. Monitors multiple wallets and exchanges, calculates P&L, tracks performance metrics, and provides alerts for significant price movements. Use when users need to track crypto holdings across multiple platforms, calculate portfolio performance and ROI, monitor price changes and set alerts, generate portfolio reports, or analyze asset allocation and diversification.
---

# Crypto Portfolio Tracker

Track and analyze cryptocurrency portfolios across multiple wallets and exchanges with real-time data.

## Features

- Multi-platform portfolio aggregation (Binance, Coinbase, wallets)
- Real-time P&L calculation
- Price alerts and notifications
- Performance analytics and reports
- Asset allocation visualization

## Quick Start

### Track Portfolio

```bash
node scripts/track_portfolio.js
```

Returns current holdings, total value, and 24h change.

### Set Price Alert

```bash
node scripts/set_alert.js --symbol BTC --price 50000 --direction above
```

### Generate Report

```bash
node scripts/generate_report.js --period 7d
```

## Configuration

Portfolio sources are configured in `references/config.json`:

```json
{
  "exchanges": ["binance", "coinbase"],
  "wallets": ["0x..."],
  "alerts": {
    "telegram": true,
    "email": false
  }
}
```

## Data Sources

- CoinGecko API (free, no key required)
- Binance API (optional, for exchange balances)
- Blockchain explorers (for wallet tracking)

## Pricing

- **Free**: Basic tracking, 1 portfolio, hourly updates
- **Pro ($9.99/month)**: Unlimited portfolios, real-time updates, advanced analytics
- **Enterprise ($49.99/month)**: API access, custom alerts, priority support
