# chezmoi Template Management

> **Detailed guide**: See [chezmoi skill](../chezmoi/SKILL.md)

Converts dotfiles into chezmoi modify templates and sets permissions correctly.

## chezmoi Directories

- Source: `~/.local/share/chezmoi/`
- Target: `~/` (home directory)

## Quick Reference

| Task | Trigger | Skill |
|------|---------|-------|
| Template consolidation | "chezmoi dedup check" | `chezmoi:consolidate` |
| MCP sync | "MCP server add" | `chezmoi:mcp-sync` |
| Commit splitting | "commit split" | `commit-splitter` |

## Template Creation Basics

### private_ Prefix Rules

| Original Permission | chezmoi Prefix |
|---------------------|----------------|
| `drwx------` (700) | `private_` |
| `drwxr-xr-x` (755) | None |
| `-rw-------` (600) | `private_` |
| `-rw-r--r--` (644) | None |

### modify Template Basic Format

```bash
#!/bin/bash
cat | jq --argjson data '{"key": "value"}' '. * $data'
```

## MCP Server Sharing

**Single source:** `.chezmoitemplates/mcp-servers.json`

**How to apply:**
```bash
chezmoi apply  # Automatically applied to all apps
```

**Related apps:**
- `~/.claude.json`
- `~/.cursor/mcp.json`
- `~/.gemini/antigravity/mcp_config.json`
- `~/.utcp_config.json`
