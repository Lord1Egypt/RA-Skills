---
title: "Customization"
source:
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-plugins
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise
category: reference
---

Custom instructions, plugins, MCP servers, and enterprise governance for Copilot CLI.

## Customization Overview

| Feature | Purpose | Location |
|---------|---------|----------|
| **Custom instructions** | Persistent behavior guidance | `AGENTS.md`, `.github/copilot-instructions.md`, `~/.copilot/copilot-instructions.md` |
| **Skills** | Task-specific instructions + scripts | `.github/skills/`, `~/.copilot/skills/` |
| **Hooks** | Shell commands at lifecycle events | `.github/hooks/`, `config.json` |
| **Custom agents** | Specialized personas with own context | `.github/agents/`, `~/.copilot/agents/` |
| **MCP servers** | External tool/data integrations | `~/.copilot/mcp-config.json` |
| **Plugins** | Distributable bundles of all above | `/plugin install` |

**Note:** Plugins can also include **LSP server configurations** (`lsp.json`) for language server integrations.

## Custom Instructions

Persistent context included automatically in every request. All custom instruction files are **combined** (not cascaded by priority). Changes take effect on next prompt.

Use `/instructions` to view and toggle loaded instruction files during a session.

### Instruction Locations

| Location | Scope |
|----------|-------|
| `~/.copilot/copilot-instructions.md` | Global (all sessions) |
| `.github/copilot-instructions.md` | Repository |
| `.github/instructions/**/*.instructions.md` | Repository (path-specific) |
| `AGENTS.md` (git root or cwd) | Repository (primary influence) |

Alternatives: `CLAUDE.md`, `GEMINI.md` (must be at repo root). If both `AGENTS.md` and `.github/copilot-instructions.md` exist, both are used.

`AGENTS.md` in the root directory is treated as **primary instructions** (stronger influence). `AGENTS.md` found in other directories (CWD, `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` paths) are **additional instructions** with less influence.

### Path-Specific Instructions

Require `applyTo` frontmatter glob:

```markdown
---
applyTo: "**/*.ts,**/*.tsx"
---
Use strict TypeScript. Prefer interfaces over types.
```

Optional `excludeAgent: "code-review"` or `"coding-agent"` to restrict which agent reads it.

### Init

`copilot /init` — analyzes project and generates starter `.github/copilot-instructions.md`.

Extra dirs via `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` env var (comma-separated paths).

Disable all: `--no-custom-instructions`.

## Plugins

Installable packages bundling agents, skills, hooks, MCP configs, and LSP configs.

### Install Sources

| Source | Command |
|--------|---------|
| Marketplace | `copilot plugin install PLUGIN@MARKETPLACE` |
| GitHub repo | `copilot plugin install OWNER/REPO` |
| Subdirectory | `copilot plugin install OWNER/REPO:PATH/TO/PLUGIN` |
| Git URL | `copilot plugin install https://gitlab.com/OWNER/REPO.git` |
| Local path | `copilot plugin install ./my-plugin` |

### Plugin Commands

`copilot plugin install SPEC` · `uninstall NAME` · `list` · `update NAME`
`copilot plugin marketplace add|list|browse|remove`

Interactive: `/plugin install`, `/plugin list`, etc.

### plugin.json Manifest

```json
{
  "name": "my-dev-tools",
  "description": "React development utilities",
  "version": "1.2.0",
  "author": { "name": "Jane Doe" },
  "agents": "agents/",
  "skills": "skills/",
  "hooks": "hooks.json",
  "mcpServers": ".mcp.json"
}
```

**Required:** `name` (kebab-case, max 64 chars). All other fields optional.

### Precedence

- **Agents/skills:** first-found wins. Project/personal override plugins.
- **MCP servers:** last-wins. Plugin MCP overrides earlier configs.
- **Built-in tools/agents:** always present, cannot be overridden.

**Default marketplaces:** `copilot-plugins`, `awesome-copilot`. Known: `anthropics/claude-code`, `claudeforge/marketplace`.

## MCP Servers

Model Context Protocol — open standard for connecting LLMs to external tools. GitHub MCP server is built-in.

### Adding a Server

**Interactive:** `/mcp add` — fill form, `Ctrl+S` to save. Available immediately.

**Config file:** Edit `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "local",
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {},
      "tools": ["*"]
    },
    "remote-api": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "headers": { "API_KEY": "..." },
      "tools": ["*"]
    }
  }
}
```

**Types:** `local`/`stdio` (stdin/stdout — `stdio` is standard MCP name, compatible with VS Code/cloud agent), `http` (Streamable HTTP), `sse` (legacy HTTP+SSE, deprecated but supported).

### Management

`/mcp show` · `/mcp add` · `/mcp edit NAME` · `/mcp delete NAME` · `/mcp disable|enable NAME`

### MCP Precedence (last-wins)

`~/.copilot/mcp-config.json` < `.vscode/mcp.json` < plugin configs < `--additional-mcp-config`

## Enterprise Governance

Enterprise owners control via: **Settings > AI controls > Copilot > Copilot Clients**.

### Policies That Apply

- CLI enablement (enterprise/org level)
- Model selection (users see only enterprise-enabled models)
- Custom agents (enterprise-configured agents available in CLI)
- Coding agent (both CLI + coding agent policies needed for `/delegate`)
- Audit logging, seat assignment

### Policies That Do NOT Apply

MCP server policies, IDE-specific policies, content exclusions (file path-based), user-configured model providers (BYOK — configured at user level via env vars, cannot be controlled by enterprise).

### Tool Permission Layers

**Layer 1 — Availability:** `--available-tools` (whitelist) or `--excluded-tools` (blacklist). If both set, available-tools wins.

**Layer 2 — Permissions:** `--allow-tool` (pre-approve) or `--deny-tool` (block). Deny always overrides allow.

**Defaults:** read-only ops auto-allowed; destructive commands, file edits, URLs require approval.

### Responsible Use

- Always review and test generated code before merging
- You are responsible for all commands the CLI executes
- Generated code may contain vulnerabilities if not reviewed
- May favor certain languages/coding styles
