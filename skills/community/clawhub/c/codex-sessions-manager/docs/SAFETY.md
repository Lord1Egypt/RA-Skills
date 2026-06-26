# Safety Guide

`codex-sessions` is a local Codex session management toolkit. It provides a CLI and a stdio MCP server for inspecting, listing, exporting, verifying, deleting, moving to trash, restoring, purging, and diagnosing local Codex sessions.

It is not a UI product and does not include a TUI, detail page, incremental project scanner, automatic stale cleanup, or automatic trash purge.

## Root Selection

The default Codex root is:

```text
~/.codex
```

Use `--root` to point the CLI at another Codex root:

```bash
node dist/cli/index.js doctor --root <path-to-codex-root>
```

MCP tools also accept an optional `root` argument.

## Read-Only Operations

These operations are intended to inspect or report information without modifying the Codex root:

| CLI | MCP | Purpose |
|---|---|---|
| `list` | `list_sessions` | List matching sessions |
| `projects` | `list_projects` | Summarize sessions by project |
| `show` | `get_session` | Read one session timeline |
| `export` | `export_session_backup` | Export a backup bundle |
| `doctor` | `inspect_root` | Diagnose root structure and compatibility |
| `verify` | `verify_sessions` | Report remaining files, indexes, SQLite rows, and warnings |
| `trash-list` | `list_trash` | List trash entries |

`doctor` and `inspect_root` are read-only diagnostics. They are intended to detect Codex storage changes, missing files, SQLite table availability, trash state, and global-state warnings.

## Write Operations

These operations modify files or indexes and require explicit confirmation:

| CLI | MCP | Writes |
|---|---|---|
| `delete --yes` | `delete_sessions` with `confirm=true` | Permanently removes live session surfaces |
| `delete --trash --yes` | `delete_sessions` with `trash=true` and `confirm=true` | Writes a trash entry, then removes live session surfaces |
| `restore --yes` | `restore_sessions` with `confirm=true` | Restores a trash entry into live session surfaces |
| `purge --yes` | `purge_trash` with `confirm=true` | Permanently removes a trash entry |
| `cleanup-index --yes` | `cleanup_session_indexes` with `confirm=true` | Rewrites JSONL indexes for selected sessions |
| `cleanup-stale --yes` | `cleanup_stale_indexes` with `confirm=true` | Rewrites JSONL indexes to remove stale rows |

Without `--yes` or `confirm=true`, destructive operations return a preview and do not perform the write.

## Delete, Trash, Restore, and Purge

Permanent delete remains the default delete mode for compatibility. However, `delete` without `--yes` only prints a preview.

For routine cleanup, prefer recoverable trash deletion:

```bash
node dist/cli/index.js delete <session-id> --trash
node dist/cli/index.js delete <session-id> --trash --yes
```

`delete --trash --yes` writes a recoverable trash bundle before removing live session surfaces.

`restore --yes` performs conflict checks before writing. It refuses to restore when a live session surface already contains the same session id or when a SQLite primary-key or unique-key conflict is detected. There is no force overwrite mode.

`purge --yes` removes only the trash entry. It does not touch live sessions.

## Side Conversations

Codex `/side` conversations are separate transcripts. They may appear in local storage as child threads linked to a parent thread.

This matters for safety:

- A parent thread and a side child thread have separate session IDs.
- Showing or exporting a parent thread does not guarantee that side child transcript content is included.
- Deleting a parent thread does not mean the child thread's full transcript is also deleted.
- If you want to handle both, preview both session IDs together before running any confirmed write operation.
- The current CLI/MCP tools do not automatically recurse from a parent thread to its side child threads.

Recommended workflow:

1. Identify the parent thread ID and any side child thread IDs.
2. Preview delete, trash, export, or verify with all IDs that should be covered.
3. Confirm only after the preview matches the intended scope.

## Cleanup Commands

`cleanup-index` and `cleanup-stale` do not delete raw session files or SQLite rows. They rewrite `session_index.jsonl` and `history.jsonl`, so they still require explicit confirmation.

Use preview first:

```bash
node dist/cli/index.js cleanup-stale
```

Execute only after reviewing the preview:

```bash
node dist/cli/index.js cleanup-stale --yes
```

## Global State Warnings

Known global-state cleanup is limited to structured keys that the tool understands.

Unknown global-state references are warnings only. The tool reports them but does not modify unknown keys automatically.

## Testing Safety

Do not experiment with dangerous write operations against a real Codex root.

Use a temporary root for smoke tests:

```bash
tmp="$(mktemp -d)"
node dist/cli/index.js doctor --root "$tmp" --json
node dist/cli/index.js cleanup-stale --root "$tmp"
```

Dangerous tests should always use temporary fixtures or disposable roots.

## Explicit Non-Goals

This project does not provide:

- UI
- TUI
- detail pages
- incremental project scanning
- automatic stale cleanup
- automatic trash purge
- force overwrite restore
- automatic editing of unknown global-state keys
