# OpenClaw MCP installation

This skill requires a working OpenClaw MCP server entry. A skill alone does not create a live MCP runtime.

## Default isolated server

Add this under OpenClaw config `mcp.servers`:

```json5
{
  mcp: {
    servers: {
      "chrome-devtools": {
        enabled: true,
        transport: "stdio",
        command: "npx",
        args: [
          "-y",
          "chrome-devtools-mcp@latest",
          "--isolated",
          "--no-usage-statistics",
          "--no-performance-crux"
        ],
        connectTimeout: 20,
        timeout: 120,
        supportsParallelToolCalls: false
      }
    }
  }
}
```

## OpenClaw UI mapping

Use these fields:

```text
Server name: chrome-devtools
Enabled: true
Transport: stdio
Command: npx
Args:
  - -y
  - chrome-devtools-mcp@latest
  - --isolated
  - --no-usage-statistics
  - --no-performance-crux
Connect timeout: 20000 ms
Request timeout: 120000 ms
Parallel tool calls: false
```

Do not use an empty custom entry. Do not leave `Transport` unset. A server with missing transport is invalid and cannot be used.

## Diagnostics

Run:

```bash
openclaw mcp reload
openclaw mcp status --verbose
openclaw mcp doctor --probe
openclaw mcp probe chrome-devtools
```

Expected result:

```text
chrome-devtools enabled
transport stdio
command npx
probe successful
```

If `probe` fails, verify:

- `node` is installed
- `npm` is installed
- `npx -y chrome-devtools-mcp@latest --help` works in the same environment as OpenClaw
- Chrome or the configured browser is installed
- the OpenClaw runtime can start child processes
- the server definition has been saved and published
