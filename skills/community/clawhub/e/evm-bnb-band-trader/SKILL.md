---
name: evm-bnb-band-trader
description: Execute BNB Chain EVM swing trades after importing a private key: buy when trigger price exceeds market condition, then place 5% take-profit and 3% stop-loss management. Use when user asks to automate BNB band/swing trading with strict TP/SL and wallet-key based execution.
---

# EVM BNB Band Trader

Implement BNB Chain swing trading with strict risk controls.

## 1) Configure secrets and params

Set environment variables before running:

- `EVM_PRIVATE_KEY` (wallet private key, never hardcode)
- `BNB_RPC_URL` (BSC RPC endpoint)
- `TOKEN_IN` (default WBNB)
- `TOKEN_OUT` (target token)
- `BUY_TRIGGER_PRICE` (trigger buy threshold)
- `BUY_SIZE_BNB` (position size in BNB)
- `TAKE_PROFIT_PCT` (default `0.05`)
- `STOP_LOSS_PCT` (default `0.03`)
- `POLL_SECONDS` (default `10`)

## 2) Run bot

Use script:

```bash
python scripts/bnb_band_bot.py --mode run
```

Dry run first:

```bash
python scripts/bnb_band_bot.py --mode dry-run
```

## 3) Strategy rules (fixed)

- Entry: execute buy when latest price >= `BUY_TRIGGER_PRICE`
- Exit TP: sell when price >= entry_price * 1.05
- Exit SL: sell when price <= entry_price * 0.97
- One-position mode: no pyramiding

## 4) Safety controls

- Refuse run if env vars missing
- Refuse run if private key format invalid
- Refuse run if gas or balance insufficient
- Log every decision with timestamp

## 5) Notes

- Script uses DEX quote+swap placeholder flow; wire production router/aggregator before real funds.
- Always run dry-run first and validate slippage/gas assumptions.
