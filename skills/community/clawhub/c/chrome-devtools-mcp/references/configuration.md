# Configuration

This skill uses two configuration layers.

## 1. OpenClaw MCP server configuration

This controls whether Chrome DevTools MCP exists as a usable MCP server.

Required fields for local stdio mode:

```json5
{
  mcp: {
    servers: {
      "chrome-devtools": {
        enabled: true,
        transport: "stdio",
        command: "npx",
        args: ["-y", "chrome-devtools-mcp@latest", "--isolated", "--no-usage-statistics", "--no-performance-crux"]
      }
    }
  }
}
```

Without this configuration, the skill can provide policy instructions but cannot operate the browser.

## 2. User policy configuration

This controls browser mode, browser type, profile, allowed URLs, protected data, and confirmation gates.

See `references/user-settings.md` and `examples/user-settings.example.json`.

## Required command

```bash
npx -y chrome-devtools-mcp@latest
```

## Default arguments

```text
--isolated
--no-usage-statistics
--no-performance-crux
```

## Mode-specific arguments

Isolated:

```text
--isolated
--no-usage-statistics
--no-performance-crux
```

Executable:

```text
--executable-path=<configured_browser_path>
--user-data-dir=<configured_profile_dir>
--no-usage-statistics
--no-performance-crux
```

Existing session:

```text
--browser-url=http://127.0.0.1:<port>
--no-usage-statistics
--no-performance-crux
```
