# Deep-Clean Battle Planner

**Turn the dreaded whole-house deep clean into a schedulable project.**

Deep cleaning fails the same way every time: starting in the wrong room,
underestimating by 2×, running out of steam with the worst rooms
untouched, and guessing at cleaner chemistry — which is how people etch
their stone countertops with vinegar or mix bleach and acid into chlorine
gas (tens of thousands of cleaning-chemical exposures hit US poison
centers every year).

## The problem
1. **No order.** Mopping before dusting, floors before shelves — every
   out-of-order step is rework.
2. **No capacity math.** A "4-hour Saturday" fits ~3.4 hours of cleaning
   once dwell times, supplies hunts, and phone checks land.
3. **No chemistry.** Soil type decides the product (alkaline for grease,
   acid for minerals, enzymes for organics) and surface decides the
   constraint (stone hates acid, laminate hates water).
4. **No upkeep model.** Deep clean once → no cadence → back to zero in a
   month.

## What this toolkit does
- `plan` — rooms + hours → ordered waves (dusty-first, top-down,
  machines-at-T-0), per-task minutes, honest deferral of what doesn't fit.
- `schedule` — waves mapped to your real time blocks at 85% capacity,
  leftovers named, upkeep cadence table printed.
- `products` — surface × soil → correct cleaner + dwell + warnings, with
  the never-mix danger table on every run.
- `zone` — one-room playbook with running time marks to keep pace honest.

## Quick start
```bash
# Plan a 4-hour, 3-room session
python3 scripts/clean_planner.py plan --rooms kitchen,bathroom-main,livingroom --hours 4

# Map 6 rooms onto a Sat/Sun/Mon weekend
python3 scripts/clean_planner.py schedule --blocks "Sat 3h,Sun 2h,Mon 1h" \
    --rooms-list kitchen,bathroom-main,livingroom,bedroom,hallway,entry

# Check the right chemistry before spraying
python3 scripts/clean_planner.py products --surface tile-grout --soil mold

# Execute one room with time markers
python3 scripts/clean_planner.py zone --room kitchen
```

Pure Python 3 stdlib. Offline. No products to buy, no accounts.

## Who needs this
- Households doing seasonal/move-out/before-guests deep cleans
- People whose cleaning sessions always end half-finished and demoralized
- Anyone unsure which cleaner is safe on which surface
- Those who want a recurrence cadence so the deep clean sticks

## License
MIT — see LICENSE.
