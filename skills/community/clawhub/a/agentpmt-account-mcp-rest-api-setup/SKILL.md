---
name: agentpmt-account-mcp-rest-api-setup
description: "Connect an agent, app, or integration to AgentPMT with an AgentPMT account Bearer Token. Use when configuring the hosted MCP server, the local npm MCP router, or direct REST API calls for tools, skills, workflows, and agents."
version: 1.0.0
homepage: https://www.agentpmt.com/docs/mcp-reference/connection
compatibility: "Requires an AgentPMT account and the agent Bearer Token from that Agent Group. No wallet signing or x402 payment setup is required for this path."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/docs/mcp-reference/connection"}}
---

# AgentPMT Account MCP And REST API Setup

Use this skill when an agent, app, or integration has an AgentPMT account Bearer Token and should call AgentPMT tools through MCP or REST.

## What This Is For

This path is for account-backed access. The user creates or selects an Agent Group, adds the tools and workflows the caller may use, adds any required software credentials, and copies the Agent Group Bearer Token. The Bearer Token authorizes calls against that Agent Group catalog.

Use the no-account AgentAddress/x402 skill instead when the caller does not have an AgentPMT account Bearer Token.

## Requirements

- AgentPMT account.
- Agent Group with the tools, workflows, and credentials the caller may use.
- Bearer Token from the Agent Group.
- MCP-compatible client for MCP usage, or any HTTP client for REST usage.

## Get The Bearer Token

In AgentPMT, open the Agent Group that should own this access, add the tools, workflows, and credentials the caller may use, and copy the Bearer Token. The Bearer Token is the only account credential used for MCP and REST API calls.

## Hosted MCP Server

Use this for agents that support remote MCP over HTTP.

Endpoint:

```text
https://api.agentpmt.com/mcp/
```

Configuration shape:

```json
{
  "mcpServers": {
    "agentpmt": {
      "url": "https://api.agentpmt.com/mcp/",
      "headers": {
        "Authorization": "Bearer <agentpmt_bearer_token>"
      }
    }
  }
}
```

After connecting, ask the client to list MCP tools. AgentPMT returns the tools and workflows available to the Agent Group attached to the Bearer Token.

## Local STDIO MCP Router

Use this when the agent client requires a local MCP command instead of a remote MCP URL.

```bash
npm install -g @agentpmt/mcp-router
agentpmt-setup
```

The setup command prompts for the Bearer Token and writes the client config. For manual configuration:

```json
{
  "mcpServers": {
    "agentpmt": {
      "command": "npx",
      "args": ["--package=@agentpmt/mcp-router@latest", "agentpmt-router"],
      "env": {
        "AGENTPMT_BEARER_TOKEN": "<agentpmt_bearer_token>",
        "AGENTPMT_MCP_ENDPOINT": "https://api.agentpmt.com/mcp/"
      }
    }
  }
}
```

The local router is a thin relay to AgentPMT. Tool execution happens in AgentPMT, not on the user's machine.

## Direct MCP Protocol

Use this only when writing an MCP client directly.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "clientInfo": {"name": "my-agent", "version": "1.0"},
    "capabilities": {}
  }
}
```

Then call:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

Use the exact tool names returned by `tools/list` when calling:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "<tool_name_from_tools_list>",
    "arguments": {}
  }
}
```

## REST API For Tools

Use REST when an agent, app, backend service, automation, or other program should integrate AgentPMT tools through authenticated HTTP calls. Additional examples and endpoint documentation is available here https://www.agentpmt.com/docs/api-reference/programmatic-access?format=agent-md

List available tools:

```http
GET https://api.agentpmt.com/products/fetch
Authorization: Bearer <agentpmt_bearer_token>
```

Invoke a tool:

```http
POST https://api.agentpmt.com/products/purchase
Authorization: Bearer <agentpmt_bearer_token>
Content-Type: application/json
```

Request body:

```json
{
  "name": "<product_slug_or_tool_name>",
  "parameters": {
    "action": "<action_name>"
  }
}
```

Use a generated product skill for the product-specific `name`, action names, schema, and sample parameters.

## Workflows

For workflows, prefer MCP. The main AgentPMT MCP server exposes the tools, workflows, and workflow-control tools available to the Agent Group behind the Bearer Token. Use `tools/list` first, then call the exact returned tool name.

## Troubleshooting

| Problem | Check |
|---|---|
| No tools appear | The Agent Group may not have tools or workflows added. |
| 401 authentication error | Re-copy or rotate the Bearer Token from the Agent Group. |
| Tool is missing | Add the product or workflow to the Agent Group, then refresh the MCP tool list. |
| Credential error | Add the required software connection credentials to the Agent Group. |

## Related Skills

- What AgentPMT is: ../what-is-agentpmt
- No-account AgentAddress/x402 flow: ../agentpmt-no-account-agentaddress-x402
