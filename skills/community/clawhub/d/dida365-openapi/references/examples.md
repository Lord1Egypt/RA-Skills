# Examples

Commands below assume the current working directory is `dida365-openapi/`. If you run them from the repo root, replace `python scripts/dida365.py` with `python dida365-openapi/scripts/dida365.py`.
Examples below focus on the stable support surface exposed by this skill.

## Auth

Persist app config:

```bash
python scripts/dida365.py auth setup \
  --client-id "$DIDA365_CLIENT_ID" \
  --client-secret "$DIDA365_CLIENT_SECRET" \
  --redirect-uri "http://127.0.0.1:36500/callback"
```

Generate an authorization URL:

```bash
python scripts/dida365.py auth authorize-url \
  --client-id "$DIDA365_CLIENT_ID" \
  --redirect-uri "http://127.0.0.1:36500/callback"
```

Exchange an authorization code:

```bash
python scripts/dida365.py auth exchange-code \
  --code "returned-code" \
  --client-id "$DIDA365_CLIENT_ID" \
  --client-secret "$DIDA365_CLIENT_SECRET" \
  --redirect-uri "http://127.0.0.1:36500/callback"
```

## Project

List projects:

```bash
python scripts/dida365.py project list
```

Get one project by exact name:

```bash
python scripts/dida365.py project get --project-name "API Demo"
```

Read project data with the special inbox id:

```bash
python scripts/dida365.py project data --project-id inbox
```

Create a project:

```bash
python scripts/dida365.py project create \
  --name "API Demo" \
  --color "#F18181" \
  --view-mode list \
  --kind TASK
```

## Task

Create a simple task:

```bash
python scripts/dida365.py task create \
  --project-id inbox \
  --title "Review Dida365 OpenAPI skill"
```

Create a note-style task:

```bash
python scripts/dida365.py task create \
  --project-id inbox \
  --title "Research notes" \
  --kind NOTE
```

Create a tagged task:

```bash
python scripts/dida365.py task create \
  --project-id inbox \
  --title "Tagged task" \
  --tags-json '["alpha","beta"]'
```

Create a task from a JSON file:

```bash
python scripts/dida365.py task create --json-file ./task-create.json
```

Update a task with nested checklist items:

```bash
python scripts/dida365.py task update \
  --task-id "your-task-id" \
  --project-id "your-project-id" \
  --items-json '[{"title":"Item 1","status":0}]'
```

Complete a task:

```bash
python scripts/dida365.py task complete \
  --project-id "your-project-id" \
  --task-id "your-task-id"
```

Move one task:

```bash
python scripts/dida365.py task move \
  --from-project-id "source-project-id" \
  --to-project-id "destination-project-id" \
  --task-id "your-task-id"
```

Move many tasks with inline JSON:

```bash
python scripts/dida365.py task move \
  --json '[{"fromProjectId":"p1","toProjectId":"p2","taskId":"t1"},{"fromProjectId":"p1","toProjectId":"p3","taskId":"t2"}]'
```

List completed tasks in a time range:

```bash
python scripts/dida365.py task completed \
  --project-id "your-project-id" \
  --start-date "2026-03-01T00:58:20.000+0000" \
  --end-date "2026-03-05T10:58:20.000+0000"
```

List tasks completed in an explicit local time range:

```bash
python scripts/dida365.py task completed \
  --start-date "2026-03-17T00:00:00+0800" \
  --end-date "2026-03-17T23:59:59+0800"
```

Filter tasks by tag:

```bash
python scripts/dida365.py task filter \
  --tag-json '["urgent"]' \
  --status-json '[0]'
```

Filter both open and completed tasks:

```bash
python scripts/dida365.py task filter \
  --project-id "your-project-id" \
  --status-json '[0,2]'
```

Create a task with multiple reminders:

```bash
python scripts/dida365.py task create \
  --project-id inbox \
  --title "Reminder example" \
  --start-date "2026-03-21T22:00:00+0800" \
  --due-date "2026-03-21T22:00:00+0800" \
  --time-zone "Asia/Shanghai" \
  --reminders-json '["TRIGGER:PT0S","TRIGGER:-PT5M"]'
```

Update task tags:

```bash
python scripts/dida365.py task update \
  --project-id "your-project-id" \
  --task-id "your-task-id" \
  --tags-json '["new-tag"]'
```

Clear a repeat rule:

```bash
python scripts/dida365.py task update \
  --project-id "your-project-id" \
  --task-id "your-task-id" \
  --repeat-flag ""
```

## Repeat Rules

Create a weekday recurring task:

```bash
python scripts/dida365.py task create \
  --project-id inbox \
  --title "Weekday example" \
  --start-date "2026-03-16T22:00:00+0800" \
  --due-date "2026-03-16T22:00:00+0800" \
  --time-zone "Asia/Shanghai" \
  --repeat-flag "RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU,WE,TH,FR"
```

Update a task to repeat every 2 weeks on multiple weekdays:

```bash
python scripts/dida365.py task update \
  --project-id "your-project-id" \
  --task-id "your-task-id" \
  --repeat-flag "RRULE:FREQ=WEEKLY;WKST=MO;INTERVAL=2;BYDAY=MO,TH,SA"
```

Set custom explicit repeat dates:

```bash
python scripts/dida365.py task update \
  --project-id "your-project-id" \
  --task-id "your-task-id" \
  --repeat-flag "ERULE:NAME=CUSTOM;BYDATE=20260319,20260320,20260328,20260331"
```

Set a lunar yearly rule:

```bash
python scripts/dida365.py task update \
  --project-id "your-project-id" \
  --task-id "your-task-id" \
  --repeat-flag "LUNAR:FREQ=YEARLY;INTERVAL=1;BYMONTH=1;BYMONTHDAY=28"
```

Set a Dida365 extended skip rule:

```bash
python scripts/dida365.py task update \
  --project-id "your-project-id" \
  --task-id "your-task-id" \
  --repeat-flag "RRULE:FREQ=DAILY;INTERVAL=3;TT_SKIP=WEEKEND,HOLIDAY"
```
