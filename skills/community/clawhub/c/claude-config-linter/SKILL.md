---
name: claude-config-linter
description: Lint your Claude Code config for token waste. Checks CLAUDE.md, hooks, skills, and commands. Gives health score and actionable fixes. Use when user asks about config optimization or token waste.
config_paths:
  - ~/.claude/CLAUDE.md
  - ~/.claude/settings.json
  - ~/.claude/skills/
  - ~/.claude/commands/
requires:
  - cclint
---

# Claude Config Linter

Lint your Claude Code config for token waste.

## Data access

- Reads CLAUDE.md, settings.json, skills/, and commands/ in ~/.claude/
- Runs offline, no network access, no credentials
- Open source: https://github.com/SingggggYee/cclint

## Usage

Requires `cclint` CLI. See https://github.com/SingggggYee/cclint for installation.

```bash
cclint
```

JSON output: `cclint --json`
