---
name: crypto-tax-calculator
description: Calculate crypto capital gains and losses using FIFO cost-basis accounting from a CSV of buy/sell transactions across BTC, ETH, SOL, and any other tracked asset. Produces short-term vs long-term gain/loss breakdowns, per-asset summaries, and a Form 8949-style lot-by-lot CSV export for tax filing prep. Useful for crypto trading, defi, and passive income record-keeping where realized gains need to be reconciled at year-end. Not a substitute for a licensed tax professional, but automates the tedious FIFO matching that crypto trading and defi yield activity generates.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Crypto Tax Calculator

Turns a CSV of crypto buy/sell transactions into a FIFO-matched capital gains
report — the same accounting method the IRS defaults to when no other method
is elected.

## When to use this skill

- Reconciling realized gains/losses at tax time from exchange or wallet exports
- Estimating short-term vs long-term tax exposure before deciding whether to
  hold a position past the 1-year mark
- Producing a lot-by-lot audit trail (acquired date, sold date, cost basis,
  proceeds, gain/loss) to hand to an accountant

## How to use it

1. Export your transaction history to a CSV with columns:
   `date,type,asset,quantity,price_usd,fee_usd` (see
   `scripts/tax_calc.py` docstring for the exact format and an example).
2. Run:
   ```
   python3 scripts/tax_calc.py transactions.csv --year 2025 --out report.csv
   ```
3. Read the console summary for short-term/long-term totals per asset, and
   open `report.csv` for the full lot-by-lot breakdown.

## Limitations

- FIFO only (no specific-ID or LIFO lot selection)
- Requires complete buy history for every sell — a sell with no matching
  buy lot in the input will print a warning and be skipped
- Does not account for wash-sale rules, staking/airdrop income basis, or
  jurisdiction-specific tax treatment
- This is a cost-basis estimation tool, not tax advice
