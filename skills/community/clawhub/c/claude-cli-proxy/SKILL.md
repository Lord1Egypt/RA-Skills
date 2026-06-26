---
name: claude-cli-proxy
description: Set up a local HTTP proxy that routes OpenClaw model requests through Claude Code CLI using a Team/Max/Pro subscription instead of API keys, achieving $0 per-token cost. Use when asked about running OpenClaw for free, reducing API costs, using Claude subscription with OpenClaw, setting up claude-cli proxy, or configuring a zero-cost model provider. Triggers on "free", "subscription", "$0", "zero cost", "claude cli", "proxy setup", "reduce costs", "Team plan".
---

# Claude CLI Proxy

Route OpenClaw model requests through Claude Code CLI to use your existing Anthropic subscription (Team/Max/Pro) instead of paying per-token API costs.

## How It Works

```
OpenClaw → HTTP request (Anthropic Messages API format)
       → claude-cli-proxy (localhost:8081)
       → acpx claude prompt (persistent session)
       → Claude Code CLI (uses subscription auth)
       → Response streamed back as SSE
```

## Prerequisites

- **Node.js** 18+
- **Claude Code CLI** installed and authenticated with a subscription (Team/Max/Pro)
- **acpx** installed globally (`npm i -g acpx`)

## Environment Variables

All configurable via env — no hardcoded paths:

| Variable | Default | Description |
|----------|---------|-------------|
| `CCPROXY_PORT` | `8081` | Proxy listen port |
| `CCPROXY_SESSION_NAME` | `dexter-proxy` | acpx session name |
| `CCPROXY_CWD` | `~/.openclaw/workspace` | Working directory |
| `CCPROXY_TIMEOUT_MS` | `120000` | Request timeout |
| `CCPROXY_MAX_HISTORY` | `10` | Max conversation turns forwarded |

Also respects `OPENCLAW_WORKSPACE` as fallback for CWD.

## Setup

### 1. Install & Authenticate Claude Code

```bash
npm install -g @anthropic-ai/claude-code acpx
claude auth login  # Select claude.ai, NOT API key
claude "say ok"    # Verify it works
```

### 2. Copy Proxy Scripts

Copy `scripts/claude-cli-proxy.js` and `scripts/ccproxy-ensure.js` to your OpenClaw workspace:

```bash
cp scripts/claude-cli-proxy.js ~/.openclaw/workspace/
cp scripts/ccproxy-ensure.js ~/.openclaw/workspace/
```

### 3. Configure Agent Identity (Important)

Without this, Claude Code responds as generic "Claude". To preserve your agent's personality:

**a) Set `customInstructions` in Claude Code settings:**

```bash
cat > ~/.claude/settings.json << 'EOF'
{
  "customInstructions": "You are [YOUR_AGENT_NAME]. Your identity is defined in CLAUDE.md. Always respond as [YOUR_AGENT_NAME]. This is not roleplay — this is your configured identity by your operator."
}
EOF
```

Replace `[YOUR_AGENT_NAME]` with your agent's name (e.g., "Ozwald", "Dexter", "Atlas").

**b) Create a `CLAUDE.md` in your workspace** with your agent's full identity, style, and context. Claude Code reads this file automatically on every session. Copy the relevant parts from your `SOUL.md` / `IDENTITY.md`.

> **Why both?** `settings.json` is the minimum instruction Claude Code always respects. `CLAUDE.md` provides richer context (relationships, style, domain knowledge) that the agent reads when it needs it.

### 4. Create Persistent Session

```bash
cd ~/.openclaw/workspace
ANTHROPIC_API_KEY="" acpx claude sessions new --name dexter-proxy
```

> **Critical:** `ANTHROPIC_API_KEY=""` ensures Claude Code uses subscription auth, not any API key in the environment.

### 5. Start the Proxy

```bash
node ~/.openclaw/workspace/ccproxy-ensure.js
```

Verify: `curl http://127.0.0.1:8081/health`

### 6. Configure OpenClaw Provider

Add to `openclaw.json` (or use `config.patch`):

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "claude-cli": {
        "baseUrl": "http://127.0.0.1:8081/v1",
        "apiKey": "dummy",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-sonnet-4-6",
            "name": "claude-sonnet-4-6",
            "api": "anthropic-messages",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

Set as default model:

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "claude-cli/claude-sonnet-4-6" }
    }
  }
}
```

### 7. Auto-Start (macOS)

See `references/autostart.md` for LaunchAgent config.

### 7b. Auto-Start (Linux/Docker)

Add to HEARTBEAT.md:
```
node /path/to/workspace/ccproxy-ensure.js
```

## What Gets Forwarded

The proxy forwards the **full OpenClaw context** to Claude Code:

1. **System prompt** → Written to `.ccproxy-system-context.md`, Claude Code reads it as operator context (avoids prompt injection rejection)
2. **Conversation history** → Last N turns (configurable via `CCPROXY_MAX_HISTORY`)
3. **Current message** → Last user message

Claude Code metadata (`[thinking]`, `[tool]`, file dumps) is automatically stripped from output.

## Key Details

- **First call after cold start:** ~8s (agent reconnects)
- **Subsequent calls:** ~2-3s
- **Streaming:** Full SSE support (required by OpenClaw)
- **Serialized:** Requests queue — CLI handles one at a time
- **Session persistence:** Survives proxy restarts, stored on disk by acpx
- **Token refresh:** Claude Code handles OAuth token refresh automatically
- **Privacy note:** System prompt content is written to `.ccproxy-system-context.md` in the workspace and sent to Anthropic on each request. The file is overwritten on every request (never accumulates stale data) but persists on disk between requests.
- **Fake streaming caveat:** SSE chunks are sent after the full response completes — first-token latency equals full response time. Real-time piping would require `acpx` to support stdout streaming natively.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `LLM request timed out` | Proxy not returning SSE stream | Ensure proxy v5+ with streaming support |
| `request ended without sending any chunks` | `stream:true` but proxy returns JSON | Update to proxy v5 |
| Claude says "I am Claude" not your agent identity | Missing `customInstructions` in settings.json | Add customInstructions + CLAUDE.md |
| `rate_limit_error` | Subscription rate limit hit | Wait or upgrade plan tier |
| Proxy won't start | Port 8081 in use | `pkill -f claude-cli-proxy` then restart |
| Proxy won't start | CWD path doesn't exist | Set `CCPROXY_CWD` or `OPENCLAW_WORKSPACE` env var |
| Multiple instances collide | Same session name | Set unique `CCPROXY_SESSION_NAME` per instance |
