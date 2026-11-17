# DSH 事件目录（实测 2026-08，含选择脑图）

> 完整目录来自运行时 `Event.listEvents` 实测。写插件要"介入某个过程"时先查本节找事件，
> 再查精确契约（payload / 模式 / 监听器签名）后编写。

## 事件选择脑图

```
要介入什么过程？
│
├─ 模型步骤/轮次
│   ├─ 步骤前拦截/改消息 → agent/pre-step (waterfall)
│   ├─ 替换调用配置     → agent/request (waterfall)
│   ├─ 请求失败处理     → agent/request-error (waterfall)
│   ├─ 轮次即将关闭     → agent/turn-stopping (serial)
│   └─ 状态变化         → agent/status (emit: idle⇄running)
│
├─ 工具执行
│   ├─ 执行前 允许/拒绝/询问 → tools/pre-execute (waterfall)
│   ├─ 执行中 超时/重试/指标 → tools/execute (waterfall)
│   ├─ 执行后 替换/增强/拦截 → tools/post-execute (waterfall)
│   └─ 结果观察(冻结快照)    → tools/result (emit)
│
├─ LLM 调用
│   └─ 每次流式调用环绕   → llm/stream (waterfall)
│
├─ 会话
│   ├─ 创建/销毁         → session/created / session/disposed (emit)
│   ├─ 事件追加(事后)    → session/event (emit)
│   └─ 持久化检查点      → session/flush (parallel)
│
├─ 提示词组装
│   ├─ 组装结果专家环绕  → system-prompt/assemble (waterfall)
│   └─ 任何提供方变化    → system-prompt/change (emit)
│
├─ 子代理/工作流
│   ├─ 子代理启动/结束   → subagent/start / subagent/end (emit)
│   └─ 工作流 start/phase/log/agent-*/end (emit)
│
├─ 审批/凭据/设置/技能/命令
│   ├─ 审批请求          → approval/request (waterfall)
│   ├─ 凭据变更          → credentials/updated (emit)
│   ├─ 设置变更          → settings/updated (emit)
│   ├─ 技能目录变化      → skills/change (emit)
│   └─ 命令注册变化      → commands/change (emit)
│
└─ 文件系统
    ├─ 写入意图决策      → fs/write-intent (waterfall)
    ├─ 编辑意图决策      → fs/edit-intent (waterfall)
    └─ 观察记录          → fs/observed (emit)
```

## 高频事件明细（插件开发最常用）

### agent/status（emit）— 监听 Agent 状态

```ts
ctx.on('agent/status', (payload) => {
  // payload: { agent: Agent; status: 'idle' | 'running' }
  if (payload.status === 'idle') { /* 轮次结束，可做自动存储等 */ }
})
```
> 注：`this: Scoped<Agent>` —— 监听器在 agent 作用域内触发；跨会话消费需注意作用域。

### tools/pre-execute（waterfall）— 工具审计/门禁

```ts
ctx.on('tools/pre-execute', async (exec, next) => {
  // exec: { name, args, agent? }
  if (exec.name === 'sensitive_tool') return { allow: false, reason: 'denied by policy' }
  return next()  // 必须放行下游
})
```

### llm/stream（waterfall）— 模型调用环绕

```ts
ctx.on('llm/stream', async function* (options, next) {
  console.log('call to', options.model)
  yield* next()  // 委托下游，得到 StreamChunk
})
```

### agent/pre-step（waterfall）— 步骤前注入记忆/拦截

```ts
ctx.on('agent/pre-step', async (payload, next) => {
  const decision = await next()
  // decision: PreStepDecision — 可替换进入步骤的 messages
  return decision
})
```

## 模式速记（waterfall 与 emit 的区别）

| 模式 | 语义 | 监听器必须 | 典型事件 |
|---|---|---|---|
| `emit` | 广播事实，无返回值 | 无 | agent/status、session/created、tools/result |
| `waterfall` | 环绕链，可改值/否决 | 调 `next()` 并 return | tools/pre-execute、llm/stream、approval/request |
| `serial` | 顺序执行，可 veto | 无（失败即停） | agent/turn-stopping |
| `parallel` | 并行执行，全部 await | 无 | session/flush |

## 精确契约获取方法

- 目录（本文件）只给用途与模式；**写代码前**用 `cordis_inspect_query`（Event/listEvents + 事件名）取精确 payload 类型与参数顺序。
- 事件名带 `this: Scoped<X>` 的：监听器在 X 作用域触发——插件挂在全局时要确认作用域语义，跨 Agent 事件不要假设能拿到具体 Agent。
- 运行时事件会随 DSH 版本演进：目录过期时以 `Event.listEvents` 实时查询为准。
