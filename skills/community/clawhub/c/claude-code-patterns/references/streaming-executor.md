# 流式工具并发执行器

本参考文档描述 `StreamingToolExecutor` 的设计细节。

## 核心问题

传统的 agent 执行模型：
1. 模型完整输出 `tool_use` 块
2. 等待模型输出完毕
3. 按顺序执行所有工具
4. 等待所有工具完成
5. 将结果发回模型

**问题**：步骤 1-2 和步骤 3-5 串行执行，浪费大量等待时间。模型输出可能需要 5-30 秒，而其中大部分时间在等工具结果。

## 核心思路

在模型流式输出的同时就开始执行工具。结果缓冲后按原顺序 yield 给调用方。

## 状态机

每个工具有 4 种状态：

```typescript
type ToolStatus = 'queued' | 'executing' | 'completed' | 'yielded'

type TrackedTool = {
  id: string
  block: ToolUseBlock
  status: ToolStatus
  isConcurrencySafe: boolean
  results: Message[]
  pendingProgress: Message[]  // 进度消息，单独处理
}
```

状态转换图：

```
[queued] ──执行条件满足──→ [executing] ──执行完毕──→ [completed] ──已yield──→ [yielded]
    │
    └──流式 fallback 时→ [completed] (synthetic error results)
```

## 并发控制

### 工具分区

```typescript
function partitionToolCalls(
  toolUseMessages: ToolUseBlock[],
  toolUseContext: ToolUseContext,
): Batch[] {
  return toolUseMessages.reduce((acc, toolUse) => {
    const tool = findToolByName(toolUseContext.options.tools, toolUse.name)
    const isConcurrencySafe = tool?.isConcurrencySafe?.(toolUse.input) ?? false

    if (isConcurrencySafe && acc.at(-1)?.isConcurrencySafe) {
      // 合并到上一个 batch
      acc[acc.length - 1].blocks.push(toolUse)
    } else {
      // 新开一个 batch
      acc.push({ isConcurrencySafe, blocks: [toolUse] })
    }
    return acc
  }, [])
}
```

**效果**：`[Read, Grep, Edit]` → `[{ safe: true, blocks: [Read, Grep] }, { safe: false, blocks: [Edit] }]`

### 执行条件

```typescript
private canExecuteTool(isConcurrencySafe: boolean): boolean {
  const executingTools = this.tools.filter(t => t.status === 'executing')
  return (
    executingTools.length === 0 ||
    (isConcurrencySafe && executingTools.every(t => t.isConcurrencySafe))
  )
}
```

解读：
- 如果没有正在执行的工具 → 可以执行
- 如果当前工具是并发安全的，且所有正在执行的工具都是并发安全的 → 可以执行
- 否则 → 等待

### 队列处理

```typescript
private async processQueue(): Promise<void> {
  for (const tool of this.tools) {
    if (tool.status !== 'queued') continue

    if (this.canExecuteTool(tool.isConcurrencySafe)) {
      await this.executeTool(tool)
    } else if (!tool.isConcurrencySafe) {
      // 非并发安全工具遇到阻碍就停止，因为需要保持顺序
      break
    }
    // 并发安全工具会尝试继续处理队列中的其他工具
  }
}
```

## 与模型流式输出的集成

```typescript
async function* callModelWithStreamingTools(
  messages: Message[],
  toolUseContext: ToolUseContext,
) {
  const executor = new StreamingToolExecutor(tools, canUseTool, toolUseContext)

  for await (const message of deps.callModel({ messages })) {
    // 1. 把模型输出 yield 给调用方（withhold 可恢复错误）
    if (!isRecoverableError(message)) {
      yield message
    }

    // 2. 收集 assistant message
    if (message.type === 'assistant') {
      assistantMessages.push(message)
      for (const toolBlock of message.toolUseBlocks) {
        executor.addTool(toolBlock, message)  // 立即开始执行！
      }
    }

    // 3. yield 已完成工具的结果（不阻塞）
    for (const result of executor.getCompletedResults()) {
      yield result.message
    }
  }

  // 4. 等待剩余工具
  for await (const result of executor.getRemainingResults()) {
    yield result.message
  }
}
```

## 进度消息

工具执行过程中可以产生进度消息（如大文件读取的进度），需要立即 yield，不能等到工具完成：

```typescript
// 工具执行器内
for await (const update of runToolUse(...)) {
  if (update.message.type === 'progress') {
    // 立即加入待 yield 列表
    tool.pendingProgress.push(update.message)
    this.progressAvailableResolve?.()  // 唤醒等待中的 getRemainingResults
  } else {
    messages.push(update.message)
  }
}
```

```typescript
// getCompletedResults
*getCompletedResults() {
  for (const tool of this.tools) {
    // 先 yield 进度消息
    while (tool.pendingProgress.length > 0) {
      yield { message: tool.pendingProgress.shift()! }
    }
    // 再 yield 完成结果
    if (tool.status === 'completed') {
      tool.status = 'yielded'
      yield* tool.results
    }
  }
}
```

## 取消机制

### 流式回退（Streaming Fallback）

当模型输出回退（如触发了 fallback 模型切换），之前流式执行的工具结果都无效：

```typescript
// 调用方检测到 streaming fallback
if (streamingFallbackOccured) {
  executor.discard()  // 丢弃所有工具
  executor = new StreamingToolExecutor(tools, canUseTool, toolUseContext)  // 重置
}
```

```typescript
discard(): void {
  this.discarded = true
  // getRemainingResults 会立即返回，不处理任何工具
}
```

### 兄弟工具错误

Bash 工具出错时，取消所有并行工具：

```typescript
const isErrorResult = message.message.content.some(
  c => c.type === 'tool_result' && c.is_error === true
)

if (isErrorResult && tool.block.name === 'Bash') {
  this.hasErrored = true
  this.siblingAbortController.abort('sibling_error')
}
```

**为什么只取消 Bash**：Bash 命令往往有隐式依赖链（mkdir 失败后 cd 就没意义），而 Read/WebFetch 等是独立的。

### 用户中断

ESC 键触发 `abort` 信号：

```typescript
private getAbortReason(tool: TrackedTool): 'sibling_error' | 'user_interrupted' | 'streaming_fallback' | null {
  if (this.discarded) return 'streaming_fallback'
  if (this.hasErrored) return 'sibling_error'
  if (this.toolUseContext.abortController.signal.aborted) {
    if (this.toolUseContext.abortController.signal.reason === 'interrupt') {
      // 用户输入了新消息
      const behavior = this.getToolInterruptBehavior(tool)
      return behavior === 'cancel' ? 'user_interrupted' : null
    }
    return 'user_interrupted'
  }
  return null
}
```

**注意**：工具有 `interruptBehavior` 属性，`cancel` 行为会被中断，`block` 行为继续执行（用于长时间运行的重要操作）。

## 工具并发安全声明

```typescript
// 每个工具实现 isConcurrencySafe 方法
interface ToolDefinition {
  isConcurrencySafe?: (input: unknown) => boolean
  interruptBehavior?: () => 'cancel' | 'block'
}

// 示例
class ReadTool {
  isConcurrencySafe(_input: ReadInput): boolean {
    return true  // 只读，无副作用
  }
}

class WriteTool {
  isConcurrencySafe(input: WriteInput): boolean {
    // 如果目标是不同的文件，可以并发
    // 如果目标是同一个文件，不能并发
    return !this.wouldOverwrite(input)
  }
}

class BashTool {
  isConcurrencySafe(_input: BashInput): boolean {
    return false  // 有副作用，永远不并发
  }

  interruptBehavior(): 'cancel' | 'block' {
    return 'cancel'  // 可以被 ESC 取消
  }
}
```

## 与传统模式的性能对比

| 阶段 | 传统模式 | 流式执行 |
|------|---------|---------|
| 模型输出 5s | 等待 5s | 等待 5s |
| 工具1 Read 3s | 等上一阶段完成才开始 | 模型输出时已开始 |
| 工具2 Grep 1s | 等上一工具完成 | 与工具1并行 |
| 工具3 Edit 1s | 等上一工具完成 | 等待前两者完成 |
| 发送结果 | 全部完成后一次性发送 | 边完成边发送 |
| **总耗时** | 5+3+1+1 = 10s | max(5, 3) + 1 = 8s |

实际场景中 Read/Grep 通常是并发的，总耗时可降至 6-7s。

## 实现检查清单

- [ ] 工具在 `tool_use` 块到达时立即开始执行
- [ ] 并发安全工具批量并行执行
- [ ] 非并发安全工具串行执行
- [ ] 结果按原始顺序 yield（即使完成时间不同）
- [ ] 进度消息立即 yield，不等待
- [ ] Bash 错误取消兄弟工具
- [ ] 流式回退时 discard 所有工具
- [ ] 用户中断时支持 interruptBehavior
