# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An OpenClaw plugin (`@openclaw-local/bulletin-tools`) that provides a multi-agent bulletin board system. Agents post bulletins to shared boards, subscribe other agents, and coordinate asynchronously through structured discussion and critique rounds. The plugin registers MCP tools that agents call to interact with bulletins, and uses OpenClaw lifecycle hooks to auto-wake agents when they have pending bulletins.

## Development

```bash
npm install          # install deps (better-sqlite3)
```

There is no build step — OpenClaw loads `.ts` files directly via the plugin SDK. There are no tests currently.

## Architecture

**Two files, two layers:**

- `index.ts` — Plugin entry point. Registers three tools (`bulletin_respond`, `bulletin_critique`, `bulletin_list`) via `api.registerTool()` and three lifecycle hooks (`before_agent_start`, `agent_end`, `before_message_write`). Contains all Discord notification logic, spawn-lock management, and completion/escalation workflows.

- `lib/bulletin-db.ts` — SQLite persistence layer using `better-sqlite3`. All DB access is synchronous. Manages schema creation, CRUD, FTS (full-text search), read cursors, and audit logging.

**Runtime data location:** `~/.openclaw/mailroom/bulletins/bulletins.db` (SQLite with WAL mode).

## Key Concepts

**Protocols** determine how a bulletin resolves:
- `advisory` / `consensus` — all subscribers must respond, then a critique round opens automatically
- `majority` — closes as soon as >50% align
- `fyi` — informational only

**Rounds:** Bulletins progress `discussion` → `critique`. Round transitions and bulletin closes use atomic SQL updates (`UPDATE ... WHERE status = 'open'`) to prevent race conditions when multiple agents respond concurrently.

**Agent waking:** When an agent starts (`before_agent_start`), urgent unresponded bulletins trigger a Gateway HTTP call (`/tools/invoke` → `sessions_spawn`) to spawn a dedicated bulletin-response session. Normal bulletins are handled at `agent_end`. Spawn locks (file-based, 10-min TTL) prevent duplicate wake calls.

**Discord integration:** Responses, critiques, dissent alerts, and resolution notices are posted to Discord threads. Config lives in `~/.openclaw/mailroom/bulletin-config.json`. Bot tokens resolve via `${ENV_VAR}` syntax against `process.env` and `~/.openclaw/secrets.json`.

## FTS Content-Sync Warning

The FTS tables (`bulletins_fts`, `responses_fts`) use `content=` mode — they do NOT auto-update. Every INSERT/UPDATE to `bulletins` or `bulletin_responses` must include a corresponding FTS insert/delete within the same transaction. Forgetting this causes search results to go stale or crash.

## External Dependencies

- Gateway API at `127.0.0.1:{port}` (default 18789) for spawning agent sessions.
- Discord notifications (`lib/discord-notify.ts`) are inlined. Long-term these should go through OpenClaw's message tool so the plugin isn't Discord-specific.
