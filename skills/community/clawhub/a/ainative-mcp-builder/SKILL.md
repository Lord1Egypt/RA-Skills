---
name: ainative-mcp-builder
description: Build and publish custom MCP servers on AINative. Use when (1) Creating a new MCP server from scratch, (2) Adding tools to an existing MCP server, (3) Publishing an MCP server to ClawHub/npm, (4) Integrating an MCP server with Claude Code or Cursor, (5) Using FastMCP (Python) or the MCP SDK (Node.js). Closes #1523.
---

# AINative MCP Builder Guide

## What is an MCP Server?

Model Context Protocol (MCP) servers expose tools that AI agents (Claude Code, Cursor, Windsurf, etc.) can call directly. AINative's MCP servers (zerodb-mcp-server, zerodb-memory-mcp) are built this way.

## Python — FastMCP

```bash
pip install fastmcp
```

```python
# my_mcp_server.py
from fastmcp import FastMCP
import requests

mcp = FastMCP("my-tools")
API_KEY = "ak_your_key"
BASE = "https://api.ainative.studio"

@mcp.tool()
def get_user_credits() -> dict:
    """Get the current user's credit balance."""
    return requests.get(
        f"{BASE}/api/v1/public/credits/balance",
        headers={"X-API-Key": API_KEY}
    ).json()

@mcp.tool()
def search_memory(query: str, limit: int = 5) -> dict:
    """Search agent memory semantically."""
    return requests.post(
        f"{BASE}/api/v1/public/memory/v2/recall",
        headers={"X-API-Key": API_KEY},
        json={"query": query, "limit": limit}
    ).json()

@mcp.tool()
def store_memory(content: str, memory_type: str = "episodic") -> dict:
    """Store a fact or event in agent memory."""
    return requests.post(
        f"{BASE}/api/v1/public/memory/v2/remember",
        headers={"X-API-Key": API_KEY},
        json={"content": content, "memory_type": memory_type}
    ).json()

if __name__ == "__main__":
    mcp.run()
```

```bash
python my_mcp_server.py
```

## Node.js — MCP SDK

```bash
npm install @modelcontextprotocol/sdk
```

```typescript
// server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server(
  { name: 'my-mcp-server', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler('tools/list', async () => ({
  tools: [{
    name: 'get_credits',
    description: 'Get current credit balance',
    inputSchema: { type: 'object', properties: {} }
  }]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'get_credits') {
    const resp = await fetch('https://api.ainative.studio/api/v1/public/credits/balance', {
      headers: { 'X-API-Key': process.env.AINATIVE_API_KEY! }
    });
    return { content: [{ type: 'text', text: JSON.stringify(await resp.json()) }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Configure in Claude Code

```json
// .claude/mcp.json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["my_mcp_server.py"],
      "env": { "AINATIVE_API_KEY": "ak_your_key" }
    }
  }
}
```

For a published npm package:
```json
{
  "mcpServers": {
    "my-tools": {
      "command": "npx",
      "args": ["my-mcp-package"],
      "env": { "AINATIVE_API_KEY": "ak_your_key" }
    }
  }
}
```

## SKILL.md Format for ClawHub

Every MCP tool should have a matching skill file so agents know when to call it:

```markdown
---
name: my-tool-name
description: One-line description. Use when (1) scenario, (2) scenario, (3) scenario.
---

# Tool Name

Brief description and usage examples.
```

Place in `.claude/skills/my-tool-name/SKILL.md`.

## Publish to npm

```bash
# package.json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "bin": { "my-mcp-server": "./dist/server.js" },
  "main": "./dist/server.js"
}

npm publish
```

## References

- `zerodb-mcp-server/` — Full 76-tool example (Node.js)
- `zerodb-memory-mcp/` — Lightweight 6-tool example (Node.js)
- `src/backend/app/api/v1/endpoints/zerodb_mcp.py` — Backend tool handlers
- MCP spec: `https://modelcontextprotocol.io`
