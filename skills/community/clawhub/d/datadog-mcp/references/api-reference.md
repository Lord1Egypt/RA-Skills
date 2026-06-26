# Datadog MCP Server — Tool Reference

Complete parameter reference for all MCP tools provided by the Datadog MCP Server.

## Logs & Traces

### get_logs

Search and retrieve log entries.

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Datadog log search query syntax |
| `from` | string | Start time (ISO 8601 or relative like `now-1h`) |
| `to` | string | End time |
| `limit` | number | Max results (default: 10) |
| `sort` | string | `timestamp` (asc) or `-timestamp` (desc) |

### list_spans

Search for spans in distributed traces.

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Span search query |
| `from` | string | Start time |
| `to` | string | End time |
| `limit` | number | Max results |

### get_trace

Retrieve all spans from a specific trace.

| Parameter | Type | Description |
|---|---|---|
| `trace_id` | string | The trace ID to retrieve |

## Metrics & Monitoring

### list_metrics

Search available metrics by name pattern.

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Metric name search pattern (e.g., `system.cpu`) |

### get_metrics

Query timeseries metric data points.

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Datadog metrics query (e.g., `avg:system.cpu.user{service:web}`) |
| `from` | number | Start time (Unix epoch seconds) |
| `to` | number | End time (Unix epoch seconds) |

### get_monitors

Retrieve monitor configurations and current status.

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Filter monitors (name, tag, or status) |

## Infrastructure

### list_hosts

Get detailed information about infrastructure hosts.

| Parameter | Type | Description |
|---|---|---|
| `filter` | string | Filter string for hosts |
| `sort_field` | string | Sort by field |
| `sort_dir` | string | `asc` or `desc` |

## Incident Management

### list_incidents

List incidents with optional filters.

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Filter query |

### get_incident

Get details for a specific incident.

| Parameter | Type | Description |
|---|---|---|
| `incident_id` | string | The incident ID |

## Dashboards

### list_dashboards

Discover available dashboards.

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Search/filter dashboards by name |

## Notes

- The remote MCP server handles intent parsing — natural language queries work directly
- Time ranges default to "last 15 minutes" if not specified
- The server selects the appropriate tool based on your prompt — you don't need to specify tool names manually
- Response format is optimized for AI agent consumption (structured, relevant context only)
