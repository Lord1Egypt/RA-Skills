---
name: corveil-dev
description: Corveil is an organizational intelligence platform that captures AI activity (coding sessions, meetings, chats), produces insights and recommendations, and builds knowledge graphs. This skill starts Corveil in dev mode and configures OpenClaw or Claude Code to route requests through it — supporting both passthrough mode (your own API key + Corveil tracking) and direct mode (Corveil virtual key).
metadata: {"clawdbot":{"emoji":"🐦‍⬛","requires":{"bins":["curl","jq"]}}}
---

# Corveil Dev

Corveil is an organizational intelligence platform. It captures AI activity from coding sessions, meetings, and chatbots — then produces insights, recommendations, user profiles, and knowledge graphs. Under the hood it acts as a zero-trust AI gateway: proxying LLM requests with authentication, spend tracking, guardrails, and plugin support.

This skill starts Corveil in dev mode and connects OpenClaw or Claude Code to route AI requests through it locally. All requests are fully logged, tracked, and subject to guardrails as they flow through Corveil.

## What You'll Need

- **Corveil binary** — installed via [GitHub Releases](https://github.com/radiusmethod/corveil-releases/releases) or the install script (see below)
- **An upstream provider API key** — OpenRouter (`sk-or-v1-...`) for multi-model access, or Anthropic (`sk-ant-...`) for direct Anthropic access. Use a dev/test key, not production credentials
- **OpenClaw** (optional) — only needed for passthrough routing; Claude Code can connect directly

A Corveil dev API key (`sk-citadel-...`) is created automatically via the API in Step 2 below — no manual setup required.

## When to Run

- Setting up a local Corveil development environment
- Testing Corveil passthrough or direct mode with Claude Code
- Developing or testing Corveil plugins, guardrails, or spend tracking
- Demoing Corveil locally

## Workflow

### 1. Install Corveil

**Option A: GitHub Releases (recommended)**

Download a signed binary from [GitHub Releases](https://github.com/radiusmethod/corveil-releases/releases). Binaries are available for macOS, Linux, and Windows (ARM64 and AMD64). Verify the download with the published checksums.

```bash
# Example: macOS ARM64 (Apple Silicon)
curl -LO https://github.com/radiusmethod/corveil-releases/releases/latest/download/corveil-darwin-arm64
chmod +x corveil-darwin-arm64
mv corveil-darwin-arm64 /usr/local/bin/corveil
corveil --version  # verify the installed binary
```

**Option B: Install script**

```bash
# Inspect the script before running:
curl -sSL https://corveil.com/install.sh -o install.sh
less install.sh   # review contents
sh install.sh
```

### 2. Start Corveil and Create an API Key

```bash
# Start in dev mode with your provider key:
corveil --dev --openrouter-api-key sk-or-v1-...
# Or with Anthropic directly:
corveil --dev --anthropic-api-key sk-ant-...
```

Corveil starts on **localhost:8000** (bound to localhost only — not exposed to the network) with:
- Ephemeral local Postgres (via `docker compose up postgres`) — disposable
- Dev login enabled (no SSO/JWT setup)
- Dashboard at http://localhost:8000

Then create an API key via the API — no need to open the dashboard:

```bash
# Log in as the dev user (stores session cookie)
curl -s -c /tmp/corveil-cookies -X POST http://localhost:8000/auth/dev-login

# Create an API key and extract the plaintext key
CORVEIL_KEY=$(curl -s -b /tmp/corveil-cookies -X POST http://localhost:8000/api/keys \
  -H 'Content-Type: application/json' \
  -d '{"name":"dev-key"}' | jq -r '.key')

echo "Your Corveil API key: $CORVEIL_KEY"
```

### 3a. Connect OpenClaw (Passthrough Mode)

Passthrough routes your own Anthropic credentials through Corveil for tracking and guardrails, while your API key authenticates directly with Anthropic.

```bash
openclaw config set models.providers.anthropic '{
  "baseUrl": "http://localhost:8000",
  "api": "anthropic-messages",
  "headers": {
    "x-citadel-api-key": "'"$CORVEIL_KEY"'"
  },
  "models": [
    {
      "id": "claude-sonnet-4-6",
      "name": "Claude Sonnet 4.6",
      "reasoning": true,
      "input": ["text", "image"],
      "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
      "contextWindow": 200000,
      "maxTokens": 16384
    }
  ]
}'
```

Costs are set to `0` because Corveil tracks spend on its side.

Your existing Anthropic API key (configured in OpenClaw) flows through to Anthropic. The `x-citadel-api-key` header authenticates with Corveil for logging, guardrails, and spend tracking.

### 3b. Connect Claude Code Directly (No OpenClaw)

#### Direct Mode

Corveil uses its own provider credentials to fulfill requests:

```bash
export ANTHROPIC_BASE_URL="http://localhost:8000"
export ANTHROPIC_API_KEY="$CORVEIL_KEY"
```

Or in `.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:8000",
    "ANTHROPIC_API_KEY": "<your-corveil-key>"
  }
}
```

#### Passthrough Mode

Your own Anthropic credentials flow through to Anthropic:

```bash
export ANTHROPIC_BASE_URL="http://localhost:8000"
export ANTHROPIC_CUSTOM_HEADERS="x-citadel-api-key: $CORVEIL_KEY"
```

Or in `.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:8000",
    "ANTHROPIC_CUSTOM_HEADERS": "x-citadel-api-key: <your-corveil-key>"
  }
}
```

### 4. Verify the Connection

```bash
# Check Corveil is running
curl http://localhost:8000/health

# Check recent logs
corveil logs --tail 5
```

Then send any request through Claude Code or OpenClaw. If it responds, requests are flowing through Corveil. Confirm in the dashboard at http://localhost:8000.

## Security Notes

- **Localhost only**: Dev mode binds to `localhost:8000` — not exposed to the network. Only local processes can reach it.
- **Ephemeral database**: Dev mode runs against the local Postgres container started by `docker compose up postgres`. API keys and logs exist only on your machine and are disposable.
- **Passthrough transparency**: In passthrough mode, your provider API key flows through the local proxy and is forwarded directly to the upstream provider. Corveil does not store your provider credentials — they are only held in memory for the duration of the request.
- **Use dev/test keys**: Use non-production API keys for your upstream provider (OpenRouter, Anthropic). Rotate them after testing if needed.
- **Install verification**: Download from [GitHub Releases](https://github.com/radiusmethod/corveil-releases/releases) with published checksums. Run `corveil --version` to verify.

## Important Rules

### Passthrough Requires the x-citadel-api-key Header
Only Claude Code (via `ANTHROPIC_CUSTOM_HEADERS`) and OpenClaw (via `headers` config) support custom headers for passthrough mode. Other tools (Cursor, aichat, Codex CLI) only support direct mode.

### Costs Should Be Zero in OpenClaw Config
When routing through Corveil, set model costs to `0` in OpenClaw since Corveil handles spend tracking.

### All Requests Are Logged
Every request flowing through Corveil is logged with full request/response capture, spend tracking, and guardrail enforcement — regardless of direct or passthrough mode.

## Reference

- Full client setup guides: https://corveil.com/docs
- GitHub Releases: https://github.com/radiusmethod/corveil-releases/releases
- Compatibility matrix: Claude Code and OpenClaw support passthrough; aichat, Cursor, OpenCode, Codex CLI, and Gemini CLI support direct mode only
