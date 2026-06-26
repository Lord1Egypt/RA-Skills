# Market Intel Endpoints Reference

Complete API endpoint specifications with request/response examples for all data sources.

## 1. Fear & Greed Index — Alternative.me

### Latest Value

```
GET https://api.alternative.me/fng/
```

Response:
```json
{
  "name": "Fear and Greed Index",
  "data": [
    {
      "value": "25",
      "value_classification": "Extreme Fear",
      "timestamp": "1712016000",
      "time_until_update": "43200"
    }
  ],
  "metadata": { "error": null }
}
```

### Historical (N days)

```
GET https://api.alternative.me/fng/?limit=30
```

Returns array of daily values, most recent first. Use `limit=0` for entire history.

### Value Classification Scale

| Range | Classification | 中文 |
|-------|---------------|------|
| 0–24 | Extreme Fear | 極度恐懼 |
| 25–49 | Fear | 恐懼 |
| 50 | Neutral | 中性 |
| 51–74 | Greed | 貪婪 |
| 75–100 | Extreme Greed | 極度貪婪 |

---

## 2. Global Market — CoinGecko

```
GET https://api.coingecko.com/api/v3/global
```

Response (only bolded fields are displayed; the rest are returned but must be ignored as they cover the full 17k+ coin global universe and are not relevant to BitoPro's 18-coin scope):

```json
{
  "data": {
    "active_cryptocurrencies": 16203,        // IGNORE
    "upcoming_icos": 0,                       // IGNORE
    "ongoing_icos": 49,                       // IGNORE
    "ended_icos": 3376,                       // IGNORE
    "markets": 1183,                          // IGNORE
    "total_market_cap": { "usd": 2850000000000 },         // DISPLAY
    "total_volume":     { "usd":   98000000000 },         // DISPLAY
    "market_cap_percentage": {
      "btc": 61.5,                                        // DISPLAY
      "eth":  7.2                                         // DISPLAY
    },
    "market_cap_change_percentage_24h_usd": -1.23,        // DISPLAY
    "updated_at": 1712016000
  }
}
```

---

## 3. Coin Rankings — CoinGecko

```
GET https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,tether,ripple,binancecoin,usd-coin,solana,dogecoin,cardano,tron,the-open-network,litecoin,bitcoin-cash,shiba-inu,polygon-ecosystem-token,apecoin,kaia,bito-coin&order=market_cap_desc&per_page=100&page=1&sparkline=false
```

Response (array):
```json
[
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "https://...",
    "current_price": 83500,
    "market_cap": 1658000000000,
    "market_cap_rank": 1,
    "fully_diluted_valuation": 1755000000000,
    "total_volume": 28500000000,
    "high_24h": 84200,
    "low_24h": 82100,
    "price_change_24h": -350.5,
    "price_change_percentage_24h": -0.42,
    "market_cap_change_24h": -7000000000,
    "market_cap_change_percentage_24h": -0.42,
    "circulating_supply": 19856000,
    "total_supply": 21000000,
    "max_supply": 21000000,
    "ath": 109114,
    "ath_change_percentage": -23.5,
    "ath_date": "2025-01-20T09:11:54.494Z",
    "atl": 67.81,
    "atl_change_percentage": 123000,
    "atl_date": "2013-07-06T00:00:00.000Z",
    "last_updated": "2026-04-10T12:00:00.000Z"
  }
]
```

### Sorting Options

| `order` Value | Description |
|--------------|-------------|
| `market_cap_desc` | Market cap high → low (default) |
| `market_cap_asc` | Market cap low → high |
| `volume_desc` | Volume high → low |
| `volume_asc` | Volume low → high |

---

## 4. Trending Coins — CoinGecko

```
GET https://api.coingecko.com/api/v3/search/trending
```

Response:
```json
{
  "coins": [
    {
      "item": {
        "id": "bitcoin",
        "coin_id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "market_cap_rank": 1,
        "thumb": "https://...",
        "small": "https://...",
        "large": "https://...",
        "slug": "bitcoin",
        "price_btc": 1.0,
        "score": 0,
        "data": {
          "price": "$83,500",
          "price_change_percentage_24h": {
            "usd": -0.42
          }
        }
      }
    }
  ]
}
```

Note: CoinGecko returns 15 trending coins by search popularity globally. **Most will NOT be on BitoPro** — cross-reference `item.symbol` against the BitoPro symbol set and drop all non-matches. Do not surface non-BitoPro trending names to the user.

---

## 5. Company Holdings — CoinGecko

### BTC Holdings

```
GET https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin
```

### ETH Holdings

```
GET https://api.coingecko.com/api/v3/companies/public_treasury/ethereum
```

Response:
```json
{
  "total_holdings": 341649,
  "total_value_usd": 28500000000,
  "market_cap_dominance": 1.72,
  "companies": [
    {
      "name": "MicroStrategy",
      "symbol": "MSTR",
      "country": "US",
      "total_holdings": 214246,
      "total_entry_value_usd": 7538000000,
      "total_current_value_usd": 17890000000,
      "percentage_of_total_supply": 1.02
    }
  ]
}
```

---

## 6. Coin Detail — CoinPaprika

```
GET https://api.coinpaprika.com/v1/tickers/btc-bitcoin
```

Response:
```json
{
  "id": "btc-bitcoin",
  "name": "Bitcoin",
  "symbol": "BTC",
  "rank": 1,
  "total_supply": 21000000,
  "max_supply": 21000000,
  "beta_value": 1.0,
  "first_data_at": "2010-07-17T00:00:00Z",
  "last_updated": "2026-04-10T12:00:00Z",
  "quotes": {
    "USD": {
      "price": 83500,
      "volume_24h": 28500000000,
      "volume_24h_change_24h": -5.2,
      "market_cap": 1658000000000,
      "market_cap_change_24h": -0.42,
      "percent_change_15m": -0.05,
      "percent_change_30m": -0.12,
      "percent_change_1h": -0.18,
      "percent_change_6h": 0.45,
      "percent_change_12h": -0.32,
      "percent_change_24h": -0.42,
      "percent_change_7d": 2.15,
      "percent_change_30d": -8.5,
      "percent_change_1y": 45.2,
      "ath_price": 109114,
      "ath_date": "2025-01-20T09:11:54Z",
      "percent_from_price_ath": -23.5
    }
  }
}
```

### Available Time Frames

| Field | Description |
|-------|-------------|
| `percent_change_15m` | 15 分鐘 |
| `percent_change_30m` | 30 分鐘 |
| `percent_change_1h` | 1 小時 |
| `percent_change_6h` | 6 小時 |
| `percent_change_12h` | 12 小時 |
| `percent_change_24h` | 24 小時 |
| `percent_change_7d` | 7 天 |
| `percent_change_30d` | 30 天 |
| `percent_change_1y` | 1 年 |

---

## 7. BitoPro Trading Pairs

```
GET https://api.bitopro.com/v3/provisioning/trading-pairs
Accept: application/json
```

> ⚠️ **Required header:** `Accept: application/json`. Without it, the endpoint returns **schema documentation** (field names as strings) rather than real data. Verified 2026-04-14.

Response (all 13 fields per pair):
```json
{
  "data": [
    {
      "pair": "btc_twd",
      "base": "btc",
      "quote": "twd",
      "basePrecision": 8,
      "quotePrecision": 0,
      "minLimitBaseAmount": "0.0001",
      "maxLimitBaseAmount": "100000000",
      "minMarketBuyQuoteAmount": "190",
      "orderOpenLimit": 200,
      "maintain": false,
      "amountPrecision": 4,
      "orderBookQuotePrecision": 0,
      "orderBookQuoteScaleLevel": 5
    }
  ]
}
```

### Field Reference

| Field | Meaning |
|-------|---------|
| `pair` | Trading pair identifier (e.g. `btc_twd`) |
| `base` / `quote` | Base / quote currency (lowercase) |
| `basePrecision` / `quotePrecision` | Max decimal places for base/quote amounts |
| `minLimitBaseAmount` / `maxLimitBaseAmount` | Min/max limit-order size in base units |
| `minMarketBuyQuoteAmount` | Min market-buy order size in quote units |
| `orderOpenLimit` | Max simultaneous open orders per pair |
| `maintain` | `true` = pair under maintenance (suspended) |
| `amountPrecision` | Decimal places allowed for order amount |
| `orderBookQuotePrecision` | Order book quote-side precision |
| `orderBookQuoteScaleLevel` | Order book price aggregation level |

Use `base` (uppercase via `.upper()`) to determine listed coins. Flag `maintain: true` pairs separately. These per-pair specs are essential for users preparing to place orders via the `bitopro-spot` skill.
