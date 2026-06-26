# IDE Migration Reference Guide

This document provides comprehensive guidance for migrating AI assistant capabilities, configurations, and settings between different IDE environments.

## Supported IDEs

| IDE | Identifier | Global Path | Project Path |
|-----|------------|-------------|--------------|
| Antigravity | `antigravity` | `~/.gemini/antigravity/` | `.agents/` |
| Claude Code | `claude` | `~/.claude/` | `.claude/` |
| OpenAI Codex | `codex` | `~/.codex/` | `.agents/` |
| VS Code Copilot | `copilot` | `~/.vscode/extensions/` | `.github/copilot-instructions.md` |
| Cursor | `cursor` | `~/.cursor/` | `.cursor/` |
| Windsurf | `windsurf` | `~/.windsurf/` | `.windsurf/` |
| JetBrains IDEs | `jetbrains` | `~/.idea/` | `.idea/` |
| OpenClaw | `openclaw` | `~/.openclaw/` | `<workspace>/skills/` |
| Trae (International) | `trae` | `~/.trae/` | `.trae/` |
| Trae CN (China) | `trae-cn` | `~/.trae-cn/` | `.trae/` |
| VS Code | `vscode` | `~/.vscode/` | `.vscode/` |
| Zed | `zed` | `~/.config/zed/` | `.zed/` |
| Neovim | `neovim` | `~/.config/nvim/` | `.nvim/` |
| Emacs | `emacs` | `~/.emacs.d/` | `.dir-locals.el` |
| Continue.dev | `continue` | `~/.continue/` | `.continue/` |
| Aider | `aider` | `~/.aider/` | `.aider.conf.yml` |
| Roo Code | `roo-code` | `~/.roo/` | `.roo/` |
| Cline | `cline` | `~/.cline/` | `.cline/` |
| Amazon Q Developer | `amazon-q` | `~/.aws/amazon-q/` | `.amazon-q/` |
| Sourcegraph Cody | `cody` | `~/.vscode/extensions/` | `.cody/` |
| Codeium | `codeium` | `~/.vscode/extensions/` | `.codeium/` |
| Tabnine | `tabnine` | `~/.vscode/extensions/` | `.tabnine/` |
| Replit AI | `replit` | `~/.replit/` | `.replit/` |
| PearAI | `pearai` | `~/.pearai/` | `.pearai/` |
| Supermaven | `supermaven` | `~/.supermaven/` | `.supermaven/` |
| Pieces | `pieces` | `~/.pieces/` | `.pieces/` |
| Blackbox AI | `blackbox` | `~/.vscode/extensions/` | `.blackbox/` |

## Handling Unknown IDEs

When encountering an IDE not in the supported list, follow these steps:

### 1. Research Phase

Search for information about the IDE's AI assistant configuration:
- Official documentation website
- GitHub repository (look for issues, wiki, docs)
- Community forums (Reddit, Discord, Stack Overflow)
- Configuration files in user's home directory

### 2. Identify Key Paths

Look for:
- **Global config**: Usually `~/.<ide-name>/` or `~/.config/<ide-name>/`
- **Project config**: Usually `.<ide-name>/` in project root
- **Rules file**: Often `.<ide-name>rules`, `<IDE>RULES.md`, or similar
- **MCP config**: Often `mcp.json`, `config.json`, or integrated in settings

### 3. Common Patterns

| Pattern Type | Common Locations |
|--------------|------------------|
| XDG Base Dir | `~/.config/<app>/`, `~/.local/share/<app>/` |
| Home Dir | `~/.<app>/`, `~/.<app>rc` |
| Project Dir | `.<app>/`, `.<app>rc`, `<app>.json` |
| Rules | `.<app>rules`, `<APP>_RULES.md`, `.instructions.md` |

### 4. Verification

After identifying paths, verify with user:
```
"I found that [IDE] uses:
- Global config: [path]
- Project config: [path]  
- Rules file: [filename]

Is this correct?"
```

## Content Types by IDE

Different IDEs use different names and locations for similar content types. This section maps the terminology and paths.

### Skills / Capabilities

| IDE | Global Path | Project Path | Format |
|-----|-------------|--------------|--------|
| Antigravity | `~/.gemini/antigravity/skills/` | `.agents/skills/` | Directory + SKILL.md |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Directory + SKILL.md |
| OpenAI Codex | `~/.codex/skills/` | `.agents/skills/` | Directory + SKILL.md |
| VS Code Copilot | `~/.copilot-skills/` | `.github/copilot-instructions.md` | Single .md file |
| Cursor | `~/.cursor/` | `.cursor/` | Directory structure |
| Windsurf | `~/.windsurf/` | `.windsurf/` | Directory structure |
| JetBrains | `~/.idea/` | `.idea/` | XML configs |
| OpenClaw | `~/.openclaw/skills/` | `<workspace>/skills/` | Directory + SKILL.md + _meta.json |
| Trae | `~/.trae/skills/` | `./.trae/skills/` | Directory + SKILL.md |
| Trae CN | `~/.trae-cn/skills/` | `./.trae/skills/` | Directory + SKILL.md |
| Continue.dev | `~/.continue/` | `.continue/` | JSON config |
| Aider | `~/.aider/` | `.aider/` | YAML/Markdown |
| Cline | `~/.cline/` | `.cline/` | JSON config |

### Rules / Instructions

| IDE | File Name | Location | Purpose |
|-----|-----------|----------|---------|
| Cursor | `.cursorrules` | Project root | Project-specific rules |
| Windsurf | `.windsurfrules` | Project root | Project-specific rules |
| VS Code Copilot | `.github/copilot-instructions.md` | Project | Project instructions |
| VS Code Copilot | `.github/instructions/` | Project | Instruction files |
| Claude Code | `CLAUDE.md` | Project root | Project context |
| OpenClaw | `AGENT_RULES.md` | Project root | Agent rules |
| Aider | `.aider.conf.yml` | Project root | Configuration |
| Cline | `.clinerules` | Project root | Project rules |
| Continue.dev | `.continuerc.json` | Project root | Configuration |

### Prompts / Templates

| IDE | Path | Location | Purpose |
|-----|------|----------|---------|
| Cursor | `.cursor/prompts/` | Project | Custom prompts |
| Windsurf | `.windsurf/prompts/` | Project | Custom prompts |
| VS Code Copilot | `.github/prompts/` | Project | Prompt templates |
| OpenClaw | `.github/prompts/` | Project | Prompt templates |
| Continue.dev | `.continue/prompts/` | Project | Custom prompts |

### MCP Server Configurations

| IDE | Config Path | Format |
|-----|-------------|--------|
| Trae | `~/.trae/mcps/` | Directory |
| Trae CN | `~/.trae-cn/mcps/` | Directory |
| Claude Code | `~/.claude/mcp.json` | JSON |
| OpenClaw | `~/.openclaw/openclaw.json` | JSON |
| Cursor | `~/.cursor/mcp.json` | JSON |
| Cline | `~/.cline/mcp.json` | JSON |
| Continue.dev | `~/.continue/config.json` | JSON |
| VS Code Copilot | settings.json | JSON |

### IDE Settings / Configurations

| IDE | Config File | Purpose |
|-----|-------------|---------|
| Trae / Trae CN | `~/.trae-cn/argv.json` | Agent arguments |
| OpenClaw | `~/.openclaw/openclaw.json` | Main config |
| Cursor | `~/.cursor/settings.json` | IDE settings |
| Windsurf | `~/.windsurf/settings.json` | IDE settings |
| VS Code | `~/.vscode/settings.json` | IDE settings |
| Zed | `~/.config/zed/settings.json` | IDE settings |
| Neovim | `~/.config/nvim/init.lua` | Editor config |
| Emacs | `~/.emacs.d/init.el` | Editor config |
| Continue.dev | `~/.continue/config.json` | Extension config |
| Aider | `~/.aider/aider.conf.yml` | Tool config |
| Cline | `~/.cline/config.json` | Extension config |

## Migration Matrix

### Skills Migration

| Source → Target | Format Conversion | Notes |
|-----------------|-------------------|-------|
| Any → Copilot | SKILL.md → `<name>.md` | Flatten to single file, update settings.json |
| Copilot → Any | `<name>.md` → SKILL.md | Wrap in skill directory structure |
| Any → OpenClaw | Directory copy | Update openclaw.json entries |
| Any → Trae/Trae-CN | Directory copy | Restart IDE after migration |
| Any → Claude | Directory copy | Restart session |
| Any → Codex | Directory copy | Preserve .system/, add openai.yaml |

### Rules Migration

| Source → Target | File Conversion |
|-----------------|-----------------|
| Cursor → Windsurf | `.cursorrules` → `.windsurfrules` |
| Windsurf → Cursor | `.windsurfrules` → `.cursorrules` |
| Cursor → Copilot | `.cursorrules` → `.github/copilot-instructions.md` |
| Windsurf → Copilot | `.windsurfrules` → `.github/copilot-instructions.md` |
| Copilot → Cursor | `.github/copilot-instructions.md` → `.cursorrules` |
| Copilot → Windsurf | `.github/copilot-instructions.md` → `.windsurfrules` |

## Migration Strategies

### Backup Strategy (Default)

Creates timestamped backups before overwriting:

```
skill-name/ → skill-name.bak.20240101120000/
```

### Overwrite Strategy

Replaces existing files without backup. Use with caution.

### Skip Strategy

Only copies files that don't exist in target. Preserves existing content.

## Post-Migration Steps by IDE

### VS Code Copilot

1. Update `settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": "~/.copilot-skills/skill-name.md" }
  ]
}
```

2. Reload VS Code window

### Cursor

1. Review `.cursorrules` for project-specific rules
2. Check `.cursor/rules/` for additional configurations
3. Restart Cursor IDE

### Windsurf

1. Review `.windsurfrules` for project-specific rules
2. Check `.windsurf/rules/` for additional configurations

### OpenClaw

1. Update `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "skill-name": {
        "path": "skills/skill-name"
      }
    }
  }
}
```

2. Run `openclaw doctor` to verify

### Trae / Trae CN

1. Restart Trae IDE
2. Open Skills Center (技能中心)
3. Verify imported skills

### Claude Code

1. Restart Claude Code session
2. Skills load automatically from `~/.claude/skills/`

### OpenAI Codex

1. Add `agents/openai.yaml` for UI visibility:

```yaml
name: skill-name
description: Skill description
```

2. Preserve `.system/` directory if present

### JetBrains IDEs

1. Review `.idea/` directory
2. Configure AI assistant plugin settings
3. Restart IDE

## Common Migration Scenarios

### Scenario 1: Trae CN → VS Code Copilot

```bash
bash smart-ide-migration.sh \
    --source trae-cn \
    --target copilot \
    --objects skills \
    --dry-run
```

Manual steps:
- Update VS Code settings.json
- Reload VS Code window

### Scenario 2: Cursor → Windsurf

```bash
bash smart-ide-migration.sh \
    --source cursor \
    --target windsurf \
    --objects skills,rules
```

Manual steps:
- Review `.windsurfrules`
- Check `.windsurf/rules/`

### Scenario 3: Multiple IDEs from Antigravity

```bash
# Use sync script for batch migration
bash sync-global-skills.sh --targets claude,codex,copilot,openclaw,trae,trae-cn
```

## Troubleshooting

### Migration Fails

Common causes:

1. **Permission denied**: Check file permissions
2. **Disk full**: Free up disk space
3. **Path too long**: Use shorter paths

### Content Drift

If verification shows content drift:

1. Check source and target files manually
2. Re-run migration with `--strategy overwrite`
3. Verify file encoding (UTF-8)

### Format Incompatibility

Some content types may not have direct equivalents:

1. **MCP configs**: May need manual format conversion
2. **IDE settings**: Different JSON schemas
3. **Rules files**: May need content adjustment

## Best Practices

1. **Always use dry-run first**: Preview changes with `--dry-run`
2. **Use backup strategy**: Default strategy creates backups
3. **Verify after migration**: Check migration report for issues
4. **Test in target IDE**: Verify skills work correctly
5. **Document customizations**: Note any manual adjustments needed

## Script Reference

### smart-ide-migration.sh

```bash
# Basic migration
bash smart-ide-migration.sh \
    --source trae-cn \
    --target claude

# Dry run (preview)
bash smart-ide-migration.sh \
    --source trae-cn \
    --target claude \
    --dry-run

# Specific content types
bash smart-ide-migration.sh \
    --source cursor \
    --target windsurf \
    --objects skills,rules

# With report
bash smart-ide-migration.sh \
    --source trae-cn \
    --target copilot \
    --report ~/migration-report.txt

# Custom workspace
bash smart-ide-migration.sh \
    --source trae-cn \
    --target claude \
    --workspace /path/to/project

# Overwrite strategy
bash smart-ide-migration.sh \
    --source trae-cn \
    --target claude \
    --strategy overwrite
```

### Command Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `--source <ide>` | Source IDE to migrate from | Yes |
| `--target <ide>` | Target IDE to migrate to | Yes |
| `--workspace <dir>` | Project root directory | No (default: current) |
| `--objects <list>` | Content types to migrate | No (auto-detect) |
| `--strategy <mode>` | Migration strategy | No (default: backup) |
| `--report <file>` | Save report to file | No |
| `--dry-run` | Preview without changes | No |

### Content Type Options

| Value | Description |
|-------|-------------|
| `skills` | Skills and capabilities |
| `rules` | Rules and instructions |
| `prompts` | Prompt templates |
| `mcp` | MCP server configurations |
| `config` | IDE configuration files |
| `project` | Project-level configurations |
