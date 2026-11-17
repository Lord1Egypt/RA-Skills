---
name: bp-log-sentinel
description: "Use when someone logs home blood-pressure readings and asks what they mean, whether their BP is high, if they should see a doctor, or whether the doctor's office reading disagrees with home readings — computes the AHA 7-day home average, categorizes against ACC/AHA 2017 + ESC/ESH 2023 thresholds, detects white-coat and masked-hypertension patterns, flags measurement-technique errors, and renders a physician-ready summary."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [blood-pressure, hypertension, health-monitoring, cardiovascular, log-analysis]
---

# BP Log Sentinel

## Overview
Home BP monitors are everywhere; correct interpretation of the log is not. People make three
systematic mistakes: (1) reacting to single readings instead of averages, (2) comparing home
numbers to **office** thresholds (home runs 3-5 mmHg lower, so home 135/85 ≈ office 140/90),
and (3) measuring badly — caffeine, full bladder, talking, crossed legs each add 5-10 mmHg,
which is an entire diagnostic category.

This skill turns a raw CSV log into a consult-grade analysis: the AHA home-monitoring average
(discard day 1, mean of days 2-7, morning + evening), category per ACC/AHA 2017 and ESC/ESH
home thresholds, white-coat vs masked-hypertension pattern when a clinic reading is supplied,
contaminated-reading flags from free-text notes, crisis-range escalation, and a doctor-ready
summary paragraph.

## When to Use
- "I've been logging my BP for a week — is this high?"
- "My home readings are 135/85 but at the doctor's it was 150/95 — which is real?"
- "My monitor says 138/88 every morning. Do I have hypertension?"
- "Should I be worried about this one 180/120 reading?"
- Preparing evidence for a doctor's appointment from a home log.
- Any CSV/list of date+time+sys/dia readings needing interpretation.

**Don't use for:** stroke/heart-attack symptoms, hypertensive crisis with symptoms (→ emergency
services immediately), titrating medication doses (physician's job), or ambulatory 24-h monitor
interpretation (different protocol).

## How It Works — Numbered Steps
1. Get the log into CSV: `date,time,systolic,diastolic,pulse` (+ optional `notes` — free text is
   scanned for technique contaminants like coffee/talking/legs crossed).
2. Run: `python3 scripts/bp_sentinel.py analyze readings.csv --clinic 150/95`
   (`--clinic` optional, enables white-coat/masked detection; `--window 7` truncates the log;
   `--keep-day1` overrides the AHA day-1 discard).
3. Read the HOME AVERAGE line — this, not any single reading, is the diagnostic quantity.
4. Check MEASUREMENT-ERROR FLAGS: contaminated readings still count, but a clean re-log is
   recommended before believing a borderline category.
5. If CLINIC COMPARISON is present, read the pattern verdict (white-coat / masked / sustained).
6. Escalate per NEXT STEPS: any ≥180/120 with symptoms = emergency care now.

## The Numbers That Matter

| Quantity | Threshold | Meaning |
|---|---|---|
| Home average (day 2-7) | <120/80 | Normal |
| | 120-129/<80 | Elevated |
| | ≥135/85 (home trigger) | Hypertensive territory (≈ office 140/90) |
| | ≥150/95 (home) | Stage 2 territory |
| Single reading | ≥180/120 | Crisis range — with symptoms, emergency |

Risk framing: each 20/10 mmHg rise roughly doubles cardiovascular mortality risk — why category
boundaries matter and why single readings don't.

## Common Pitfalls
1. **Reading the monitor's built-in average.** Device averages include day 1 (anxiety-inflated)
   and don't follow the morning/evening protocol; the AHA day-2-7 average is the reference.
2. **Applying office thresholds to home numbers.** Home BP runs lower; a home 135/85 is already
   equivalent to office 140/90. The tool applies home triggers.
3. **Wrist/cuff-position errors.** Wrist monitors must be at heart level; an unsupported arm
   below heart level adds up to 10 mmHg.
4. **Judging by the highest reading.** Trends and averages diagnose; spikes (unless ≥180/120
   with symptoms) are usually technique or noise.
5. **Ignoring white-coat/masked patterns.** Clinic-only or home-only evidence alone misses both;
   the pattern needs both numbers, which is why `--clinic` exists.
6. **Stopping the log after diagnosis starts.** Home monitoring also guides treatment — keep
   logging monthly weeks.
7. **Wrong cuff size.** A too-small cuff overreads by 5-15 mmHg — measure arm circumference
   once and buy accordingly.

## Example
```
User: "Doctor's office said 128/82, but my home cuff shows ~135/86 every
evening for a week. One night it hit 184/122."

$ python3 scripts/bp_sentinel.py analyze week.csv --clinic 128/82
HOME AVERAGE: 139/89 mmHg  (12 readings over 6 days, day 1 discarded)
CATEGORY: Stage 1 hypertension (home average)
CLINIC COMPARISON: clinic 128/82 vs home 139/89
  MASKED HYPERTENSION: home high, clinic normal
  -> carries risk close to sustained hypertension; this log is exactly
     the evidence your physician needs.
!! 1 reading ≥180/120 (crisis range): 2026-10-02 20:14 — with symptoms,
   emergency care NOW.

Answer: this is a classic masked pattern — the office reading under-detected
it. Print the report and book an appointment; treat the 184/122 night as an
escalation signal if it recurs with symptoms.
```

## Safety Note
Information tool, not a diagnosis; diagnosis requires a clinician confirming with proper
technique. Thresholds: ACC/AHA 2017 guideline, ESC/ESH 2023 home-monitoring guidance. Symptoms
(chest pain, breathlessness, neuro deficits, vision change) + high reading = emergency services.

## References
- `references/measurement-protocol.md` — the 10-rule AHA measurement procedure, why each rule
  shifts numbers, and the correct 7-day logging schedule.
- `references/interpretation.md` — threshold tables (office vs home vs ambulatory), white-coat
  and masked hypertension epidemiology and prognosis, and how physicians use home logs.
