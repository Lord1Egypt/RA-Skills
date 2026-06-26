---
name: add-tools
description: Search engine for AI agents to discover free and paid tools, APIs, and MCP servers
tags: [tools, search, api, x402, mcp, agents, discovery]
---

# add.tools

A search engine for AI agents to discover tools, APIs, and MCP servers — both free and paid (via x402 micropayments).

## What it does

add.tools indexes tools and API endpoints that AI agents can use. Agents send a search query and get back ranked results with metadata about each tool's capabilities, pricing, and reliability.

The index includes both free tools and paid x402-enabled endpoints, so agents can find the right tool regardless of pricing model.

## Usage

### Search for tools

```bash
# JSON response for agents
curl -H "Accept: application/json" "https://add.tools/search?q=send+email"

# With explicit format param
curl "https://add.tools/search?q=weather+forecast&format=json"
```

### Report feedback

```bash
curl -X POST "https://add.tools/feedback" \
  -H "Content-Type: application/json" \
  -d '{"query": "send email", "chosen_tool": "...", "success": true}'
```

Helps improve search quality over time.

## Content negotiation

Every URL on add.tools serves both humans and agents from the same URL. Set `Accept: application/json` or append `?format=json` for machine-readable responses. Default is HTML with clean server-rendered content that LLMs can also parse directly.

## Links

- Website: https://add.tools
- GitHub: https://github.com/add-tools
