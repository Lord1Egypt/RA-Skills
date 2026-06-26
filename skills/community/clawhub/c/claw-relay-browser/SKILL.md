---
name: claw-relay-openclaw
description: Control a remote browser through Claw Relay using the CLI client. Use when you need to navigate authenticated websites, click buttons, fill forms, take screenshots, or read page content on a user's real browser — and your platform doesn't support MCP. Triggers on remote browser control, authenticated browsing, real browser, cookie-based access, browser relay.
---

# Claw Relay — OpenClaw CLI Client

> **If your platform supports MCP (Copilot CLI, Claude Desktop, Gemini CLI), use `skills/browser/SKILL.md` instead.** This skill is for OpenClaw, nanobot, ZeroClaw, and other agents that call tools via `exec`.

## ⚠️ IMPORTANT: No MCP Required

**Do NOT write an MCP server, bridge, or wrapper.** You already have everything you need:
- The `exec` tool (built into OpenClaw)
- The `relay-client.cjs` script (in this folder)

That's it. One `exec` call per browser action. No MCP, no bridge, no custom server.

## Setup

Set environment variables (or pass as flags):

```bash
export CLAW_RELAY_URL="wss://relay.clawrelay.dev/"
export CLAW_RELAY_TOKEN="your-token"
export CLAW_RELAY_AGENT="your-agent-id"
```

The client script is at `skills/openclaw/relay-client.cjs` in the claw-relay repo.

## Usage

```bash
node relay-client.cjs [--url URL] [--token TOKEN] [--agent-id ID] ACTION [ARGS...]
```

Flags override env vars. Every invocation connects, authenticates, performs ONE action, prints JSON, and exits.

## Actions

| Action | Args | Description |
|--------|------|-------------|
| `navigate` | `<url>` | Navigate to URL |
| `snapshot` | — | Get accessibility tree with element refs |
| `screenshot` | `[filepath]` | Take screenshot; saves to filepath if given |
| `click` | `<ref>` | Click element by ref |
| `fill` | `<ref> <text>` | Replace input content with text |
| `type` | `<ref> <text>` | Append text to input |
| `press` | `<key>` | Press keyboard key (Enter, Tab, Escape, etc.) |
| `hover` | `<ref>` | Hover over element |
| `select` | `<ref> <values...>` | Select dropdown option(s) |
| `evaluate` | `<js>` | Run JavaScript in the page |
| `close` | — | Close the browser tab |

## Workflow

```
navigate → snapshot → find ref → act → snapshot → verify
```

1. **Navigate** to the target URL
2. **Snapshot** to read the page and get element refs (e.g. `e3`, `e7`)
3. **Act** — click, fill, type, press using refs from the snapshot
4. **Verify** — snapshot again to confirm the page changed

### Example: Search GitHub

```bash
# Step 1: Navigate
node relay-client.cjs navigate https://github.com

# Step 2: Snapshot to find the search input ref
node relay-client.cjs snapshot

# Step 3: Fill the search box (say ref is e3)
node relay-client.cjs fill e3 claw-relay

# Step 4: Press Enter
node relay-client.cjs press Enter

# Step 5: Snapshot to read results
node relay-client.cjs snapshot
```

### Example: Click a Button

```bash
# Find the button
node relay-client.cjs snapshot
# Output shows button at ref e7

# Click it
node relay-client.cjs click e7

# Verify
node relay-client.cjs snapshot
```

### Example: Take a Screenshot

```bash
node relay-client.cjs screenshot /tmp/page.png
# Output: {"ok":true,"path":"/tmp/page.png","bytes":...}
```

### Example: Run JavaScript

```bash
node relay-client.cjs evaluate "document.title"
```

## OpenClaw exec Integration

Use the `exec` tool directly. Each call connects, authenticates, performs one action, and exits:

```bash
exec: node /path/to/relay-client.cjs snapshot
exec: node /path/to/relay-client.cjs navigate https://github.com
exec: node /path/to/relay-client.cjs click e3
```

Set `CLAW_RELAY_URL`, `CLAW_RELAY_TOKEN`, and `CLAW_RELAY_AGENT` in your environment or pass them as flags each time.

**Do NOT try to keep a persistent connection, start a background process, or write wrapper scripts.** The CLI handles connection lifecycle automatically.

## Security Constraints

- **Allowlist** — your agent can only access sites explicitly allowed in its config
- **Blocklist** — banking, email, and auth providers are always blocked regardless of allowlist
- **Rate limiting** — actions are rate-limited per agent
- **Audit log** — every action is logged with agent ID, action, target, and result

## Troubleshooting

### "Invalid token or agent_id"
- Agent ID is **case-sensitive**. Check `config.yaml` for exact casing (e.g., `Rusty` ≠ `rusty`)
- Make sure the token matches exactly — no extra spaces or line breaks
- The relay must be restarted after editing `config.yaml`

### "Agent lacks scope for 'navigate'"
- Your agent's `scopes` in `config.yaml` don't include the action you're trying to use
- Common scopes: `read` (snapshot/screenshot), `navigate`, `interact` (click/fill/type), `execute` (evaluate)
- Ask the relay admin to update your scopes

### Script errors
- **"require is not defined"** — the script must be `.cjs`, not `.js` (the repo uses ES modules)
- **"Cannot find module 'ws'"** — run `npm install` in the `relay-server/` directory first

### Common mistakes
- ❌ Writing an MCP server or bridge — you don't need one
- ❌ Keeping a persistent connection — each call is stateless
- ❌ Wrapping the CLI in another script — just call it directly via `exec`

## What Makes This Different

Local browser tools require agent and browser on the same machine. Claw Relay doesn't. Your agent runs anywhere and controls the user's real browser remotely — real cookies, real sessions, real logins. No headless browser, no fake profiles.
