# CJL Skills Collection — Development Guide

This is a personal Claude Code skills repository. Each skill is a self-contained directory installable to `~/.claude/skills/` to extend Claude Code's capabilities.

## Repository Structure

```
cjl-plugin/
├── .claude-plugin/
│   └── plugin.json            # Plugin manifest
├── skills/                    # Skill directories
│   ├── cjl-*/                # Each skill has its own directory
│   │   └── SKILL.md          # Skill definition
│   └── cjl-slides/           # Complex skill with subdirectories
│       ├── SKILL.md
│       └── scripts/
└── README.md                 # English (default)
    README_zh.md              # 简体中文
    README_ja.md              # 日本語
```

## Skill Format

Each `SKILL.md` follows this structure:

```yaml
---
name: skill-name
description: "What this skill does. Use when user says..."
user_invocable: true|false
version: "x.x.x"
---

# Skill content in markdown...
```

## Skill Naming Convention

- All skills prefixed with `cjl-`
- Workflow skills (skill chains) include `-flow` suffix (e.g., `cjl-paper-flow`)
- Commands: `/cjl-{name}`

## Adding a New Skill

1. Create `skills/cjl-{name}/SKILL.md`
2. Add frontmatter with `name`, `description`, `user_invocable`, `version`
3. Write the skill content
4. Update `README.md` skill table
5. Update `plugin.json` version if needed

## Version Policy

- Each skill maintains its own `version` in SKILL.md frontmatter
- Plugin version in `plugin.json` is incremented for releases

## Testing Changes

After modifying a skill:
1. Copy to `~/.claude/skills/`
2. Restart Claude Code to reload skills
3. Test via `/cjl-{name}` or natural language trigger

## Multi-Language README

When adding a new language:
1. Create `README_{lang}.md` with proper frontmatter
2. Add `languages:` block to all README variants
3. Add cross-links between all README files
