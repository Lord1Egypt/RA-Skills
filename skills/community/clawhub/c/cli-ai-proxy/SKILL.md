---
name: cli_ai_proxy
description: "Manage cli-ai-proxy: local OpenAI-compatible proxy that routes requests through Gemini CLI and Claude Code. The proxy itself reads no credentials; the underlying CLIs handle their own auth."
user-invocable: true
metadata: { "openclaw": { "emoji": "🔀", "skillKey": "cli-ai-proxy", "requires": { "anyBins": ["gemini", "claude"], "bins": ["node", "npm"] }, "install": [ { "id": "npm", "kind": "node", "package": "cli-ai-proxy", "bins": ["cli-ai-proxy"], "label": "Install cli-ai-proxy via npm" } ] } }
---

# CLI AI Proxy

Local OpenAI-compatible proxy that bridges Gemini CLI and Claude Code to a unified REST API. Requests go through the installed CLI tools — the proxy makes no direct AI-vendor API calls and holds no API keys. Authentication (OAuth, API keys, session tokens) is managed by the `gemini` / `claude` CLIs themselves.

## What This Installs

This skill installs the `cli-ai-proxy` package from the public npm registry. Specifically:

- **Source:** public npm registry package `cli-ai-proxy` (no GitHub clone, no local build step)
- **Postinstall scripts:** none — the package's `package.json` declares no `preinstall`/`postinstall` hooks
- **Runtime dependencies:** one — `yaml` (config parsing)
- **Filesystem writes:** only under the global npm prefix (for the binary) and, when the proxy runs, under its working directory for `config.yaml`, `.proxy.pid`, and `proxy.log`
- **Config mutations:** only if you explicitly run `configure-provider.sh` / `cli-ai-proxy configure-openclaw`, which edits `~/.openclaw/openclaw.json` and writes a `.bak` backup next to it first
- **Network at runtime:** localhost HTTP server only; outbound calls are performed by the user's installed `gemini` / `claude` CLIs, not by the proxy itself

## When to Use

✅ User asks to start/stop/check the AI proxy
✅ User wants to route requests through Gemini CLI or Claude Code
✅ User asks about available models or proxy health
✅ User wants to configure OpenClaw to use the proxy
✅ Troubleshooting proxy connectivity or CLI issues

❌ Direct API calls to OpenAI/Anthropic/Google (this proxy only uses CLI tools)
❌ Managing API keys (CLIs handle their own authentication)

## Quick Reference

| Action | Command |
|--------|---------|
| Start proxy | `{baseDir}/scripts/start.sh` |
| Stop proxy | `{baseDir}/scripts/stop.sh` |
| Check status | `{baseDir}/scripts/status.sh` |
| Health check | `{baseDir}/scripts/health.sh` |
| Configure OpenClaw | `{baseDir}/scripts/configure-provider.sh` |
| Full install | `{baseDir}/scripts/install.sh` |

## Proxy Lifecycle

### Starting

```bash
{baseDir}/scripts/start.sh
```

Starts the proxy on `127.0.0.1:9090` (default). The proxy listens for OpenAI-compatible requests and routes them to the appropriate CLI tool.

Before starting, verify at least one CLI is available:
- `gemini --version` (Gemini CLI)
- `claude --version` (Claude Code)

### Checking Status

```bash
{baseDir}/scripts/status.sh
```

Shows: running/stopped, PID, health endpoint data, available CLI providers, concurrency stats.

### Stopping

```bash
{baseDir}/scripts/stop.sh
```

Gracefully shuts down the proxy: stops accepting connections, kills active CLI subprocesses, cleans up.

## Available Models

| Model ID | Provider | Backend Model |
|----------|----------|---------------|
| `gemini` | Gemini CLI | CLI default (auto-upgrades) |
| `claude` | Claude Code | CLI default (auto-upgrades) |
| `claude-sonnet` | Claude Code | sonnet |
| `claude-opus` | Claude Code | opus |

When OpenClaw is configured, use as `cli-ai-proxy/gemini`, `cli-ai-proxy/claude`, etc.

## OpenClaw Integration

To configure OpenClaw to route through the proxy:

```bash
{baseDir}/scripts/configure-provider.sh
```

This automatically:
1. Adds `cli-ai-proxy` as a provider in `~/.openclaw/openclaw.json`
2. Registers all proxy models in the agent defaults
3. Creates a backup of the original config

After configuring, set the default model in `openclaw.json`:
```json
{ "agents": { "defaults": { "model": { "primary": "cli-ai-proxy/gemini" } } } }
```

## API Endpoints

The proxy exposes:

- `POST /v1/chat/completions` — Chat completions (streaming + non-streaming)
- `GET /v1/models` — List available models
- `GET /health` — Health check with provider status and concurrency info

Default base URL: `http://127.0.0.1:9090/v1`

For full API details see [references/api.md](references/api.md).

## Image Support

The proxy supports images in messages. When a request contains `image_url` content parts:

1. Images are saved to temporary files
2. The prompt instructs the CLI to read the image via its built-in file tools
3. Temp files are automatically cleaned up after each request

Supports both base64 data URLs and remote image URLs.

## Configuration

Config file: `config.yaml` in the proxy installation directory.

Key settings:
- `server.port` — Listen port (default: 9090)
- `concurrency.max` — Max concurrent CLI processes (default: 5)
- `timeout` — CLI process timeout in ms (default: 300000)
- `defaultModel` — Default model when none specified

For full configuration options see [references/configuration.md](references/configuration.md).

## Troubleshooting

### Proxy won't start
1. Check if port 9090 is already in use: `lsof -i :9090`
2. Verify Node.js is available: `node --version`
3. Check logs: read the proxy.log file in the installation directory

### CLI not available
1. Verify CLI is installed and in PATH: `which gemini` or `which claude`
2. Check CLI auth: `gemini --version` or `claude --version`
3. The proxy health endpoint shows which CLIs are available

### 429 Too Many Requests
The concurrency limit has been reached. Either:
- Wait for current requests to complete
- Increase `concurrency.max` in config.yaml

### Timeout errors (504)
The CLI process took too long. Either:
- Increase `timeout` in config.yaml
- Check if the CLI is hanging (auth issues, network)

For more troubleshooting see [references/troubleshooting.md](references/troubleshooting.md).
