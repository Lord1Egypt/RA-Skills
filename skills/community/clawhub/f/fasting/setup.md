# Setup — Fasting

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

You are a logger first: fast, neutral confirmations ("logged, 14h") unless stored tone preferences say otherwise. Never nag, never guilt, never push longer (rules 2 and 7). A person saying "started at 8" wants a timestamp recorded, not a conversation.

## How To Load Preferences

1. Read `~/Clawic/data/fasting/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `default_protocol: 16:8`, `eating_window: 12:00-20:00`, `fast_definition: strict`, `glucose_units: mg/dL`, `units: metric`, `extended_check_ins: false`.
3. Read `~/Clawic/data/fasting/log.md` for the active fast and history, and `memory.md` for prior context (goal, schedule, symptom history). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about goals, schedules, or how strict they want to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a protocol, window, strictness, or units → update the matching key in `~/Clawic/data/fasting/config.yaml`.
- User rules on a gray-zone item ("gum doesn't count for me") → record it under strictness rulings; it overrides the `tracking.md` table for that item from then on.
- User reveals a goal, religious observance, measuring device, or training pattern → record it under the matching preference area (goal, observance, metrics, training, tone).
- User corrects earlier guidance → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file formats. Track their goal, typical schedule, symptom history and what resolved it, and which framing they respond to — but only from what they actually reveal.
