# BasicOps MCP verification

Use this reference after configuration or when investigating whether BasicOps MCP is already usable.

## What to verify

A good verification sequence checks three things:

1. the BasicOps MCP server is registered
2. BasicOps tools are visible
3. at least one low-risk call can succeed

## Good low-risk checks

Prefer a harmless read.

Examples:
- inspect whether BasicOps tools are present
- use a client-native probe command when available, for example `openclaw mcp probe <name>`
- call a minimal identity or workspace read if the environment exposes one safely
- verify that a BasicOps read tool returns an authentication-success response instead of unauthorized

## Signs of success

- the tool surface clearly includes BasicOps tools
- probe-style verification shows a healthy non-trivial tool count when the client exposes counts
- no unauthorized or missing-server errors remain
- a simple read succeeds

## Signs of incomplete setup

- the server is present but no tools are visible
- probe-style verification returns zero or near-zero tools when dozens are expected
- the server is visible but unauthorized
- the client still needs a reload or restart
- the wrong auth header format was used

## Completion message shape

Keep the verification summary short.

Examples:
- "BasicOps MCP is connected and the tool surface is visible."
- "The BasicOps MCP server is configured, but this client still needs a reload before the tools will appear."
- "The server entry exists, but authentication is failing."
