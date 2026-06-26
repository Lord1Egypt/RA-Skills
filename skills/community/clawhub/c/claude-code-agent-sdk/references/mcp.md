# Using MCP to Connect External Tools

> Configure MCP servers to extend your agent with external tools. Covers transport types, tool search, authentication, and error handling.

MCP (Model Context Protocol) connects AI agents to external tools and data sources.

## Quick Start

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use the docs MCP server to explain what hooks are in Claude Code",
  options: {
    mcpServers: {
      "claude-code-docs": { type: "http", url: "https://code.claude.com/docs/mcp" }
    },
    allowedTools: ["mcp__claude-code-docs__*"]
  }
})) { /* ... */ }
```

## Adding MCP Servers

### In Code

```typescript
// TypeScript - stdio server
mcpServers: {
  filesystem: {
    command: "npx",
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
  }
}

// HTTP/SSE server
mcpServers: {
  "remote-api": {
    type: "sse",  // or "http" for streamable HTTP
    url: "https://api.example.com/mcp/sse",
    headers: { Authorization: `Bearer ${process.env.API_TOKEN}` }
  }
}
```

```python
# Python
mcp_servers={
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"],
    }
}
```

### From Config File (`.mcp.json`)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
    }
  }
}
```

Load via `settingSources: ["project"]` (enabled by default).

## Allowing MCP Tools

Tool naming convention: `mcp__<server-name>__<tool-name>`

```typescript
allowedTools: [
  "mcp__github__*",           // All tools
  "mcp__db__query",           // Only query
  "mcp__slack__send_message"  // Only send_message
]
```

The `*` wildcard allows all tools from a server.

⚠️ `permissionMode: "acceptEdits"` does NOT auto-approve MCP tools. Use `allowedTools` wildcards instead of `bypassPermissions`.

## Transport Types

| Transport | When to Use | Configuration |
|:---|:---|:---|
| **stdio** | Local processes (command-line servers) | `command` + `args` + `env` |
| **HTTP/SSE** | Cloud-hosted/remote APIs | `type: "http"/"sse"` + `url` + `headers` |
| **SDK MCP** | Custom in-code tools | See [Custom Tools guide](/en/agent-sdk/custom-tools) |

## Authentication

### Environment Variables

```typescript
mcpServers: {
  github: {
    command: "npx",
    args: ["-y", "@modelcontextprotocol/server-github"],
    env: { GITHUB_TOKEN: process.env.GITHUB_TOKEN }
  }
}
```

`.mcp.json` uses `${GITHUB_TOKEN}` syntax.

### HTTP Headers

```typescript
mcpServers: {
  "secure-api": {
    type: "http",
    url: "https://api.example.com/mcp",
    headers: { Authorization: `Bearer ${process.env.API_TOKEN}` }
  }
}
```

### OAuth2

The SDK does not automatically handle OAuth flows. Complete OAuth in your application, then pass the access token via headers.

## Tool Search

When configuring many MCP tools, tool search hides tool definitions from context, loading only the tools needed for each turn. Enabled by default. See [Tool Search guide](/en/agent-sdk/tool-search) for details.

## Discovering Available Tools

```typescript
for await (const message of query({ prompt: "...", options })) {
  if (message.type === "system" && message.subtype === "init") {
    console.log("Available MCP tools:", message.mcp_servers);
  }
}
```

## Tool Search (Scaling to Thousands of Tools)

Enabled by default (requires Sonnet 4+/Opus 4+). Dynamically discovers and loads tools on demand, preventing context window bloat.

Configure via `ENABLE_TOOL_SEARCH` environment variable:

| Value | Behavior |
|-------|----------|
| (unset) | Enabled by default |
| `true` | Always enabled |
| `auto` | Activates when tool definitions >10% of context |
| `auto:N` | Custom threshold (e.g., `auto:5`) |
| `false` | Disabled, preloads all tools |

```python
options = ClaudeAgentOptions(
    mcp_servers={"enterprise": {"type": "http", "url": "https://tools.example.com/mcp"}},
    allowed_tools=["mcp__enterprise__*"],  # Wildcard pre-approval
    env={"ENABLE_TOOL_SEARCH": "auto:5"}
)
```

Limitations: Maximum 10,000 tools, returns 3-5 most relevant tools per search. Optimize with descriptive tool names and keyword-rich descriptions.