---
name: coding-agent-loops
description: Run long-lived AI coding agents (Codex, Claude Code) in persistent tmux sessions with Ralph retry loops and completion hooks. Use when running multi-step coding tasks, PRD-based workflows, or any programming agent that needs to survive restarts, retry on failure, and notify on completion.
---

# Coding Agent Loops

Run AI coding agents in persistent, self-healing sessions with automatic retry and completion notification.

## Core Concept

Instead of one long agent session that stalls or dies, run many short sessions in a loop. Each iteration starts fresh — no accumulated context. The agent picks up where it left off via files and git history. This is the "Ralph loop" pattern.

## Prerequisites

- `tmux` installed
- `ralphy-cli`: `npm install -g ralphy-cli`
- A coding agent: `codex` (Codex CLI) or `claude` (Claude Code)
- Stable tmux socket: always use `~/.tmux/sock` (default `/tmp` socket gets reaped by macOS)

## Quick Start

### Single Task
```bash
tmux -S ~/.tmux/sock new -d -s my-task \
  "cd /path/to/repo && ralphy --codex 'Fix the authentication bug'; \
   EXIT_CODE=\$?; echo EXITED: \$EXIT_CODE; \
   openclaw system event --text 'Ralph loop my-task finished (exit \$EXIT_CODE) in \$(pwd)' --mode now; \
   sleep 999999"
```

### PRD-Based Workflow (Preferred for Multi-Step Work)
```bash
tmux -S ~/.tmux/sock new -d -s feature-build \
  "cd /path/to/repo && ralphy --codex --prd PRD.md; \
   EXIT_CODE=\$?; echo EXITED: \$EXIT_CODE; \
   openclaw system event --text 'Ralph loop feature-build finished (exit \$EXIT_CODE) in \$(pwd)' --mode now; \
   sleep 999999"
```

### Parallel Agents on Separate Tasks
```bash
ralphy --codex --parallel --prd PRD.md
```

## Session Management

### Check Progress
```bash
tmux -S ~/.tmux/sock capture-pane -t my-task -p | tail -20
```

### List Active Sessions
```bash
tmux -S ~/.tmux/sock list-sessions
```

### Kill a Session
```bash
tmux -S ~/.tmux/sock kill-session -t my-task
```

## The Completion Hook (Mandatory)

Always append this to tmux commands:
```bash
; EXIT_CODE=$?; echo "EXITED: $EXIT_CODE"; \
openclaw system event --text "Ralph loop <name> finished (exit $EXIT_CODE) in $(pwd)" --mode now; \
sleep 999999
```

**Why each part matters:**
- `EXIT_CODE=$?` — captures the agent's exit code
- `echo "EXITED: $EXIT_CODE"` — visible in tmux pane output
- `openclaw system event` — fires a wake event so OpenClaw notifies you immediately
- `sleep 999999` — keeps the shell alive so output remains readable

## PRD Format

Ralph tracks completion via markdown checklists:
```markdown
## Tasks
- [ ] Create the API endpoint
- [ ] Add input validation
- [ ] Write tests
- [x] Already done (skipped)
```

Ralph validates that all items are checked before accepting a completion signal from the agent.

## When to Use What

| Scenario | Tool |
|----------|------|
| Multi-step features, PRD checklists | `ralphy --codex --prd PRD.md` |
| Tasks that have stalled before | `ralphy --codex "task"` (auto-retry) |
| Tiny focused fixes, one-file changes | `codex exec --full-auto "task"` |
| Parallel work on different tasks | `ralphy --codex --parallel --prd PRD.md` |
| Skip tests/lint for speed | `ralphy --codex --fast "task"` |
| Use Claude Code instead of Codex | `ralphy --claude "task"` |

## Key Principles

1. **Always use tmux** — background exec processes die on gateway/host restart. tmux sessions persist.
2. **Always use the stable socket** (`~/.tmux/sock`) — the default `/tmp` socket gets cleaned up.
3. **Always add the completion hook** — without it you won't know when the agent finishes.
4. **Log active sessions** — record running sessions in daily notes or a tracking file so you don't lose awareness.
5. **Verify before declaring failure** — after a process ends, check `git log`, `git diff`, and process output before concluding it failed.
6. **PATH in tmux** — tmux may not inherit your full PATH. Prepend `/opt/homebrew/bin:` if tools aren't found.

## Troubleshooting

- **Agent exits immediately**: Check `~/.codex/log/codex-tui.log` for auth errors. May need `codex auth login`.
- **Ralph marks tasks done but nothing committed**: Ralph can mark PRD tasks complete even when the agent fails silently. Always verify via `git log --oneline -3` and `git diff --stat`.
- **API rate limits (429s)**: Common when running multiple parallel agents. Ralph's retry handles this, but reduce parallelism if persistent.
- **Session disappeared**: tmux sessions can die from OOM or system restarts. Check with `tmux -S ~/.tmux/sock has-session -t <name>` and restart if needed.
