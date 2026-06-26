# Balance

## Spot balances

```bash
node "$HL_SCRIPTS_DIR/balance.js" spot
```

Response shape:
```json
{
  "balances": [
    { "coin": "USDC", "token": 0, "total": "500.0", "hold": "0.0", "entryNtl": "0.0" },
    { "coin": "ETH",  "token": 3, "total": "0.1",   "hold": "0.0", "entryNtl": "320.0" }
  ]
}
```

- `total`: full balance including held amounts
- `hold`: locked in open orders
- `entryNtl`: notional value at entry price

## Perp positions and margin

```bash
node "$HL_SCRIPTS_DIR/balance.js" perp
```

Response shape:
```json
{
  "assetPositions": [
    {
      "type": "oneWay",
      "position": {
        "coin": "ETH",
        "szi": "0.1",
        "leverage": { "type": "cross", "value": 5 },
        "entryPx": "3200.0",
        "unrealizedPnl": "12.5",
        "liquidationPx": "2900.0",
        "marginUsed": "64.0"
      }
    }
  ],
  "marginSummary": {
    "accountValue": "564.0",
    "totalMarginUsed": "64.0"
  },
  "withdrawable": "500.0"
}
```

- `szi`: signed size — positive = long, negative = short
- `withdrawable`: max USDC that can be withdrawn without closing positions
