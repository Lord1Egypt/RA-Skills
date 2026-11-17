# Memory Template — Fasting

Files under `~/Clawic/data/fasting/`: `config.yaml` (declared preferences, keys from the SKILL.md Configuration table), `log.md` (the fast log), `memory.md` (observed context). Config is what the user declared; memory is what you observed — an observation never overwrites a declared preference without confirmation.

## log.md (one row per fast)

```markdown
# Fast Log

| start | end | hours | protocol | flags |
|---|---|---|---|---|
| 2026-07-21T20:00-05:00 | 2026-07-22T12:00-05:00 | 16.0 | 16:8 | |
| 2026-07-22T21:30-05:00 | (active) | | 16:8 | est |
```

- Timestamps always carry the UTC offset; elapsed = absolute difference (`tracking.md`).
- The active fast is the last row with `(active)`; close it by writing end + hours at first caloric intake.
- Flags: `est` (estimated boundary) · `retro` (logged late) · `broke-early` (before target — still a completed fast, rule 7) · `observance` (religious mode, sunset/ruling boundaries) · `flagged` (lenient-definition intake kept the clock, `tracking.md`).

## memory.md

```markdown
# Fasting Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Goal, protocol history, typical schedule, observances -->
<!-- Shift work, travel patterns, immovable meals -->

## Symptom History
<!-- What they've reported, at what hour, what resolved it -->

## Rulings and Preferences
<!-- Gray-zone rulings per item; tone; check-in wishes; device used -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their pattern |
| `complete` | Know their protocol and rhythms well |
