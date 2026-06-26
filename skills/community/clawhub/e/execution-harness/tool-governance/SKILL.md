---
name: tool-governance
version: 2.0.0
description: 工具使用安全与可靠性。当工具反复失败、agent 绕过权限否决、或需要破坏性操作保护时使用。不适用于 agent 提前停止（用 execution-loop）或上下文管理（用 context-memory）。参见 error-recovery（限速恢复）。
license: MIT
triggers:
  - tool retry
  - tool error
  - permission denied
  - denial bypass
  - checkpoint rollback
  - bash safety
  - destructive command
  - tool input validation
---

# Tool Governance

工具使用的安全护栏：防止重试死循环、追踪权限否决、破坏性操作备份、输入验证。

## When to Use

- 工具反复失败 → Tool error escalation
- Agent 换说法绕过否决 → Denial circuit breaker
- Bash 可能造成不可逆破坏 → Checkpoint + rollback
- 需要阻止危险命令 → Tool input guard

## When NOT to Use

- Agent 提前停止 → 用 `execution-loop`
- 上下文管理 → 用 `context-memory`

---

## Patterns

### 2.1 Tool error escalation [script]

PostToolUseFailure hook 按 `tool_name + input_hash`（输入前 200 字符的哈希）分组计数连续失败，写入 `tool-errors.json`。PreToolUse hook 在每次调用前读取计数：3 次注入 `additionalContext` 软提示，5 次返回 `permissionDecision: "deny"` 硬阻止。`additionalContext` 是概率性干预（LLM 可能忽略），`updatedInput` 是确定性干预（直接改写输入）——高置信度场景优先用后者。tracker 和 advisor 必须同时部署，advisor 依赖 tracker 写入的状态文件做计数判断，单独部署任何一个都无效。 → [详见](references/tool-error.md)

### 2.2 Denial circuit breaker [script]

Agent 被拒绝后可能换表述重试——`rm` 被拦就试 `unlink`。本 pattern 追踪被否决的 tool+input 组合：3 次注入"该操作已被拒绝，换完全不同的方案"，5 次将该组合标记为 session 级禁止，PreToolUse 直接 block。与 2.1 的区别：2.1 处理技术失败（exit code != 0），2.2 处理策略拒绝（permission denied），解决方向完全不同——前者换参数/换工具，后者必须换方案。 → [详见](references/denial-circuit-breaker.md)

### 2.3 Checkpoint + rollback [script]

Claude Code 内置 checkpoint 只覆盖 Write/Edit，不覆盖 Bash 副作用。本 pattern 在 PreToolUse 检测到破坏性 Bash 命令（`rm -rf`、`git reset --hard`、`docker rm` 等）时，先 `git add -A && git stash create` 创建快照。命令执行后如果 PostToolUseFailure 触发，自动 `git stash apply` 回滚。代价是每次快照有 I/O 开销，且正则匹配可能误判注释中的命令。 → [详见](references/checkpoint-rollback.md)

### 2.4 Graduated permission rules [config]

一刀切的权限模型要么太松（YOLO mode 全放行）要么太紧（每次都确认）。本 pattern 用 PreToolUse hook 对工具调用做三级风险分类：Read/Glob/Grep 为 safe 自动放行，Write/Edit 检查路径是否在项目目录内（系统目录 deny），Bash 按命令内容匹配 dangerous（`rm -rf /`、`curl|sh` 直接 deny）/ medium（`sudo`、`--force` 放行但告警）。风险矩阵可通过外部 JSON 配置扩展，不同项目各自调整。 → [详见](references/graduated-permissions.md)

### 2.5 Component-scoped hooks [config]

全局 hooks 对所有 session 生效，但某些验证只在特定任务中需要。在 SKILL.md 或 agent frontmatter 中声明的 hooks 只在该组件激活时生效（Stop hook 在 subagent 中自动转为 SubagentStop）。配合 `once: true` 可实现一次性初始化 hook——session 开始时执行一次后自动停用。全局 hooks 先执行，组件 hooks 后执行；全局已 block 则组件 hook 不触发。 → [详见](references/scoped-hooks.md)

### 2.6 Tool input guard [script]

Agent 构造的 Bash 命令可能意外包含路径逃逸、全局破坏或远程注入——特别是从文件内容提取路径拼接命令时。PreToolUse hook 独立检查三类模式：路径边界（`realpath` 确认在项目根目录内，`/tmp` 和工具路径白名单放行）、破坏性黑名单（`rm -rf /`、`mkfs`、`dd`）、pipe-to-shell（`curl|sh`、`wget|sh`）。命中任一即 deny。独立于 2.4 的粗粒度分层，专做 Bash 细粒度输入校验。 → [详见](references/tool-input-guard.md)

## Hook Protocol: PreToolUse 的三种响应

PreToolUse hook 不只是 allow/deny。Claude Code 支持三种响应：

| 响应 | stdout 字段 | 用途 |
|------|-----------|------|
| **Allow/Deny** | `permissionDecision: "allow"` 或 `"deny"` | 放行或拦截工具调用 |
| **Modify Input** | `updatedInput: {...}` | 修改工具参数后放行 |
| **Inject Context** | `additionalContext: "..."` | 不改工具调用，但给 agent 补充信息 |

`updatedInput` 的典型用法：

```bash
# 给危险的 bash 命令自动加 timeout
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
if echo "$TOOL_INPUT" | grep -qE '^(find|du|tar) '; then
  MODIFIED=$(echo "$TOOL_INPUT" | sed 's/^/timeout 60 /')
  jq -n --arg cmd "$MODIFIED" \
    '{"hookSpecificOutput":{"updatedInput":{"command":$cmd}}}'
  exit 0
fi
```

注意多 hook 场景下 `updatedInput` 是 **last-one-wins**——后执行的 hook 覆盖前面的修改。详见 `principles.md` 的 Hook Aggregation Rules。

## Scripts

| 脚本 | Hook 类型 | 功能 |
|------|----------|------|
| `tool-error-tracker.sh` | PostToolUseFailure | 追踪连续失败 |
| `tool-error-advisor.sh` | PreToolUse | 5 次失败后 block |
| `denial-tracker.sh` | Stop | 从对话中推断权限否决 |
| `checkpoint-rollback.sh` | PreToolUse (Bash) | 破坏性命令前 stash |
| `tool-input-guard.sh` | PreToolUse (Bash) | 安全验证 |

## Workflow

工具调用前后的决策流：

```
工具调用 → PreToolUse hook 检查
  ├─ input guard (2.6): 路径逃逸/黑名单/curl|sh? → deny
  ├─ graduated permissions (2.4): safe/medium/dangerous? → allow/warn/deny
  ├─ denial tracker (2.2): 该 tool+pattern 已被 session 禁止? → block
  ├─ error advisor (2.1): 同一 tool+input 已连续失败?
  │     ├─ <3 次 → 放行
  │     ├─ 3-4 次 → additionalContext 软提示，放行
  │     └─ ≥5 次 → permissionDecision: deny
  └─ checkpoint (2.3): 破坏性命令? → git stash create 快照后放行

工具执行 → 成功? 结束
         → 失败? PostToolUseFailure hook
               ├─ tracker (2.1): tool_name+input_hash 计数 +1，写入 tool-errors.json
               └─ checkpoint (2.3): 有快照? → git stash apply 回滚
```

部署要求：tracker（观测）和 advisor（干预）必须同时注册。advisor 读取 tracker 写入的 `tool-errors.json` 做计数判断——只部署 tracker 等于只记录不拦截，只部署 advisor 则无数据可读。首次部署时，先单独跑 tracker 一个 session 收集失败基线，确认数据采集正常后再启用 advisor，根据实际失败分布调整 3x/5x 阈值（某些工具天然失败率高，阈值需要上调）。

<example>
cargo build 反复失败（cargo 未安装）：
1-2 次: tracker 记录，advisor 放行
3 次: advisor 注入 additionalContext="已连续失败 3 次，stderr: command not found"
5 次: advisor 返回 deny，agent 被迫改策略 → apt-get install cargo → tracker 重置，恢复可用
</example>

<anti-example>
只部署 tracker 不部署 advisor → agent 对同一命令重试 47 次，tracker 忠实记录全程，无人拦截
</anti-example>

## Output

| 文件 | 路径 | 说明 |
|------|------|------|
| `tool-errors.json` | `.claude/tool-errors.json` | 工具失败记录：工具名、命令、退出码、stderr、时间戳、连续失败计数 |
| `denials.json` | `.claude/denials.json` | 阻止记录：被 block 的工具调用、阻止原因、触发阈值、时间戳 |
| checkpoint stash entries | `git stash list` | 破坏性命令前由 checkpoint-rollback.sh 自动创建的 git stash 条目，命名格式 `harness-checkpoint-<timestamp>` |

## Usage

在 `.claude/settings.json` 中配置 hook：

```jsonc
{
  "hooks": {
    // 工具重试断路器（Pattern 2.1）+ 否决追踪（Pattern 2.2）
    "PreToolUse": [
      {
        "matcher": { "tool_name": "Bash|Write|Edit" },
        "hooks": [{
          "type": "command",
          "command": "bash tool-governance-pre.sh"
        }]
      }
    ],
    // 工具错误追踪（Pattern 2.3）+ 破坏性命令备份（Pattern 2.4）
    "PostToolUse": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash tool-governance-post.sh"
        }]
      }
    ]
  }
}
```

Hook 输入/输出格式：

PreToolUse hook 收到 stdin JSON：
```json
{"tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/build"}}
```

断路器触发时输出（deny + 原因）：
```json
{"decision": "deny", "hookSpecificOutput": {"reasonForBlocking": "[TOOL-GOV] Bash 连续失败 3 次，同一命令模式。请换一种方法或检查前提条件。"}}
```

updatedInput 修改工具参数（如加 --dry-run）：
```json
{"decision": "allow", "hookSpecificOutput": {"updatedInput": {"command": "rm -rf /tmp/build --dry-run"}}}
```

additionalContext 注入建议：
```json
{"decision": "allow", "hookSpecificOutput": {"additionalContext": "[TOOL-GOV] 检测到破坏性命令 rm -rf，已创建 git stash checkpoint harness-checkpoint-1710489600"}}
```

## Related

| Skill | 关系 |
|-------|------|
| `execution-loop` | Ralph 提供持续执行保障；tool-governance 提供工具级安全护栏。agent 不停 + 工具不炸 = 完整执行 |
| `error-recovery` | 处理限速 (rate limit)、crash、MCP 断连等 session 级故障；tool-governance 处理工具级重试失败。二者互补不重叠 |
| `quality-verification` | 编辑后 linting、提交前测试；tool-governance 在工具调用前拦截，quality-verification 在工具调用后验证。前者防错，后者查错 |
