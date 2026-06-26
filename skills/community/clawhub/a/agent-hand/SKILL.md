# Agent Hand — AI Agent Command Center

Your AI army command center. Monitor and manage all AI agent sessions from one terminal.

Built for the one-person company (OPC) era — when you run Claude, Cursor, Codex, Gemini, and more simultaneously, Agent Hand is how you stay in control.

## What It Does

- **Unified Dashboard**: See every AI agent's status at a glance — running, waiting, idle, done
- **Instant Switch**: Jump into any agent session, work with it, Ctrl+Q back to command center
- **Smart Prioritization**: AI-powered session sorting — the agent that needs you most floats to top
- **Canvas Workflow** (Pro): Visual workflow map of all your agents and their task flow
- **Hook System**: Auto-detects Claude Code, Cursor, Codex, Windsurf, Kiro, OpenCode, Gemini sessions
- **Multi-Profile**: Separate work contexts (client projects, personal, side hustle)

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/weykon/agent-hand/master/install.sh | bash
```

Installs the `agent-hand` binary. Works on macOS (ARM + Intel) and Linux.

Requires: tmux

## Quick Start

```bash
# Launch the dashboard
agent-hand

# Auto-register hooks for all supported AI tools
agent-hand hooks install
```

Then just use your AI tools normally. Agent Hand detects new sessions automatically.

## Key Bindings

| Key | Action |
|-----|--------|
| `Ctrl+N` | Enter selected session |
| `Ctrl+Q` | Return to dashboard |
| `j/k` | Navigate sessions |
| `p` | Open Canvas (Pro) |
| `/` | Search sessions |
| `?` | Help |

## Pricing

- **Free**: Full TUI dashboard, session management, hook system
- **Pro** ($19/year): Canvas workflow, AI summaries, collaboration
- **Max** (coming): Web 3D dashboard, relationship graphs

## Links

- GitHub: https://github.com/weykon/agent-hand
- Website: https://agent-hand.dev

## Who Is This For

Solo developers, OPC founders, anyone running multiple AI agents daily. If you've ever lost track of which terminal has which AI — this is for you.
