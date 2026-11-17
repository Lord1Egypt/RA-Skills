---
name: calendar-gaps
description: Find scheduling conflicts and free time slots in a day's calendar events (pure computation, no account or network needed).
metadata:
  openclaw:
    requires:
      bins: ["node"]
---

# calendar-gaps

Given a day's events as JSON, report:

- **conflicts**: pairs of events that overlap, with the overlapping window;
- **free slots**: gaps of at least N minutes inside working hours;
- **busy time**: minutes of working time already booked;
- all-day events (listed, but they do not block time).

It needs no credentials and makes no network calls, so it works with any
calendar source that can produce JSON.

## Input

A JSON array, on stdin or in a file:

```json
[
  {"start": "2026-11-13T10:00:00-08:00", "end": "2026-11-13T11:00:00-08:00", "summary": "Project sync"},
  {"start": "2026-11-13T10:30:00-08:00", "end": "2026-11-13T11:15:00-08:00", "summary": "Design review"},
  {"start": "2026-11-13", "end": "2026-11-14", "summary": "Holiday"}
]
```

`start`/`end` are ISO 8601 date-times with an offset (or `Z`). A date-only
`start` marks an all-day event.

## Usage

Run it with `node` (installed copies do not always keep the executable bit):

```bash
node {baseDir}/scripts/calendar-gaps --date 2026-11-13 --tz America/Los_Angeles --work 09:00-17:00 --min 30 --file events.json
some-calendar-command --json | node {baseDir}/scripts/calendar-gaps --date 2026-11-13 --tz America/Los_Angeles
```

Options:

| Option | Default | Meaning |
|---|---|---|
| `--date` | (required) | Day to analyse: `YYYY-MM-DD`, `today` or `tomorrow`, in `--tz` |
| `--tz` | `UTC` | IANA time zone for working hours and output |
| `--work` | `09:00-17:00` | Working hours window |
| `--min` | `30` | Minimum free-slot length in minutes |
| `--file` | stdin | Events JSON file |
| `--json` | off | Machine-readable output |

## How to use the result

- Mention conflicts first and suggest which meeting to move, using a free
  slot of the same length.
- When the user asks "when can I fit X (N minutes)?", run with `--min N` and
  offer the first two or three slots.
- In a morning briefing, list the day's free slots in one line.
