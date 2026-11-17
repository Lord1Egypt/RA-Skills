---
name: baby-fever-triage
description: "Use when a baby or small child has a fever at 2 AM and the parents must decide: ER now, doctor in the morning, or watch-and-wait at home. Age-aware triage rules (0-3 months = automatic urgent), red-flag symptom checks, correct weight-based acetaminophen/paracetamol and ibuprofen dosing by weight (never by age), alternating-dose scheduler with safe intervals, temperature-trend log, and a structured handoff summary to bring to the pediatrician. Informational support, not a doctor — but it prevents the two most common and dangerous mistakes: under-dosing a suffering child and over-dosing by accident."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [fever, pediatrics, triage, dosing, infant-health, parenting, first-aid]
---

# Baby Fever Triage — 2 AM Decision Support

## Overview

A feverish child at night is one of the highest-anxiety moments in parenting. The two failure modes are symmetrical and both dangerous:

1. **Under-reacting** — a 5-week-old with 38.2°C and no other signs. Under 3 months, fever is an automatic medical urgency because newborns can have serious bacterial infections with no localizing signs. Parents who don't know this "wait until morning" — and that wait is genuinely dangerous.
2. **Over-dosing** — a suffering 8 kg one-year-old. "Give 5 mL of the infant drops" — but infant drops are concentrated (100 mg/mL) and the same 5 mL that's correct for syrup (160 mg/5mL) is a **double-to-triple overdose**. Confusion between concentrations is a leading cause of pediatric acetaminophen poisoning.

This skill is a calm, structured decision-support tool for exactly that moment:

- **Age-aware triage** — hard-coded rules: under 3 months + ≥38°C = urgent now; 3-6 months + ≥39°C = same-day; older + responsive + drinking = usually home care with checks.
- **Red-flag checklist** — 14 symptoms that escalate any fever regardless of age or height of fever (non-blanching rash, grunting breathing, inability to wake, first febrile seizure, etc.).
- **Weight-based dosing calculator** — mg per kg by actual weight, cross-checked against the product you actually have (infant drops vs children's syrup vs adult tablets), with mL amounts per concentration and a hard error if the concentration is unknown.
- **Alternating-dose scheduler** — if a pediatrician approved alternating acetaminophen and ibuprofen, generate the exact safe timeline (≥4h between same-drug doses for acetaminophen, ≥6h for ibuprofen, max doses/day enforced).
- **Fever log** — timestamped temperature route (rectal/axillary/forehead), meds given, fluid intake, behavior — becomes the pediatrician handoff sheet.
- **Handoff summary** — a compact structured summary that makes the doctor visit 10x more productive.

**This skill is informational support and does not replace medical judgment. When rules and your gut disagree, the doctor wins.**

## When to Use

- A child 0-5 years has a measured fever and parents are deciding what to do
- Calculating a correct weight-based dose of acetaminophen (paracetamol) or ibuprofen
- Planning alternating doses through the night without interval errors
- Logging a fever illness course for the pediatrician visit
- Don't use for: adult fever (different rules), fever lasting >5 days in any child (needs in-person exam regardless of how well the child looks), chronic conditions / immunocompromised children ( thresholds differ — call their specialist), or as a replacement for calling emergency services when red flags are present.

## How It Works

1. **Triage** — `python3 scripts/fever.py triage --age-months 7 --temp 39.1 --unit c` returns an urgency tier (EMERGENCY-NOW / SAME-DAY / HOME-CARE) with the exact reason string and the age rule that fired.
2. **Red flags** — `flags` interactively walks the 14-item checklist; any yes escalates to the top of the flow.
3. **Dose** — `dose --drug acetaminophen --weight-kg 8.2 --conc mg-per-ml:100` → mg dose, mL for the actual product, next-allowed time, max/day. Refuses to compute without concentration.
4. **Scheduler** — `schedule --weight-kg 8.2 --start "2026-09-27 02:00" --hours 12 --drugs both` prints a per-half-hour timeline of what's allowed when, enforcing both per-drug intervals AND the stagger.
5. **Log** — `log temp 38.4 --route axillary` / `log med acetaminophen 120mg --at ...` builds the illness record; `log show` prints the course.
6. **Handoff** — `handoff` renders the doctor-ready summary: age, course, peak temps, red flags checked, meds given with times, fluid intake, questions to ask.

All state in a single `fever.json` in cwd (or `--db`); fully local — health data should never leave the house.

## Dosing Reference (memorize the shape, verify the amount)

| Age group | Acetaminophen (mg/kg/dose) | Ibuprofen (mg/kg/dose) | Notes |
|---|---|---|---|
| 0-28 days | **call doctor, do not dose at home** | never | fever here is an emergency workup |
| 1-3 months | only if doctor directed | never | 10-15 mg/kg/dose when directed |
| 3-36 months | 10-15 mg/kg/dose | 5-10 mg/kg/dose | ibuprofen only ≥6 months |
| 3-12 years | 10-15 mg/kg/dose | 5-10 mg/kg/dose | max 4-5 doses/day acetaminophen |
| Any | max 75 mg/kg/day acetaminophen; 40 mg/kg/day ibuprofen | | hard ceilings |

Common concentrations: infant drops 80mg/0.8mL & 160mg/5mL syrups (US), 100 mg/mL and 120mg/5mL (EU/RU: эфералган/панадол-беби), 250mg/5mL suspension. **Never compute a mL dose without reading the bottle.**

## Commands

```bash
# Triage by age and temperature
python3 scripts/fever.py triage --age-months 5 --temp 39.4 --unit c
# → SAME-DAY: 3-6 months with ≥39°C needs to be seen today

# Red-flag checklist (non-interactive: pass flags directly)
python3 scripts/fever.py flags --non-blanching-rash no --inconsolable yes ...
# any yes → EMERGENCY-NOW

# Weight-based dose with the actual product
python3 scripts/fever.py dose --drug ibuprofen --weight-kg 11.5 --conc mg-per-ml:20
# → 87-115 mg → 4.3-5.8 mL of the 20mg/mL suspension, next dose no sooner than 6h

# Night alternating scheduler
python3 scripts/fever.py schedule --weight-kg 8.2 --start "2026-09-27 22:00" --hours 14 --drugs both
# prints timeline: 22:00 A, 02:00 I, 06:00 A, 10:00 I ... intervals verified

# Illness log
python3 scripts/fever.py log temp 38.9 --route rectal
python3 scripts/fever.py log med acetaminophen 123mg --at "2026-09-27 23:15"
python3 scripts/fever.py log fluids 60ml
python3 scripts/fever.py handoff
```

## Common Pitfalls

1. **Dosing by age instead of weight.** Two-year-olds vary from 10 to 17 kg; the age-bands on the box are a marketing convenience. Always weigh or use a recent clinic weight.
2. **Mixing up concentrations.** 80mg/0.8mL drops vs 160mg/5mL syrup vs 100mg/mL EU drops: the same "5 mL" spans 160 mg to 500 mg. This skill refuses a mL answer without `--conc`.
3. **Treating the thermometer, not the child.** A responsive, drinking 18-month-old at 39.5°C needs comfort and observation; a listless 39.0°C child needs a doctor. Behavior > number.
4. **Sponging with cold water / alcohol rubs.** Old advice, now harmful — causes shivering and raises core temp, alcohol absorbed through skin. Skip it.
5. **Alternating drugs on a fuzzy memory.** At 4 AM nobody remembers the 02:00 dose. The scheduler prints the timeline; the log records what was actually given.
6. **Assuming fever alone is the enemy.** Fever is an immune response; the danger signs are behavior, hydration, breathing, rash. A well-appearing child with fever needs comfort, not war.
7. **Forgetting the under-3-months rule.** No home care, no watchful waiting: any ≥38°C in this age group is same-day medical evaluation, ideally within an hour.
8. **Using this skill instead of calling for help.** Triage rules are conservative, but if parental instinct says emergency, the skill's "HOME-CARE" verdict loses to that instinct.

## Verification Checklist

- [ ] `triage` returns one of EMERGENCY-NOW / SAME-DAY / HOME-CARE with a reason and age-rule citation
- [ ] Under-3-month rule fires automatically and cannot be overridden by "looks fine"
- [ ] `dose` refuses to output mL without a concentration; mg/kg math verified against the table
- [ ] `schedule` never places two of the same drug <4h (acetaminophen) or <6h (ibuprofen) apart, and enforces daily maxima
- [ ] `handoff` output contains course timeline, red flags checked, med times, and is readable in <60 seconds
- [ ] Disclaimers present in SKILL.md, script output, and handoff: informational, not a doctor

## References

- `references/triage-rules.md` — full rule sources, exception cases, escalation criteria, and when NOT to use this skill
