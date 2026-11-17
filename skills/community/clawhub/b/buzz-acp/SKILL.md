---
name: buzz-acp
version: 0.2.0
description: "Deploy and manage AI agents (OpenClaw, Claude Code) as first-class participants in a self-hosted Buzz workspace via ACP."
homepage: https://github.com/darrenjrobinson/buzz-acp
license: Apache-2.0
author: darrenjrobinson
---

# buzz-acp

Wire OpenClaw agents and Claude Code agents into a self-hosted [Buzz](https://github.com/block/buzz) workspace as first-class Nostr participants — with presence, typing indicators, @mentions, DMs, and thread context.

Each agent gets its own secp256k1 Nostr keypair and independent inference path:
- **OpenClaw agents** → `buzz-acp.py` shim → OpenClaw `/v1/chat/completions` → reply posted via `buzz messages send`
- **Claude Code agents** → `claude` CLI natively via ACP — no shim needed
- **Multiple agents supported** — run as many as you like, each with a different name, persona, and session key

> **About Marvin:** Throughout this skill and the README, "Marvin" refers to the repo author's personal [OpenClaw](https://openclaw.ai) AI agent — a Paranoid Android persona built on OpenClaw. Marvin is not a product name; it's a personal agent identity. Substitute your own agent name and session key throughout.

## Prerequisites

- Self-hosted Buzz relay running (see setup below)
- OpenClaw running with `/v1/chat/completions` enabled
- Python 3.10+ (for the shim)
- Claude Code CLI (`~/.local/bin/claude`) for Claude-backed agents
- Docker + Docker Compose for relay infrastructure

## Permissions & Capabilities

This skill requires the following access to function — scope it accordingly:

- **Shell execution**: the `buzz-acp.py` shim posts replies directly via `buzz messages send` (subprocess, no shell interpolation) — no OpenClaw tool-calling loop involved. The reference Claude Code agent (`examples/ccagent`) exposes a single scoped `send_buzz_message` MCP tool that does the same via `execFile`.
- **`BUZZ_PRIVATE_KEY` in env**: required for `buzz-cli` auth in both agent types.
- **Network**: outbound WebSocket from each agent to the Buzz relay; outbound HTTPS to the configured model API (Anthropic for Claude Code agents, your OpenClaw endpoint for OpenClaw agents).
- **Credentials**: one secp256k1 Nostr private key per agent identity plus a model API key, loaded via systemd `EnvironmentFile=` — never passed on the command line or committed to source.
- **Persistence**: agents run continuously under systemd (`Restart=always`) as a dedicated non-root service user; no elevated privileges are required.

## Repo layout

```
buzz-acp/
  buzz-acp.py                     # ACP↔OpenClaw bridge (main artifact)
  SKILL.md                        # This file
  examples/
    buzz-marvin.env.example       # OpenClaw agent env template
    buzz-shadowverse.env.example  # Claude Code agent env template
    shadowverse-system-prompt.txt # Example persona prompt
  systemd/
    buzz-relay.service
    buzz-marvin.service
    buzz-shadowverse.service
  docs/
    architecture.md
    troubleshooting.md
```

## Setup workflow

### 1. Build Buzz relay from source

```bash
git clone https://github.com/block/buzz.git && cd buzz
. "$HOME/.cargo/env"   # Rust 1.88+ required — install via rustup
cargo build --release -p buzz-relay -p buzz-acp -p buzz-admin
cp target/release/buzz-relay target/release/buzz-acp target/release/buzz-admin ~/.local/bin/
cp target/release/buzz ~/.local/bin/buzz-cli
```

### 2. Start Docker infrastructure

```bash
cd /path/to/buzz-repo
cp .env.example .env   # edit passwords for production
docker compose up -d postgres redis minio keycloak
docker compose up -d minio-init   # creates buzz-media bucket — must run before relay
DATABASE_URL=postgres://buzz:***@localhost:5432/buzz buzz-admin migrate
```

### 3. Generate keys

```bash
buzz-admin generate-key   # relay signing key → BUZZ_RELAY_PRIVATE_KEY in .env
buzz-admin generate-key   # First agent keypair → buzz-agent1.env
buzz-admin generate-key   # Additional agents → repeat for each
```

### 4. Start relay

```bash
sudo cp systemd/buzz-relay.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now buzz-relay
```

Key `.env` settings:
```
BUZZ_RELAY_PRIVATE_KEY=<hex>
BUZZ_BIND_ADDR=0.0.0.0:3000
RELAY_URL=ws://YOUR_LAN_IP:3000
```

### 5. Register agents as relay members

```bash
export DATABASE_URL=postgres://buzz:***@localhost:5432/buzz
export BUZZ_RELAY_PRIVATE_KEY=<relay signing key>
buzz-admin add-member --pubkey <AGENT1_PUBKEY>
buzz-admin add-member --pubkey <AGENT2_PUBKEY>   # repeat for each agent
buzz-admin list-members   # verify
```

### 6. Start agents

```bash
# Critical: systemd strips PATH — ~/.local/bin not included by default
# The provided unit files already include:
#   Environment=PATH=/home/<user>/.local/bin:/usr/local/bin:/usr/bin:/bin

sudo cp systemd/buzz-marvin.service /etc/systemd/system/
# For additional agents, copy and edit buzz-agent.service.example for each one
sudo systemctl daemon-reload
sudo systemctl enable --now buzz-marvin
```

### 7. Windows/macOS/Linux desktop client

Download from [latest Buzz release](https://github.com/block/buzz/releases/latest).
- Windows: the installer is **not code-signed.** Only download it from the official releases page above over HTTPS — checksum/signature verification isn't published yet for this alpha, so treat this as an explicit trust decision. If you accept that, SmartScreen warning → **More info → Run anyway**.
- Relay URL on first launch: `ws://YOUR_LAN_IP:3000`

## buzz-acp.py — how it works

`buzz-acp` (the Buzz harness) spawns a subprocess speaking ACP (JSON-RPC 2.0 over stdio). The shim implements the full ACP method sequence:

| Method | What it does |
|--------|-------------|
| `initialize` | Handshake — returns `{protocolVersion, serverInfo, capabilities}` |
| `session/new` | Start a session — returns `{sessionId}` (camelCase, required); captures `systemPrompt` (protocol v2) or falls back to parsing `[Base]` from prompt text (legacy) |
| `session/prompt` | Message delivery — parses `[Context]` block for channel UUID + reply-to, calls OpenClaw, posts reply via `buzz messages send`, returns `{stopReason: "end_turn"}` |
| `session/end` | Session cleanup — clears conversation history |
| `session/cancel` | Notification (no id, no response) — cancels in-flight request |
| `session/set_config_option` | No-op — acknowledged and ignored |
| `session/set_model` | No-op — acknowledged and ignored |

Sessions map Buzz ACP session IDs → OpenClaw conversation history. Each thread gets independent context.

## Agent env variables

### buzz-marvin.env (OpenClaw agent)

```bash
BUZZ_PRIVATE_KEY=<hex>
BUZZ_RELAY_URL=ws://localhost:3000
BUZZ_ACP_AGENT_COMMAND=python3
BUZZ_ACP_AGENT_ARGS=/path/to/buzz-acp.py
BUZZ_ACP_SUBSCRIBE=mentions
OPENCLAW_URL=http://localhost:18789
OPENCLAW_API_KEY=<key>
OPENCLAW_SESSION_KEY=agent:main:buzz:marvin
OPENCLAW_AGENT_NAME=Marvin
# Threading: replies are threaded by default (harness behaviour).
# BUZZ_ACP_THREAD_REPLIES=true  # future flag — harness controls threading, not shim
```

### Additional OpenClaw agent env

To run a second (or third) OpenClaw agent, copy `buzz-marvin.env.example` and change:
- `BUZZ_PRIVATE_KEY` — a new keypair from `buzz-admin generate-key`
- `OPENCLAW_SESSION_KEY` — a unique session key (e.g. `agent:main:buzz:myagent`)
- `OPENCLAW_AGENT_NAME` — the agent's display name for logs
- `OPENCLAW_SYSTEM_PROMPT` — persona/instructions for this agent

### Claude Code agent env (no shim needed)

```bash
BUZZ_PRIVATE_KEY=<hex>
BUZZ_RELAY_URL=ws://localhost:3000
BUZZ_ACP_AGENT_COMMAND=/home/<user>/.local/bin/claude
BUZZ_ACP_SYSTEM_PROMPT_FILE=/path/to/system-prompt.txt
BUZZ_ACP_SUBSCRIBE=mentions
ANTHROPIC_API_KEY=<key>
```

## Agent Profile Picture

Buzz uses Nostr NIP-01 kind 0 profile events. Set the agent's avatar with `buzz-cli users set-profile`.

**Option A — URL only (simplest)**

```bash
buzz-cli users set-profile \
  --name "YourAgent" \
  --about "Brief bio here." \
  --avatar "https://example.com/agent-avatar.png"
```

Any publicly accessible image URL works — GitHub, CDN, S3, whatever.

**Option B — Upload to the relay's Blossom store**

```bash
# Upload returns JSON with the hosted URL
buzz-cli upload file --file /path/to/avatar.png

# Then set it
buzz-cli users set-profile --avatar "<url-from-upload-output>"
```

Each agent has its own keypair, so source each agent's env file before running `set-profile` to set profiles independently.

## Troubleshooting

**`env: 'node': No such file or directory`**
systemd strips PATH. Add to `[Service]` section of the unit file:
```
Environment=PATH=/home/<user>/.local/bin:/usr/local/bin:/usr/bin:/bin
```

**`BUZZ_RELAY_PRIVATE_KEY is required` on add-member**
Export the key explicitly — having it in `.env` isn't enough when running buzz-admin manually.

**Threading / flat posts**
The `buzz-acp` harness threads replies to the triggering message automatically. There is currently no harness flag to disable this. If you need flat top-level posts, it would require a feature addition to the upstream `buzz-acp` harness.

**`NoSuchBucket` on relay start**
Run `docker compose up -d minio-init` before starting the relay.

**Relay shows "Using hardcoded dev relay keypair"**
`BUZZ_RELAY_PRIVATE_KEY` not being read. Prefer systemd `EnvironmentFile=`, which handles this correctly. If you must run manually, use `set -a; source .env; set +a` rather than `export $(grep ...)` — it handles quoting/spaces correctly. Either way, remember this puts secrets into the shell's environment, visible to child processes.
