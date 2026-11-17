---
name: arcli
description: Manage Apple Reminders from the command line on macOS. List, add, edit, complete and delete reminders, filter by due date, with JSON output for agent use.
author: gopaljigaur
license: MIT
platform: macOS
requires:
  binaries: [arcli]
  install: "npm install -g @gopaljigaur/arcli"
tags: [reminders, todo, macos, productivity, apple]
---

# arcli: Apple Reminders CLI

`arcli` manages Apple Reminders on macOS via EventKit. Every command supports `--json`. Exit codes: 0 success, 1 runtime error, 2 validation error, 10 not authorized.

**First run:** `arcli setup` to grant Reminders access (System Settings > Privacy & Security > Reminders).

## Lists

```bash
arcli lists [--json]
```

Returns `{ lists: [{ id, name, source, writable, open }] }`. `open` is the number of incomplete reminders. Prefer `--list-id <id>` over a list name: ids are stable, names can repeat across accounts.

## List Reminders

```bash
arcli reminders [<listName>] [--list-id <id>] [--due today|overdue|upcoming] \
  [--all | --completed] [--flagged] [--limit <n>] [--json]
```

- No list means every list
- Open reminders only by default; `--all` includes completed, `--completed` returns only completed
- `--due today` includes overdue, like the Today view in Reminders.app; `overdue` and `upcoming` are exclusive
- Sorted by due date, undated last
- `--flagged` adds a Reminders.app call (about a second) and sets `flagged: true` on each result

## Show One

```bash
arcli show <id> [--json]
```

Returns `{ reminder }` including `flagged`.

## Add

```bash
arcli add <title> [--list <name> | --list-id <id>] [--due <when>] \
  [--notes <text>] [--url <url>] [--priority none|low|medium|high] [--flagged] [--json]
```

No list means the default list for new reminders. A timed due date also gets an alert at that time.

## Edit

```bash
arcli edit <id> [--title <text>] [--list <name> | --list-id <id>] [--due <when> | --no-due] \
  [--notes <text>] [--url <url>] [--priority none|low|medium|high] [--flagged | --unflagged] [--json]
```

`--list` moves the reminder. `--notes ""` clears notes. `--no-due` clears the due date and its alerts.

## Complete

```bash
arcli complete <id> [--json]
arcli uncomplete <id> [--json]
```

## Delete

```bash
arcli delete <id> -y [--json]
```

Without `-y` it asks for confirmation, and refuses when there is no terminal. Agents must pass `-y`. There is no undo, so `arcli show <id>` first to confirm the target.

## Due Formats

- `YYYY-MM-DD` (all day)
- `YYYY-MM-DD HH:mm` or `YYYY-MM-DDTHH:mm`
- `today`, `tomorrow`, or either with a time: `"tomorrow 09:00"`

Output `due` is local time: `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm`, or `null`.

## Reminder Shape

`{ id, title, list, listId, due, completed, completedAt, priority, notes, url, createdAt, modifiedAt }`, plus `flagged` on `show`, `add`, `edit` and `reminders --flagged`. `priority` is `none`, `low`, `medium` or `high`.

## Agent Best Practices

- Always use `--json` and check `ok` before proceeding
- Use `arcli reminders --json` to find ids before `edit`, `complete` or `delete`
- Use `--list-id` from `arcli lists` instead of names
- Flags need Automation access to Reminders.app; a `NOT_AUTHORIZED` error on a flag call names the setting
- macOS only

## Error Codes

| Code | Meaning |
|------|---------|
| `NOT_AUTHORIZED` | Reminders access, or Automation access for flags, not granted |
| `LIST_NOT_FOUND` | No list with that name or id |
| `AMBIGUOUS_LIST` | More than one list with that name; use `--list-id` |
| `REMINDER_NOT_FOUND` | No reminder with that id |
| `MISSING_REQUIRED` | A required argument is missing |
| `INVALID_ARGUMENT` | A flag value is invalid |
| `SAVE_FAILED` / `DELETE_FAILED` | Reminders refused the change |
| `FLAG_FAILED` | The reminder was saved but Reminders.app could not set the flag |
