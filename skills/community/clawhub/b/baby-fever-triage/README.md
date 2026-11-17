# Baby Fever Triage

**2 AM. Feverish baby. One question: ER now, doctor in the morning, or home care?**

A calm decision-support tool for the highest-anxiety moment in parenting. It
runs the two checks that matter — age-aware triage and weight-based dosing —
and refuses to guess where guessing is dangerous.

## The problem

Parents facing a feverish child at night make two symmetrical, dangerous mistakes:

1. **Under-reacting.** A 5-week-old at 38.2 °C looks fine — drinks, sleeps. But
   under 3 months, fever can be the *only* sign of serious bacterial infection.
   "Wait until morning" is the single most dangerous choice in this scenario.
2. **Over-dosing.** An 8 kg one-year-old gets "5 mL of the drops." Infant drops
   are concentrated: the same 5 mL that is correct for syrup is a 2–3×
   overdose. Concentration confusion is a leading cause of pediatric
   acetaminophen poisoning.

Both mistakes come from doing math and risk-assessment while exhausted and
terrified. This skill does the math and holds the rules steady.

## What it does

| Command | What you get |
|---|---|
| `triage` | EMERGENCY-NOW / SAME-DAY / HOME-CARE verdict + the exact rule that fired |
| `flags` | 14-item red-flag checklist (non-blanching rash, grunting, unresponsive…) — any YES = emergency |
| `dose` | mg/kg by weight, mL **only** if you pass the actual bottle concentration |
| `schedule` | alternating acetaminophen/ibuprofen timeline, intervals verified |
| `log` / `handoff` | illness course → one-page pediatrician summary |

## Quick start

```bash
# 1. Triage: 7 months old, 39.1°C
python3 scripts/fever.py triage --age-months 7 --temp 39.1 --unit c

# 2. Red flags (any yes = emergency)
python3 scripts/fever.py flags --inconsolable no --non-blanching-rash no

# 3. Dose for 8.2 kg child with EU 100mg/mL drops
python3 scripts/fever.py dose --drug acetaminophen --weight-kg 8.2 --conc mg-per-ml:100

# 4. Overnight alternating plan
python3 scripts/fever.py schedule --weight-kg 8.2 --start "22:00 tonight" --hours 12

# 5. Track and hand off
python3 scripts/fever.py log temp 38.9 --route rectal
python3 scripts/fever.py handoff
```

## Safety design

- **Refuses mL without concentration** — the #1 overdose vector is closed.
- **Under-3-months rule cannot be overridden** by "looks fine."
- **Ibuprofen blocked under 6 months.**
- 100% local (one `fever.json`), disclaimers on every output.

## Honest limits

Informational support, not a doctor. Built for previously-healthy children
0–5 y. Immunocompromised or chronically ill children have different thresholds —
call their specialist. If your gut says emergency, your gut wins over this tool.

MIT License. © 2026 Denis Voronin
