---
name: codex-tmux
description: >
  Launch long-running Codex (or Claude Code) coding tasks via tmux on WSL2/Linux, bypassing SIGTERM timeouts.
  Use this skill INSTEAD OF coding-agent whenever: (1) the task may take >60s, (2) you need full-auto Codex execution,
  (3) you are on WSL2 with a custom OpenAI-compatible proxy (OPENAI_BASE_URL), (4) you want to monitor/steer a
  background Codex session mid-run, (5) building or extending the MyClaw project, (6) any multi-file code generation
  task. This skill has higher priority than coding-agent for Codex full-auto workflows on this machine.
  Triggers: codex tmux, long task, full-auto, MyClaw, background codex, WSL2 coding agent.
---

# Codex via tmux (WSL2 / Custom Proxy)

Preferred pattern for all Codex full-auto tasks on this machine. Avoids SIGTERM, supports mid-run steering.

## Environment (this machine)

```bash
OPENAI_API_KEY="sk-5Ds6eFbTEE1zu5fQ14F4FfB5892b419dB1BfC7292147B9Ef"
OPENAI_BASE_URL="http://152.53.52.170:3003/v1"
```

Always pass both vars. Do NOT rely on shell inheritance — OpenClaw subprocesses don't source `.bashrc`.

## Standard Launch Pattern

```bash
SESSION="codex-<feature>"   # e.g. codex-auth, codex-tools
WORKDIR=~/MyClaw            # or target repo

tmux new-session -d -s "$SESSION" -c "$WORKDIR" \
  "OPENAI_API_KEY='sk-5Ds6e...' OPENAI_BASE_URL='http://152.53.52.170:3003/v1' \
   codex --model gpt-5.3-codex --full-auto '$(cat /tmp/task.txt)'"
```

Write long prompts to `/tmp/task.txt` first, then reference via `$(cat /tmp/task.txt)`.

## Monitoring

```bash
# Check if alive
tmux has-session -t "$SESSION" 2>/dev/null && echo running || echo done

# Tail output (last 50 lines)
tmux capture-pane -t "$SESSION" -p | tail -50

# Or via OpenClaw exec:
exec("tmux capture-pane -t codex-auth -p | tail -30")
```

## Mid-run Steering

```bash
tmux send-keys -t "$SESSION" "停一下。先做 API 层，不要改 UI。" Enter
tmux send-keys -t "$SESSION" "类型定义在 src/types.ts，用那个。" Enter
```

## Task JSON Tracking

Write to `/tmp/codex-tasks.json` to track parallel jobs:

```json
{
  "id": "feat-tools",
  "session": "codex-tools",
  "model": "gpt-5.3-codex",
  "desc": "实现工具系统 exec/read/write/web_fetch",
  "repo": "MyClaw",
  "startedAt": 1772433000000,
  "status": "running"
}
```

## Completion Check

Poll every 2–3 min via:
```bash
tmux has-session -t "$SESSION" 2>/dev/null || echo "DONE"
git -C "$WORKDIR" log --oneline -3
```

Codex "完成" = tmux session 自动退出 + git commit 存在。

## Cleanup

```bash
tmux kill-session -t "$SESSION" 2>/dev/null
git worktree prune
```

## MyClaw-Specific Notes

- Repo: `~/MyClaw`, GitHub: https://github.com/InuyashaYang/MyClaw
- 模型首选 `gpt-5.3-codex`，轻量测试用 `gpt-4.1-mini`
- 详细已知坑见 → `references/lessons.md`
