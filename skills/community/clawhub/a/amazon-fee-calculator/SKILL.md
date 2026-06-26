# Amazon FBA Fee Calculator — Know Your REAL Profit

**Stop guessing. Know exactly what you'll make before you sell a single unit.**

## Description
Full FBA profitability calculator with 2026 fee schedule. Calculates referral fees, FBA fulfillment fees, storage costs, and net margin. Supports all size tiers and 20+ categories.

## When to Use
- User wants to calculate Amazon FBA profitability
- User asks about Amazon fees, margins, or ROI
- User is evaluating whether to sell a product on Amazon
- User compares FBA vs FBM costs
- User mentions COGS, margin, or break-even price

## Usage
```bash
# Basic: selling price + product cost
cd <skill_dir>/scripts && python3 calculator.py 24.99 5.00

# Full options
cd <skill_dir>/scripts && python3 calculator.py 9.95 2.00 --ship 0.50 --weight 8 --category grocery --units 200 --ppc 1.50
```

## Options
- `--ship COST` — Shipping cost to FBA per unit
- `--weight OZ` — Product weight in ounces
- `--dims L W H` — Dimensions in inches
- `--category CAT` — Product category (grocery, beauty, electronics, etc.)
- `--units N` — Monthly units sold (for projections)
- `--ppc COST` — PPC/advertising cost per unit

## What It Calculates
- Referral fee (category-specific, with thresholds)
- FBA fulfillment fee (weight-based, by size tier)
- Monthly storage fee (per unit, seasonal rates)
- Total cost per unit
- Profit per unit, margin %, ROI %
- Monthly and annual profit projections
- Break-even selling price

## No Dependencies
Pure Python 3. No pip install. No API keys. Works everywhere.
