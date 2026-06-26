# ClawDef — Security Documentation

## Overview

ClawDef is a local-only web dashboard for monitoring and optimizing OpenClaw token usage. It runs on `127.0.0.1:3456` and does not send user data to third parties.

## Files Accessed

### Read-only
- `~/.openclaw/openclaw.json` — Current model configuration
- `~/.openclaw/agents/*/sessions/*.jsonl` — Session transcripts (for token counting)
- `/tmp/openclaw/*.log` — Gateway logs (for request tracking)
- `~/.openclaw/workspace/skills/*/SKILL.md` — Installed skill metadata

### Read + Write
- `~/.openclaw/openclaw.json` — Writes to `agents.defaults.model.primary` (model switching) and `skills.entries` (skill enable/disable). No other fields are modified.
- `<install_dir>/data/clawdef.db` — Local SQLite database for monitoring data, user accounts, and optimization logs

## Network Activity

| Destination | Purpose |
|-------------|---------|
| `127.0.0.1:3456` | Web dashboard (served to browser via localhost) |
| `127.0.0.1:11612` | Gateway health check (`GET /health`) and chat proxy |
| User-configured model API URLs | Manual model health checks only |

All frontend assets are served from local files. No CDN dependencies.

## Authentication

- No default password — first-run setup required via web UI
- Passwords stored as bcrypt hashes (10 rounds)
- JWT tokens expire after 7 days
- Three roles: Admin (full), Editor (manage skills/models), Viewer (read-only)

## Code Characteristics

- **No `child_process`** — no shell command execution
- **No `process.env`** — all paths use hardcoded defaults
- **No `eval()` or `Function()`** — no dynamic code execution
- **No outbound network requests** beyond localhost and user-configured model APIs
- **Bound to 127.0.0.1** — not externally accessible by default
- **No telemetry** — no data collection or phone-home

## Dependencies

| Package | Purpose |
|---------|---------|
| express | HTTP server framework |
| better-sqlite3 | Local SQLite database (native module) |
| jsonwebtoken | JWT authentication |
| bcryptjs | Password hashing |
| ws | WebSocket for real-time log streaming |
| chart.js | Dashboard charts (bundled locally, no CDN) |

## Risk Assessment

- **Can modify OpenClaw config**: Yes, but only the `model.primary` field and `skills.entries` section. All writes are logged in the local database.
- **Can control Gateway**: Dashboard offers a "restart Gateway" button that returns a CLI instruction — it does not execute shutdown commands.
- **Reads session data**: Session transcripts contain user conversations. The dashboard only extracts token counts and model names — full conversation content is not stored.
