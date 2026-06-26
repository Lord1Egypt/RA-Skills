---
name: cryptoprice
description: Query real-time cryptocurrency prices using the Binance API. Get latest prices for Bitcoin, Ethereum, and all BN listed cryptocurrencies. No API key required.
---

# CryptoPrice - Cryptocurrency Price Query

Query real-time cryptocurrency prices using the official Binance API.

## Quick Start

### Query Popular Coin Prices

```bash
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py
```

### Query Specific Coin

```bash
# Query Bitcoin
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py BTCUSDT

# Query Ethereum
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py ETHUSDT

# Shorthand (auto-completes USDT)
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py BTC
```

### JSON Format Output

```bash
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py --json
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py BTC --json
```

### List All Trading Pairs

```bash
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py --list
```

## Supported Coins

Popular coins displayed by default:
- **BTC** - Bitcoin
- **ETH** - Ethereum
- **BNB** - Binance Coin
- **SOL** - Solana
- **XRP** - Ripple
- **DOGE** - Dogecoin
- **ADA** - Cardano
- **AVAX** - Avalanche
- **DOT** - Polkadot
- **LINK** - Chainlink

## API Data Source

- **Binance Spot API**: `https://api.binance.com/api/v3/ticker/price`
- No API Key required
- Real-time data with low latency
