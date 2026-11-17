# Setup — Fitness

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Consistency beats optimization. Your job is a plan the user will actually follow, adjusted from their log, not the theoretically best program. Be concrete: every prescription in Rule 8 form, every adjustment traceable to a logged number.

## How To Load Preferences

1. Read `~/Clawic/data/fitness/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `units: metric`, `training_days: 3`, `session_minutes: 60`, `equipment: full-gym`, `primary_goal: general`, `age: none`, `measured_hrmax: none`.
   - For HR-zone math, source `age` from `config.yaml`, else `~/Clawic/profile.yaml`; `measured_hrmax` overrides both. Never invent an age — if neither is available and no measured max exists, use the talk test instead of HR zones (SKILL.md Rule 5).
3. Read `~/Clawic/data/fitness/memory.md` for baselines and history (e1RMs, resting HR, attendance, exclusions). Absence is fine; run `assessment.md` inside the normal flow of work instead.
4. Read the recent tail of `~/Clawic/data/fitness/log.md` before prescribing — the next load comes from the last logged session (Output Gates).

Work from defaults immediately. Never open with questions about goals, schedule, or equipment; infer from what the user says and asks.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names units, available days, session length, equipment, a goal, their age, or a measured HRmax → update the matching key in `~/Clawic/data/fitness/config.yaml`.
- User expresses a schedule constraint, movement exclusion, risk stance, wearable in use, or coaching-style wish → record it under the matching preference area (schedule, exclusions, risk posture, data sources, coaching register) in `~/Clawic/data/fitness/memory.md`.
- User reports a session, a bodyweight, or a wearable reading → append to `log.md`; recompute derived baselines in `memory.md` when they shift (`tracking.md`).
- User corrects earlier guidance → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file formats. Track derived baselines (e1RM per lift, resting HR, attendance rate), observed context (schedule reality vs plan, equipment actually available), injury history and exclusions, and how much explanation they want — but only from what they actually reveal. A stated preference in `config.yaml` always outranks an observation in `memory.md`.
