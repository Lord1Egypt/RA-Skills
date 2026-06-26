---
name: crypto-price-alert
version: 1.0.0
description: Real-time cryptocurrency price alerts and monitoring. Track Bitcoin, Ethereum, and 100+ coins with custom price alerts delivered to your Telegram, Discord, or Email.
tags: crypto, trading, alerts, bitcoin, ethereum, finance, monitoring
license: MIT
---

# Crypto Price Alert

> Never miss a price movement. Real-time crypto alerts delivered to your favorite channels.

## Features

- **Real-time price tracking**: Monitor 100+ cryptocurrencies
- **Custom alerts**: Set price targets (above/below)
- **Multi-channel delivery**: Telegram, Discord, Email, Slack
- **Scheduled reports**: Daily/weekly price summaries
- **Portfolio tracking**: Monitor your holdings
- **Technical indicators**: RSI, MACD, Moving Averages

## Supported Coins

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- Binance Coin (BNB)
- Cardano (ADA)
- 100+ more via CoinGecko API

## Usage

### Set Price Alert

```
"Alert me when BTC goes above $70,000"
"Notify me if ETH drops below $3,500"
"Send me a daily crypto price report at 9am"
```

### Portfolio Tracking

```
"Track my portfolio: 0.5 BTC, 10 ETH, 100 SOL"
"Show me my portfolio value"
"What's my profit/loss today?"
```

### Technical Analysis

```
"What's the RSI for Bitcoin?"
"Is ETH in oversold territory?"
"Show me BTC's 7-day moving average"
```

## Configuration

```json
{
  "alerts": [
    {
      "coin": "bitcoin",
      "target_price": 70000,
      "condition": "above",
      "channels": ["telegram", "email"]
    }
  ],
  "portfolio": [
    {"coin": "bitcoin", "amount": 0.5},
    {"coin": "ethereum", "amount": 10}
  ],
  "report_schedule": "0 9 * * *"
}
```

## Delivery Channels

| Channel | Setup |
|---------|-------|
| Telegram | Provide bot token and chat ID |
| Discord | Set up webhook URL |
| Email | Configure SMTP settings |
| Slack | Add webhook URL |

## Pricing for Custom Setup

| Service | Price |
|---------|-------|
| Basic Setup (1 alert) | $50 |
| Pro Setup (10 alerts + reports) | $150 |
| Portfolio Tracking | $100/year |
| Enterprise (API integration) | $500+ |

## Data Sources

- CoinGecko API (free tier)
- CoinMarketCap API (requires key)
- Binance API (real-time)

## Requirements

- OpenClaw with cron enabled
- Optional: Telegram/Discord bot setup

## Perfect For

- Crypto traders
- HODLers
- DeFi enthusiasts
- Investment firms
- Anyone who wants to track crypto

---

*Version: 1.0.0*
*Author: OpenClaw Community*