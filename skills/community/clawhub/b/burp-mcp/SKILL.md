---
name: burp-mcp
slug: burp-mcp
version: 0.1.0
description: Connect to a local Burp Suite MCP Server over SSE and list or call Burp tools from the workspace. Use when Burp Suite is running with the PortSwigger MCP extension enabled on http://127.0.0.1:9876/.
metadata: {"clawdbot":{"requires":{"bins":["python"]},"os":["win32","linux","darwin"],"install":[{"id":"python-mcp","kind":"pip","package":"mcp","label":"Install the official Python MCP SDK"}],"configPaths.optional":["./skills/burp-mcp/config.json"]}}
---

# Burp MCP

Use this skill to talk to a **local Burp Suite MCP Server** exposed by the PortSwigger extension.

## When to use

- Burp Suite is already running locally
- The MCP extension is loaded and enabled
- You want to inspect available Burp tools
- You want to call a specific Burp MCP tool from the terminal or from OpenClaw via `exec`

## Endpoint

Default endpoint used by this skill:

```text
http://127.0.0.1:9876/
```

Important: on this machine, the live SSE endpoint is `/`, not `/sse`.

## Commands

List Burp tools:

```bash
python ./skills/burp-mcp/scripts/burp_mcp.py list-tools
```

Call a Burp tool:

```bash
python ./skills/burp-mcp/scripts/burp_mcp.py call <tool_name> '<json_args>'
```

Examples:

```bash
python ./skills/burp-mcp/scripts/burp_mcp.py list-tools
python ./skills/burp-mcp/scripts/burp_mcp.py call get_proxy_http_history '{"offset":0,"count":5}'
python ./skills/burp-mcp/scripts/burp_mcp.py call get_proxy_http_history_regex '{"offset":0,"count":10,"regex":"login|token|auth"}'
python ./skills/burp-mcp/scripts/burp_mcp.py call output_project_options '{}'
```

## How agents should use it

### 1) Always start with `list-tools`

Burp MCP tool names and schemas can change with extension version. Before calling tools in a new setup, list tools first:

```bash
python ./skills/burp-mcp/scripts/burp_mcp.py list-tools
```

This returns JSON entries with:
- `name`
- `description`
- `inputSchema`

### 2) Match args to `inputSchema`

When calling a tool, build the JSON object to match the tool's required schema exactly.

Example:

- `get_proxy_http_history` requires:
  - `offset` (integer)
  - `count` (integer)

So call it like:

```bash
python ./skills/burp-mcp/scripts/burp_mcp.py call get_proxy_http_history '{"offset":0,"count":20}'
```

### 3) Prefer safe read-only tools first

Safe first calls:
- `get_proxy_http_history`
- `get_proxy_http_history_regex`
- `get_proxy_websocket_history`
- `get_scanner_issues`
- `output_project_options`
- `output_user_options`

Be careful with mutation tools such as:
- `set_project_options`
- `set_user_options`
- `set_proxy_intercept_state`
- `set_task_execution_engine_state`
- `set_active_editor_contents`

## Output behavior

- `list-tools` prints JSON array of tools
- `call` prints JSON object:
  - `isError`
  - `content`

Burp often returns tool results as `text` blocks. Some tools return newline-separated JSON strings inside `content[].text`, so callers may need a second parse step if they want structured output.

## Troubleshooting

- If connection fails, verify Burp is open and the MCP extension is enabled
- If `/sse` fails, use `/` instead
- If tool calls return schema errors, re-run `list-tools` and check `inputSchema`
- If nothing returns, test manually with:

```bash
curl http://127.0.0.1:9876 -v
```

A healthy server should return `text/event-stream`

## Notes

- Uses the official Python `mcp` SDK
- Requires asyncio
- Assumes the `mcp` package is already installed in the active Python environment
