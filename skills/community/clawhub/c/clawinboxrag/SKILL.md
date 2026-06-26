---
name: ClawInboxRAG
description: Community skill for parsing and executing local mailbox retrieval commands (`mail ...`) against a local backend with safe defaults, bounded output, and read-only constraints.
---

# ClawInboxRAG (Community Skill)

Parse and execute `mail ...` commands for a local mailbox retrieval backend.

## What this skill does

- Parses chat commands with `scripts/parse_mail.py`.
- Routes allowed actions to `scripts/run_cli.sh`.
- Keeps output concise and citation-friendly.
- Enforces safety constraints (read-only posture, limited command surface, bounded result counts).

## Prerequisites

- Local backend checkout.
- Working Python environment and `uv` runner.
- Gmail OAuth read-only scope.
- Environment variables:
  - `GMAIL_RAG_REPO` (required)
  - `GMAIL_RAG_UV_BIN` (optional, default `uv`)
  - `MAIL_DEFAULT_MODE` (`hybrid` default)
  - `MAIL_DEFAULT_LIMIT` (`5` default)
  - `MAIL_MAX_LIMIT` (`25` default)

## Supported input

Trigger: input starts with `mail` (case-insensitive).

Actions recognized by parser:

- `mail help` -> `help`
- `mail status` / `mail stat` -> `status`
- `mail labels` / `mail label` -> `labels`
- `mail sync` -> `sync`
- `mail recents [max|top|limit N]` -> `recents`
- everything else -> `search` (if non-empty query remains)

Search options recognized by parser:

- Mode: `keyword`, `semantic`, `hybrid` (plus localized aliases in parser)
- Limit: `max N`, `top N`, `limit N`, `limite N`
- Label prefix: `label <prefix>` or `tag <prefix>`
- Date filters: `after <date>`, `before <date>`, `between <date> and <date>`
- Summary flag: `resume` (also `résume`, `résumé`, `summary`)

## Command mapping

Use `scripts/run_cli.sh` for execution.

- `help` -> return usage guidance (no CLI call required).
- `search` -> `search <query> [--keyword|--semantic|--hybrid] --limit N [--label-prefix X] [--after ISO] [--before ISO]`
- `recents` -> `recents --limit N`
- `status` -> `status`
- `labels` -> `labels`
- `sync` -> run in order:
  1. `ingest-primary --limit 50`
  2. `embed --limit 200`
  3. `refresh-labels`

## Safety constraints

- Read-only Gmail posture.
- No credential/token disclosure.
- No full raw body dumping by default.
- Clamp numeric limits to configured max.
- Validate date parsing before CLI options.
- Use safe argument passing; do not interpolate untrusted shell strings.
