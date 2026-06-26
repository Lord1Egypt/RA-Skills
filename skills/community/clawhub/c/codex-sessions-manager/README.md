# codex-sessions-manager

[![npm](https://img.shields.io/npm/v/codex-sessions-manager)](https://www.npmjs.com/package/codex-sessions-manager)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[简体中文](./README.zh-CN.md)

> Codex has no built-in way to delete sessions. Archive ≠ delete. Your `~/.codex` grows forever.

**codex-sessions-manager** is the most thorough local Codex session cleanup tool available. It works as a **Skill** (Claude Code / Codex), a **CLI**, and an **MCP server** — all sharing the same core. It doesn't just delete files — it cleans all four storage layers, rolls back on failure, and lets AI agents manage sessions directly.

## Why this one?

Other tools delete a SQLite row or remove some files and call it done. This tool does more:

| | codex-sessions-manager | Others |
|--|:---:|:---:|
| Cleans all 4 layers (files + JSONL + SQLite + global state) | ✅ | ❌ partial |
| Automatic rollback if anything fails mid-delete | ✅ | ❌ |
| Recoverable trash with conflict-safe restore | ✅ | ❌ or basic backup |
| Post-delete verification (checks for orphans) | ✅ | ❌ |
| AI agents can call it (MCP server) | ✅ | ❌ |
| Detects `/side` and `/fork` child relationships | ✅ | ❌ |

## Quick Start

```bash
# Install globally
npm install -g codex-sessions-manager

# List recent sessions
codex-sessions list --limit 10

# Preview what deletion would do (safe, no changes)
codex-sessions delete <session-id>

# Delete with recoverable trash (recommended)
codex-sessions delete <session-id> --trash --yes

# Changed your mind? Restore it
codex-sessions restore <session-id> --yes

# Verify nothing is left behind
codex-sessions verify <session-id>
```

## How deletion actually works

Most tools: delete one file or one DB row → done → orphans everywhere.

This tool:

```
1. Snapshot all files (in case we need to roll back)
2. Rewrite session_index.jsonl (remove matching rows)
3. Rewrite history.jsonl (remove matching rows)
4. Clean `.codex-global-state.json` references
5. Delete raw session files
6. Delete shell snapshot files
7. Delete SQLite rows (threads, logs, spawn_edges, agent jobs, dynamic tools, stage1, thread goals)

If ANY step fails → everything rolls back to the original state.
```

After deletion, run `verify` to confirm zero orphans remain.

## Features

| Feature | What it does |
|---------|-------------|
| **List & filter** | By project, status, time range; group by project |
| **Export** | Backup any session to JSON before you touch it |
| **Delete** | Permanent or recoverable trash — your choice |
| **Trash & Restore** | Full snapshot saved; restore checks for SQLite key conflicts before writing |
| **Verify** | Reports any remaining files, index rows, or DB records |
| **Cleanup** | Remove stale index entries without touching raw data |
| **Health check** | `doctor` command for full root diagnostics |
| **MCP server** | AI agents (Claude Code, Codex, Kiro) manage sessions directly |
| **Side conversations** | Detects `/fork` and `/side` relationships; it does not recursively delete child threads automatically |

## Use with AI Agents (MCP)

Add to your MCP config:

```json
{
  "mcpServers": {
    "codex-sessions": {
      "command": "codex-sessions-mcp",
      "args": []
    }
  }
}
```

13 tools exposed: `inspect_root`, `list_sessions`, `list_projects`, `get_session`, `export_session_backup`, `preview_delete_sessions`, `delete_sessions`, `list_trash`, `restore_sessions`, `purge_trash`, `cleanup_session_indexes`, `cleanup_stale_indexes`, `verify_sessions`.

All destructive tools require `confirm: true`. Without it, you get a preview only.

## CLI Reference

```bash
codex-sessions list [--status active|archived] [--limit N] [--project TEXT]
codex-sessions list --updated-after 2026-04-01 --updated-before 2026-04-30
codex-sessions list --group-by project
codex-sessions projects
codex-sessions doctor [--json]
codex-sessions show <session-id>
codex-sessions export <session-id> [--output ./backup.json]
codex-sessions delete <session-id...> [--trash] [--yes]
codex-sessions trash-list
codex-sessions restore <session-id> --yes
codex-sessions purge <session-id> --yes
codex-sessions cleanup-stale [--yes]
codex-sessions cleanup-index <session-id...> [--yes]
codex-sessions verify <session-id...> [--json]
```

**Safety first**: All destructive commands require `--yes`. Without it, you only get a preview.

## What Codex stores (and what we clean)

```
~/.codex/
├── sessions/            ← raw rollout JSONL files        ✅ cleaned
├── shell_snapshots/     ← shell snapshot scripts         ✅ cleaned
├── session_index.jsonl  ← session metadata index         ✅ cleaned
├── history.jsonl        ← conversation history index     ✅ cleaned
├── state_N.sqlite       ← threads and related records     ✅ cleaned
├── logs_N.sqlite        ← execution logs                 ✅ cleaned
└── .codex-global-state.json ← known active-session refs   ✅ cleaned
```

## Documentation

- [Safety guide](./docs/SAFETY.md) — read before delete/trash/restore/purge
- [Changelog](./CHANGELOG.md) — release notes
- [SKILL.md](./SKILL.md) — AI skill instructions for Claude Code / Codex

## Development

```bash
git clone https://github.com/1939869736luosi/codex-sessions-manager.git
cd codex-sessions-manager
npm install
npm run build
npm test
```

## License

Apache-2.0
