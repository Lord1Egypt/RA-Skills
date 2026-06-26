---
name: dotfile
metadata:
  author: es6kr
  version: "0.1.2"
description: Synchronization management with external tools. agents - Windows+WSL ~/.agents share + ~/.claude/plugins split layout [agents.md], chezmoi - dotfile template management [chezmoi.md], knowledge - session knowledge → Serena memory [knowledge.md], mcp - MCP server synchronization [mcp.md], syncthing - chezmoi Syncthing sync and diagnostics [syncthing.md]. Use when "knowledge sync", "chezmoi add", "dotfile management", "syncthing", "MCP server add", "MCP sync", "external sync", "(?d)", ".stignore", "ignored files", "stignore settings", "sync incomplete", "sync status", "DB reset", "stale cache", "syncthing diagnostics", "index reset", "rescan", "encryption consistency", "Failed to verify encryption", "receive-encrypted mismatch", "garbage encryptionPassword", "Antigravity Syncthing", "Gemini Syncthing re-register", "Windows WSL agents layout", "plugins split", "marketplace EACCES". For ClawHub-related tasks → delegate to /clawhub skill.
depends-on:
  - chezmoi
---

# Sync

Manages data synchronization with external tools (Serena, chezmoi, Syncthing, etc.).

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| agents | Windows+WSL multi-agent share layout (~/.agents source of truth + ~/.claude/plugins split) | [agents.md](./agents.md) |
| chezmoi | dotfile chezmoi template management | [chezmoi.md](./chezmoi.md) |
| knowledge | Session knowledge → Serena memory sync | [knowledge.md](./knowledge.md) |
| mcp | MCP server sync (delegated to chezmoi) | [mcp.md](./mcp.md) |
| syncthing | chezmoi source Syncthing sync and diagnostics | [syncthing.md](./syncthing.md) |

## Quick Reference

### Agents Layout (Windows + WSL)

```
"Windows WSL agents layout"  → ~/.agents source of truth, ~/.claude/{skills,rules,agents} symlinks
"plugins split"              → Why ~/.claude/plugins/ is NOT shared
"marketplace EACCES"         → Recovery for plugin marketplace rename collisions
```

**Bootstrap script:** `~/.agents/skills/dotfile/scripts/link-shared-ai-configs.{sh,ps1}`
- Creates symlinks from `~/.agents/{skills,rules,agents}/` into Claude / Codex / Gemini / Antigravity
- Idempotent + auto-backup to `.bak/<name>-<timestamp>`

### Knowledge Sync

```
"knowledge sync"        → Current project session → Serena memory
```

### Chezmoi

```
"chezmoi add"           → Add a dotfile to chezmoi
"dotfile management"    → chezmoi template operations
```

**Configurations managed by chezmoi:**
- `~/.utcp_config.json` - UTCP global config
- `~/.claude.json`, `~/.cursor/mcp.json` - MCP server config
- `~/Library/.../Syncthing/config.xml` - Syncthing default config

**MCP server sharing:**
- Single source: `.chezmoitemplates/mcp-servers.json`
- `chezmoi apply` → Automatically applied to all apps

### MCP

```
"MCP server add"        → Edit mcp-servers.json → chezmoi apply
"MCP sync"              → Apply MCP config to all apps
```

### Syncthing

```
"syncthing setup"       → chezmoi source sync configuration
".stignore"             → Ignore pattern configuration
"sync incomplete"       → Per-folder status/need item diagnostics
"encryption consistency"→ Garbage encryptionPassword diagnosis & API PUT cleanup
"DB reset"              → Stale index reset (delete index-v2)
```

**Auto-generated `.stignore`:**
- `.git`
- `(?d).DS_Store` — Prevents orphaned `.DS_Store` on remote deletion
- `*.bak`
