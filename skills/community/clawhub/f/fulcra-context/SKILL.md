---
name: fulcra-context
description: Access user-consented Fulcra context data including biometrics, sleep, activity, calendar, location, and the Fulcra metric catalog through the hosted MCP server or Fulcra CLI. Use for bounded read/context workflows only; use fulcra-annotations for writes.
homepage: https://fulcradynamics.com
---

# Fulcra Context

Fulcra gives agents user-consented access to personal context such as biometrics, sleep, activity, calendar, location, and metric catalog data.

This ClawHub skill is intentionally docs-first. It does not ship executable helper scripts, install hooks, background jobs, transcript processors, weather enrichment, export tools, or arbitrary CLI wrappers. Use Fulcra's hosted MCP server or the Fulcra CLI directly, and keep every read bounded to the user's current request.

Use the companion `fulcra-annotations` skill when an agent needs to create annotation definitions or record user-approved events back to Fulcra.

## Privacy Boundary

- Ask before reading Fulcra data.
- Read only the metrics or time window needed for the current answer.
- Do not print, log, paste, or forward access tokens, refresh tokens, credential files, raw private records, or direct capability URLs.
- Do not share real calendar, location, notes, transcripts, or identifying context in public channels unless the user explicitly approves that exact disclosure.
- Do not run transcript, third-party enrichment, raw export, or broad library-file workflows from this skill.
- If the user asks for persistent files, exports, dashboards, or public examples, confirm the exact destination and retention plan first. Prefer synthetic fixtures for public artifacts.

## Setup

### Option 1: Hosted MCP Server

Use Fulcra's hosted MCP server at:

```text
https://mcp.fulcradynamics.com/mcp
```

Claude Desktop settings:

```json
{
  "mcpServers": {
    "fulcra_context": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.fulcradynamics.com/mcp"]
    }
  }
}
```

Local stdio server option:

```json
{
  "mcpServers": {
    "fulcra_context": {
      "command": "uvx",
      "args": ["fulcra-context-mcp"]
    }
  }
}
```

Open source MCP server: <https://github.com/fulcradynamics/fulcra-context-mcp>

### Option 2: Fulcra CLI

Use the Fulcra CLI for repeatable automation:

```bash
uv tool run fulcra-api --help
```

Authenticate once:

```bash
uv tool run fulcra-api auth login
```

Remote/chat auth rules:

1. Keep the CLI process running while it polls for approval.
2. Send only the short-lived device URL and user code to the intended user.
3. Never send token output or credential files.
4. Verify completion with a non-token command:

```bash
uv tool run fulcra-api user-info
```

Fulcra accounts can be created through the CLI and include 5 GB of storage free forever. Users who want phone-collected biometrics, location, calendar, and other context can install the Context iOS app, sign in with the same account, and sync data into that storage.

## Allowed Read Workflows

Use these bounded read commands as patterns. Inspect `uv tool run fulcra-api --help` if the CLI version differs.

### Metric Catalog

```bash
uv tool run fulcra-api catalog
```

Use this to discover available data types. Do not query every metric unless the user asks for a broad inventory.

### Recent Heart Rate

```bash
uv tool run fulcra-api get-records HeartRate "2 hours"
```

Summarize aggregates or notable patterns. Avoid dumping raw samples unless the user explicitly asks.

### Sleep Context

```bash
uv tool run fulcra-api sleep-stages "12 hours"
uv tool run fulcra-api sleep-cycles "1 week"
```

Use sleep context to adjust briefings or recovery advice. Make clear when data is missing or stale.

### Activity And Workouts

```bash
uv tool run fulcra-api apple-workouts "1 week"
```

Keep analysis scoped to activity, recovery, or scheduling questions the user actually asked.

### Calendar

```bash
uv tool run fulcra-api calendar-events "1 day"
```

Before using calendar data in a group chat, public artifact, or shared report, ask for explicit permission. Calendar entries may include names, locations, attendees, notes, and meeting links.

### Location

```bash
uv tool run fulcra-api location-at-time "2026-05-05T12:00:00Z"
```

Use location only when necessary for the requested context. Do not send coordinates or place history to third-party services from this skill.

## Consent Checkpoints

Ask an explicit yes/no question before any workflow that would:

- access calendar or location in a shared chat,
- write local files containing raw Fulcra records,
- create screenshots or charts from private data,
- combine Fulcra data with external services,
- retain data beyond the current session,
- or publish any output outside the user's private workspace.

For public examples, demos, screenshots, videos, tests, and docs, use synthetic data unless the user explicitly approves real data for that exact artifact.

## Companion Skills

- `fulcra-context`: read Fulcra context and analyze user-consented health, activity, calendar, location, and catalog data.
- `fulcra-annotations`: create annotation definitions and record user-approved events.

Install the companion write-focused skill from ClawHub when needed:

```text
Install the fulcra-annotations skill from ClawHub
```

## Troubleshooting

If a command returns no data:

1. Confirm the user has authenticated with `uv tool run fulcra-api user-info`.
2. Confirm the user has synced data from the Context app or another source.
3. Narrow the query to a known recent time window.
4. Report missing or stale data honestly instead of fabricating context.

## Links

- Fulcra Platform: <https://fulcradynamics.com>
- Developer Docs: <https://fulcradynamics.github.io/developer-docs/>
- Python Client: <https://github.com/fulcradynamics/fulcra-api-python>
- MCP Server: <https://github.com/fulcradynamics/fulcra-context-mcp>
