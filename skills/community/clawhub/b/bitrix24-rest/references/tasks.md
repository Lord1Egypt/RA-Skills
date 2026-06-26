# Tasks

Use this file for task CRUD, delegation, checklists, comments, planner data, and filtering.

## Core Methods

- `tasks.task.list` — list tasks with filters, sorting, and pagination
- `tasks.task.get` — get one task by ID
- `tasks.task.add` — create task
- `tasks.task.update` — update task
- `tasks.task.complete` — mark task as completed
- `tasks.task.renew` — reopen task
- `tasks.task.delegate` — delegate task
- `tasks.task.delete` — delete task
- `tasks.task.favorite.add` / `tasks.task.favorite.remove`

Checklist:

- `task.checklistitem.add` / `task.checklistitem.getlist`
- `task.checklistitem.complete` / `task.checklistitem.renew`
- `task.checklistitem.delete`

Comments:

- `task.commentitem.add` / `task.commentitem.getlist`

Planner:

- `task.planner.getlist` — returns task IDs from current user's "Plan for the day"

Deprecated: `task.item.*` methods — do not use.

## Critical: Filter Syntax

`tasks.task.list` uses prefix operators on filter keys:

- `>=DEADLINE` — deadline on or after date
- `<=DEADLINE` — deadline on or before date
- `!STATUS` — status not equal to value
- `RESPONSIBLE_ID` — assigned user
- `CREATED_BY` — creator
- `GROUP_ID` — project group

Dates in filters use `YYYY-MM-DD` format.

**Wrong:** `filter[DEADLINE]=2026-03-10` — this does not filter by exact date.
**Right:** `filter[>=DEADLINE]=2026-03-10` + `filter[<=DEADLINE]=2026-03-10` for tasks with deadline on that day.

## Statuses

- `1` — new
- `2` — waiting (pending)
- `3` — in progress
- `4` — supposedly completed (awaiting approval)
- `5` — completed
- `6` — deferred

To exclude deferred tasks: `filter[!STATUS]=6`

## Common Use Cases

### Overdue tasks (for proactive warnings)

Tasks where deadline has passed but task is not completed or deferred:

```bash
python3 scripts/bitrix24_call.py tasks.task.list \
  --param 'filter[RESPONSIBLE_ID]=1' \
  --param 'filter[<DEADLINE]=2026-03-08' \
  --param 'filter[<REAL_STATUS]=5' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=DEADLINE' \
  --param 'select[]=STATUS' \
  --param 'order[DEADLINE]=asc' \
  --json
```

`<DEADLINE` = deadline before today. `<REAL_STATUS` = status less than 5 (excludes completed=5 and deferred=6).

Use this in morning briefing and task lists to flag overdue items with "⚠️".

### Show active tasks for current user

First get user ID, then list active tasks:

```bash
python3 scripts/bitrix24_call.py user.current --json
python3 scripts/bitrix24_call.py tasks.task.list \
  --param 'filter[RESPONSIBLE_ID]=1' \
  --param 'filter[!STATUS]=5' \
  --param 'filter[!STATUS]=6' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=STATUS' \
  --param 'select[]=DEADLINE' \
  --param 'order[DEADLINE]=asc' \
  --json
```

Note: to exclude both statuses 5 and 6, use `REAL_STATUS` with range filter or pass `filter[<REAL_STATUS]=5`.

### Tasks with deadline on a specific date

```bash
python3 scripts/bitrix24_call.py tasks.task.list \
  --param 'filter[>=DEADLINE]=2026-03-10' \
  --param 'filter[<=DEADLINE]=2026-03-10' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=DEADLINE' \
  --param 'select[]=STATUS' \
  --json
```

### Create a task

```bash
python3 scripts/bitrix24_call.py tasks.task.add \
  --param 'fields[TITLE]=Task title' \
  --param 'fields[RESPONSIBLE_ID]=1' \
  --param 'fields[DEADLINE]=2026-03-15' \
  --param 'fields[PRIORITY]=2' \
  --json
```

### Add checklist item

```bash
python3 scripts/bitrix24_call.py task.checklistitem.add \
  --param 'TASKID=456' \
  --param 'FIELDS[TITLE]=Subtask text' \
  --json
```

### Add comment

```bash
python3 scripts/bitrix24_call.py task.commentitem.add \
  --param 'TASKID=456' \
  --param 'FIELDS[POST_MESSAGE]=Comment text' \
  --json
```

## Working Rules

- Always use `select[]` to pick only the fields you need.
- Use `order[DEADLINE]=asc` to sort by deadline.
- Pagination: page size is 50, use `start=0`, `start=50`, etc.
- Get user ID from `user.current` before filtering by `RESPONSIBLE_ID`.
- For read-only requests, execute immediately.

## Good MCP Queries

- `tasks task list filter`
- `task checklistitem`
- `task commentitem`
- `task planner`
