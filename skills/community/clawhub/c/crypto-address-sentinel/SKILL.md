---
name: crypto-address-sentinel
description: Monitor wallet balances and on-chain activity. Get alerts when balances change or when specified conditions are met. Use for tracking portfolio, detecting unusual activity, or monitoring airdrop eligibility across multiple chains.
version: 1.0.0
tags:
  - crypto
  - wallet
  - monitoring
  - alert
  - portfolio
---

# Crypto Address Sentinel

Monitor wallet addresses across multiple blockchains and get notified of important events.

## Setup

### Environment Variables
- `WATCHED_ADDRESSES` - Comma-separated list of addresses to monitor
- `ALERT_WEBHOOK` - Webhook URL for alerts (optional)
- `CHECK_INTERVAL_MINUTES` - How often to check (default: 60)

## Usage

```
# Check all watched addresses
 addresses

# Get balance for specific address
balance <address>

# Add address to watchlist
add <address>

# Remove from watchlist
remove <address>
```

## Supported Chains
- Ethereum
- Arbitrum
- Optimism
- Base
- Polygon
- BNB Chain
- Solana

## Features
- Balance monitoring
- Activity detection
- Custom alert conditions
- Multi-chain support
- Periodic reports
