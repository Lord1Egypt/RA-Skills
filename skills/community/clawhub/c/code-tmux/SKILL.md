---
name: code-tmux
description: Run coding tasks using a persistent tmux session with git worktree isolation. Supports multiple coding agents (Claude Code, Codex, CodeBuddy, OpenCode, etc.). Activate when user asks to build, fix, refactor, or review code. Always uses tmux for persistent multi-turn conversation — never one-shot mode.
---

# Coding Agent Task (tmux + worktree)

Run coding tasks by spawning a coding agent in a **tmux session + git worktree**. Every task gets its own isolated branch and persistent conversation.

## Step 0: Determine which agent to use

**Check memory first:**
```
memory_search("preferred coding agent tool")
```

- If found → use that tool, no need to ask
- If not found → ask the user:

  > "Which coding agent should I use? (default: claude)
  > Options: claude, codex, opencode, codebuddy, or any CLI tool name"

  Then save the answer to memory:
  ```
  memory: preferred_coding_agent = <tool>
  ```
  Write to `MEMORY.md` under a "Preferences" section.

**Default if user doesn't answer:** `claude`

## Step 1 & 2: Setup worktree + Start session

### If tool is `claude` (recommended)

Use `claude -w` — it manages the worktree automatically. Add `--tmux` to also create a tmux session:

```bash
cd <project>
# worktree + tmux in one command:
claude -w <branch-name> --tmux --dangerously-skip-permissions
```

- `-w <name>` creates and checks out a new git worktree branch automatically
- `--tmux` opens it in a tmux session (uses iTerm2 panes if available, otherwise classic tmux)
- No need to manually `git worktree add` or `tmux new-session`

### If tool is other (codex, opencode, codebuddy, etc.)

Manage worktree and tmux manually:

```bash
# Create worktree
git -C <project> worktree add -b <branch> <worktree-path> main

# Symlink env files
ln -sf <project>/.env <worktree-path>/.env
ln -sf <project>/.env.local <worktree-path>/.env.local   # if exists

# Create tmux session and launch agent
tmux new-session -d -s <task-name> -c <worktree-path>
tmux send-keys -t <task-name> "nvm use 20 && <tool-command>" Enter
```

| Tool | Command |
|---|---|
| `codex` | `codex` |
| `opencode` | `opencode` |
| `codebuddy` | `codebuddy` (or check its CLI name) |
| other | use the tool's interactive CLI command |

## Step 3: Send task with plan-first instruction

For `claude -w --tmux`, the session name is auto-set to the branch name. Find it with:
```bash
tmux list-sessions
```

Then send the task:
```bash
tmux send-keys -t <session-name> -l -- "Your task here.

Before making any changes, show me a plan of what you intend to do and wait for my approval."
sleep 0.1
tmux send-keys -t <session-name> Enter
```

## Step 4: Relay plan to user

```bash
# Poll for plan output
tmux capture-pane -t <task-name> -p | tail -30
```

When agent outputs a plan → **relay it to the user**, wait for their confirmation before proceeding.

Relay flow:
1. Agent outputs plan → relay to user
2. User says "ok" / requests changes → forward to agent
3. Agent proceeds → monitor and relay further questions

```bash
# Send user's response
tmux send-keys -t <task-name> -l -- "<user response>"
sleep 0.1
tmux send-keys -t <task-name> Enter

# Check if waiting for input
tmux capture-pane -t <task-name> -p | tail -10 | grep -E "❯|Yes.*No|proceed|permission|plan|approve"
```

## Step 5: Parallel tasks

Same pattern, multiple sessions:
```bash
tmux new-session -d -s task-a -c /tmp/task-a
tmux new-session -d -s task-b -c /tmp/task-b
```

Check all at once:
```bash
for s in task-a task-b; do
  echo "=== $s ==="
  tmux capture-pane -t $s -p 2>/dev/null | tail -5
done
```

## Step 6: Cleanup

For `claude -w --tmux` (worktree auto-managed):
```bash
tmux kill-session -t <branch-name>
git worktree remove <worktree-path>   # branch preserved
```

For other tools (manual worktree):
```bash
git -C <project> worktree remove <worktree-path>   # branch preserved
tmux kill-session -t <task-name>
```

User can then test in main workspace:
```bash
git switch <branch>
```

## Rules

- **Check memory first** — never ask for tool preference if already saved
- **Always** use worktrees — one per task, no exceptions
- **Always** use tmux — persistent session, multi-turn conversation
- **Always** show plan first, wait for user approval before agent touches files
- **Always** symlink `.env` files — don't copy
- One status message when starting, one when done or stuck
- See `references/troubleshooting.md` for common issues
