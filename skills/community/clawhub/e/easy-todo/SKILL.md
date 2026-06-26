---
name: todo
description: Personal TODO list manager. Add tasks with deadlines and priorities, mark them done, set up recurring items, and receive morning and evening summaries.
user-invocable: true
metadata: {"openclaw": {"requires": {"bins": ["node"]}}}
---

# TODO Skill

You manage the user's personal TODO list. All tasks are persisted in `~/.openclaw/skills/todo/todos.md`.

## Running the CLI

```bash
node ~/.openclaw/skills/todo/cli.js <command> [options]
```

The file creates `todos.md` in the same directory automatically on first run.

## Commands

```
add "<title>" [--due YYYY-MM-DD] [--priority high|medium|low] [--notes "..."] [--tags tag1,tag2]
complete <id-or-title>
cancel <id-or-title>
list
list --today
list --upcoming [--days N]
list --completed
list --recurring
add-recurring "<title>" --frequency daily|weekly|monthly-first|monthly-last [--priority high|medium|low]
add-recurring "<title>" --days mon,wed,fri [--priority high|medium|low]
briefing morning
briefing evening
materialize
```

All commands print plain text. Exit 0 = success.

---

## Handling user messages

### Adding a task
1. Extract the title.
2. If no due date was mentioned, **ask for one before running the command** — unless the user explicitly said "no deadline" or "no due date".
3. Map urgency to priority: "urgent" / "ASAP" → `high`; "whenever" / "no rush" → `low`; otherwise `medium`.
4. Run `add` and relay the output.

### Completing a task
Match "done", "finished", "completed", "ticked off", etc. Use the task ID (`T3`) or a title fragment with `complete`.

### Recurring tasks
Confirm frequency if ambiguous:
- "every day" / "daily" → `--frequency daily`
- "every Monday" / "weekly" → `--frequency weekly`
- "first of the month" → `--frequency monthly-first`
- "end of the month" / "last day" → `--frequency monthly-last`
- "every Tuesday and Thursday" / "Mon, Wed, Fri" / any specific days → `--days tue,thu`

For `--days`, accepted formats: full names (`monday`), three-letter abbreviations (`mon`), or numbers (`1` for Monday). Multiple days are comma-separated. Examples:
- "every weekday" → `--days mon,tue,wed,thu,fri`
- "Tuesdays and Thursdays" → `--days tue,thu`
- "every weekend" → `--days sat,sun`

---

## Scheduled reminders

Run these automatically on the following schedule, without waiting for the user to ask:

| Time  | Command | What to send |
|-------|---------|--------------|
| 08:30 | `briefing morning` | Morning overview: overdue, due today, upcoming 7 days |
| 18:00 | `briefing evening` | Evening check-in: tasks still open today |

Also run `materialize` once per day (e.g. at 00:05 or alongside the morning briefing) to convert any due recurring tasks into active items before the briefing runs.

---

## todos.md

The file is managed entirely by `cli.js` — never edit it by hand. It contains a JSON block (machine-readable) and Markdown tables (human-readable) that are regenerated on every write.
