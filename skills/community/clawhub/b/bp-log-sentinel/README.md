# BP Log Sentinel

**You logged your blood pressure for a week. Now what does it mean?**

Home BP monitors are everywhere; correct interpretation is not. People panic over single
readings, compare home numbers against office thresholds, and never realize their technique
(coffee, full bladder, talking) is adding a whole diagnostic category of pressure. And the
doctor's office can miss real hypertension entirely — masked hypertension reads normal in the
calm clinic and high at home.

## What it does

- **AHA 7-day home average** — discards day 1 (anxiety-inflated), averages days 2-7,
  morning + evening, with standard deviation.
- **Category verdict** against ACC/AHA 2017 and ESC/ESH home thresholds (home ≥135/85 ≈ office
  140/90 — the detail everyone gets wrong).
- **White-coat vs masked-hypertension detection** when you supply the clinic reading.
- **Technique-error flags** — scans free-text notes for coffee/talking/full bladder/crossed
  legs and friends; each adds 5-15 mmHg.
- **Crisis escalation** — any ≥180/120 reading called out with symptom guidance.
- **Physician-ready report** — averaging method, average ± SD, pattern, next steps.

## Quick start

```bash
python3 scripts/bp_sentinel.py demo                      # see a full worked example
python3 scripts/bp_sentinel.py analyze readings.csv --clinic 128/82
```

CSV header: `date,time,systolic,diastolic,pulse[,notes]` — the notes column powers the
technique-error detector.

## Real-world problem it solves

A user's cuff shows ~135/86 every evening for a week; at the doctor's it read 128/82, so they
were told "fine". Running the log: home average 139/89, **masked hypertension pattern** — which
carries risk close to sustained hypertension. One evening spike hit 184/122, flagged as crisis
range with symptom guidance. The printed report is exactly what the physician needs to act on
instead of dismissing.

## Scope & limits

Adults, information tool, not a diagnosis — a clinician confirms with proper technique.
Not for pregnancy, children, or symptomatic emergencies (call emergency services). Pure Python
3 stdlib, no dependencies. MIT license.
