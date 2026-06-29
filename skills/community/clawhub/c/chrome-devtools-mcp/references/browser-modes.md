# Browser modes

## isolated

Default mode. Use for normal browser work when the task does not require a pre-existing login state.

Properties:

- temporary profile
- avoids normal user profile
- lowest-risk default
- suitable for navigation, inspection, screenshots, console/network debugging, and performance traces

MCP server args:

```text
-y
chrome-devtools-mcp@latest
--isolated
--no-usage-statistics
--no-performance-crux
```

## executable

Use when the user chooses Chrome, Chrome for Testing, Chromium, or a custom compatible executable.

Properties:

- explicit browser executable
- explicit user data directory
- Chromium is compatibility mode
- dedicated automation profile is required unless the user explicitly chooses a specific real profile

MCP server args:

```text
-y
chrome-devtools-mcp@latest
--executable-path=<configured_browser_path>
--user-data-dir=<configured_profile_dir>
--no-usage-statistics
--no-performance-crux
```

## existing-session

Use only when the user explicitly needs a running authenticated browser.

Properties:

- higher risk than isolated mode
- can access open tabs and signed-in state
- requires localhost-only browser URL
- requires explicit policy setting `allowExistingSession: true`

MCP server args:

```text
-y
chrome-devtools-mcp@latest
--browser-url=http://127.0.0.1:<port>
--no-usage-statistics
--no-performance-crux
```

Rejected endpoint examples:

```text
http://0.0.0.0:9222
http://192.168.1.10:9222
http://example.com:9222
```

Allowed endpoint examples:

```text
http://127.0.0.1:9222
http://localhost:9222
http://[::1]:9222
```
