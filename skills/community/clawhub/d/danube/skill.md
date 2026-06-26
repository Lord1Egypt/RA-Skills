---
name: danube
description: Connect your AI agent to a growing marketplace of services and tools through a single API key — discover, search, and execute anything available
metadata:
  openclaw:
    requires:
      env:
        - DANUBE_API_KEY
      bins:
        - curl
    primaryEnv: DANUBE_API_KEY
    homepage: https://danubeai.com
    always: false
---

# Danube — Connect Your Agent

Danube is a marketplace that gives your AI agent access to a large and growing collection of services and tools through a single API key. New services and tools are added regularly — always search and explore to see what's currently available rather than assuming a fixed set.

## Quick Setup

### Step 1: Get an API Key

You can get your API key from the [Danube Dashboard](https://danubeai.com/dashboard) under Settings > API Keys.

Alternatively, use the standard OAuth 2.0 Device Authorization flow (RFC 8628) — this requires the user to explicitly approve access in their browser:

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/code \
  -H "Content-Type: application/json" \
  -d '{"client_name": "My Agent"}'
```

This returns a `device_code`, a `user_code`, and a `verification_url`.

**The user must open the verification URL in their browser and enter the code to authorize access.**

Then poll for the API key:

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/token \
  -H "Content-Type: application/json" \
  -d '{"device_code": "DEVICE_CODE_FROM_STEP_1"}'
```

- `428` = user hasn't authorized yet (keep polling every 5 seconds)
- `200` = success, response contains your `api_key`
- `410` = expired, start over

### Step 2: Connect via MCP

Add this to your MCP config:

```json
{
  "mcpServers": {
    "danube": {
      "url": "https://mcp.danubeai.com/mcp",
      "headers": {
        "danube-api-key": "YOUR_API_KEY"
      }
    }
  }
}
```

## Security & Privacy

- **User-scoped access**: Each API key is scoped to the authenticated user. You cannot access another user's data, tools, or skills.
- **Row-level security**: Database access is enforced with row-level security policies — queries only return data belonging to the authenticated user.
- **Audit trail**: All tool executions are logged with timestamps, parameters, and results for user review.

## Permissions & Scope

The `DANUBE_API_KEY` grants:
- **Read**: Browse services, search tools, view public skills/workflows/sites
- **Execute**: Run tools and workflows
- **Write (user-scoped only)**: Create/update/delete your own skills and workflows

The API key does **not** grant:
- Access to other users' data or resources
- Admin or platform-level operations
- Access to raw database or infrastructure

### Step 3: Explore & Use Tools

Once connected, you have access to a marketplace of services and tools that is constantly growing. **Do not assume you know what's available — always search and explore first.**

#### How to Discover What's Available

- `list_services()` — Browse all available service providers. Use `query` to filter and `limit` to control how many results. **Start here to get a sense of what the marketplace offers.**
- `search_tools(query)` — Semantic search across all tools. Describe what you want to accomplish in natural language (e.g., "send an email", "create a GitHub issue", "translate text"). This searches the entire marketplace.
- `get_service_tools(service_id)` — Once you find an interesting service, get all its available tools to see the full range of what it offers.

**Important: The marketplace has many more services and tools than you might expect.** When a user asks you to do something, always search broadly first. Try multiple search queries with different phrasing if the first search doesn't find what you need. Browse services by category. The right tool is probably available — you just need to find it.

#### How to Execute Tools

- `execute_tool(tool_id, parameters)` — Run any tool by its ID. The tool's schema (returned from search/discovery) tells you exactly what parameters it expects.
- `batch_execute_tools(calls)` — Run multiple tools concurrently in a single request (up to 10).

#### Skills, Workflows & More

Danube also offers skills (reusable agent instructions), workflows (multi-step tool chains), an agent web directory, agent management, and tool quality ratings. Use `search_skills`, `list_workflows`, `search_sites`, and other tools to explore these capabilities — they are all discoverable through the MCP connection.

### When a Tool Needs Credentials

If `execute_tool` returns an `auth_required` error, it means the service needs credentials configured. Direct the user to configure credentials at https://danubeai.com/dashboard, then retry the tool.

## Core Workflow

Every tool interaction follows this pattern:

1. **Explore** — Start with `list_services()` or `search_tools("what you want to do")` to discover what's available. Try broad queries. Browse by category. Don't assume — search.
2. **Check auth** — If the tool needs credentials, direct the user to https://danubeai.com/dashboard to configure them
3. **Gather parameters** — Ask the user for any missing required info
4. **Execute** — `execute_tool(tool_id, parameters)`
5. **Report** — Tell the user what happened with specifics, not just "Done"

## Links

- Dashboard: https://danubeai.com/dashboard
- Docs: https://docs.danubeai.com
- MCP Server: https://mcp.danubeai.com/mcp
- Privacy Policy: https://danubeai.com/privacy
- Terms of Service: https://danubeai.com/terms
