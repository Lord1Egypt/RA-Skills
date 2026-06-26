# BasicOps MCP setup flow

Use this reference for the main installation and configuration sequence.

## Default connection shape

The preferred BasicOps MCP connection shape is:

- URL: `https://app.basicops.com/mcp`
- Transport: streamable HTTP
- Auth: `Authorization: Bearer <basicops-api-key>`

Never hard-code a real token into the skill. Treat the token as user secret material.

## End-to-end flow

1. Check whether a BasicOps MCP server is already present.
2. If present, verify that it exposes usable BasicOps tools.
3. If missing, add a BasicOps MCP server entry to the client’s MCP configuration.
4. Add authentication using a BasicOps API key, usually sent as a bearer token.
5. Reload or restart the client if required.
6. Verify tool visibility and a low-risk read.
7. Hand off to the operator skill.

## Minimal config ingredients

Most MCP clients need the same logical pieces even if the syntax differs:

- server name, for example `basicops`
- server URL
- transport type
- auth header or secret reference

## Minimal user questions

Ask only for what is actually missing.

Typical missing pieces:
- Do you already have a BasicOps API key?
- Which MCP client should I configure?
- Am I allowed to edit the local MCP config for this environment?

## When to stop and ask

Stop and ask if:
- the environment is not MCP-capable
- the client config location is unknown and cannot be discovered safely
- the user has no BasicOps bearer token yet
- a reload/restart is required and the environment cannot do it automatically

## Good completion pattern

- say that BasicOps MCP is configured
- say whether a restart or reload is still needed
- say whether tool visibility was verified
- say it is ready for the operator skill
