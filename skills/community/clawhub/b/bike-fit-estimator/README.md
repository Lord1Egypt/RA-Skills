# Bike Fit Estimator

**Knee pain at mile 20 is geometry, not weakness — and geometry is
computable from two measurements.**

Millions of riders are on bikes a size off, with saddle heights inherited
from a previous owner or set by eyeball. The result: front-of-knee pain,
numb hands, hot feet, sore necks — and the conclusion "cycling hurts,"
when the bike was simply never set up for their body. A professional fit
costs $150–400; a large part of it is formula + symptom table you can run
yourself, and this skill runs it offline.

## What it does

- **`size`** — frame-size band (road/commuter/gravel/MTB), saddle height
  (inseam × 0.885 LeMond, Holmes 25–35° knee-angle cross-check), crank
  length, KOPS setback starting point, standover clearance target.
- **`position`** — saddle-to-bar drop by flexibility × ride type, reach
  heuristic, saddle tilt, and the one-variable-at-a-time transition
  protocol.
- **`pain`** — routes 9 symptom classes (front/back/outer knee, numb
  hands, saddle numbness, hot foot, neck/traps, lower back, hip rocking)
  to ranked causes with the exact first adjustment to try.
- **`standover`** — clearance verdict for a specific frame listing.

## Quick start

```bash
python3 scripts/bike_fit.py size --inseam 84 --height 178 --type road
python3 scripts/bike_fit.py position --height 178 --flexibility medium --type road
python3 scripts/bike_fit.py pain --symptom numb-hands
python3 scripts/bike_fit.py standover --inseam 84 --standover-height 80 --type road
```

Stdlib-only Python 3. Offline.

## Repository layout

- `SKILL.md` — triggers, workflow, pain-routing table, pitfalls
- `references/fit-science.md` — the geometry, formulas, cleat science,
  flexibility gates, adjustment protocol
- `references/used-bike-buying.md` — fit-first used-bike screening
- `scripts/bike_fit.py` — the estimator

## License

MIT © Denis Voronin
