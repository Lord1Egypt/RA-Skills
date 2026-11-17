## Hook 与 Tool 之间的数据传递方式——完整图鉴

`_session.id` / `exec.agent.id` 只是身份锚点。系统还有**六条显式数据通路**，每条有自己的语义和流向。

---

### 通路 1：stdin payload → Hook（桥下发）

Bridge 构造 JSON 写入 hook 进程的 stdin。从 [base()](packages/hooks/hooks-claude-code/src/index.ts#L322-L331) 和各事件 payload 函数可以看到完整字段：

| 字段 | 来源 | 含义 |
|---|---|---|
| `session_id` | `agent.session.header.id` | 身份锚点 |
| `transcript_path` | `sessionPersistence.locate()` | 日志文件路径 |
| `cwd` | `agent.session.header.cwd` | 工作目录 |
| `hook_event_name` | 硬编码 | 当前事件类型 |
| `tool_name` | `exec.name` | 触发的工具名 |
| `tool_input` | `exec.arguments` | 工具输入参数 |
| `tool_use_id` | `exec.callId` | 工具调用 ID |

**方向**：Bridge → Hook 进程。Hook 读取这些信息做决策，但不直接"传递"给 tool。

---

### 通路 2：Hook stdout JSON → Bridge（钩回传）

Hook 进程通过 stdout JSON 返回结构化结果。从 [HookOutput](packages/hooks/hook-protocol/src/types.ts#L89-L137) 的完整字段：

| 字段 | 语义 | 下游去向 |
|---|---|---|
| `decision` | `approve`/`block`/`deny`/`ask` | → 映射为 PreToolDecision / PreStepDecision |
| `reason` | 决策理由 | → 伴随 decision 展示给用户或模型 |
| `additionalContext` | 额外上下文文本 | → **注入到下一个模型请求** |
| `continue` | 是否继续运行 | → 控制流程是否中断 |
| `stopReason` | 中断原因 | → 伴随 continue:false |
| `systemMessage` | 用户警告 | → 展示给用户（当前未启用） |
| `updatedInput` | 工具输入改写 | → **当前不生效**，仅记录警告 |

**方向**：Hook 进程 → Bridge → 扩展点决策 / 模型上下文。

---

### 通路 3：additionalContext → 模型上下文（最重要的跨层传递）

这是 hook 向 tool/模型**注入信息**的唯一正式通道。从 [contextFrom()](packages/hooks/hooks-claude-code/src/index.ts#L192-L196)：

```ts
function contextFrom(merged: MergedHookOutcome): UserMessage | undefined {
  if (merged.additionalContext.length === 0) return undefined
  const content: ContentBlock[] = merged.additionalContext.map(text => ({ type: 'text', text }))
  return createUserMessage({ content, source: PLUGIN_SOURCE })
}
```

Merge 后的 `additionalContext` 被包装成 `UserMessage`，注入到 agent 的 inbox。后续的模型请求会读到这段上下文，tool 的执行也可能因此改变行为。

**流转路径**：

```
Hook stdout: { additionalContext: "项目规范：所有文件必须用 UTF-8" }
  → mergeHookOutputs() → merged.additionalContext[]
    → contextFrom() → UserMessage
      → agent.inject() / prependContext()
        → inbox → 下一步模型请求 → tool 执行上下文
```

**这是唯一让 hook 的输出间接影响 tool 行为的通路。**

---

### 通路 4：Decision → 扩展点裁决（权限控制流）

Hook 的 `decision` 经过 [mergeHookOutputs()](packages/hooks/hook-protocol/src/merge.ts#L72-L101) 合并后，由 bridge 映射到具体扩展点的类型化决策：

| Hook 点 | 映射目标 | 效果 |
|---|---|---|
| `PreToolUse` | `PreToolDecision` | `deny` → 拒绝执行, `ask` → 请求确认 |
| `UserPromptSubmit` | `PreStepDecision` | `deny` → `kind: 'reject'` |
| `PostToolUse` | `PostToolDecision` | `deny` → `kind: 'block'` + 反馈 |
| `Stop` | 流程控制 | `deny` → 强制继续（steer） |

合并规则：**deny > ask > allow**，最严格者胜。这是数据传递的一种特殊形式——传递的是**控制信号**而非数据载荷。

---

### 通路 5：Session 事件日志（共享真相源）

Hook 的每次调用都会在 session 日志中追加事件对，从 [runPoint()](packages/hooks/hooks-claude-code/src/index.ts#L157-L183)：

```ts
appendHookInvoked(session, { turn, point, dialect, handlerId, matcher })
// ... 执行 hook ...
appendHookResult(session, { turn, point, handlerId, output, durationMs })
```

Tool 的执行同样追加 `tool/call` 和 `tool/result` 事件。所有消费者（持久化、UI、query）都从同一日志读取。

**方向**：Hook/Tool → 日志 → 任意消费者。这是**发布-订阅**式的间接传递。

---

### 通路 6：Agent.steer() / Agent.inject()（行为注入）

Hook 的输出还能通过两种方式直接改变 agent 的后续行为：

| 方法 | 触发条件 | 效果 |
|---|---|---|
| `agent.inject(context)` | `additionalContext` 非空 | 注入到 `next-step` inbox，**不唤醒**驱动 |
| `agent.steer(message)` | Stop hook `deny` | 注入到 `next-step` inbox，**唤醒**驱动继续运行 |

从 [agent-loop/agent.ts](packages/core/agent-loop/src/agent.ts#L124-L130)：

```ts
steer(input: UserMessage): void {
  this.send(input, 'next-step', true)   // wakeup = true
}
inject(input: UserMessage): void {
  this.send(input, 'next-step', false)  // wakeup = false
}
```

`steer` 是"我命令你继续"，`inject` 是"下次醒来时顺便带上这个"。

---

### 完整数据流图

```
                        stdin payload
  Bridge ──────────────────────────────→ Hook 进程
    │                                      │
    │  agent.session.header.id             │  stdout JSON
    │  exec.name, exec.arguments           │
    │  exec.callId                         │
    │                                      ↓
    │                              ┌──────────────┐
    │                              │  mergeHook   │
    │                              │  Outputs()   │
    │                              └──┬───┬───┬───┘
    │                                 │   │   │
    │         decision ───────────────┘   │   │
    │         → PreToolDecision            │   │
    │         → PreStepDecision            │   │
    │                                     │   │
    │         additionalContext ──────────┘   │
    │         → agent.inject()                │
    │         → 下一个模型请求                  │
    │         → tool 执行上下文                 │
    │                                         │
    │         continue:false ─────────────────┘
    │         → agent.steer() 或 halt
    │
    │  appendHookInvoked / appendHookResult
    └──────────────→ Session 事件日志 ←──────────── Tool 执行
                         │
                    持久化 / UI / Query
```

---

### 速查表

| 通路 | 方向 | 载荷类型 | 是否跨进程 |
|---|---|---|---|
| stdin payload | Bridge → Hook | 身份 + 上下文元数据 | ✅ 跨进程 |
| stdout JSON | Hook → Bridge | decision + context + control | ✅ 跨进程 |
| additionalContext | Hook → 模型 → Tool | 自由文本 | ✅→内 |
| decision | Hook → 扩展点 | 枚举裁决 | ✅→内 |
| session 事件日志 | Hook/Tool → 消费者 | 结构化事件 | 内 |
| steer / inject | Hook → Agent inbox | UserMessage | 内 |

一句话：**身份靠 `_session.id` 定位，控制靠 decision 裁决，信息靠 additionalContext 透传，真相靠事件日志存证，行为靠 steer/inject 驱动。五条通道，各司其职。**

[Tool Execution Pipeline](../30-capability/tool-pipeline.md)
[Capability Seams](seams.md)
[Session Log and Events](agent-lifecycle.md)




## Hook ↔ Tool 数据通路思维导图

```
Hook ↔ Tool 数据传递全景
│
├── 身份锚点（谁在说话）
│   ├── Hook 侧
│   │   ├── 来源: bridge.base() 构造 stdin payload
│   │   ├── 字段: payload.session_id
│   │   ├── 等价: agent.session.header.id
│   │   └── 用途: Hook 用此 key 写外部存储
│   │
│   ├── Tool 侧
│   │   ├── 来源: agent-loop executeToolCalls() 绑定 exec.agent
│   │   ├── 字段: exec.agent.id
│   │   ├── 等价: ctx.agents.requireInitiator().id
│   │   └── 用途: Tool 用此 key 读外部存储
│   │
│   └── 不变式: payload.session_id === exec.agent.id
│       ├── 铸造: 工厂 CreateAgentOptions.sessionId 唯一源头
│       ├── 传播: withInitiator() → AsyncLocalStorage → requireInitiator()
│       ├── 投影: bridge 从 agent.session.header.id 读取，不信任 hook 输出
│       └── 隔离: 子 agent 独立 session，parentSession 记血统但不共享 id
│
├── 通路 1: stdin payload（Bridge → Hook）
│   ├── 构造者: bridge.base() + 事件特有字段
│   ├── 载荷字段
│   │   ├── session_id ← agent.session.header.id
│   │   ├── transcript_path ← sessionPersistence.locate()
│   │   ├── cwd ← agent.session.header.cwd
│   │   ├── hook_event_name ← 当前事件类型硬编码
│   │   ├── tool_name ← exec.name          [PreToolUse/PostToolUse]
│   │   ├── tool_input ← exec.arguments     [PreToolUse/PostToolUse]
│   │   ├── tool_use_id ← exec.callId       [PreToolUse/PostToolUse]
│   │   ├── prompt ← blocksToText(content)  [UserPromptSubmit]
│   │   ├── source ← session 启动来源       [SessionStart]
│   │   └── stop_hook_active ← false        [Stop]
│   ├── 传递方式: JSON 写入 hook 进程 stdin
│   └── 环境变量
│       ├── CLAUDE_PROJECT_DIR ← config.projectDir ?? workdir
│       └── 工作目录 ← agent.session.header.cwd
│
├── 通路 2: stdout JSON（Hook → Bridge）
│   ├── 解析: parseHookOutput(exitCode, stdout, stderr)
│   ├── 结构: HookOutput
│   │   ├── exitCode ← 进程退出码
│   │   ├── stderr ← 阻断原因文本
│   │   ├── stdout ← 原始文本（可能非 JSON）
│   │   ├── decision ∈ {approve, allow, block, deny, ask}
│   │   ├── reason ← 决策理由
│   │   ├── continue ∈ {true, false}  → false = 中断
│   │   ├── stopReason ← 中断原因
│   │   ├── additionalContext ← 额外上下文文本
│   │   ├── systemMessage ← 用户警告
│   │   ├── updatedInput ← 工具输入改写（⚠️ 当前不生效）
│   │   └── hookEventName ← 事件鉴别器
│   └── 合并: mergeHookOutputs() → MergedHookOutcome
│       ├── decision: deny > ask > allow（最严格胜）
│       ├── reason: 同 rank 的理由用 \n\n 拼接
│       ├── stop: 任一 hook continue:false 即 sticky
│       ├── additionalContext: 所有 hook 的按序累积
│       └── systemMessages: 所有 hook 的按序累积
│
├── 通路 3: additionalContext（Hook → 模型 → Tool）
│   ├── 触发: merged.additionalContext 非空
│   ├── 包装: contextFrom() → createUserMessage({ source: { kind: 'plugin' } })
│   ├── 注入路径
│   │   ├── SessionStart → agent.inject(context)  → next-step, 不唤醒
│   │   ├── UserPromptSubmit → prepend 到 downstream.messages
│   │   └── PostToolUse → prepend 到 downstream.additionalContexts
│   ├── 到达 Tool 的路径
│   │   ├── inbox → preStep() → claimed messages
│   │   │   └── 包含 additionalContext 生成的 UserMessage
│   │   ├── systemPrompt.assemble() → runtimeContext.project()
│   │   └── 模型请求 → 模型决策 → tool 调用参数
│   └── 特点: 间接传递，经模型中转，非点对点
│
├── 通路 4: Decision（Hook → 扩展点裁决）
│   ├── 映射表
│   │   ├── PreToolUse
│   │   │   ├── deny  → { kind: 'deny', reason }
│   │   │   ├── ask   → { kind: 'ask', reason }
│   │   │   └── allow → next() 放行
│   │   ├── UserPromptSubmit
│   │   │   ├── deny  → { kind: 'reject' }
│   │   │   └── allow → prepend context + next()
│   │   ├── PostToolUse
│   │   │   ├── deny  → { kind: 'block', feedback, additionalContexts }
│   │   │   └── allow → prepend context + next()
│   │   └── Stop
│   │       └── deny  → agent.steer() 强制继续
│   ├── 合并规则: mergeHookOutputs() 单调最严格
│   └── 效果: 控制流，非数据流
│
├── 通路 5: Session 事件日志（Hook/Tool → 共享真相源）
│   ├── Hook 写入
│   │   ├── hook/invoked: { turn, point, dialect, handlerId, matcher? }
│   │   └── hook/result:  { turn, point, handlerId, decision, exitCode?, durationMs }
│   ├── Tool 写入
│   │   ├── tool/call:   { turn, step, callId, name, arguments }
│   │   └── tool/result: { turn, step, callId, content, isError }
│   ├── 关联: handlerId 配对 invoked/result; callId 配对 call/result
│   └── 消费者
│       ├── 持久化: session/event → sessionPersistence
│       ├── UI 渲染: surface 事件
│       ├── Session Query: SQLite 索引 + 搜索
│       └── 不变式检查: request/header 与 deriveMessages() 一致性
│
├── 通路 6: steer / inject（Hook → Agent 行为注入）
│   ├── agent.inject(message)
│   │   ├── target: 'next-step'
│   │   ├── wakeup: false
│   │   └── 语义: "下次醒来带上，别现在动"
│   ├── agent.steer(message)
│   │   ├── target: 'next-step'
│   │   ├── wakeup: true
│   │   └── 语义: "现在就继续跑，带上这个"
│   └── 触发场景
│       ├── inject ← additionalContext 非空
│       └── steer  ← Stop hook deny（强制继续）
│
└── 不生效 / 保留通路
    ├── updatedInput
    │   ├── 语义: Hook 请求改写 tool 输入参数
    │   ├── 现状: bridge log + warn，不执行
    │   └── 原因: 输入改写延后到 interception extension-points
    │
    ├── systemMessage
    │   ├── 语义: Hook 向用户展示警告
    │   ├── 现状: bridge log + warn，不展示
    │   └── 原因: 展示机制尚未实现
    │
    └── continue:false（run-level halt）
        ├── 语义: 请求终止整个运行
        ├── 现状: merged.stop 记录但未执行
        └── 原因: 缺少 run-level halt 机制（TODO）
```

一句话：**六条通路，三种流向——跨进程靠 stdin/stdout，跨时间靠事件日志，跨层级靠 additionalContext 经模型中转。**

[Tool Execution Pipeline](../30-capability/tool-pipeline.md)
[Capability Seams](seams.md)
[Cordis Waterfall Dispatch](events.md)



## 六条通路的实现原理与逻辑

---

### 通路 1：stdin payload（Bridge → Hook）

**原理**：Bridge 是可信的内部代码，Hook 是不受信的外部进程。唯一安全的传递方式是将数据序列化后写入进程 stdin——进程隔离保证了 Hook 无法回写篡改。

**实现逻辑**（[hooks-claude-code/index.ts](packages/hooks/hooks-claude-code/src/index.ts#L322-L347)）：

```
1. base(ctx, agent, event) 构造公共字段
   ├─ session_id ← agent?.session.header.id   // 身份锚点，永远从 agent 引用读
   ├─ transcript_path ← sessionPersistence.locate()  // 日志路径
   ├─ cwd ← agent?.session.header.cwd         // 工作目录
   └─ hook_event_name ← event                 // 事件类型

2. 事件特有字段叠加在 base 上
   ├─ PreToolUse: + tool_name, tool_input, tool_use_id
   ├─ UserPromptSubmit: + prompt
   ├─ SessionStart: + source
   └─ Stop: + stop_hook_active

3. runHook() 将 payload JSON.stringify 后写入 stdin
   ├─ shell.run({ command, stdin: JSON.stringify(payload), timeoutMs, env, workdir })
   └─ trailing newline: CC 需要 \n，Codex 不需要
```

**关键设计**：Bridge **从不信任 Hook 的输出中的身份信息**，`session_id` 的来源始终是 `agent.session.header.id`，单向写入，不可逆向影响。

---

### 通路 2：stdout JSON 解码（Hook → Bridge）

**原理**：Hook 通过 stdout 返回结构化结果，但 stdout 是一个原始字节流——可能不是 JSON，可能是畸形 JSON。解码器必须**全量**（total）：任何输入都产生合法的 `HookOutput`，永不抛异常。

**实现逻辑**（[hook-protocol/codec.ts](packages/hooks/hook-protocol/src/codec.ts#L67-L97)）：

```
parseHookOutput(exitCode, stdout, stderr, expectedEventName):
│
├─ exit 2 → 阻断型
│   ├─ decision = 'block'
│   └─ reason = stderr.trim()  // stderr 就是阻断理由
│
├─ exit 0 + stdout 以 '{' 开头 → 尝试 JSON 解析
│   ├─ 解析成功 → applyStructured()
│   │   ├─ 顶层字段: continue, stopReason, systemMessage
│   │   ├─ 顶层 decision: 仅接受 'approve'/'block'（传统通道）
│   │   └─ hookSpecificOutput: 事件作用域字段
│   │       ├─ hookEventName 门卫: 不匹配 expectedEventName → 丢弃事件作用域字段
│   │       ├─ permissionDecision: 'allow'/'deny'/'ask'（覆盖顶层 decision）
│   │       ├─ additionalContext
│   │       └─ updatedInput
│   └─ 解析失败 → 保留 plain stdout，无结构化字段
│
├─ exit 0 + stdout 非 JSON → plain text，无 decision
│
└─ 其他 exit / undefined → 非阻断错误，无 decision，无 exitCode
```

**两通道合并规则**：顶层 `decision`（approve/block）和 `hookSpecificOutput.permissionDecision`（allow/deny/ask）是**两条独立通道**，permissionDecision **覆盖**顶层 decision。这防止了 `{"decision":"approve", "hookSpecificOutput":{"permissionDecision":"deny"}}` 的歧义——deny 胜出。

---

### 通路 3：additionalContext（Hook → 模型 → Tool）

**原理**：Hook 是外部进程，Tool 是内部函数，它们之间没有直接调用关系。唯一让 Hook 的输出影响 Tool 行为的方式是**修改模型看到的上下文**——模型据此调整决策，间接改变 Tool 的调用参数。

**实现逻辑**（[hooks-claude-code/index.ts](packages/hooks/hooks-claude-code/src/index.ts#L192-L234)）：

```
1. 多个 Hook 的 additionalContext 在 mergeHookOutputs() 中按序累积
   → merged.additionalContext: string[]

2. contextFrom(merged) 将字符串数组包装为 UserMessage
   → content: merged.additionalContext.map(text => ({ type: 'text', text }))
   → source: { kind: 'plugin', plugin: 'hooks-claude-code' }

3. 不同事件点的注入方式不同：
   ├─ SessionStart: agent.inject(context)
   │   └─ send(target='next-step', wakeup=false)  // 不唤醒，等下次自然触发
   ├─ UserPromptSubmit: prepend 到 downstream.messages
   │   └─ return { kind: 'enter', messages: [...downstream.messages, ours] }
   └─ PostToolUse: prepend 到 downstream.additionalContexts
       └─ return { ...downstream, additionalContexts: [ours, ...theirs] }

4. 到达 Tool 的完整路径：
   inject/inbox → preStep() → claimed messages
     → systemPrompt.assemble() → runtimeContext.project()
       → 模型请求 context → 模型决策 → tool call arguments
```

**关键特征**：这是**间接传递**，经模型中转。Hook 不能直接告诉 Tool "做什么"，只能告诉模型"考虑这个"，由模型决定如何影响 Tool。这是架构上的有意限制——Hook 不应有 Tool 的直接控制权。

---

### 通路 4：Decision 裁决（Hook → 扩展点 → 控制流）

**原理**：Cordis 事件系统使用 **waterfall** 分发模式——监听器按注册顺序依次执行，每个监听器可以**委托**（delegate）给下游（`next()`），也可以**短路**（不调 `next()`）。Hook bridge 把 merged decision 映射到类型化的扩展点决策，插入 waterfall 链。

**实现逻辑**（[hooks-claude-code/index.ts](packages/hooks/hooks-claude-code/src/index.ts#L238-L277)）：

```
PreToolUse 瀑布:
  ctx.on('tools/pre-execute', async (exec, next) => {
    1. 从 exec.agent 取 turn
    2. runPoint('PreToolUse', exec.name, payload, { agent, turn, signal })
    3. mergeHookOutputs() → merged
    4. 映射:
       ├─ merged.decision === 'deny' → return { kind: 'deny', reason }  // 短路，不调 next()
       ├─ merged.decision === 'ask'  → return { kind: 'ask', reason }   // 短路
       └─ 否则 → return next()                                        // 委托给下游
    5. additionalContext 总是注入（即使 deny 也能携带上下文）
  })

PostToolUse 瀑布:
  ctx.on('tools/post-execute', async (exec, result, next) => {
    1. runPoint('PostToolUse', ...) → merged
    2. 映射:
       ├─ merged.decision === 'deny'
       │   → return { kind: 'block', feedback: [...], additionalContexts: [...] }
       └─ 否则 → downstream = next()
           → return { ...downstream, additionalContexts: prependContext(ours, theirs) }
  })

Stop 瀑布:
  ctx.on('agent/turn-stopping', async ({ agent, turn, signal }) => {
    1. runPoint('Stop', ...) → merged
    2. merged.decision === 'deny'
       → agent.steer(message)  // 强制继续：注入唤醒消息
  })
```

**合并逻辑**（[merge.ts](packages/hooks/hook-protocol/src/merge.ts#L72-L101)）：

```
mergeHookOutputs(outputs):
  rank: deny=3, ask=2, allow=1, none=0
  遍历所有 HookOutput:
    ├─ maxRank = max(rank(output.decision))      // 最严格胜
    ├─ stop = ∃(output.continue === false)        // 任一 halt 即 sticky
    ├─ reasonsByRank: 同 rank 的理由按序收集       // 只有胜出 rank 的理由展示
    ├─ additionalContext: 所有 hook 的按序累积     // 不分胜负，全部保留
    └─ systemMessages: 所有 hook 的按序累积
```

**单调性**：deny 一旦出现，后续 allow 无法降级。这是**单调拒绝不变式**——权限只能收紧，不能放松。

---

### 通路 5：Session 事件日志（发布-订阅共享真相源）

**原理**：Session 日志是 append-only 的事件流。Hook 和 Tool 各自追加事件，消费者通过遍历事件流读取。这是 **CQRS** 的变体——写入和读取解耦，通过持久化事件流关联。

**实现逻辑**（[hook-protocol/events.ts](packages/hooks/hook-protocol/src/events.ts#L58-L105)）：

```
Hook 调用期间追加事件对:

  appendHookInvoked(session, { turn, point, dialect, handlerId, matcher? })
    → session.append('hook/invoked', payload)

  [执行 hook 进程]

  appendHookResult(session, { turn, point, handlerId, output, durationMs })
    → session.append('hook/result', {
        turn, point, handlerId,
        decision: output.decision ?? (output.continue === false ? 'stop' : 'pass'),
        exitCode?,              // 仅在 exitCode !== undefined 时记录
        stderrSummary?,         // trim + cap at stderrSummaryMaxChars + '…'
        durationMs,
      })

Tool 执行期间追加事件对:

  appendToolCall(session, { turn, step, callId, name, arguments })
    → session.append('tool/call', ...)

  appendToolResult(session, { turn, step, callId, content, isError })
    → session.append('tool/result', ...)
```

**stderr 截断**：`summarizeStderr()` 将 stderr trim 后截断到 `stderrSummaryMaxChars`（默认 500 字符），超出部分用 `…` 标记。这是**有界持久化**——防止恶意/故障 hook 喷涌 stderr 撑爆存储。

**消费者**：
- `session/event` → 持久化插件写入磁盘
- `deriveMessages()` → 从事件流重构 LLM 请求上下文
- UI 订阅 surface 事件渲染界面
- Session Query 建立搜索索引

---

### 通路 6：steer / inject（Hook → Agent 行为注入）

**原理**：Agent 的 inbox 是两个有序队列（`next-turn` 和 `next-step`）。Hook 通过往 inbox 插入消息来改变 agent 的后续行为。**唤醒标志**（wakeup）决定是"下次自然触发时带上"还是"现在就启动驱动"。

**实现逻辑**（[agent-loop/agent.ts](packages/core/agent-loop/src/agent.ts#L117-L130)）：

```
agent.send(message, target, wakeup):
  ├─ 判断是否为 abort 后的唤醒输入
  │   → wakingAfterAbort = wakeup && phase !== 'idle' && signal.aborted
  ├─ 确定目标队列
  │   → resolvedTarget = wakingAfterAbort ? 'next-turn' : target
  ├─ 插入消息
  │   → inbox.splice(resolvedTarget, Infinity, 0, [message])
  └─ 唤醒（如果需要）
      → wakeup && wakeDriver(wakingAfterAbort)

agent.inject(message):
  → send(message, 'next-step', wakeup=false)
  // 语义: "塞进 next-step 队列，不触发驱动"
  // 使用场景: SessionStart hook 注入上下文——agent 即将自然启动，无需额外唤醒

agent.steer(message):
  → send(message, 'next-step', wakeup=true)
  // 语义: "塞进 next-step 队列，立即唤醒驱动"
  // 使用场景: Stop hook deny——agent 已停下，必须强制唤醒才能继续

wakeDriver():
  ├─ phase === 'idle' → 启动新驱动
  │   → setPhase({ kind: 'running', ... })
  │   → ctx.agents.withInitiator(this, () => this.kick())
  └─ phase !== 'idle' → 锁存 wakeRequested = true
      → 等当前活动结束后重播唤醒
```

**wakeup 的微妙之处**：`inject` 不唤醒是因为注入发生在 agent **即将运行**的路径上（如 SessionStart → 自然进入首个 turn），多一次唤醒是冗余且危险的。`steer` 必须唤醒是因为注入发生在 agent **已经停下**的路径上（如 turn-stopping），不唤醒就没人消费这条消息。

---

### 完整调用时序

```
模型输出 tool call
  │
  ├─ Cordis waterfall: 'tools/pre-execute'
  │   │
  │   ├─ Bridge 收到 exec (含 exec.agent, exec.name, exec.arguments, exec.callId)
  │   │
  │   ├─ base(ctx, exec.agent, 'PreToolUse')  → payload 含 session_id
  │   │
  │   ├─ matchesMatcher(group.matcher, exec.name, 'claude-code')
  │   │   → 匹配的 hook 才执行
  │   │
  │   ├─ appendHookInvoked(session, ...)       → 事件日志: hook/invoked
  │   │
  │   ├─ runHook(shell, hook, { payload, ... })
  │   │   ├─ JSON.stringify(payload) → stdin
  │   │   ├─ shell.run({ command, stdin, timeoutMs, env, workdir })
  │   │   ├─ hook 进程执行，写 stdout/stderr
  │   │   └─ parseHookOutput(exitCode, stdout, stderr)
  │   │       → HookOutput
  │   │
  │   ├─ appendHookResult(session, ...)        → 事件日志: hook/result
  │   │
  │   ├─ mergeHookOutputs(all outputs)         → MergedHookOutcome
  │   │
  │   └─ 映射到 PreToolDecision
  │       ├─ deny → return { kind: 'deny', reason }  ← 短路
  │       └─ allow → contextFrom(merged) → prependContext → next()
  │
  ├─ [如果放行] executeToolCalls(ctx, turn, step, toolCalls, signal)
  │   ├─ agent = ctx.agents.requireInitiator()
  │   ├─ exec = { callId, name, arguments, agent, signal }
  │   ├─ ctx.tools.dispatch(exec) → ToolResult
  │   └─ appendToolCall / appendToolResult  → 事件日志
  │
  ├─ Cordis waterfall: 'tools/post-execute'
  │   └─ [同 PreToolUse 模式，映射到 PostToolDecision]
  │
  └─ turn-stopping 检查
      └─ Stop hook: deny → agent.steer() → 继续运行
```

一句话：**stdin 序列化跨进程边界，codec 全量解码容错畸形输出，merge 单调最严格合并，waterfall 短路或委托，additionalContext 经模型间接透传，steer/inject 差异仅在唤醒标志。每条通路的选择都不是随意的——进程隔离、容错性、单调性、间接性、唤醒语义——各有其不可替代的工程理由。**

[Tool Execution Pipeline](../30-capability/tool-pipeline.md)
[Capability Seams](seams.md)
<!-- 防御性模式（待补充） -->