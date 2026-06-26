---
name: create-mcp-server
description: |
  Create, deploy, and manage MCP (Model Context Protocol) servers using the MCPHero platform via the mcpheroctl CLI. Use this skill when the user wants to build an MCP server, deploy tools that wrap APIs or databases, automate MCP server creation, or connect AI clients (Claude Desktop, Cursor, etc.) to custom tools through MCPHero.
---

# Create MCP Servers with MCPHero

[MCPHero](https://mcphero.app) lets agents **build their own tools**. Instead of burning tokens on API schemas, SQL queries, and output parsing every run, the agent creates a persistent MCP server once and calls it forever. A 50,000-token integration becomes a 50-token tool call.

This skill covers the **mcpheroctl CLI** workflow for building servers end-to-end.

**Production API base URL:** `https://api.mcphero.app/api`

---

## Prerequisites

Before using this skill, the user must have `mcpheroctl` installed and authenticated.

### Install mcpheroctl

```bash
# via Homebrew (macOS/Linux)
brew install arterialist/mcpheroctl/mcpheroctl

# via uv (cross-platform)
uv tool install mcpheroctl
```

### Authenticate

1. Log in to the [MCPHero Dashboard](https://mcphero.app).
2. Go to **Settings** → **Organization** → **Developers**.
3. Click **Create API key** and copy the token.
4. Run:

```bash
mcpheroctl auth login --token <YOUR_ORG_TOKEN>
```

### Verify

```bash
mcpheroctl auth status
```

---

## The Wizard Pipeline

The CLI follows this linear flow. After any async step, poll `wizard state` and check `processing_status == "idle"` before proceeding.

```
1. create-session          → Returns server_id (save it, needed everywhere)
2. conversation (loop)     → Gather requirements; stop when is_ready: true
3. start                   → Transition to tool suggestion (async → poll)
4. list-tools              → Review AI-suggested tools
5. refine-tools (optional) → Iterate on tools until satisfied (async → poll)
6. submit-tools            → Confirm selection (deletes unselected tools)
7. (auto env var suggest)  → Triggered automatically after submit-tools (async → poll)
8. list-env-vars           → Review suggested env vars
9. refine-env-vars (opt.)  → Iterate on env vars (async → poll)
10. submit-env-vars        → Provide actual values (call even if list is empty — backend needs it to transition)
11. set-auth               → Generate bearer token for the server
12. generate-code          → Trigger code generation (async → poll)
13. deploy                 → Deploy to MCPHero runtime → returns server_url + bearer_token
```

**Always call `submit-env-vars`**, even when `list-env-vars` returns `[]`. The backend requires this step to transition to the next state. With no env vars, just call it with no `--var` flags.

---

## State Machine

The `setup_status` field in `wizard state` tells you where you are:

```
gathering_requirements     → User is chatting about requirements
tools_generating           → LLM is generating tool suggestions (async, poll)
tools_selection            → Tools ready for review/selection
env_vars_generating        → LLM is generating env var suggestions (async, poll)
env_vars_setup             → Env vars ready for review/submission
auth_selection             → Ready for auth setup
code_generating            → LLM is generating code (async, poll)
code_gen                   → Code ready for review
deployment_selection       → Ready to deploy
ready                      → Server deployed and live
```

States ending in `_generating` are transient — poll until they transition. The `processing_status` field is the reliable check: `"idle"` means done, `"processing"` means wait, `"error"` means check `processing_error`.

---

## Full Wizard Example

Always use `--json` for scriptable output. Without it, human-friendly messages go to stderr and can confuse parsing.

```bash
# 1. Create session
mcpheroctl wizard create-session --json
# → {"server_id": "abc-123-..."}
SERVER_ID="abc-123-..."

# 2. Describe requirements (iterate until is_ready: true)
mcpheroctl wizard conversation $SERVER_ID --json \
  -m "I have a PostgreSQL database with customers and orders tables. I need tools to find customers by name, fetch orders for a customer, and get last hour's orders."
# Repeat with follow-up messages until output shows: "is_ready": true

# 3. Start tool suggestion (async)
mcpheroctl wizard start $SERVER_ID --json
# → {"status": "processing"}

# Poll until processing is done (check processing_status, not setup_status)
until mcpheroctl wizard state $SERVER_ID --json 2>/dev/null | \
  python3 -c "import sys,json; exit(0 if json.load(sys.stdin).get('processing_status')=='idle' else 1)"; do
  sleep 3
done

# 4. Review tools (state should be "tools_selection")
mcpheroctl wizard list-tools $SERVER_ID --json

# 5. Refine if needed (async → poll again)
mcpheroctl wizard refine-tools $SERVER_ID --json \
  -f "Add error handling for missing customers. Rename get_customers_orders to get_orders_by_customer."

# 6. Submit selected tool IDs
mcpheroctl wizard submit-tools $SERVER_ID --json \
  --tool-id <tool-uuid-1> \
  --tool-id <tool-uuid-2> \
  --tool-id <tool-uuid-3>

# 7. Wait for env var suggestion (auto-triggered, state becomes "env_vars_setup")
until mcpheroctl wizard state $SERVER_ID --json 2>/dev/null | \
  python3 -c "import sys,json; exit(0 if json.load(sys.stdin).get('processing_status')=='idle' else 1)"; do
  sleep 3
done

# 8. Review env vars
mcpheroctl wizard list-env-vars $SERVER_ID --json

# 9. Submit env var values (format: VAR_UUID=VALUE)
# ALWAYS call this even if list-env-vars returned [] — backend needs it to transition.
# With env vars:
mcpheroctl wizard submit-env-vars $SERVER_ID --json \
  --var "<env-var-uuid-1>=localhost" \
  --var "<env-var-uuid-2>=5432"
# Without env vars (empty list):
mcpheroctl wizard submit-env-vars $SERVER_ID --json

# 10. Set authentication
mcpheroctl wizard set-auth $SERVER_ID --json
# → {"bearer_token": "..."}  ← SAVE THIS

# 11. Generate code (async → poll)
mcpheroctl wizard generate-code $SERVER_ID --json
until mcpheroctl wizard state $SERVER_ID --json 2>/dev/null | \
  python3 -c "import sys,json; exit(0 if json.load(sys.stdin).get('processing_status')=='idle' else 1)"; do
  sleep 3
done

# 12. Deploy
mcpheroctl wizard deploy $SERVER_ID --json
# → {"server_url": "/mcp/<server-id>/mcp", "bearer_token": "...", "step": "complete"}
```

**IMPORTANT: `deploy` returns a relative `server_url`** like `/mcp/<id>/mcp`. Prepend the base domain to get the full URL:
```
https://api.mcphero.app/mcp/<server-id>/mcp
```

---

## Server Management

```bash
mcpheroctl server list --json [CUSTOMER_ID]  # List all servers
mcpheroctl server get SERVER_ID --json       # Get server details + status
mcpheroctl server update SERVER_ID           # Update name/description
mcpheroctl server delete SERVER_ID --yes     # Delete (irreversible)
mcpheroctl server api-key SERVER_ID --json   # Retrieve bearer token
```

---

## Polling Pattern

The reliable way to poll is to check `processing_status`, not `setup_status`:

```bash
until mcpheroctl wizard state $SERVER_ID --json 2>/dev/null | \
  python3 -c "import sys,json; exit(0 if json.load(sys.stdin).get('processing_status')=='idle' else 1)"; do
  sleep 3
done
```

---

## Connecting a Deployed Server to MCP Clients

After `deploy`, construct the full server URL:
```
https://api.mcphero.app{server_url}
```

### Claude Desktop config

```json
{
  "mcpServers": {
    "my-server": {
      "url": "https://api.mcphero.app/mcp/<server-id>/mcp",
      "headers": {
        "Authorization": "Bearer <bearer_token>"
      }
    }
  }
}
```

Config file locations:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/claude/claude_desktop_config.json`

---

## Key Tips

**Free tier**: Max 5 tools per server. `wizard_submit_tools` will error if more are selected.

**server_id is everything**: Save the UUID returned from `create_session`. Every subsequent call needs it.

**Env var format in CLI**: `--var "UUID=VALUE"` — the UUID is the env var's `id` from `list-env-vars`, not its name.

**Empty env vars**: Even if `list-env-vars` returns `[]`, you must still call `submit-env-vars` (with no vars) so the backend transitions to the next state.

**Regenerate without redeploy**: After using `wizard_regenerate_tool_code`, the code change takes effect immediately for already-deployed servers (the server auto-remounts).

**Always use `--json`**: In CLI commands, `--json` sends structured data to stdout. Without it, human-friendly messages go to stderr and can break piping/parsing.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General failure |
| 2 | Usage/argument error |
| 3 | Resource not found |
| 4 | Not authenticated |
| 5 | Conflict |
