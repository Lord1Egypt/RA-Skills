# datadog-mcp

An [OpenClaw](https://openclaw.ai) skill for querying Datadog observability data through Datadog's official [MCP Server](https://docs.datadoghq.com/bits_ai/mcp_server/).

[![CI](https://github.com/bcwilsondotcom/openclaw-datadog-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/bcwilsondotcom/openclaw-datadog-mcp/actions/workflows/ci.yml)
[![Security](https://github.com/bcwilsondotcom/openclaw-datadog-mcp/actions/workflows/security.yml/badge.svg)](https://github.com/bcwilsondotcom/openclaw-datadog-mcp/actions/workflows/security.yml)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-datadog--mcp-orange)](https://clawhub.ai/bcwilsondotcom/datadog-mcp)

## What This Does

Connects your OpenClaw agent to Datadog's official MCP Server, giving it the ability to:

- **Search logs** — find errors, investigate issues across services
- **Query metrics** — timeseries data, latency percentiles, error rates
- **Investigate traces** — distributed tracing, span analysis
- **Check monitors** — alert status, thresholds, configurations
- **Manage incidents** — list active incidents, get details, track resolution
- **List dashboards** — discover and reference dashboards
- **Inspect infrastructure** — host health, agent status, resource usage
- **Run synthetic tests** — check synthetic test results
- **Trigger workflows** — execute Datadog Workflow Automation

## Why MCP Instead of REST API?

Datadog's MCP Server is **not just a REST API wrapper**. It:

1. **Parses natural language** — "show me Redis errors" → correct log query, time range, filters
2. **Selects the right endpoint** — agent describes intent, server picks the tool
3. **Returns AI-optimized responses** — structured, relevant context without noise
4. **Handles auth and errors** — no HTTP plumbing in your agent's context
5. **Runs on Datadog infrastructure** — your data never leaves Datadog

## Quick Start

### 1. Get Credentials

From [app.datadoghq.com](https://app.datadoghq.com):
- **API Key**: Organization Settings → API Keys → New Key
- **Application Key**: Organization Settings → Application Keys → New Key

### 2. Set Environment Variables

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-application-key"
export DD_SITE="datadoghq.com"  # optional, default is US1
```

### 3. Install the Skill

```bash
clawhub install datadog-mcp
```

### 4. Validate

```bash
./scripts/validate.sh
```

## Documentation

| Document | Description |
|---|---|
| [SKILL.md](SKILL.md) | Agent-facing skill instructions |
| [docs/setup.md](docs/setup.md) | Detailed setup guide |
| [docs/architecture.md](docs/architecture.md) | How the MCP Server works |
| [references/incident-response.md](references/incident-response.md) | Incident triage runbook |
| [references/troubleshooting.md](references/troubleshooting.md) | Common troubleshooting patterns |
| [references/api-reference.md](references/api-reference.md) | Complete tool parameter reference |

## Supported Transports

| Transport | Description | Setup |
|---|---|---|
| **Remote HTTP** (recommended) | Datadog-hosted, no local install | Configure mcporter with HTTP endpoint |
| **Local stdio** | Community npm package | `npx datadog-mcp-server` |
| **Claude Code** | Built-in MCP support | `claude mcp add --transport http` |
| **Codex CLI** | OpenAI's terminal agent | Native integration |

## Multi-Site Support

| Region | `DD_SITE` value |
|---|---|
| US1 (default) | `datadoghq.com` |
| US3 | `us3.datadoghq.com` |
| US5 | `us5.datadoghq.com` |
| EU | `datadoghq.eu` |
| AP1 | `ap1.datadoghq.com` |
| US1-FED | `ddog-gov.com` |

## Contributing

Contributions welcome. Please open an issue first for significant changes.

## License

[MIT-0](LICENSE) — free to use, modify, redistribute. No attribution required.
