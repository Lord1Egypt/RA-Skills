---
name: clear-skills
description: >
  This skill should be used when the user wants to clear, remove, or clean up AI agent rules,
  skills, or instruction files from their coding environment. It supports one-click cleanup
  of rule/instruction files for all major AI coding platforms on Windows, macOS, and Linux,
  including Cursor, Windsurf, Claude Code, Codex CLI, GitHub Copilot, Gemini CLI, Cline,
  Trae IDE, Amazon Q, Continue.dev, Aider, OpenCode, Amp, Goose, Kilo Code, Kiro,
  Neovate, OpenHands, PI, Qoder, Roo Code, Zencoder, Droid, OpenClaw, QClaw,
  CoPaw, EasyClaw, ArkClaw, LobsterAI, HiClaw, AutoClaw, AntiClaw, Manus,
  HappyCapy, QoderWork, and WorkBuddy/CodeBuddy. Triggers on phrases like "清除agent技能",
  "删除规则文件", "清空所有AI规则", "clear agent rules", "remove AI skills", "一键清除技能".
---

# Clear Skills Skill

## Overview

Scans and removes AI agent rules/skills files from all major AI coding platforms on your machine. Supports **50+ platforms**, covering both **project-level** and **user-global** scopes, running on **Windows · macOS · Linux**.

**Core Features:**
- ✅ **Smart Scanning**: Only removes files/directories that actually exist. Platforms not installed or without rules won't be shown or removed
- ✅ **Self-Protection**: By default, this skill (clear-skills) is protected and won't be cleared, allowing safe cleanup of other platforms
- ✅ **Auto Backup**: Automatically backs up to desktop before deletion, allowing recovery anytime
- ✅ **Preview Mode**: Use `--dry-run` to confirm which files will be deleted before actually removing them
- ✅ **Flexible Control**: Supports filtering by platform, scope, project directory, and more
- ✅ **Pure Python**: Uses only Python 3 standard library, no external dependencies required

**All Supported Platforms:**

### Mainstream AI IDE
Cursor · Windsurf(Codeium) · Cline · Trae IDE · Amazon Q · Continue.dev

### Agent Framework / CLI
Claude Code · Codex CLI · GitHub Copilot · Gemini CLI · Aider · OpenCode

### Emerging AI Tools
Amp · Goose · Kilo Code · Kiro (AWS) · Neovate · OpenHands · PI · Qoder · Roo Code · Zencoder

### OpenClaw Ecosystem
OpenClaw · QClaw · CoPaw · EasyClaw · ArkClaw · LobsterAI · HiClaw · AutoClaw · AntiClaw

### Other AI Agents
Manus · HappyCapy · QoderWork · Droid (Factory)

### WorkBuddy
WorkBuddy / CodeBuddy

---

## Usage

### Step 1: Confirm User Intent

After receiving a cleanup request, confirm the following with the user (skip if already specified):

1. **Cleanup Scope**: Current project only (`project`), global only (`global`), or both (`all`, default)?
2. **Platform Scope**: All platforms, or specific platforms only?
3. **Backup**: Back up to desktop by default. Users can disable with `--no-backup` (not recommended).

### Step 2: Execute Script

Call `scripts/clear_agent_rules.py`. This script uses **pure Python 3 standard library only**, no additional dependencies needed.

**Quick Start Examples**

```bash
# Preview mode (recommended to see what will be deleted first)
python scripts/clear_agent_rules.py --dry-run

# Clear current project + global, all platforms, auto backup (default behavior)
# Note: This skill is protected by default and won't be cleared
python scripts/clear_agent_rules.py
```

# Clear only specified platforms
python scripts/clear_agent_rules.py --platforms cursor,claude,copilot

# Clear only OpenClaw ecosystem (including QClaw, CoPaw, etc.)
python scripts/clear_agent_rules.py --platforms openclaw,qclaw,copaw

# Clear only QoderWork skills
python scripts/clear_agent_rules.py --platforms qoderwork

# Clear only current project rules
python scripts/clear_agent_rules.py --mode project

# Clear only global rules
python scripts/clear_agent_rules.py --mode global

# Specify project directory
python scripts/clear_agent_rules.py --project /path/to/myproject

# No backup (dangerous, use with caution)
python scripts/clear_agent_rules.py --no-backup

# Non-interactive execution (skip YES confirmation, suitable for scripts/CI)
python scripts/clear_agent_rules.py --yes

# Clear all WorkBuddy skills including this one (dangerous)
python scripts/clear_agent_rules.py --mode global --include-self
```

### Advanced Usage

```bash
# Clear only AI IDE platforms (Cursor, Windsurf, Cline, etc.)
python scripts/clear_agent_rules.py --platforms cursor,windsurf,cline,trae,amazonq,continue

# Clear only CLI tools (Claude Code, Copilot, Aider, etc.)
python scripts/clear_agent_rules.py --platforms claude,copilot,aider,gemini,codex

# Clear only project-level rules for specific platforms
python scripts/clear_agent_rules.py --mode project --platforms cursor,copilot

# Scan specific project directory
python scripts/clear_agent_rules.py --project /path/to/specific/project

# Export scan results without deleting (for manual review)
python scripts/clear_agent_rules.py --dry-run > scan_results.txt
```

> **Note**: On Windows, `python` command might be `python3` or `py`, depending on your environment.

#### Parameter Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--mode` | `project` / `global` / `all` | `all` |
| `--project` | Project root directory path | Current working directory |
| `--platforms` | Specify platforms (comma-separated) | `all` |
| `--no-backup` | Disable backup | Disabled (backup by default) |
| `--dry-run` | Preview mode, don't actually delete | Disabled |
| `--yes` | Skip YES confirmation prompt | Disabled |
| `--include-self` | Don't protect this skill, will also clear clear-skills itself | Disabled (protected by default) |

**Available Platform Identifiers:**
```
cursor, windsurf, cline, trae, amazonq, continue,
claude, codex, copilot, gemini, aider, opencode,
amp, goose, kilocode, kiro, neovate, openhands, pi, qoder,
roocode, zencoder, droid,
openclaw, qclaw, copaw, easyclaw, arkclaw, lobsterai,
hiclaw, autoclaw, anticlaw, manus, happycapy,
qoderwork,
workbuddy
```

---

## Platform Rule File Reference

For detailed paths, see `references/platforms.md`.

### Project-Level Rules (relative to project root)

| Category | Platform | Main Files/Directories |
|----------|----------|----------------------|
| **AI IDE** | Cursor | `.cursorrules`, `.cursor/rules/` |
| | Windsurf | `.windsurfrules`, `.windsurf/rules/` |
| | Cline | `.clinerules`, `.clinerules/` |
| | Trae IDE | `.trae/project_rules.md` |
| | Amazon Q | `.amazonq/rules/` |
| | Continue.dev | `.continuerc.json`, `.continue/rules/` |
| **CLI** | Claude Code | `CLAUDE.md` |
| | Codex CLI | `AGENTS.md` |
| | GitHub Copilot | `.github/copilot-instructions.md` |
| | Gemini CLI | `GEMINI.md` |
| | Aider | `.aider.conf.yml` |
| | OpenCode | `AGENTS.md`, `CLAUDE.md` |
| **Emerging Tools** | Amp | `AGENTS.md` |
| | Goose | `.goosehints`, `.goose/` |
| | Kilo Code | `.kilocode/rules/` |
| | Kiro (AWS) | `.kiro/steering/`, `.kiro/` |
| | Neovate | `AGENTS.md` |
| | OpenHands | `config.toml`, `.openhands/` |
| | PI | `.pi/settings.json`, `.pi/` |
| | Qoder | `.qoder/rules/` |
| | Roo Code | `.roo/rules/`, `.roorules` |
| | Zencoder | `.zencoder/rules/` |
| | Droid (Factory) | `.droid/`, `AGENTS.md` |
| **Others** | Antigravity | `.antigravity/rules.md` |
| | OpenClaw | `.openclaw/` |
| | QoderWork | `.qoderwork/skills/` |
| | WorkBuddy | `.workbuddy/skills/` |

### Global-Level Rules (user home directory)

| Category | Platform | Path |
|----------|----------|------|
| **AI IDE** | Cursor | `~/.cursor/rules/` |
| | Cline | `~/Documents/Cline/Rules/` |
| | Trae IDE | `~/.trae/user_rules.md` |
| | Continue.dev | `~/.continue/` |
| **CLI** | Claude Code | `~/.claude/` |
| | Gemini CLI | `~/.gemini/GEMINI.md` |
| | Aider | `~/.aider.conf.yml` |
| | OpenCode | `~/.config/opencode/` |
| **Emerging Tools** | Amp | `~/.factory/AGENTS.md` |
| | Goose | `~/.config/goose/` |
| | Kilo Code | `~/.kilocode/rules/` |
| | Kiro (AWS) | `~/.kiro/` |
| | Neovate | `~/.neovate/AGENTS.md` |
| | OpenHands | `~/.openhands/` |
| | PI | `~/.pi/agent/settings.json` |
| | Roo Code | `~/.roo/rules/` |
| | Droid (Factory) | `~/.factory/` |
| **OpenClaw Ecosystem** | OpenClaw/QClaw etc. | `~/.openclaw/` |
| | CoPaw | `~/.copaw/` |
| **Others** | Manus | `~/.manus/` |
| | HappyCapy | `~/.happycapy/` |
| | QoderWork | `~/.qoderwork/skills/` |
| | WorkBuddy | `~/.workbuddy/skills/` |
| **Note** | Qoder/Zencoder | Project-level only, no global config |

---

## Safety Mechanisms

- **Default Backup**: Backs up all files to desktop before deletion (`~/Desktop/agent-rules-backup-timestamp/`), allowing recovery anytime.
- **Preview Mode**: Use `--dry-run` to confirm which files will be deleted before actually executing.
- **Confirmation Prompt**: Requires manual `YES` confirmation by default to prevent accidental operations.
- **Self-Protection (Enabled by Default)**:
  - When running `--mode global` or `--mode all`, this skill (clear-skills) is **protected by default** and won't be cleared.
  - This allows safe cleanup of other platforms' rules without worrying about deleting the tool itself.
  - If you truly need to delete this skill, use `--include-self` to disable self-protection.
- **Smart Scanning**: The script only scans and deletes files/directories that **actually exist**. If certain platforms are not installed on your system or their rule files don't exist, those empty targets won't be shown or deleted.

---

## FAQ

**Q: Will this delete my project code?**
A: No. This tool only removes AI agent rule/skill files (e.g., `.cursorrules`, `CLAUDE.md`, `.workbuddy/skills/`). Your source code and other files are completely safe.

**Q: Can I recover deleted files?**
A: Yes. All files are automatically backed up to your desktop before deletion. You can manually copy them back if needed.

**Q: What if I only want to clear one platform?**
A: Use the `--platforms` parameter to specify which platforms to clean. Example: `python scripts/clear_agent_rules.py --platforms cursor,copilot`

**Q: Why doesn't this skill get deleted when I clear global rules?**
A: This is an intentional self-protection feature. The skill needs to exist to be able to clear itself. Use `--include-self` if you really want to delete it too.

**Q: Does this work on Windows/macOS/Linux?**
A: Yes. The script uses pure Python and handles all three operating systems automatically.

**Q: Can I run this in a CI/CD pipeline?**
A: Yes. Use `--yes --no-backup` flags for non-interactive execution. Use with caution in automated environments.

---

## Troubleshooting

**Permission Denied Errors**
- If you encounter permission errors, try running the script with appropriate permissions (e.g., administrator/root)
- On Windows, some directories may require elevated privileges

**Large Backup Size**
- If the backup is too large, use `--no-backup` (not recommended) or manually manage backup location
- Consider cleaning up old backup folders from your desktop

**Platform Not Found**
- If a platform isn't detected, it means the platform isn't installed or has no rule files
- This is normal behavior—the script only targets existing files
