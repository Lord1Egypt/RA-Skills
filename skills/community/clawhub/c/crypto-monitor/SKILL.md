---
name: crypto-monitor
description: "Cryptocurrency market monitoring with real-time prices, on-chain data, whale tracking, and alerting. Trigger on: crypto, BTC, ETH, 加密货币, 比特币, 以太坊, 行情, 价格, whale, 巨鲸, 链上数据, 空投, airdrop, 代币, token price."
version: 1.0.0
license: MIT
---

# Crypto Monitor 🪙

Real-time cryptocurrency monitoring skill for OpenClaw. Tracks prices, on-chain movements, whale activity, and sends alerts.

## What it does

- **Real-time price tracking**: BTC, ETH, and top 100 tokens via CoinGecko API
- **Whale alerts**: Monitors large on-chain transfers on Ethereum and Bitcoin
- **Trending tokens**: Discovers hot/trending tokens on DEXes
- **Portfolio tracking**: Track your holdings and P&L
- **Custom alerts**: Price thresholds, volume spikes, whale movements
- **Airdrop radar**: Upcoming and active airdrop opportunities

## Trigger Conditions

Activate when user asks about:
- Cryptocurrency prices (BTC, ETH, etc.)
- Market trends, volume, or volatility
- Whale transactions or large transfers
- Airdrop hunting or claiming
- Exchange rates and conversions
- DeFi protocol information
- Token discovery and research

## Prerequisites

- `curl`, `jq` (auto-installed if missing)
- Internet access

## Installation

```
clawhub install clawto/crypto-monitor
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/price.sh` | Fetch real-time prices |
| `scripts/whale.sh` | Track large transactions |
| `scripts/trending.sh` | Discover trending tokens |
| `scripts/portfolio.sh` | Track portfolio value |
| `scripts/airdrop.sh` | Find active airdrops |

## Usage

```
# Check BTC price
Price: $87,432 (+2.3% 24h) | Vol: $28.5B | Market Cap: $1.72T

# Check whale activity
🐋 Whale Alert: 2,847 BTC ($248M) moved from Binance to unknown wallet
🐋 Whale Alert: 15,000 ETH ($48.3M) deposited to Coinbase

# Trending tokens (24h)
🔥 WIF: +45.2% | $2.87 | Vol: $890M
🔥 BONK: +32.1% | $0.000042 | Vol: $345M
```

## 🫶 Donation

If this skill helps you profit, consider donating:

- **BTC**: `bc1pdah8vmmuctw3cxz0lsryh5rpzqn8jv546jma3auxpgxeqplrd32s4m68cs`

## Testing

```
./test/run.sh
```

## License

MIT
