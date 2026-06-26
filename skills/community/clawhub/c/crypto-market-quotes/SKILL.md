---
name: crypto-market-quotes
description: Query real-time cryptocurrency prices, market data, and trends across major exchanges (Binance, Coinbase, Kraken). Supports BTC, ETH, and major altcoins with price, 24h change, market cap, and volume data.
emoji: ₿
tags: [crypto, blockchain, market-data, trading, binance, coingecko]
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Crypto Market Quotes — 加密货币实时行情

Real-time cryptocurrency prices and market data from public APIs. No API key required for basic queries. Supports multiple exchanges and data sources.

## Supported Data Sources

| Source | Type | API Key? | Endpoint |
|:-------|:-----|:---------|:---------|
| Binance | Spot Ticker | No | `api.binance.com` |
| CoinGecko | Market Data | No | `api.coingecko.com` |
| Kraken | Ticker | No | `api.kraken.com` |

## Quick Start

### Single coin price (Binance)

```bash
curl -s "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
```

Key response fields:
- `lastPrice` — current price
- `priceChangePercent` — 24h change %
- `volume` — 24h volume (base asset)
- `quoteVolume` — 24h volume (quote asset)
- `highPrice` — 24h high
- `lowPrice` — 24h low
- `count` — number of trades

### Multiple coins

```bash
curl -s "https://api.binance.com/api/v3/ticker/24hr?symbols=[\"BTCUSDT\",\"ETHUSDT\",\"SOLUSDT\"]"
```

### Top coins by market cap (CoinGecko, no key needed)

```bash
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false"
```

Features: includes market_cap, total_volume, circulating_supply, ath (all-time high), ath_change_percentage, atl, image (icon URL)

### Kraken ticker

```bash
curl -s "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
```

## Supported Coins (Binance)

| Coin | Symbol | Common Pair |
|:-----|:-------|:------------|
| Bitcoin | BTC | BTCUSDT |
| Ethereum | ETH | ETHUSDT |
| Solana | SOL | SOLUSDT |
| XRP | XRP | XRPUSDT |
| Cardano | ADA | ADAUSDT |
| Dogecoin | DOGE | DOGEUSDT |
| Avalanche | AVAX | AVAXUSDT |
| Chainlink | LINK | LINKUSDT |
| Polkadot | DOT | DOTUSDT |
| Sui | SUI | SUIUSDT |

## Error Handling

### Binance rate limiting
```bash
# Binance allows 1200 requests per minute. On 429:
# Wait 60 seconds before retrying
sleep 60 && curl -s "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
```

### CoinGecko rate limiting
```bash
# Without API key: 30 calls/min, 50 calls/min with demo key
# On 429: wait and retry
```

## Format Output

### Single coin
```
₿ BTC/USDT 实时行情
价格: $XX,XXX.XX
24h涨跌: +X.XX% 🟢
24h高: $XX,XXX.XX
24h低: $XX,XXX.XX
24h成交量: XXX BTC ($XXX.XXM)
交易次数: XXX
```

### Top coins table
```
📊 Top 10 加密货币
币种     价格        24h       市值        7日
BTC     $XX,XXX    +X.XX% 🟢  $X.XXT    +X.XX%
ETH     $X,XXX     -X.XX% 🔴  $X.XXB    -X.XX%
SOL     $XXX       +X.XX% 🟢  $XX.XB    +X.XX%
...
```

### Market overview
```
📈 加密货币市场概况 (2026-05-22)

总市值: $X.XXT   24h成交量: $XXB
BTC支配率: XX.X%  恐惧贪婪指数: XX (贪婪)

🏆 涨幅榜
1. SOL  +8.5% 🟢   $XXX.XX
2. SUI  +5.2% 🟢   $X.XX
3. DOGE +3.1% 🟢   $0.XXX

📉 跌幅榜
1. XRP  -2.3% 🔴   $X.XX
2. ADA  -1.8% 🔴   $X.XX
```

## Use Cases
- Pre-trade price check across exchanges
- Portfolio tracking (fetch multiple tickers)
- Market sentiment analysis (gainers/losers)
- Alert threshold monitoring

## Notes
- Binance public API does NOT require authentication for ticker endpoints — fastest and most reliable
- CoinGecko API has rate limits (~30 calls/min without key)
- Prices are in USD (USDT pairs) unless specified
- For production monitoring, consider Binance WebSocket streams for real-time updates
