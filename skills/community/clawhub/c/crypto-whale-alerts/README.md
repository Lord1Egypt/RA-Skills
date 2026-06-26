# Crypto Whale Alerts Skill

Real-time cryptocurrency whale activity tracker that monitors large on-chain transactions and wallet movements to generate actionable trading alerts.

## Features

- **Large Transaction Detection** - Tracks transactions above configurable USD threshold
- **Whale Wallet Monitoring** - Watchlist of known whale and institutional addresses
- **Accumulation/Distribution Detection** - Identifies when whales are buying or selling
- **Multi-Chain Support** - Works with Ethereum, Bitcoin, and major L2s
- **Configurable Alerts** - Set minimum thresholds and cooldown periods
- **Python 3.9+ Compatible** - Zero external dependencies

## Setup

```bash
# Configure minimum threshold (default: $100k)
export WHALE_MIN_USD=500000

# Configure alert cooldown in minutes (default: 60)
export WHALE_COOLDOWN=30

# Run scans
python scripts/whale_alerts.py scan        # Scan for whale transactions
python scripts/whale_alerts.py summary      # Get whale activity summary
python scripts/whale_alerts.py watch        # List watched whale wallets
python scripts/whale_alerts.py set-threshold 250000
```

## Use Cases

- Catch early signals of price movements from institutional wallets
- Identify accumulation patterns before breakouts
- Monitor exchange outflows/inflows for market signals
- Generate trading alerts from on-chain whale activity
- Track DeFi protocol movements and smart money flows