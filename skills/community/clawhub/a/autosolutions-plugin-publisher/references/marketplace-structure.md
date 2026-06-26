# Anthropic Marketplace Structure — Complete Reference

This document encodes the exact directory layout, file formats, and conventions used by
Anthropic's official `knowledge-work-plugins` marketplace. Every marketplace plugin you
create must follow this structure to install correctly in Cowork and Claude Code.

## How Cowork Discovers and Installs Plugins

1. **Marketplace registration**: User runs `/plugin marketplace add owner/repo`.
   Cowork clones the repo and reads `.claude-plugin/marketplace.json`.
2. **Plugin discovery**: Each entry in `marketplace.json` has a `source` field pointing
   to a plugin directory relative to the repo root.
3. **Plugin installation**: Cowork reads the plugin's `.claude-plugin/plugin.json`,
   copies the plugin directory to its local cache, and registers skills/commands/agents.
4. **Persistence**: Installed plugins persist across sessions via `installed_plugins.json`
   on the user's machine.

## Directory Layout

```
marketplace-repo/
├── .claude-plugin/
│   └── marketplace.json            ← REQUIRED: catalog of all plugins
├── plugin-a/                       ← Plugin directory at ROOT level
│   ├── .claude-plugin/
│   │   └── plugin.json             ← REQUIRED: plugin manifest
│   ├── skills/                     ← Auto-triggered knowledge
│   │   └── skill-name/
│   │       ├── SKILL.md            ← Required per skill
│   │       └── references/         ← Optional deep-dive docs
│   ├── commands/                   ← User-invoked slash commands
│   │   └── command-name.md
│   ├── agents/                     ← Subagent definitions
│   │   └── agent-name.md
│   ├── hooks/                      ← Event-driven automation
│   │   └── hooks.json
│   ├── .mcp.json                   ← MCP server connections
│   ├── CONNECTORS.md               ← Tool-agnostic placeholders
│   └── README.md                   ← Plugin documentation
├── plugin-b/                       ← Another plugin (same level)
│   └── ...
├── openclaw-install.sh             ← OpenClaw deployment script
├── LICENSE
└── README.md                       ← Marketplace-level docs
```

### Critical: Plugin Directories at Root Level

**CORRECT:**
```
repo/
├── .claude-plugin/marketplace.json  →  source: "./my-plugin"
├── my-plugin/
│   └── .claude-plugin/plugin.json
```

**WRONG:**
```
repo/
├── .claude-plugin/marketplace.json  →  source: "./plugins/my-plugin"
├── plugins/
│   └── my-plugin/
│       └── .claude-plugin/plugin.json
```

This is the #1 mistake when creating marketplace plugins. Anthropic's own marketplace
puts every plugin at the repo root (`./operations`, `./productivity`, `./sales`), and the
install system expects this convention.

## marketplace.json — Full Schema

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Organization Name",
    "email": "contact@example.com"
  },
  "metadata": {
    "description": "What this marketplace offers",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugin-name",
      "description": "One-paragraph description of what the plugin does",
      "version": "1.0.0",
      "author": {
        "name": "Author Name"
      },
      "homepage": "https://github.com/owner/repo",
      "repository": "https://github.com/owner/repo",
      "license": "MIT",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "category": "research-analysis",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

### Field Reference

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Marketplace identifier, kebab-case |
| `owner.name` | Yes | Organization or person |
| `owner.email` | No | Contact email |
| `metadata.description` | No | Marketplace-level description |
| `metadata.version` | No | Marketplace version |
| `plugins[].name` | Yes | Must match the plugin directory name |
| `plugins[].source` | Yes | Relative path from repo root: `"./plugin-name"` |
| `plugins[].description` | Yes | Shown in search results |
| `plugins[].version` | Yes | Semver |
| `plugins[].author.name` | No | Plugin-level author |
| `plugins[].homepage` | No | URL |
| `plugins[].repository` | No | GitHub URL |
| `plugins[].license` | No | SPDX identifier |
| `plugins[].keywords` | No | Array of strings for search |
| `plugins[].category` | No | Primary category |
| `plugins[].tags` | No | Additional tags |

### Multiple Plugins in One Marketplace

A marketplace can contain many plugins. Each gets its own root-level directory and
its own entry in the `plugins` array:

```json
{
  "plugins": [
    { "name": "plugin-a", "source": "./plugin-a", ... },
    { "name": "plugin-b", "source": "./plugin-b", ... }
  ]
}
```

## plugin.json — Full Schema

Located at `plugin-name/.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": {
    "name": "Author Name",
    "url": "https://example.com"
  },
  "homepage": "https://github.com/owner/repo",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

Only `name` is strictly required. Everything else is recommended.

Optional component path overrides:
```json
{
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

## Component Schemas (Summary)

### Skills
- Location: `skills/skill-name/SKILL.md`
- Frontmatter: `name` (required), `description` (required), `version` (optional)
- Description: third-person with trigger phrases in quotes
- Body: imperative instructions, under 3,000 words
- Use `references/` subdirectory for detailed content

### Commands
- Location: `commands/command-name.md`
- Frontmatter: `description`, `allowed-tools`, `model`, `argument-hint` (all optional)
- Body: directives FOR Claude (not documentation for users)
- `$ARGUMENTS` = all args; `$1`, `$2` = positional; `@path` = file inclusion

### Agents
- Location: `agents/agent-name.md`
- Frontmatter: `name` (required), `description` (required), `model` (required),
  `allowed-tools` or `tools` (optional)
- Description should include `<example>` blocks showing trigger conditions
- Body: system prompt for the subagent

### MCP Servers
- Location: `.mcp.json` at plugin root
- Types: stdio (local), sse (remote SSE), http (remote HTTP)
- Use `${CLAUDE_PLUGIN_ROOT}` for paths, `${ENV_VAR}` for secrets

### Hooks
- Location: `hooks/hooks.json`
- Events: PreToolUse, PostToolUse, Stop, SessionStart, etc.
- Types: prompt-based (LLM-driven) or command-based (deterministic)

## Install Commands Reference

```bash
# Register a marketplace
/plugin marketplace add owner/repo-name

# Install a plugin from a registered marketplace
/plugin install plugin-name@marketplace-name

# Install from local clone (development)
claude /plugin marketplace add ./
claude /plugin install plugin-name@marketplace-name
```

## Naming Conventions

- Marketplace name: kebab-case (e.g., `autosolutions-plugins`)
- Plugin name: kebab-case (e.g., `npd-validator`)
- Skill directories: kebab-case (e.g., `validate-product`)
- Command files: kebab-case (e.g., `run-analysis.md`)
- Agent files: kebab-case (e.g., `npd-market-demand.md`)
- All lowercase, hyphens only, no spaces or special characters

## Real-World Example: Anthropic's Marketplace

Anthropic's `knowledge-work-plugins` marketplace contains plugins like:
- `operations/` — vendor management, process docs, compliance tracking
- `productivity/` — task management, memory, calendar sync
- `engineering/` — standups, code review, incident response
- `sales/` — pipeline management, outreach, deal strategy

Each follows exactly the structure documented above. The `marketplace.json` at
`.claude-plugin/marketplace.json` lists all plugins with `source: "./plugin-name"`.
