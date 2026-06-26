---
name: datadog-mcp
description: Datadog observability via the official MCP Server — query logs, traces, metrics, monitors, incidents, dashboards, hosts, synthetics, and workflows through Datadog's remote MCP endpoint. Use when investigating production issues, checking monitor status, searching logs/traces, querying metrics timeseries, managing incidents, or listing dashboards and synthetic tests. Supports both remote (Streamable HTTP) and local (stdio) MCP transports. Requires DD_API_KEY and DD_APP_KEY.
homepage: https://github.com/bcwilsondotcom/openclaw-datadog-mcp
metadata:
  openclaw:
    emoji: "🐕"
    requires:
      env:
        - DD_API_KEY
        - DD_APP_KEY
      optional_env:
        - DD_SITE
---

# Datadog MCP Server

Query Datadog observability data through the official MCP Server.

## Requirements

| Variable | Required | Description |
|---|---|---|
| `DD_API_KEY` | ✅ | Datadog API key (Organization Settings → API Keys) |
| `DD_APP_KEY` | ✅ | Datadog Application key (Organization Settings → Application Keys) |
| `DD_SITE` | Optional | Datadog site (default: `datadoghq.com`) |

## Setup

### Option A: Remote MCP Server (Recommended)

Datadog hosts the MCP server — no local install needed.

```bash
mcporter add datadog \
  --transport http \
  --url "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp" \
  --header "DD-API-KEY:$DD_API_KEY" \
  --header "DD-APPLICATION-KEY:$DD_APP_KEY"
```

To select specific toolsets, append `?toolsets=logs,metrics,monitors` to the URL.

### Option B: Local stdio MCP Server

Use the community `datadog-mcp-server` npm package:

```bash
npx datadog-mcp-server \
  --apiKey "$DD_API_KEY" \
  --appKey "$DD_APP_KEY" \
  --site "$DD_SITE"
```

### Option C: Claude Code / Codex CLI

```bash
claude mcp add --transport http datadog-mcp \
  "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp?toolsets=core"
```

## Available Toolsets

| Toolset | Tools | Description |
|---|---|---|
| `core` | General platform tools | Default — always included |
| `logs` | `get_logs` | Search and retrieve log entries |
| `traces` | `list_spans`, `get_trace` | Investigate distributed traces |
| `metrics` | `list_metrics`, `get_metrics` | Query timeseries metrics data |
| `monitors` | `get_monitors` | Retrieve monitor configs and status |
| `hosts` | `list_hosts` | Infrastructure host information |
| `incidents` | `list_incidents`, `get_incident` | Incident management |
| `dashboards` | `list_dashboards` | Discover dashboards |
| `synthetics` | Synthetic test tools | Synthetic monitoring tests |
| `workflows` | Workflow automation tools | List, inspect, execute workflows |

Select toolsets via URL query parameter: `?toolsets=logs,metrics,monitors,incidents`

## Usage Examples

- **Error investigation:** *"Show me error logs from service:api-gateway in the last hour"* — uses `get_logs` with query filters
- **Monitor status:** *"Are there any triggered monitors for the payments service?"* — uses `get_monitors` with service tag filter
- **Metrics query:** *"Show me p99 latency for web-app over the last 4 hours"* — uses `list_metrics` then `get_metrics` for timeseries
- **Incident response:** *"List active incidents"* — uses `list_incidents`
- **Trace investigation:** *"Find slow spans for service:checkout taking over 5s"* — uses `list_spans` with duration filter

## Operational Runbooks

- `references/incident-response.md` — step-by-step incident triage via MCP
- `references/troubleshooting.md` — log/trace/metric correlation patterns
- `references/api-reference.md` — complete tool parameters and response schemas

## Multi-Site Support

| Region | Site |
|---|---|
| US1 (default) | `datadoghq.com` |
| US3 | `us3.datadoghq.com` |
| US5 | `us5.datadoghq.com` |
| EU | `datadoghq.eu` |
| AP1 | `ap1.datadoghq.com` |
| US1-FED | `ddog-gov.com` |

For the remote MCP server, the site is determined by your API key's org. For the local server, pass `--site`.

## Security Notes

- API keys grant read access to your Datadog org — treat them as secrets
- Application keys inherit the permissions of the user who created them
- Use scoped application keys with minimal permissions for production
- The remote MCP server runs on Datadog infrastructure — data does not leave Datadog
- The local stdio server runs on your machine — API calls go directly to Datadog's API
