# Data Sources Reference

## Price Data

### onchainos CLI
- **ETH**: `1:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`
- **SOL**: `501:So11111111111111111111111111111111111111112`
- **BNB**: `56:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`

Command:
```bash
onchainos market prices "1:0x...,501:...,56:..."
```

### BTC Price
- **Method**: Web search
- **Query**: `BTC price today USD`
- **Source**: CoinMarketCap, CoinGecko, etc.

## Fear & Greed Index

### API Endpoint
```
https://api.alternative.me/fng/?limit=2
```

### Response Format
```json
{
  "data": [
    {
      "value": "18",
      "value_classification": "Extreme Fear",
      "timestamp": "1773273600"
    }
  ]
}
```

### Classifications
| Value | Classification | Emoji |
|-------|---------------|-------|
| 0-24 | Extreme Fear | 🔴 |
| 25-49 | Fear | 🟠 |
| 50-74 | Greed | 🟢 |
| 75-100 | Extreme Greed | 🔵 |

## Liquidation Data

### Sources
1. **Primary**: Web search aggregation
   - Query: `crypto liquidation 24h today total amount`
   - Sources: CoinGlass, Gate, CoinAnk

2. **Fallback**: Direct API (requires key)
   - CoinGlass API: `https://api.coinglass.com/...`
   - Requires authentication

### Typical Values
- 24h total: $50M - $500M
- 1h: $5M - $50M
- High volatility: >$200M

## News Sources

### Cointelegraph RSS
```
https://cointelegraph.com/rss
```

### TokenInsight RSS
```
https://tokeninsight.com/rss/news
```

### Content Selection
- Prioritize: Regulation, macro, DeFi security
- Avoid: Price predictions, shilling
- Count: 5-8 items

## Economic Calendar

### Source
```
https://incrypted.com/en/calendar/
```

### Event Types
| Icon | Type | Examples |
|------|------|----------|
| 🔴 | Token Unlocks | KAITO, LayerZero, WhiteBIT |
| 🔴 | Fed Decisions | Interest rate decisions |
| 🟡 | Economic Data | CPI, GDP, unemployment |
| 📍 | Conferences | DC Blockchain Summit, NBX |

### Lookahead
- Fetch next 7 days of events
- Highlight same-day events
- Note timezone (usually UTC)
