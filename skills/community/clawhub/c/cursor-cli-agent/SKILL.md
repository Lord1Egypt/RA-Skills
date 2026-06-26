---
name: cursor-agent
description: 'Delegate coding tasks to Cursor Agent CLI. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (use sessions_spawn with runtime:"acp"), or any work in ~/clawd workspace (never spawn agents here). Requires a bash tool that supports pty:true.'
metadata:
  {
    "openclaw": { "emoji": "🎯", "requires": { "anyBins": ["agent"] } },
  }
---

# Cursor Agent Skill

Execute coding tasks using Cursor CLI (`agent` command). Supports multiple frontier models (GPT-5, Claude Opus/Sonnet, Gemini, Grok, etc.).

## ⚠️ PTY Mode Required!

Cursor Agent is an interactive terminal application that requires PTY to work correctly.

```bash
# ✅ Correct
bash pty:true command:"agent 'Your prompt'"

# ❌ Wrong - will hang without PTY
bash command:"agent 'Your prompt'"
```

---

## Bash Tool Parameters

| Parameter    | Type    | Description                                           |
| ------------ | ------- | ----------------------------------------------------- |
| `command`    | string  | Shell command to execute                               |
| `pty`        | boolean | **Required!** Allocates pseudo-terminal for interactive CLIs |
| `workdir`    | string  | Working directory (agent only sees this folder's context) |
| `background` | boolean | Run in background, returns sessionId for monitoring    |
| `timeout`    | number  | Timeout in seconds (kills process on expiry)           |
| `elevated`   | boolean | Run on host instead of sandbox (if allowed)            |

---

## Quick Start

```bash
# Check status and login
agent status
agent login

# List available models
agent --list-models

# Quick task (interactive mode)
bash pty:true command:"agent 'Add error handling to the API calls'"

# Specify working directory
bash pty:true workdir:~/Projects/myproject command:"agent 'Build a snake game'"
```

---

## The Pattern: workdir + background + pty

For longer tasks, use background mode:

```bash
# Start background task
bash pty:true workdir:~/project background:true command:"agent --yolo 'Refactor the auth module'"

# Returns sessionId, monitor with process tool
process action:list
process action:log sessionId:XXX
process action:poll sessionId:XXX

# Send input
process action:submit sessionId:XXX data:"yes"

# Terminate
process action:kill sessionId:XXX
```

**Why workdir matters:** Agent wakes up in a focused directory, doesn't wander off reading unrelated files (like your soul.md 😅).

---

## Command Flags Reference

| Flag | Description |
|------|-------------|
| `prompt` | Initial prompt for the agent |
| `--yolo` / `--force` | Auto-approve all operations (dangerous but fast) |
| `--model <model>` | Specify model (gpt-5, sonnet-4, opus-4, gemini, grok, etc.) |
| `--workspace <path>` | Working directory |
| `-w, --worktree [name]` | Run in isolated git worktree |
| `--print` | **Non-interactive mode**, output to console |
| `--mode <mode>` | Execution mode: plan (read-only planning), ask (Q&A) |
| `--plan` | Plan mode (read-only, no file modifications) |
| `--cloud` | Cloud mode |
| `--resume` | Resume previous session |
| `--trust` | Trust workspace (headless mode only) |

---

## Execution Modes

### Interactive Mode (default)
```bash
bash pty:true workdir:~/project command:"agent 'Build a dark mode toggle'"
```

### Auto-Execute Mode (--yolo)
```bash
# Auto-approve all operations, fast execution
bash pty:true workdir:~/project command:"agent --yolo 'Refactor the auth module'"
```

### Plan Mode (--plan)
```bash
# Read-only mode, generate plan without executing
bash pty:true workdir:~/project command:"agent --plan 'Analyze the codebase structure'"
```

### Ask Mode (--mode ask)
```bash
# Q&A only, no file modifications
bash pty:true command:"agent --mode ask 'Explain how the auth flow works'"
```

### Non-Interactive Mode (--print) ⭐ Unique Feature

Cursor's unique `--print` mode, ideal for scripting and CI/CD:

```bash
# Non-interactive execution, output to console
bash pty:true command:"agent --print 'Generate a summary of the codebase'"

# JSON output (ideal for parsing)
bash pty:true command:"agent --print --output-format json 'List all API endpoints'"

# Streaming JSON (real-time processing)
bash pty:true command:"agent --print --output-format stream-json 'Analyze the project'"
```

**Use cases:**
- CI/CD integration
- Automation scripts
- Batch tasks
- Scenarios requiring parsed results

---

## Git Worktree Isolation

For parallel processing of multiple independent tasks:

```bash
# Run in isolated worktree
bash pty:true workdir:~/project command:"agent -w fix-issue-78 'Fix the login bug'"

# Specify base branch
bash pty:true workdir:~/project command:"agent -w feature-x --worktree-base develop 'Add feature X'"
```

---

## Parallel Issue Fixing

Use git worktrees to fix multiple issues simultaneously:

```bash
# 1. Create worktrees for each issue
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 2. Launch agent in each worktree (background + PTY)
bash pty:true workdir:/tmp/issue-78 background:true command:"agent --yolo 'Fix issue #78: login bug. Commit and push.'"
bash pty:true workdir:/tmp/issue-99 background:true command:"agent --yolo 'Fix issue #99: API timeout. Commit and push.'"

# 3. Monitor progress
process action:list
process action:log sessionId:XXX

# 4. Create PRs
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title "fix: ..." --body "..."

# 5. Cleanup
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

---

## Batch PR Reviews

**⚠️ NEVER review PRs in OpenClaw's own project directory!**

```bash
# Clone to temp directory
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130

# Review in plan mode (read-only)
bash pty:true workdir:$REVIEW_DIR command:"agent --plan 'Review this PR for security issues and code quality'"

# Cleanup
trash $REVIEW_DIR
```

### Batch Review Multiple PRs

```bash
# Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Launch multiple agents in parallel
bash pty:true workdir:~/project background:true command:"agent --plan 'Review PR #86. git diff origin/main...origin/pr/86'"
bash pty:true workdir:~/project background:true command:"agent --plan 'Review PR #87. git diff origin/main...origin/pr/87'"

# Monitor
process action:list

# Post results to GitHub
gh pr comment 86 --body "<review content>"
```

---

## Process Tool (Background Task Management)

| Action | Description |
|--------|-------------|
| `list` | List all running sessions |
| `poll` | Check if session is still running |
| `log` | Get session output (supports offset/limit) |
| `write` | Send raw data to stdin |
| `submit` | Send data + newline (simulate Enter) |
| `send-keys` | Send key presses |
| `paste` | Paste text |
| `kill` | Terminate session |

---

## Model Selection

```bash
# List available models
agent --list-models

# Specify model
bash pty:true command:"agent --model opus-4 'Complex refactoring task'"
bash pty:true command:"agent --model gpt-5 'Build a CLI tool'"
bash pty:true command:"agent --model gemini 'Analyze this Python codebase'"
```

---

## Auto-Notify on Completion

For long-running tasks, append a wake trigger to your prompt:

```bash
bash pty:true workdir:~/project background:true command:"agent --yolo 'Build a REST API for todos.

When completely finished, run: openclaw system event --text \"Done: Built todos REST API\" --mode now'"
```

This triggers immediate notification instead of waiting for heartbeat.

---

## Authentication

```bash
# Check login status
agent status

# Login
agent login

# Logout
agent logout

# View account info
agent about
```

---

## ⚠️ Rules

1. **Always use pty:true** - Will hang without PTY
2. **Use background for long tasks** - Don't block main thread
3. **--yolo for building** - Auto-approve changes
4. **--plan for reviewing** - Read-only analysis
5. **--print for scripting** - Non-interactive, parseable output
6. **Use -w worktree for isolation** - Parallel task processing
7. **NEVER start in ~/.openclaw/** - It'll read your soul docs!
8. **Notify user on completion** - Don't leave user guessing

---

## Progress Updates

When spawning background agents:
- Send 1 short message stating what's running
- Only update when something changes:
  - Milestone completed
  - User input needed
  - Error or user action required
  - Task finished (explain what changed)

---

## Learnings

- **PTY is essential:** Without `pty:true`, interactive agents hang or output garbage.
- **--print is powerful:** Cursor's unique non-interactive mode, ideal for CI/CD and scripted tasks.
- **--plan for safety:** When unsure what the agent will do, use `--plan` first.
- **worktree for parallel:** For multiple independent tasks, worktree isolation is the best choice.
- **submit vs write:** `submit` sends data + Enter, `write` sends raw data only.