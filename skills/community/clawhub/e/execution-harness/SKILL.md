---
name: execution-harness-hub
description: "Agent 执行可靠性体系的导航入口。当用户询问 agent 为什么停了、怎么防 agent 提前退出、execution harness 是什么、40 个 pattern 有哪些、6 轴架构、hook 怎么配时匹配。不执行具体操作——各子 skill 分别处理。"
triggers:
  - execution harness
  - agent 可靠性
  - agent 为什么停了
  - 40 patterns
  - 6 轴架构
  - harness 体系
  - hook 怎么配
  - agent reliability
  - Ralph 怎么用
  - 执行可靠性
version: 2.0.0
author: lanyasheng
---

# Execution Harness — 导航入口

40 patterns x 6 轴，让 Claude Code agent 把活干完。不是框架，不做模型调用——只管 hook 和脚本。

这个 skill 不执行操作。它帮你找到该用哪个子 skill。

## 你遇到什么问题？

| 问题 | 用哪个 skill | 关键 pattern |
|------|-------------|-------------|
| Agent 做了一半就停了 | **execution-loop** | 1.1 Ralph Stop Hook — 阻止提前退出，5 个安全阀 |
| "应该可以"但没跑测试 | **execution-loop** | 1.2 Doubt Gate — 检测投机语言，要求验证 |
| `cargo build` 重试 12 次 | **tool-governance** | 2.1 Tool Error Escalation — 3 次提示、5 次 block |
| `rm -rf` 毁了未提交代码 | **tool-governance** | 2.3 Checkpoint + Rollback — 自动 git stash |
| 压缩后忘了设计决策 | **context-memory** | 3.1 Handoff Documents — 决策写磁盘 |
| Context 快满了还在读大文件 | **context-memory** | 3.4 Token Budget — 80%+ 禁止直读 |
| 限速后 tmux 挂死 | **error-recovery** | 5.1 Rate Limit Recovery — cron 扫描恢复 |
| 5 个 agent 编辑同一文件 | **multi-agent** | 4.3 File Claim and Lock — 10min TTL 排他锁 |
| 提交了编译不过的代码 | **quality-verification** | 6.4 Test-Before-Commit — commit 前跑测试 |

## 6 轴速查

| 轴 | Skill | Pattern 数 | 核心能力 |
|----|-------|-----------|---------|
| 1 | **execution-loop** | 7 | Ralph Stop Hook、Doubt Gate、Drift Re-anchoring |
| 2 | **tool-governance** | 6 | 错误升级、权限否决、破坏性命令拦截 |
| 3 | **context-memory** | 8 | Handoff 文档、Compaction 抢救、Token Budget |
| 4 | **multi-agent** | 6 | Coordinator/Fork/Swarm、文件锁、盲审分离 |
| 5 | **error-recovery** | 7 | 限速恢复、Crash 恢复、模型降级建议 |
| 6 | **quality-verification** | 6 | 编辑后 lint、commit 前测试、session 指标 |

## 最小配置

3 个 hook 解决最常见的 3 个问题：

```jsonc
// ~/.claude/settings.json
{
  "hooks": {
    "Stop": [{"hooks": [
      {"type": "command", "command": "bash execution-loop/scripts/ralph-stop-hook.sh"},
      {"type": "command", "command": "bash execution-loop/scripts/doubt-gate.sh"}
    ]}],
    "PreToolUse": [{"hooks": [
      {"type": "command", "command": "bash tool-governance/scripts/tool-error-advisor.sh"}
    ]}],
    "PostToolUse": [{"matcher": {"tool_name": "Write|Edit|MultiEdit"}, "hooks": [
      {"type": "command", "command": "bash quality-verification/scripts/post-edit-check.sh"}
    ]}]
  }
}
```

## 仓库

GitHub: [lanyasheng/execution-harness](https://github.com/lanyasheng/execution-harness) | 90 tests | 依赖：bash、jq、python3、pytest
