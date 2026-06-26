# Troubleshooting

## Claude Code doesn't start

```bash
# Check node version
tmux send-keys -t <session> "node --version" Enter
# If wrong version:
tmux send-keys -t <session> "nvm use 20 && claude --dangerously-skip-permissions" Enter
```

## Worktree branch conflict

```
fatal: 'feat/x' is already checked out at '/tmp/task-x'
```
Either remove the existing worktree first, or use a different branch name:
```bash
git worktree remove /tmp/task-x
# then retry
```

## .env not found in worktree

```bash
ln -sf <project>/.env <worktree-path>/.env
```

## tmux session already exists

```bash
tmux kill-session -t <name>
tmux new-session -d -s <name> -c <path>
```

## Claude Code hangs / no output

```bash
tmux capture-pane -t <session> -p | tail -20
# If stuck on a question, relay to user then:
tmux send-keys -t <session> "y" Enter
# or Ctrl+C to interrupt:
tmux send-keys -t <session> C-c
```

## Main workspace can't checkout worktree branch

Git won't allow two worktrees on the same branch simultaneously.
Remove the worktree first:
```bash
git worktree remove /tmp/task-x   # branch is preserved
git switch feat/x                  # now works in main workspace
```
