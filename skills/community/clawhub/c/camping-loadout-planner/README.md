# camping-loadout-planner

**Derive camping gear from conditions, not from what you packed last time.** Takes
forecast low, precip, bugs, water spacing, altitude, bear country and trek style →
generates the loadout with reasons, runs sleep-system math (bag comfort + pad R +
liner vs the derived requirement), audits pack weight against class budgets with a
ranked cut list, and sizes the camp kitchen from headcount.

## The real-world problem

Camping trips fail on predictable physics: a 20°F-*limit* bag treated as a 20°F-comfort
bag (it isn't — limit is "survive curled up"), a summer pad under a winter bag (the
ground drains the night), packs that "fit fine" turning out to be 35 lb on a 15-mile
day, and 4 lb of just-in-case gear that never gets used. Every one of these is a
derivable number: the coldest night defines the sleep stack, source spacing defines
water carry, the weight budget defines what stays home.

## What it does

| Capability | Detail |
|---|---|
| Condition-driven gear list | every item arrives with its WHY (precip %, bug season, low temp, water gap) |
| Sleep system math | required comfort = low − 5°F (− radiative/clear sky, − altitude lapse); bag+pad+liner stack verdict with °F margin |
| Pad R-value gates | R bands by night temp, stackable R (cheap foam under air pad) |
| Weight budget audit | base weight vs traditional/lightweight/UL budgets, cut list ranked (duplicates & low-use first), 20%-body-weight check |
| Kitchen sizing | fuel grams per person-day (canister fit check), food lb, water plan by terrain |
| Bear-country routing | canister-mandatory regions (Sierra/grizzly/Adirondacks) vs hang/ursack |

## Quick start

```bash
python3 scripts/camping_loadout.py --demo
python3 scripts/camping_loadout.py --trip scripts/trip.example.json
python3 scripts/camping_loadout.py --sleep 34 29 2 --sleep-liner 9
python3 scripts/camping_loadout.py --budget 24 lightweight
```

Stdlib only.

## Example

2-night shoulder-season trip, forecast low 34°F, clear skies, black-bear country.
Demo output: sleep requirement 26°F (34 − 5 − 3 radiative); the 29°F-comfort bag +
R-2 pad + liner stack → 38°F effective, margin +12°F, PAD OK. Gear list arrives
with per-item reasons (headnet OFF — bug season over; 2 L carry — sources every
4 mi; ursack — black bear country). Base weight 10.5 lb vs the 20–30 lb lightweight
budget → WITHIN BUDGET; day-1 pack 22.1 lb vs the 20%-body ceiling → OK.

## Why it matters

~40M Americans camp annually. The failure modes (cold nights, heavy packs, water
misplans) are all arithmetic on conditions you already know before leaving. This turns
packing from folklore-plus-anxiety into a checklist with stated margins — and the
cut list usually saves 2–4 lb without touching anything essential.
