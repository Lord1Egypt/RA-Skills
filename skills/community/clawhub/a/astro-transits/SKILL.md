---
name: astro-transits
description: Astrological transit calculator with natal chart support. Daily transits, weekly forecasts, void-of-course Moon, aspects, stations, and ingresses. Uses Swiss Ephemeris.
version: 1.0.0
homepage: https://github.com/mizukaizen/openclaw-skills-public
license: MIT
metadata: {"clawdbot":{"emoji":"🌟","requires":{"bins":["python3"],"env":[]},"primaryEnv":""}}
---

# Astro Transits

Full astrological transit calculator for AI agents. Calculates planetary positions, aspects to any natal chart, Moon phases, void-of-course periods, stations, and ingresses. Uses Swiss Ephemeris (pyswisseph) with Moshier fallback — no API key needed.

## Setup

Install the dependency:

```bash
pip install pyswisseph
```

Generate a natal chart (one-time setup per user):

```bash
python3 {baseDir}/scripts/natal_chart.py \
  --date "1993-05-13" \
  --time "01:20" \
  --tz "Australia/Brisbane" \
  --lat -27.2308 --lon 153.0972 \
  --save natal.json
```

Parameters:
- `--date` — Birth date (YYYY-MM-DD)
- `--time` — Birth time in 24h format (HH:MM)
- `--tz` — Timezone name (e.g. `America/New_York`, `Europe/London`, `Australia/Brisbane`)
- `--lat` / `--lon` — Birth location coordinates
- `--save` — Save chart to JSON file for reuse

## Daily Transits

```bash
python3 {baseDir}/scripts/transits.py --chart natal.json
python3 {baseDir}/scripts/transits.py --chart natal.json --date 2026-03-15
```

Returns: current planetary positions, active aspects to natal chart (ranked by significance), Moon sign/phase, stations, and ingresses. Top 8 aspects shown with orb, house placement, and interpretive meaning.

## Weekly Forecast

```bash
python3 {baseDir}/scripts/transits.py --chart natal.json --week
```

Returns: top 3 most significant transits for the coming week with peak dates and themes.

## Void-of-Course Moon

```bash
python3 {baseDir}/scripts/voc_check.py
```

Returns JSON: `{"voc": true/false}` with end time, duration, and next Moon sign if currently void-of-course. No natal chart needed — this is a universal calculation.

## What It Covers

- **Planets:** Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, True Node
- **Aspects:** Conjunction, sextile, square, trine, opposition (with variable orbs for personal vs outer planets)
- **Houses:** Placidus house system
- **Events:** Planetary stations (retrograde/direct), sign ingresses
- **Moon:** Phase, sign, void-of-course detection
- **Interpretations:** Built-in aspect meanings for all planet-aspect combinations

## Notes

- No API key or external service required — all calculations run locally
- Swiss Ephemeris provides sub-arcsecond accuracy
- Falls back to Moshier ephemeris if Swiss Eph data files are absent
- Natal chart JSON can be generated once and reused indefinitely
- Timezone handling uses Python's `zoneinfo` (Python 3.9+)
