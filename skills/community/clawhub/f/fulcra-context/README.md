# Fulcra Context

Fulcra Context is a docs-first ClawHub skill for connecting agents to user-consented Fulcra data through the hosted MCP server or Fulcra CLI.

The published ClawHub package intentionally does not include executable helper scripts. That keeps the install surface narrow: no install hooks, no transcript processing, no third-party enrichment, no raw export utilities, no background jobs, and no arbitrary CLI wrapper.

## Quick Start

1. Authenticate with Fulcra:

   ```bash
   uv tool run fulcra-api auth login
   ```

   For remote agents, share only the device URL and user code with the intended user. Never share token output or credential files.

   Check live help before relying on new auth options:

   ```bash
   uv tool run fulcra-api auth login --help
   ```

2. Verify access:

   ```bash
   uv tool run fulcra-api user-info
   ```

3. Read only the data needed for the current task:

   ```bash
   uv tool run fulcra-api catalog
   uv tool run fulcra-api get-records HeartRate "2 hours"
   uv tool run fulcra-api sleep-stages "12 hours"
   uv tool run fulcra-api calendar-events "1 day"
   uv tool run fulcra-api metric-time-series --help
   ```

## Privacy Rules

- Ask before reading Fulcra data.
- Keep reads scoped to the user's request.
- Do not expose tokens, credential files, raw private records, or capability URLs.
- Ask before using calendar or location in shared contexts.
- Do not send coordinates or place history to third-party services from this skill.
- Use synthetic data for public demos, screenshots, docs, and tests unless the user explicitly approves real data for that exact artifact.

## What To Use This Skill For

- Sleep and recovery context.
- Recent biometric or activity summaries.
- Metric catalog discovery.
- Calendar-aware private briefings.
- Location-aware private assistance when explicitly requested.

Use `fulcra-annotations` for write workflows such as creating annotation definitions or recording user-approved events.

## MCP Server

Hosted MCP endpoint:

```text
https://mcp.fulcradynamics.com/mcp
```

MCP tokens are not Fulcra API tokens. Do not send MCP tokens to `api.fulcradynamics.com`; restart the MCP OAuth flow if a hosted MCP client gets 401/auth failures after token expiry or a server redeploy.

Claude Desktop example:

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

## Source Helpers

The GitHub repository may contain optional source helper scripts for maintainers and advanced local deployments. Those scripts are not part of the ClawHub skill package. If you clone the source repository and run helper scripts manually, review the code, use private output directories, and get explicit user approval for any local files, calendar/location access, or persistent exports.

## Links

- Fulcra Platform: <https://fulcradynamics.com>
- Developer Docs: <https://docs.fulcradynamics.com>
- Python Client: <https://github.com/fulcradynamics/fulcra-api-python>
- MCP Server: <https://github.com/fulcradynamics/fulcra-context-mcp>
