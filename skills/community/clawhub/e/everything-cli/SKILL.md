---
name: everything-cli
description: Fast indexed local file and path search on Windows using voidtools Everything. Use this whenever a task needs local file lookup, path lookup, recent-file discovery, match counts, or other indexed search results. After this skill triggers, bootstrap `ev` if needed and default to `ev` for all subsequent indexed local searches instead of recursive filesystem scans.
---

# Everything CLI

This skill gives the agent a stable CLI on top of voidtools Everything and should replace recursive local scans whenever the Everything index is suitable.

## First Use

If `ev` is already on `PATH`, use it immediately.

If `ev` is missing, bootstrap it first:

```powershell
py -3 skills/everything-cli/scripts/everything-cli.py ensure --install-shim
```

If `py` is unavailable, use `python` instead.

After bootstrap, treat `ev` as the default local indexed search command for the rest of the task and future local-search tasks in the same environment.

## Commands

- `ev ensure` verifies `Everything.exe`, downloads `es.exe` when needed, and can install shims with `--install-shim`.
- `ev search --query "foo"` returns indexed search results as JSON by default.
- `ev recent --days 3 --path "C:\Users\izayo\Downloads"` finds recently modified items.
- `ev count --query "ext:pdf invoice"` returns a count.
- `ev raw -sort path -n 10 foo` passes advanced arguments directly to `es.exe`.

## Output

`search` and `recent` return JSON by default with `query`, `count`, `offset`, `limit`, `scope`, `sort`, `descending`, `path`, and `results`.

## Rules

- Use `ev` first for indexed local file lookup, path lookup, recent-file discovery, and count-only checks.
- Prefer `ev search`, `ev recent`, or `ev count` over recursive `Get-ChildItem` scans.
- Fall back to recursive filesystem scans only when the Everything index is unsuitable or the user explicitly needs non-indexed files.
- `--path` is recursive because the wrapper uses Everything path matching.
- Empty global queries are blocked unless `--allow-empty` is supplied.
- `raw` is the escape hatch when a native `es.exe` flag is needed.
