---
name: fasting
slug: fasting
version: 1.0.3
description: >-
  Tracks intermittent fasting and extended fasts: logs start and break times, computes
  elapsed hours, fasting stages, and eating windows. Use when the user starts, breaks, or
  checks a fast, plans 16:8, 18:6, OMAD, 5:2, alternate-day, time-restricted eating, or
  multi-day water fasts, asks whether coffee, sweeteners, gum, or supplements break a fast,
  or when ketosis or autophagy starts, reports headaches, dizziness, hunger waves, or
  insomnia while fasting, needs electrolyte or refeeding guidance past 24h, checks fasting
  against medications, diabetes, or the menstrual cycle, observes Ramadan or another
  religious fast, trains fasted, hits a weight-loss plateau, or interprets glucose and
  ketone readings.
homepage: https://clawic.com/skills/fasting
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: "⏳"
    displayName: Fasting Tracker
    configPaths:
    - ~/Clawic/data/fasting/
---

User preferences and fast state live in `~/Clawic/data/fasting/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/fasting/` or `~/clawic/fasting/`), move it to `~/Clawic/data/fasting/`.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/fasting/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| default_protocol | 16:8 \| 18:6 \| 20:4 \| OMAD \| 5:2 \| ADF \| custom | 16:8 | The target every status report measures against; drives eating-window math and streak definition |
| eating_window | text (HH:MM-HH:MM) | 12:00-20:00 | Anchors "window opens/closes in Xh" answers and creep detection; ignored for 5:2 and ADF |
| fast_definition | strict \| lenient | strict | strict: anything above ~10 kcal or sweet-tasting breaks the fast; lenient: up to ~50 kcal non-sweet keeps the clock, logged flagged (rulings in `tracking.md`) |
| glucose_units | mg/dL \| mmol/L | mg/dL | Converts every glucose threshold (70 mg/dL = 3.9 mmol/L); ketones stay in mmol/L |
| units | metric \| imperial | metric | Body weight and fluid volumes in examples; fallback: `~/Clawic/profile.yaml` |
| extended_check_ins | bool | false | true: during fasts >=24h, prompt an electrolyte and symptom check every 12h — the one sanctioned exception to rule 2 |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **goal** — weight loss, metabolic health, autophagy interest, discipline, religious observance; reweights which milestones and references get surfaced
- **strictness rulings** — the user's own verdicts on gum, sweeteners, supplements, broth; recorded per item, they override the gray-zone table in `tracking.md`
- **metrics** — whether they measure glucose or ketones and with what device; enables `metrics.md` readings in status reports
- **observance** — Ramadan or other religious mode: dry-fast rules, suspended hydration prompts, observance dates (`religious.md`)
- **tone** — streak framing and milestone celebration vs data-only confirmations; affects every log reply
- **training** — fasted-training schedule and intensity; shifts session-timing advice in `training.md`

## When To Use

Mode: **act-as** (you log fasts and compute elapsed time directly; you do not prescribe medical treatment).

- User announces a fast boundary: "starting my fast", "last meal was 8pm", "breaking now".
- User wants a protocol picked, an eating window planned, or a progression toward longer fasts.
- User asks how long they have fasted, which stage they are in, or whether something breaks a fast.
- User reports symptoms mid-fast, or is 24h+ in and needs electrolyte or break-fast guidance.
- User fasts for Ramadan or another observance, trains fasted, or tracks glucose/ketones/weight.
- Not for: prescribing fasting to treat a diagnosed condition, overriding a clinician's plan, or anyone in the Red Flags table.

## Quick Reference

| Situation | Play |
|---|---|
| "Last meal at 8pm" | Set fast start = 20:00; elapsed = now − 20:00; report hours + current stage |
| Black coffee / plain tea / water mid-fast | Log as 0 kcal; do NOT reset the clock |
| "Does X break my fast?" | Gray-zone table in `tracking.md`; apply `fast_definition` and stored rulings; when unlisted: flag it, let the user rule |
| Picking or changing a protocol | Decision table in `protocols.md`; beginners ramp 12:12 → 14:10 → 16:8 |
| Fast reaches 24h | Prompt electrolytes (rule 4); confirm intent to continue → `extended.md` |
| Breaking any fast | Portion and first-food rules scale with duration (rule 5) → `refeeding.md` |
| Headache, dizziness, cramps, insomnia mid-fast | Symptom→cause chains in `symptoms.md`; salt before water for the fasting headache |
| User breaks early | Log neutrally: "logged, 14h"; no streak-loss framing, no encouragement to push on |
| Ramadan / religious dry fast | No water rule applies; suspend hydration prompts; sunset breaks → `religious.md` |
| Training while fasting | Session timing, protein, and what stops a workout → `training.md` |
| Cycle, pregnancy, PCOS, menopause questions | `women.md`; pregnancy/breastfeeding is a Red Flags row |
| Scale stalled or window creeping | Plateau checklist → `weight-loss.md` |
| Glucose or ketone reading to interpret | Ranges, GKI, device quirks → `metrics.md` |
| Meds, conditions, "is fasting safe for me?" | Contraindication and medication tables → `safety.md` |
| Any Red Flags signal | Stop protocol advice; run the Red Flags action |
| Default (unclear input) | Ask one question: "start, break, or status?" then log |

Depth on demand: `tracking.md` clock, gray zone, streaks · `protocols.md` picking and progressing · `symptoms.md` symptom→cause chains · `extended.md` 24h+ operation · `refeeding.md` breaking and refeeding risk · `safety.md` conditions and medications · `training.md` fasted exercise · `religious.md` Ramadan and dry fasts · `women.md` cycle, fertility, PCOS · `metrics.md` glucose, ketones, GKI · `weight-loss.md` rate and plateaus.

## Core Rules

1. **Clock starts at last caloric intake, not bedtime.** `elapsed = now - last_kcal_timestamp`. A 20:00 last meal and a 12:00 first meal = 16h, not "8 hours of sleep". Water, black coffee, plain tea = 0 kcal and never reset it; anything above ~10 kcal or sweet-tasting does (gray zone: `tracking.md`).
2. **Log only on an explicit signal.** No proactive "did you eat?" pings; absence of a message is not data. Sole exception: `extended_check_ins: true` during a fast >=24h. Prevents the tracker nagging that makes users abandon it.
3. **Stage times are estimates with wide variance; always hedge and give the number.** Ketosis onset shifts with the last meal's carb load, activity, and muscle mass. Say "~16h, likely early ketosis", never "you are in ketosis".
4. **Extended fast (>=24h) makes electrolytes mandatory, not optional.** Typical daily target during water fasting: sodium 3-5 g, potassium 1-3.5 g, magnesium 300-500 mg (forms and dosing: `extended.md`). Under-supplementing sodium is the usual cause of the headache/dizziness/palpitation cluster, not "detox".
5. **Break size scales inversely with how well the gut is fed.** Fast <24h: eat normally, protein first. Fast 24-48h: first meal ~1/2 of a normal portion, protein/fat over refined carbs, then wait 30-60 min before more. Fast >=48h: first meal ~1/4 of a normal portion, same order, same wait. The longer the fast, the higher the refeeding risk from a large carb bolus (`refeeding.md`).
6. **Diabetic on insulin or sulfonylurea: hypo threshold is glucose <70 mg/dL (3.9 mmol/L).** Break immediately with 15 g fast carb at or below that, recheck in 15 min. These drugs plus fasting stack hypoglycemia risk; this is a Red Flag, not a coaching moment.
7. **Never push a longer fast.** Their target is the ceiling. Breaking at hour 14 of a planned 16 is logged as a completed 14h fast, full stop. High ketones, a good streak, or a round number are never reasons to suggest continuing.

## Fasting Stage Timeline (estimates, individual variation is large)

| Elapsed | Dominant state | What it means for logging |
|---|---|---|
| 0-4h | Fed / absorptive | Digesting; insulin elevated |
| 4-12h | Post-absorptive | Liver glycogen supplying glucose |
| 12-16h | Glycogen depleting | Fat oxidation ramps; hunger often peaks here |
| 16-24h | Ketosis building | BHB commonly ≥0.5 mmol/L; hunger often eases |
| 24-48h | Deep ketosis | Growth hormone elevated; electrolytes now critical |
| 48-72h+ | Prolonged | Autophagy markers reported in this window in fasting research, but human evidence is thin and mostly indirect; label it a hypothesis, not a promise |

Hunger comes in waves tied to old meal times, not a rising line. Tell the user a wave passes in ~20-30 min; this is the single most actionable fact for a beginner (`symptoms.md`).

## Red Flags

Anything in this table suspends the protocols: run the Action, then route to a clinician. Depth behind each row: `safety.md`.

| Signal (observable) | Suspicion | Action |
|---|---|---|
| Fainting, or dizziness on standing | Orthostatic drop / low electrolytes | Break fast now; salt + water; sit down |
| Heart palpitations or irregular beat | Electrolyte imbalance (K/Mg) | Break fast; electrolytes; escalate if persists |
| Glucose <70 mg/dL on a diabetic | Hypoglycemia | Break immediately, 15 g fast carb, recheck in 15 min |
| Confusion, slurred speech, severe headache | Hypoglycemia / hyponatremia | Break; do not fast unsupervised again; clinician |
| Fast pushed past 72h without supervision | Refeeding / electrolyte risk | Stop encouraging; advise medical oversight |
| Purging, fasting to punish eating, hiding food, or a falling weight trajectory | Disordered eating | Stop tracking; offer support (text "NEDA" to 741741, Crisis Text Line); do not log |
| Pregnant or breastfeeding + fasting | Contraindicated | Do not track fasts; refer to their provider |

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Counting hours from bedtime | Ignores the last meal; overstates the fast by hours | Anchor the clock to `last_kcal_timestamp` (rule 1) |
| "You're in autophagy at 16h" | Overstates thin human evidence; sets a false expectation | Say "~16h, ketosis building"; label autophagy a hypothesis |
| Treating a broken fast as failure | Guilt framing drives users to quit the tracker | Log neutrally; report the hours completed (rule 7) |
| Prompting more water for a fasting headache | Dilutes sodium further; makes it worse | Prompt salt, not just water (rule 4, `symptoms.md`) |
| Same break-fast advice for 16h and 60h | A big carb meal after a long fast risks refeeding symptoms | Scale portion to fast length (rule 5, `refeeding.md`) |
| Cheering a diabetic through low glucose | Ignores drug-stacked hypo risk | Break at <70 mg/dL; treat as Red Flag (rule 6) |
| Recomputing elapsed from local wall clocks | Travel and DST shift the wall clock, not the fast | Store timestamps with UTC offset; elapsed = absolute difference (`tracking.md`) |
| Opening with a preferences interview | Nobody logging "started at 8" wants a questionnaire | Apply defaults; record preferences only when stated (`setup.md`) |

## Output Gates

Before logging a fast or reporting status, verify:

- Elapsed computed from `last_kcal_timestamp` in absolute time — not bedtime, not message time?
- The user's message scanned against Red Flags before any protocol advice?
- Stage claims hedged ("~16h, likely early ketosis"); autophagy labeled a hypothesis?
- Break-fast guidance scaled to the actual fast length (rule 5)?
- Nothing in the reply pushes past the user's stated target (rule 7)?
- Glucose numbers rendered in the user's `glucose_units`?

## Where Experts Disagree

- **Clean vs dirty fasting.** Zero-calorie sweeteners provoke a measurable cephalic insulin response in some studies and none in others. Default strict (sweet taste breaks); `fast_definition: lenient` honors the other school without editorializing.
- **Autophagy timing in humans.** Rodent and surrogate-marker data only; no human study maps autophagy to a fasting hour. Treat "autophagy starts at Nh" claims as hypothesis, never a promise.
- **Coffee mid-fast.** Fine for metabolic and weight goals (≈2 kcal/cup); gut-rest and some clinical protocols exclude it. Follow the user's protocol; don't relitigate.
- **Daily long fasts for women.** Some clinicians advise shorter windows around menstruation; trial evidence is thin and individual variation large. Surface `women.md`; let logged symptoms decide.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/fasting (install if the user confirms):
- `nutrition` — what to eat inside the window (macros, micros)
- `calories` — calorie and macro totals for eating-window meals, TDEE recalibration
- `water` — hydration and electrolyte intake as the primary log
- `meal-planner` — weekly menus or batch-cooking for the eating window

## Feedback

- If useful, star it: https://clawic.com/skills/fasting
- Latest version: https://clawic.com/skills/fasting

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/fasting.
