---
name: cf-workers-logs
description: |
  Query Cloudflare Workers Observability logs via API. Use when the user asks to check logs,
  debug Workers, look up errors, or investigate Worker/Durable Object/Workflow behavior.
  Triggers on keywords like "check logs", "worker logs", "look up error", "debug worker".
metadata: '{"openclaw":{"requires":{"env":["CF_OBSERVABILITY_ACCOUNT_ID","CF_OBSERVABILITY_API_TOKEN"],"bins":["curl"]}}}'
user-invocable: true
homepage: https://github.com/adaHubble/cf-workers-logs
---

# Query Cloudflare Workers Observability Logs

Query the CF Workers Observability API to retrieve structured logs from any Workers, Durable Objects, Workflows, Queues, and Cron Triggers in your Cloudflare account.

## Prerequisites

Set these environment variables (e.g. in your project's `.env` or shell profile):

- `CF_OBSERVABILITY_ACCOUNT_ID` — your Cloudflare account ID
- `CF_OBSERVABILITY_API_TOKEN` — API token with Workers Observability read permission

## API Endpoint

```
POST https://api.cloudflare.com/client/v4/accounts/{accountId}/workers/observability/telemetry/query
Authorization: Bearer {apiToken}
Content-Type: application/json
```

## Request Body Format

```json
{
  "queryId": "cc-{timestamp}",
  "timeframe": {
    "from": "<unix_ms_start>",
    "to": "<unix_ms_end>"
  },
  "view": "events",
  "limit": 50,
  "parameters": {
    "filters": [
      {"key": "<field>", "operation": "<op>", "type": "<type>", "value": "<value>"}
    ],
    "filterCombination": "and",
    "calculations": [],
    "groupBys": [],
    "needle": {"value": "<search_text>", "isRegex": false, "matchCase": false},
    "limit": 50
  }
}
```

### Filter Operations

- String: `eq`, `neq`, `includes`, `doesNotInclude`, `startsWith`, `regex`, `exists`, `doesNotExist`
- Number: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `exists`, `doesNotExist`

### Standard Fields

| Field | Type | Description |
|-------|------|-------------|
| `$workers.scriptName` | string | Worker script name |
| `$workers.outcome` | string | `ok` / `exception` |
| `$workers.entrypoint` | string | Entrypoint class (Worker, DO, Workflow) |
| `$workers.eventType` | string | `fetch`, `rpc`, `queue`, `scheduled`, `alarm` |
| `msg` | string | Log message |
| `level` | string | Log level (`log`, `info`, `warn`, `error`) |
| `error` | string | Error message |
| `status` | number | HTTP status code |

Any custom fields logged via `console.log({ key: value })` are also queryable as top-level fields.

### Full-text Search

Use `needle.value` for free-text search across all fields. Useful when you don't know which field contains the value.

## How to Execute

Use Bash with `curl` to call the API. **Do NOT use WebFetch** (it processes through an AI model and loses structure).

### Step 1: Read credentials

Read `CF_OBSERVABILITY_ACCOUNT_ID` and `CF_OBSERVABILITY_API_TOKEN` from environment variables. If not set in the shell, search for them in project `.env` files:

```bash
grep -r 'CF_OBSERVABILITY_' --include='.env' --include='.env.*' . 2>/dev/null
```

### Step 2: Build and execute query

Construct the curl command based on the user's request. Default time range: last 1 hour. Default limit: 30.

### Step 3: Format output

Parse the JSON response and format as a timeline:

```
{timestamp} [{level}] [{scriptName}/{entrypoint}] {msg}
         {extra fields if present: error=, status=, eventType=}
```

Events are in `result.events.events[]`. Each event has:
- `source`: structured log fields (msg, level, plus any custom fields)
- `$workers`: Worker metadata (scriptName, outcome, eventType, entrypoint)
- `$metadata`: system metadata (timestamp, requestId)
- `timestamp`: event timestamp in unix ms

Sort events by timestamp ascending for chronological view.

## Common Query Patterns

### By Worker name
```json
{"filters": [{"key": "$workers.scriptName", "operation": "eq", "type": "string", "value": "my-worker"}]}
```

### Errors only
```json
{"filters": [{"key": "level", "operation": "eq", "type": "string", "value": "error"}]}
```

### By entrypoint (Durable Object / Workflow class)
```json
{"filters": [{"key": "$workers.entrypoint", "operation": "eq", "type": "string", "value": "MyDurableObject"}]}
```

### By event type (alarm, queue, scheduled, etc.)
```json
{"filters": [{"key": "$workers.eventType", "operation": "eq", "type": "string", "value": "alarm"}]}
```

### Exceptions (Worker crashed)
```json
{"filters": [{"key": "$workers.outcome", "operation": "eq", "type": "string", "value": "exception"}]}
```

### Custom field filter
```json
{"filters": [{"key": "userId", "operation": "eq", "type": "string", "value": "user_123"}]}
```

### Free-text search
```json
{"needle": {"value": "search text here", "isRegex": false, "matchCase": false}}
```

### Combine filters
```json
{
  "filters": [
    {"key": "$workers.scriptName", "operation": "eq", "type": "string", "value": "my-worker"},
    {"key": "level", "operation": "eq", "type": "string", "value": "error"}
  ],
  "filterCombination": "and"
}
```

## Argument Parsing

When invoked as `/cf-workers-logs`, parse `$ARGUMENTS` for:

- `worker=my-worker` → filter by `$workers.scriptName`
- `level=error` → filter by level
- `entrypoint=MyDO` → filter by `$workers.entrypoint`
- `event=alarm` → filter by `$workers.eventType`
- `search=xxx` → needle search
- `<key>=<value>` → filter by custom field
- `last=1h` / `last=30m` / `last=24h` → time range (default: 1h)
- `limit=N` → result limit (default: 30)
- No arguments → show recent errors across all Workers (last 1h, level=error)

Multiple arguments can be combined: `/cf-workers-logs worker=my-api level=error last=24h`
