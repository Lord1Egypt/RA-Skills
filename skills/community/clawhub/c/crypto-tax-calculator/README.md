# Crypto Tax Calculator

A zero-dependency Python tool that computes FIFO (first-in-first-out)
capital gains and losses from a CSV of crypto buy/sell transactions.

## What it does

- Matches every sell against the oldest open buy lots for that asset (FIFO)
- Classifies each realized gain/loss as short-term (<365 days held) or
  long-term (≥365 days held)
- Prints a per-asset and total summary to the console
- Optionally exports a detailed, lot-by-lot CSV suitable for handing to a
  tax preparer or importing into tax software

## Quick start

```bash
python3 scripts/tax_calc.py transactions.csv
python3 scripts/tax_calc.py transactions.csv --year 2025 --out report.csv
```

## Input format

```csv
date,type,asset,quantity,price_usd,fee_usd
2024-01-15,buy,BTC,0.5,42000,10
2025-06-01,sell,BTC,0.2,68000,5
```

`fee_usd` is optional and defaults to 0. Dates accept `YYYY-MM-DD` or
`YYYY-MM-DDTHH:MM:SS`.

## Dependencies

Standard library only — no `pip install` required.

## Disclaimer

This tool estimates cost basis and realized gains for informational
purposes. It does not implement wash-sale adjustments, specific-lot
identification, or jurisdiction-specific rules. Verify results with a
licensed tax professional before filing.
