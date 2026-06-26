# Datadog MCP Server Architecture

## How It Works

```
┌─────────────┐     MCP Protocol      ┌──────────────────┐     Datadog API     ┌──────────┐
│  OpenClaw   │ ──────────────────────→│  Datadog MCP     │ ──────────────────→│ Datadog  │
│  Agent      │  Streamable HTTP       │  Server           │  Internal calls    │ Platform │
│             │ ←──────────────────────│  (mcp.datadoghq) │ ←──────────────────│          │
└─────────────┘     Structured         └──────────────────┘     Raw data       └──────────┘
                    responses
```

## Request Flow

1. **Agent sends prompt** — e.g., "Show me error logs from service:api"
2. **MCP Server parses intent** — determines this is a `get_logs` call
3. **Server constructs API request** — builds the correct Datadog API query
4. **Server fetches data** — calls Datadog's internal APIs
5. **Server formats response** — returns structured, AI-optimized data
6. **Agent receives context** — uses the data to answer the user

## Key Design Decisions

### Why Remote (Not Local)?

The Datadog MCP Server runs on Datadog's infrastructure:

- **Data stays in Datadog** — logs/traces/metrics never leave the platform
- **No local dependencies** — no Docker, no Python, no Node.js required
- **Always up to date** — Datadog maintains the server
- **Better performance** — co-located with the data

### Why MCP (Not Direct API)?

The MCP protocol provides:

- **Tool discovery** — agent learns available capabilities dynamically
- **Intent parsing** — natural language → API calls handled server-side
- **Error handling** — standardized error responses across all tools
- **Composability** — works alongside other MCP servers seamlessly

### Transport: Streamable HTTP

The Datadog MCP Server uses the **Streamable HTTP** transport:

- Single HTTP endpoint (not WebSocket)
- Server-Sent Events (SSE) for streaming responses
- Stateless — no persistent connection needed
- Works behind corporate proxies and firewalls
- Auth via HTTP headers (`DD-API-KEY`, `DD-APPLICATION-KEY`)

## Toolset Architecture

Tools are organized into **toolsets** — groups of related capabilities:

```
core (always included)
├── logs
│   └── get_logs
├── traces
│   ├── list_spans
│   └── get_trace
├── metrics
│   ├── list_metrics
│   └── get_metrics
├── monitors
│   └── get_monitors
├── hosts
│   └── list_hosts
├── incidents
│   ├── list_incidents
│   └── get_incident
├── dashboards
│   └── list_dashboards
├── synthetics
│   └── (synthetic test tools)
└── workflows
    └── (workflow automation tools)
```

Select toolsets via URL: `?toolsets=logs,metrics,monitors`

This reduces the tool surface area, keeping the agent's context focused on relevant capabilities.

## Security Model

```
Authentication:
  DD-API-KEY ──→ Identifies the Datadog organization
  DD-APPLICATION-KEY ──→ Scoped to creating user's permissions

Authorization:
  Read-only by default (get/list tools)
  Write access requires explicit toolsets (workflows)
  No credential storage on MCP server — passed per-request
```
