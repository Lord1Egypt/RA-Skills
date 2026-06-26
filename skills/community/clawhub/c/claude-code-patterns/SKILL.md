---
name: claude-code-patterns
description: Claude Code 源码中提取的 AI Agent 工程模式。当需要设计 agent 调度、工具并发执行、上下文压缩、状态机循环、流式处理等复杂 agent 系统时使用此 skill。触发场景：(1) 设计多轮对话 agent (2) 实现工具并发执行 (3) 构建上下文管理策略 (4) 优化 agent 启动性能 (5) 设计错误恢复机制。
---

# Claude Code 工程模式

Claude Code 是 Anthropic 官方 CLI 产品，其源码展现了业界顶级的 AI Agent 工程实践。本 skill 提炼其核心设计模式。

## 核心模式概览

| 模式 | 解决的问题 | 适用场景 |
|------|-----------|---------|
| 启动并行化 | 启动延迟高 | 需要 I/O 预取的 agent 系统 |
| 状态机 Query Loop | 递归栈溢出、状态追踪困难 | 多轮对话、复杂任务编排 |
| 流式工具并发执行 | 工具执行阻塞模型输出 | 多工具调用场景 |
| 多层上下文压缩 | 上下文溢出 | 长对话、大项目 |
| 错误恢复 withhold | 中间错误暴露给用户 | 任何可能失败的 API 调用 |
| 熔断器 | 失败操作无限重试 | 自动重试逻辑 |
| 工具并发安全声明 | 工具执行冲突 | 多工具并发系统 |

---

## 1. 启动并行化 + Profiling

**问题**：Agent 启动需要加载配置、连接服务、预取数据，串行执行导致启动慢。

**解决方案**：所有阻塞操作并行化，用 checkpoint 测量瓶颈。

```typescript
// 入口文件最顶部 — 模块加载前就开始计时
profileCheckpoint('main_entry');

// 并行启动所有 I/O
const [mdmResult, keychainResult, commandsResult] = await Promise.all([
  startMdmRawRead(),        // 并行读取 MDM 配置
  startKeychainPrefetch(),  // 并行预取 keychain
  getCommands(),            // 并行加载命令
]);

profileCheckpoint('all_parallel_done');
```

**关键技巧**：
- 纯文件读取可以在信任对话框显示前开始（无执行风险）
- `--bare` 模式跳过所有非必要预取，专为脚本调用优化
- 用 `profileCheckpoint()` 定位瓶颈，不要猜测

**应用建议**：
```typescript
// 而不是
await loadConfig();
await connectMCP();
await prefetchMemory();

// 应该
await Promise.all([
  loadConfig(),
  connectMCP(),
  prefetchMemory(),
]);
```

---

## 2. 状态机 Query Loop

**问题**：多轮对话用递归实现会导致栈溢出，且难以追踪状态变化原因。

**解决方案**：用 `while(true)` + 不可变 State 对象，每次 continue 记录原因。

```typescript
type State = {
  messages: Message[]
  toolUseContext: ToolUseContext
  transition: Continue | undefined  // 记录上次 continue 的原因
  maxOutputTokensRecoveryCount: number
  hasAttemptedReactiveCompact: boolean
  // ...
}

type Continue = 
  | { reason: 'next_turn' }
  | { reason: 'max_output_tokens_recovery'; attempt: number }
  | { reason: 'reactive_compact_retry' }
  | { reason: 'stop_hook_blocking' }
  // ...

async function* queryLoop(params: QueryParams) {
  let state: State = initialState(params)
  
  while (true) {
    const { messages, toolUseContext, transition } = state
    
    // 执行查询逻辑...
    
    if (needsFollowUp) {
      state = {
        messages: [...messages, ...toolResults],
        toolUseContext: updatedContext,
        transition: { reason: 'next_turn' },
      }
      continue  // 不用递归，用 continue
    }
    
    return { reason: 'completed' }
  }
}
```

**为什么不用递归**：
- 递归栈会增长，长对话可能溢出
- `transition` 字段让每次 continue 的原因可追踪
- 测试可以断言 `transition.reason` 而不是检查消息内容

**Continue 的各种路径**：

| 原因 | 触发条件 | 处理方式 |
|------|---------|---------|
| `next_turn` | 正常工具调用后 | 合并消息继续 |
| `max_output_tokens_recovery` | 输出被截断 | 注入恢复提示 |
| `reactive_compact_retry` | 上下文太长 | 压缩后重试 |
| `stop_hook_blocking` | hook 要求继续 | 注入 hook 消息 |

---

## 3. 流式工具并发执行（StreamingToolExecutor）

**问题**：传统模式是等模型输出完毕再执行工具，浪费大量时间。

**解决方案**：工具在流式输出时就开始执行，结果缓冲后按序 yield。

```typescript
class StreamingToolExecutor {
  private tools: TrackedTool[] = []
  
  // 添加工具到队列，立即开始执行（如果并发条件允许）
  addTool(block: ToolUseBlock, assistantMessage: AssistantMessage) {
    const isConcurrencySafe = this.checkConcurrencySafe(block)
    this.tools.push({ block, status: 'queued', isConcurrencySafe })
    void this.processQueue()  // 立即处理，不等待
  }
  
  // 获取已完成的结果（非阻塞）
  *getCompletedResults() {
    for (const tool of this.tools) {
      if (tool.status === 'completed' && tool.results) {
        tool.status = 'yielded'
        yield* tool.results
      }
    }
  }
}

// 使用方式
for await (const message of callModel()) {
  if (message.type === 'assistant') {
    for (const toolBlock of message.toolUseBlocks) {
      executor.addTool(toolBlock, message)  // 立即开始执行
    }
  }
  // 同时 yield 已完成的结果
  for (const result of executor.getCompletedResults()) {
    yield result
  }
}
```

**并发安全分区**：

```typescript
// 工具声明自己是否并发安全
class ReadTool {
  isConcurrencySafe(input: Input): boolean {
    return true  // 只读，可并发
  }
}

class BashTool {
  isConcurrencySafe(input: Input): boolean {
    return false  // 可能写文件，串行
  }
}

// 调度器根据声明分区
function partitionToolCalls(tools: ToolUseBlock[]): Batch[] {
  // 连续的并发安全工具合并成一个 batch
  // 非并发安全工具单独一个 batch
}
```

**Bash 错误级联取消**：
```typescript
// Bash 出错时取消所有并行工具
if (tool.block.name === 'BASH' && isErrorResult) {
  this.hasErrored = true
  this.siblingAbortController.abort('sibling_error')
}
```

---

## 4. 多层上下文压缩

**问题**：单一压缩策略无法平衡性能和信息保留。

**解决方案**：5 层防御，从轻到重。

```
Layer 1: History Snip      → 删除旧消息（最轻量，~0 cost）
Layer 2: Microcompact      → 压缩单个工具结果（缓存友好）
Layer 3: Context Collapse  → 折叠历史段落（保留粒度）
Layer 4: Auto Compact      → 全量摘要（最重量）
Layer 5: Reactive Compact  → 被动响应 API 413 错误
```

**各层触发条件**：

| 层 | 触发条件 | 特点 |
|---|---------|-----|
| Snip | 消息数 > 阈值 | 删除最旧的非关键消息 |
| Microcompact | 单个工具结果 > 阈值 | 只压缩该结果，不动其他 |
| Collapse | 上下文 > 90% | 折叠旧段落为摘要 |
| Auto Compact | 上下文 > 93% | 全量摘要 |
| Reactive Compact | API 返回 413 | 最后防线 |

**熔断器设计**：
```typescript
const MAX_CONSECUTIVE_FAILURES = 3

if (tracking?.consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) {
  // 停止重试，避免浪费 API 调用
  return { wasCompacted: false }
}
```

---

## 5. 错误恢复 Withhold 模式

**问题**：流式输出中遇到可恢复错误，如果直接 yield 给调用方，调用方会终止。

**解决方案**：先 withhold（扣留）错误，尝试恢复，成功则调用方无感知。

```typescript
// 流式输出中
if (isRecoverableError(message)) {
  withheld = true
  // 不 yield，先尝试恢复
}

// 尝试恢复
const recovered = await tryRecovery()
if (recovered) {
  // 继续新的查询循环，调用方完全不知道出过错
  state = { messages: recovered.messages, ... }
  continue
}

// 恢复失败才 yield 错误
yield withheldError
```

**适用场景**：
- `prompt_too_long` → 尝试压缩后重试
- `max_output_tokens` → 升级 token 限制或注入恢复提示
- `media_size_error` → 压缩图片后重试

---

## 6. Task 系统的类型设计

**问题**：任务 ID 难以识别类型，日志可读性差。

**解决方案**：Task ID 带类型前缀。

```typescript
const TASK_ID_PREFIXES = {
  local_bash: 'b',
  local_agent: 'a',
  in_process_teammate: 't',
  remote_agent: 'r',
  workflow: 'w',
  monitor: 'm',
  dream: 'd',
}

// 生成: "t3f8a2b1c9" 一眼知道是 teammate
function generateTaskId(type: TaskType): string {
  const prefix = TASK_ID_PREFIXES[type]
  const random = crypto.randomBytes(8).toString('hex').slice(0, 8)
  return prefix + random
}
```

---

## 7. 其他实用模式

### 内容哈希替代随机 UUID
```typescript
// 避免每次 API 调用都破坏 prompt cache
const contentHash = hashContent(settings)
const tempFile = `${cacheDir}/settings_${contentHash}.json`
```

### `using` 关键字管理资源
```typescript
// 自动 dispose，即使发生异常
using pendingMemoryPrefetch = startRelevantMemoryPrefetch(messages)
// ... 代码 ...
// 离开作用域时自动调用 pendingMemoryPrefetch[Symbol.dispose]()
```

### Tombstone 消息
```typescript
// fallback 时用 tombstone 标记需要移除的消息，而不是直接删除
yield { type: 'tombstone', message: orphanedMessage }
```

### Speculation（预测执行）
```typescript
// 用户还在打字时，开始预测并执行
type SpeculationState = {
  status: 'idle'
} | {
  status: 'active'
  id: string
  messagesRef: { current: Message[] }
  timeSavedMs: number  // 累计节省的时间
}
```

---

## 参考文档

- [state-machine-loop.md](references/state-machine-loop.md) — 状态机循环的完整实现
- [streaming-executor.md](references/streaming-executor.md) — 流式执行器的详细设计
- [context-management.md](references/context-management.md) — 上下文压缩的完整策略

---

## 快速应用清单

设计 AI Agent 系统时，检查以下问题：

- [ ] 启动时是否并行化了所有 I/O？
- [ ] 多轮对话是否用状态机而非递归？
- [ ] 工具执行是否可以和模型输出重叠？
- [ ] 工具是否声明了并发安全属性？
- [ ] 是否有多层上下文压缩策略？
- [ ] 可恢复错误是否在内部消化？
- [ ] 重试逻辑是否有熔断器？
- [ ] Task ID 是否包含类型信息？
