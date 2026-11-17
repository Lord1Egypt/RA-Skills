## Hook 用 `_session.id` 写，工具用 `exec.agent.id` 读——同一实体，两个身份入口

这是 deepseek-harness 中一条关键的**身份接缝（identity seam）**模式。Hook 和 Tool 操作的是同一个逻辑实体（一次 agent 会话），但它们处于系统的不同层级，拿到身份的路径也不同。

---

### Hook 侧：`_session.id` 写数据

Hook 是**外部进程**——一个由 bridge（如 `hooks-claude-code`）fork 出来的 shell 命令。它不在 Cordis 上下文内运行，没有 `ctx`，没有 `agent` 对象。它唯一能拿到的身份信息就是 bridge 通过 **stdin payload** 传进来的数据。

在 [hooks-claude-code/index.ts](packages/hooks/hooks-claude-code/src/index.ts#L131-L146) 中，bridge 构造 payload 并调用 `runHook`：

```ts
const { output, durationMs } = await runHook(ctx.shell, hook, {
  payload,          // ← bridge 构建，包含 session 信息
  ...
})
```

Hook 进程从 stdin JSON 里读到 `_session.id`（session 的唯一标识），用这个 ID 作为 key 把数据写到外部存储（文件、数据库、共享内存等）。这是 hook **唯一靠谱的身份锚点**——它是个隔离进程，别的东西它都摸不到。

---

### Tool 侧：`exec.agent.id` 读数据

Tool 是**内部函数**——运行在 Cordis 上下文里，由 agent-loop 调度。在 [tool-calls.ts](packages/core/agent-loop/src/tool-calls.ts#L72-L82) 中可以看到：

```ts
const agent = ctx.agents.requireInitiator()
const { session } = agent

const exec = {
  callId: block.id,
  name: block.name,
  arguments: parseArguments(block.arguments),
  agent,    // ← agent 引用直接挂在执行上下文上
  signal,
}
```

Tool 的执行上下文 `exec` 携带了完整的 `agent` 对象引用。通过 `exec.agent.id` 可以拿到 agent 的身份标识，再以此去**读取** hook 之前用 `_session.id` 写入的数据。

---

### 为什么是两个不同的路径？

| | Hook | Tool |
|---|---|---|
| **运行环境** | 外部 shell 进程（隔离） | Cordis 上下文内（内部函数） |
| **身份来源** | stdin JSON payload（`_session.id`） | 执行上下文对象（`exec.agent.id`） |
| **操作方向** | 写（往外部存储写数据） | 读（从外部存储读数据） |
| **本质** | 跨越进程边界的身份锚 | 内存内直接引用 |

这不是 bug，是**架构设计**：Hook 在系统边界之外，只能通过序列化的 payload 拿到身份；Tool 在系统内部，直接持有对象引用。两个 ID 在语义上指向同一个实体，只是获取方式反映了各自所在层级的能力差异。

---

### 实际流转示意

```
Hook (外部进程)
  ↓ stdin JSON { _session.id: "abc123", ... }
  ↓ 用 "abc123" 作为 key → 写入 Store

      〰〰〰  共享存储  〰〰〰

Tool (内部函数)
  ↓ exec.agent.id → "abc123"  (同一标识)
  ↓ 用 "abc123" 作为 key → 从 Store 读取
```

关键不变式：`_session.id === exec.agent.id`，bridge 和 agent-loop 共同维护这个等式。

---

如果想更深入理解这套身份体系如何嵌入到更大的接缝架构中，可以看看 [Capability Seams](seams.md) 和 [Tool Execution Pipeline](../30-capability/tool-pipeline.md)。

[Capability Seams](seams.md)
[Tool Execution Pipeline](../30-capability/tool-pipeline.md)
[Agent Loop and Turn Flow](agent-lifecycle.md)

---

### 实战案例：身份断裂导致数据读取不到

> 来源：DSH-Context-Pro 项目实测，2026-08-19

**问题**：`insightEngine` 插件用 `_session.id` 存储洞察数据，但 `get_insights` 工具用 `exec.agent.id` 读取——两者不相等，导致读取不到数据。888.md 架构文档保证 `agent.id === session.header.id`，但实际运行时出现偏差。

**根因**：`ToolExecutionInput.agent` 是**可选字段**（`agent?: Agent`），agent-loop 正常路径虽传入，但某些边缘路径（如非 agent 上下文调用 tool、或 agent 对象被代理包装）可能导致 `exec.agent.id` 与 `session.id` 不同。

**修复模式**：获取当前会话 ID 时，优先走 `agent.session.id`（与 `session/event` 同一来源），再回退到 `agent.id`：

```ts
// 工具执行上下文中获取 session ID
const sessionId = String(exec.agent?.session?.id ?? exec.agent?.id ?? 'unknown')
//                       ↑ 优先：走 Session 对象，与 session/event 一致
//                                    ↑ 回退：走 Agent 对象（888.md 保证相等）
```

**身份获取优先级**（从高到低）：
1. `agent.session.id`（推荐，与 session/event 同一来源）
2. `agent.id`（888.md 保证相等，但可能因边缘路径不可用）
3. `'unknown'`（兜底）


## Bridge 和 Agent-Loop 如何共同维护 `_session.id === exec.agent.id`

核心原则：**身份只诞生一次，两个路径只是同一真理的不同投影。**

---

### 第一步：工厂铸造——身份的唯一源头

在 [AgentRegistry.createAgent()](packages/core/agent/src/index.ts#L197-L202) 中，调用者传入 `CreateAgentOptions.sessionId`，工厂用这**一个值**同时创建 agent 和 session：

```
sessionId  ──┬──→  agent.id = sessionId
              │
              └──→  session.header.id = sessionId
```

从出生起，`agent.id` 和 `session.header.id` 就是同一个字符串。没有第二条路径能赋予它们不同的值。

---

### 第二步：Agent-Loop 守护——把 agent 绑进执行上下文

在 [ReactLoopAgent 构造函数](packages/core/agent-loop/src/agent.ts#L88-L99) 中：

```ts
constructor(
  private loopCtx: Context,
  public readonly id: SessionId,      // ← 工厂传入的 sessionId
  public readonly session: Session,    // ← 工厂创建的 session，header.id === id
) {
  this.ctx = this.scope.ctx.extend({ agent: this })  // ← 把自己挂到上下文
}
```

然后在 [executeToolCalls()](packages/core/agent-loop/src/tool-calls.ts#L72-L82) 中：

```ts
const agent = ctx.agents.requireInitiator()  // ← 从 async context 取出当前 agent
const { session } = agent                     // ← agent.session，header.id === agent.id

const exec = {
  callId: block.id,
  name: block.name,
  arguments: parseArguments(block.arguments),
  agent,    // ← 同一个 agent 对象引用
  signal,
}
```

关键：`ctx.agents.requireInitiator()` 返回的是通过 [withInitiator()](packages/core/agent/src/index.ts#L341-L343) 设置进 `AsyncLocalStorage` 的那个 agent 实例。而 `withInitiator` 在 [wakeDriver()](packages/core/agent-loop/src/agent.ts#L168-L180) 中被调用：

```ts
this.loopCtx.agents.withInitiator(this, () => this.kick())
```

`this` 就是构造时绑定了 `id` 和 `session` 的那个 `ReactLoopAgent`。整条驱动链——turn → step → executeToolCalls——都在这个 `withInitiator` 边界内运行，所以 `requireInitiator()` 永远返回同一个 agent。

**Tool 侧的不变式**：`exec.agent.id === exec.agent.session.header.id`，由构造函数保证。

---

### 第三步：Bridge 读取——从同一个 agent 取出同一个 id

在 [hooks-claude-code/index.ts](packages/hooks/hooks-claude-code/src/index.ts#L322-L331) 中，`base()` 函数构建 hook 的 stdin payload：

```ts
function base(ctx: Context, agent: Agent | undefined, event: string): Record<string, unknown> {
  return {
    session_id: agent?.session.header.id ?? '',   // ← 从 agent.session.header.id 读取
    transcript_path: ...,
    cwd: agent?.session.header.cwd ?? process.cwd(),
    hook_event_name: event,
  }
}
```

而 bridge 在每个扩展点拿到的 `agent` 参数从哪来？从 Cordis 事件回调里来。以 PreToolUse 为例：

```ts
ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
  const turn = lastTurn(exec.agent)
  const merged = await runPoint('PreToolUse', exec.name,
    preToolPayload(ctx, exec),          // ← preToolPayload 调用 base(ctx, exec.agent, ...)
    { ...exec.agent ? { agent: exec.agent } : {}, turn, signal: exec.signal })
  ...
})
```

`exec.agent` —— 正是 agent-loop 在 `executeToolCalls` 中绑定的那个 agent。

所以 bridge 的 `base()` 读到的 `agent.session.header.id` 就是工厂铸造的那个 `sessionId`。

**Hook 侧的不变式**：payload 中的 `session_id` === `agent.session.header.id` === `agent.id`。

---

### 全链路图

```
工厂: CreateAgentOptions.sessionId = "abc123"
  │
  ├─→ agent.id = "abc123"
  ├─→ session.header.id = "abc123"
  │
  ├─→ Agent-Loop: withInitiator(agent)
  │     │
  │     ├─→ Tool 侧: exec.agent = agent
  │     │     exec.agent.id ──────────────────→ "abc123"
  │     │
  │     └─→ Bridge 侧: Cordis 事件回调收到同一个 agent
  │           base() 读 agent.session.header.id ─→ "abc123"
  │           payload.session_id ──────────────→ "abc123"
  │
  └─→ 不变式: payload.session_id === exec.agent.id ✓
```

---

### 为什么不会出问题？

| 威胁 | 防御 |
|---|---|
| agent.id 和 session.header.id 不一致 | 工厂是唯一入口，两者在创建时绑定，之后都是 `readonly` |
| Tool 拿到错误的 agent | `withInitiator()` 通过 `AsyncLocalStorage` 传播，整条驱动链在同一边界内 |
| Bridge 拿到错误的 agent | Cordis 事件系统把 `exec.agent` 透传给 bridge 回调，不存在二次查找 |
| Session 被替换 | `agent.session` 是 `readonly` 属性，构造后不可变 |

一句话总结：**工厂铸造身份，agent-loop 传播引用，bridge 从引用中投影。三步没有复制，只有透传——所以等式由构造保证，而非运行时检查。**

---

如果想进一步理解这套机制如何嵌入更大的扩展点体系，可以看看 [Capability Seams](seams.md) 和 [Cordis Waterfall Dispatch](events.md)。

[Capability Seams](seams.md)
[Cordis Waterfall Dispatch](events.md)
[Tool Execution Pipeline](../30-capability/tool-pipeline.md)


## 中途换 Agent——等式依然成立，因为每次换都是一次全新铸造

"换 agent" 在这个系统里不是替换同一个 agent 的 id，而是**创建一个全新的子 agent**，拥有自己独立的 session 和 identity。等式不变，只是作用域变了。

---

### 关键机制：子 agent 是独立实体，不是父 agent 的变体

从 [child-agent.ts](packages/subagent/subagent/src/child-agent.ts#L107-L125) 的 `childSessionMeta()` 可以看到：

```ts
function childSessionMeta(
  parent: Agent,
  childDepth: number,
  lineageSeedLength: number,
): NonNullable<CreateAgentOptions['meta']> {
  const parentHeader = parent.session.header
  return {
    cwd: parentHeader.cwd,
    parentSession: parentHeader.id,   // ← 记录血统，但不继承 id
    origin: 'subagent',
    delegationDepth: childDepth,       // ← 递归深度 +1
    ...
  }
}
```

子 agent 的 `parentSession` 记录了"我是谁生的"，但 `sessionId` 是**全新的**——由工厂的 `CreateAgentOptions.sessionId` 独立铸造。

---

### 身份隔离的三层保障

#### 1. 每个 agent 有自己的 `withInitiator` 边界

父 agent 的驱动链：

```
父 agent (id="parent-123")
  └─ withInitiator(父) 
       └─ executeToolCalls → exec.agent = 父
       └─ Cordis 事件 → bridge 读 父.session.header.id = "parent-123"
```

子 agent 的驱动链：

```
子 agent (id="child-456")
  └─ withInitiator(子)          ← 独立的边界
       └─ executeToolCalls → exec.agent = 子
       └─ Cordis 事件 → bridge 读 子.session.header.id = "child-456"
```

`AsyncLocalStorage` 保证两条链互不干扰——子 agent 的 tool 调用永远不会读到父 agent 的引用。

#### 2. Bridge 的 subagent 事件用**子 agent** 的身份

在 [hooks-claude-code/index.ts](packages/hooks/hooks-claude-code/src/index.ts#L281-L295) 中：

```ts
ctx.on('subagent/start', (info) => {
  const child = ctx.get('agents')?.get(info.id)  // ← 取子 agent
  subagentChildren.set(info.runId, child)
  detached.track(runPoint('SubagentStart', SUBAGENT_TYPE,
    subagentPayload(ctx, 'SubagentStart', info, child),  // ← child 的 session_id
    { ...child ? { agent: child } : {}, signal: detached.signal })
  ...
})
```

bridge 传给 hook 的 `session_id` 是**子 agent 的 session id**，不是父的。子 agent 内部的 hook 和 tool 也遵循同一等式，只是在自己的作用域内。

#### 3. 递归深度有上限

[child-agent.ts](packages/subagent/subagent/src/child-agent.ts#L52-L58) 的 `resolveChildDepth()` 强制递增深度并检查上限：

```ts
function resolveChildDepth(parent: Agent, maxDepth: number | undefined): number {
  const childDepth = delegationDepthOf(parent) + 1
  if (maxDepth !== undefined && childDepth > maxDepth)
    throw new SubagentDepthError(childDepth, maxDepth)
  return childDepth
}
```

不可能无限套娃。

---

### 完整的嵌套图景

```
工厂铸造 parent-123
  ├─ parent agent.id = "parent-123"
  ├─ parent session.header.id = "parent-123"
  │
  ├─ Tool 调用触发 subagent 委派
  │   │
  │   └─ 工厂铸造 child-456（sessionId 全新）
  │       ├─ child agent.id = "child-456"
  │       ├─ child session.header.id = "child-456"
  │       ├─ child session.header.parentSession = "parent-123"  ← 血统记录
  │       ├─ child session.header.delegationDepth = 1
  │       │
  │       ├─ child 的 Tool: exec.agent.id = "child-456"  ✓
  │       └─ child 的 Hook: payload.session_id = "child-456"  ✓
  │
  ├─ parent 的 Tool: exec.agent.id = "parent-123"  ✓ （不受子 agent 影响）
  └─ parent 的 Hook: payload.session_id = "parent-123"  ✓
```

**每一层 agent 独立维护等式，互不污染。**

---

### 那 Hook 写的数据怎么跨层读？

如果父 agent 的 hook 用 `_session.id = "parent-123"` 写了数据，子 agent 的 tool 用 `exec.agent.id = "child-456"` 去读——**读不到，也不应该读到**。它们不是同一个 session。

如果需要跨层传递，正确做法是：
- Hook 把数据写在 payload 的 `additionalContext` 里，bridge 会注入到模型上下文
- 父 agent 把需要传递的信息放进子 agent 的 **seed**（fork 前缀事件）
- 子 agent 的 hook/tool 只操作自己的 session 存储空间

这不是缺陷，是**最小权限原则**——子 agent 不应该隐式继承父 agent 的外部存储状态。

---

一句话：**换 agent 就是换 session，换 session 就是换身份宇宙。每个宇宙内部等式自洽，宇宙之间靠血统记录和 seed 传递显式关联，绝不共享身份标识。**

[Capability Seams](seams.md)
<!-- 作用域 Agent 注册（待补充） -->
[Cordis Waterfall Dispatch](events.md)


## 等式被打破——后果与防御

这是个好问题。等式 `payload.session_id === exec.agent.id` 由构造保证而非运行时检查，所以一旦被打破，后果是**静默的数据错乱**——没有异常，没有栈追踪，只有幽灵般的读写错位。

---

### 破坏场景与后果

#### 场景 1：Hook 写到了别人的 key

```
Hook 拿到 session_id = "A"，写入 Store["A"] = data
Tool 拿到 exec.agent.id = "B"，从 Store["B"] 读取 → 读不到
```

**后果**：Tool 读到空结果或旧数据，决策基于过期信息。最坏情况：权限 hook 在 session A 上写了"允许"，但 session B 的 tool 读到的是"拒绝"或反之——**权限倒置**。

#### 场景 2：两个 session 的数据交叉污染

```
Session A 的 hook 写 Store["A"] = { approved: true }
Session B 的 hook 写 Store["B"] = { approved: false }
由于 id 错位，A 的 tool 读到 Store["B"] → approved: false
```

**后果**：一个 session 的行为被另一个 session 的 hook 结果控制——**跨会话泄漏**。

#### 场景 3：持久化后无法恢复

Session 日志记录的是 `session.header.id`，但如果 hook payload 中的 `session_id` 不一致，持久化回放时无法将 hook 事件与正确的 session 关联——**日志不可重构**，违反了系统的核心不变式。

---

### 系统有哪些防御？

#### 1. 构造时只读——破坏路径极窄

从 [agent.ts](packages/core/agent-loop/src/agent.ts#L88-L99) 可以看到，`id` 和 `session` 都是构造函数的 `public readonly` 属性：

```ts
constructor(
  private loopCtx: Context,
  public readonly id: SessionId,        // readonly
  public readonly session: Session,      // readonly
) { ... }
```

TypeScript 层面无法重新赋值。JavaScript 运行时层面，需要显式 `(agent as any).id = 'evil'` 才能打破——这不是意外，是蓄意破坏。

#### 2. Agent-Loop 的不变式检查器

从 [agent-loop/invariant.ts](packages/core/agent-loop/src/invariant.ts#L27-L51) 可以看到，系统在每次 LLM 调用前验证 session 一致性：

```ts
ctx.on('llm/stream', (options: GenerateOptions, next) => {
  if (!isAgentLoopRequest(options)) return next()
  if (options.sessionId === undefined)
    fail('a loop-built request must carry a session id')
  const session = ctx.sessions.get(options.sessionId)
  if (!session)
    fail(`a loop-built request must carry a live session id, got "${String(options.sessionId)}"`)
  // 还会检查 deriveMessages() 是否与 request 一致
  ...
})
```

如果 `sessionId` 指向了错误的或不存在的 session，**不变式检查器会在 LLM 调用前拦截**，而不是静默通过。

#### 3. AsyncLocalStorage 边界隔离

`withInitiator()` 通过 `AsyncLocalStorage` 传播 agent 引用，这是 Node.js 原生的异步上下文隔离机制。只要驱动链在 `withInitiator` 边界内运行，`requireInitiator()` 返回的就是正确的 agent。**打破它需要跨边界的操作**（如将异步回调逃逸到边界外再回来），这在正常代码路径中不会发生。

#### 4. 子 agent 的深度上限

从 [child-agent.ts](packages/subagent/subagent/src/child-agent.ts#L52-L58) 的 `resolveChildDepth()` 可知，嵌套深度有硬上限。这防止了无限递归导致的栈/上下文耗尽——即使某个层级出了问题，也不会级联到所有层级。

---

### 真正的风险在哪？

等式在**正常路径**上几乎不可能被打破。但以下场景是薄弱点：

| 风险路径 | 具体场景 | 防御状态 |
|---|---|---|
| **Hook 进程篡改 payload** | 外部 hook 进程修改了 stdin JSON 中的 `session_id` | ⚠️ 无防御——hook 是不受信外部进程 |
| **存储层 key 碰撞** | 两个不相关 session 恰好产生相同的存储 key | ⚠️ 依赖调用者使用完整 session_id 作为 key |
| **跨边界的异步逃逸** | 把 `exec.agent` 引用存到全局变量，在另一个 `withInitiator` 边界内使用 | 🔒 TypeScript `readonly` + 代码规范 |
| **手动构造 exec 上下文** | 绕过 `executeToolCalls` 手动构造 `ToolExecutionInput` 并填入错误 agent | 🔒 不变式检查器会在 LLM 调用时拦截 |

**最大的真实风险是第一条**：hook 进程可以返回包含任意 `session_id` 的输出（虽然它不直接影响 bridge 的 payload 构造，但如果 hook 的输出被持久化且后续被错误关联，就会产生幽灵数据）。不过 bridge 的 `base()` 函数始终从 `agent.session.header.id` 取值，不信任 hook 输出中的身份信息——所以 hook 无法**篡改** bridge 发出的 `session_id`，只能篡改自己写入外部存储的 key。

---

### 总结

> 等式由构造保证，由 readonly 封印，由 AsyncLocalStorage 隔离，由不变式检查器兜底。打破它需要蓄意绕过三层防御。如果真的打破，后果是静默的数据错乱——这正是为什么系统选择**从构造上保证**而非**运行时检查**：运行时检查只能捕获已发生的错误，构造保证让错误不可表达。

如果还想深入理解这套防御哲学，可以看看 <!-- 防御性模式（待补充） -->。

<!-- 防御性模式（待补充） -->
[Session Log and Events](agent-lifecycle.md)
[Capability Seams](seams.md)


## 幽灵错位如何现形、如何收尸

等式被打破是静默的，但系统留了足够多的**尸检线索**和**复位路径**。

---

### 第一步：让它现形——不变式检查器会把幽灵变成尸体

系统有一个**可配置的运行时不变式注册表**，每个包注册自己的检查。从 [invariants/src/index.ts](packages/runtime-diagnostics/invariants/src/index.ts#L97-L110) 可以看到核心机制：

```ts
register(packageName: string, installer: InvariantInstaller): () => void {
  // 每个包注册自己的检查，失败时抛 InvariantError
  const installInvariant = (childCtx: Context) => (
    installer(childCtx, (message): never => {
      throw new InvariantError(packageName, message)
    })
  )
}
```

而 [agent-loop/invariant.ts](packages/core/agent-loop/src/invariant.ts#L27-L51) 在**每次 LLM 请求前**验证 session 身份一致性：

```ts
ctx.on('llm/stream', (options: GenerateOptions, next) => {
  if (options.sessionId === undefined)
    fail('a loop-built request must carry a session id')
  const session = ctx.sessions.get(options.sessionId)
  if (!session)
    fail(`a loop-built request must carry a live session id, got "${String(options.sessionId)}"`)
  // 还验证 deriveMessages() 与 request 一致——日志重构脱同步检测
})
```

**如果等式被打破，不变式检查器会在 LLM 调用前把它变成一个 `InvariantError` 异常，附带完整的包名和违规描述。** 幽灵不再是幽灵，而是一个带栈追踪的崩溃。

---

### 第二步：定位错位——session 事件日志是唯一的真相源

Session 日志是 event-sourced 的，只追加不修改。当错位发生时，日志里会留下矛盾痕迹：

| 事件 | 记录的 ID | 应该等于 |
|---|---|---|
| `hook/invoked` | 通过 `handlerId` 关联到 session | session.header.id |
| `tool/call` | 通过 agent 引用关联到 session | agent.id |
| `request/header` | sessionId | session.header.id |

**排查方法**：遍历同一 session 的事件流，提取所有携带身份信息的字段，检查是否一致。从 [hook-protocol/types.ts](packages/hooks/hook-protocol/src/types.ts#L14-L33) 可以看到，每个 `hook/invoked` 和 `hook/result` 事件都记录了 `turn`、`point`、`handlerId`——足够回溯到具体哪个 hook 点出了问题。

---

### 第三步：复位——三层策略，按严重度递进

#### 策略 A：重启 session（最轻）

等式被打破通常意味着运行时状态已经不可信。最快的复位是：
1. 丢弃当前 agent 的 live 状态
2. 用 `ctx.agents.resume()` 从持久化日志重建 session
3. 工厂重新铸造 agent，`id` 和 `session.header.id` 重新绑定

日志是真相，内存状态是投影。**重建投影，丢弃损坏的缓存。**

#### 策略 B：截断到最近的一致点（中等）

如果日志本身也被污染（比如 hook 的输出被错误持久化）：
1. 找到日志中最后一个 `request/header` 与 `deriveMessages()` 一致的 checkpoint
2. 截断其后的所有事件
3. 从截断点 resume

不变式检查器的日志重构脱同步检测（`JSON.stringify(options.messages) !== JSON.stringify(expected)`）精确地标识了这种分歧。

#### 策略 C：完全重建（最重）

如果不确定污染范围：
1. 保留 session 日志作为事后分析
2. 用 `CreateAgentOptions.sessionId` 创建全新 session（新 id）
3. 通过 seed 将未污染的父 session 前缀注入新 session
4. 新宇宙，新身份，从干净状态开始

---

### 第四步：防止再犯——给等式加运行时守卫

系统已经提供了基础设施，只需在身份接缝处加一个检查：

```ts
// 在 tools/pre-execute 或 hook bridge 中加
if (payload.session_id !== exec.agent.id) {
  ctx.invariants // 如果服务存在
    ? fail(`identity seam: payload.session_id="${payload.session_id}" ≠ agent.id="${exec.agent.id}"`)
    : throw new Error(`identity seam violation`)
}
```

但注意：**当前系统故意没有加这个运行时检查**，因为等式由构造保证，运行时检查是冗余成本。这是一个权衡——如果你观察到了幽灵错位，说明构造保证已被绕过（可能是外部 hook 进程篡改、非正常代码路径等），此时才值得加守卫。

---

### 总结：复位流程

```
幽灵错位
  │
  ├─ 不变式检查器自动拦截 → InvariantError（如果启用）
  │     │
  │     └─ 异常终止当前 turn → 进入 error 处理
  │
  ├─ 如果静默通过（检查器未启用）
  │     │
  │     ├─ 从 session 日志提取身份字段 → 交叉比对
  │     ├─ 定位第一个不一致的事件 → 截断点
  │     └─ resume 或 create 新 session
  │
  └─ 防止再犯
        ├─ 启用 invariants（config.enabled: true）
        ├─ 在身份接缝处加运行时守卫
        └─ 确保外部 hook 不信任 payload 中的身份，只从 agent 引用读取
```

一句话：**日志是真相，内存是投影，不变式是警犬。投影坏了就重建投影，日志坏了就截断日志，两者都坏了就换个宇宙。**

<!-- 防御性模式（待补充） -->
[Session Log and Events](agent-lifecycle.md)
[Architecture Overview](../00-understanding/dsh-platform.md)