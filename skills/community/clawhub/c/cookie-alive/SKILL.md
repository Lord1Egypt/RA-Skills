---
name: session_cookie_online
description: Persist, refresh, and serve website session cookies through a local SQLite-backed cookie store. Use when Codex needs to keep authenticated cookies alive by calling a lightweight refresh URL on a schedule, save cookies under ~/.cookie_alive/*.db, or hand a Cookie header or JSON cookie map to another program.
---

# Session Cookie Online

## Overview

Use this skill when a website session must stay alive without building a full browser-automation system.

The runtime script stores named session profiles in SQLite, replays a deterministic HTTP keepalive request, merges `Set-Cookie` updates back into the database, and exposes the current cookies to downstream programs.

## Quick Start

1. Pick a database name. The default is `default`, which resolves to `~/.cookie_alive/default.db`.
2. Capture the current cookie as either a `Cookie` header string or a JSON object.
3. Store or update a named profile with `python {baseDir}/scripts/cookie_alive.py upsert ...`.
4. Validate the stored cookie with `python {baseDir}/scripts/cookie_alive.py get --profile <profile>`.
5. Refresh it once with `python {baseDir}/scripts/cookie_alive.py refresh --profile <profile>`.
6. Keep it alive with `python {baseDir}/scripts/cookie_alive.py run --profile <profile>`.

## Workflow Rules

- Prefer a lightweight authenticated endpoint for `--refresh-url`, such as `/ping`, `/me`, or a low-cost page load. Avoid heavy pages when a cheaper endpoint exists.
- Store cookies with `--cookie-header` when the source is browser devtools or another HTTP client. Store them with `--cookie-json` when the source is already structured.
- Use `get --format header` when another program needs a literal `Cookie` header value.
- Use `get --format record` or `list` when another program needs metadata such as `interval_seconds`, `last_status_code`, or `last_refreshed_at`.
- If the target site requires JavaScript timers, WebSocket traffic, or browser-only activity to stay logged in, use external browser automation to renew the cookie and write the updated cookie back with `upsert`. This skill only performs deterministic HTTP requests.

## Script

- `scripts/cookie_alive.py`
  Use this CLI for profile CRUD, one-shot refreshes, and repeat keepalive loops.

## References

- `references/commands.md`
  Load this file for exact CLI shapes, storage path rules, and copy-paste examples.
