# Perp Trade

## Open position

```bash
# Step 1: get preview
node "$HL_SCRIPTS_DIR/trade.js" perp open <COIN> <long|short> <SIZE> [--leverage N] [--cross|--isolated]
# Step 2: after user confirms, re-run with --confirmed
node "$HL_SCRIPTS_DIR/trade.js" perp open <COIN> <long|short> <SIZE> [--leverage N] [--cross|--isolated] --confirmed
```

- `--leverage N`: sets leverage before placing order via `updateLeverage()`; omit to use current account leverage (defaults to cross margin)
- `--cross` (default): cross margin — shared margin pool
- `--isolated`: isolated margin — fixed margin per position

The script outputs a preview JSON first. After `--confirmed`, calls `updateLeverage()` (if `--leverage` specified), then places the IOC order. On the `--confirmed` run the preview line is output again — use the last JSON line as the result.

**Leverage warning:** If `leverage ≥ leverage_warn` (default 20x from `hyperliquid.yaml`), the preview sets `leverageWarning: true` — show an extra warning before prompting.

**Leverage change warning:** If `--leverage N` is specified, the preview sets `leverageChangeWarning: true`. The leverage update takes effect immediately on the exchange before the order is placed. If the user has an existing cross-margin position for this coin, its leverage will change as well. Show the warning: "Note: this leverage setting takes effect immediately and will apply to all existing cross-margin positions for this coin."

Result format: `{ "ok": true, "oid": 12345, "avgPx": "3200.50", "filledSz": "0.1" }`

## IOC price calculation

Buy: price = mid × (1 + slippage_pct/100)
Sell: price = mid × (1 − slippage_pct/100)

`slippage_pct` defaults to 5 and is configurable in `~/.aurehub/hyperliquid.yaml` under `risk.slippage_pct`.

## Close position

```bash
# Step 1: get preview
node "$HL_SCRIPTS_DIR/trade.js" perp close <COIN> <SIZE>
# Step 2: after user confirms, re-run with --confirmed
node "$HL_SCRIPTS_DIR/trade.js" perp close <COIN> <SIZE> --confirmed
```

Direction is **auto-detected**: the script calls `clearinghouseState()` and reads `szi` (signed position size):
- `szi > 0` (long) → places a sell order with `r: true` (reduce-only)
- `szi < 0` (short) → places a buy order with `r: true`

If no open position is found for the coin, the script exits with an error. On the `--confirmed` run the preview line is output again — use the last JSON line as the result.

Result format: `{ "ok": true, "oid": 12345, "avgPx": "3200.50", "filledSz": "0.1", "closedDirection": "long" }`

## Leverage limits

Each asset has a `maxLeverage` field in the perp metadata. If requested leverage exceeds this, `updateLeverage()` will fail. The error message will indicate the asset's maximum. Lever must also be between 1 and 100.

## Funding rates

Hyperliquid perps use a mark-price-based funding mechanism. Funding is charged/credited continuously. Long positions pay funding when the mark price is above the oracle; shorts receive it. Check current funding rates at app.hyperliquid.xyz.
