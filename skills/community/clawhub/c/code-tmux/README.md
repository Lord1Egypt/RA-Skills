# claude-code-tmux

An [OpenClaw](https://openclaw.ai) skill that runs coding tasks using a **persistent tmux session with git worktree isolation**.

Supports multiple coding agents — Claude Code, Codex, OpenCode, CodeBuddy, or any interactive CLI tool.

## What it does

- **Asks once, remembers forever** — first run asks which coding agent you prefer, saves it to memory, never asks again
- Every task gets its own **git worktree** (isolated branch, no file conflicts)
- Agent runs in a **tmux session** — persistent, multi-turn conversation
- **Plan mode by default** — agent always shows a plan and waits for your approval before touching files
- OpenClaw agent acts as **relay**: forwards plans/questions to you, sends your answers back

## Install

```bash
npx clawhub@latest install claude-code-tmux
```

Or clone directly:
```bash
git clone https://github.com/yuanshenstarto/claude-code-tmux.git
```

## Supported agents

| Agent | CLI |
|---|---|
| [Claude Code](https://github.com/anthropics/claude-code) | `claude` |
| [Codex](https://github.com/openai/codex) | `codex` |
| [OpenCode](https://github.com/sst/opencode) | `opencode` |
| CodeBuddy | `codebuddy` |
| Any interactive CLI | custom |

## Workflow

```
First run: "Which coding agent? (default: claude)" → saved to memory

You → OpenClaw agent → tmux session (your chosen agent) → git worktree
                  ↑_____________________________________________↓
                         relay: plans, questions, answers
```

When finished, the branch is preserved — switch to it in your main workspace to test.

## Requirements

- [tmux](https://github.com/tmux/tmux)
- Your preferred coding agent CLI installed
- Node.js >= 20 (for Claude Code / Codex)
- git

## License

MIT
