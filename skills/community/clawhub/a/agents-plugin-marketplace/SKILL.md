---
name: "agents-plugin-marketplace"
description: "84 production-ready agentic plugins, 192 agents, 156 skills & 102 commands for Claude Code, Codex CLI, Cursor, OpenCode & Gemini CLI"
---

# Agentic Plugin Marketplace (OpenClaw)

84 production-ready agentic workflow building blocks: 84 plugins, 192 agents, 156 skills, 102 commands — built for Claude Code and consumed natively by OpenAI Codex CLI, Cursor, OpenCode, Gemini CLI, and GitHub Copilot.

**Source:** `C:\Users\Harry\Downloads\agents\`
**Original:** https://github.com/wshobson/agents
**License:** MIT

本技能基於 GitHub 上的 [wshobson/agents](https://github.com/wshobson/agents) 修改與封裝。

## Overview

A marketplace of agentic plugins with a single source-of-truth (`plugins/` directory) mapped to multiple agent harnesses:

| Harness | Status |
|---------|--------|
| Claude Code | Native plugin support |
| OpenAI Codex CLI | Supported |
| Cursor | Supported |
| OpenCode | Supported |
| Gemini CLI | Supported |
| GitHub Copilot | Supported |

## Structure

```
agents/
├── plugins/           # Plugin definitions (source of truth)
│   ├── python-development/
│   ├── web-framework/
│   ├── database/
│   └── ... (84 plugins)
├── docs/              # Documentation and harness guides
├── tools/             # Utility tools
├── AGENTS.md          # Agent definitions
└── Makefile           # Build and install commands
```

## Usage in OpenClaw

When the user needs agentic workflow building blocks:
1. Browse `plugins/` for available plugins
2. Each plugin contains agent definitions, skill references, and commands
3. Reference `docs/` for cross-harness usage patterns
