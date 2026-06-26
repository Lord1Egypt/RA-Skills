# Plugins Reference

A plugin is a self-contained directory extending Claude Code with skills, agents, hooks, MCP servers, and LSP servers.

## Plugin Components

### Skills
- Location: `skills/` or `commands/` directory in plugin root
- Skills are directories with `SKILL.md`; commands are simple markdown files
- Auto-discovered on install; Claude can invoke automatically

### Agents
- Location: `agents/` directory
- Frontmatter: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`
- **Security restriction**: `hooks`, `mcpServers`, `permissionMode` not supported in plugin agents

### Hooks
- Location: `hooks/hooks.json` or inline in `plugin.json`
- Same lifecycle events as user-defined hooks
- Types: `command`, `http`, `prompt`, `agent`

### MCP Servers
- Location: `.mcp.json` in plugin root or inline in `plugin.json`
- Use `${CLAUDE_PLUGIN_ROOT}` for paths

### LSP Servers
- Provide code intelligence (definitions, references, diagnostics)
- Install language server binary separately

## Installation Scopes

| Scope | Who sees it |
|-------|------------|
| User | All your projects |
| Project | Everyone working on the project |

## Plugin Manifest (`plugin.json`)

Required fields: `name`, `version`, `description`

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What my plugin does",
  "skills": "skills/",
  "agents": "agents/",
  "hooks": { ... },
  "mcpServers": { ... }
}
```

## Directory Structure

```
my-plugin/
├── plugin.json          # Manifest
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── agents/
│   └── my-agent.md
├── hooks/
│   └── hooks.json
├── servers/
│   └── mcp-server.js
└── scripts/
    └── format-code.sh
```

## CLI Commands

| Command | Purpose |
|---------|---------|
| `claude plugin install <name>@<marketplace>` | Install plugin |
| `claude plugin uninstall <name>` | Remove plugin |
| `claude plugin enable <name>` | Enable disabled plugin |
| `claude plugin disable <name>` | Disable without removing |
| `claude plugin update [name]` | Update plugin(s) |

## Environment Variables

- `CLAUDE_PLUGIN_ROOT` — absolute path to the plugin's cached directory
- `CLAUDE_PLUGIN_DATA_DIR` — persistent writable data directory

## Debugging

- `/plugin` in session to manage
- `/reload-plugins` to reload without restart
- Check `~/.claude/plugins/` for cached files
- Use `--debug` for detailed logs
