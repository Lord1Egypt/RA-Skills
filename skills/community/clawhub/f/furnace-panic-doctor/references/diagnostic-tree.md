# The Full Diagnostic Tree

Branch-by-branch detail for the 10-minute no-tools check. Numbers and
timing marks come from common service literature; your unit's manual
overrides anything here.

## 0. Safety triage (30 seconds — always first)

| Signal | Meaning | Action |
|---|---|---|
| CO alarm sounding | carbon monoxide | Everyone out → 911/utility from outside. No re-entry until cleared. |
| Rotten-egg / sulfur smell | gas leak (odorant) | Leave. No switches. Gas utility emergency line from outside. |
| Fuel-oil smell | oil leak / delayed ignition | Switch off if safe, ventilate, oil service emergency. |
| Soot around registers or on furnace | combustion problem, possible cracked exchanger | OFF. Emergency HVAC. CO risk. |
| Sharp acrid burning-plastic smell | electrical insulation melting | OFF at switch + breaker. Emergency electrician/HVAC. |
| Smoke | fire risk | OFF, fire department if visible flame/smoke persists. |

If none: proceed. Keep a CO alarm with fresh battery near sleeping areas
regardless — this is the non-negotiable of heating season.

## 1. Thermostat (2 min)

- Blank display → batteries (AA/AAA on most) or common-wire power.
- Set: MODE=HEAT, FAN=AUTO, target = room + 5°C.
- Listen for the tiny relay click ~5 s after raising target.
  - Click + nothing at furnace: go to POWER/FUEL.
  - No click: thermostat or its wiring. Jump R↔W at the thermostat base
    (paperclip, 5 s — old-school but definitive) — heat starts = replace
    thermostat ($25-150 DIY). Nothing = furnace-side.
- Smart thermostat: check "equipment offline"/power-stealer cycling logs.

## 2. Power (2 min)

- The furnace switch: looks like a light switch on/near the unit. UP.
- Breaker panel: FURNACE / AIR HANDLER / HEATER — reset once if tripped.
  Trips AGAIN immediately = short — stop, PRO with electrical note.
- Blower sanity check: thermostat FAN=ON. Blower runs = 120V + motor OK.
- Door safety switch: burner door must be fully seated (pushes a plunger).

## 3. Fuel (2 min)

- **Natural gas**: valve handle parallel to pipe = OPEN. If it was closed:
  open SLOWLY (quarter-turn per second) to avoid regulator slam.
- **Pilot (standing pilot units)**: follow the door-label relight
  procedure exactly (usually: knob→PILOT, push+hold, light, hold 30-60 s,
  release, knob→ON). Won't stay lit after 3 tries = thermocouple or draft
  — PRO. Do NOT keep striking matches into an accumulating gas cloud.
- **Hot-surface igniter (HSI)**: watch through the window: orange glow
  before each ignition attempt. No glow = igniter or board.
- **Intermittent spark (ISU)**: rapid clicking = spark working; no flame =
  gas supply or flame sense.
- **Oil**: tank gauge > 1/8? Filter/sieve clog at tank? Reset button on
  burner primary control — ONCE. Repeated trips = clogged nozzle/strainer —
  PRO (and do not run dry: bleed is a tech job).
- **Propane**: gauge %, and remember pilots die first when tank is low.

## 4. Airflow (2 min)

- **Filter**: the #1 cause of everything. Pull it: no light through it =
  replace. Write the date on the new one. Arrow points toward the blower.
- Registers: open in all rooms, furniture not blocking returns (the BIG
  grilles — a blocked return starves the system worse than closed supplies).
- Exhaust vent termination outdoors (white PVC on high-eff; metal on 80%):
  snow drift, bird nest, frost plug. Clear by hand.
- Intake pipe (second PVC): same check. Blocked intake = pressure switch
  trip = no ignition that looks electrical.
- Condensate (high-eff): drain line/pump flowing? A wet-vac on the drain
  outlet clears most clogs. Float switch trips shut the furnace down when
  the pan fills.

## 5. Observe one full cycle (3 min)

Raise target 3-5°C. Watch + listen + time:

| Phase | Normal | Red flag |
|---|---|---|
| Draft inducer | small fan starts first | hum but no rotation (frozen/bad) |
| Ignition | HSI glow ~20-40 s, or spark, or pilot | click-click-click no light |
| Flame | blue, steady, all burners, soft roar | yellow tips dancing, one burner not lit, flame rolling out |
| Blower | starts 30-90 s after flame | never starts / scrapes / squeals |
| Register air | noticeably warm in 2-3 min | cool air > 5 min |
| Cycle | 5-15 min then quiet stop | stops in <3 min (short cycle) or runs forever |
| Shutdown | flame off, blower runs 1-2 min more | blower dies with flame instantly |

## 6. Symptom table cross-reference

Take the strongest observation to `symptom-table.md` for ranked causes,
DIY/pro flags, and cost bands.

## 7. Verdicts

- **DIY-FIX**: do the numbered fix, power-cycle the switch (30 s off),
  re-test ONE cycle. Fixed? Log it. Not fixed → next cause, or PRO.
- **PRO-CALL**: run `--brief`, photograph the model/serial plate (inside
  the burner door), decide emergency vs. business-hours with the
  freeze-risk math (`--freeze-risk`).
- **STOP-NOW**: execute the safety script. The comfort problem is now a
  safety incident; treat it as one.

## 8. The freeze-risk math (waiting safely)

A rough house loses heat at `(T_in − T_out)/K` per hour, K ≈ 8 with normal
internal gains (people, fridge, standby power); wind, poor insulation, or
open rooms can halve K.

- Projected ≥ 12°C when help arrives: wait comfortably, normal hours.
- 7-12°C: drip the farthest cold faucet, close unused rooms, re-check
  hourly.
- < 7°C: open cabinets under exterior-wall sinks, keep one room ≥ 15°C
  with a safe heater, and if it will pass below ~4-5°C: shut the main
  water valve and drain the lowest faucet. Frozen-and-burst beats cold
  by an order of magnitude in damage.

## 9. Prevention calendar (after the crisis)

- Filter: 1-3 months (1" pleated), 6-12 months (4-5" media)
- Professional tune-up: annually, BEFORE the season (September-October —
  techs are 30-50% cheaper and available)
- CO alarm: replace every 5-7 years, test monthly in season
- Exhaust/intake terminations: check after every big snow/ice storm
- Keep 3 correct-size filters in the house — the 2 AM store run is real
