# Spot Trade

## Buy flow

1. Parse coin and size from user intent
2. Run: `node "$HL_SCRIPTS_DIR/trade.js" spot buy <COIN> <SIZE>` — outputs preview JSON; exits with structured error if balance is insufficient
3. Apply confirmation logic from `requiresConfirm`/`requiresDoubleConfirm` flags
4. After user confirms, re-run:
```bash
node "$HL_SCRIPTS_DIR/trade.js" spot buy <COIN> <SIZE> --confirmed
```
5. Use the last JSON line as the result; report fill price or "not filled" outcome

Result format: `{ "ok": true, "oid": 12345, "avgPx": "3200.50", "filledSz": "0.1" }`

## Sell flow

1. Parse coin and size
2. Run: `node "$HL_SCRIPTS_DIR/trade.js" spot sell <COIN> <SIZE>` — outputs preview JSON; exits with structured error if balance is insufficient
3. Apply confirmation logic from `requiresConfirm`/`requiresDoubleConfirm` flags
4. After user confirms, re-run:
```bash
node "$HL_SCRIPTS_DIR/trade.js" spot sell <COIN> <SIZE> --confirmed
```
5. Use the last JSON line as the result

## Asset symbol convention

- Use the token name directly: `ETH`, `BTC`, `SOL`
- `trade.js` appends `/USDC` internally for `SymbolConverter` lookup
- If the asset is not found, the script exits with `{"error":"Asset X not found..."}`

## IOC price calculation

Buy: price = mid × (1 + slippage_pct/100)
Sell: price = mid × (1 − slippage_pct/100)

`slippage_pct` defaults to 5 and is configurable in `~/.aurehub/hyperliquid.yaml` under `risk.slippage_pct`. This applies only to IOC market orders — GTC limit orders use the exact price the user specifies.

If the IOC order returns unfilled, the price moved more than `slippage_pct`% between the mid fetch and the order. Retry or reduce size.
