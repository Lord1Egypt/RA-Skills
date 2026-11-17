# Clean Air Room Planner

**Buy the right purifier. Place it right. Breathe measurable better air.**
Exact CADR sizing from room volume × target air changes (5 ACH smoke,
4–5 allergy, 2–3 general), adequacy checks for the purifier you already
own, DIY Corsi-Rosenthal box engineering, a PM2.5 event diary, and
filter-life tracking in real hours.

## The problem

Wildfire smoke now affects tens of millions of people for weeks per year;
pollen seasons are lengthening; and the purifier market answers with
confusing "for rooms up to X" claims computed at 2 ACH on maximum speed —
a standard inadequate for smoke. People under-buy, run units on sleep
mode (CADR drops 4×), place them in corners, and change filters on a
calendar instead of on loading. The physics of fixing this is one
multiplication; nobody does it.

## What it does

- `size` — required CADR (m³/h + CFM) from floor area, ceiling, and use.
- `check` — verdict on your existing unit: achieved ACH, minutes per air
  change, steady-state indoor/outdoor estimate.
- `crbox` — DIY box-fan + MERV-13 effective clean airflow estimate.
- `log add/analyze` — PM2.5 diary: indoor/outdoor ratio, purifier on/off
  effect, peaks, time-in-Good-band.
- `filter new/tick/status` — run-hour tracking with smoke-loading
  multipliers and change-due dates.

## Quick start

```bash
python3 scripts/clean_air.py size --area 20 --ceiling 2.7 --use smoke
python3 scripts/clean_air.py check --area 20 --cadr 300 --use smoke
python3 scripts/clean_air.py crbox --fan-cfm 1800 --filters 4
python3 scripts/clean_air.py log add --indoor 45 --outdoor 210
python3 scripts/clean_air.py log analyze
python3 scripts/clean_air.py filter new --name "Living HEPA" --rated-hours 2000
```

Stdlib-only Python 3. Data stays in a local JSON file.

## Who needs this

Everyone downwind of a wildfire (statistically: a growing share of North
America, southern Europe, Siberia, Australia), allergy sufferers (20–30 %
of adults in developed countries), and anyone who bought a purifier on
marketing claims and wonders why the air monitor disagrees.

## Disclaimer

Educational tool. Follow local public-health advisories during smoke
events; sensitive groups should relocate when advised.

## License

MIT © 2026 Denis Voronin
