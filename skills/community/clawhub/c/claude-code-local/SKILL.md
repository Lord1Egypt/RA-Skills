---
name: claude-code-local
description: "Call Claude Code as a non-interactive coding agent on the same machine as OpenClaw. Use when: (1) You need to delegate coding, refactoring, or bug-fixing tasks to Claude Code, (2) You want non-interactive code exploration and analysis, (3) You need to run batch code reviews, (4) You're setting up automated CI/CD code checks, (5) You want to use Claude Code as a specialized subordinate for project work while keeping the orchestrator agent focused on coordination."
---

# Claude Code Local

调用本机 Claude Code 作为非交互 coding agent。Orchestrator 负责指挥和验收，Claude Code 负责写代码。

## Quick Reference

| 场景 | 命令模板 |
|------|---------|
| 短任务 | `cd <project> && claude --bare -p "<任务>" --max-turns 10` |
| 长任务 | `cd <project> && claude --bare -p "<任务>" --output-format stream-json --verbose --include-partial-messages --max-turns 30` |
| 全权限 | `cd <project> && claude --bare -p "<任务>" --dangerously-skip-permissions --output-format stream-json --verbose --include-partial-messages --max-turns 30` |
| 只读分析 | `cd <project> && claude --bare -p "<任务>" --permission-mode plan --allowedTools "Read,Glob,Grep,LSP" --max-turns 10` |
| JSON 输出 | `cd <project> && claude --bare -p "<任务>" --output-format json --max-turns 10` |

## Key Flags

| Flag | Purpose |
|------|---------|
| `--bare` | Minimal mode, skip hooks/LSP/plugins, faster startup |
| `-p` / `--print` | Non-interactive, output to stdout (**do not use PTY**) |
| `--max-turns N` | Limit turns: 10 short, 30 long |
| `--output-format stream-json` | Streaming output, prevents timeout |
| `--output-format json` | Single JSON with `result` field |
| `--verbose` | Detailed logging (with stream-json) |
| `--include-partial-messages` | Incremental output (with stream-json) |

## Permission Modes

Default to the lowest level that accomplishes the task.

| Level | Mode | Flags | Use Case |
|-------|------|-------|----------|
| 1 Read | plan | `--permission-mode plan --allowedTools "Read,Glob,Grep,LSP"` | Code exploration, doc review |
| 2 Analyze | default | `--allowedTools "Read,Bash,Glob,Grep,LSP"` | Run diagnostic commands |
| 3 Edit | acceptEdits | `--permission-mode acceptEdits --allowedTools "Read,Edit,Write,Bash,Glob,Grep,LSP"` | Modify source files |
| 4 Full | bypass | `--dangerously-skip-permissions` | Trusted projects, batch ops |

## Timing Expectations

| Complexity | Duration | max-turns |
|-----------|----------|-----------|
| Simple (回答问题) | 2-5 min | 5-10 |
| Medium (探索+单文件) | 5-15 min | 10-20 |
| Complex (多文件+测试) | 15-30 min | 20-40 |

> **Never kill Claude Code when exec times out.** Check `ps aux | grep claude` first.

## Post-Task Checklist

- [ ] Summary of changes
- [ ] Modified files list
- [ ] Commands executed
- [ ] `git status --short`
- [ ] `git diff --stat`
- [ ] Test results
- [ ] Next steps

## References

- `references/streaming.md` — Stream-JSON event types and filtering
- `references/troubleshooting.md` — Common failures and fixes
