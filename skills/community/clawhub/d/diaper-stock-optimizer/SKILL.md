---
name: diaper-stock-optimizer
description: Use when buying diapers in bulk, planning a Costco/Amazon stock-up run, checking how long current diaper stock will last, or deciding size transitions — size-by-size quantity math from the baby's birthday (growth-band durations + tapering changes/day), days-of-stock countdown with order verdicts, and per-size box-lifespan and cost estimates.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [diapers, baby, stock-up, bulk-buying, parenting, newborn, supplies]
---

# Diaper Stock Optimizer

Bulk diaper buying fails in two opposite ways: people either buy three
boxes of size 1 right before the baby grows out of size 1 (donated,
unused), or run out at 2 AM and pay convenience-store prices. The math
that prevents both is boring but decisive — how many days a baby
typically spends in each size, how many changes per day that age band
uses, and what's actually on the shelf. This skill runs that math from
a single input every parent knows exactly: the birthday.

## When to Use

- Planning a bulk stock-up (warehouse club, Amazon subscribe box,
  baby-shower registry) — what sizes and how many of each
- Deciding whether to buy the jumbo box of the current size or
  already start the next size
- Checking how many days of diapers are left in the closet and when
  to order
- Comparing box sizes and price tiers ("does a 240-count box of
  size 3 even get used before size 4?")
- Building a registry: what to put on it in what quantities

Don't use for: cloth diaper wash schedules (different math entirely),
or medical advice about rash/urine output — output-count questions go
to a pediatrician.

## The Model

Sizes N-7 are modeled as time bands a 50th-percentile baby passes
through, each with its own changes-per-day range that **tapers inside
the band** (a fresh size-2 baby uses ~9/day; one about to size up uses
~6/day):

| Size | Weight (kg) | Typical days in size | Changes/day |
|------|------------|---------------------|-------------|
| N    | 0-4.5      | ~3 weeks            | 8-12        |
| 1    | 4-6.5      | ~6 weeks            | 7-10        |
| 2    | 6-8.5      | ~8 weeks            | 6-9         |
| 3    | 8-11.5     | ~10 weeks           | 5-8         |
| 4    | 10-14.5    | ~5 months           | 4-7         |
| 5    | 13-18.5    | ~6 months           | 4-6         |
| 6    | 16-23      | ~7 months           | 4-6         |
| 7    | 20-30+     | pulls-up territory  | 3-5         |

Key truth: sizes 1-3 are **short stops** (a big box often outlives the
size), while size 4 is where babies park for months — that's the size
to overstock, not size 1.

## Workflow

1. Get the birthday (exact input, no guessing) and today's stock count.
2. Run the planner for the horizon you're buying for:
   ```bash
   python3 scripts/diaper_stock_calculator.py plan \
       --from 2026-10-20 --to 2027-01-20 --birthday 2026-08-15
   ```
   Output: per-size days × avg changes/day = need, rounded up to
   case multiples of 20. A plan JSON is saved to `scripts/data/`.
3. Check the shelf against the plan:
   ```bash
   python3 scripts/diaper_stock_calculator.py usage \
       --file scripts/data/plan_2026-10-20.json --stock 140
   ```
   Verdicts: `ORDER NOW` (<7 days), `order within a few days` (<14),
   `stocked` (with days until next order).
4. For single-size sanity checks (registry items, one box at the
   store): `burn --size 3 --lbs --tier premium` → weight band, box
   lifespans, cost.
5. Round **up** and prefer buying late over early for sizes 1-3;
   babies run big or small — adjust after the next well-visit weigh-in.

## Interpreting for a big or small baby

The model is calibrated to the 50th percentile. Adjust by observed
weight, not age: if the pediatrician says 90th percentile, expect size
transitions **earlier** than the day math says (buy one box less of
each small size); 10th percentile means longer stays. The `burn` mode
weight bands are the cross-check — size is chosen by weight, never by
age alone.

## Common Pitfalls

1. **Overbuying sizes 1-2.** New parents get size-1 boxes from
   everyone; the band is ~6 weeks. One jumbo box + one backup is
   plenty; put size 4 on the registry instead.
2. **Buying newborn size at all without reason.** Many babies skip N
   entirely (>3.5 kg at birth). Wait for the birth weight.
3. **Ignoring the taper.** A flat "8/day for size 2" overbuys by ~20%;
   the last weeks in a size use 6/day.
4. **Case-count tunnel vision.** A 240-box that gets outgrown at
   diaper 160 is not a bargain. The planner's `need` vs `buy` columns
   expose exactly this gap.
5. **Trusting brand age labels.** "Size 3, 16-28 lbs" on the package
   is marketing elastic; actual fit is belly-to-thigh geometry. When
   blowouts or thigh marks appear, size up regardless of the table.
6. **Measuring stock in "boxes" not "diapers."** Counts per box vary
   30-250 by size and brand; always count units.

## Verification Checklist

- [ ] Birthday confirmed against an actual document, not memory
- [ ] Current stock counted in units (not boxes) for `usage`
- [ ] Plan horizon matches the sale/shipping cadence you're buying for
- [ ] Sizes 1-3 rounded down (short bands), size 4+ rounded up
- [ ] Re-check after every well-visit weigh-in — rescale the plan

## One-Shot Recipe: baby-shower registry quantities

```bash
python3 scripts/diaper_stock_calculator.py plan \
    --from 2026-11-01 --to 2027-05-01 --birthday 2026-11-01
```
Take the `buy` column as the registry ceiling per size, then halve
sizes N-1 (guests oversupply small sizes) and keep size 4 whole. Add
one wipe pack per 100 diapers — wipes don't expire or size out.
