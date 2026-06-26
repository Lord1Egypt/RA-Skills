---
name: accli
description: Manage Apple Calendar events from the command line on macOS — create, update, delete, search, export, and check availability with full JSON output for agent use.
author: gopaljigaur
license: MIT
platform: macOS
requires:
  binaries: [accli]
  install: "npm install -g @gopaljigaur/accli"
tags: [calendar, macos, productivity, apple, events]
---

# accli — Apple Calendar CLI

`accli` manages Apple Calendar on macOS via EventKit. All commands support `--json` for structured output. Exit codes: 0=success, 1=runtime error, 2=validation error, 10=auth error.

**First run:** `accli setup` to grant Calendar permissions (Full Access required in System Settings > Privacy & Security > Calendars).

## Calendars

```bash
accli calendars [--json]
```

Returns list of calendars with `id`, `name`, `source`, `index`, `writable`. Always prefer `--calendar-id <id>` over calendar name — IDs are stable, names are not.

## Events

```bash
accli events [<calendarName>] [--calendar-id <id>] --from <date> --to <date> [--json]
```

Lists events in a date range. Calendar is required (use name, `--calendar-id`, or set a default via `accli config set-default`).

## Single Event

```bash
accli event [<calendarName>] <eventId> [--calendar-id <id>] [--json]
```

Fetches full event detail including alerts array (minutes before start).

## Create Event

```bash
accli create <calendarName> --summary <text> --start <datetime> --end <datetime> \
  [--location <text>] [--description <text>] [--all-day] \
  [--alert <minutes>] [--alert <minutes>] \
  [--recur daily|weekly|monthly|yearly] [--recur-count <n>] [--recur-end <YYYY-MM-DD>] \
  [--json]
```

- `--alert` is repeatable — adds one alert per flag (minutes before start)
- `--recur-end` and `--recur-count` are mutually exclusive
- All-day events: use `YYYY-MM-DD` for `--start` and `--end`
- Timed events: use `YYYY-MM-DDTHH:mm`

## Update Event

```bash
accli update <calendarName> <eventId> \
  [--summary <text>] [--start <datetime>] [--end <datetime>] \
  [--location <text>] [--description <text>] \
  [--alert <minutes>] [--alert <minutes>] \
  [--dry-run] [--json]
```

`--alert` on update replaces all existing alerts. Omit `--alert` to leave alerts unchanged.
`--dry-run` returns `{ dryRun: true, wouldUpdate: { eventId, changes } }` without modifying anything.

## Delete Event

```bash
accli delete <calendarName> <eventId> [--dry-run] [--json]
```

`--dry-run` returns `{ dryRun: true, wouldDelete: { id, summary, calendar, start, end } }` without deleting.

## Search

```bash
accli search --query <text> [--from <date>] [--to <date>] [--calendar-id <id>] [--json]
```

Case-insensitive search across summary, location, and description. Searches all calendars unless `--calendar-id` is provided. Returns events with `calendarId` field for targeting.

## Export

```bash
accli export --from <date> --to <date> [--calendar-id <id>] [--json]
```

Exports all events grouped by calendar. Response: `{ calendars: [{ id, name, source, events, truncated }], totalEvents, truncated }`. Each calendar truncates at 500 events per calendar and sets `truncated: true` if hit.

## Free/Busy

```bash
accli freebusy --from <datetime> --to <datetime> [--calendar-name <name>] [--json]
```

Returns busy time slots across calendars.

## Config

```bash
accli config set-default --calendar-id <id> [--json]
accli config show [--json]
accli config clear [--json]
```

Persists default calendar to `~/.acclirc` (override with `ACCLI_CONFIG_PATH`). Commands that require a calendar use the default when no calendar is specified.

## DateTime Formats

- Timed: `YYYY-MM-DDTHH:mm` or `YYYY-MM-DDTHH:mm:ss`
- Date-only (all-day events, --from/--to): `YYYY-MM-DD`

## Agent Best Practices

- Always use `--json` for programmatic parsing
- Use `--calendar-id` not calendar name (stable across renames)
- Use `--dry-run` before destructive operations to confirm target event
- Use `accli search` to find event IDs before update/delete
- Check `ok: false` in JSON response before proceeding
- `accli export` is suitable for full calendar backup; check `truncated` field
- Multiple alerts: repeat `--alert` flag — e.g. `--alert 5 --alert 15`
- macOS only — do not attempt on non-darwin systems

## Error Codes

| Code | Meaning |
|------|---------|
| `NOT_AUTHORIZED` | Calendar access not granted or set to Add Only |
| `CALENDAR_NOT_FOUND` | Calendar ID or name not found |
| `AMBIGUOUS_CALENDAR` | Multiple calendars with same name — use `--calendar-id` |
| `EVENT_NOT_FOUND` | Event ID not found in calendar |
| `MISSING_REQUIRED` | Required flag missing |
| `INVALID_ARGUMENT` | Invalid flag value |
| `INVALID_RANGE` | Start is after end |
