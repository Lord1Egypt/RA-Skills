---
name: crypto-market-intel
description: Crypto Market Intelligence - Free market data pipeline for any OpenClaw agent. Zero API keys needed. Fetch real-time crypto prices, market metrics, Fear & Greed index, DeFi TVL, stock indices, and macro indicators. Use when you need crypto prices, market data, market analysis, fear and greed, DeFi TVL, stock prices, macro data, market intelligence, or trading signals.
---

# Crypto Market Intelligence

Real-time market data pipeline for crypto, stocks, and macro indicators. Zero API keys required. All data fetched from free public APIs.

## When to Use

Trigger this skill when you need:
- Current cryptocurrency prices and market caps
- Bitcoin/Ethereum dominance
- Fear & Greed Index
- Trending coins
- DeFi Total Value Locked (TVL)
- Stock market indices (S&P 500, Nasdaq, Dow, VIX)
- AI stock prices (NVDA, AMD, MSFT, etc.)
- Macro indicators (DXY dollar index, 10Y Treasury yield)
- Pre-fetched data for trading analysis
- Market intelligence for portfolio decisions

## Quick Start

Fetch all market data:

```bash
cd ~/.openclaw/skills/crypto-market-intel/scripts
python3 market-data-fetcher.py all --output ~/market-data
```

Analyze market conditions:

```bash
./analyze-market.sh
```

## Core Features

✅ **6 Free APIs, Zero Keys**
- CoinGecko (coins, global metrics, trending)
- Alternative.me (Fear & Greed Index)
- DeFi Llama (DeFi TVL)
- Yahoo Finance (stocks, indices, bonds)

✅ **Crypto Coverage**
- Top 30 coins by market cap
- Global market metrics (total mcap, volume, dominance)
- Fear & Greed Index (current + 7-day history)
- Trending coins
- DeFi Total Value Locked

✅ **Stocks & Macro**
- Major indices (S&P 500, Nasdaq, Dow, VIX)
- AI stocks (NVDA, AMD, AVGO, MRVL, TSM, ASML, ARM, MSFT, AMZN, GOOG, META, ORCL)
- AI energy (VST, CEG, OKLO, SMR, TLN)
- AI infrastructure (VRT, ANET, CRDO)
- Dollar Index (DXY)
- 10-Year Treasury Yield

✅ **Agent-Ready Output**
- JSON format for easy parsing
- Structured data with timestamps
- Works as cron job or on-demand
- No hallucinated prices — real market data

## Usage

### Fetch Crypto Data Only

```bash
python3 scripts/market-data-fetcher.py crypto --output ./data
```

Output: `data/crypto-latest.json`

### Fetch Stocks/Macro Only

```bash
python3 scripts/market-data-fetcher.py stocks --output ./data
```

Output: `data/stocks-latest.json`

### Fetch Everything

```bash
python3 scripts/market-data-fetcher.py all --output ./data
```

### Automated Analysis

Run the analyzer wrapper to fetch data and generate a market summary prompt:

```bash
./scripts/analyze-market.sh ~/market-data
```

This fetches fresh data and outputs a structured prompt for the agent to analyze:
- Market sentiment (Fear & Greed)
- Top movers (biggest gains/losses)
- Macro environment (DXY, yields, VIX)
- Notable signals

## Cron Integration

Schedule hourly market data fetches:

```bash
crontab -e

# Fetch market data every hour
0 * * * * cd ~/.openclaw/skills/crypto-market-intel/scripts && python3 market-data-fetcher.py all --output ~/market-data
```

The agent can then read pre-fetched data for instant analysis without waiting for API calls.

## Data Schema

### Crypto Output (`crypto-latest.json`)

```json
{
  "fetched_at": "2026-03-13T15:45:00Z",
  "source": "coingecko+alternative.me",
  "top_coins": [
    {
      "symbol": "BTC",
      "name": "Bitcoin",
      "price": 68500.0,
      "market_cap": 1340000000000,
      "volume_24h": 28000000000,
      "change_24h_pct": 2.5,
      "change_7d_pct": -1.2,
      "change_1h_pct": 0.3,
      "ath": 69000.0,
      "ath_change_pct": -0.7,
      "rank": 1
    }
  ],
  "global": {
    "total_market_cap_usd": 2400000000000,
    "total_volume_24h_usd": 85000000000,
    "btc_dominance": 55.8,
    "eth_dominance": 17.2,
    "active_cryptocurrencies": 13245,
    "market_cap_change_24h_pct": 1.8
  },
  "fear_greed": [
    {
      "value": 62,
      "label": "Greed",
      "date": "1710346800"
    }
  ],
  "trending": [
    {
      "name": "Solana",
      "symbol": "SOL",
      "rank": 5,
      "score": 0
    }
  ],
  "defi_tvl": {
    "total_tvl": 95800000000,
    "date": 1710288000,
    "change_1d": 2.1
  }
}
```

### Stocks Output (`stocks-latest.json`)

```json
{
  "fetched_at": "2026-03-13T15:45:00Z",
  "stocks": {
    "indices": [
      {
        "symbol": "^GSPC",
        "price": 5200.5,
        "prev_close": 5180.0,
        "change_pct": 0.4
      }
    ],
    "ai_chips": [
      {
        "symbol": "NVDA",
        "price": 890.25,
        "prev_close": 885.0,
        "change_pct": 0.59
      }
    ]
  },
  "dxy": {
    "price": 103.45,
    "prev_close": 103.2
  },
  "treasury_10y": {
    "yield": 4.25,
    "prev_close": 4.22
  }
}
```

## Rate Limits & Fair Use

| API | Rate Limit | Notes |
|-----|------------|-------|
| CoinGecko | 10-50 calls/min | Free tier, no key required |
| Alternative.me | Unlimited | Public endpoint |
| DeFi Llama | Unlimited | Public endpoint |
| Yahoo Finance | ~2000 calls/hour | Unofficial API, use responsibly |

**Recommendation:** Run fetcher hourly, not more frequently. APIs are free but fair use matters.

## Troubleshooting

**Problem:** Fetch fails with timeout

**Solution:** Check network connection, try again in a few minutes. Some APIs have temporary outages.

---

**Problem:** Yahoo Finance returns no data for a stock

**Solution:** Symbol may be delisted or unavailable. Check symbol accuracy (use `^` prefix for indices, e.g., `^GSPC`).

---

**Problem:** DeFi TVL is null

**Solution:** DeFi Llama API may be updating. Historical data endpoint occasionally has lag. Try again later.

---

**Problem:** Fear & Greed returns empty

**Solution:** Alternative.me may be down. Check https://alternative.me/crypto/fear-and-greed-index/ directly.

## Architecture Notes

- **No authentication** — all APIs are public, no keys to manage
- **HTTP requests only** — uses Python's built-in `urllib` (no external deps)
- **Error tolerant** — if one API fails, others still succeed
- **Portable** — works on any system with Python 3.7+
- **Configurable output** — use `--output` flag to set data directory

## Integration Examples

### Discord Bot Alert

```bash
#!/bin/bash
python3 scripts/market-data-fetcher.py crypto --output /tmp
FEAR=$(jq '.fear_greed[0].value' /tmp/crypto-latest.json)
if [ "$FEAR" -lt 25 ]; then
  echo "🚨 Extreme Fear detected: $FEAR — potential buy opportunity"
fi
```

### Trading Bot Pre-Analysis

```python
import json

# Load pre-fetched data
with open("~/market-data/crypto-latest.json") as f:
    data = json.load(f)

# Extract top movers
top_coins = data["top_coins"]
gainers = sorted(top_coins, key=lambda x: x["change_24h_pct"], reverse=True)[:5]

print("Top 5 Gainers (24h):")
for coin in gainers:
    print(f"{coin['symbol']}: +{coin['change_24h_pct']:.2f}%")
```

## References

See `references/api-sources.md` for detailed API documentation, endpoints, response schemas, and rate limit specifics.

---

**Last Updated:** 2026-03-13
