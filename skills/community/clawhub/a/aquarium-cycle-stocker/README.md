# Aquarium Cycle & Stocker

Stop killing fish in the first six weeks. This toolkit plans the fishless nitrogen cycle
with a dated dosing/testing calendar and a hard "safe to stock" gate, computes
**adult-size** bioload for any stocking list (the pet store sells juveniles — you're
signing an IOU), screens species compatibility and schooling minimums, and converts your
nitrate readings into an exact water-change schedule that respects your tap-water floor.

## The real-world problem

- New-tank syndrome (ammonia/nitrite spike before bacteria colonize) is the #1 killer of
  beginner fish — the cycle takes 3–6 weeks and most people add fish on day 3.
- "One inch per gallon" ignores adult size and body shape: a 20 cm fancy goldfish is ~8×
  the biomass of six neons. Thousands of tanks are overstocked on day one.
- Nitrate creep is invisible until fish stress: without the production-vs-tap-floor
  equation, water-change routines either under-deliver or waste water.

## What it does

`scripts/tank_plan.py` — three subcommands, Python stdlib, no dependencies:

- **`cycle`** — dated fishless-cycle calendar (bottled-bacteria seeding flag), expected
  readings per phase, the 24-hour 2-ppm ammonia clearance gate (twice), emergency
  fish-in-cycle protocol
- **`stock`** — 24-species database (adult cm, shape factor, temp/pH bands, schooling
  minimums, temperament); computes shape-weighted adult bioload vs filter capacity;
  flags conflicts (betta+guppy=NO, angels+neons=RISKY...) and schooling violations;
  builds a 14-day-staggered stocking-wave plan
- **`wc`** — one-shot change size to hit target nitrate; steady-state weekly fraction
  from measured nitrate production; detects the tap≥target impossibility and routes to
  plants/resin/RO options

## Quick start

```bash
python3 scripts/tank_plan.py cycle --volume 75 --temp 26 --bacteria
python3 scripts/tank_plan.py stock --volume 75 --fish "8 ember tetra" --fish "6 corydoras" \
    --fish "1 honey gourami"
python3 scripts/tank_plan.py wc --volume 75 --nitrate 35 --target 20 --tap 8 --production 12
```

## Reference

`references/cycle-and-stocking.md` — NH₃/pH toxicity table, nitrite "brown blood" salt
antidote, cycle speed levers, quarantine protocol, goldfish special cases, test-kit
gotchas (the nitrate bottle #2 shake).

## License

MIT © Denis Voronin
