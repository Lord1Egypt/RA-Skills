---
name: agent-hooks
version: 1.0.0
description: Claude Code Stop/PreToolUse/PostToolUse hook 脚本集。当 agent 提前停止、工具反复失败、或以投机语言完成任务时自动干预。每个脚本是独立的 bash hook，配到 settings.json 即可生效。不用于设计决策（用 harness-design-patterns）或运维监控（用 agent-ops）。
license: MIT
triggers:
  - agent keeps stopping
  - ralph
  - persistent execution
  - 不要停
  - tool retry
  - 工具重试
  - doubt gate
  - speculative
  - post edit check
  - hook scripts
---

# Agent Hooks

即插即用的 Claude Code hook 脚本。解决 3 类问题：agent 提前停止、工具重试死循环、投机性完成。

## When to Use

- Agent 在复杂任务中只完成一部分就停了 → 用 Ralph hooks
- 工具反复失败但 agent 一直重试同一个命令 → 用 tool-error hooks
- Agent 说"可能""大概"就声称完成了 → 用 doubt-gate hook
- 编辑后想立即知道有没有引入错误 → 用 post-edit-check hook

## When NOT to Use

- Headless `-p` 模式（Stop hook 不触发，用 `--max-turns`）
- 设计多 agent 系统架构 → 用 `harness-design-patterns`
- 监控运行中的 session、处理限速 → 用 `agent-ops`

---

## 安装

将需要的 hook 加入 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [
        {"type": "command", "command": "bash /path/to/agent-hooks/scripts/ralph-stop-hook.sh"},
        {"type": "command", "command": "bash /path/to/agent-hooks/scripts/doubt-gate.sh"}
      ]
    }],
    "PostToolUseFailure": [{
      "hooks": [
        {"type": "command", "command": "bash /path/to/agent-hooks/scripts/tool-error-tracker.sh", "async": true}
      ]
    }],
    "PreToolUse": [{
      "hooks": [
        {"type": "command", "command": "bash /path/to/agent-hooks/scripts/tool-error-advisor.sh"}
      ]
    }],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [
        {"type": "command", "command": "bash /path/to/agent-hooks/scripts/post-edit-check.sh", "async": true}
      ]
    }]
  }
}
```

所有脚本需要环境变量 `NC_SESSION`（session ID）。状态写入 `$HOME/<config-dir>/shared-context/sessions/<session-id>/`（路径可通过 `$HOME` 环境变量配置）。

## Scripts

| 脚本 | Hook 类型 | 功能 | 详情 |
|------|----------|------|------|
| `ralph-init.sh <id> [max]` | CLI 调用 | 初始化持续执行状态（支持 crash 恢复） | [详情](references/01-ralph.md) |
| `ralph-stop-hook.sh` | Stop | 阻止提前停止，4 个安全阀保底 | [详情](references/01-ralph.md) |
| `ralph-cancel.sh <id> [reason]` | CLI 调用 | 发送 30s TTL 取消信号 | [详情](references/07-cancel-ttl.md) |
| `tool-error-tracker.sh` | PostToolUseFailure | 追踪连续失败，3 次软提示 / 5 次强制换方案 | [详情](references/03-tool-error.md) |
| `tool-error-advisor.sh` | PreToolUse | 5 次失败后 block 同一命令 | [详情](references/03-tool-error.md) |
| `doubt-gate.sh` | Stop | 检测投机语言，强制提供证据 | [详情](references/13-doubt-gate.md) |
| `post-edit-check.sh` | PostToolUse (Write\|Edit) | 编辑后即时跑 linter/type checker | [详情](references/15-post-edit-diagnostics.md) |

## Hook 协议

所有 hook 脚本遵循 Claude Code hook 协议：
- **输入**：stdin 接收 JSON（包含 tool_name, tool_input, session_id 等）
- **输出**：stdout 输出 JSON 决策

```json
{"continue": true}                                    // 放行
{"decision": "block", "reason": "..."}                 // 阻止（Stop hook）
{"hookSpecificOutput": {"additionalContext": "..."}}   // 注入上下文
```

## 安全阀

Ralph stop hook 在以下条件下 MUST 放行，NEVER block：
1. 认证失败（401/403，从 stop_reason 检测）
2. Cancel 信号存在且未过期
3. 闲置超时 > 2 小时
4. 达到 max_iterations

> 注：Context usage >= 95% 安全阀**未实现**——Claude Code 不在 hook 输入或 transcript 中暴露 context_window_size。Claude Code 自身的 reactive compaction 机制会独立处理 context 溢出。

## 条件判断规则

- 如果 headless `-p` 模式 → 不要用 Ralph，而是用 `--max-turns`
- 如果任务 < 5 分钟 → 不需要 Ralph
- 如果不确定 → 先不启用，观察 agent 是否提前停止再决定
