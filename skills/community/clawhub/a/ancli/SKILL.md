---
name: ancli
description: Read and write Apple Notes from the command line on macOS: list folders and notes, search, show, create, append, move and delete, with JSON output for agent use.
author: gopaljigaur
license: MIT
platform: macOS
requires:
  binaries: [ancli]
  install: "npm install -g @gopaljigaur/ancli"
tags: [notes, macos, productivity, apple]
---

# ancli: Apple Notes CLI

`ancli` drives Notes.app through JXA. Every command takes `--json`; errors then
come back as `{ "ok": false, "error": { "code", "message" } }` on stdout.
Exit codes: 0 success, 1 runtime error, 2 validation error, 10 not authorized.

**First run:** `ancli setup` triggers the macOS Automation prompt. If access was
denied, the user turns on Notes under their terminal in System Settings >
Privacy & Security > Automation. An agent cannot grant it.

## Ids

Notes ids are Core Data URLs (`x-coredata://.../ICNote/p123`). JSON carries
both `id` (short, `p123`) and `url` (full). Either works as an argument. On
`AMBIGUOUS_ID`, use the `url`.

## Folders

```bash
ancli folders [--json]
```

Returns `{ folders: [{ id, url, name, account, count }] }`. A `--folder`
argument takes a name (case-insensitive), `Account/Folder`, or an id.

## List

```bash
ancli list [--folder <folder>] [--limit <n>] [--json]
```

Most recently modified first, default limit 20. Returns `{ count, total, notes }`;
each note has `id`, `url`, `title`, `folder`, `created`, `modified`, `locked`.
No bodies. Recently Deleted is skipped unless named with `--folder`.

## Search

```bash
ancli search <query> [--folder <folder>] [--limit <n>] [--json]
```

Case-insensitive match on title and text. Same shape as `list`, plus a
`snippet` around the match for unlocked notes.

## Show

```bash
ancli show <id> [--html] [--json]
```

`--json` returns `note.text` (plain text), or `note.body` (HTML) with `--html`.
Also `account`, `shared` and `attachments`. A locked note has `locked: true`
and no text or body.

## Create

```bash
ancli create <title> [body] [--folder <folder>] [--json]
printf 'Milk\nEggs\n' | ancli create "Shopping list" --folder Notes
```

Body from the argument, or stdin when piped or given as `-`. Without
`--folder` the note goes to the default account's default folder.

## Append

```bash
ancli append <id> [text] [--json]
```

Adds text as new lines at the end. Refuses locked notes (`NOTE_LOCKED`) and
notes with attachments (`HAS_ATTACHMENTS`), since rewriting the body would
drop them.

## Move

```bash
ancli move <id> <folder> [--json]
```

## Delete

```bash
ancli delete <id> --yes [--json]
```

Moves the note to Recently Deleted (30 days). Deleting a note already there
removes it for good; the response has `permanent: true`. Without a terminal
`--yes` is required.

## Agent best practices

- Use `--json` and check `ok` before going on.
- Find ids with `list` or `search`, then act on them. Prefer `url` when
  storing an id.
- Use `list` for titles; call `show` only for the notes you need to read.
- Confirm with the user before `delete`, and never delete from Recently
  Deleted unless asked.

## Error codes

| Code | Meaning |
|------|---------|
| `NOT_AUTHORIZED` | Terminal may not control Notes (Automation permission) |
| `TIMEOUT` | Notes did not answer, often an unanswered permission prompt |
| `NOTE_NOT_FOUND` | No note with that id |
| `FOLDER_NOT_FOUND` | No folder with that name or id |
| `AMBIGUOUS_ID` | Short id matches several notes; use the full `url` |
| `AMBIGUOUS_FOLDER` | Folder name exists in several accounts; use `Account/Folder` or an id |
| `NOTE_LOCKED` | Note is locked |
| `HAS_ATTACHMENTS` | Append refused to keep attachments |
| `MISSING_REQUIRED` | Required argument missing |
| `INVALID_ARGUMENT` | Unknown command or bad value |
