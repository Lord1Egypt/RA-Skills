---
name: agent-skill-manager
description: >
  Cross-platform skill manager for 11 domestic Chinese AI agent products
  (AutoClaw, Kimi, MiniMax Code, WorkBuddy, Trae, DuMate,
  CodeBuddy, Comate, Qoder). Installs as the `askill` CLI — sync your
  skills to all products with one command. Use when the user wants to
  manage, install, sync, or remove Agent Skills across multiple AI coding
  tools and platforms.
license: MIT
---

# Agent Skill Manager

Cross-platform (macOS / Windows) skill sync for 11 domestic AI agent products.

## Quick Start

```bash
# Install
pip install -e .

# Check status across all products
askill status

# Sync all skills to all products
askill sync

# Install a new skill
askill install https://github.com/user/repo/tree/main/skill-name
askill sync
```

## When to Use

- User wants to install a skill to multiple AI products simultaneously
- User asks "sync skills between products" or "install skill to all agents"
- User wants to check which products have which skills
- User asks to remove a skill from all products

## Commands

| Command | Description |
|---------|-------------|
| `askill status [name]` | Show installation status across all 9 products |
| `askill sync [name]` | Sync skill(s) from central repo to all products |
| `askill list` | List all skills in central repository |
| `askill install <path\|url>` | Install a skill to central repository |
| `askill remove <name>` | Remove a skill from central repo and all products |
| `askill pack <name>` | Package a skill as .zip for DuMate upload |
| `askill products` | List all supported products |
| `askill version` | Show version |

## Supported Products

| Product | Company | Sync Method |
|---------|---------|-------------|
| AutoClaw | — | symlink/junction |
| Kimi | Moonshot AI | symlink/junction |
| MiniMax Code | MiniMax | native |
| WorkBuddy | Tencent | symlink + settings.json |
| Trae | ByteDance | symlink/junction |
| DuMate | Baidu | pack .zip |
| CodeBuddy | Tencent | symlink + settings.json |
| Comate / Wenxin Kuaima | Baidu | symlink/junction |
| Qoder / Tongyi Lingma | Alibaba | symlink/junction |

## Adding New Products

Edit `src/agent_skill_manager/products.py` and add to the `PRODUCTS` list:

```python
{
    "name": "New Product",
    "short": "newprod",
    "macos_path": HOME / ".newproduct" / "skills",
    "windows_path": HOME / ".newproduct" / "skills",
    "sync_method": "symlink",
    "note": "Description",
    "extra_dirs_macos": [],
    "extra_dirs_windows": [],
}
```

## Architecture

All skills live in `~/.agents/skills/` (the emerging universal standard). 
The `askill sync` command creates symlinks (macOS) or junctions (Windows) 
to each product's skill directory.

```
~/.agents/skills/          ← Central Repository
  └── my-skill/
      └── SKILL.md
           │
           ├── junction → ~/.openclaw/skills/my-skill/
           ├── junction → ~/.config/agents/skills/my-skill/
           ├── junction → ~/.workbuddy/skills/my-skill/
           ├── junction → ~/.trae/skills/my-skill/
           ├── junction → ~/.codebuddy/skills/my-skill/
           ├── junction → ~/.comate/skills/my-skill/
           └── junction → ~/.qoderwork/skills/my-skill/
```

For detailed product paths and configuration, see `docs/product-paths.md`.
