---
name: mcp-builder
description: |
  Bootstraps new Model Context Protocol (MCP) servers from a natural language description. Use when the user asks to build an MCP server, create an MCP tool, scaffold an MCP integration, or add MCP capabilities to an existing project.
  NOT for: general API design, non-MCP tool building, or frontend tasks.
version: 1.0.0
author: asimons81
source: https://github.com/asimons81/Agentic-Atlas
tags: [mcp, infrastructure, api, typescript, python, tooling]
agency_score: 7
---

# MCP Builder Skill

Bootstraps new Model Context Protocol servers from natural language descriptions.

## Instructions

When the user requests an MCP server or tool:

1. Identify the core functionality from the description
2. Determine the appropriate transport (stdio for CLI, SSE for web)
3. Scaffold a TypeScript or Python MCP server using the official SDK
4. Generate tool definitions from API schemas or describe them manually
5. Include a test harness with example invocations
6. Provide configuration for Claude Code, Cursor, and OpenCode

## Features

- TypeScript (recommended) and Python scaffolding
- Auto-generates tool definitions from API schemas (OpenAPI, JSON Schema)
- STDIO and SSE transport support
- Built-in error handling and validation
- Test harness with mock LLM calls
- Claude Code / Cursor / OpenCode configuration snippets

## Architecture

```
mcp-server/
├── src/
│   ├── index.ts          # Server entry point
│   ├── tools.ts          # Tool definitions
│   └── handlers.ts       # Request handlers
├── package.json
├── tsconfig.json
├── README.md
└── test/
    └── harness.ts        # Test harness
```

## Output Format

1. Project scaffold (all files)
2. Tool definitions with descriptions and input schemas
3. Configuration snippet for Claude Code's `mcpServers` config
4. Test invocation example

## Example

```
User: "Build an MCP server for our internal issue tracker with create, list, and close operations"

→ Generate: TypeScript MCP server with 3 tools, JSON Schema for each, test harness, Claude Code config
```

## Dependencies

Requires: Node.js 18+, TypeScript, @modelcontextprotocol/sdk
