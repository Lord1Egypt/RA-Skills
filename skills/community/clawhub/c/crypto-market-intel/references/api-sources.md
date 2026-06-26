# Market Data API Sources

Comprehensive reference for all free APIs used by the crypto-market-intel skill.

## API Overview

| API | Purpose | Auth Required | Rate Limit | Reliability |
|-----|---------|--------------|------------|-------------|
| CoinGecko | Crypto prices, market cap, global metrics | No | 10-50 calls/min | ⭐⭐⭐⭐⭐ |
| Alternative.me | Fear & Greed Index | No | Unlimited | ⭐⭐⭐⭐ |
| DeFi Llama | DeFi Total Value Locked | No | Unlimited | ⭐⭐⭐⭐⭐ |
| Yahoo Finance | Stock prices, indices, bonds | No | ~2000 calls/hour | ⭐⭐⭐⭐ |

## 1. CoinGecko API

**Base URL:** `https://api.coingecko.com/api/v3`

**Free Tier:** 10-50 calls/minute (varies by endpoint)

### Endpoints Used

#### Markets Endpoint
```
GET /coins/markets
```

**Parameters:**
- `vs_currency=usd` — Price currency
- `order=market_cap_desc` — Sort by market cap
- `per_page=30` — Number of coins to return
- `page=1` — Pagination
- `sparkline=false` — Exclude sparkline data
- `price_change_percentage=1h,24h,7d` — Include price change metrics

**Response Fields (used):**
- `symbol` — Ticker symbol
- `name` — Coin name
- `current_price` — Current price in USD
- `market_cap` — Total market capitalization
- `total_volume` — 24h trading volume
- `price_change_percentage_24h` — 24h price change %
- `price_change_percentage_7d_in_currency` — 7d price change %
- `price_change_percentage_1h_in_currency` — 1h price change %
- `ath` — All-time high price
- `ath_change_percentage` — % below ATH
- `market_cap_rank` — Market cap rank

**Example Request:**
```bash
curl "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1&sparkline=false&price_change_percentage=1h,24h,7d"
```

#### Global Market Data
```
GET /global
```

**Response Fields (used):**
- `data.total_market_cap.usd` — Total crypto market cap
- `data.total_volume.usd` — 24h trading volume
- `data.market_cap_percentage.btc` — Bitcoin dominance %
- `data.market_cap_percentage.eth` — Ethereum dominance %
- `data.active_cryptocurrencies` — Number of active coins
- `data.market_cap_change_percentage_24h_usd` — 24h market cap change %

**Example Request:**
```bash
curl "https://api.coingecko.com/api/v3/global"
```

#### Trending Coins
```
GET /search/trending
```

**Response Fields (used):**
- `coins[].item.name` — Coin name
- `coins[].item.symbol` — Ticker symbol
- `coins[].item.market_cap_rank` — Market cap rank
- `coins[].item.score` — Trending score

**Example Request:**
```bash
curl "https://api.coingecko.com/api/v3/search/trending"
```

### Rate Limits

- **Free tier:** 10-50 calls/minute (not strictly enforced)
- **Recommended:** 1 call per endpoint per minute
- **Error handling:** 429 status code on rate limit exceeded
- **Retry strategy:** Wait 60 seconds and retry

### Documentation

Official docs: https://www.coingecko.com/en/api/documentation

---

## 2. Alternative.me Fear & Greed Index

**Base URL:** `https://api.alternative.me`

**Free Tier:** Unlimited (public endpoint)

### Endpoint

```
GET /fng/?limit=7
```

**Parameters:**
- `limit=7` — Return last 7 days of data

**Response Schema:**
```json
{
  "name": "Fear and Greed Index",
  "data": [
    {
      "value": "62",
      "value_classification": "Greed",
      "timestamp": "1710346800",
      "time_until_update": "43200"
    }
  ]
}
```

**Response Fields (used):**
- `data[].value` — Index value (0-100)
- `data[].value_classification` — Label (Extreme Fear, Fear, Neutral, Greed, Extreme Greed)
- `data[].timestamp` — Unix timestamp

**Example Request:**
```bash
curl "https://api.alternative.me/fng/?limit=7"
```

### Classification Ranges

| Value | Label |
|-------|-------|
| 0-24 | Extreme Fear |
| 25-49 | Fear |
| 50-74 | Greed |
| 75-100 | Extreme Greed |

### Rate Limits

No strict rate limits. Public endpoint, use responsibly.

### Documentation

Web interface: https://alternative.me/crypto/fear-and-greed-index/

---

## 3. DeFi Llama API

**Base URL:** `https://api.llama.fi`

**Free Tier:** Unlimited (public API)

### Endpoint

```
GET /v2/historicalChainTvl
```

Returns historical Total Value Locked across all chains.

**Response Schema:**
```json
[
  {
    "date": 1710288000,
    "tvl": 95800000000
  }
]
```

**Response Fields (used):**
- `tvl` — Total Value Locked in USD
- `date` — Unix timestamp

**Example Request:**
```bash
curl "https://api.llama.fi/v2/historicalChainTvl"
```

### Rate Limits

No strict rate limits. Public API, designed for open access.

### Documentation

Official docs: https://defillama.com/docs/api

---

## 4. Yahoo Finance API (Unofficial)

**Base URL:** `https://query1.finance.yahoo.com`

**Free Tier:** ~2000 calls/hour (soft limit)

**Note:** This is an unofficial API. Yahoo does not officially support programmatic access, but this endpoint is publicly available and widely used.

### Endpoint

```
GET /v8/finance/chart/{symbol}
```

**Parameters:**
- `interval=1d` — Daily data
- `range=5d` — Last 5 days

**Symbols Used:**

**Indices:**
- `^GSPC` — S&P 500
- `^IXIC` — Nasdaq Composite
- `^DJI` — Dow Jones Industrial Average
- `^VIX` — CBOE Volatility Index

**AI Stocks:**
- Chips: `NVDA`, `AMD`, `AVGO`, `MRVL`, `TSM`, `ASML`, `ARM`
- Cloud: `MSFT`, `AMZN`, `GOOG`, `META`, `ORCL`
- Energy: `VST`, `CEG`, `OKLO`, `SMR`, `TLN`
- Infrastructure: `VRT`, `ANET`, `CRDO`

**Macro:**
- `DX-Y.NYB` — US Dollar Index (DXY)
- `^TNX` — 10-Year Treasury Yield

**Response Schema:**
```json
{
  "chart": {
    "result": [
      {
        "meta": {
          "regularMarketPrice": 5200.5,
          "previousClose": 5180.0,
          "currency": "USD"
        }
      }
    ]
  }
}
```

**Response Fields (used):**
- `chart.result[0].meta.regularMarketPrice` — Current price
- `chart.result[0].meta.previousClose` — Previous close
- `chart.result[0].meta.currency` — Currency (USD, etc.)

**Example Request:**
```bash
curl "https://query1.finance.yahoo.com/v8/finance/chart/NVDA?interval=1d&range=5d"
```

### Rate Limits

- **Soft limit:** ~2000 calls/hour
- **Enforcement:** Occasional 429 errors
- **Recommendation:** Batch requests, cache results
- **Error handling:** Retry with exponential backoff

### Symbol Formatting

- **Stocks:** Use ticker as-is (`NVDA`, `MSFT`)
- **Indices:** Prefix with `^` (`^GSPC`, `^VIX`)
- **URL encoding:** Replace `^` with `%5E` in URLs

### Reliability Notes

This API is unofficial and subject to change without notice. It has been stable for years but could break at any time. Monitor for errors and have a fallback plan.

---

## Error Handling

All fetcher functions include error handling:

```python
try:
    req = urllib.request.Request(url, headers={...})
    resp = urllib.request.urlopen(req, timeout=timeout)
    return json.loads(resp.read())
except Exception as e:
    print(f"⚠️ Failed: {url[:60]}... — {e}")
    return None
```

**Strategy:**
- Timeout: 15 seconds per request
- Failed requests return `None`
- Other APIs continue even if one fails
- Output files are written even with partial data

---

## Fair Use Guidelines

All APIs are free and public. Follow these guidelines to maintain access:

1. **Rate limits:** Don't exceed documented limits
2. **Caching:** Store results, don't refetch the same data repeatedly
3. **Throttling:** Add delays between requests when fetching many endpoints
4. **User-Agent:** Always set a descriptive User-Agent header
5. **Error handling:** Back off on errors, don't spam failed requests

**Recommended Fetch Frequency:**
- **Market data:** Hourly (more frequent is unnecessary)
- **Fear & Greed:** Daily (updates once per day)
- **DeFi TVL:** Daily (slow-moving metric)

---

## Testing API Availability

Check if APIs are responsive:

```bash
# CoinGecko
curl -I "https://api.coingecko.com/api/v3/ping"

# Alternative.me
curl -I "https://api.alternative.me/fng/"

# DeFi Llama
curl -I "https://api.llama.fi/protocols"

# Yahoo Finance
curl -I "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
```

All should return `200 OK` status.

---

**Last Updated:** 2026-03-13
