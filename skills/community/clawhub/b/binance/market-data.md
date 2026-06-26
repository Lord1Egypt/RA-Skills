# Binance Market Data Patterns

Use public endpoints first to validate symbols, filters, and pricing assumptions.

## Common Spot REST calls

```bash
BASE="${BINANCE_BASE_URL:-https://api.binance.com}"

# Latest price
curl -s "$BASE/api/v3/ticker/price?symbol=BTCUSDT" | jq

# 24h stats
curl -s "$BASE/api/v3/ticker/24hr?symbol=BTCUSDT" | jq

# Order book snapshot
curl -s "$BASE/api/v3/depth?symbol=BTCUSDT&limit=100" | jq

# Recent trades
curl -s "$BASE/api/v3/trades?symbol=BTCUSDT&limit=100" | jq

# Klines
curl -s "$BASE/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=200" | jq
```

## Filter validation before order building

```bash
curl -s "$BASE/api/v3/exchangeInfo?symbol=BTCUSDT" | jq '.symbols[0].filters'
```

Validate at least:
- `PRICE_FILTER` tick size and min/max price
- `LOT_SIZE` step size and min/max quantity
- `MIN_NOTIONAL` minimum quote value

## Data source awareness

Binance market endpoints can be served by memory cache or matching engine paths.
When debugging inconsistencies, verify endpoint data source characteristics in official docs.

## Safe local snapshot

```bash
mkdir -p ~/binance/snapshots
curl -s "$BASE/api/v3/exchangeInfo?symbol=BTCUSDT" > ~/binance/snapshots/BTCUSDT-exchangeInfo.json
```
