---
name: coding-sessions
description: Run long-lived AI coding agents (Codex CLI, Claude Code, Ralph loops) in persistent tmux sessions with completion hooks and automatic monitoring. Use when launching coding agents for multi-step tasks, managing background programming sessions, running Ralph loops with PRD validation, or needing coding work that survives process restarts.
---

# Coding Sessions

Orchestrate long-running AI coding agents in persistent tmux sessions with completion notifications and health monitoring.

## Why tmux?

Background exec processes die on gateway restart. Any coding agent expected to run >5 minutes MUST run inside tmux. This is non-negotiable.

**Always use the stable socket** (`~/.tmux/sock`) — the default `/tmp` socket gets reaped by macOS.

## Quick Start

### Single Codex Task

```bash
tmux -S ~/.tmux/sock new -d -s <name> "cd <project-dir> && \
  PATH=/opt/homebrew/bin:\$PATH codex exec --full-auto '<task description>'; \
  EXIT_CODE=\$?; echo 'EXITED:' \$EXIT_CODE; \
  openclaw system event --text '<name> finished (exit \$EXIT_CODE) in <project-dir>' --mode now; \
  sleep 999999"
```

### Ralph Loop (preferred for multi-step work)

```bash
tmux -S ~/.tmux/sock new -d -s <name> "cd <project-dir> && \
  PATH=/opt/homebrew/bin:\$PATH ralphy --codex --prd PRD.md; \
  EXIT_CODE=\$?; echo 'EXITED:' \$EXIT_CODE; \
  openclaw system event --text 'Ralph loop <name> finished (exit \$EXIT_CODE) in <project-dir>' --mode now; \
  sleep 999999"
```

### Parallel Ralph Loops

```bash
tmux -S ~/.tmux/sock new -d -s <name> "cd <project-dir> && \
  PATH=/opt/homebrew/bin:\$PATH ralphy --codex --parallel --prd PRD.md; \
  EXIT_CODE=\$?; echo 'EXITED:' \$EXIT_CODE; \
  openclaw system event --text 'Ralph parallel <name> finished (exit \$EXIT_CODE)' --mode now; \
  sleep 999999"
```

## Command Anatomy

Every tmux coding session follows this pattern:

1. **Stable socket:** `-S ~/.tmux/sock` (survives macOS `/tmp` cleanup)
2. **Named session:** `-s <name>` (human-readable, used for monitoring)
3. **PATH fix:** `PATH=/opt/homebrew/bin:$PATH` (Ralph/Codex need Homebrew binaries)
4. **The agent command:** `codex exec --full-auto` or `ralphy --codex`
5. **Completion hook:** Captures exit code, fires `openclaw system event` for instant notification
6. **Sleep tail:** `sleep 999999` keeps the shell alive so output remains readable

## Monitoring

```bash
# List all sessions
tmux -S ~/.tmux/sock list-sessions

# Check recent output
tmux -S ~/.tmux/sock capture-pane -t <name> -p | tail -20

# Check if session exists
tmux -S ~/.tmux/sock has-session -t <name> 2>/dev/null && echo "alive" || echo "dead"

# Kill a completed session
tmux -S ~/.tmux/sock kill-session -t <name>
```

## When to Use Ralph vs Raw Codex

| Scenario | Tool |
|----------|------|
| Multi-step feature with PRD/checklist | `ralphy --codex --prd PRD.md` |
| Task that has stalled or failed before | `ralphy --codex` (auto-retry with fresh context) |
| Parallel independent tasks | `ralphy --codex --parallel --prd PRD.md` |
| Tiny focused fix, one-file change | `codex exec --full-auto` |
| Exploratory work, investigation | `codex exec --full-auto` |

## PRD Format

Ralph tracks completion via markdown checklists:

```markdown
## Tasks
- [ ] Create the API endpoint
- [ ] Add input validation
- [ ] Write tests
- [x] Already done (skipped by Ralph)
```

Ralph restarts the agent with fresh context each iteration. The agent picks up where it left off via files + git history. Include test-first instructions in task prompts for deterministic validation.

## Post-Completion Verification

Before declaring success or failure, always check:

1. `git log --oneline -3` — did the agent commit?
2. `git diff --stat` — uncommitted changes?
3. Read the tmux pane output — what actually happened?

Ralph can mark PRD tasks as done even when codex fails silently. Verify via git, not PRD checkboxes.

## Logging

After starting any long-running session, log it in daily notes (`memory/YYYY-MM-DD.md`) under "Active Long-Running Processes" with the session name and original command. This ensures context survives compaction and heartbeat monitoring can track/restart sessions.

## Troubleshooting

- **"Failed to refresh token"** in `~/.codex/log/codex-tui.log` → run `codex auth login`
- **Agent reads files and exits** → wrap in Ralph loop (auto-retry solves this)
- **API rate limits (429s)** with parallel agents → reduce parallelism or stagger starts
- **Session died** → restart with same command from daily notes
