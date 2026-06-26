# Channels Reference

Channels are MCP servers that push external events into a Claude Code session. Available in research preview (v2.1.80+).

## Overview

A channel is an MCP server running locally, spawned by Claude Code as a subprocess over stdio.

- **One-way**: Forward alerts, webhooks, monitoring events for Claude to act on
- **Two-way**: Also expose a reply tool so Claude can respond back
- **Permission relay**: Opt in to relay permission prompts for remote approval

## Requirements

1. `@modelcontextprotocol/sdk` package
2. Declare `claude/channel` capability
3. Emit `notifications/claude/channel` events
4. Connect over stdio transport

## Building a Webhook Receiver

### 1. Create project and install SDK

```bash
mkdir webhook-channel && cd webhook-channel
bun add @modelcontextprotocol/sdk
```

### 2. Write the channel server (`webhook.ts`)

```typescript
#!/usr/bin/env bun
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

const mcp = new Server(
  { name: 'webhook', version: '0.0.1' },
  {
    capabilities: { experimental: { 'claude/channel': {} } },
    instructions: 'Events from the webhook channel arrive as <channel source="webhook" ...>.',
  },
)

await mcp.connect(new StdioServerTransport())

Bun.serve({
  port: 8788,
  hostname: '127.0.0.1',
  async fetch(req) {
    const body = await req.text()
    await mcp.notification({
      method: 'notifications/claude/channel',
      params: {
        content: body,
        meta: { path: new URL(req.url).pathname, method: req.method },
      },
    })
    return new Response('ok')
  },
})
```

### 3. Register in MCP config

```json
{
  "mcpServers": {
    "webhook": { "command": "bun", "args": ["./webhook.ts"] }
  }
}
```

### 4. Test with development flag

```bash
claude --dangerously-load-development-channels server:webhook
```

```bash
curl -X POST localhost:8788 -d "build failed on main"
```

## Server Options

- `capabilities.experimental['claude/channel']` — declares channel capability
- `instructions` — added to Claude's system prompt

## Notification Format

```typescript
{
  method: 'notifications/claude/channel',
  params: {
    content: string,      // body of <channel> tag
    meta: Record<string, string>  // becomes tag attributes
  }
}
```

## Expose a Reply Tool

Add a tool handler to your MCP server so Claude can send messages back through the channel.

## Gate Inbound Messages

Implement sender checks to prevent prompt injection from untrusted sources.

## Relay Permission Prompts

Forward tool approval prompts to remote channels for approval/denial.

## Troubleshooting

- **Event doesn't arrive**: Run `/mcp` to check server status. Check `~/.claude/debug/<session-id>.txt`
- **Connection refused**: Port not bound or stale process. Use `lsof -i :<port>` to diagnose
