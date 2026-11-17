# arcli

Apple Reminders CLI for macOS. List, add, edit, complete and delete reminders
from the command line, with `--json` for scripts and agents. Uses EventKit
through JXA, so Reminders.app does not have to be open.

```bash
npm install -g @gopaljigaur/arcli
arcli setup                          # grant Reminders access once
arcli lists
arcli reminders Groceries            # open reminders in one list
arcli reminders --due today          # due today or overdue, every list
arcli add "Buy milk" --list Groceries --due "tomorrow 09:00" --priority high --flagged
arcli edit <id> --title "Buy oat milk" --no-due
arcli complete <id>
arcli delete <id>                    # asks first; -y in scripts
```

## Commands

| Command | What it does |
|---------|--------------|
| `setup` | Asks macOS for Reminders access and reports how many lists it sees |
| `lists` | Every list with its id, account and open count |
| `reminders [list]` | Open reminders from one list (by name or `--list-id`) or all of them |
| `show <id>` | One reminder, flag included |
| `add <title>` | New reminder in `--list`, or the default list |
| `edit <id>` | Change title, list, due date, notes, URL, priority or flag |
| `complete <id>` / `uncomplete <id>` | Mark done or not done |
| `delete <id>` | Remove; asks unless `-y`, and refuses without a terminal |

`reminders` filters: `--due today|overdue|upcoming` (today includes overdue,
like Reminders.app), `--all` to include completed, `--completed` for only
completed, `--flagged`, `--limit <n>`.

Fields for `add` and `edit`: `--title`, `--list` or `--list-id`, `--due`,
`--no-due`, `--notes`, `--url`, `--priority none|low|medium|high`, `--flagged`,
`--unflagged`. `--due` takes `YYYY-MM-DD`, `"YYYY-MM-DD HH:mm"`, `today`,
`tomorrow`, or either with a time such as `"tomorrow 09:00"`. A timed due date
also gets an alert at that time, as Reminders.app does.

## Output

Every command takes `--json`. Errors then come back on stdout as
`{ "ok": false, "error": { "code", "message" } }`. A reminder looks like:

```json
{
  "id": "7AF983C5-0000-0000-0000-000000000000",
  "title": "Buy milk",
  "list": "Groceries",
  "listId": "1A2B3C4D-0000-0000-0000-000000000000",
  "due": "2026-11-07T09:00",
  "completed": false,
  "completedAt": null,
  "priority": "high",
  "notes": "",
  "url": "",
  "createdAt": "2026-11-06T11:23:21.104Z",
  "modifiedAt": "2026-11-06T11:23:21.104Z",
  "flagged": true
}
```

`due` is local time, `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm`. `flagged` is present
on `show`, `add` and `edit`, and on `reminders --flagged`; plain listings leave
it out.

## Permissions

`arcli setup` triggers the macOS prompt. If access was denied, allow your
terminal (and/or `osascript`) in System Settings > Privacy & Security >
Reminders.

EventKit has no flag, so flags go through Reminders.app scripting. The first
flag read or write asks for Automation access to Reminders; if denied, allow it
in System Settings > Privacy & Security > Automation. Flag calls start
Reminders.app in the background and take a second or two.

Exit codes: `0` ok, `1` runtime error, `2` bad arguments, `10` Reminders access
not granted.

## License

MIT
