---
name: furnace-panic-doctor
description: "Use when the heat is out or acting up - no heat, weak heat, short cycling, weird noises, pilot out, error codes. Runs a 10-minute no-tools diagnostic tree, separates DIY-fixable from call-a-pro causes, documents everything for the technician, and knows the safety lines that mean stop now."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [furnace, heating, hvac, home-repair, no-heat, troubleshooting, emergency]
---

# Furnace Panic Doctor

## Overview

The furnace dies at 2 AM in January. Panic. Cold house, kids asleep, unknown
repair bill. Homeowners either (a) call emergency service immediately —
$300 trip fee for a problem that was a $0 filter change, or (b) freeze until
morning with a problem that was actually dangerous (cracked heat exchanger
symptoms are not a filter problem).

This skill is the calm voice in the middle of the night: a **10-minute,
no-tools diagnostic tree** that ends in one of three verdicts:

1. **DIY-FIX** — exact steps (filter, thermostat batteries, pilot relight,
   breaker, exhaust vent blockage, drain line)
2. **PRO-CALL** — what's broken, what it likely costs, what to say on the
   phone, and whether "emergency" pricing is warranted
3. **STOP-NOW** — safety lines (soot at registers, sulfur smell, CO alarms,
   burning electrical smell, fuel odors): shut down per the script and
   act on the danger, not the comfort

It also produces a **technician briefing sheet** — symptoms, what you
checked, model/serial, timeline. Techs fix documented problems faster and
charge less diagnostic time.

## When to Use

- "Furnace/heater/boiler not working" — any fuel, any brand
- Weak or uneven heat, blower runs constantly, short cycling
- Thermostat blank or unresponsive
- Pilot light out / won't stay lit (gas)
- Error codes on the control board (LED blink patterns)
- Burning smell when heat starts (dust vs. electrical vs. worse)
- Loud noises: scraping, bang-boom on ignition, screech
- Water around the furnace / AC coil
- "Is this dangerous or just cold?" — the safety triage question

**Don't use for:** heat pumps in cooling-mode problems, active fire/gas
emergency (call the gas utility's emergency line — script covers this),
boilers with leaking pressure relief valves spraying water (shut off feed,
call plumber). If any CO alarm sounds: everyone out, then 911/gas utility —
no diagnostics.

## The diagnostic tree (summary)

Full script in `references/diagnostic-tree.md`; flow:

```
SAFETY TRIAGE (30 seconds)
  CO alarm / sulfur / fuel smell / smoke → STOP-NOW script
  → otherwise ↓
THERMOSTAT (2 min): blank? batteries? set HEAT+AUTO, fan ON, target 5° above
  room. Did it click?
POWER (2 min): furnace switch ON? breaker? door safety switch engaged?
  (blower test: fan ON at thermostat)
FUEL (2 min): gas valve handle parallel to pipe? pilot lit / hot-surface
  igniter glowing? oil tank level? propane %?
AIRFLOW (2 min): filter (2-inch dust ring = culprit #1), registers open,
  exhaust vent exterior clear (snow/bird nest), condensate drain flowing
OBSERVE ONE CYCLE (3 min): ignition → flame (blue, steady, all burners)
  → blower starts within ~1 min → warm air at nearest register
  → cycle length 5-15 min → quiet shutdown
  Anything else → symptom table match
SYMPTOM TABLE: short-cycling / no-ignition / ignites-then-dies / blows-cold /
  noise-X / smell-Y / water / error-code-N → cause list with DIY flags
VERDICT: DIY-FIX steps | PRO-CALL brief | STOP-NOW script
```

## Files

| File | Purpose |
|---|---|
| `scripts/furnace_check.py` | Interactive diagnostic: questions → verdict → steps → technician brief |
| `references/diagnostic-tree.md` | The full tree with all branch detail |
| `references/symptom-table.md` | 25+ symptoms → ranked causes → DIY or PRO, cost bands |
| `references/manuals-and-codes.md` | Where to find model/serial plates; common error-code families |
| `README.md` | The 2 AM problem |

## Usage

```bash
# The night it happens: interactive walk-through
python3 scripts/furnace_check.py

# Jump straight to a symptom
python3 scripts/furnace_check.py --symptom "short cycling"

# Non-interactive verdict from flags you already checked
python3 scripts/furnace_check.py --no-heat --filter-clean --pilot-lit

# Print a technician briefing for what you've ruled out
python3 scripts/furnace_check.py --symptom "blows cold" --brief
```

## Workflow

1. Ask the safety-triage questions FIRST (script does this automatically).
   Any STOP-NOW hit: execute that script (shut fuel/electric per manual,
   evacuate for CO, utility emergency numbers), nothing else matters.
2. Run the interactive tree — it asks one question at a time, with photos
   described in words ("handle parallel to the pipe = OPEN").
3. Reach a verdict. DIY-FIX: follow numbered steps exactly; skip "seems
   similar" shortcuts. PRO-CALL: generate the brief, make normal-hours
   call if the house is safe and pipes won't freeze (see threshold calc).
4. Freeze protection while you wait: run the pipe-protection math
   (script's `--freeze-risk` helper): house temp drop rate, which faucets
   to drip, when to drain if truly cold.
5. After the fix: log what it was (`--log`) — next failure starts from
   history, not zero.

## Common Pitfalls

1. **Relighting a pilot repeatedly.** A pilot that won't STAY lit is a
   thermocouple (cheap PRO fix) or a drafting problem — not a match
   problem. Three attempts max, then stop (gas accumulation risk).
2. **"Closed" vents save money myth.** Closing registers restricts airflow,
   overheats the exchanger, trips high-limit → short cycling that looks
   like a control failure. Open them.
3. **Filter direction matters.** Arrow on the frame = airflow direction,
   toward the blower. Backwards filters flap, whistle, and shed dust.
4. **The furnace switch looks like a light switch.** Someone flipped it
   thinking it was lights. It's the #2 no-heat cause after filters.
5. **Testing right after a fix.** Furnaces lock out for 1-3 failed ignition
   attempts; power-cycle at the switch (30 s off) before declaring failure.
6. **Space heaters as the plan.** Fine for one room overnight; not a
   whole-house strategy. Do the freeze-risk math instead of hoping.
7. **CO "nuisance alarm" assumption.** It's never a nuisance until a
   professional says so. Ageing alarms false-alarm at LOW levels — treat
   every alarm as real, get out, test doesn't continue until cleared.

## Example Session

> 2 AM, gas furnace, no heat, house 15°C and dropping. Run script:
> thermostat OK → switch OK → breaker OK → blower runs on FAN-ON (motor
> alive) → no ignition glow, no flame → filter filthy BUT that's airflow
> not ignition... symptom table: no-ignition + blower-OK → igniter or
> flame sensor. DIY: sand flame sensor with dollar bill? — modern call:
> NO (see pitfalls). Verdict: PRO-CALL, likely flame-sensor clean/replace,
> $150-350 normal hours. Freeze math: house loses 1.2°C/h → 8 h to
> pipe-risk threshold at -8°C outside → safe to wait for morning; drip
> the faucet furthest from the heater. Brief printed with model plate
> location noted.

## Verification Checklist

- [ ] Safety triage completed before ANY diagnostic step
- [ ] Verdict names the most likely cause(s), not just "call someone"
- [ ] DIY steps tried in order, one at a time, furnace power-cycled between
- [ ] Freeze-protection math done if waiting until morning
- [ ] Technician brief has: symptoms, checks done, model/serial, timeline
