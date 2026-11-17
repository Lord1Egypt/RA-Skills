# Agent 循环生命周期与事件流（实测 2026-08，555 文档蒸馏）

> 一个 Agent 从收到消息到回复，内部经历 turn → step 的事件序列。**理解这里 = 知道该监听
> 哪个事件介入哪个环节**。来源：`packages/core/agent-loop/src/agent.ts`、`docs/agent-lifecycle.md`。

## 1. turn 与 step（概念）

- **turn** = 零个或多个 step：在第一个输入被 claim 前打开，在"无所欠"时关闭。
- **step** = 一次模型请求 + 它调用的工具，嵌套在 turn 内。

```
turn/start
  ├─ step 1：模型请求 → 工具调用 → 工具结果
  ├─ step 2（工具欠另一次请求 / 有新输入）：再走一遍
  └─ turn/end（无所欠）
```

## 2. 单步事件序列（8 步有序）

```
① claim 输入        inbox.claim(target, turn)
② 组装提示词        ctx.systemPrompt.assemble()（system-prompt/assemble waterfall）
③ agent/pre-step   waterfall：可拒绝(reject)或改写/进入(enter messages) ← 权威决策
④ 进入后           step/start + user/message 落盘
                    agent/request waterfall → llm/stream → assistant/chunk* → assistant/message
⑤ 请求失败         agent/request-error waterfall：retry vs 终止
⑥ 成功            assistant/message 落盘（含 usage + sourceEventSeqs）
⑦ 有工具调用       tool/call → tools/pre-execute → tools/execute → tools/post-execute → tool/result
                    → step/end
⑧ 轮次收尾         tools 欠请求或新输入 → 再 claim 走新 step；
                    否则 agent/turn-stopping（serial，无 next()）→ turn/end
```

## 3. 两大事件域（durable vs live）

| 域 | 事件 | 用途 |
|---|---|---|
| **持久会话事件**（session/event）| `turn/*`, `step/*`, `user/message`, `assistant/*`, `tool/*` | 可回放事实，落盘 |
| **实时扩展点**（agent/*）| inbox, status, pre-step, request, request-error, turn-stopping | 活协调/拦截，不持久 |

**关键**：`agent/pre-step`、`agent/request`、`llm/stream`、三个 `tools/*` 是 **waterfall**（监听者必须 `next()`）；
`agent/turn-stopping` 是 **serial 且无 next()**。

## 4. 扩展点速查（想介入哪里看这里）

| 想做什么 | 监听事件 | 模式 |
|---|---|---|
| 步骤前拦截/改写消息 | `agent/pre-step` | waterfall（reject / enter messages）|
| 修改 LLM 调用配置 | `agent/request` | waterfall |
| 包装/变换 token 流 | `llm/stream` | waterfall |
| 处理请求失败（重试）| `agent/request-error` | waterfall |
| 轮次关闭前钩子 | `agent/turn-stopping` | serial（无 next）|
| 观察轮次结束（自动存储等）| `agent/status`（idle）| emit |
| 工具门禁/审计 | `tools/pre-execute` / `post-execute` | waterfall |

## 5. 事件生产者-消费者矩阵（Event Producer/Consumer Matrix）

> DSH 有自动生成的 `docs/event-producer-consumer.md`，列出每个 harness 事件：模式 / 声明处 /
> 分发包 / 监听包。产出自 `scripts/gen-doc-graphs.ts` 的 `renderEventRelations`（AST 扫描
> `ctx.on/emit/parallel/serial/waterfall` 调用点），并有"每个声明事件必须至少有分发者"的
> **死词汇守卫**（无监听者允许，无分发者报错）。

**用法**（运行时等效，比静态文档更准）：
```
cordis_inspect_query(Event/listEvents, 无 input)          → 事件目录（名+模式+签名）
cordis_inspect_query(Event/listEvents, {event:"agent/pre-step"}) → 精确 payload + 监听器签名
```
（见 [inspect-workflow.md](../10-setup/inspect-workflow.md)）

**典型案例**：`agent/pre-step` 被 agent-instructions、compaction-basic、goal-round-driver、
hooks-claude-code、plan-mode 等多个插件监听——都是"给轮次挂策略"的形态。

## 6. 对插件开发者的意义

1. **选对事件介入点**：拦截用 waterfall（`agent/pre-step`），观察用 emit（`agent/status` idle → 自动存储）。
2. **waterfall 必须 `next()`**：监听 `agent/pre-step` 不委托 = 下游全部跳过（见 events.md waterfall 语义）。
3. **持久 vs 实时**：需要"可回放事实"监听 session/event；需要"进程内协调"用 agent/*。
4. **step 边界语义**：`agent/pre-step` 在 `step/start` 之前触发（有测试断言此顺序）——在轮次开始前注入内容用它。
