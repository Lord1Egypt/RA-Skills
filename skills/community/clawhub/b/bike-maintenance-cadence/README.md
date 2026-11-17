# Bike Maintenance Cadence

**The problem.** Bikes fail by cascade. A $20 chain ridden 500 km past its 0.75% wear limit grinds the cassette ($60) and chainrings ($60) into matching its stretch — then the "sudden" repair bill is $150+ instead of $20, several times a year. The entire economics of bike ownership is *catching wear at the chain-checker stage*, and almost nobody owns a chain checker ($10) or knows component lifetimes in km — especially not adjusted for their actual conditions: wet/winter riding roughly doubles drivetrain wear, and a shed-stored bike corrodes cables between rides.

**What this does.** Converts how you actually ride into a **dated, per-component service calendar** and a **wear-parts budget**:

- **`schedule`** — weekly km + conditions + storage → dated next-service entries per component (chain measure at 2,280 km in wet conditions vs 4,000 dry; pads, cables, tires, BB, bearings, headset, tubeless sealant, suspension hours), plus the every-ride/weekly/monthly/quarterly/yearly cadence ladder
- **`budget`** — lifetime table × your km → realistic annual wear-parts cost: 120 km/wk wet commuter with discs ≈ $458/yr, itemized (chain $83, tires $76, cassette $57...) with the chain-discipline note that keeps cassette costs out of 2 of 3 drivetrain bills
- **`diagnose`** — symptom → ordered check sequence: skip-under-load (chain gauge → cassette → stiff link → B-gap), mystery creak (chainring bolts first — free fix, most common), disc rub, spongy lever, ghost-shifts, thump-per-revolution

Plus the cascade doctrine: replace the chain at 0.75% and the cassette survives 2–3 chains; ride to 1.0% and you buy both; a new chain on a worn cassette skips under load within a week — *that skip is the cassette's verdict*.

**Example.** Urban commuter, 120 km/week, rain, shed-stored, last full service August: the calendar shows pads were due in September, chain in August — 3 months overdue, which is exactly why it's now skipping under load in the 3 most-used cogs. The diagnose router confirms: measure the chain (likely past 1.0%), budget chain + cassette together, ~$95 — versus $150+ if the chainrings join.

## Quick start

```bash
python3 scripts/bike_cadence.py schedule --km-week 120 --conditions wet --storage shed --last-service 2026-08-01
python3 scripts/bike_cadence.py budget --km-week 120 --conditions wet --disc
python3 scripts/bike_cadence.py diagnose --symptom skip-under-load
```

## Files

- `SKILL.md` — component lifetime tables, cascade rules, symptom router, pitfalls
- `references/bike-wear-engineering.md` — chain-wear physics, parts pricing, cadence ladder, diagnostic trees, torque table, tool ladder, revival + pre-big-ride checklists
- `scripts/bike_cadence.py` — scheduler/budget/diagnostician (stdlib only)

## License

MIT © 2026 Denis Voronin
