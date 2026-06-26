# Calendar

Use this file for personal calendars, group calendars, meetings, sections, recurrence, and availability checks.

## Core Methods

- `calendar.event.get` — list events in a date range (requires `type` and `ownerId`)
- `calendar.event.get.nearest` — list upcoming events (simplest way to get schedule)
- `calendar.event.getbyid` — get one event by ID
- `calendar.event.add` — create event
- `calendar.event.update` — update event
- `calendar.event.delete` — delete event
- `calendar.section.get` — list calendars (sections)
- `calendar.section.add` — create calendar
- `calendar.accessibility.get` — check user availability
- `calendar.meeting.status.get` — get current user's meeting participation status
- `calendar.resource.list` — list calendar resources

There is NO `calendar.get` or `calendar.list` method. Always use the full method names above.

## Critical: Required Parameters

`calendar.event.get` requires two mandatory parameters:

- `type` — one of: `user`, `group`, `company_calendar`
- `ownerId` — user ID for `user` type, group ID for `group`, `0` for `company_calendar`

Without these, the call fails with `ERROR_METHOD_NOT_FOUND` or similar.

`from` and `to` use date format `YYYY-MM-DD` (not datetime). Defaults: `from` = 1 month ago, `to` = 3 months ahead.

## Common Use Cases

### Show schedule via batch (preferred — one HTTP call)

Combine calendar + tasks in one request:

```bash
python3 scripts/bitrix24_batch.py \
  --cmd 'events=calendar.event.get?type=user&ownerId=1&from=2026-03-11&to=2026-03-11' \
  --cmd 'tasks=tasks.task.list?filter[RESPONSIBLE_ID]=1&filter[>=DEADLINE]=2026-03-11T00:00:00&filter[<=DEADLINE]=2026-03-11T23:59:59&select[]=ID&select[]=TITLE&select[]=DEADLINE&select[]=STATUS' \
  --json
```

### Show user's schedule for a specific day

Get user ID from cached config or `user.current`, then query events:

```bash
python3 scripts/bitrix24_call.py user.current --json
python3 scripts/bitrix24_call.py calendar.event.get \
  --param 'type=user' \
  --param 'ownerId=1' \
  --param 'from=2026-03-10' \
  --param 'to=2026-03-10' \
  --json
```

### Show upcoming events (easiest for "what's on my schedule")

```bash
python3 scripts/bitrix24_call.py calendar.event.get.nearest \
  --param 'type=user' \
  --param 'ownerId=1' \
  --param 'days=7' \
  --param 'forCurrentUser=true' \
  --json
```

### Check availability before scheduling

```bash
python3 scripts/bitrix24_call.py calendar.accessibility.get \
  --param 'users[]=1' \
  --param 'users[]=2' \
  --param 'from=2026-03-10' \
  --param 'to=2026-03-11' \
  --json
```

### Create an event

```bash
python3 scripts/bitrix24_call.py calendar.event.add \
  --param 'type=user' \
  --param 'ownerId=1' \
  --param 'name=Team Meeting' \
  --param 'from=2026-03-10T10:00:00' \
  --param 'to=2026-03-10T11:00:00' \
  --json
```

## Working Rules

- Always pass `type` and `ownerId` for `calendar.event.get`.
- Use `calendar.event.get.nearest` for "show my schedule" — it needs fewer parameters.
- Get user ID from `user.current` first if you don't know it.
- Check `calendar.accessibility.get` before proposing meeting slots.
- For read-only requests, execute immediately — do not ask permission.
- One retry on first failure, then report blocker.

## Good MCP Queries

- `calendar event get nearest`
- `calendar accessibility`
- `calendar section`
- `calendar resource booking`
