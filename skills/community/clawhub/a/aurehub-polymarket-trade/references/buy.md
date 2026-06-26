# Buy Reference

## Command

```bash
node "$POLY_SCRIPTS_DIR/trade.js" --buy --market <slug> --side YES|NO --amount <usd>
```

- `--market` — market slug (from browse output or Polymarket URL)
- `--side` — `YES` or `NO`
- `--amount` — USDC.e to spend (dollars)

## Example

```bash
node "$POLY_SCRIPTS_DIR/trade.js" --buy --market bitcoin-100k-2025 --side YES --amount 25
```

## Flow

1. Fetches market data (Gamma API)
2. Shows preview: estimated price, estimated shares, spend amount
3. Runs hard-stop checks (market status, min order size); if USDC.e insufficient, offers POL→USDC.e auto-swap
4. Safety gate prompt (if amount >= $50)
5. Approves exact USDC.e amount to exchange contract
6. Submits FOK market order to Polymarket CLOB
7. Reports fill status and order ID

## Amount Semantics

For BUY, `--amount` is in **dollars (USDC.e)**. The SDK calculates the number of shares automatically based on the orderbook price.

## After the Buy

Your YES/NO shares are ERC-1155 tokens held in your wallet at the CTF contract address. Check them with `balance.js` (shows open positions with current value) or on Polygonscan.
