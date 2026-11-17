# Dryer Vent Fire Guard

**Do towels need two cycles? That's not "the dryer getting old" — that's a fire risk audit you haven't done yet.**

Clothes dryers start ~13,000–15,500 reported house fires per year (US), and about a third trace to a lint-choked vent. The progression is silent: lint builds in the duct for years → airflow drops → loads take 90 minutes instead of 45 → the element runs hotter longer → the baked lint (an excellent fuel) ignites. Every household already has the two diagnostic signals — **dry time** and **what's behind the dryer** — but nobody knows what to do with them.

## What this skill does

- **Dry-time test bands**: time a standard towel load → HEALTHY / WATCH / RESTRICTED / SEVERE.
- **Code audit**: enter the vent run (material, length, elbows, diameter) → equivalent length vs the IRC 35-ft allowance, with foil/vinyl violations flagged.
- **Risk stacking**: vertical rises, screen hoods, indoor venting, nests, overdue cleaning — each with its WHY.
- **Action ladder**: clean-now protocol → duct replacement → reroute math (every elbow removed buys back 5 ft) → termination fixes.
- **Recurrence**: annual vs semi-annual cleaning cadence from your laundry volume, plus the wasted-energy price of ignoring it (~$40–100/yr in extra cycles alone).

## Quick start

```bash
# Built-in severe demo: foil flex, 4 elbows, 75-minute loads, never cleaned
python3 scripts/dryer_vent_audit.py --demo

# Your vent: rigid metal, 18 ft, 2 elbows, loads dry in 48 min
python3 scripts/dryer_vent_audit.py --material rigid --length-ft 18 --elbows 2 \
    --diameter-in 4 --dry-minutes 48 --loads-per-week 8
```

## Why it matters

- A plugged vent is the one home hazard that advertises itself (slow drying) and still gets ignored for years.
- Cleaning costs $0–200; a dryer fire averages five figures in damage — and they cluster in winter, with the machine running unattended.
- Dry-time creep also quietly doubles your energy per load: the audit prices that in the verdict.

## What's inside

```
SKILL.md                             trigger conditions, verdict bands, action ladder, pitfalls
references/vent-code-and-fire-model.md   IRC code tables, fire mechanism, inspection walkthrough
scripts/dryer_vent_audit.py          the audit engine (stdlib-only Python, offline)
```

## Scope & honesty

Verdicts are code-geometry + symptom based, not a substitute for physically inspecting/cleaning the run. A dying heating element can also slow drying — the reference includes the air-fluff disambiguation test. Fire statistics: USFA/CPSC.
