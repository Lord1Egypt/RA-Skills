---
name: claude-code-remote
description: "Call Claude Code as a non-interactive coding agent on a remote machine via OpenClaw Node. Use when: (1) Your coding agent is on a separate machine from the Gateway, (2) You need to delegate coding tasks to a Claude Code instance connected via Node, (3) You want to use a worktree or fast local filesystem for remote projects, (4) Environment variables need login shell loading via bash -lc, (5) You're coordinating multi-agent workflows across machines."
---

# Claude Code Remote (OpenClaw Node)

通过 OpenClaw Node 在远程机器上以非交互模式调用 Claude Code。

```
Gateway ──exec host=node──→ Node ──bash -lc──→ claude --bare ──→ AI API
```

## Quick Reference

| 场景 | 命令模板 |
|------|---------|
| 短任务 | `bash -lc 'cd <project> && claude --bare -p "<任务>" --max-turns 10'` |
| 长任务流式 | `bash -lc 'cd <project> && claude --bare -p "<任务>" --output-format stream-json --verbose --include-partial-messages --max-turns 30'` |
| 全权限 | `bash -lc 'cd <project> && claude --bare -p "<任务>" --dangerously-skip-permissions --output-format stream-json --verbose --include-partial-messages --max-turns 30'` |
| 只读分析 | `bash -lc 'cd <project> && claude --bare -p "<任务>" --permission-mode plan --allowedTools "Read,Glob,Grep,LSP" --max-turns 10'` |

## Key Differences from Local

| Aspect | Local | Remote (Node) |
|--------|-------|---------------|
| Command wrapper | Direct | `bash -lc '...'` required |
| Project path | Native | Use WSL/Linux paths for speed |
| Env loading | Shell-dependent | Must be before `.bashrc` interactive guard |
| Exec tool | Standard | `host=node node=<id>` |

## Permission Modes

Same four levels as `claude-code-local`. See `references/permissions.md`.

| Level | Remote-Specific Note |
|-------|---------------------|
| 1 Read | Safe—no filesystem writes |
| 2 Analyze | `bash -lc` may need Node approval |
| 3 Edit | Writes may trigger Node security policy |
| 4 Full | Some Nodes block certain write operations |

## Node Security Workarounds

- Multi-line heredocs → Write script to `/tmp/` first
- Inline Python → Same, use script file
- Write operations → Backup before modifying: `cp f f.bak.$(date +%F)`

## OpenClaw Exec Configuration

```json
{
  "command": "bash -lc 'cd <project> && claude --bare -p \"<task>\" --max-turns 10'",
  "host": "node",
  "node": "<your-node-id>",
  "background": true,
  "timeout": 600
}
```

## Worktree Setup

For projects on slow cross-filesystem mounts (e.g., WSL `/mnt/c/`):

```bash
git worktree add -b work-branch /home/user/project-worktree main
```

Shares git data, keeps working files on fast native filesystem.

## Environment Setup

Ensure API credentials load in non-interactive shells:

```bash
# In ~/.bashrc, BEFORE the interactive guard:
export ANTHROPIC_API_KEY=sk-...

# Interactive guard (keep as-is):
case $- in
    *i*) ;;
      *) return;;
esac
```

## Timing & Post-Task

Same as `claude-code-local`. See its SKILL.md for timing table and checklist.

## References

- `references/permissions.md` — Detailed permission mode behavior
- `references/troubleshooting.md` — Remote-specific failure modes
