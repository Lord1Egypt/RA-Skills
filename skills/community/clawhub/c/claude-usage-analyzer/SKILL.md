---
name: claude-usage-analyzer
description: Analyze Claude Code token usage. Shows where tokens went, which projects cost most, and how to reduce waste. Use when user asks about token usage, costs, or burn rate.
config_paths:
  - ~/.claude/projects/*/*.jsonl
requires:
  - claude-usage-analyzer
---

# Claude Usage Analyzer

Analyze your Claude Code token usage by parsing local session logs.

## Data access

- Reads `~/.claude/projects/*/*.jsonl` (local Claude Code session logs)
- Runs offline, no network access, no API keys, no credentials
- Open source: https://github.com/SingggggYee/claude-usage-analyzer

## Usage

Requires the `claude-usage-analyzer` CLI to be pre-installed. See https://github.com/SingggggYee/claude-usage-analyzer for installation instructions.

```bash
claude-usage-analyzer
```

More commands:

- `claude-usage-analyzer report --days 7` (last 7 days)
- `claude-usage-analyzer sessions` (top sessions by cost)
- `claude-usage-analyzer session <id>` (per-turn breakdown)
- `claude-usage-analyzer --json` (machine-readable output)
