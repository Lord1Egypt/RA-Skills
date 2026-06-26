---
name: chezmoi
metadata:
  author: es6kr
  version: "0.1.1"
description: chezmoi dotfile management. apply - interactive diff review per file [apply.md], consolidate - merge duplicate templates [consolidate.md], cross-platform - Windows/macOS compatibility [cross-platform.md], doctor - check required files and copy if missing [doctor.md], mcp-sync - MCP server synchronization [mcp-sync.md]. For commit splitting → commit-splitter. Use when "chezmoi apply", "chezmoi diff", "diff review", "per-file apply", "chezmoi consolidate", "duplicate templates", "MCP sync", "chezmoi Windows", "cross platform", "utcp to mcp", "move to global mcp", "chezmoi mcp migration", "chezmoi doctor", "missing script", "SourceGit".
---

# chezmoi

chezmoi dotfile template management and workflow automation.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| apply | Interactive diff review — per-file AskUserQuestion approval + commit-tidy | [apply.md](./apply.md) |
| consolidate | Detect duplicate modify templates and generate shared scripts | [consolidate.md](./consolidate.md) |
| cross-platform | macOS/Windows compatibility diagnostics and fixes | [cross-platform.md](./cross-platform.md) |
| doctor | Check required files and auto-copy if missing | [doctor.md](./doctor.md) |
| mcp-sync | MCP server configuration synchronization | [mcp-sync.md](./mcp-sync.md) |

## Related Skills

| Feature | Skill |
|---------|-------|
| Commit splitting | `commit-splitter` |

## Quick Reference

### Apply (Interactive Diff Review)

```
"chezmoi apply"             → Per-file diff review + AskUserQuestion approval
"chezmoi diff"              → Show all changes, decide per file
```

### Consolidate (Template Merging)

```
"chezmoi check duplicates"  → Detect templates with identical content
"merge templates"           → Consolidate into shared scripts
```

### Doctor (Environment Validation)

```
"chezmoi doctor"            → Check for required scripts
"missing script"            → Auto-copy scripts to ~/bin/
```

### MCP Sync (MCP Synchronization)

```
"add MCP server"            → Add to mcp-servers.json and apply
"MCP sync"                  → Propagate MCP config to all apps
```

## Directory Structure

```
~/.local/share/chezmoi/
├── .chezmoi-lib/              # Shared scripts
│   ├── executable_vscode-settings.sh
│   ├── executable_vscode-keybindings.sh
│   ├── executable_mcp-servers.sh
│   ├── executable_generate-utcp-config.sh
│   └── executable_sourcegit-preference.sh
├── .chezmoitemplates/         # Shared data
│   └── mcp-servers.json       # MCP server single source of truth
├── .chezmoiignore             # OS-specific path branching
├── modify_*.sh.tmpl           # Per-app modify templates
├── private_Library/           # macOS app settings
│   └── private_Application Support/
└── AppData/                   # Windows app settings
    ├── Roaming/               # %APPDATA%
    └── Local/                 # %LOCALAPPDATA%
```

## Required Validation Before Apply

**Always run `chezmoi diff` to review changes before any `chezmoi apply`.**

```bash
# 1. Preview changes
chezmoi diff

# 2. Apply after user approval
chezmoi apply
```

- Skip apply if diff output is empty
- Show diff results to user and get approval via AskUserQuestion
- See the chezmoi section in `~/.agent/rules/iac.md`
