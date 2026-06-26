---
name: binance-web3
description: Query token prices, market data, K-line charts, and smart money trading signals via Binance Web3 APIs. Use when users search tokens, check prices, view market data, analyze charts, or track smart money signals on BSC/Base/Solana/Ethereum.
metadata:
  version: "1.0"
  author: moer
---

# Binance Web3 Skill

Query token data and smart money signals via Binance Web3 APIs. No API key required.

## Supported Chains

| Chain | chainId | platform |
|-------|---------|----------|
| BSC | 56 | bsc |
| Base | 8453 | base |
| Solana | CT_501 | solana |
| Ethereum | 1 | eth |

## Scripts

### 1. Token Search

Search tokens by name, symbol, or contract address.

```bash
./scripts/token-search.sh "PEPE" "56,8453"
```

### 2. Token Dynamic Data

Get real-time price, volume, holders, liquidity.

```bash
./scripts/token-dynamic.sh 56 "0x55d398326f99059ff775485246999027b3197955"
```

### 3. Token K-Line

Get candlestick data for technical analysis.

```bash
./scripts/token-kline.sh "0x55d398326f99059ff775485246999027b3197955" bsc 1h 100
```

### 4. Smart Money Signals

Get trading signals from professional investors.

```bash
./scripts/trading-signal.sh 56
./scripts/trading-signal.sh CT_501
```

## Quick Reference

| API | Endpoint | Use Case |
|-----|----------|----------|
| Token Search | `web3.binance.com/bapi/defi/v5/.../token/search` | Find tokens |
| Token Dynamic | `web3.binance.com/bapi/defi/v4/.../token/dynamic/info` | Price, volume, holders |
| K-Line | `dquery.sintral.io/u-kline/v1/k-line/candles` | Charts |
| Smart Money | `web3.binance.com/bapi/defi/v1/.../signal/smart-money` | Trading signals |

All APIs use `Accept-Encoding: identity` header. No authentication required.
