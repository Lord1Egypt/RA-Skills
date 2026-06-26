# MCP Server Synchronization

Maintains the same MCP server list across multiple apps (Claude, Cursor, Antigravity, UTCP).

> Detailed implementation: See [chezmoi/mcp-sync.md](../chezmoi/mcp-sync.md)

## Quick Reference

| Task | Command |
|------|---------|
| Add MCP server | Edit `mcp-servers.json` → `chezmoi apply` |
| Reverse migration | Move from UTCP manual → `mcp-servers.json` single source |
| Verify application | `jq '.mcpServers \| keys' ~/.claude.json` |

## Single Source

```
~/.local/share/chezmoi/.chezmoitemplates/mcp-servers.json
```

After editing, `chezmoi apply` → Automatically applied to all apps:
- `~/.claude.json` (mcpServers)
- `~/.cursor/mcp.json` (mcpServers)
- `~/.gemini/antigravity/mcp_config.json` (mcpServers)
- `~/.utcp_config.json` (manual_call_templates)

## Triggers

- "MCP server add", "MCP sync"
- "utcp to mcp", "move to global mcp"
- "chezmoi mcp migration"
