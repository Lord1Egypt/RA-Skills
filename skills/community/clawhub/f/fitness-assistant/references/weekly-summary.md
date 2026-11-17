# Weekly summary

A short recap sent once a week — by default **Sunday 21:00 in the user's own timezone** — so the user can see how the week went and what changes next week.

## Schedule

- Default: Sunday 21:00 local time. Use the user's IANA timezone and the cron expression `0 21 * * 0` (see scheduling.md for the exact tool/CLI call and payload).
- One job only, named "Weekly fitness summary": if it already exists, update it instead of creating a duplicate, then confirm the next run time.
- If the user prefers another day or hour, keep it weekly and use their choice; ask only if they raise it.

## What to include

Use the fixed weekly-summary framing text from [references/dialogues.md](references/dialogues.md) and the fixed section labels from languages.md:

1. **Training this week** — sessions completed vs planned, total training time, the intensity usually used, and anything missed.
2. **Nutrition this week** — how closely the days matched the calorie/protein targets, which menu or ingredient changes were made, dishes the user liked.
3. **Spending this week** — only when a daily budget is set: estimated food cost for the week against the budget, and where it drifted.
4. **Next week** — 1–3 concrete suggestions: menu adjustments, training progression from the training log, and budget tweaks. Mention if a three-day review is due.

## Rules

- Write everything in the user's chosen language only, using the fixed weekly-summary dialogue and the standard labels.
- Use only data actually recorded in the profile, training log, and budget estimates, plus what the user reported. If a section has no data, say it is not recorded yet and ask for it once — never invent sessions, meals, or spending.
- Keep it short and skimmable: bullets, no full daily plan, no new medical claims.
- Keep numbers in the user's units and currency, and keep cost figures labelled as estimates.
