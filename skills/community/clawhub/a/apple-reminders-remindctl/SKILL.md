---
name: apple-reminders
description: Manage Apple Reminders via the remindctl CLI. Use for time-anchored or place-anchored tracking that doesn't belong on the calendar.
---

# Apple Reminders (remindctl)

Use this skill when Luis wants to track, capture, or check on time-anchored or place-anchored items that don't warrant a calendar event.

## When to use this vs other stores

- **Reminders** — actions tied to a time, place, or recurrence. "Remind me to..."
- **Google Calendar** — events with a fixed time block and duration. "Schedule..."
- **Open Brain** — durable facts, context, decisions, patterns. "Remember that..."

If an item belongs in two stores (e.g. "remind me to take Mounjaro every Wednesday" is both a recurring reminder AND a protocol fact worth knowing), create the reminder first, then capture a thought in Open Brain referencing the reminder by its ID prefix in the format `reminder:4A83`.

Most reminders are ephemeral ("grab milk") and do NOT belong in Open Brain. Only mirror when the item is durable context Luis will want to reason about later.

## Hard rules

1. **Default write target is the `Kaidan` list.** Never write to other lists unless Luis explicitly names one ("add this to Shopping").
2. **Never use `delete`.** Use `complete` instead — it's reversible via `--incomplete`. Completed reminders auto-purge per Reminders' own settings.
3. **Never use list-level mutations** — no `list --rename`, no `list --delete`, no `list --create` without Luis explicitly asking.
4. **Always pass `--json` on read commands** (`show`, `list`). Parse the output, present a human summary back.
5. **Always pass `--no-input`** to ensure non-interactive execution.
6. **Use ID prefixes (e.g. `4A83`), not indexes (`1`, `2`)**, for any operation that spans more than one command. Indexes shift between `show` runs; ID prefixes are stable.

## Priority mapping

Use Luis's A/B/C mode framework when setting `--priority`:
- `high` — A-mode floor (protocol, non-negotiable)
- `medium` — B-mode (important, can flex)
- `low` or `none` — C-mode (nice-to-have)

If priority isn't obvious from context, ask or default to `none`.

## Common patterns

**Check today's reminders:**
```
remindctl show today --json --no-input
```

**Check Luis's Kaidan list:**
```
remindctl list Kaidan --json --no-input
```

**Check all lists at once:**
```
remindctl list --json --no-input
```

**Add to default Kaidan list:**
```
remindctl add "Title here" --list Kaidan --no-input --json
```

**Add with due date:**
```
remindctl add "Take Mounjaro" --list Kaidan --due "2026-05-13 09:00" --no-input --json
```

**Add recurring:**
```
remindctl add "Water garden" --list Kaidan --due tomorrow --repeat "every 3 days" --no-input --json
```

**Add location-based (geofence):**
```
remindctl add "Grab the mail" --list Kaidan --location "<address>" --radius 100 --no-input --json
```

**Complete by ID prefix:**
```
remindctl complete 4A83 --json --no-input
```

**Edit (change title, move list, set due, etc.):**
```
remindctl edit 4A83 --due "2026-05-14 18:00" --json --no-input
```

**Clear a due date or recurrence:**
```
remindctl edit 4A83 --clear-due --no-repeat --json --no-input
```

## Filters available on `show`

`today | tomorrow | week | overdue | upcoming | open | completed | all | <YYYY-MM-DD>`

Default to `today` for "what do I have today" questions. Use `overdue` proactively when Luis hasn't checked in a while.

## Failure modes

- **Authorization revoked:** `remindctl status` returns not-authorized. Tell Luis to run `remindctl authorize` from a terminal at the Mac Mini.
- **List not found:** Reminders requires the list to exist. Don't auto-create — ask Luis whether he wants the `Kaidan` list created or whether he meant a different list.
- **Ambiguous ID prefix:** If `edit`/`complete` returns an ambiguity error, run `show --json` and use a longer prefix or the full ID.
- **Quiet output is misleading:** Always parse `--json` output to confirm success rather than assuming silence means success.

## Notes on scope

- `remindctl` is installed via Homebrew: `brew install steipete/tap/remindctl`
- Requires macOS Reminders Automation permission (granted)
- All operations target the user's iCloud Reminders, so changes are visible on iPhone, Watch, and other Apple devices within seconds
