# The Schengen 90/180 Rule — Algorithm & Edge Cases

## The Rule

A non-EU national on visa-free (or short-stay visa) status may be present in the Schengen area **at most 90 days in any rolling 180-day window**.

"Rolling" is the tricky part: on any date D during your presence, look back 180 days (including D). The total days present in that window must be ≤ 90.

## Day Counting Conventions

- **Entry day counts** as a day of presence.
- **Exit day does NOT count** (the day you leave is not a full day present — you exit at the border).
  - Consequently: a stay from Jan 10 (entry) to Apr 10 (exit) = Jan 10..Apr 9 = 90 days. Exactly legal.
- Presence is per-person, whole Schengen area — a hop to the UK does not "reset" anything; those days still count if within the window.

## Algorithm (implemented in `border_buddy.py schengen`)

```
for reference_date D:
    window_start = D - 179 days        # 180-day window including D
    used = count of presence-days in [window_start, D]
    remaining = 90 - used
    # earliest date the oldest presence exits the window:
    # window_start advances day by day; days fall off the front
```

The script also computes:

- **Overstay risk**: if a planned stay (last visit's departure) would push `used > 90`, flag it with the exact number of overstay days.
- **Window exit dates**: for each past visit, the date it stops counting (entry_date + 180 days).
- **Next safe entry**: earliest date you can enter and stay a requested number of days legally.

## Worked Example

Visits: 2026-01-10 → 2026-04-10 (90 presence days: Jan 10–Apr 9), then 2026-06-01 → 2026-06-20 (19 presence days: Jun 1–19).

On 2026-06-20 the window covers 2025-12-23 → 2026-06-20:
- First trip: Jan 10 – Apr 9 inside window: 90 days
- Second trip: Jun 1 – Jun 19: 19 days
- Total = 109 → **overstay by 19 days**. The calculator flags this before it happens.

## Edge Cases

1. **Multi-country Schengen trips count once.** France 30d + Germany 30d + Italy 30d = one 90-day presence pool. People budget per-country and overstay.
2. **Cruise days in Schengen ports** count as presence days (you're ashore).
3. **Transit through Schengen counts** if you cross a border (even a 6-hour landside layover day).
4. **The window moves daily.** "I have 30 days left" is only true *today*; tomorrow old days fall off and the number changes. Always compute as-of a specific date.
5. **Visa nationals vs visa-free** use the same 90/180 math for Type C visas; long-stay (D) national visas follow the country's own rules and don't consume the 90/180 pool the same way.
6. **Exit-day convention differences**: some calculators count the exit day. This skill follows the EU Commission's convention (entry counts, exit doesn't). When borderline, keep a 1–2 day safety margin.

## Input Format

`--visits` accepts JSON:

```json
[
  {"entry": "2026-01-10", "exit": "2026-04-09", "country": "PT"},
  {"entry": "2026-06-01", "exit": "2026-06-20", "country": "ES"}
]
```

or CSV `entry,exit,country` with header. Dates ISO `YYYY-MM-DD`. Country is informational (presence is area-wide).
