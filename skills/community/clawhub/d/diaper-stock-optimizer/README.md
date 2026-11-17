# Diaper Stock Optimizer

**Buy the right number of diapers in the right sizes — before the baby outgrows them or you run out at 2 AM.**

Every new parent faces the same trap: warehouse clubs and baby showers
push giant boxes of small sizes, but babies blast through sizes N-2 in
weeks. Unused size-1 diapers are the single most-donated baby item in
the country. Meanwhile the sizes babies actually park in (4-5) are
 chronically understocked. This tool turns one input you know exactly
 — the birthday — into a size-by-size buying plan, a days-of-stock
countdown, and box-lifespan math.

## What it does

- **plan** — how many diapers of each size a date range needs, using
  growth-band durations (50th-percentile) and tapering changes/day
  (10/day newborn → 4/day toddler). Rounds to case multiples of 20.
- **usage** — takes a saved plan + your current shelf count and
  returns days-of-stock left, projected run-out date, and an order
  verdict (ORDER NOW / order soon / stocked).
- **burn** — one-size sanity check: weight band, box lifespans,
  cost by price tier.

## The problem in numbers

- Year-one diaper spend: **$700-$1,200** per baby
- A size-1 jumbo box outlives the size for 1 in 3 babies
- Convenience-store emergency buys cost ~2x warehouse pricing
- Size 4 is the parking lot: **5+ months** — the size to overstock

## Quick start

```bash
python3 scripts/diaper_stock_calculator.py plan \
    --from 2026-10-20 --to 2027-01-20 --birthday 2026-08-15
```

```
size    days     chg/day    need     buy
----------------------------------------
2         53         7.4     395     400
3         40         7.2     287     300
----------------------------------------
TOTAL     93                         700
```

```bash
python3 scripts/diaper_stock_calculator.py usage \
    --file scripts/data/plan_2026-10-20.json --stock 140
```

```
Days of stock left: 19.1  (at planned usage)
Projected run-out: 2026-11-07
VERDICT: Stocked - next order in ~5 days
```

## Install

No dependencies. Python 3.8+.

## License

MIT © Denis Voronin
