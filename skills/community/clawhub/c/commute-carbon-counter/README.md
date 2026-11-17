# Commute Carbon Counter

**Know the real carbon footprint of how you move — and what actually changes it.**

For most people, daily mobility is their #1 personal emissions source (often 2–4 t CO2/yr
for a solo car commuter — more than home heating). Yet footprint calculators ask 40
questions once a year and produce one opaque number. This tool makes your mobility a
measurable system: log a trip in 10 seconds, see kg CO2 per trip/week/month, compare
modes honestly per-passenger-km, and get a ranked list of the trips that dominate your
footprint.

## What it does

- 🚗 **14 transport modes** with per-passenger-km emission factors (car, carpool, EV,
  bus, coach, metro, tram, train, bike, e-bike, walk, scooter, motorcycle, plane)
- 👥 **Honest carpool math** — same vehicle, emissions split by heads: 3-person carpool
  = 64 g/pkm, better than the bus
- 📊 **Reports with baseline** — every period shows your actual CO2 *and* the all-car
  counterfactual, so you see what your choices saved
- 🏆 **Top-trip ranking** — the two car trips a week that are half your footprint
- 🎯 **Annual trajectory vs budget** — are you on track for your 1.5°C-lifestyle
  mobility target (default 1 t/yr, configurable)?
- 🔁 **One-off comparisons** — `compare --km 18` answers "metro vs driving" instantly
- 📴 Local JSON storage, pure stdlib, zero dependencies

## Quick start

```bash
python3 scripts/commute_carbon.py log --mode car --km 18 --note office
python3 scripts/commute_carbon.py log --mode carpool --km 18 --passengers 3
python3 scripts/commute_carbon.py log --mode metro --km 9
python3 scripts/commute_carbon.py week
python3 scripts/commute_carbon.py compare --km 18
```

## Who needs this

- Anyone weighing a commute-mode change (car → transit, EV purchase, carpool)
- People tracking a personal sustainability goal who want feedback, not guilt
- Remote/hybrid workers quantifying what office days actually cost
- Companies running commute challenges (CSV export per participant)
- The perennial "should I fly or train" question, with numbers attached

## Example output

```
Week 2026-09-02 → 2026-09-08   9 trips, 214 km
  CO2: 14.2 kg   (baseline all-car: 41.1 kg  →  65% saved)
  top trips:
    1. 2026-09-03 car 36 km → 6.9 kg   office
```

Factor sources and honesty about ranges: [`references/emission-factors.md`](references/emission-factors.md)

## License

MIT
