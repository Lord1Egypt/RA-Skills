---
name: Crypto Airdrop Hunter & Market Reporter
description: Automated crypto airdrop discovery and daily market analysis. Finds high-funding projects, tracks market structure, support/resistance, and macro news. No API keys required. Self-contained — no external dependencies.
---

# Crypto Airdrop Hunter & Market Reporter

v1.0.1 - Fixed: Removed external skill dependencies, self-contained state management.

Fully automated skill for crypto traders who want daily market reports and airdrop alerts without manually checking every day.

## What This Skill Does

### 📊 Daily Market Report
- BTC/ETH price action & candle analysis
- Support & Resistance levels
- Trend detection (bullish/bearish/range)
- BTC Dominance & altcoin season signals
- Macro news with bullish/bearish labels

### 🎁 Airdrop Discovery
- Finds projects with big funding ($5M+) from top VCs
- Tracks projects that haven't launched tokens yet
- Monitors testnet activity & engagement opportunities
- Filters overhyped projects

### 🚨 Smart Monitoring
- Checks S/R proximity (alerts when within 2%)
- Tracks altcoin volatility (configurable thresholds)
- Monitors macro news events

## Installation

```bash
# Clone or download this skill to your workspace
# No API keys needed - uses free CoinGecko API

# Run manually:
node scripts/market_daily_report.js
node scripts/generate_airdrop_report.js --period=weekly
node scripts/heartbeat_check.js
```

## Configuration

Edit `config.json` to customize:

```json
{
  "airdrop": {
    "minFunding": 5000000,
    "vcs": ["a16z", "Paradigm", "Sequoia", "Binance Labs", "Polychain"],
    "chains": ["ethereum", "solana", "polygon", "arbitrum", "optimism"],
    "preferredHypeLevel": ["low", "low-moderate", "moderate"]
  },
  "market": {
    "watchCrypto": ["bitcoin", "ethereum"],
    "altcoinPicks": ["hype", "mnt", "sol", "arb"]
  },
  "schedule": {
    "marketDaily": "0 0 * * *",
    "airdropWeekly": "0 0 * * 1,4"
  }
}
```

## Setup with OpenClaw Cron

Add to your OpenClaw for automated reports. No external skills required:

```json
// Daily market report (7am your timezone)
{
  "schedule": { "kind": "cron", "expr": "0 0 * * *" },
  "payload": { 
    "kind": "agentTurn",
    "message": "cd /path/to/crypto-airdrop-hunter && node scripts/market_daily_report.js"
  }
}

// Airdrop report (Mon & Thu)
{
  "schedule": { "kind": "cron", "expr": "0 0 * * 1,4" },
  "payload": {
    "kind": "agentTurn", 
    "message": "cd /path/to/crypto-airdrop-hunter && node scripts/generate_airdrop_report.js --period=weekly"
  }
}
```

State is stored in `state.json` within the skill folder (not external).

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `market_daily_report.js` | Daily market analysis | `node scripts/market_daily_report.js` |
| `generate_airdrop_report.js` | Airdrop discovery | `node scripts/generate_airdrop_report.js --period=weekly` |
| `heartbeat_check.js` | Quick monitoring | `node scripts/heartbeat_check.js` |

## Data Sources

- **Market Data**: CoinGecko API (free tier)
- **Airdrop Data**: Manual tracking + DefiLlama
- **No API keys required**

## Output Examples

### Market Report
```
📊 Daily Market Report - Selasa, 24 Maret 2026

BTC Price Action (24h)
💰 Current: $70,929 (+3.56%)
📈 Market Cap: $1.42T

Candlestick (24h Close)
🟢 Moderate bullish

Support & Resistance
🔴 Support: $84,800
🟢 Resistance: $88,000
📍 Midpoint: $86,400

Trend: Bullish bias
Summary: ✅ Bullish environment. Pullback ke support = buying opportunity.
```

### Airdrop Report
```
📋 Laporan Airdrop - Weekly

1. Monad (L1 Blockchain)
   💰 Funding: $225M Series B
   🏦 Investor: Paradigm, a16z Crypto
   ⛓️ Chain: Solana ecosystem
   📊 Status: Private testnet, public launch Q3 2026
   📈 Hype: moderate
```

## Requirements

- Node.js 18+
- Internet connection
- OpenClaw (optional, for automation)

## License

MIT

## Author

Built with OpenClaw