---
name: codex-sessions-manager
description: Use this skill when the user wants to inspect, search, export, verify, clean up, delete, restore, or purge local Codex sessions.
---

# Codex Sessions Manager

This is a template Skill for using the `codex-sessions` toolkit from an agent workflow. Replace placeholders with paths for the target machine.

## Scope

Use this Skill for local Codex session history stored under a Codex root such as:

```text
<path-to-codex-root>
```

Use the installed CLI:

```bash
npm install -g codex-sessions-manager
```

This provides:

```text
codex-sessions
codex-sessions-mcp
```

For local development, use the repository from:

```text
<path-to-codex-sessions-repo>
```

This Skill is for Codex session inspection and safety operations. It is not for generic chat history, non-Codex clients, or editing the current live conversation.

## Preferred Order

Prefer MCP tools when the `codex-sessions` MCP server is available:

- `inspect_root`
- `list_sessions`
- `list_projects`
- `get_session`
- `export_session_backup`
- `preview_delete_sessions`
- `delete_sessions`
- `list_trash`
- `restore_sessions`
- `purge_trash`
- `cleanup_session_indexes`
- `cleanup_stale_indexes`
- `verify_sessions`

Use CLI only when MCP is unavailable or blocked.

For Codex `/side` conversations, treat the parent thread and side child thread as separate sessions. Do not assume parent operations include side child transcripts. If the user wants both handled, identify the child session IDs first and include them in the preview or confirmed operation.

## CLI Fallback

Prefer the installed CLI:

```bash
codex-sessions doctor --root <path-to-codex-root>
codex-sessions list --root <path-to-codex-root> --limit 20
codex-sessions projects --root <path-to-codex-root>
codex-sessions show <session-id> --root <path-to-codex-root>
codex-sessions export <session-id> --root <path-to-codex-root> --output ./backup.json
codex-sessions delete <session-id> --root <path-to-codex-root>
codex-sessions delete <session-id> --root <path-to-codex-root> --trash
codex-sessions delete <session-id> --root <path-to-codex-root> --trash --yes
codex-sessions trash-list --root <path-to-codex-root>
codex-sessions restore <trash-id-or-session-id> --root <path-to-codex-root> --yes
codex-sessions purge <trash-id-or-session-id> --root <path-to-codex-root> --yes
codex-sessions cleanup-index <session-id> --root <path-to-codex-root>
codex-sessions cleanup-index <session-id> --root <path-to-codex-root> --yes
codex-sessions cleanup-stale --root <path-to-codex-root>
codex-sessions cleanup-stale --root <path-to-codex-root> --yes
codex-sessions verify <session-id> --root <path-to-codex-root>
```

When working from a cloned repository instead, run commands from:

```bash
cd <path-to-codex-sessions-repo>
```

Examples:

```bash
node dist/cli/index.js doctor --root <path-to-codex-root>
node dist/cli/index.js list --root <path-to-codex-root> --limit 20
node dist/cli/index.js projects --root <path-to-codex-root>
node dist/cli/index.js show <session-id> --root <path-to-codex-root>
node dist/cli/index.js export <session-id> --root <path-to-codex-root> --output ./backup.json
node dist/cli/index.js delete <session-id> --root <path-to-codex-root>
node dist/cli/index.js delete <session-id> --root <path-to-codex-root> --trash
node dist/cli/index.js delete <session-id> --root <path-to-codex-root> --trash --yes
node dist/cli/index.js trash-list --root <path-to-codex-root>
node dist/cli/index.js restore <trash-id-or-session-id> --root <path-to-codex-root> --yes
node dist/cli/index.js purge <trash-id-or-session-id> --root <path-to-codex-root> --yes
node dist/cli/index.js cleanup-index <session-id> --root <path-to-codex-root>
node dist/cli/index.js cleanup-index <session-id> --root <path-to-codex-root> --yes
node dist/cli/index.js cleanup-stale --root <path-to-codex-root>
node dist/cli/index.js cleanup-stale --root <path-to-codex-root> --yes
node dist/cli/index.js verify <session-id> --root <path-to-codex-root>
```

## Safety Rules

- Run `inspect_root` or CLI `doctor` before delete, restore, purge, or cleanup when Codex storage may have changed.
- `delete` without `--yes` is preview-only.
- Permanent delete remains available, but prefer recoverable deletion with `--trash --yes`.
- MCP `delete_sessions` requires `confirm=true` to execute. Use `trash=true` for recoverable deletion.
- `restore` and `purge` require `--yes` in CLI mode.
- MCP `restore_sessions` and `purge_trash` require `confirm=true`.
- Restore refuses live session conflicts and SQLite key conflicts. There is no force overwrite mode.
- `purge` removes only the trash entry and must not touch live sessions.
- `cleanup-index` and `cleanup-stale` rewrite JSONL indexes. They do not delete raw files or SQLite rows, but they still require `--yes`.
- MCP `cleanup_session_indexes` and `cleanup_stale_indexes` require `confirm=true` to rewrite indexes.
- Unknown global-state references are warnings only. Do not edit unknown global-state keys automatically.
- If `verify`, `doctor`, or `inspect_root` reports warnings, tell the user. Do not claim the root is fully clean.
- `/side` conversations may be stored as separate child threads. Current CLI/MCP behavior does not automatically recurse from parent to side child threads.

## Non-Goals

Do not build or imply support for:

- UI
- TUI
- detail pages
- incremental project scanning
- automatic stale cleanup
- automatic trash purge
- force overwrite restore
