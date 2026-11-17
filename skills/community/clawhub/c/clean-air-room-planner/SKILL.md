---
name: clean-air-room-planner
description: Use when buying or placing an air purifier, living through wildfire smoke, pollen season, or construction dust — computes the exact HEPA CADR a room needs from volume, desired air changes per hour (5 ACH smoke, 4-5 allergy, 2-3 general), checks whether YOUR purifier is adequate or where to move it, sizes DIY box-fan filters (CFM from fan curves + MERV pressure drop), runs a pollution diary that correlates indoor PM2.5 with outdoor events, and tells you when to change filters based on real usage hours.
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [air-quality, hepa, cadr, wildfire-smoke, pm25, allergy, purifier-sizing, home]
---

# Clean Air Room Planner

## Overview

Every wildfire season, three mistakes repeat at scale: people buy purifiers
too small for their rooms (marketing "large room" claims assume only 2 air
changes per hour), they run them on quiet mode (CADR drops 3–5×), and they
put them in the wrong place. The engineering is simple — **clean air
delivery rate (CADR) must match room volume × desired air changes per hour
(ACH)** — but the industry makes it hard to do the math.

This skill is that math, plus the operational kit around it:

1. **Purifier sizing** — CFM/CADR needed from room dimensions and target
   ACH (5 for smoke events, 4–5 allergy season, 2–3 general freshness),
   with noise and CADR-margin guidance.
2. **Adequacy check** — is your existing purifier enough for THIS room?
   Verdict + how long a full air change takes + whether running it on low
   makes it useless (it usually does).
3. **DIY box-fan filter sizing** — the CR Box (corsi-rose boxfan + MERV-13)
   engineering: fan free-flow CFM, filter pressure drop, effective clean
   airflow estimate, and filter-area rules.
4. **Pollution diary** — log indoor/outdoor PM2.5 readings; the analyzer
   computes indoor/outdoor ratio, infiltration factor, decay constants,
   and event summaries (how bad, how long, what helped).
5. **Filter-life tracker** — real usage hours vs rated life with
   change-due dates instead of "check the color of the light".

## When to Use

- Buying a purifier: "what CADR do I need for a 20 m² bedroom / 250 sq ft
  living room?"
- Smoke/pollen event: "is my purifier adequate, and where do I put it?"
- Building a DIY box-fan filter (Corsi-Rosenthal box)
- Deciding whether to run HVAC fan / recirculate during a smoke event
- "When should I actually change this filter?"
- Reviewing a PM2.5 log: how much smoke got in, did the purifier help?

**Don't use for:** CO / radon / VOC removal (HEPA does nothing for gases —
activated carbon is a different mechanism; the tool says so explicitly),
industrial cleanrooms, or medical-grade isolation.

## Quick Start

```bash
# Size a purifier for a room (metric)
python3 scripts/clean_air.py size --area 20 --ceiling 2.7 --use smoke

# Same in imperial
python3 scripts/clean_air.py size --area 220 --height 9 --unit ft --use smoke

# Is my purifier enough? (rated 300 m³/h CADR)
python3 scripts/clean_air.py check --area 20 --ceiling 2.7 --use smoke --cadr 300

# DIY Corsi-Rosenthal box from a 20" box fan + 4 MERV-13 filters
python3 scripts/clean_air.py crbox --fan-cfm 1800 --filters 4

# Pollution diary
python3 scripts/clean_air.py log add --indoor 45 --outdoor 210 --note "smoke peak"
python3 scripts/clean_air.py log add --indoor 18 --outdoor 190 --purifier on
python3 scripts/clean_air.py log analyze

# Filter life
python3 scripts/clean_air.py filter new --name "Living HEPA" --rated-hours 2000
python3 scripts/clean_air.py filter tick --name "Living HEPA" --hours 8
python3 scripts/clean_air.py filter status
```

## The Physics in Brief

### CADR sizing

```
required CADR (m³/h) = room volume (m³) × target ACH
```

| Situation | Target ACH |
|---|---|
| Wildfire smoke event | 5 |
| Allergy season | 4–5 |
| General air quality | 2–3 |

(ACH conventions from smoke-readiness guidance: 5 ACH keeps PM2.5 at a
fraction of outdoor levels with windows closed; higher is better during
peaks.)

Buy 1.5–2× the computed CADR if you want to run at low speed (quiet,
overnight) — CADR on low is typically 20–35 % of the high-speed rating.

### Placement

- Central location beats a corner; the far corner of a large room can be
  under-served.
- Do NOT blow cleaned air out an open doorway; point the outlet into the
  room's main volume.
- During smoke events: close windows, run purifier continuously, set HVAC
  to recirculate (no outdoor air intake) if it has a MERV-11+ filter.

### DIY Corsi-Rosenthal box

A box fan (1500–2200 CFM free-flow) + 4–5 MERV-13 furnace filters as a
cube on the intake side. Measured by academic teams (Corsi, Rosenthal et
al., 2020–2022) at **600–900 CFM (1000–1500 m³/h) clean air delivery** —
beating most $400 commercial units for ~$60 of parts, at higher noise.

Pressure-drop rule of thumb: each MERV-13 filter adds resistance; effective
airflow ≈ free-flow CFM × 0.35–0.5 depending on filter count and fan curve.
More filter surface area (filters in parallel) = less resistance = more
flow.

### PM2.5 numbers that matter

| PM2.5 µg/m³ | Meaning |
|---|---|
| 0–12 | Good |
| 12–35 | Moderate (sensitive groups take care) |
| 35–55 | Unhealthy for sensitive groups |
| 55–150 | Unhealthy |
| 150–250 | Very unhealthy |
| 250+ | Hazardous |

Indoor/outdoor ratio with windows closed, no filtration: typically 0.5–0.8
of outdoor during heavy smoke. With adequate HEPA at 5 ACH in one sealed
room: 0.1–0.2.

### Filter life

HEPA media doesn't "clog" on schedule — it loads with dust. Rated hours
(500–3000 h) assume average dust. The tracker uses real run-hours and a
smoke-loading multiplier (each heavy smoke week counts ~3×) and schedules
replacement before pressure drop kills CADR.

## Common Pitfalls

1. **Trusting "for rooms up to X m²" on the box.** Those claims assume
   2 ACH or less — adequate for dust, NOT for smoke. Always recompute
   from CADR.
2. **Running on night mode during an event.** CADR on low can be 4× lower;
   the room never reaches steady state.
3. **One purifier for the whole apartment.** Clean the bedroom (smallest
   room, longest occupancy); keep the door closed; that's your clean-air
   room.
4. **Opening windows to "air out" during smoke.** This resets the room to
   outdoor levels; only ventilate when outdoor PM2.5 drops below indoor.
5. **Expecting HEPA to remove gases.** Smoke smell/VOCs need activated
   carbon; HEPA handles particles only.

## Verification Checklist

- [ ] size output CADR = volume × ACH exactly
- [ ] check output includes minutes-per-air-change and a clear verdict
- [ ] crbox effective CFM is 35–50 % of fan free-flow (sanity band)
- [ ] log analyze prints I/O ratio trend and event summary
- [ ] filter status shows % life used and change-due date

## Examples

```
$ python3 scripts/clean_air.py size --area 20 --ceiling 2.7 --use smoke
Room: 54 m³ (20 m² x 2.7 m)
Target: 5 ACH (wildfire smoke)
Required CADR: 270 m³/h  (~158 CFM)
  buy margin: 400 m³/h to allow quiet-speed operation

$ python3 scripts/clean_air.py check --area 20 --ceiling 2.7 --use smoke --cadr 300
Your purifier: 300 m³/h in 54 m³ room → 5.6 ACH → ADEQUATE for smoke
  full air change every ~11 minutes; run on HIGH during peaks.
```

Conventions from public smoke-readiness guidance (EPA Wildfire Smoke
Guide, AHAM CADR definitions) and peer-reviewed Corsi-Rosenthal box
measurements. Local conditions vary; use a PM2.5 monitor to verify.
