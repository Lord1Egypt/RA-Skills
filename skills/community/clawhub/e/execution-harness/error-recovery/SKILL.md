---
name: error-recovery
version: 2.0.0
description: Agent 错误恢复与容错。当 session 遇到限速、crash 或模型失败时使用。不适用于工具重试死循环（用 tool-governance）或 agent 提前停止（用 execution-loop）。参见 tool-governance（错误追踪数据）。
license: MIT
triggers:
  - rate limit
  - 限速
  - crash recovery
  - stale session
  - MCP disconnect
  - model fallback
  - agent hang
---

# Error Recovery

Agent session 的错误恢复：限速恢复、crash 状态恢复、MCP 断连、模型降级。

## When to Use

- tmux agent 限速后挂死 → Rate limit recovery
- Session crash 后恢复进度 → Crash state recovery
- 模型反复失败 → Model fallback advisory

## When NOT to Use

- 工具重试 → 用 `tool-governance`
- Agent 提前停止 → 用 `execution-loop`

---

## Patterns

### 5.1 Rate Limit Recovery [script]

周期性扫描 tmux pane 内容，检测限速关键词（429 / "too many requests" / "usage limit"），限速解除后自动发送按键恢复。

实现要点：
- 扫描：`tmux capture-pane -t "$pane" -p -S -20` 取最后 20 行，grep `rate.?limit|429|too many requests|usage limit`
- **二次验证**（关键）：发送 Enter 前重新 capture 最后 5 行，如果匹配 `\[y/N\]|\[yes/no\]|confirm|delete|overwrite|force push`，拒绝发送——此时 pane 内容已从限速提示变成了破坏性确认
- 轮询间隔 60 秒，PID 文件防多实例

→ [详见](references/rate-limit.md)

### 5.2 Crash State Recovery [design]

新 session 启动时扫描残留状态，可恢复的从断点继续，损坏的回滚。

需要检查的残留状态：
- `sessions/*/ralph.json`：`active=true` 且 `last_checked_at` 超过 7200 秒（2 小时）→ 设 `active=false, deactivation_reason="stale"`
- `.claims/*.lock`：超过 15 分钟未释放 → `find .claims -name "*.lock" -mmin +15 -delete`
- `.working-state/current-plan.md`：存在则注入"上次 session 有中断的计划"到 additionalContext

Claude Code 自身的 `conversationRecovery.ts` 已处理消息链修复（孤立 tool_use 补 placeholder），hook 只需聚焦 ralph.json 和 lock 这些外部状态。

**无脚本时**：新 session 开始时手动执行 `find .claims -name "*.lock" -mmin +15 -delete` 和检查 `cat sessions/*/ralph.json | grep active`。 → [详见](references/crash-recovery.md)

### 5.3 Stale Session Daemon [design]

检测 session 静默死亡并抢救认知状态。

实现要点：
- Heartbeat 写入：PostToolUse hook 异步写 `date +%s > sessions/$SESSION_ID/heartbeat`
- Daemon 每分钟检查：heartbeat age > 300 秒且 `tmux has-session -t $SESSION` 失败 → session 死亡
- 抢救：从 transcript 提取未保存的发现，写入 `sessions/$SESSION/handoffs/scavenged.md`，设 status 为 `scavenged`

与 crash recovery 的区别：crash recovery 恢复执行状态，stale session daemon 抢救认知状态。

**无 daemon 时**：手动检查 `tmux ls` 和对比 `sessions/*/heartbeat` 时间戳识别死 session。 → [详见](references/stale-session.md)

### 5.4 MCP Reconnection [design]

检测 MCP 工具调用的连接错误并重连。

实现要点：
- 错误模式：grep `ECONNREFUSED|ECONNRESET|EPIPE|MCP.*disconnect|transport.*closed|server.*not.*running`
- 指数退避：`1<<(attempt-1)` 秒 → 1, 2, 4, 8, 16 秒
- 上限 5 次，状态跟踪：`sessions/$SESSION_ID/mcp-retry-$TOOL.json` 含 `{attempt, last_attempt_ts}`
- 超过上限 → 注入 fallback 建议（替代工具或提示用户重启 MCP server）
- Claude Code 没有 MCP restart API，hook 只能建议

**无脚本时**：手动 `npx @anthropic-ai/claude-code mcp restart <server>` 或重启 Claude Code session。 → [详见](references/mcp-reconnection.md)

### 5.5 Graceful Tool Degradation [design]

工具连续失败后自动注入替代工具建议。

实现要点：
- 映射表：`.working-state/fallback-tools.md`（如 `mcp__firecrawl__scrape` → `WebFetch`，注明能力差异）
- PostToolUse hook：regex 检测 `error|ECONNREFUSED|not found|command not found`
- 失败计数：`sessions/$SESSION_ID/fail-count-$TOOL.txt`，连续 2 次失败后查映射表注入降级建议
- 成功使用后重置失败计数

**无脚本时**：工具连续失败 2 次后，agent 应主动尝试替代工具（如 Firecrawl 不可用时用 WebFetch）。 → [详见](references/graceful-degradation.md)

### 5.6 Model Fallback Advisory [design]

模型连续失败时建议升级模型。

实现要点：
- 状态文件：`sessions/$SESSION_ID/failure-tracker.json` 含 `{consecutive_failures, current_model}`
- 阈值：连续 3 次失败触发升级建议（haiku → sonnet → opus），成功后重置计数
- 529 vs 429：429 等一下就好（honoring retry-after），529 需要换模型
- **限制**：StopFailure hook 通过 additionalContext 建议 agent，无法直接切换模型
- Subagent 架构中可实现真正的自动切换：定义 `analyzer-haiku` 和 `analyzer-sonnet` 两个 agent，coordinator 失败后用更高模型的 agent 重试

**无脚本时**：模型连续失败 3 次后，手动在 prompt 中指定 `--model sonnet` 或切换 subagent 的 model 字段。 → [详见](references/model-fallback.md)

### 5.7 Anti-Stampede Retry Asymmetry [design]

前台/后台对 529 的处理刻意不对称。

规则：
- 前台任务遇 529 → 重试最多 3 次，honoring retry-after header
- 后台任务（summary、compaction、async hook）遇 529 → 立即放弃，不重试
- async hook 设 `curl --max-time 5`，超时 exit 0 静默退出

原因：后台任务丢失可容忍，但后台重试会在系统最脆弱的时候叠加负载。 → [详见](references/anti-stampede.md)

## Scripts

| 脚本 | 用途 |
|------|------|
| `rate-limit-recovery.sh` | 扫描 tmux 自动恢复 |

## Workflow

```
1. 检测错误类型（rate limit / crash / MCP disconnect / model failure）
   ⚠ 先查 ralph.json 和 lock 文件判断错误是暂时性还是永久性。
     永久性错误（auth 401/403、PTL）直接上报，不进入重试。

2. 按错误类型选择恢复策略（不同错误码的恢复路径独立，不共享重试计数）
   → rate limit (429): 扫描 tmux pane，二次验证内容后发送 Enter
   → crash: 读取 ralph.json 残留状态，清理过期 lock，从断点恢复
   → MCP disconnect: 指数退避重连，5 次失败后降级到本地工具
   → model failure (529): 3 次失败后建议升级模型或切换 provider

3. 区分前台/后台重试
   前台 session → 执行重试（honors retry-after）
   后台 session → 记录错误后放弃，不重试（anti-stampede）

4. 执行恢复

5. 验证 session 状态（ralph.json 一致、lock 文件已清理、pane 响应正常）
   → 成功 → 恢复执行
   → 失败 → 上报给用户，附带错误类型 + 已尝试的恢复策略 + 失败原因
```

<example>
场景：tmux agent 遇到 429 限速
检测: rate-limit-recovery.sh 执行 `tmux capture-pane -t $pane -p -S -20`
匹配: 输出含 "Rate limited. Press Enter to retry"
二次验证: 重新 capture 最后 5 行，不含 [y/N]、confirm 等确认提示
动作: 发送 Enter 键恢复执行
结果: Agent 从限速中自动恢复，无需人工干预
</example>

<example>
场景：新 session 启动发现上次 crash 残留
检测 1: sessions/abc123/ralph.json active=true，last_checked_at 距今 3 小时（>7200s 阈值）
动作 1: 设 active=false, deactivation_reason="stale"
检测 2: .claims/src_auth.lock 已存在 20 分钟（>15min 阈值）
动作 2: 自动删除过期 lock
检测 3: .working-state/current-plan.md 存在
动作 3: additionalContext 注入"请先读取 .working-state/current-plan.md 恢复上次计划"
</example>

<example>
场景：MCP 工具断连后指数退避重连
触发: agent 调用 mcp__firecrawl__scrape，返回 ECONNREFUSED
重试: 1s → 2s → 4s 间隔重试 3 次（第 3 次成功）
状态: 记录到 sessions/xxx/mcp-retry-firecrawl.json {attempt: 3, last_attempt_ts: ...}
失败路径: 5 次全部失败 → 注入 "[MCP FALLBACK] Firecrawl 失败，可用 WebFetch（不支持 JS 渲染）"
</example>

<anti-example>
错误: 3 个后台 agent 同时遇到 529 过载，全部重试
原因: 后台重试叠加放大服务端压力，529 持续从 2 分钟延长到 15 分钟
正确: 后台 session 应直接放弃（exit 0），只记录日志
规则: 前台重试 + 后台放弃 = anti-stampede 不对称
</anti-example>

## Output

| 输出 | 说明 |
|------|------|
| recovery log entries | 每次恢复操作记录到 `logs/error-recovery.log`，含时间戳、pane、错误类型、执行动作、结果 |
| restored ralph.json | crash 恢复后 ralph.json 状态回到最后一致的 checkpoint，迭代计数器和任务列表保留 |
| cleaned lock files | 清除残留的 `.lock` 文件（如 `ralph.lock`、`session.lock`），防止后续 session 启动被阻塞 |

## Usage

在 `.claude/settings.json` 中配置 hook：

```jsonc
{
  "hooks": {
    // Crash recovery：新 session 启动时扫描残留状态
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash crash-recovery-check.sh"
        }]
      }
    ],
    // MCP 错误追踪 + 工具降级建议
    "PostToolUse": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash error-tracker.sh"
        }]
      }
    ],
    // Stale session heartbeat（async，不阻塞 agent）
    "PostToolUse": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash heartbeat-write.sh",
          "async": true
        }]
      }
    ]
  }
}
```

Hook 输出格式：

Crash recovery 发现残留状态时：
```json
{"decision": "allow", "hookSpecificOutput": {"additionalContext": "[CRASH RECOVERY] 检测到上次 session 残留: ralph.json active=true (stale 3h), 2 个过期 lock 已清理, .working-state/current-plan.md 存在。请先读取 .working-state/current-plan.md 恢复上次计划。"}}
```

MCP 重连失败后的 fallback 建议：
```json
{"decision": "allow", "hookSpecificOutput": {"additionalContext": "[MCP FALLBACK] mcp__firecrawl__scrape 连续失败 5 次 (ECONNREFUSED)。可用替代: WebFetch（不支持 JS 渲染，适合静态页面）。"}}
```

## Related

| Skill | 关系 |
|-------|------|
| `tool-governance` | error-recovery 的错误追踪数据（连续失败次数、错误类型分布）喂给 tool-governance 做工具降级决策 |
| `execution-loop` | Ralph crash 后由 error-recovery 恢复 ralph.json 状态，execution-loop 从断点继续执行 |
| `context-memory` | crash 恢复时 handoff state 由 context-memory 保障跨 session 存活，error-recovery 负责触发 handoff 写入 |
