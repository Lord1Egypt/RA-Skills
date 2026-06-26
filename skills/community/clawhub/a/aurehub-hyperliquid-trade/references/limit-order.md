# Limit Order Flow

This reference covers GTC limit orders: place, list, cancel, and modify.

## Confirmation Logic

After running `limit-order.js place ...` (without `--confirmed`), the script outputs a `preview` JSON object. Read it and:

- If `requiresDoubleConfirm: true` — ask the user to confirm **twice** before re-running with `--confirmed`
- If `requiresConfirm: true` — ask once
- If both are false — re-run with `--confirmed` immediately (no prompt needed)
- If `leverageWarning: true` — add an extra warning line about high leverage before prompting
- If `leverageChangeWarning: true` — show: "Note: this leverage setting takes effect immediately and will apply to all existing cross-margin positions for this coin."

Preview format:
```json
{
  "preview": true,
  "action": "Open Long ETH (Perpetual)",
  "coin": "ETH",
  "side": "long",
  "price": 3000,
  "size": 0.1,
  "leverage": 10,
  "marginMode": "Cross",
  "tradeValue": "300.00",
  "marginUsed": "30.00",
  "confirmThreshold": 100,
  "largeThreshold": 1000,
  "leverageWarn": 20,
  "requiresConfirm": false,
  "requiresDoubleConfirm": false,
  "leverageWarning": false,
  "leverageChangeWarning": true
}
```

## Place a Limit Order

```bash
# Spot buy 0.1 ETH at $3000
node "$HL_SCRIPTS_DIR/limit-order.js" place spot buy ETH 3000 0.1
# After user confirms:
node "$HL_SCRIPTS_DIR/limit-order.js" place spot buy ETH 3000 0.1 --confirmed

# Perp reduce-only order (for TP/SL — closes existing position, will not open a new one)
node "$HL_SCRIPTS_DIR/limit-order.js" place perp short ETH 3500 0.1 --reduce-only --confirmed
```

### `--reduce-only` flag

Add `--reduce-only` to any `place` command to mark the order as reduce-only. The order will only reduce an existing position — it will **never** open a new position. Use this for take-profit and stop-loss orders. Works with both spot and perp, though most useful for perp.

### Trigger Orders (Stop Loss / Take Profit)

Use `--trigger-price` with `--sl` or `--tp` to place a trigger order. The exchange monitors the price and automatically places a market order when the trigger is hit.

```bash
# Stop loss: triggers market sell when price drops to $3056
node "$HL_SCRIPTS_DIR/limit-order.js" place perp short ETH 3200 0.1 --trigger-price 3056 --sl --reduce-only --confirmed

# Take profit: triggers market sell when price rises to $3408
node "$HL_SCRIPTS_DIR/limit-order.js" place perp short ETH 3200 0.1 --trigger-price 3408 --tp --reduce-only --confirmed
```

Required flags:
- `--trigger-price <price>` — the price at which the exchange triggers the order
- `--sl` or `--tp` — tells the exchange the trigger direction (`--sl`: trigger when price moves against you; `--tp`: trigger when price moves in your favor)
- `--reduce-only` — strongly recommended for TP/SL to prevent accidental position opening

Success output includes `"status": "waitingForTrigger"`:
```json
{ "ok": true, "oid": 12345, "coin": "ETH", "side": "short", "price": 3200, "size": 0.1, "status": "waitingForTrigger", "triggerPrice": 3056, "tpsl": "sl" }
```

Success output:
```json
{ "ok": true, "oid": 12345, "coin": "ETH", "side": "buy", "price": 3000, "size": 0.1, "status": "resting" }
```

`status` is `"resting"` (live on book) or `"filled"` (immediately matched).

## List Open Orders

```bash
node "$HL_SCRIPTS_DIR/limit-order.js" list
node "$HL_SCRIPTS_DIR/limit-order.js" list --coin ETH
```

Output:
```json
{ "orders": [{ "oid": 12345, "coin": "ETH", "side": "B", "limitPx": "3000", "sz": "0.1", "timestamp": 1700000000000 }] }
```

`side`: `"B"` = bid/buy, `"A"` = ask/sell.

Present as a table: Order ID | Coin | Side | Price | Size | Time.

## Cancel an Order

```bash
node "$HL_SCRIPTS_DIR/limit-order.js" cancel 12345
```

Output: `{ "ok": true, "orderId": 12345 }`

## Modify an Order

The script always outputs a preview first. After user confirms, re-run with `--confirmed`:

```bash
# Step 1: get preview
node "$HL_SCRIPTS_DIR/limit-order.js" modify 12345 --price 2900
# → { "preview": true, "orderId": 12345, "coin": "ETH", "side": "B", "oldPrice": 3000, "newPrice": 2900, "oldSize": 0.1, "newSize": 0.1 }
# Show user: "Changing order 12345: $3000 → $2900, size 0.1 (unchanged). Confirm? [y/N]"

# Step 2: after user confirms, re-run with --confirmed
node "$HL_SCRIPTS_DIR/limit-order.js" modify 12345 --price 2900 --confirmed
# → { "preview": true, ... }   ← preview line (ignore)
# → { "ok": true, "oldOid": 12345, "oid": 67890, "newPrice": 2900, "newSize": 0.1 }
```

Use the **last** JSON line as the result. The `--confirmed` run re-emits the preview line first — ignore it.

**Note:** Hyperliquid implements modify as cancel + reorder internally. The order ID **changes**: `oldOid` is the cancelled order, `oid` is the new resting order. Update any stored order ID to `oid` before issuing further cancel or modify commands.

Modify always requires single confirmation — no size-based threshold.
