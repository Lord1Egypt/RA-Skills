---
name: "agent3-hub"
version: "1.0.0"
description: "Universal AI resource registry — search and invoke agents, MCP servers, and APIs through a single MCP endpoint. Includes Telegram content search, Google search, X/Twitter search, and more."
tags: ["mcp", "registry", "search", "agents", "api", "telegram", "google", "twitter", "a2a"]
metadata:
  openclaw:
    requires:
      env:
        - AGENT3_API_KEY
---

# Agent3 Hub

Agent3 Hub is an open registry for AI agents, MCP servers, and APIs. It exposes every registered resource as a tool via a single MCP endpoint — connect once, invoke anything.

**Endpoint:** `https://hub.agent3.me/api/mcp`
**Protocol:** MCP 2025-03-26 (Streamable HTTP)
**Get a free API key:** https://hub.agent3.me/auth/signup

---

## Setup

### Claude Desktop / any MCP client

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agent3": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://hub.agent3.me/api/mcp"],
      "env": {
        "AGENT3_API_KEY": "a2a_your_key_here"
      }
    }
  }
}
```

### Direct HTTP (curl)

```bash
curl -X POST https://hub.agent3.me/api/mcp \
  -H "Authorization: Bearer $AGENT3_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "resources_search",
      "arguments": { "query": "telegram search" }
    }
  }'
```

### Anthropic SDK (Python)

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    mcp_servers=[{
        "type": "url",
        "url": "https://hub.agent3.me/api/mcp",
        "headers": {"Authorization": "Bearer a2a_your_key_here"}
    }],
    messages=[{"role": "user", "content": "Search Telegram for 'AI agents 2026'"}]
)
```

---

## Available Tools

| Tool | Description | Auth |
|------|-------------|------|
| `resources_search` | Search the registry by keyword or semantic query | Required |
| `resources_invoke` | Invoke any registered resource by ID + operation | Required |
| `resources_get` | Get full details of a resource by ID | Required |
| `resources_resolve` | Resolve a resource endpoint URL | Required |
| `resources_stats` | Get usage stats for a resource | Required |
| `agents_search` | Text search across registered agents | Required |
| `agents_semantic_search` | Semantic/vector search across agents | Required |
| `agents_get` | Get agent details by ID | Required |
| `agents_invoke` | Invoke an A2A agent directly | Required |
| `agents_register` | Register a new agent in the hub | Required |
| `tools/list` | List all available tools | Public |
| `resources/list` | List all resources | Public |
| `initialize` | Server info and capabilities | Public |

---

## Example: Search Telegram Content

```bash
curl -X POST https://hub.agent3.me/api/mcp \
  -H "Authorization: Bearer $AGENT3_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "resources_invoke",
      "arguments": {
        "resourceId": "a23cc5a9-0bfb-4466-acbe-fbc9af723ba4",
        "operationId": "search-content",
        "input": { "query": "AI news" }
      }
    }
  }'
```

## Example: Search Google

```bash
curl -X POST https://hub.agent3.me/api/mcp \
  -H "Authorization: Bearer $AGENT3_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "resources_invoke",
      "arguments": {
        "resourceId": "a5a14786-6738-47e2-a8e7-982ca4a90735",
        "operationId": "search",
        "input": { "query": "MCP protocol 2026" }
      }
    }
  }'
```

---

## Rate Limits (Free Tier)

| Category | Daily Limit |
|----------|-------------|
| Telegram search | 20 calls/day |
| Google search | 20 calls/day |
| X/Twitter search | 20 calls/day |
| Registry search & get | Unlimited |

Limits reset at midnight UTC. Upgrade available at hub.agent3.me.

---

## Resource Types

| Type | Description |
|------|-------------|
| `agent` | A2A protocol AI agents |
| `api` | REST / GraphQL / MCP web services |
| `sdk` | Software development kits |
| `data` | Data services and feeds |

---

## Links

- Registry: https://hub.agent3.me
- Docs: https://hub.agent3.me/docs
- Get API key: https://hub.agent3.me/auth/signup
- MCP endpoint: https://hub.agent3.me/api/mcp
