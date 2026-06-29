---
name: get-users-current-time-date
description: "Get Users Current Time / Date: Get the user's current date and time in their configured timezone. Use when an agent needs get users current time / date, user timezone datetime, get current local time for a user, build time aware reminders, schedule messages in the user timezone, add local timestamps to logs, get current datetime through AgentPMT-hosted remote tool calls. Discovery terms: get users current time / date, user timezone datetime, get current local time for a user."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/user-timezone-datetime
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/user-timezone-datetime"}}
---
# Get Users Current Time / Date

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Agents running in the cloud don't know what timezone their users are in. This tool returns the current date and time in the user's configured timezone so agents can schedule, format, and reason about time using the user's local context. The tool returns both local and UTC timestamps, the timezone name, and useful derived fields such as local date, local time, and UTC offset. This enables time aware workflows like reminders, deadlines, and calendar or messaging logic without repeatedly asking the user what time zone they are in.

## Product Instructions
### User Timezone DateTime

Returns the current date and time based on the user's configured timezone setting. Uses IANA timezone names (e.g., "America/New_York", "Europe/London") to provide accurate local time with UTC offset, DST detection, and formatted date/time components.

#### Actions

##### get_current_datetime

Returns the current local datetime, UTC datetime, and derived fields for the user's configured timezone.

**Required Parameters:** None (timezone is automatically injected from the user's account settings)

**Response Fields:**
- `timezone` (string) -- IANA timezone name used (e.g., "America/Chicago")
- `utc_datetime` (string) -- Current UTC datetime in ISO 8601 format
- `local_datetime` (string) -- Current local datetime in ISO 8601 format
- `local_date` (string) -- Local date in YYYY-MM-DD format
- `local_time` (string) -- Local time in HH:MM:SS format
- `utc_offset` (string) -- UTC offset formatted as "+HH:MM" or "-HH:MM"
- `utc_offset_minutes` (integer) -- UTC offset in total minutes
- `is_dst` (boolean or null) -- Whether daylight saving time is currently active

**Example Request:**
```json
{
  "action": "get_current_datetime"
}
```

**Example Response:**
```json
{
  "action": "get_current_datetime",
  "timezone": "America/New_York",
  "utc_datetime": "2026-03-10T18:30:00+00:00",
  "local_datetime": "2026-03-10T14:30:00-04:00",
  "local_date": "2026-03-10",
  "local_time": "14:30:00",
  "utc_offset": "-04:00",
  "utc_offset_minutes": -240,
  "is_dst": true
}
```

#### Workflows

1. **Check current time before scheduling** -- Call `get_current_datetime` to determine the user's current local time before creating calendar events or setting reminders.
2. **Time-aware greetings** -- Use `local_time` to provide contextual greetings (good morning/afternoon/evening) based on the user's actual local time.
3. **Cross-timezone coordination** -- Use `utc_datetime` and `utc_offset` together to help users coordinate meetings across different timezones.
4. **DST awareness** -- Check the `is_dst` field to inform users about daylight saving time status when scheduling recurring events.

#### Notes

- The user's timezone is automatically provided from their account settings; no manual timezone input is needed.
- If the user has not configured a timezone, the request will fail with a validation error ("User timezone is required").
- All IANA timezone names are supported (e.g., "US/Eastern", "Asia/Tokyo", "Pacific/Auckland").
- The `is_dst` field may return `null` for timezones that do not observe daylight saving time.
- UTC offset is provided in both human-readable string format and numeric minutes for programmatic use.

## When To Use
- Use this skill for `Get Users Current Time / Date` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: get users current time / date, user timezone datetime, get current local time for a user, build time aware reminders, schedule messages in the user timezone, add local timestamps to logs, get current datetime.
- Supported action names: `get_current_datetime`.

## Use Cases
- Get current local time for a user
- Build time aware reminders
- Schedule messages in the user timezone
- Add local timestamps to logs
- Convert between UTC and user local time
- Validate timezone configuration
- Generate date strings for reports

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `get_current_datetime` (action slug: `get-current-datetime`): Returns the current local datetime, UTC datetime, and derived fields (local date, local time, UTC offset, DST status) based on the user's configured timezone. Price: `3` credits. Parameters: none.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "user-timezone-datetime"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "user-timezone-datetime"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "user-timezone-datetime"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "user-timezone-datetime"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "user-timezone-datetime"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "user-timezone-datetime"
  }
}
```

## Call This Tool
Product slug: `user-timezone-datetime`

Marketplace page: https://www.agentpmt.com/marketplace/user-timezone-datetime

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Get-Users-Current-Time--Date",
    "arguments": {
      "action": "get_current_datetime"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "user-timezone-datetime",
  "parameters": {
    "action": "get_current_datetime"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_current_datetime` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/user-timezone-datetime
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
