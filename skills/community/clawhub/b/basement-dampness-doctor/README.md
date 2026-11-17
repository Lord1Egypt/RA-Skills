# Basement Dampness Doctor

**Condensation or leak? A dehumidifier or a contractor? Physics answers before you spend.**

Musty basements get one of two wrong treatments: a dehumidifier bought for a
water problem, or a $12k waterproofing system sold for an air problem. This
skill separates them with checkable physics: moisture condenses on any surface
colder than the air's dew point, so the tool computes the dew point (Magnus
formula), estimates the wall-surface temperature from a deep-soil seasonal
lag model, and renders a CONDENSATION vs LIQUID verdict — then ranks the 10
classic moisture sources cheapest-first (downspout extenders before drain
tile) and sizes the dehumidifier honestly (AHAM pints/day, cold-basement
derating, energy cost at your rate).

## What it does

- **`analyze`** — dew point vs wall temperature verdict; efflorescence vs mold
  vs tide-mark decoder; suggested RH target and capacity class.
- **`dehumidifier`** — pints/day sizing from area × dampness class × openness,
  ×1.2 cold-basement derating, drain-hose advice, $/month energy pricing, and
  an existing-unit "is it keeping up?" check from measured bucket-fill rates.
- **`sources`** — ranked audit of the 10 sources with fix prices; wall-sign
  reading (efflorescence = liquid path; mold-on-organics = air problem).
- **`log`** — humidity CSV analyzer: average/min/max, high-RH clusters by
  month, worst-case dew point, calibration note.

## Who needs this

Anyone with a basement or crawl space that smells, grows spots, or sweats —
and anyone about to spend $50 or $10,000 on the wrong fix.

## Usage

```bash
python3 scripts/dampdoctor.py analyze --air-t 22 --rh 70 --soil-t 14 \
  --wall-t 16 --area 800 --ceiling 2.3 --season summer
python3 scripts/dampdoctor.py dehumidifier --area 800 --class wet --energy-rate 0.34
python3 scripts/dampdoctor.py sources --grading negative --downspouts 0.5 \
  --gutters clogged --dryer-vent inside --sump none --wall-signs efflorescence
python3 scripts/dampdoctor.py log --csv basement_log.csv --target 50
```

Physics + decoder + fix prices: `references/moisture-physics.md`.

## License

MIT © 2026 Denis Voronin
