---
name: crypto-whale-alerts
description: |
  Real-time cryptocurrency whale tracker for AI agents and crypto traders.
  Monitors large on-chain transactions on Bitcoin, Ethereum, and major altcoins,
  tracks known whale wallets (exchanges, institutions, smart money), detects
  accumulation/distribution patterns, and generates actionable alerts.

  Commands:
  - whale_alerts.py scan       Scan for whale transactions above threshold
  - whale_alerts.py summary   Get whale activity summary
  - whale_alerts.py watch     List tracked whale wallet addresses
  - whale_alerts.py set-threshold <usd>  Set minimum USD threshold

  Environment: WHALE_MIN_USD (default 100000), WHALE_COOLDOWN (default 60 min).
  Python 3.9+, zero external dependencies. Uses mock data structure that
  maps to real Etherscan/Blockchair API responses in production.

  Whale classification: INFLOW (exchange receiving, potential selling pressure)
  vs OUTFLOW (cold storage, accumulation signal). Watchlist includes Binance,
  Coinbase, Grayscale, and notable smart money addresses.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash, Read
---

# Crypto Whale Alerts

Tracks large on-chain transactions and whale wallet movements to generate actionable crypto trading alerts.

## Configuration

```bash
# Set minimum transaction threshold in USD
export WHALE_MIN_USD=500000

# Set alert cooldown period in minutes
export WHALE_COOLDOWN=30
```

## Commands

```bash
# Scan for whale transactions above threshold
python scripts/whale_alerts.py scan

# Get whale activity summary
python scripts/whale_alerts.py summary

# View tracked whale wallet addresses
python scripts/whale_alerts.py watch

# Change minimum threshold
python scripts/whale_alerts.py set-threshold 250000
```

## Alert Interpretation

- **INFLOW** (green): Large transaction into exchange hot wallet
  - Could indicate imminent selling pressure
  - Watch for distribution patterns

- **OUTFLOW** (red): Large transaction from exchange to cold storage
  - Could indicate accumulation phase
  - Often precedes price increases

## Watchlist

Includes major exchange hot wallets, institutional custodians, and notable smart money addresses:
- Binance Hot (multiple wallets)
- Coinbase Custody
- Grayscale Trust wallets
- DeFi protocol treasuries

## Production Integration

For live data, connect to:
- Etherscan API for Ethereum transactions
- Blockchair API for multi-chain coverage
- Glassnode for whale wallet labels

The script uses mock data with real field structure for easy API integration.