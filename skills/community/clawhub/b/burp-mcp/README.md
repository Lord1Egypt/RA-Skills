# burp-mcp

Connect to a local Burp Suite MCP Server over SSE and list/call Burp tools from an OpenClaw workspace.

## What this is

This skill wraps the official Python MCP SDK and talks to the PortSwigger Burp Suite MCP extension over SSE.

Default endpoint:

```text
http://127.0.0.1:9876/
```

On this setup, the live SSE endpoint is `/`, not `/sse`.

## Files

- `SKILL.md` — skill instructions and usage guidance
- `config.json` — configurable SSE URL
- `scripts/burp_mcp.py` — CLI for listing and calling Burp MCP tools

## Requirements

- Python
- `mcp` Python package installed
- Burp Suite running locally with the PortSwigger MCP extension enabled

## Usage

From inside the repo:

List tools:

```bash
python ./scripts/burp_mcp.py list-tools
```

Call a tool:

```bash
python ./scripts/burp_mcp.py call <tool_name> '<json_args>'
```

Example:

```bash
python ./scripts/burp_mcp.py call get_proxy_http_history '{"offset":0,"count":5}'
```

From an OpenClaw workspace where this skill is installed under `skills/burp-mcp/`:

```bash
python ./skills/burp-mcp/scripts/burp_mcp.py list-tools
python ./skills/burp-mcp/scripts/burp_mcp.py call get_proxy_http_history '{"offset":0,"count":5}'
```

## Agent usage pattern

1. Run `list-tools`
2. Read `inputSchema`
3. Build matching JSON args
4. Run `call <tool_name> '<json_args>'`
5. Parse `content[].text` if the Burp tool returns embedded JSON text blocks

## Notes

- Safe read-first tools include history, scanner issue, and config export functions
- Some Burp tools mutate state; check the tool description before calling
- Output is intentionally raw MCP-shaped JSON so agents can post-process it cleanly
