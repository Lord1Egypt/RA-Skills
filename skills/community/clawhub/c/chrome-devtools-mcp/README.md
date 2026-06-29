# chrome-devtools-mcp

OpenClaw skill package for safe, configurable use of the official Chrome DevTools MCP server.

This skill does not decide one fixed browser setup for everyone. It gives OpenClaw a browser-control policy.

The user chooses:

- isolated browser or existing session
- Chrome, Chrome for Testing, Chromium, or custom executable
- temporary profile or specific profile directory
- allowed and blocked URLs
- whether the agent may inspect cookies/storage
- whether the agent may submit forms or perform account-changing actions

The default is safest:

- isolated Chrome
- temporary profile
- cookie/storage inspection allowed for debugging, with secret values redacted by default
- form submission allowed only when configured and task-relevant
- no destructive actions without explicit confirmation
- telemetry disabled

## Critical distinction

Installing this skill is not enough to make Chrome DevTools MCP usable.

OpenClaw must also have an enabled MCP server definition under `mcp.servers`. If the UI shows a custom server with `missing transport`, the server is not configured and the agent cannot use Chrome DevTools MCP tools.

Use this default OpenClaw MCP server definition:

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

After saving/publishing the MCP config, run:

```bash
openclaw mcp reload
openclaw mcp status --verbose
openclaw mcp doctor --probe
openclaw mcp probe chrome-devtools
```

## Package structure

```text
chrome-devtools-mcp/
  SKILL.md
  README.md
  references/
    configuration.md
    browser-modes.md
    security-policy.md
    user-settings.md
    skillspector.md
    openclaw-mcp-install.md
  examples/
    mcp.chrome.isolated.json
    mcp.chromium.executable.json
    mcp.existing-session.json
    mcp.allowed-domain.json
    user-settings.example.json
    openclaw.mcp.chrome.isolated.json5
    openclaw.mcp.chromium.executable.json5
    openclaw.mcp.existing-session.json5
    openclaw.mcp.allowed-domain.json5
  scripts/
    validate_skill.py
```

## What this skill provides

This package provides instructions, configuration examples, security rules, validation checks, and publishing guidance for using Chrome DevTools MCP inside OpenClaw.

It does not implement a new MCP server. It wraps and documents correct use of the official `chrome-devtools-mcp` server.

Default MCP command:

```bash
npx -y chrome-devtools-mcp@latest
```

Default safe mode:

```bash
npx -y chrome-devtools-mcp@latest \
  --isolated \
  --no-usage-statistics \
  --no-performance-crux
```

## Browser modes

### 1. Isolated Chrome session

Default mode. Use it for normal browser tasks, page inspection, debugging, screenshots, and performance checks when no existing login state is required.

### 2. Configured browser executable

Use it when the user wants Chrome, Chrome for Testing, Chromium, or a custom compatible executable.

Chromium is compatibility mode. Do not assume it is fully equivalent to Chrome.

### 3. Existing browser session

Use it only when the user explicitly needs an already-running authenticated browser session and enables existing-session mode.

Remote debugging must remain localhost-only.

## Install in OpenClaw

1. Put the `chrome-devtools-mcp` directory in the OpenClaw skills location used by your agent.
2. Add an OpenClaw MCP server definition from `examples/openclaw.mcp.chrome.isolated.json5` or another mode-specific example.
3. Save and publish the OpenClaw configuration.
4. Run `openclaw mcp reload`.
5. Run `openclaw mcp probe chrome-devtools`.
6. Use the skill only after the server probes successfully.

## UI field mapping

For the default isolated setup, configure the custom MCP server entry as:

```text
Name: chrome-devtools
Enabled: true
Transport: stdio
Command: npx
Args:
  - -y
  - chrome-devtools-mcp@latest
  - --isolated
  - --no-usage-statistics
  - --no-performance-crux
MCP Connect Timeout: 20000 ms
MCP Request Timeout: 120000 ms
MCP Parallel Tool Calls: false
```

Do not leave `Transport` empty. Empty transport is the cause of `missing transport`.

## MCP examples

Standard MCP-client examples:

- `examples/mcp.chrome.isolated.json`
- `examples/mcp.chromium.executable.json`
- `examples/mcp.existing-session.json`
- `examples/mcp.allowed-domain.json`

OpenClaw `mcp.servers` examples:

- `examples/openclaw.mcp.chrome.isolated.json5`
- `examples/openclaw.mcp.chromium.executable.json5`
- `examples/openclaw.mcp.existing-session.json5`
- `examples/openclaw.mcp.allowed-domain.json5`

## Validation

Run:

```bash
python3 scripts/validate_skill.py
```

The validation script checks required files, YAML frontmatter, required metadata fields, required example JSON files, JSON syntax, OpenClaw JSON5 examples, safe defaults, and obviously unsafe instruction strings.

## SkillSpector scan

Run before publishing:

```bash
skillspector scan . --no-llm --format markdown
skillspector scan . --no-llm --format sarif --output skillspector.sarif
```

Publish only if validation passes and SkillSpector has no critical or high findings.
