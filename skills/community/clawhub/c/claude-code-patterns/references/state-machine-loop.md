# 状态机 Query Loop 完整实现

本参考文档提供状态机 Query Loop 的完整设计模式和实现细节。

## 核心设计原则

1. **不可变状态** — 每次状态更新创建新对象，不用 `.push()` 等可变操作
2. **单入口循环** — `while(true)` + `continue`，不用递归
3. **显式 transition** — 记录每次循环结束的原因
4. **参数不可变** — 循环外提取 `params`，循环内不修改

## 完整骨架代码

```typescript
// ===================== 状态定义 =====================

type State = {
  messages: Message[]
  toolUseContext: ToolUseContext
  transition: Continue | undefined
  maxOutputTokensRecoveryCount: number
  hasAttemptedReactiveCompact: boolean
  autoCompactTracking?: AutoCompactTrackingState
  turnCount: number
  pendingToolUseSummary?: Promise<ToolUseSummaryMessage | null>
}

type Continue =
  | { reason: 'next_turn' }
  | { reason: 'max_output_tokens_recovery'; attempt: number }
  | { reason: 'max_output_tokens_escalate' }
  | { reason: 'reactive_compact_retry' }
  | { reason: 'collapse_drain_retry'; committed: number }
  | { reason: 'stop_hook_blocking' }
  | { reason: 'token_budget_continuation' }

// ===================== 循环骨架 =====================

export async function* query(
  params: QueryParams,
): AsyncGenerator<StreamEvent, Terminal> {
  const consumedCommandUuids: string[] = []

  try {
    const terminal = yield* queryLoop(params, consumedCommandUuids)
    return terminal
  } finally {
    // 确保清理所有消耗的命令
    for (const uuid of consumedCommandUuids) {
      notifyCommandLifecycle(uuid, 'completed')
    }
  }
}

async function* queryLoop(
  params: QueryParams,
  consumedCommandUuids: string[],
): AsyncGenerator<StreamEvent, Terminal> {
  // === 提取不可变参数 ===
  const {
    systemPrompt,
    userContext,
    systemContext,
    canUseTool,
    fallbackModel,
    querySource,
    maxTurns,
  } = params

  // === 初始化可变状态 ===
  let state: State = {
    messages: params.messages,
    toolUseContext: params.toolUseContext,
    transition: undefined,
    maxOutputTokensRecoveryCount: 0,
    hasAttemptedReactiveCompact: false,
    turnCount: 1,
    pendingToolUseSummary: undefined,
  }

  // === 主循环 ===
  while (true) {
    const {
      messages,
      toolUseContext,
      transition,
      maxOutputTokensRecoveryCount,
      hasAttemptedReactiveCompact,
      turnCount,
    } = state

    // ========== 每个迭代开始 ==========

    // 1. 上下文预处理（压缩、折叠等）
    const { compactionResult, tracking } = await autoCompactIfNeeded(
      messages,
      toolUseContext,
      cacheSafeParams,
      querySource,
      state.autoCompactTracking,
    )

    // 2. API 调用
    const { assistantMessages, toolResults, toolUseBlocks } = 
      await callModelStreaming(messages, toolUseContext)

    // 3. 检查是否需要继续
    if (toolUseBlocks.length === 0) {
      // 无工具调用，检查 stop hooks
      const stopHookResult = yield* handleStopHooks(...)
      if (stopHookResult.preventContinuation) {
        return { reason: 'stop_hook_prevented' }
      }
      if (stopHookResult.blockingErrors.length > 0) {
        // stop hook 要求重试
        state = {
          messages: [...messages, ...assistantMessages, ...stopHookResult.blockingErrors],
          toolUseContext,
          transition: { reason: 'stop_hook_blocking' },
          maxOutputTokensRecoveryCount: 0,
          hasAttemptedReactiveCompact,
          turnCount,
          autoCompactTracking: tracking,
          pendingToolUseSummary: undefined,
        }
        continue
      }
      return { reason: 'completed' }
    }

    // 4. 工具执行
    const toolUpdates = await runTools(toolUseBlocks, ...)
    const toolResults = collectResults(toolUpdates)

    // ========== 继续下一轮 ==========

    state = {
      messages: [...messages, ...assistantMessages, ...toolResults],
      toolUseContext: updatedContext,
      transition: { reason: 'next_turn' },
      maxOutputTokensRecoveryCount: 0,
      hasAttemptedReactiveCompact: false,
      turnCount: turnCount + 1,
      autoCompactTracking: tracking,
      pendingToolUseSummary: nextPendingToolUseSummary,
    }
    continue
  }
}
```

## 各 Transition 的处理逻辑

### `next_turn` — 正常继续

最常见的情况，工具执行完毕，准备下一轮。

```typescript
state = {
  messages: [...messages, ...assistantMessages, ...toolResults],
  toolUseContext: updatedContext,
  transition: { reason: 'next_turn' },
  turnCount: turnCount + 1,
  // 重置恢复计数器
  maxOutputTokensRecoveryCount: 0,
  hasAttemptedReactiveCompact: false,
}
continue
```

### `max_output_tokens_recovery` — 输出被截断

```typescript
const recoveryMessage = createUserMessage({
  content: `Output token limit hit. Resume directly — no apology, no recap. ` +
    `Pick up mid-thought if that is where the cut happened. ` +
    `Break remaining work into smaller pieces.`,
  isMeta: true,
})

state = {
  messages: [...messages, ...assistantMessages, recoveryMessage],
  toolUseContext,
  transition: { reason: 'max_output_tokens_recovery', attempt: count + 1 },
  maxOutputTokensRecoveryCount: count + 1,
  // 注意：不重置 hasAttemptedReactiveCompact
}
continue
```

**为什么最多尝试 3 次**：
```typescript
const MAX_OUTPUT_TOKENS_RECOVERY_LIMIT = 3
if (maxOutputTokensRecoveryCount >= MAX_OUTPUT_TOKENS_RECOVERY_LIMIT) {
  yield lastMessage  // surface the withheld error
  return { reason: 'max_output_tokens' }
}
```

### `max_output_tokens_escalate` — 升级 token 限制

第一次截断时，先尝试升级到更高限制再重试，而不是立即注入恢复消息。

```typescript
// 如果之前用的是 8k 默认值，升级到 64k
if (maxOutputTokensOverride === undefined) {
  state = {
    messages,
    toolUseContext,
    transition: { reason: 'max_output_tokens_escalate' },
    maxOutputTokensOverride: 64_000,  // 升级！
  }
  continue
}
```

### `reactive_compact_retry` — 上下文太长

```typescript
const compacted = await tryReactiveCompact({ hasAttempted, ... })
if (compacted) {
  const postCompactMessages = buildPostCompactMessages(compacted)
  state = {
    messages: postCompactMessages,
    toolUseContext,
    transition: { reason: 'reactive_compact_retry' },
    hasAttemptedReactiveCompact: true,  // 标记已尝试过
    autoCompactTracking: undefined,     // 重置跟踪状态
  }
  continue
}
// 恢复失败，surface 错误
yield lastMessage
return { reason: 'prompt_too_long' }
```

### `collapse_drain_retry` — 先排空折叠再压缩

```typescript
// 优先尝试已有的 collapse（便宜，保持粒度）
const drained = contextCollapse.recoverFromOverflow(messages, querySource)
if (drained.committed > 0) {
  state = {
    messages: drained.messages,
    toolUseContext,
    transition: { reason: 'collapse_drain_retry', committed: drained.committed },
  }
  continue
}
// 没有可排空的折叠，尝试 reactive compact
```

## 状态重置规则

不是所有字段都需要在每次 continue 时重置：

| 字段 | next_turn | compact_retry | stop_hook | token_recovery |
|------|-----------|---------------|-----------|----------------|
| messages | 合并+重置 | 替换 | 合并+重置 | 合并+重置 |
| turnCount | +1 | 不变 | 重置为 1 | 不变 |
| maxOutputTokensRecoveryCount | 重置为 0 | 不变 | 重置为 0 | +1 |
| hasAttemptedReactiveCompact | 重置为 false | 设为 true | 保持 | 保持 |
| autoCompactTracking | 继承/更新 | 重置为 undefined | 继承 | 继承 |

## 测试策略

利用 `transition` 字段做断言，不需要检查消息内容：

```typescript
// ❌ 脆弱的测试：检查消息内容
expect(messages[messages.length - 1]).toContain('Output token limit')

// ✅ 健壮的测试：检查 transition
const terminal = await collectTerminal(query(...))
expect(terminal.transition).toEqual({ reason: 'max_output_tokens_recovery', attempt: 1 })
```

## 常见陷阱

### 1. 不要在循环内重新提取 params

```typescript
// ❌ 错误：每次迭代都重新提取，可能被修改
while (true) {
  const { systemPrompt } = params  // 不要这样做
}

// ✅ 正确：在循环外提取，之后只读
const { systemPrompt } = params
while (true) {
  // 使用 systemPrompt...
}
```

### 2. 合并状态时不要遗漏字段

```typescript
// ❌ 错误：遗漏了 autoCompactTracking
state = { messages: newMessages, toolUseContext, turnCount: n + 1 }

// ✅ 正确：显式列出所有字段
state = {
  messages: newMessages,
  toolUseContext,
  turnCount: n + 1,
  maxOutputTokensRecoveryCount: 0,
  hasAttemptedReactiveCompact: false,
  transition: { reason: 'next_turn' },
  pendingToolUseSummary: undefined,
  autoCompactTracking: tracking,
}
```

### 3. 恢复时保持 hasAttemptedReactiveCompact

如果 compact 已经尝试过且失败，不要重置这个标志，否则会陷入无限循环。
