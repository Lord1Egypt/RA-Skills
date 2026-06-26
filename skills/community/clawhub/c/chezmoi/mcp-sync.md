# MCP Server Synchronization (MCP Sync)

Maintains an identical MCP server list across multiple apps (Claude, Cursor, Antigravity, UTCP).

## Architecture

```
mcp-servers.json (single source of truth)
       │
       ├──→ ~/.claude.json (mcpServers)
       ├──→ ~/.cursor/mcp.json (mcpServers)
       ├──→ ~/.gemini/antigravity/mcp_config.json (mcpServers)
       └──→ ~/.utcp_config.json (manual_call_templates)
```

## Workflow

### 1. Adding an MCP Server

**Edit the single source:**

```bash
# File location
~/.local/share/chezmoi/.chezmoitemplates/mcp-servers.json
```

**Format:**
```json
{
  "server-name": {
    "transport": "stdio",
    "command": "npx",
    "args": ["-y", "package-name"]
  }
}
```

### 2. Apply

```bash
chezmoi apply
```

**Auto-propagated targets:**
- `~/.claude.json`
- `~/.cursor/mcp.json`
- `~/.gemini/antigravity/mcp_config.json`
- `~/.utcp_config.json`

### 3. Verification

```bash
# Check MCP config in each app
jq '.mcpServers | keys' ~/.claude.json
jq '.mcpServers | keys' ~/.cursor/mcp.json
jq '.manual_call_templates[].name' ~/.utcp_config.json
```

## Conversion Scripts

### mcp-servers.sh

Injects mcpServers object for Claude, Cursor, and Antigravity:

```bash
cat | jq --slurpfile mcp "$MCP_JSON" '.mcpServers = (.mcpServers // {}) * $mcp[0]'
```

### generate-utcp-config.sh

Generates manual_call_templates array for UTCP:

```bash
jq '[to_entries[] | {
  name: .key | gsub("-"; "_"),
  call_template_type: "mcp",
  config: { mcpServers: { (.key): .value } }
}] | sort_by(.name)' "$MCP_JSON"
```

## MCP Configuration Source Distinction

| Source | Location | Target | Purpose |
|--------|----------|--------|---------|
| **Default MCP** | `.chezmoi-lib/executable_mcp-servers.sh` | `~/.claude.json`, `~/.cursor/mcp.json` | Built-in editor default servers like code-mode, context7 |
| **Shared MCP** | `.chezmoitemplates/mcp-servers.json` | Claude, Cursor, Gemini, UTCP | Team-shared / multi-app common servers |

**Deciding where to add configuration:**
- Editor-only default servers → `executable_mcp-servers.sh`
- Servers shared across multiple apps → `mcp-servers.json`

## VSCode Settings Rules

When adding settings to `executable_vscode-settings.sh`:

- **Keep keys in alphabetical order** (c → s → w)
- Current order: `claudeCode.*` → `claudeSessions.*` → `search.*` → `window.*` → `workbench.*`
- `files.exclude` is managed in a separate jq pipeline (order does not matter)

## Per-App Additional Configuration

When app-specific additional servers are needed beyond the default MCP servers:

1. Add configuration in the corresponding app's modify template
2. Keep only common servers in `mcp-servers.json`

**Example (Cursor-only server):**

```bash
# modify_mcp.json.tmpl
#!/bin/bash
cat | jq --slurpfile mcp "$MCP_JSON" '
  .mcpServers = (.mcpServers // {}) * $mcp[0] * {
    "cursor-only-server": { ... }
  }
'
```

## Reverse Migration (UTCP → Global MCP)

Procedure for moving `manual_call_templates` from project/global `.utcp_config.json` to the `mcp-servers.json` single source of truth.

### When to Use

- When you want to use MCP servers registered only in UTCP from Claude/Cursor/Gemini as well
- When "utcp to mcp", "move to global mcp", "chezmoi mcp migration" is mentioned

### Procedure

#### Step 1: Check Target Files

```bash
# Project UTCP config
cat ./.utcp_config.json 2>/dev/null | jq '.manual_call_templates[].name'

# Global UTCP config
cat ~/.utcp_config.json 2>/dev/null | jq '.manual_call_templates[].name'

# Servers already in mcp-servers.json
cat ~/.local/share/chezmoi/.chezmoitemplates/mcp-servers.json | jq 'keys'
```

#### Step 2: Select Migration Targets

Use AskUserQuestion (multiSelect: true) to select which manuals to migrate.

**Auto-filtering exclusions:**
- Items where the same server name (after kebab-case conversion) already exists in `mcp-servers.json`
- Items with `${VAR}` environment variable references are flagged separately (env handling required)

#### Step 3: Convert (manual_call_templates → mcp-servers.json format)

**Reverse transformation** of `generate-utcp-config.sh`:

```bash
# manual_call_template item:
{
  "name": "claude_sessions",
  "call_template_type": "mcp",
  "config": {
    "mcpServers": {
      "claude-sessions": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "claude-sessions-mcp@latest"]
      }
    }
  }
}

# → mcp-servers.json format:
{
  "claude-sessions": {
    "transport": "stdio",
    "command": "npx",
    "args": ["-y", "claude-sessions-mcp@latest"]
  }
}
```

**Conversion rules:**
- Extract the first key-value pair from `config.mcpServers` as-is
- Ignore the `name` field (mcp-servers.json uses kebab-case keys)
- Preserve the `transport` field

**`${VAR}` environment variable handling:**
- `${VAR}` → needs conversion to chezmoi template or actual value
- Check `.utcp.env` / `.utcp.local.env` for values and decide:
  - Managed as chezmoi data → `{{ .var_name }}` template
  - Secret token → embed actual value in chezmoi or maintain separate env

#### Step 4: Add to mcp-servers.json

```bash
# Edit chezmoi source
chezmoi edit --apply ~/.local/share/chezmoi/.chezmoitemplates/mcp-servers.json
# Or edit directly
```

Maintain **alphabetical key ordering** after additions.

#### Step 5: Apply and Verify

```bash
chezmoi apply

# Confirm propagation to each app
jq '.mcpServers | keys' ~/.claude.json
jq '.manual_call_templates[].name' ~/.utcp_config.json
```

#### Step 6: Clean Up Original (Optional)

After migration is complete, use AskUserQuestion to confirm whether to remove migrated items from the project `.utcp_config.json`.

- Global `~/.utcp_config.json` is auto-generated by chezmoi, so manual cleanup is unnecessary
- Project `.utcp_config.json` is manually managed → duplicate items can be removed

## Checklist

- [ ] mcp-servers.json includes transport field
- [ ] Server names use kebab-case
- [ ] All apps verified after chezmoi apply
- [ ] UTCP underscore conversion verified (`server-name` → `server_name`)
