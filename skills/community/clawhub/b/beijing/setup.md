# Setup — Beijing

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Beijing rewards preparation and punishes improvisation — apps, permits, and air quality all have hard edges. Be concrete, quote numbers with their date, and route by the user's role and timeline before recommending anything.

## How To Load Preferences

1. Read `~/Clawic/data/beijing/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
3. Read `~/Clawic/data/beijing/memory.md` for prior context (their trip or move, district, family setup). Absence is fine; proceed without comment.
4. `home_currency` may fall back to `~/Clawic/profile.yaml` if the user keeps a shared profile.

Work from defaults immediately. Never open with questions about budget, dates, or preferences — infer role and timeline from the request (Core Rule 1 allows exactly one clarifying question when routing is genuinely blocked).

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names their district, budget band, dietary needs, Mandarin level, or home currency → update the matching key in `~/Clawic/data/beijing/config.yaml`.
- User reveals durable context (arrival date, employer area, kids and their school, ayi arrangement, visa type) → record it in `~/Clawic/data/beijing/memory.md`.
- User corrects earlier guidance ("we moved to Shunyi") → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their stage (planning trip, arrived, settled, leaving), home base, family situation, and recurring concerns — but only from what they actually reveal.
