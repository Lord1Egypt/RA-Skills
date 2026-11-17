# Diaper Economics & Growth Bands — Reference

## Why this problem is real

A baby uses 2,500-3,000 disposable diapers in year one alone, at
$0.20-$0.50 per diaper — a $700-$1,200 annual spend that is one of the
largest hidden line items of the first year. Virtually all of the
avoidable waste in that budget comes from **size timing errors**, not
brand choice:

- **Overbuy** a size the baby is about to leave → unused diapers that
  charities gladly take but that cost real money.
- **Underbuy / run out** → emergency purchases at drugstore per-unit
  prices (often 2x warehouse pricing).
- **Premature size-up** (parents read blowouts as "too small" when the
  real cause is a bad fit adjustment) → leaks that cost laundry and
  sleep.

The counterintuitive structure of diaper demand:

1. Usage is **highest when sizes are shortest**. Newborns go through
   10+/day but spend only ~3 weeks in size N and ~6 in size 1.
2. Usage **tapers inside every band** as bladder capacity grows —
   the average hides a 30-40% decline from entry to exit.
3. Size 4 is the "parking lot" — 5+ months at ~5/day. This is where
   bulk buys actually pay off.

## The bands (model constants)

Sourced from major-brand published weight ranges (Pampers/Huggies/
store brands converge) and CDC/WHO growth-chart p50 weight-by-age for
band durations:

| Size | kg range  | lbs (approx) | Days @ p50 | Changes/day |
|------|-----------|--------------|-----------:|-------------|
| N    | 0-4.5     | 0-10         |     21     | 8-12        |
| 1    | 4-6.5     | 8-14         |     42     | 7-10        |
| 2    | 6-8.5     | 12-19        |     56     | 6-9         |
| 3    | 8-11.5    | 16-25        |     70     | 4-8         |
| 4    | 10-14.5   | 22-32        |    140     | 4-7         |
| 5    | 13-18.5   | 28-41        |    180     | 4-6         |
| 6    | 16-23     | 35+          |    210     | 4-6         |
| 7    | 20-30     | 41+          |    240     | 3-5         |

Overlaps are intentional: brands overlap ranges so transitions can
happen early (lean baby) or late (chunky thighs). The script maps age
→ band via cumulative p50 days, then linearly tapers changes/day from
band-max at entry to band-min at exit.

## Adjustment heuristics (percentile drift)

- **90th percentile baby**: weight-based transitions fire earlier —
  shave ~20% off each band's days for sizes 1-3.
- **10th percentile**: add ~15%.
- **Preemie**: expect a longer N/1 period; many skip nothing.
- After every well-visit weigh-in, prefer the weight band over the
  calendar.

## Sizing-up signals (fit, not age)

Size up when two or more appear:
- Red marks on thighs or waist that don't fade in 15 minutes
- Blowouts at the leg gussets (up the back = fit issue, not size)
- Tabs fastening on the outermost setting
- Belly band rolls or gaps at the legs

Do NOT size up for: pee volume alone (absorbency handles it), one
random blowout, or age labels on the box.

## Cost engineering

Per-diaper price bands (US, 2025-2026 era):

| Tier | $/diaper | Examples |
|------|----------|----------|
| economy | $0.20-0.28 | store brands (Costco Kirkland, Target Up&Up, Amazon Mama Bear) |
| standard | $0.28-0.35 | Pampers Swaddlers tier, Huggies Little Snugglers on subscription |
| premium | $0.40-0.55 | sensitive-skin lines, overnight specialty |

Levers that actually move the bill:
1. **Warehouse club membership amortized over diapers alone** often
   pays for itself in year one (5-10% under Amazon subscribe pricing).
2. **Subscription discounts** (5-15%) — but pair with the stock
   planner or you'll accumulate a size the baby is leaving.
3. **Overnight specialty diapers** only for night from size 3+ —
   they solve wake-ups, not days.
4. **Per-unit math beats box-price math**: the `burn` mode prints
   $/box so comparisons normalize automatically.

## Registry recipe (worked)

Expected birthday 2026-11-01, registry horizon 6 months:

```bash
python3 scripts/diaper_stock_calculator.py plan \
    --from 2026-11-01 --to 2027-05-01 --birthday 2026-11-01
```

Then halve N/1 (guests oversupply small sizes), keep 2-3 near-nominal,
full 4. Include ~1 pack wipes per 100 diapers (wipes never size out).

## What this model deliberately does NOT do

- No brand absorption-quality modeling (leak equity between brands at
  the same size is real but anecdotal).
- No rash/sensitive-skin advice — medical, see a pediatrician.
- No cloth-diaper wash cadence (a genuinely different problem).
- No subscription-logistics optimization (shipping cadence vs stock
  room) — covered partially by the `usage` verdict thresholds.

## Safety notes

- Never reuse a diaper, never "air out" a saturated one to finish it.
- Overnight diapers from size 3 are the standard fix for
  sleep-disrupting leaks; sizing up for night only is a legitimate
  split strategy (day size 3, night size 4) and the planner's output
  supports it: buy the night size's box with the difference.
