---
name: codex-sessions-manager
description: Use this skill when the user wants to inspect, search, export, verify, clean up, delete, restore, or purge local Codex sessions stored under a Codex root such as ~/.codex.
metadata:
  source: https://github.com/1939869736luosi/codex-sessions-manager
---

# Codex Sessions Manager

## Overview

This skill manages local Codex sessions through the `codex-sessions` toolkit.

Use it when the user wants to work with local Codex conversation history instead of the current live conversation.

This repository provides:

- a Node / TypeScript CLI
- a local stdio MCP server
- this Skill entrypoint

The project is not a UI product, TUI, detail page, incremental scanner, or automatic cleanup service.

## Setup

Install the CLI before using fallback commands:

```bash
npm install -g codex-sessions-manager
```

This provides:

```text
codex-sessions
codex-sessions-mcp
```

For local development, build the repository first:

```bash
cd <path-to-codex-sessions-repo>
npm install
npm run build
```

The default Codex root is:

```text
~/.codex
```

Use `--root <path-to-codex-root>` when working with another Codex root.

## When To Use

Use this skill for requests like:

- "List my recent Codex sessions"
- "Find sessions for this project"
- "Show this session"
- "Find side conversations for this session"
- "Export this session"
- "Preview deleting these sessions"
- "Move these sessions to trash"
- "Restore this trash entry"
- "Purge this trash entry"
- "Verify whether this session is fully removed"
- "Inspect the Codex root before deleting or restoring"
- "Clean stale JSONL indexes"

Do not use this skill for:

- generic ChatGPT history questions
- non-Codex chat clients
- editing the current live conversation
- automatic cleanup schedules
- provider or model repair

## Preferred Order

### 1. Prefer MCP first

If the `codex-sessions` MCP server is available in the current agent session, use these tools:

- `inspect_root`
- `list_sessions`
- `list_projects`
- `get_session`
- `export_session_backup`
- `preview_delete_sessions`
- `delete_sessions` (requires `confirm=true` to execute; pass `trash=true` for recoverable deletion)
- `list_trash`
- `restore_sessions` (requires `confirm=true`)
- `purge_trash` (requires `confirm=true`)
- `cleanup_session_indexes` (requires `confirm=true` to rewrite JSONL indexes)
- `cleanup_stale_indexes` (requires `confirm=true` to rewrite JSONL indexes)
- `verify_sessions`

Use MCP tools first. CLI is the fallback when MCP is unavailable or blocked.

For session lookup, narrow in this order:

1. project
2. status
3. updated / created time
4. preview or `get_session`

For project-aware listing, pass `project` to `list_sessions` or use `groupBy="project"`.

For time filters, pass `updatedAfter`, `updatedBefore`, `createdAfter`, or `createdBefore`. Date-only filters use the local calendar day. Timezone-less datetime strings must be rejected.

### 2. Fall back to CLI

Prefer the installed CLI:

```bash
codex-sessions doctor --root <path-to-codex-root>
codex-sessions doctor --root <path-to-codex-root> --json
codex-sessions list --root <path-to-codex-root> --limit 20
codex-sessions list --root <path-to-codex-root> --project TEXT
codex-sessions list --root <path-to-codex-root> --group-by project
codex-sessions list --root <path-to-codex-root> --updated-after 2026-04-01 --updated-before 2026-04-30
codex-sessions projects --root <path-to-codex-root>
codex-sessions show <session-id> --root <path-to-codex-root>
codex-sessions export <session-id> --root <path-to-codex-root> --output ./backup.json
codex-sessions delete <session-id...> --root <path-to-codex-root>
codex-sessions delete <session-id...> --root <path-to-codex-root> --yes
codex-sessions delete <session-id...> --root <path-to-codex-root> --trash
codex-sessions delete <session-id...> --root <path-to-codex-root> --trash --yes
codex-sessions trash-list --root <path-to-codex-root>
codex-sessions restore <trash-id-or-session-id> --root <path-to-codex-root>
codex-sessions restore <trash-id-or-session-id> --root <path-to-codex-root> --yes
codex-sessions purge <trash-id-or-session-id> --root <path-to-codex-root>
codex-sessions purge <trash-id-or-session-id> --root <path-to-codex-root> --yes
codex-sessions cleanup-index <session-id...> --root <path-to-codex-root>
codex-sessions cleanup-index <session-id...> --root <path-to-codex-root> --yes
codex-sessions cleanup-stale --root <path-to-codex-root>
codex-sessions cleanup-stale --root <path-to-codex-root> --yes
codex-sessions verify <session-id...> --root <path-to-codex-root>
```

When working from a cloned repository instead, run commands from the built repository:

```bash
cd <path-to-codex-sessions-repo>
```

Commands:

```bash
node dist/cli/index.js doctor --root <path-to-codex-root>
node dist/cli/index.js doctor --root <path-to-codex-root> --json
node dist/cli/index.js list --root <path-to-codex-root> --limit 20
node dist/cli/index.js list --root <path-to-codex-root> --project TEXT
node dist/cli/index.js list --root <path-to-codex-root> --group-by project
node dist/cli/index.js list --root <path-to-codex-root> --updated-after 2026-04-01 --updated-before 2026-04-30
node dist/cli/index.js projects --root <path-to-codex-root>
node dist/cli/index.js show <session-id> --root <path-to-codex-root>
node dist/cli/index.js export <session-id> --root <path-to-codex-root> --output ./backup.json
node dist/cli/index.js delete <session-id...> --root <path-to-codex-root>
node dist/cli/index.js delete <session-id...> --root <path-to-codex-root> --yes
node dist/cli/index.js delete <session-id...> --root <path-to-codex-root> --trash
node dist/cli/index.js delete <session-id...> --root <path-to-codex-root> --trash --yes
node dist/cli/index.js trash-list --root <path-to-codex-root>
node dist/cli/index.js restore <trash-id-or-session-id> --root <path-to-codex-root>
node dist/cli/index.js restore <trash-id-or-session-id> --root <path-to-codex-root> --yes
node dist/cli/index.js purge <trash-id-or-session-id> --root <path-to-codex-root>
node dist/cli/index.js purge <trash-id-or-session-id> --root <path-to-codex-root> --yes
node dist/cli/index.js cleanup-index <session-id...> --root <path-to-codex-root>
node dist/cli/index.js cleanup-index <session-id...> --root <path-to-codex-root> --yes
node dist/cli/index.js cleanup-stale --root <path-to-codex-root>
node dist/cli/index.js cleanup-stale --root <path-to-codex-root> --yes
node dist/cli/index.js verify <session-id...> --root <path-to-codex-root>
```

## Safety Rules

- Run MCP `inspect_root` or CLI `doctor` before delete, restore, purge, or cleanup when Codex storage may have changed.
- Treat delete, restore, purge, and cleanup as dangerous write paths.
- Always preview before destructive actions unless the user has already clearly confirmed execution.
- CLI `delete` without `--yes` is preview-only.
- MCP `delete_sessions` without `confirm=true` is preview-only.
- Permanent delete remains available for compatibility.
- Prefer recoverable deletion with CLI `--trash --yes` or MCP `trash=true, confirm=true`.
- `delete --trash` without `--yes` only previews moving sessions to trash.
- `restore` and `purge` require `--yes` in CLI mode.
- MCP `restore_sessions` and `purge_trash` require `confirm=true`.
- Restore refuses live session conflicts and SQLite key conflicts. There is no force overwrite mode.
- `purge` removes only the trash entry and must not touch live sessions.
- `cleanup-index` and `cleanup-stale` rewrite `session_index.jsonl` and `history.jsonl`. They do not delete raw files or SQLite rows, but they still require `--yes`.
- MCP `cleanup_session_indexes` and `cleanup_stale_indexes` require `confirm=true` to rewrite JSONL indexes.
- Global-state cleanup is limited to known structured keys.
- Unknown global-state references are warnings only. Do not edit or delete unknown keys automatically.
- If `verify`, `doctor`, or `inspect_root` reports warnings, tell the user. Do not claim the root is fully clean.
- Do not output chat content when reporting doctor, verify, or global-state warnings.

## Side Conversations

Codex `/side` creates an ephemeral side conversation with a separate transcript. In local storage, it can appear as a separate child thread linked to a parent thread.

When a user asks about side conversations:

- Treat the parent thread and side child thread as separate sessions with separate transcripts.
- Search, show, export, delete, trash, restore, or verify the child thread by its own session ID.
- Do not assume deleting, exporting, or summarizing a parent thread also handles its side child threads.
- If the user wants a parent thread and its side conversations handled together, identify the child thread IDs first, preview all selected IDs together, and only then run any confirmed write operation.
- Current CLI/MCP behavior does not automatically recurse from parent to side child threads.

## Response Style

- For list requests: show session ID, updated time, size, project, status, and readable title.
- For project requests: show project name/path, session count, status counts, latest updated time, and total size.
- For show requests: summarize the session and include key metadata.
- For side-conversation requests: distinguish parent thread ID and child thread ID, and say whether the requested action covers one or both.
- For delete requests: explain whether this is preview-only, permanent delete, or recoverable trash delete.
- For trash requests: distinguish moved to trash, restored, and purged.
- For restore conflicts: explain that the live session already exists and identify conflicting surfaces when available.
- For verify requests: report whether files, JSONL rows, SQLite rows, shell snapshots, global-state refs, or warnings remain.
- For doctor / inspect requests: report OK, missing, and warning states without printing chat content.
- For unknown global-state refs: report key path and count, not full global state content.

## Non-Goals

Do not build or imply support for:

- UI
- TUI
- detail pages
- incremental project scanning
- automatic stale cleanup
- automatic trash purge
- force overwrite restore
- automatic editing of unknown global-state keys
- non-Codex chat cleanup
