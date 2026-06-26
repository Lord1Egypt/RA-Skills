# Plugin Creation

Guide for authoring Claude Code plugins.

## Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin metadata
├── commands/                 # Slash commands (optional)
│   └── my-command.md
├── agents/                   # Specialized agents (optional)
│   └── my-agent.md
├── skills/                   # Agent Skills (optional)
│   └── my-skill/
│       └── SKILL.md
├── hooks/                    # Event handlers (optional)
├── .mcp.json                 # MCP server config (optional)
└── README.md
```

## plugin.json

```json
{
  "name": "plugin-name",
  "description": "What the plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Author Name",
    "email": "email@example.com"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Lowercase, hyphens only. Must match directory name |
| `description` | string | yes | Plugin functionality description |
| `version` | string | yes | Semver (e.g., "1.0.0") |
| `author.name` | string | no | Author name |
| `author.email` | string | no | Author email |

## Validation Checklist

- [ ] `.claude-plugin/plugin.json` exists
- [ ] `name` matches directory name
- [ ] `version` is valid semver
- [ ] All component files have frontmatter
- [ ] README.md present

## Plugin Locations

| Location | Purpose |
|----------|---------|
| `~/.claude/plugins/my-plugin/` | Personal |
| `.claude/plugins/my-plugin/` | Project-scoped |
