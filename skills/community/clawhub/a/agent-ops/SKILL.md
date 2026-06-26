---
name: agent-ops
version: 1.0.0
description: Agent session 运维工具。当需要检测和恢复 API 限速、回收死 session 的知识、在破坏性操作前自动快照、或监控 context 使用率时使用。不用于安装 hook 脚本（用 agent-hooks）或架构设计（用 harness-design-patterns）。
license: MIT
triggers:
  - rate limit recovery
  - 限速恢复
  - stale session
  - 死 session
  - checkpoint rollback
  - context budget
  - token budget
  - model fallback
  - agent monitoring
  - session ops
---

# Agent Ops

Agent session 运维工具集。监控、恢复、保护运行中的 agent session。

## When to Use

- tmux 中的 agent 遇到 API 限速后挂死 → Rate Limit 恢复
- Session 静默死亡，需要回收其知识 → Stale Session Daemon
- Bash 命令可能造成不可逆破坏 → Checkpoint + Rollback
- Context 快用完，需要预算管理 → Token Budget / Context 估算
- 模型反复失败需要切换 → Auto Model Fallback

## When NOT to Use

- 安装 Stop/PreToolUse hook → 用 `agent-hooks`
- 设计 agent 架构 → 用 `harness-design-patterns`

---

## 工具概览

| 工具 | 类型 | 功能 | 详情 |
|------|------|------|------|
| **Rate Limit 恢复** | bash 脚本 / cron | 扫描 tmux pane 检测限速，自动发 Enter 恢复 | [详情](references/04-rate-limit.md) |
| **Context 估算** | bash 脚本 | 读 transcript 尾部 4KB 提取 token 使用率 | [详情](references/05-context-estimation.md) |
| **Stale Session Daemon** | daemon / cron | Heartbeat 检测 + 死 session 知识回收 | [详情](references/17-stale-session-daemon.md) |
| **Checkpoint + Rollback** | hook 脚本 | PreToolUse git stash + PostToolUseFailure 自动回滚 | [详情](references/19-checkpoint-rollback.md) |
| **Token Budget** | hook 脚本 | UserPromptSubmit 注入预算感知指令 | [详情](references/20-token-budget.md) |
| **Auto Model Fallback** | hook 脚本 | 3 次连续失败后升级 Haiku→Sonnet→Opus | [详情](references/21-model-fallback.md) |

## Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/context-usage.sh <transcript>` | 从 transcript JSONL 尾部估算 context 使用率 |

## Session State

所有状态统一在 `sessions/<session-id>/` 下。详见 [session-state-layout.md](../../shared/session-state-layout.md)。

## 条件判断规则

- 如果只有 1-2 个 session 在跑 → Rate Limit 恢复手动即可，不需要 daemon
- 如果 session 预计 < 30 分钟 → 不需要 Stale Session Daemon
- 如果没有破坏性 Bash 命令 → 不需要 Checkpoint
- 如果不确定 context 够不够 → 先跑 `context-usage.sh` 检查再决定
