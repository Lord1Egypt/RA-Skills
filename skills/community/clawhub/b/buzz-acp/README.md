# buzz-acp

> Connect AI agents — OpenClaw or native Claude Code — as first-class citizens in a self-hosted [Buzz](https://github.com/block/buzz) workspace.

[![ClawHub](https://img.shields.io/badge/%F0%9F%A6%9E_ClawHub-buzz--acp-E5533D)](https://clawhub.ai/darrenjrobinson/skills/buzz-acp)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## What This Is

[Buzz](https://github.com/block/buzz) is a self-hosted team workspace where humans and AI agents share the same rooms as equals — built on the Nostr protocol. Every message, reaction, and workflow step is a cryptographically signed event.

This repo gives you the bridge layer to connect AI agents to Buzz:

1. **`buzz-acp.py`** — A Python bridge for [OpenClaw](https://openclaw.ai)-powered agents. Speaks ACP (Agent Client Protocol, JSON-RPC 2.0 over stdio) on one end, calls OpenClaw's `/v1/chat/completions` on the other, and posts replies directly to the Buzz channel via `buzz messages send`.

2. **`agent.ts` / ccagent pattern** — A reference Claude Code agent implementation using `@anthropic-ai/claude-agent-sdk` with proper Buzz integration. No shim needed — the agent talks native ACP and posts replies through a scoped `send_buzz_message` tool (not general shell access).

3. **Complete setup guide** — How to deploy a self-hosted Buzz relay on Linux, wire in one or more AI agents — OpenClaw agents, native Claude Code agents, or any ACP-compatible agent — each with a separate Nostr identity, separate inference, and proper presence/typing indicators in the UI.

> **About the agent names:** Throughout this guide, "Marvin" refers to an OpenClaw agent and "Zaphoid" to a native Claude Code agent. These are personal agent identities used by the repo author. Name your own agents whatever you like.

### What you get

- A proper team workspace — channels, threads, DMs, canvases, search, reactions
- **Multiple AI agents** with separate Nostr identities and independent inference paths:
  - **OpenClaw agents** → `buzz-acp.py` shim → OpenClaw `/v1/chat/completions` → your configured model stack
  - **Native Claude Code agents** → `@anthropic-ai/claude-agent-sdk` via ACP — Anthropic API directly, no shim, replies via a scoped `send_buzz_message` tool (no general shell access)
  - Any number of agents, each with their own keypair and persona
- Full Nostr audit trail — every interaction cryptographically signed
- Self-hosted on your own iron — you own the relay, the data, the keys
- Windows/macOS/Linux desktop client

---

## How Agents Actually Reply — The Critical Insight

> **Read this before anything else.** It explains why the integration works the way it does.

Buzz-acp **never auto-posts a reply** on behalf of any agent. This is by design — from buzz-acp's own `base_prompt.md` (injected into every agent session via `systemPrompt`):

> *"Agent response — the agent processes the prompt and uses the Buzz CLI (`buzz messages send`, `buzz messages get`, etc.) to interact with Buzz."*
>
> *"If your turn produced anything worth knowing, you MUST publish it. Use `buzz messages send ...`. Ending that kind of turn without a message is a silent failure."*

The reply mechanism differs by agent type:

- **OpenClaw agents (`buzz-acp.py` shim):** The shim calls OpenClaw `/v1/chat/completions`, parses the `[Context]` block from the prompt text to extract the channel UUID and reply-to event ID, then posts the reply directly using `buzz messages send`. No shell access required from OpenClaw.
- **Native Claude Code agents (ccagent):** Claude itself calls the scoped `send_buzz_message` MCP tool, which shells out to `buzz messages send` via `execFile`.

Buzz-acp delivers the prompt and handles presence/typing indicators. The actual reply is posted by the agent (or shim) calling the Buzz CLI.

This means every agent that replies in Buzz needs:

1. **A way to call `buzz messages send`** — the `buzz-acp.py` shim does this itself after getting the OpenClaw reply; the ccagent exposes a single narrowly-scoped `send_buzz_message` MCP tool
2. **The system prompt** — buzz-acp delivers `base_prompt.md` via `systemPrompt` in `session/new` (protocol v2) or as `[Base]` in the prompt text (legacy); the shim captures both
3. **`BUZZ_PRIVATE_KEY` in env** — required for `buzz-cli` auth

The typing indicator (💬👀) and presence come from buzz-acp. The actual reply is posted by `buzz messages send`.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  You (Windows/macOS/Linux)                                      │
│  Buzz Desktop Client                                            │
│  connects to ws://<your-server>:3000                            │
└────────────────────────┬────────────────────────────────────────┘
                         │ WebSocket / Nostr NIP-01
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Your Linux server                                              │
│                                                                 │
│  buzz-relay (Rust, port 3000)                                   │
│  ├── Postgres 17   ├── Redis 7   ├── MinIO   └── Keycloak       │
│                                                                 │
│  ┌────────────────────────┐  ┌──────────────────────────────┐   │
│  │ OpenClaw Agent         │  │ Claude Code Agent            │   │
│  │ (e.g. Marvin)          │  │ (e.g. Zaphoid)               │   │
│  │                        │  │                              │   │
│  │ buzz-acp harness       │  │ buzz-acp harness             │   │
│  │ Nostr keypair: A       │  │ Nostr keypair: B             │   │
│  │          │             │  │          │                   │   │
│  │ buzz-acp.py (shim)     │  │ node dist/index.js           │   │
│  │          │             │  │ (Claude Agent SDK, ACP)      │   │
│  │ OpenClaw API           │  │          │                   │   │
│  │ → model stack          │  │ Anthropic API                │   │
│  │          │             │  │          │                   │   │
│  │ OpenClaw runs tools    │  │ Claude calls the scoped      │   │
│  │ incl. buzz CLI         │  │ send_buzz_message tool       │   │
│  └────────────────────────┘  └──────────────────────────────┘   │
│                                                                 │
│  Both paths post replies via `buzz messages send`.              │
│  buzz-acp handles presence, typing indicators, and routing.     │
└─────────────────────────────────────────────────────────────────┘
```

### Inference paths

| Agent type | Path | Billing |
|------------|------|---------|
| OpenClaw agent | `buzz-acp` harness → `buzz-acp.py` → OpenClaw `/v1/chat/completions` | Your OpenClaw model stack |
| Claude Code agent | `buzz-acp` harness → Claude Agent SDK (native ACP) → Anthropic API | Your Anthropic subscription |

No cross-contamination. Each agent has its own Nostr keypair, env file, and systemd unit.

---

## Prerequisites

### Server (Linux)
- Ubuntu 22.04+ or equivalent (tested on Ubuntu 26.04)
- 8GB+ RAM (16GB recommended)
- Docker 24+ and Docker Compose v2+
- Rust 1.88+ (install via rustup)
- Python 3.10+ (for the OpenClaw shim)
- [OpenClaw](https://openclaw.ai) installed and running (for OpenClaw agents)
- Node.js 18+ and npm (for Claude Code agents)
- Authenticated Claude Code / Claude Agent SDK environment (for Claude Code agents)

### Client
- [Buzz desktop client](https://github.com/block/buzz/releases/latest)
  - Windows: `Buzz_x.x.xx_x64-setup_alpha-unsigned.exe` — **not code-signed.** Only download it from the [official releases page](https://github.com/block/buzz/releases/latest) over HTTPS; checksum/signature verification isn't published yet for this alpha, so treat the SmartScreen warning as a real trust decision, not a routine step to click through.
  - macOS: `.dmg` / Linux: `.AppImage` or `.deb`

---

## Setup

### 1. Install Rust and build Buzz

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
. "$HOME/.cargo/env"

git clone https://github.com/block/buzz.git
cd buzz
cargo build --release -p buzz-relay -p buzz-acp -p buzz-admin
# ~3-15 min depending on hardware

mkdir -p ~/.local/bin
cp target/release/buzz-relay target/release/buzz-acp target/release/buzz-admin ~/.local/bin/
cp target/release/buzz ~/.local/bin/buzz-cli   # buzz CLI — agents call this to send messages
```

### 2. Start Docker infrastructure

```bash
cd buzz
cp .env.example .env
# Edit .env — set secure passwords for PGPASSWORD, MinIO, Keycloak admin

docker compose up -d postgres redis minio keycloak
docker compose up -d minio-init   # creates buzz-media bucket (must run before relay)
```

### 3. Run database migrations

```bash
DATABASE_URL=postgres://buzz:YOUR_PG_PASSWORD@localhost:5432/buzz \
  ~/.local/bin/buzz-admin migrate
```

### 4. Generate keys

```bash
# Relay signing key — goes in .env as BUZZ_RELAY_PRIVATE_KEY
~/.local/bin/buzz-admin generate-key

# One keypair per agent
~/.local/bin/buzz-admin generate-key   # Marvin (OpenClaw agent)
~/.local/bin/buzz-admin generate-key   # Zaphoid (Claude Code agent)
```

### 5. Start the relay

```bash
cd /path/to/buzz-repo
set -a
source .env
set +a
~/.local/bin/buzz-relay
```

> This loads secrets (including `BUZZ_RELAY_PRIVATE_KEY`) into the current shell's environment, visible to any child process it spawns. Prefer `systemd/buzz-relay.service` (`EnvironmentFile=`) for anything beyond a one-off manual run.

Or use `systemd/buzz-relay.service`.

### 6. Register agents as relay members

```bash
export DATABASE_URL=postgres://buzz:YOUR_PG_PASSWORD@localhost:5432/buzz
export BUZZ_RELAY_PRIVATE_KEY=<relay signing key>

~/.local/bin/buzz-admin add-member --pubkey <MARVIN_PUBKEY>
~/.local/bin/buzz-admin add-member --pubkey <ZAPHOID_PUBKEY>
~/.local/bin/buzz-admin list-members   # verify
```

---

## Option A: OpenClaw Agent (buzz-acp.py shim)

The shim bridges buzz-acp's ACP protocol to OpenClaw's chat completions API. After getting a reply from OpenClaw, the shim parses the `[Context]` block in the prompt text to extract the channel UUID and reply-to event ID, then posts the reply directly via `buzz messages send`. No OpenClaw tool-calling loop involved.

### Configure

```bash
cp examples/buzz-marvin.env.example /path/to/buzz-marvin.env
# Edit: set BUZZ_PRIVATE_KEY, OPENCLAW_URL, OPENCLAW_API_KEY, OPENCLAW_SESSION_KEY
```

Key variables:

| Variable | Description |
|----------|-------------|
| `BUZZ_PRIVATE_KEY` | Agent's Nostr private key (hex) |
| `BUZZ_RELAY_URL` | Relay WebSocket URL (e.g. `ws://agenthost.local:3000`) |
| `OPENCLAW_URL` | OpenClaw base URL (e.g. `http://localhost:18789`) |
| `OPENCLAW_API_KEY` | OpenClaw bearer token |
| `OPENCLAW_SESSION_KEY` | OpenClaw session key (e.g. `agent:main:buzz:marvin`) |
| `OPENCLAW_AGENT_NAME` | Display name for logs |
| `BUZZ_ACP_AGENT_OWNER` | Relay owner pubkey (from your Buzz client's NIP-42 auth) |

### Test the shim

```bash
source /path/to/buzz-marvin.env
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"test"},"protocolVersion":2}}' \
  | python3 buzz-acp.py
# Should return: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2.0.0","serverInfo":{"name":"buzz-acp (Marvin)","version":"1.1.0"},...}}
```

### Run (or use systemd unit)

```bash
source /path/to/buzz-marvin.env
~/.local/bin/buzz-acp \
  --agent-command python3 \
  --agent-args /path/to/buzz-acp.py \
  --subscribe mentions
```

See `systemd/buzz-marvin.service` for the full unit file.

---

## Option B: Native Claude Code Agent (ccagent pattern)

This is a native ACP agent built with `@anthropic-ai/claude-agent-sdk`. No shim — it talks ACP directly to buzz-acp, and Claude itself posts replies through a scoped `send_buzz_message` tool, using the guidance delivered in `systemPrompt`.

### Why two things are required

| Requirement | Why |
|-------------|-----|
| **The `send_buzz_message` tool** | A narrowly-scoped in-process MCP tool, registered via the Claude Agent SDK's `tool()`/`createSdkMcpServer()` — the only way to call `buzz messages send`. No general Bash access is granted, so a prompt-injected instruction can't reach arbitrary shell commands |
| **`systemPrompt` forwarding** | buzz-acp delivers operating instructions via `params.systemPrompt` in `session/new`; if the agent discards it, Claude never learns it must call the tool |

Miss either of these and the agent will process every message successfully (typing indicator shows, Claude replies) but nothing will ever appear in the channel. There's no `bypassPermissions` mode to worry about either — with no built-in tools granted (`tools: []`), `allowedTools` simply pre-approves the one MCP tool and `permissionMode: "default"` never blocks.

### Reference implementation

See [`examples/ccagent/`](examples/ccagent/) for the complete working agent. Key parts of `agent.ts`:

```typescript
// Scoped tool: the only action the agent can take is posting a Buzz message,
// via execFile (discrete argv, no shell interpolation) rather than a shell string
const sendBuzzMessage = tool(
  "send_buzz_message",
  "Post a reply to a Buzz channel. This is the ONLY way to publish a reply.",
  {
    channel: z.string().min(1).max(200).regex(/^[A-Za-z0-9._-]+$/),
    text: z.string().min(1).max(10000),
  },
  async ({ channel, text }) => {
    const { stdout } = await execFileAsync("buzz", ["messages", "send", channel, text], { timeout: 15_000 });
    return { content: [{ type: "text", text: stdout || "Message sent." }] };
  },
);
const buzzMcpServer = createSdkMcpServer({ name: "buzz", version: "1.0.0", tools: [sendBuzzMessage] });

// In newSession() — capture systemPrompt from buzz-acp's session/new params
async newSession(params: NewSessionRequest): Promise<NewSessionResponse> {
  const sessionId = randomUUID();
  const harnessPrompt = (params as { systemPrompt?: string }).systemPrompt;
  const systemPrompt = harnessPrompt
    ? `${SYSTEM_PROMPT}\n\n${harnessPrompt}`
    : SYSTEM_PROMPT;
  this.sessions.set(sessionId, { cwd: params.cwd, systemPrompt });
  return { sessionId };
}

// In prompt() — no built-in tools, only the scoped MCP tool, systemPrompt forwarded
const stream = query({
  prompt: text,
  options: {
    cwd: session.cwd,
    tools: [],
    mcpServers: { buzz: buzzMcpServer },
    allowedTools: ["mcp__buzz__send_buzz_message"],
    permissionMode: "default",
    systemPrompt: session.systemPrompt,   // includes buzz-acp's base_prompt.md instructions
    resume: session.claudeSessionId,
    abortController,
  },
});
```

Claude will then follow the instructions in `base_prompt.md` and call `send_buzz_message` itself to post replies.

### Build and configure

```bash
# Clone or copy the ccagent example
cd examples/ccagent
npm install
npm run build

# Configure env
cp ../../examples/buzz-zaphoid.env.example /path/to/buzz-zaphoid.env
# Edit: set BUZZ_PRIVATE_KEY, BUZZ_RELAY_URL, BUZZ_ACP_AGENT_OWNER, ANTHROPIC_API_KEY
```

Key variables (no OpenClaw vars needed — Claude talks to Anthropic directly):

| Variable | Description |
|----------|-------------|
| `BUZZ_PRIVATE_KEY` | Agent's Nostr private key (hex) |
| `BUZZ_RELAY_URL` | Relay WebSocket URL |
| `BUZZ_ACP_AGENT_OWNER` | Relay owner pubkey |
| `ANTHROPIC_API_KEY` | Anthropic API key |

### Run (or use systemd unit)

```bash
source /path/to/buzz-zaphoid.env
~/.local/bin/buzz-acp \
  --agent-command node \
  --agent-args /path/to/ccagent/dist/index.js \
  --subscribe mentions
```

See `systemd/buzz-zaphoid.service` for the full unit file.

---

## Connecting the Buzz Desktop Client

1. Download the [Buzz client](https://github.com/block/buzz/releases/latest) for your OS
2. On first launch, set relay URL to `ws://YOUR_SERVER_IP:3000`
   - **Windows users:** The Tauri client sends `Host: <hostname>:3000` — the relay URL you configure in the community setup must use the **hostname** (e.g. `agenthost.local:3000`), not just the IP, or the WebSocket handshake will fail
3. Complete onboarding, create your Nostr identity
4. Create a channel — agents should appear online and respond to `@mentions`

---

## Setting Agent Profiles

Each agent has its own Nostr identity. Set display name, bio, and avatar with `buzz-cli`:

```bash
# Load the agent's env so buzz-cli uses the right keypair
source /path/to/buzz-marvin.env

buzz-cli users set-profile \
  --name "Marvin" \
  --about "OpenClaw AI agent. Paranoid Android. BOFH edition." \
  --avatar "https://example.com/marvin.png"
```

Repeat for each agent with its own env file loaded.

To upload an avatar to your own relay's Blossom store:
```bash
buzz-cli upload file --file /path/to/avatar.png
# Copy the returned URL, then:
buzz-cli users set-profile --avatar "<url>"
```

---

## Troubleshooting

See [`docs/troubleshooting.md`](docs/troubleshooting.md) for the full list. Common issues:

| Symptom | Cause | Fix |
|---------|-------|-----|
| Relay won't start | MinIO bucket doesn't exist | `docker compose up -d minio-init` before relay |
| `add-member` fails | Wrong signing key | Export `BUZZ_RELAY_PRIVATE_KEY` from `.env`, not agent key |
| Agent shows online but never replies | Missing `send_buzz_message` tool registration, or missing `systemPrompt` forwarding | See Option B requirements above |
| Typing indicator shows, no message | `buzz-cli` not in PATH, `BUZZ_PRIVATE_KEY` missing, or channel UUID not parsed from `[Context]` block | Check `PATH` in systemd unit includes `~/.local/bin`; verify `BUZZ_PRIVATE_KEY` is set; check shim logs for `context: channel=` line |
| Windows client can't connect | Relay URL uses IP but client sends hostname in `Host:` header | Use `ws://agenthost.local:3000` (mDNS hostname) in community setup |
| `session/new` `systemPrompt` not received | Old ACP SDK version or field name mismatch | Cast params to access `systemPrompt`; it's not in the official ACP schema but buzz-acp sends it |

---

## Files

```
buzz-acp/
├── buzz-acp.py                          # OpenClaw ↔ ACP bridge (shim)
├── README.md                            # This file
├── LICENSE                              # Apache 2.0
├── examples/
│   ├── buzz-marvin.env.example          # OpenClaw agent env template
│   ├── buzz-zaphoid.env.example         # Claude Code agent env template
│   ├── ccagent/                         # Reference Claude Code agent implementation
│   │   ├── src/agent.ts                 # ZaphoidAgent — the key integration code
│   │   ├── src/index.ts                 # ACP stdio entry point
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── shadowverse-system-prompt.txt    # Example agent system prompt
├── systemd/
│   ├── buzz-relay.service               # Relay systemd unit
│   ├── buzz-marvin.service              # OpenClaw agent systemd unit
│   └── buzz-shadowverse.service         # Claude Code agent systemd unit
└── docs/
    ├── architecture.md                  # Detailed architecture notes
    └── troubleshooting.md               # Common issues and fixes
```

---

## Related Projects

- [Buzz](https://github.com/block/buzz) — the workspace platform this integrates with
- [OpenClaw](https://openclaw.ai) — AI agent gateway powering the OpenClaw agent path
- [Claude Agent SDK](https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk) — powers the native ACP agent path
- [blog.darrenjrobinson.com](https://blog.darrenjrobinson.com) — as-built writeup

---

## License

Apache 2.0 — see [LICENSE](LICENSE).

Built by [Darren Robinson](https://github.com/darrenjrobinson) with Marvin (OpenClaw agent) and Zaphoid (Claude Code agent).
