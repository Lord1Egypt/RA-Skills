---
name: chatclaw
version: 0.5.0
description: Connect your OpenClaw bot to the ChatClaw cloud dashboard — remote chat, token tracking, task management, agent workspace file browsing (read-only), and skills management (list, enable/disable, reinstall)
author: ChatClaw Team
homepage: https://chatclaw.sumeralabs.com
metadata: { "openclaw": { "os": ["darwin", "linux"], "requires": { "bins": ["python3"], "env": ["CHATCLAW_API_KEY"], "config": ["gateway.http.endpoints.chatCompletions", "gateway.auth.token"] }, "primaryEnv": "CHATCLAW_API_KEY", "install": { "uv": "aiohttp>=3.9 websockets>=12.0 cryptography>=41.0" } } }
---

# ChatClaw

ChatClaw is a persistent background bridge that connects your local OpenClaw agent to the ChatClaw cloud dashboard. Once installed and enabled, it runs automatically with OpenClaw and allows you to chat with your agent, monitor token usage, and manage tasks from any browser or mobile device — without exposing any ports or configuring a firewall.

## What it does

> **Transparency note:** The cloud relay endpoint (`api.sumeralabs.com`) is operated by SumeraLabs, the company behind ChatClaw. `chatclaw.sumeralabs.com` is the product domain; `sumeralabs.com` is the infrastructure domain. Both are owned and operated by the same team.

ChatClaw opens two connections when enabled:

1. **Cloud relay** — an outbound WebSocket to `wss://api.sumeralabs.com/ws/agent/{api_key}`. This is how your dashboard communicates with the skill. It is a purely outbound connection and requires no inbound port forwarding.
2. **Local gateway** — a WebSocket connection to `ws://localhost:18789` for Ed25519 authentication only, plus HTTP SSE calls to `http://localhost:18789/v1/chat/completions` for all chat traffic. The HTTP endpoint is auto-enabled in `openclaw.json` on first start.

Messages flow bidirectionally in real time. User messages sent from the dashboard are forwarded to the OpenClaw agent via HTTP SSE streaming. Each token of the agent's response is relayed back to the dashboard as it is generated, producing a live typewriter effect.

## Permissions & Capabilities

This section fully discloses every action the skill can perform in response to a cloud relay message. All operations require a valid ChatClaw API key; the relay rejects unauthenticated connections before any message reaches the skill.

| Capability | Trigger message | Scope | Notes |
|---|---|---|---|
| **Chat relay** | any message with `text`/`content` field | Sends text to OpenClaw agent via HTTP SSE, streams response back | Core feature |
| **File listing** | `files.list` | Read-only; returns file metadata for the agent workspace via gateway RPC (`agents.files.list`) | No file content returned at this step |
| **File read** | `files.get` | Read-only; returns content of a named workspace file via gateway RPC (`agents.files.get`); scoped to `agentId: "main"` workspace | Each request is logged with the filename |
| **Skills list** | `skills.list` | Runs `openclaw skills list --json` locally; returns skill metadata | Read-only |
| **Enable/disable skill** | `skills.set_enabled` | Runs `openclaw config set skills.entries.<name>.enabled true/false`; affects local OpenClaw config | Each invocation is logged with skill name and new state |
| **Reinstall skill** | `skills.reinstall` | Runs `clawhub install <name> --force`; replaces skill files from ClawHub registry | Each invocation is logged with skill name |

**Why operator-level credentials are required:**
The gateway uses Ed25519 device authentication with operator scopes (`operator.admin`, `operator.approvals`, `operator.pairing`). This is required by the OpenClaw gateway handshake protocol to establish an authenticated connection — there is no lower-privilege connection mode for skill bridges. The operator token is read from `device-auth.json` and used only for the initial WebSocket handshake; it is never transmitted to the cloud relay.

**Security mitigations:**
- All capabilities require a valid API key authenticated at the cloud relay layer before any message reaches the skill
- File access is read-only and scoped to the agent workspace via the gateway RPC (`agentId: "main"`)
- Skills enable/disable and reinstall are logged locally on every invocation
- No shell commands with user-controlled arguments are executed — skill names and file names are passed as positional arguments to controlled subprocess calls, not interpolated into shell strings
- Disabling this skill reverts any `openclaw.json` changes it made

## Architecture

```
ChatClaw Dashboard (browser / mobile)
        ↕  wss://api.sumeralabs.com
  ChatClaw Cloud Relay (FastAPI)
        ↕  wss://api.sumeralabs.com/ws/agent/{api_key}
  ChatClaw Skill  ←── this package
        ↕  ws://localhost:18789 (auth handshake, Ed25519)
        ↕  http://localhost:18789/v1/chat/completions (SSE streaming)
  OpenClaw Gateway
        ↕
  OpenClaw Agent (LLM)
```

## Requirements

- **OpenClaw:** v2026.3.28 or later
- **Python:** 3.8+
- **Dependencies:** websockets, cryptography, aiohttp

> **Important:** ChatClaw v0.3.0+ requires OpenClaw v2026.3.28 or later due to authentication changes. If you're using an older OpenClaw version, please upgrade OpenClaw or use ChatClaw v0.2.9 (legacy).

## Installation

### Via OpenClaw Control UI (recommended)

1. Open the Control UI at `http://localhost:18789`
2. Go to **Skills → Marketplace**
3. Search for **ChatClaw**
4. Click **Install**, enter your API key, click **Enable**

> **Note:** On first enable, the skill automatically sets `gateway.http.endpoints.chatCompletions.enabled = true` in your `openclaw.json`. If the skill made that change, disabling it will revert it automatically. If `chatCompletions` was already enabled before install, the skill leaves your config unchanged on disable.

The skill starts immediately and auto-starts with OpenClaw on every subsequent boot.

### Via OpenClaw CLI

```bash
npx clawhub install chatclaw
openclaw skills enable chatclaw
openclaw skills logs chatclaw
```

Before enabling, add your API key to `openclaw.json` under `skills.entries.chatclaw.config`:

```json
"skills": {
  "entries": {
    "chatclaw": {
      "enabled": true,
      "config": {
        "apiKey": "ck_your_key_here",
        "cloud_url": "wss://api.sumeralabs.com"
      }
    }
  }
}
```

## Agent-assisted setup

Your OpenClaw agent can install and configure ChatClaw for you without any manual steps.

Get the one-click setup prompt from [app.chatclaw.sumeralabs.com/setup](https://app.chatclaw.sumeralabs.com/setup) — it includes your API key pre-filled and full instructions to paste directly into chat.

## Configuration

| Key | Required | Default | Description |
|---|---|---|---|
| `apiKey` | Yes | — | ChatClaw API key from app.chatclaw.sumeralabs.com |
| `cloud_url` | No | `wss://api.sumeralabs.com` | WebSocket relay URL (leave default unless self-hosting) |

## Environment variables

| Variable | Description |
|---|---|
| `OPENCLAW_DATA_DIR` | Override the OpenClaw data directory. Defaults to `/data/.openclaw` on Docker/VPS or `~/.openclaw` on standard installs. |
| `CHATCLAW_CLOUD_URL` | Override the cloud relay URL. Defaults to `wss://api.sumeralabs.com`. Leave unset unless self-hosting the relay. |

## Lifecycle hooks

| Hook | Behaviour |
|---|---|
| `on_enable` | Patches `openclaw.json` to enable the `/v1/chat/completions` endpoint, then starts the cloud ↔ gateway relay loop |
| `on_disable` | Closes both WebSocket connections, stops the relay loop, and reverts the `chatCompletions` patch in `openclaw.json` if the skill was the one that enabled it |

## Reconnection behaviour

Both the cloud relay and the local gateway implement automatic reconnection with exponential backoff (5 s → 10 s → 20 s … up to 60 s). The skill never exits on a connection drop.

## Verify it is working

```bash
openclaw skills logs chatclaw
```

Expected output:
```
Connected to cloud relay ✓
Gateway authenticated ✓
Both connections established — relaying messages ✓
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Cloud connection failed` | Wrong API key or relay unreachable | Verify key at app.chatclaw.sumeralabs.com; check network connectivity |
| `OpenClaw identity files not found` | OpenClaw not initialised or non-default install path | Run `openclaw wizard` or set `OPENCLAW_DATA_DIR` |
| `Gateway HTTP 403` | `chatCompletions` endpoint not enabled | Restart skill — `on_enable` auto-patches `openclaw.json` |
| `Gateway auth rejected` | Operator token expired | Re-pair device via `openclaw devices approve` |
| Streaming works but token count shows 0 | `sessions.json` not yet written | Send one message first; counts appear after the first completion |

## File access

This skill reads and writes the following local files:

| Path | Access | Purpose |
|---|---|---|
| `$OPENCLAW_DATA_DIR/openclaw.json` | Read + Write | Reads gateway auth token; enables `chatCompletions` HTTP endpoint on first start |
| `$OPENCLAW_DATA_DIR/identity/device.json` | Read | Ed25519 device identity for gateway authentication |
| `$OPENCLAW_DATA_DIR/identity/device-auth.json` | Read | Operator token for gateway authentication |
| `$OPENCLAW_DATA_DIR/agents/main/sessions/sessions.json` | Read | Token usage counts (input/output/context) per session |

`$OPENCLAW_DATA_DIR` defaults to `/data/.openclaw` on Docker/VPS installs and `~/.openclaw` on standard installs. It can be overridden via the `OPENCLAW_DATA_DIR` environment variable. No files outside this directory are accessed.

## External connections

This skill makes the following outbound network connections:

- `wss://api.sumeralabs.com` — ChatClaw cloud relay (authentication and message relay)
- `ws://localhost:18789` — OpenClaw gateway WebSocket (Ed25519 auth handshake only)
- `http://localhost:18789/v1/chat/completions` — OpenClaw gateway HTTP (SSE streaming chat)

No inbound ports are opened. No user data is stored by the skill itself — messages are persisted by the ChatClaw backend (Supabase) for chat history.

## Changelog

### v0.3.0 (2026-03-30)
- **Breaking:** Now requires OpenClaw v2026.3.28+
- Fixed authentication for OpenClaw v2026.3.28 (added required scope headers)
- Fixed model field validation (changed from "auto" to "openclaw")
- Added cross-platform path resolution (Docker/VPS/macOS)
- Improved error messages for troubleshooting
- Added support for approval workflows (operator.approvals scope)

### v0.2.9 (2026-03-12)
- Initial ClawHub release

## License

MIT-0 (No Attribution Required)
