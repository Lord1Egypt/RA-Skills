---
name: claude-code-statusline
description: Install and configure a custom Claude Code status line showing real-time token usage, context window percentage, git branch, and color-coded warnings. Use when the user asks to "install statusline", "setup statusline", "configure statusline", "setup status line", "install status bar", "show token usage", "context window display", "statusline colors", "statusline thresholds", or wants to customize their Claude Code status bar display.
---

# Claude Code Status Line

Install a security-hardened status line for Claude Code CLI that displays:

```
user@host:dir (branch) | Model | In:8.5K Out:1.2K Cache:7K [23%]
```

## Prerequisites

- Python 3 (standard library only, no pip dependencies)
- `git` (optional, for branch display)

## Script

`scripts/statusline_installer.py` -- Python 3, standard library only.

```bash
# Install with defaults
python3 scripts/statusline_installer.py install

# Install with custom thresholds
python3 scripts/statusline_installer.py install --threshold-yellow 30 --threshold-orange 50 --threshold-red 70

# Install with combined token display
python3 scripts/statusline_installer.py install --token-display combined

# Check installation
python3 scripts/statusline_installer.py status

# Update config
python3 scripts/statusline_installer.py configure --threshold-red 80 --color-green cyan

# Remove
python3 scripts/statusline_installer.py uninstall [--remove-config]
```

## How It Works

1. **install** -- Copies `statusline.py` to `~/.claude/scripts/`, creates config at `~/.claude/statusline.config` (perms 600), updates `~/.claude/settings.local.json` with `python3 ~/.claude/scripts/statusline.py` command.

2. **status** -- JSON output: script installed, config state, settings configured, git availability.

3. **configure** -- Update thresholds (`--threshold-yellow/orange/red`), colors (`--color-green/yellow/orange/red`), display mode (`--token-display separate|combined`). Validates threshold ordering.

4. **uninstall** -- Removes script, reverts settings. `--remove-config` also deletes config file.

## Configuration

Config file: `~/.claude/statusline.config`

| Option | Default | Values |
|---|---|---|
| `TOKEN_DISPLAY` | `separate` | `separate` (In/Out/Cache), `combined` (total) |
| `THRESHOLD_YELLOW` | `40` | 0-100 |
| `THRESHOLD_ORANGE` | `50` | 0-100 |
| `THRESHOLD_RED` | `70` | 0-100 |
| `COLOR_*` | standard ANSI | Color name or ANSI code |

Available colors: green, yellow, orange, red, blue, cyan, magenta, purple, white, pink, bright-green, bright-yellow, bright-red, bright-blue, bright-cyan, bright-magenta.

## After Install

Restart Claude Code (`exit` then `claude`) to activate.
