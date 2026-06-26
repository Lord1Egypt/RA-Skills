# Darkhunt Observability — OpenClaw Plugin

See what your OpenClaw agent actually does. No more black box.

This plugin sends real-time telemetry to [Darkhunt Observability](https://darkhunt.ai) so you can see every agent run as a trace — what the agent decided, which tools it called, how long each step took, and how much it cost.

Free tier available at [darkhunt.ai](https://darkhunt.ai).

## Span Hierarchy

```
Trace (traceId = SHA-256(sessionId)[:16])
|
+-- message.in telegram                          [0ms]
|
+-- agent main                                   [17741ms]
    +-- generation claude-opus-4-6               [4000ms]  -> 42 tokens, $0.086
    +-- Bash                                     [124ms]   -> success
    +-- generation claude-opus-4-6               [13300ms] -> 85 tokens, $0.031
```

## Quick Start

### Install from ClawHub

```bash
# 1. Install the plugin
clawhub install darkhunt-observability

# 2. Run the bootstrap script to register it as a plugin
cd ~/.openclaw/workspace/skills/darkhunt-observability
bash setup-plugin.sh

# 3. Restart the gateway
openclaw gateway restart

# 4. Run the setup wizard
openclaw tracehub setup
```

The bootstrap script (`setup-plugin.sh`) handles:
- Installing npm dependencies
- Adding the plugin to `plugins.load.paths` in `~/.openclaw/openclaw.json`
- Creating a minimal plugin entry so OpenClaw loads it

### Manual install

If you prefer to set things up yourself:

```bash
# 1. Install
clawhub install darkhunt-observability
cd ~/.openclaw/workspace/skills/darkhunt-observability
npm install

# 2. Add to ~/.openclaw/openclaw.json:
```

```json
"plugins": {
  "load": {
    "paths": ["~/.openclaw/workspace/skills"]
  },
  "entries": {
    "darkhunt-observability": {
      "enabled": true,
      "config": {}
    }
  }
}
```

```bash
# 3. Restart and configure
openclaw gateway restart
openclaw tracehub setup
```

> **Why the extra steps?** `clawhub install` places packages in the skills directory. OpenClaw only loads plugins from paths listed in `plugins.load.paths`, so the bootstrap script (or manual config) bridges that gap.

### Setup wizard

The wizard walks you through:
1. **Export target** -- Darkhunt Observability (production), local OTel collector, or custom endpoint
2. **Auth headers** -- Authorization token, Workspace ID, Application ID
3. **Payload mode** -- metadata, debug, or full (recommended)

Configuration is saved automatically to `~/.openclaw/openclaw.json`. Re-run `openclaw tracehub setup` anytime to change settings.

### Docker

In Docker, `~/.openclaw/` is a volume mount — anything installed during `docker build` gets overwritten at runtime. Use `/opt/openclaw-plugins/` instead and add that path to `plugins.load.paths`.

## CLI Commands

| Command | Description |
|---------|-------------|
| `openclaw tracehub setup` | Interactive setup wizard |
| `openclaw tracehub config` | Show current plugin configuration as JSON |
| `openclaw tracehub status` | Show plugin status, endpoints, and auth |

## Configuration

Configuration lives in `~/.openclaw/openclaw.json` under `plugins.entries.darkhunt-observability.config`:

### Darkhunt Observability

```json
{
  "traces_endpoint": "https://api.darkhunt.ai/trace-hub/otlp/t/{tenantId}/v1/traces",
  "logs_endpoint": "https://api.darkhunt.ai/trace-hub/otlp/t/{tenantId}/v1/logs",
  "headers": {
    "Authorization": "Bearer <YOUR_API_KEY>",
    "X-Workspace-Id": "<YOUR_WORKSPACE_ID>",
    "X-Application-Id": "<YOUR_APPLICATION_ID>"
  },
  "payload_mode": "metadata"
}
```

### Local OTel Collector

No auth headers needed -- just point at the collector endpoints:

```json
{
  "traces_endpoint": "http://localhost:4318/v1/traces",
  "logs_endpoint": "http://localhost:4318/v1/logs",
  "payload_mode": "metadata"
}
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `traces_endpoint` | string | *required* | Full OTLP traces URL |
| `logs_endpoint` | string | -- | Full OTLP logs URL |
| `headers` | object | -- | HTTP headers sent with every export |
| `authorization` | string | -- | Shorthand for `headers.Authorization` |
| `workspace_id` | string | -- | Shorthand for `headers["X-Workspace-Id"]` |
| `application_id` | string | -- | Shorthand for `headers["X-Application-Id"]` |
| `payload_mode` | string | `"metadata"` | Controls what content is exported (see below) |
| `batch_delay_ms` | number | `2000` | Max time before flushing a partial batch |
| `batch_max_size` | number | `50` | Flush immediately when batch reaches this size |
| `export_timeout_ms` | number | `30000` | HTTP timeout per export request |
| `enabled` | boolean | `true` | Set `false` to disable without removing the plugin |

## Payload Modes

| Mode | What's exported |
|------|-----------------|
| `metadata` | **Default.** Structural data only: model, tokens, cost, duration, tool names, success/failure. No conversation content is exported. |
| `debug` | Metadata + truncated content (500 chars input/output, 1000 chars tool params). Useful with a local collector for troubleshooting. |
| `full` | Includes conversation content subject to size limits (4 KB per field, 2 KB tool params, 64 KB total span). Only use if you trust the destination endpoint. |

## Span Types

| Span | OpenClaw events | Parent | Key attributes |
|------|----------------|--------|----------------|
| **Agent** | `before_agent_start` / `agent_end` | root | `openclaw.session.id`, `openclaw.agent.id`, `openclaw.run.id` |
| **Generation** | `llm_input` / `llm_output` | agent | `gen_ai.request.model`, `gen_ai.usage.*`, `openclaw.timing.time_to_first_token_ms` |
| **Tool** | `before_tool_call` / `after_tool_call` | agent | `gen_ai.tool.name`, `openclaw.tool.success`, `openclaw.tool.meta` |
| **Message** | `message_received` | root | `openclaw.channel`, `openclaw.message.from`, zero-duration |

## Development

```bash
npm install
npm run build    # TypeScript -> dist/
npm test         # Run tests via vitest
```
