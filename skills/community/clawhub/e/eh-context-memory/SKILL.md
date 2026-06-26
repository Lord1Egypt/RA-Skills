---
name: context-memory
version: 2.0.0
description: 上下文窗口管理与跨 session 知识传递。当需要跨阶段传递决策、压缩前抢救知识时使用。不适用于工具重试（用 tool-governance）或多 agent 协调（用 multi-agent）。参见 execution-loop（阶段边界）。
license: MIT
triggers:
  - context management
  - 上下文管理
  - handoff document
  - compaction
  - token budget
  - memory consolidation
  - context estimation
author: OpenClaw Team
---

# Context & Memory

上下文窗口生命周期管理：跨阶段知识传递、压缩前知识抢救、token 预算。

## When to Use

- 多阶段任务跨阶段传递决策 → Handoff documents
- 即将压缩需要保存知识 → Compaction memory extraction
- 需要监控 context 使用率 → Context budget estimation

## When NOT to Use

- Agent 提前停止 → 用 `execution-loop`
- 多 agent 协调 → 用 `multi-agent`

---

## Patterns

### 3.1 Handoff 文档 [design]

阶段结束或压缩前，将五段结构写入 `sessions/<session-id>/handoffs/stage-N.md`：

```markdown
## Decided
- 选用 Redis Cluster 6 节点，hash slot 自动分片

## Rejected
- Codis（社区停更，Proxy 延迟 +2ms）
- Sentinel（不支持分片，只做主从故障转移）

## Risks
- 节点间 gossip 协议在跨机房部署时延迟可能超过心跳超时

## Files Modified
- config/redis.yaml, src/cache/cluster.ts

## Remaining
- 压测 6 节点写入 QPS 是否满足峰值要求
```

五段缺一不可。压缩摘要由 LLM 决定保留什么，handoff 由你决定——信息在磁盘上，任何级别的 compact 都不会丢失。注入方式：下个 agent prompt 中加 `once: true` 引用此文件。 → [详见](references/handoff-documents.md)

### 3.2 Compaction 前记忆提取 [script]

Claude Code 没有 PreCompact hook。通过 Stop hook 每 N 轮（`COMPACTION_EXTRACT_INTERVAL` 环境变量，默认 15 轮）定期快照关键决策到磁盘。

与 handoff 互补：handoff 是计划内的阶段传递，compaction 提取是应急的自动抢救。Claude Code 内部 4 级 compaction：MicroCompact（10-50K tokens，免费）、Session Memory（60-80%，免费）、Full Compact（80-95%，1 次 API 调用）、Reactive Compact（413 触发，紧急）。 → [详见](references/compaction-extract.md)

### 3.3 三门控记忆合并 [design]

跨 session 积累的 handoff 文件会碎片化、重复、矛盾。三门控按计算成本从低到高排列，任一失败即跳过：

1. **Time gate**: 距上次合并 >= 24 小时
2. **Session gate**: 累积 >= 5 个新 session 的 handoff
3. **FileLock gate**: 获取文件锁（10 次重试，5-100ms 指数退避）

通过后合并逻辑：按时间排序所有 handoff，提取 Decided/Rejected，去重，后来的决策覆盖早期的（如 stage-3 否决了 stage-1 选的方案，以 stage-3 为准）。 → [详见](references/memory-consolidation.md)

### 3.4 Token 预算分配 [design]

UserPromptSubmit hook 估算 context 使用量，按阈值梯度注入行为指令（基于 200K window）：

| Context 使用率 | 行为指令 |
|---------------|----------|
| < 40% | 自由读取文件 |
| 40-60% | 警告，优先使用 grep |
| 60-80% | 优先 grep/subagent，避免读大文件 |
| 80-95% | 必须使用 subagent，禁止直接读文件 |
| >= 95% | 必须允许 agent 停止（否则 context 溢出崩溃） |

Hook 输出格式：`{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"[CONTEXT BUDGET] 当前 ~150K/200K (75%), 优先用 grep 和 subagent"}}`。

前半段消耗过多 context 导致后半段被迫压缩是常见失败模式。 → [详见](references/token-budget.md)

### 3.5 Context Token 估算 [script]

从 transcript JSONL 尾行提取 token 数：`tail -1 "$TRANSCRIPT" | jq -r '.usage.input_tokens // empty'`。

关键限制：
- transcript 不暴露 `context_window_size`（该字段仅通过 statusLine stdin pipe 提供给 HUD），只能拿原始 token 数
- 需过滤 stream placeholder 行（`input_tokens <= 10`）
- 阈值判断基于 200K window 假设
- 精度粗略：bytes/4 估算可偏差 20-30%，Claude Code 内部用 `Math.ceil(totalTokens * (4/3))` 做 33% padding

→ [详见](references/context-usage.md)

### 3.6 文件系统作工作记忆 [design]

`.working-state/` 目录下两个核心文件：

- `current-plan.md` — 当前计划，随时覆写更新
- `decisions.jsonl` — 决策日志，append-only，每行一个 JSON：

```json
{"ts": "2025-03-15T10:30:00Z", "decision": "选用 Redis Cluster", "reason": "需要分片能力", "alternatives": ["Codis", "Sentinel"]}
```

compact 或 crash 后 agent 读这两个文件恢复状态。需要在 prompt 中明确要求 agent 写入。恢复指令："read `.working-state/current-plan.md` and `.working-state/decisions.jsonl` first"。 → [详见](references/filesystem-working-memory.md)

### 3.7 Compaction 质量审计 [design]

compact 后对照 `decisions.jsonl` 检查 compact summary 中是否保留了关键决策：

1. 读 `decisions.jsonl` 最近 5 条，提取关键词
2. grep compact summary（`tail -c 4096 "$TRANSCRIPT"`）查这些关键词
3. 缺失 → 注入：`{"decision":"allow","hookSpecificOutput":{"additionalContext":"[COMPACT AUDIT] 以下决策在压缩中丢失: ..."}}`

关键词匹配是粗糙近似。漏检代价（方向倒退）远大于误检代价（多注入几条）。 → [详见](references/compaction-quality-audit.md)

### 3.8 Auto-Compact 断路器 [design]

`MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3`。连续 3 次 auto-compact 失败后停止尝试，等 Reactive Compact（API 413 触发）兜底。

递归保护：如果 compact 来源是 `'session_memory'`、`'compact'` 或 `'marble_origami'`，跳过 auto-compact。历史数据：1,279 个 session 出现 50+ 次连续失败，浪费约 250K API 调用/天。hook 开发者需处理 circuit breaker 跳过的情况。 → [详见](references/auto-compact-circuit-breaker.md)

## Scripts

| 脚本 | 用途 |
|------|------|
| `context-usage.sh <transcript>` | 从 transcript 尾行提取 input_tokens（原始数，非百分比） |
| `compaction-extract.sh` | Stop hook 定期触发，提取关键决策到 handoff |

## Workflow

```
阶段结束？
  → 写 handoff（Decided/Rejected/Risks/Files/Remaining 五段，缺一不可）
  → 不确定是否阶段边界？查任务清单或问用户

Context > 80%？
  → 运行 compaction-extract.sh 抢救关键决策到磁盘
  → 注入预算指令：禁止读大文件，委托 subagent

Compact 刚发生？
  → 审计存活：对照 decisions.jsonl 检查 compact summary
  → 发现遗失 → 自动注入缺失决策
  → 连续失败 3 次 → circuit breaker 生效，等 Reactive Compact 兜底
```

<example>
场景: Handoff 保护决策不丢失
任务: 20 轮 Redis 方案讨论
第 16 轮: 定方案 Redis Cluster 6 节点，否决 Codis（社区停更）和 Sentinel（不支持分片）
第 17 轮: 写 handoff 到 sessions/xxx/handoffs/stage-2.md（Decided/Rejected/Risks/Files/Remaining 五段）
第 20 轮: Full Compact 截断 context
结果: Compact 后 agent 读 stage-2.md，恢复全部决策，不会重提 Codis
</example>

<example>
场景: Compaction 质量审计发现决策丢失
前提: decisions.jsonl 最近 5 条含 "Redis Cluster"、"Codis"、"Sentinel"
触发: Full Compact 后审计 hook 启动
检测: grep compact summary（tail -c 4096），"Codis" 未出现
动作: 注入 additionalContext "[COMPACT AUDIT] 丢失决策: 否决 Codis（社区停更，Proxy +2ms）"
结果: Agent 读到注入信息，不会再提议 Codis
</example>

<example>
场景: Token 预算阻止 context 溢出
状态: 第 30 轮，UserPromptSubmit hook 检测 input_tokens = 170K
计算: 170K / 200K = 85%，超过 80% 阈值
注入: "[CONTEXT BUDGET] 85%, 必须使用 subagent，禁止直接读大文件"
结果: Agent 切换 subagent 委派，避免第 35 轮溢出触发紧急 Reactive Compact
</example>

<anti-example>
同样 20 轮讨论，没写 handoff。第 20 轮 Compact 后 agent 丢失 Codis 被否决的原因，重新提议"考虑 Codis？"。用户花 3 轮重复解释——浪费 token，决策质量倒退。
</anti-example>

## Output

| 产物 | 路径 | 说明 |
|------|------|------|
| 阶段 handoff 文件 | `sessions/xxx/handoffs/stage-N.md` | 每个阶段边界写一份，包含 Decided/Rejected/Risks/Files/Remaining |
| 压缩抢救文件 | `compaction-extract.json` | 压缩前自动提取的关键决策和否决记录 |
| context 使用率估算 | `context-usage.sh` 输出 | 当前 token 占比、预警阈值、剩余容量估算 |

## Usage

在 `.claude/settings.json` 中配置 hook：

```jsonc
{
  "hooks": {
    // Token 预算注入（Pattern 3.4）
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash context-usage.sh \"$TRANSCRIPT_PATH\""
        }]
      }
    ],
    // 定期快照关键决策（Pattern 3.2）
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash compaction-extract.sh",
          "async": true
        }]
      }
    ]
  }
}
```

`context-usage.sh` 输出格式：
```json
{"decision": "allow", "hookSpecificOutput": {"additionalContext": "[CONTEXT BUDGET] ~150K/200K (75%). 优先用 grep 和 subagent，避免直接读大文件。"}}
```

`compaction-extract.sh` 每 15 轮触发一次（`COMPACTION_EXTRACT_INTERVAL` 环境变量控制），将 `decisions.jsonl` 最近条目写入 handoff 文件。

## Related

- `execution-loop` — 阶段边界信号触发 handoff 写入（Pattern 1.4 task completion 完成时即为阶段边界）
- `multi-agent` — 跨 agent 任务交接时，handoff 文件作为知识传递载体（替代口头 context 传递）
- `error-recovery` — crash 恢复时读取最近的 handoff 文件重建进度（Pattern 5.2 crash state recovery）
