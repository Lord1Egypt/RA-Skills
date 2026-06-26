# Time Tracking and Work Reports

Use this file for work day management, time tracking on tasks, absence reports, and work schedules.

Scope: `timeman`

## Work Day Management

- `timeman.status` — get current work day status (OPENED/CLOSED/PAUSED/EXPIRED)
- `timeman.open` — start or resume work day
- `timeman.pause` — pause work day
- `timeman.close` — end work day
- `timeman.settings` — get work time settings for a user
- `timeman.schedule.get` — get work schedule by ID

Status values from `timeman.status`:

- `OPENED` — work day is active
- `CLOSED` — work day is finished
- `PAUSED` — work day is paused
- `EXPIRED` — opened before today and never closed

## Time Control and Absence Reports

- `timeman.timecontrol.reports.get` — get absence report for a user/month
- `timeman.timecontrol.reports.users.get` — list users in department with access level
- `timeman.timecontrol.report.add` — submit absence explanation
- `timeman.timecontrol.settings.get` / `.set` — time control module settings
- `timeman.timecontrol.reports.settings.get` — report UI settings

## Task Time Tracking

- `task.elapseditem.add` — add time spent on a task
- `task.elapseditem.getlist` — list time entries for a task
- `task.elapseditem.get` — get a single time entry
- `task.elapseditem.update` — update time entry
- `task.elapseditem.delete` — delete time entry

## Office Network

- `timeman.networkrange.get` — get office network ranges
- `timeman.networkrange.set` — set office network ranges
- `timeman.networkrange.check` — check if IP is in office network

## Common Use Cases

### Check work day status

```bash
python3 scripts/bitrix24_call.py timeman.status --json
```

### Check work day status for another user

```bash
python3 scripts/bitrix24_call.py timeman.status \
  --param 'USER_ID=42' \
  --json
```

### Start work day

```bash
python3 scripts/bitrix24_call.py timeman.open --json
```

### End work day

```bash
python3 scripts/bitrix24_call.py timeman.close --json
```

### Get absence report for a user

```bash
python3 scripts/bitrix24_call.py timeman.timecontrol.reports.get \
  --param 'USER_ID=42' \
  --param 'MONTH=3' \
  --param 'YEAR=2026' \
  --json
```

### List department users for time reports

```bash
python3 scripts/bitrix24_call.py timeman.timecontrol.reports.users.get \
  --param 'DEPARTMENT_ID=5' \
  --json
```

### Get time spent on a task

```bash
python3 scripts/bitrix24_call.py task.elapseditem.getlist \
  --param 'TASKID=456' \
  --json
```

### Log time on a task

```bash
python3 scripts/bitrix24_call.py task.elapseditem.add \
  --param 'TASKID=456' \
  --param 'FIELDS[SECONDS]=3600' \
  --param 'FIELDS[COMMENT_TEXT]=Development work' \
  --json
```

### Get user work schedule

```bash
python3 scripts/bitrix24_call.py timeman.settings \
  --param 'USER_ID=42' \
  --json
```

## Building Department Reports

To build a time report for a department:

1. Get department employees: `im.department.employees.get`
2. For each employee, get work day status: `timeman.status` with `USER_ID`
3. For detailed reports: `timeman.timecontrol.reports.get` with `USER_ID`, `MONTH`, `YEAR`
4. For task time: `task.elapseditem.getlist` per task

## Working Rules

- `timeman.status` returns current user by default — pass `USER_ID` for other users.
- `timeman.timecontrol.reports.get` requires `USER_ID`, `MONTH`, and `YEAR` (all mandatory).
- Access to other users' reports depends on role (manager/admin).
- `task.elapseditem.*` uses `TASKID` (not `TASK_ID`).
- Time entries use `SECONDS` field, not hours.

## Note: No Email API

Bitrix24 has `mailservice.*` methods for configuring SMTP/IMAP mail services, but there is **no REST API for reading or sending individual emails** from Bitrix24 mailboxes.

## Good MCP Queries

- `timeman status open close`
- `timeman timecontrol reports`
- `task elapseditem time spent`
- `timeman schedule settings`
