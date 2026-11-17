# Metrics — Glucose, Ketones, GKI

Readings get reported with a hedge, never a diagnosis. Units: glucose in the user's `glucose_units` — conversion mg/dL ÷ 18 = mmol/L (70 mg/dL = 3.9). Ketones always mmol/L.

## Blood Ketones (BHB)

| BHB (mmol/L) | Read during a fast |
|---|---|
| <0.5 | Not yet nutritional ketosis — normal before ~16h |
| 0.5-1.5 | Light nutritional ketosis — typical at 16-24h |
| 1.5-3.0 | Deep — typical on extended fasts |
| >3.0 | Common at 48h+ in non-diabetics and fine there; in a diabetic WITH high glucose and nausea/vomiting → DKA pattern, urgent (`safety.md`) |

The 0.5-3.0 nutritional-ketosis band follows Volek & Phinney. Higher ketones do not mean faster fat loss — there is no bonus for chasing the number, and "my ketones are great" is never a reason to extend a fast (rule 7).

## Glucose

- Normal fasted range 70-100 mg/dL (3.9-5.6 mmol/L). Non-diabetics can dip into the 60s late in extended fasts without symptoms — glucose and ketones together tell the story (GKI below); glucose alone late in a fast reads scarier than it is.
- Medicated diabetic: rule 6 verbatim — <70 mg/dL (3.9 mmol/L) breaks the fast with 15 g fast carb, recheck in 15 min. No GKI nuance applies to this threshold.
- Dawn phenomenon: the morning rise is cortisol-driven glucose release, not a broken fast — expect it in morning readings and say so before the user distrusts their log.

## GKI (Glucose-Ketone Index)

Formula: GKI = glucose (mmol/L) ÷ BHB (mmol/L). Worked example: glucose 85 mg/dL → 85 ÷ 18 = 4.7 mmol/L; BHB 1.6 → GKI = 4.7 ÷ 1.6 ≈ 3.

| GKI | State |
|---|---|
| <3 | Deep ketosis — the therapeutic-research zone (Seyfried; therapeutic contexts, not a general target) |
| 3-9 | Moderate ketosis — typical for extended fasts and strict keto |
| >9 | Not meaningfully in ketosis |

For everyday tracking, BHB alone is enough; GKI earns its arithmetic only when the user runs both meters and asks for it.

## Device Quirks

| Device | Quirk | Play |
|---|---|---|
| Urine strips | Fade with keto-adaptation — kidneys stop dumping acetoacetate, so weeks in, strips read "out of ketosis" while blood BHB is high | Trust them in week 1; retire them after; never read a faded strip as a broken fast |
| Blood glucose meter | ISO 15197 tolerates ±15% — single readings are noisy | Trend over 3+ readings beats any point; a lone weird number gets re-measured, not acted on |
| Breath acetone | Tracks fat-oxidation trend; lags and diverges from blood BHB | Use for direction, not thresholds |
| CGM | Compression lows at night — sensor pressed during sleep reads a false low | An asymptomatic nocturnal "low" that recovers on position change is the sensor, not hypoglycemia; a medicated diabetic confirms by fingerstick |

Measure at consistent times (morning + pre-break is the useful pair); readings scattered across random hours are uninterpretable and produce false trend talk.

## What Goes in a Status Report

Elapsed hours + hedged stage estimate + latest reading with units + trend direction if 3+ readings exist. No diagnosis, no praise for high ketones, no extension suggestions off a good number (rule 7).
