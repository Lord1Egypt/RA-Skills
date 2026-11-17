# Firewood Cord Calculator

**A "cord" of firewood, a "face cord," and a "truckload" are three
different amounts of wood — and only one of them is 128 cubic feet.**

Firewood is sold in a language designed to confuse: the cord (128 ft³
stacked) gets quietly replaced by face cords (⅓), ricks (whatever the
rack is), and pickup loads (~½–⅔). Then species swings energy 2× per
cord, "seasoned" often means cut-last-month, and green oak burns at ~55%
of its nameplate heat because you're boiling water in your stove.

## What It Does

`scripts/cord_calc.py`:

```bash
python3 scripts/cord_calc.py volume --length-ft 8 --height-ft 4 --depth-in 16
python3 scripts/cord_calc.py evaluate --species red-oak --price 300 --moisture 22
python3 scripts/cord_calc.py compare --price 300 --species red-oak --propane 2.60 --gas 1.40
python3 scripts/cord_calc.py season --species white-oak --split-in 5 --ready 2027-11-01
python3 scripts/cord_calc.py annual --sqft 2000 --hdd 5000 --fraction 0.6
```

- **Volume honesty**: stack dimensions + packing factor (tight/hand/loose)
  → true cord fraction. A hand-stacked 8×4×16" face cord is 0.30 cord,
  not 0.33.
- **Energy evaluation**: 20-species BTU table × moisture correction ×
  stove efficiency → delivered MMBtu and $/MMBtu for any offer.
- **Fuel comparison**: wood vs propane, natural gas, resistance electric,
  and heat pump at YOUR prices — with the fair cord price computed for
  your local market.
- **Seasoning back-planner**: split-by date for a ready-by date,
  species-specific, adjusted for split thickness.
- **Annual demand sizing**: house ft² × climate HDD → cords/season with
  the 1.4× first-year reality factor and stacking-space math.

## Who Needs This

- Anyone buying firewood who's been quoted "a cord, $350, cash"
- Wood-burning households comparing heat costs vs their heat pump/gas
  furnace before winter
- Rural property owners sizing seasoning schedules for self-cut wood
- Sellers who want to price honestly without shorting themselves
- Post-storm cleanup: what's that downed cherry actually worth in heat?

## Example

Seller offers "seasoned red oak, $300/cord." The evaluate + compare pass
at real market prices ($2.60/gal propane, $1.40/therm gas, COP-3 heat
pump) shows: wood at $17.86/MMBtu vs heat pump $13.68 and gas $14.74 —
fair wood price in that market is ≤ $230/cord, and a moisture meter
reading of 28% (not the claimed "seasoned") drops delivered heat another
12%. That's a $150 negotiation won with arithmetic.

## License

MIT — see LICENSE.
