# AI Agent Rule/Skill File Path Reference

This document lists the rule file storage locations for all major AI IDE / coding platforms on **Windows / macOS / Linux**.

---

## 1. Project-Level Rule Files (relative to project root, common across all platforms)

| Platform | File/Directory Path | Notes |
|----------|---------------------|-------|
| **Cursor** | `.cursorrules` | Legacy single file |
| **Cursor** | `.cursor/rules/*.mdc` | New multi-file directory |
| **Windsurf (Codeium)** | `.windsurfrules` | Legacy single file |
| **Windsurf (Codeium)** | `.windsurf/rules/*.md` | New multi-file directory |
| **Claude Code** | `CLAUDE.md` | Project root |
| **Codex CLI** | `AGENTS.md` | Project root |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Main config file |
| **GitHub Copilot** | `.github/instructions/*.instructions.md` | Scoped rules |
| **Gemini CLI** | `GEMINI.md` | Project root |
| **Cline** | `.clinerules` | Legacy single file |
| **Cline** | `.clinerules/` | New multi-file directory |
| **Trae IDE** | `.trae/project_rules.md` | Project rules |
| **Amazon Q** | `.amazonq/rules/*.md` | Multi-file directory |
| **Continue.dev** | `.continuerc.json` | Workspace config |
| **Continue.dev** | `.continue/rules/*.md` | Rules directory |
| **Aider** | `.aider.conf.yml` | Project config file |
| **OpenCode** | `AGENTS.md` or `CLAUDE.md` | Project root |
| **Antigravity** | `.antigravity/rules.md` | Google Antigravity |
| **Amp** | `AGENTS.md` | Unified standard |
| **Goose** | `.goosehints`, `.goose/` | Project-level hints and rules |
| **Kilo Code** | `.kilocode/rules/` | Multi-file rules directory |
| **Kiro (AWS)** | `.kiro/steering/`, `.kiro/` | Steering rules |
| **Neovate** | `AGENTS.md` | Compatible with AGENTS.md standard |
| **OpenHands** | `config.toml`, `.openhands/` | Config and project directory |
| **PI (pi-coding-agent)** | `.pi/settings.json`, `.pi/` | Coding agent config |
| **Qoder** | `.qoder/rules/` | Project-level rules |
| **Roo Code** | `.roo/rules/`, `.roorules` | Directory structure and single file |
| **Zencoder** | `.zencoder/rules/` | Project-level Zen Rules |
| **Droid (Factory)** | `.droid/`, `AGENTS.md` | Factory AI platform |
| **WorkBuddy/CodeBuddy** | `.workbuddy/skills/` | Project-level skills |
| **OpenClaw Ecosystem** | `.openclaw/` | Project-level config directory |
| **QoderWork** | `.qoderwork/skills/` | Project-level skills directory |

---

## 2. User Global-Level Rule Files (by OS)

### Windows (`HOME` = `%USERPROFILE%`, e.g., `C:\Users\admin`)

| Platform | Path |
|----------|------|
| **Cursor** | `%USERPROFILE%\.cursor\rules\` |
| **Claude Code** | `%USERPROFILE%\.claude\CLAUDE.md` |
| **Claude Code (directory)** | `%USERPROFILE%\.claude\` |
| **Gemini CLI** | `%USERPROFILE%\.gemini\GEMINI.md` |
| **Cline** | `%USERPROFILE%\Documents\Cline\Rules\` |
| **Trae IDE** | `%USERPROFILE%\.trae\user_rules.md` |
| **WorkBuddy/CodeBuddy** | `%USERPROFILE%\.workbuddy\skills\` |
| **Continue.dev** | `%USERPROFILE%\.continue\` |
| **Aider** | `%USERPROFILE%\.aider.conf.yml` |
| **OpenCode** | `%USERPROFILE%\.config\opencode\` |
| **Amp** | `%USERPROFILE%\.factory\AGENTS.md` |
| **Goose** | `%APPDATA%\Block\goose\config\` |
| **Kilo Code** | `%USERPROFILE%\.kilocode\rules\` |
| **Kiro (AWS)** | `%USERPROFILE%\.kiro\` |
| **Neovate** | `%USERPROFILE%\.neovate\AGENTS.md` |
| **OpenHands** | `%USERPROFILE%\.openhands\` |
| **PI (pi-coding-agent)** | `%USERPROFILE%\.pi\agent\settings.json` |
| **Roo Code** | `%USERPROFILE%\.roo\rules\` |
| **Droid (Factory)** | `%USERPROFILE%\.factory\` |
| **OpenClaw** | `%USERPROFILE%\.openclaw\` |
| **QClaw** | `%USERPROFILE%\.openclaw\` (shared with OpenClaw) |
| **CoPaw** | `%USERPROFILE%\.copaw\` |
| **Manus** | `%USERPROFILE%\.manus\` |
| **HappyCapy** | `%USERPROFILE%\.happycapy\` |
| **QoderWork** | `%USERPROFILE%\.qoderwork\skills\` |

### macOS (`HOME` = `/Users/<username>`)

| Platform | Path |
|----------|------|
| **Cursor** | `~/.cursor/rules/` |
| **Claude Code** | `~/.claude/CLAUDE.md` |
| **Claude Code (directory)** | `~/.claude/` |
| **Gemini CLI** | `~/.gemini/GEMINI.md` |
| **Cline** | `~/Documents/Cline/Rules/` |
| **Trae IDE** | `~/.trae/user_rules.md` |
| **WorkBuddy/CodeBuddy** | `~/.workbuddy/skills/` |
| **Continue.dev** | `~/.continue/` |
| **Aider** | `~/.aider.conf.yml` |
| **OpenCode** | `~/.config/opencode/` |
| **Amp** | `~/.factory/AGENTS.md` |
| **Goose** | `~/.config/goose/` |
| **Kilo Code** | `~/.kilocode/rules/` |
| **Kiro (AWS)** | `~/.kiro/` |
| **Neovate** | `~/.neovate/AGENTS.md` |
| **OpenHands** | `~/.openhands/` |
| **PI (pi-coding-agent)** | `~/.pi/agent/settings.json` |
| **Roo Code** | `~/.roo/rules/` |
| **Droid (Factory)** | `~/.factory/` |
| **OpenClaw** | `~/.openclaw/` |
| **CoPaw** | `~/.copaw/` |
| **Manus** | `~/.manus/` |
| **HappyCapy** | `~/.happycapy/` |
| **QoderWork** | `~/.qoderwork/skills/` |
| **Note** | Qoder/Zencoder | Project-level only, no global config |

### Linux (`HOME` = `/home/<username>`)

| Platform | Path |
|----------|------|
| **Cursor** | `~/.cursor/rules/` |
| **Claude Code** | `~/.claude/CLAUDE.md` |
| **Claude Code (directory)** | `~/.claude/` |
| **Gemini CLI** | `~/.gemini/GEMINI.md` |
| **Cline** | `~/Documents/Cline/Rules/` or `~/Cline/Rules/` |
| **Trae IDE** | `~/.trae/user_rules.md` |
| **WorkBuddy/CodeBuddy** | `~/.workbuddy/skills/` |
| **Continue.dev** | `~/.continue/` |
| **Aider** | `~/.aider.conf.yml` |
| **OpenCode** | `~/.config/opencode/` |
| **Amp** | `~/.factory/AGENTS.md` |
| **Goose** | `~/.config/goose/` |
| **Kilo Code** | `~/.kilocode/rules/` |
| **Kiro (AWS)** | `~/.kiro/` |
| **Neovate** | `~/.neovate/AGENTS.md` |
| **OpenHands** | `~/.openhands/` |
| **PI (pi-coding-agent)** | `~/.pi/agent/settings.json` |
| **Roo Code** | `~/.roo/rules/` |
| **Droid (Factory)** | `~/.factory/` |
| **OpenClaw** | `~/.openclaw/` |
| **CoPaw** | `~/.copaw/` |
| **Manus** | `~/.manus/` |
| **HappyCapy** | `~/.happycapy/` |
| **QoderWork** | `~/.qoderwork/skills/` |
| **Note** | Qoder/Zencoder | Project-level only, no global config |

---

## 3. Universal Cross-Platform Files (read by multiple platforms)

| Filename | Supported Platforms |
|----------|---------------------|
| `AGENTS.md` | Codex CLI, Cursor, Claude Code, Cline, Continue, OpenCode, Amp, Neovate, Droid |
| `CLAUDE.md` | Claude Code, OpenCode, Neovate (compatible read) |
| `.cursorrules` | Cursor, Cline (automatic compatible read) |
| `.windsurfrules` | Windsurf, Cline (automatic compatible read) |

---

## 4. OpenClaw Ecosystem

The following platforms are based on or derived from OpenClaw, and their config directories may be compatible:

| Platform | Description | Config Path |
|----------|-------------|-------------|
| **OpenClaw** | Original open-source AI Agent | `~/.openclaw/` |
| **QClaw** | Tencent WeChat/QQ version | `~/.openclaw/` (shared) |
| **EasyClaw** | Zero-config desktop version | `~/.openclaw/` (shared) |
| **ArkClaw** | Volcano Engine version | `~/.openclaw/` (possibly shared) |
| **LobsterAI** | NetEase version | `~/.openclaw/` (possibly shared) |
| **HiClaw** | Hi version | `~/.openclaw/` (possibly shared) |
| **AutoClaw** | Zhipu version | `~/.openclaw/` (possibly shared) |
| **AntiClaw** | Anti version | `~/.openclaw/` (possibly shared) |

> Note: Some derivative versions may use independent config directories. If unsure about the specific path, you can use `--platforms openclaw` to clear them uniformly.

---

## 5. Emerging AI Tools

The following are emerging AI coding tools that have risen rapidly in recent years, supporting diverse configuration methods:

| Platform | Type | Description | Main Paths |
|----------|------|-------------|------------|
| **Amp** | AI coding agent | Developed by Sourcegraph, supports AGENTS.md unified standard | `AGENTS.md` / `~/.factory/AGENTS.md` |
| **Goose** | Open-source AI Agent | Open-sourced by Block, supports MCP protocol and skill extensions | `.goosehints` / `~/.config/goose/` |
| **Kilo Code** | VS Code extension | Based on Roo Code/Cline, multi-mode support | `.kilocode/rules/` / `~/.kilocode/rules/` |
| **Kiro** | AWS Agentic IDE | Official Amazon AI development environment | `.kiro/steering/` / `~/.kiro/` |
| **Neovate** | Terminal AI assistant | Compatible with AGENTS.md standard | `AGENTS.md` / `~/.neovate/AGENTS.md` |
| **OpenHands** | AI-driven development | Open-source multi-agent collaboration platform | `.openhands/` / `~/.openhands/` |
| **PI (pi-coding-agent)** | Coding agent CLI | Developed by badlogic, minimalist design | `.pi/settings.json` / `~/.pi/agent/settings.json` |
| **Qoder** | Alibaba intelligent coding platform | Supports project-level rule configuration | `.qoder/rules/` |
| **Roo Code** | VS Code extension | "Aggressive" fork of Cline | `.roo/rules/`, `.roorules` / `~/.roo/rules/` |
| **Zencoder** | AI coding Agent | Supports VS Code/JetBrains plugins | `.zencoder/rules/` |
| **Droid (Factory)** | Factory AI terminal agent | Enterprise-level AI coding assistant | `.droid/`, `AGENTS.md` / `~/.factory/` |

> Note: The Command Code tool currently lacks sufficient information and is not included in the list. If needed, please refer to relevant official documentation.
