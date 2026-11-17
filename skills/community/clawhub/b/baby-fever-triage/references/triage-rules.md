# Triage Rules & Dosing Reference

This document is the reasoning backbone of the `fever.py` triage engine. Read it
once; the script exists so you never have to reconstruct this at 2 AM.

## Why an age-tiered system

Fever in a newborn is not the same disease as fever in a toddler. The younger the
child, the less the immune system localizes infection: a 4-week-old with a
urinary tract infection, bacteremia, or meningitis may show *nothing but fever*.
That single fact drives the hardest rule in pediatrics:

> **Any infant under 3 months with rectal temperature ≥ 38.0 °C (100.4 °F)
> requires same-day (ideally within the hour) medical evaluation — regardless of
> how well the baby looks.**

No home care, no watchful waiting, no "let's see what morning brings."

## The rule ladder (as implemented in `triage_core`)

| Priority | Condition | Verdict | Rule id |
|---|---|---|---|
| 1 | Core temp ≥ 41.0 °C at any age | EMERGENCY-NOW | `temp>=41` |
| 2 | Age < 3 m AND core ≥ 38.0 °C | EMERGENCY-NOW | `age<3m+38C` |
| 3 | Age < 3 m, no fever yet | SAME-DAY (any illness) | `age<3m-urgent-ish` |
| 4 | 3–6 m AND core ≥ 39.0 °C | SAME-DAY | `3-6m+39C` |
| 5 | 3–6 m, lower temp | HOME-CARE + recheck 24 h | `3-6m-home` |
| 6 | > 6 m AND child NOT responsive | EMERGENCY-NOW | `behavior` |
| 7 | > 6 m AND not drinking | SAME-DAY | `fluids` |
| 8 | > 6 m, responsive, drinking | HOME-CARE | `6m-5y-behavior` |

**Behavior beats numbers** above 6 months: an interactive, drinking child at
39.8 °C is usually less concerning than a listless one at 38.5 °C.

## Measurement routes and correction

Rectal is the reference standard under ~4 years. Other routes read low, so the
engine adds an offset to estimate core temperature before applying rules:

| Route | Adjustment added | Note |
|---|---|---|
| rectal | +0.0 °C | gold standard for the rules above |
| oral | +0.3 °C | affected by recent drinks |
| axillary (armpit) | +0.5 °C | least reliable; fine for trend |
| forehead/temporal | +0.3 °C | read per device instructions |

## The 14 red flags (any single YES = EMERGENCY-NOW)

1. **non-blanching rash** — press a clear glass against the rash; if it stays
   visible, treat as meningococcal until proven otherwise.
2. **inconsolable** — continuous high-pitched cry > 1 h, comforted by nothing.
3. **unresponsive** — hard to wake, limp/floppy.
4. **grunting** — grunting exhale = working to breathe.
5. **breathing-fast** — infant > 60/min, 1–4 y > 40/min, or ribs sucking in
   (retractions).
6. **blue-lips** — cyanosis of lips/tongue/face.
7. **seizure** — any convulsion; first febrile seizure always needs evaluation
   even if it stopped.
8. **bulging-fontanelle** — tensely bulging soft spot in an infant.
9. **neck-stiffness** — with photophobia (older children).
10. **dehydrated** — no tears, dry mucous membranes, no urine/wet diaper ≥ 8 h,
    sunken eyes/fontanelle.
11. **refusing-fluids** — or vomiting everything repeatedly.
12. **temperature-over-41** — ≥ 41 °C / 105.8 °F.
13. **fever-5-days** — duration alone forces an in-person exam (think
    Kawasaki, pneumonia, UTI).
14. **getting-worse** — recovery then relapse suggests secondary bacterial
    infection.

## Weight-based dosing math

```
dose_mg = mg_per_kg × weight_kg
volume_mL = dose_mg ÷ concentration_mg_per_mL
```

| Drug | mg/kg/dose | min interval | max doses/24 h | ceiling | min age |
|---|---|---|---|---|---|
| acetaminophen (paracetamol) | 10–15 | 4 h | 5 | 75 mg/kg/day | 1 m*, doctor-directed below 3 m |
| ibuprofen | 5–10 | 6 h | 4 | 40 mg/kg/day | 6 m |

\* Neonates (0–28 days): **never dose at home** — fever there is an emergency
workup, and acetaminophen kinetics are different.

### The concentration trap

The same "5 mL" can deliver anywhere from 120 mg to 500 mg depending on product:

| Product | Concentration |
|---|---|
| US infant drops | 160 mg per 5 mL (32 mg/mL) |
| US children's syrup | 160 mg per 5 mL |
| EU drops (e.g., Efferalgan bébé) | 100 mg/mL |
| EU/RU syrup 120 mg/5 mL | 24 mg/mL |
| EU/RU suspension 250 mg/5 mL | 50 mg/mL |
| Ibuprofen suspension 100 mg/5 mL | 20 mg/mL |
| Ibuprofen suspension 200 mg/5 mL | 40 mg/mL |

This is why `fever.py dose` **refuses to print mL without `--conc`**. Always
read the physical bottle in front of you.

## Alternating therapy (only if a clinician approved it)

The safe pattern: each drug keeps its own clock, staggered so something is
actionable roughly every 2 h:

- acetaminophen at 22:00, 02:00, 06:00, 10:00 … (≥ 4 h apart)
- ibuprofen at 01:00, 07:00, 13:00 … (≥ 6 h apart)

Track the *actual* doses given with `fever.py log med` — memory at 4 AM is not a
dosage safety system. The evidence on whether alternating is better than
single-drug therapy is mixed; the risk is dosing error, which the log and
scheduler are designed to prevent.

## What NOT to do

- No aspirin, ever, in children with fever (Reye's syndrome).
- No cold-water sponging or alcohol rubs (shivering, absorption).
- No bundling a hot child "to sweat it out".
- No waking a sleeping child solely to give a dose — sleep is medicine too
  (exception: doctor-directed schedule).
- No dosing "extra-strength" adult formulations for children.

## Scope and honest limits

- Designed for ages 0–5 years, previously healthy children.
- Immunocompromised, chemo, sickle-cell, no-spleen, recent surgery, chronic
  illness: call their specialist — thresholds are different and lower.
- This tool structures published pediatric guidance; it cannot examine your
  child. When its output and your instinct disagree, the doctor wins.
