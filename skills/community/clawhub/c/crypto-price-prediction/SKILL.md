---
name: "crypto-price-prediction"
description: "Fetches next-hour predicted price for BTC/ETH from external prediction API. Supports BTCUSDT and ETHUSDT symbols only."
version: "1.0.1"
author: "Hermes Agent"
license: "MIT"
metadata:
  hermes:
    tags: [mlops, crypto, prediction, trading, api]
    related_skills: []
---

# Crypto Price Prediction Skill

Fetches **next-hour predicted price** for BTC or ETH from an external prediction API. Not a local technical analysis model — just an API wrapper.

- **API source**: `https://myfastapi.zeabur.app/v1/demo/predictions/next_hour/{BTC|ETH}`
- **Symbols supported**: `BTCUSDT`, `ETHUSDT` only
- **Horizon**: 1 hour (fixed — API limitation)
- **Output**: Unified JSON with current price (hour start), predicted price, and direction

## When to Use

- Quick next-hour price check for BTC/ETH
- When you want an external model's prediction instead of local TA

## Not For

- Other symbols (SOL, BNB, etc.)
- Horizons other than 1 hour
- Local technical analysis (no Binance/CoinGecko fallback here)

## Installation

Self-contained. Python 3.8+ stdlib only. Node.js 18+ for OpenClaw wrapper.

## Usage

### Hermes CLI
```bash
# BTC next-hour prediction
hermes skill run crypto-price-prediction --symbol BTCUSDT --hours 1

# ETH next-hour prediction
hermes skill run crypto-price-prediction --symbol ETHUSDT --hours 1
```

### OpenClaw API
```javascript
const { predictPrice } = require('./skill.js').tools;

const result = await predictPrice({ symbol: 'BTCUSDT', hours: 1 });
// Returns unified JSON prediction object
```

### Direct Python
```bash
cd /opt/data/.hermes/skills/crypto-price-prediction
TZ=Asia/Hong_Kong python3 scripts/predict.py --coin BTC
TZ=Asia/Hong_Kong python3 scripts/predict.py --coin ETH
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--symbol` | string | `BTCUSDT` | Trading pair: `BTCUSDT` or `ETHUSDT` |
| `--hours` | number | `1.0` | Horizon (API only supports 1h) |
| `--timezone` | string | (prompt) | User timezone (e.g., `HKT`, `UTC`, `America/New_York`) |

## Output Format (Unified JSON v1.0.1)

Both Hermes CLI and OpenClaw return identical JSON structure:

```json
{
  "timestamp": "2026-07-22 21:00 HKT",
  "symbol": "BTCUSDT",
  "horizonHours": 1,
  "currentPrice": 66405.74,
  "predictedPrice": 65662.84,
  "predictedDirection": "DOWN"
}
```

### Field Rules

| Field | Description |
|-------|-------------|
| `timestamp` | Prediction target time in user's timezone (format: `YYYY-MM-DD HH:MM TZ`) |
| `symbol` | Trading pair (`BTCUSDT` or `ETHUSDT`) |
| `horizonHours` | Always `1` (API limitation) |
| `currentPrice` | Price at start of current hour (e.g., if prediction at 08:02, price at 08:00). 2 decimal places. |
| `predictedPrice` | Predicted price at next hour mark. 2 decimal places. |
| `predictedDirection` | `UP` if `currentPrice < predictedPrice`, else `DOWN` |

### Verbal Output (when all fields populated)

```
Current price of BTC at 2026-07-22 20:00 HKT: 66,405.74
Predicted price of BTC at 2026-07-22 21:00 HKT: 65,662.84
Predicted direction of BTC in the next hour: DOWN
```

## Timezone Handling

- **First run**: Prompts user for timezone (e.g., `HKT`, `UTC`, `America/New_York`)
- **Remembered**: Stored locally, reused on subsequent runs
- **Refused**: Defaults to GMT (UTC)

## API Details

- **Endpoint**: `GET https://myfastapi.zeabur.app/v1/demo/predictions/next_hour/{BTC|ETH}`
- **Response**: `{"BTC predicted price (next_hour)": 64063.6992}` (float)
- **Rate limit**: Unknown — use reasonably
- **Current price source**: CoinGecko API (free, no key)

## Troubleshooting

- **API timeout/unreachable**: Check network access to `myfastapi.zeabur.app`
- **Invalid symbol**: Only `BTCUSDT`/`ETHUSDT` accepted
- **Non-1h horizon**: API only provides next-hour; `--hours` other than 1 logs warning
- **Current price fetch fails**: Prediction still returned, `currentPrice` and `predictedDirection` will be `null`

## Version History

### v1.0.1 (2026-07-24)
- Unified JSON output for Hermes CLI and OpenClaw
- Added `currentPrice` (hour-start price) and `predictedDirection` (UP/DOWN)
- Removed `changePercent`, `direction`, `confidence`, `dataSource`, `signals`
- Added timezone prompt + persistence (default: GMT)
- Verbal output with formatted prices (2 decimal places)
- Removed "zeabur" from description

### v1.0.0 (Initial)
- BTC/ETH next-hour prediction via external API
- Hermes CLI + OpenClaw plugin
- HKT timezone handling

## Disclaimer

**Not financial advice.** External API predictions are opaque — no visibility into methodology. Use at your own risk.

## License

MIT