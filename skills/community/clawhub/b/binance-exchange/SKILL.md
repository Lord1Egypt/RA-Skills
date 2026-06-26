---
name: binance-exchange
description: Query Binance spot exchange data: real-time prices, 24h change, K-line charts, and market data. Use when users want to check crypto prices, trading volume, or market trends on Binance. Requires proxy (http://127.0.0.1:1082).
metadata:
  version: "1.1"
  author: moer
---

# Binance Exchange Skill

Query Binance spot exchange data via API. Requires proxy for network access.

## Prerequisites

**Proxy Configuration:**
```bash
# Uses system proxy
export HTTP_PROXY="http://127.0.0.1:1082"
export HTTPS_PROXY="http://127.0.0.1:1082"
```

**Note:** Binance API may be restricted in certain regions. Use a proxy node in allowed regions (HK/SG/JP/UK/DE).

## API Endpoints

| Endpoint | Use Case |
|----------|----------|
| `/api/v3/ticker/price` | Real-time prices |
| `/api/v3/ticker/24hr` | 24h statistics |
| `/api/v3/klines` | K-line/candlestick data |
| `/api/v3/exchangeInfo` | Trading rules & symbols |

## Scripts

### 1. Price Query

```bash
# Single symbol
./scripts/price.sh BTCUSDT

# Multiple symbols
./scripts/price.sh BTCUSDT ETHUSDT BNBUSDT
```

### 2. 24h Change (via K-lines)

```bash
# Single symbol
./scripts/change.sh BTCUSDT

# Top gainers (requires custom processing)
./scripts/gainers.sh
```

### 3. K-Line Data

```bash
# BTC 1hour K-line (100 candles)
./scripts/kline.sh BTCUSDT 1h 100

# ETH 4hour K-line
./scripts/kline.sh ETHUSDT 4h 50
```

### 4. Token Info (New!)

```bash
# Get basic price
./scripts/token-info.sh BTCUSDT

# Get 24h statistics
./scripts/token-info.sh BTCUSDT stats
```

**Returns:**
- Symbol, price, 24h change, change %, 24h high/low, volume, quote volume

### 5. Search Symbols

```bash
# Search USDT pairs
./scripts/search.sh USDT
```

## Quick Reference

| Data | Command |
|------|---------|
| BTC price | `./scripts/price.sh BTCUSDT` |
| 24h stats | `./scripts/token-info.sh BTCUSDT stats` |
| K-line | `./scripts/kline.sh BTCUSDT 1h 100` |

## Rate Limits

- 1200 requests/minute (public endpoints)
- Use caching for frequent queries
