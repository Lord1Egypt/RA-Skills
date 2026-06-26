# accli

[![npm](https://img.shields.io/npm/v/@gopaljigaur/accli)](https://www.npmjs.com/package/@gopaljigaur/accli)
[![clawhub skill](https://img.shields.io/badge/clawhub-accli--plus-00c896)](https://clawhub.ai/gopaljigaur/accli-plus)

Apple Calendar CLI for macOS — manage calendars and events from the command line (via JXA + EventKit).

## Install

```bash
npm i -g @gopaljigaur/accli
```

**OpenClaw skill:**
```bash
clawhub install accli-plus
```

## Quick start

```bash
accli setup
accli calendars
accli events --calendar-name "Work" --from 2025-01-01 --to 2025-01-31
```

## Permissions (macOS)

On first run, you may need to grant Calendar access.

1. Run `accli setup`
2. In **System Settings → Privacy & Security → Calendars**, ensure the responsible app (often `osascript` and/or your terminal) has **Full Access** (not “Add Only”).

## Commands

- `setup` — trigger macOS Calendar permission prompt
- `calendars` — list calendars
- `events` — list events in a range
- `event` — fetch a single event by ID (includes alerts in output)
- `create` — create an event (supports `--alert`, `--recur`, etc.)
- `update` — update an event (supports `--dry-run`)
- `delete` — delete an event (supports `--dry-run`)
- `search` — search events across all calendars
- `export` — export all events from all calendars
- `freebusy` — show busy time slots
- `config` — set/show/clear default calendar

Run `accli <command> --help` for command-specific options.

## Alerts

Set one or more alerts on create or update using `--alert <minutes>` (minutes before event start). Repeatable.

```bash
accli create Home --summary "Standup" --start 2025-01-15T09:00 --end 2025-01-15T09:30 --alert 5 --alert 15
accli update Home <event-id> --alert 5 --alert 10
```

`--alert` on update replaces all existing alerts. Omit to leave alerts unchanged. The `accli event` command now includes alerts in its output.

> Note: iCloud calendars preserve multiple alerts. Google Calendar via CalDAV syncs only one.

## Search

Search events across all calendars in a date range using a case-insensitive query matched against summary, location, and description.

```bash
accli search --query "standup" --from 2025-01-01 --to 2025-01-31
accli search --query "meeting" --calendar-id "ABC123" --json
```

## Export

Export all events from all calendars (or a subset) in a date range. Output is grouped by calendar.

```bash
accli export --from 2025-01-01 --to 2025-12-31 --json
accli export --from 2025-01-01 --to 2025-03-31 --calendar-id "ABC123"
```

## Dry Run

Use `--dry-run` on `delete` or `update` to preview what would happen without making any changes.

```bash
accli delete Work <event-id> --dry-run
accli update Work <event-id> --summary "New title" --dry-run --json
```

## Recurring Event Scope

Use `--span` on `delete` or `update` to control which occurrences of a recurring event are affected.

- `--span this` (default) — only this occurrence
- `--span future` — this and all future occurrences
- `--span all` — all occurrences (deletes/updates the entire series)

```bash
accli delete Work <event-id> --span all
accli update Work <event-id> --summary "Renamed" --span future
```

## Recurring Events

Create recurring events using `--recur` on the `create` command. Supported frequencies: `daily`, `weekly`, `monthly`, `yearly`.

```bash
accli create Work --summary "Weekly sync" --start 2025-01-15T10:00 --end 2025-01-15T11:00 --recur weekly
accli create Work --summary "Daily standup" --start 2025-01-15T09:00 --end 2025-01-15T09:30 --recur daily --recur-count 20
accli create Personal --summary "Birthday" --start 2025-06-01 --end 2025-06-01 --all-day --recur yearly --recur-end 2030-01-01
```

- `--recur-count <n>` — stop after N occurrences
- `--recur-end <date>` — stop on or before the given date (YYYY-MM-DD)
- Both `--recur-end` and `--recur-count` require `--recur` to be set

## JSON output

Add `--json` to most commands to output JSON (including errors).

## Agent-Ready

Designed for coding agents and automation: structured `--json` output on all commands, distinct exit codes (0=success, 1=runtime, 2=validation, 10=auth), machine-readable error codes, and persistent calendar IDs for reliable targeting.

## Notes

- macOS only (`darwin`), because it uses `osascript` + EventKit.
- Config path defaults to `~/.acclirc` but can be overridden via `ACCLI_CONFIG_PATH` (or `ACCLI_HOME`).

---

Forked from [joargp/accli](https://github.com/joargp/accli).
