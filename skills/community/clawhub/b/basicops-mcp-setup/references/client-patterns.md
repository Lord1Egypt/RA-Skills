# BasicOps MCP client patterns

Use this reference when fitting the BasicOps MCP connection into a specific MCP-capable environment.

## Principle

Do not assume every client uses the same config shape. Map the same logical connection into the client’s native MCP pattern.

Core connection ingredients stay the same:
- endpoint URL
- streamable HTTP transport
- bearer-token authentication

## Preferred behavior

### If the environment already has an MCP management tool
Use it.

Examples of acceptable behavior:
- update the client’s MCP registry through its supported command or UI
- use an existing config helper instead of manually editing JSON if that helper is already part of the environment

### If the environment stores MCP servers in config files
Add a BasicOps MCP server entry using the client’s expected schema.

### If the environment is OpenClaw-like
Expect MCP servers to live in a config structure with a server name plus transport details and headers.

OpenClaw quick recipe:

```bash
openclaw mcp add basicops --transport streamable-http \
  --url https://app.basicops.com/mcp \
  --header "Authorization=Bearer <KEY>"
openclaw mcp probe basicops
openclaw mcp reload
```

OpenClaw-specific notes:
- `--header` uses `KEY=value`, not HTTP-style `KEY: value`
- `openclaw mcp probe <name>` is a good verification step because it confirms tool visibility and authentication together
- `openclaw mcp reload` makes the tools available to the current runtime session instead of waiting for a future restart or new session

### If the environment is another MCP-capable agent client
Find the equivalent place where HTTP MCP servers are declared, then map the same URL, transport, and auth into that schema.

## Configuration shape to preserve

Whatever the client format, keep these semantics:
- name identifies BasicOps clearly
- URL points to the BasicOps MCP endpoint
- transport is HTTP-compatible and matches the client’s streamable HTTP support
- auth uses a bearer token and does not leak in normal replies

## Handoff rule

Once the BasicOps MCP surface is visible and verified, stop doing setup work and switch to `basicops-mcp-operator` for task/project operations.
