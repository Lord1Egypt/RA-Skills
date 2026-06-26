# Balance Reference

## Command

```bash
node "$POLY_SCRIPTS_DIR/balance.js"
```

## Output Format

```
0x1234...abcd
   POL:    0.1234
   USDC.e: $100.50  ← trading token
   CLOB:   $50.00  ← available for orders
```

## Fields

- **POL** — native gas token balance (need >= 0.01 POL to trade)
- **USDC.e** — Bridged USDC on Polygon (the token used for all Polymarket trades)
- **CLOB** — balance deposited into the Polymarket CLOB system (only shown if CLOB credentials are configured)

## CLOB Balance vs Wallet Balance

Your USDC.e wallet balance and CLOB balance are separate:
- **Wallet USDC.e** — funds in your wallet, approved per-trade
- **CLOB balance** — funds deposited into Polymarket's system for pending/open orders

For market orders (FOK), funds are approved from your wallet directly — you do not need a CLOB deposit.
