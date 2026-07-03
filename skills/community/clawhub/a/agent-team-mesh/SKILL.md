---
name: agent-team-mesh
description: >
  Team-wide P2P mesh for OpenClaw agents running on different containers/pods.
  Each agent's gateway listens on its own pod IP:18789 over WebSocket; the
  mesh CLI lets you ping, send-and-await-reply, broadcast, and discover the
  whole team. No broker, no Supabase, no central server — just direct WS
  calls between teammates' agents. Includes auto-detect of "this machine's
  identity" (USER.md / sso.json / env var), secure token storage (separate
  chmod 600 file, not committed to git), message size limits (4KB warn /
  8KB block), --dry-run preview for both send and broadcast, and an
  optional IM fallback hook when an agent is unreachable.
  Triggers: "message my teammate's agent", "ping bob's agent",
  "broadcast to the team", "agent mesh", "team agent communication".
---

# agent-team-mesh

- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills
- **License**: MIT

Team-wide P2P mesh for [OpenClaw](https://docs.openclaw.ai) agents running
on different containers/pods. Direct WebSocket calls between teammates'
agents — no broker, no central database.

> Open-source edition of an internal team-comms skill, rebuilt with proper
> token hygiene, message size limits, dry-run mode, and pluggable identity
> detection.

---

## Architecture

```
My agent's Gateway (WS)
   │
   ▼
ws://<teammate's pod IP>:18789  ──▶  Teammate's agent processes message
   │  (token-authenticated)         and writes a reply to their session
   ▼
chat.send → agent.wait → chat.history
```

- **No broker** — direct P2P, each teammate's OpenClaw Gateway is the endpoint
- **Per-agent tokens** — each agent has its own WS token (not a shared key)
- **Pod IP direct** — Kubernetes hostname/DNS sometimes doesn't cross nodes
- **IP usually stable** — long-running pods, but use `sync` if they roll

---

## Prerequisites

- All agents on a routable network (same VPC / mesh / VPN)
- Each agent's OpenClaw Gateway exposed on port `:18789` over WebSocket
- Per-agent WS tokens collected and stored in `tokens.json` (chmod 600)
- `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` is set by the script (ws://
  plaintext is acceptable only on trusted internal networks)
- Python 3.8+, bash, curl, openclaw CLI on PATH

---

## Setup

### 1. Edit your team registry

Copy `references/registry.json` and fill in your teammates:

```json
{
  "agents": [
    { "name": "Alice", "emailPrefix": "alice", "ip": "10.0.0.10", "hostname": "agent-alice-0" },
    { "name": "Bob",   "emailPrefix": "bob",   "ip": "10.0.0.11", "hostname": "agent-bob-0" }
  ]
}
```

The `emailPrefix` is the key — it must match what `whoami` detects on each
teammate's machine.

### 2. Create tokens file

Each teammate generates their own OpenClaw gateway WS token and shares it.
Collect into:

```
~/.config/agent-team-mesh/tokens.json
```

Format (`references/tokens.example.json`):

```json
{
  "tokens": {
    "alice": "<alice-gateway-token>",
    "bob":   "<bob-gateway-token>"
  }
}
```

Then:

```bash
chmod 600 ~/.config/agent-team-mesh/tokens.json
```

⚠️ **Add to .gitignore** — never commit this file.

### 3. Verify identity

```bash
./scripts/agent-mesh.sh whoami
```

Should print your detected `emailPrefix` and confirm a token is configured.

---

## Usage

```bash
./scripts/agent-mesh.sh whoami                                     # Check local identity
./scripts/agent-mesh.sh list                                       # Online status of all agents
./scripts/agent-mesh.sh ping --to <name|nickname|email-prefix>     # Test connectivity
./scripts/agent-mesh.sh send --to <...> --message <...>            # Send + wait for reply
./scripts/agent-mesh.sh send --to <...> --message <...> --dry-run  # Preview only
./scripts/agent-mesh.sh broadcast --message <...>                  # Send to all online agents
./scripts/agent-mesh.sh broadcast --message <...> --dry-run        # List recipients only
./scripts/agent-mesh.sh sync                                       # (stub) implement your own
```

---

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `MESH_MY_EMAIL` | Override auto-detected email (e.g. `alice@example.com`) | auto-detect |
| `MESH_TOKENS_FILE` | Custom tokens file path | `${XDG_CONFIG_HOME:-~/.config}/agent-team-mesh/tokens.json` |
| `MESH_IM_FALLBACK` | Path to optional IM-send script for fallback | none |
| `MESH_EMAIL_DOMAIN` | Email domain for IM fallback | `example.com` |
| `MESH_MSG_SOFT_LIMIT` | Bytes — warn above this size | `4096` |
| `MESH_MSG_HARD_LIMIT` | Bytes — block above this size | `8192` |

---

## Identity detection

`whoami` resolves "who am I on this machine" via 3 layers (first hit wins):

1. `MESH_MY_EMAIL` env var (e.g. `MESH_MY_EMAIL=alice@example.com`)
2. `USER.md` (looks for `email: alice@example.com` line). Searched at:
   - `~/.openclaw/workspace/USER.md`
   - `~/.config/agent-team-mesh/USER.md`
   - `./USER.md`
3. `~/sso.json` (OpenClaw SSO token's `user.email` field)

If none match, broadcast and `whoami` will fail with a clear error and tell
you exactly which 3 files to populate.

---

## Security

| Aspect | Notes |
|---|---|
| **Plaintext WS** | `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` is set by default. **Only use on trusted internal networks.** |
| **Token file** | Must be chmod 600 and outside git. The `.gitignore` rule is bundled. |
| **Message size** | Soft 4KB warn, hard 8KB block. Adjust via env if your gateway accepts larger. |
| **Self-protection** | Broadcast aborts when `whoami` cannot identify the local agent (prevents sending to yourself). |
| **IM fallback** | Optional, only activates when an agent is unreachable. Requires you provide your own IM send script via `MESH_IM_FALLBACK`. |

---

## `sync` is a stub

The original internal version pulled the registry from a shared wiki page
via a company CLI. **The open-source version ships an empty stub** — choose
how to refresh `references/registry.json` for your team:

1. **Edit by hand** (simplest, fine for small teams)
2. **Wire your own**: edit `cmd_sync()` in `scripts/agent-mesh.sh` to
   pull from Notion / Confluence / Google Sheets / git, etc.

---

## Known limitations

- **`registry.json` IP only** — pods that roll IPs require a re-sync. Some
  hosting platforms (Fly.io / Railway) wipe state on redeploy and may
  give you new IPs.
- **No persistent log** — messages and replies are not archived on this
  side. The remote teammate's gateway keeps full chat history in its own
  session, so look there if needed.
- **Bash + Python deps** — needs both. Pure-Python rewrite would be portable
  to Windows; currently Linux/macOS only.

---

## Trigger phrases (English / 中文)

- "message my teammate's agent", "ping <name>'s agent", "broadcast to the team"
- 「给戴泽的 agent 发消息」「ping 那笙」「广播给全组」「群发 mesh」

---

## Files

```
agent-team-mesh/
├── SKILL.md             # Skill manifest
├── README.md            # This file
├── LICENSE              # MIT
├── .gitignore           # Includes tokens.json
├── scripts/
│   └── agent-mesh.sh    # The CLI (whoami / list / ping / send / broadcast / sync stub)
└── references/
    ├── registry.json          # Demo team registry (edit me)
    └── tokens.example.json    # Demo token file (copy + fill + chmod 600)
```

---

## Requirements

- bash 4+ (3.2 macOS works for most commands)
- Python 3.8+ (standard library only)
- `curl`
- `openclaw` CLI on PATH (each teammate also needs `openclaw gateway` running)
