---
name: meeting-cadence-optimizer
description: Analyze how the user's meeting load correlates with how their days actually feel -- using their own evening-debrief and morning check-in history -- and recommend an optimal meeting cadence. Use this whenever the user says things like "am I overbooked", "too many meetings", "optimize my schedule", "meeting cadence", "meeting burnout", "what's my meeting sweet spot", or wonders whether their schedule is wearing them down. Also good as a weekly (Sunday/Monday) review. Reads back Fulcra annotations and computes the numbers deterministically. Needs at least ~a week of evening debriefs to say anything useful. Do NOT use it to read raw calendar data alone or for objective health pulls.
---

# Meeting Cadence Optimizer

Find the meeting load where the user's days actually go well -- grounded in their own logged data, not vibes. This skill reads back their **Evening Debrief** records (day rating, meeting count, cadence feedback) and **Morning Check-In** records (energy), then computes the relationship between meeting density and day quality. Let the data do the convincing.

## Prerequisites

- Fulcra CLI authenticated (`uv tool run fulcra-api auth login`).
- Run with `uv run --python 3.12`.
- Meaningful output needs history: this works once there are several **evening-debrief** entries with `meeting_count` and `day_rating`. The skill reports a confidence level so you know how much to trust it.

## Analyze (read-only)

```bash
uv run --python 3.12 ~/.claude/skills/meeting-cadence-optimizer/scripts/cadence.py analyze --days 30
```

Returns, computed from the user's own records:
- `data_points` and a `confidence` gate: **insufficient** (<7 days), **low** (7-13), **medium** (14-29), **high** (30+).
- `avg_meeting_count`, `avg_day_rating`
- `day_rating_by_meeting_count` -- the average day rating at each meeting count (the core table)
- `best_rated_meeting_count` -- the count with the highest average rating (the "sweet spot")
- `meeting_count_vs_rating_correlation` -- Pearson r (negative = more meetings, worse days)
- `too_many_feedback_count` -- how often they flagged "too many"

## How to present it

Match your confidence to the data, and **only state numbers the script returned** -- never invent a correlation:

- **insufficient:** "I need about a week of evening debriefs before I can find your pattern -- keep wrapping up your days and I'll have something soon." Don't push numbers.
- **low:** "Early signal, low confidence -- here's what I'm seeing so far..."
- **medium / high:** Lead with the sweet spot and the table, e.g. *"Your days average 7.4 with 3-4 meetings but drop to 5.1 at 6+. Your sweet spot looks like 4. You've flagged 'too many' 5 times this month."* Then offer one or two concrete moves: cap daily meetings, add buffers after long ones, protect a focus block.

Keep recommendations actionable and few. The goal is a decision, not a dashboard.

## Save the analysis (optional)

To record the analysis as a Fulcra annotation (useful for a weekly cadence so trends are themselves trackable):

```bash
uv run --python 3.12 .../cadence.py save --days 30 --dry-run   # preview
uv run --python 3.12 .../cadence.py save --days 30             # write
```

Writes a "Cadence Analysis" moment annotation and reports `verified_matches`. If there's no data yet, `save` skips the write rather than recording an empty analysis.

## Weekly use

This is a natural Sunday-evening or Monday-morning review. If the user wants it automated, it can be scheduled to run weekly and surface the result in their next morning briefing.

## Privacy

Meeting patterns and day ratings are personal. Don't surface them publicly. Never print API tokens.

## Where this fits

The analytical capstone of the Fulcra concierge reflection loop (shared lib in `~/.fulcra-concierge/lib`). It consumes what **evening-debrief** (meeting count + day rating) and **subjective-checkin** (energy) record -- so its quality grows directly with how consistently those two are used.
