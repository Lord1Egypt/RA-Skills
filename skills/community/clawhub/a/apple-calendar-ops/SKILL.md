---
name: apple-calendar-ops
description: "Read, create, update, and delete Apple Calendar events via CalDAV. Use when the user wants to inspect calendars or events, add a calendar event, change an existing event, delete an event, or provide Apple Calendar data to a higher-level scheduler/orchestrator."
---

# Apple Calendar Ops

This skill is the Apple Calendar operation layer.

It handles stable calendar reads and writes. It does **not** do high-level scheduling, cross-system planning, or task prioritization.

## Core boundary

Use this skill for concrete Apple Calendar operations:

- list calendars
- fetch events in a time range
- create an event
- update an event
- delete an event

Do **not** use this skill to decide how the day should be planned. That belongs to a higher-level task/orchestrator.

## Operating rules

Default stance:

- reads are safe
- writes should be dry-run-friendly
- updates/deletes should prefer explicit event ids
- fuzzy title matching may help locate events, but should not be the only basis for risky writes

Credentials should come from `/home/agent/.openclaw/workspace/secrets.json`.

Read `references/boundary.md` before changing the skill's scope.
Read `references/event-contract.md` before writing or consuming event JSON.

## Quick start

### Read calendars

```bash
python3 /home/agent/.openclaw/workspace/skills/apple-calendar-ops/scripts/calendar_fetch.py --list-calendars
```

### Read events

```bash
python3 /home/agent/.openclaw/workspace/skills/apple-calendar-ops/scripts/calendar_fetch.py \
  --start 2026-03-12T00:00:00+08:00 \
  --end 2026-03-13T00:00:00+08:00
```

### Create event

```bash
python3 /home/agent/.openclaw/workspace/skills/apple-calendar-ops/scripts/calendar_create.py \
  --calendar "Calendar" \
  --title "Example event" \
  --start 2026-03-12T14:00:00+08:00 \
  --end 2026-03-12T15:00:00+08:00 \
  --dry-run
```

## Scripts

- `scripts/calendar_common.py` — shared config, secret loading, and JSON helpers
- `scripts/calendar_fetch.py` — list calendars and fetch events
- `scripts/calendar_create.py` — create an event
- `scripts/calendar_update.py` — update an event
- `scripts/calendar_delete.py` — delete an event

## References

- `references/boundary.md` — scope and non-goals
- `references/event-contract.md` — normalized event shape for all scripts

## First-version goal

Version 1 should make Apple Calendar readable and safely writable.

That means:

- reliable read access for scheduler inputs
- explicit create/update/delete flows
- machine-readable output
- conservative handling of risky writes
