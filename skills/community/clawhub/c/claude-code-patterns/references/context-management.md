# 多层上下文压缩策略

本参考文档描述 Claude Code 的 5 层上下文压缩体系。

## 为什么需要多层？

单一压缩策略无法同时满足：
- **低延迟**：压缩越简单越快，但压缩效果差
- **高保真**：保留关键信息，但压缩率低
- **低 API 消耗**：摘要需要额外 API 调用

多层策略按需渐进升级：先尝试轻量手段，撑不住再升级到重量手段。

## 5 层防御体系

```
┌─────────────────────────────────────────────────────────────────┐
│                    上下文使用量                                  │
├─────────────────────────────────────────────────────────────────┤
│  0% ─────┬────────────────────────────────────────────────── │
│           │                                                     │
│  70% ────┼── Snip ────────────────────────────────────────── │
│           │    删除旧消息                                        │
│  80% ────┼── Microcompact ─────────────────────────────────── │
│           │    压缩单个工具结果                                  │
│  90% ────┼── Context Collapse ──────────────────────────────│
│           │    折叠历史段落                                      │
│  93% ────┼── Auto Compact ────────────────────────────────────│
│           │    全量摘要                                          │
│  95% ────┼── [Blocking!] ──────────────────────────────────── │
│           │    禁止继续                                         │
│  100% ───┴── Manual Compact Required ───────────────────────│
└─────────────────────────────────────────────────────────────────┘
         ↑ API 返回 413 时触发 Reactive Compact（跨层）
```

## 各层详解

### Layer 1: History Snip（最轻量）

**原理**：直接删除最旧的非关键消息，不调用 API。

```typescript
function snipCompactIfNeeded(messages: Message[]): {
  messages: Message[]
  tokensFreed: number
  boundaryMessage?: Message
} {
  const MAX_MESSAGES_BEFORE_SNIP = 500
  if (messages.length <= MAX_MESSAGES_BEFORE_SNIP) {
    return { messages, tokensFreed: 0 }
  }

  // 保留最近的 N 条消息和所有 tool_use/tool_result 对
  const recentMessages = messages.slice(-MAX_MESSAGES_BEFORE_SNIP)
  const preserved = preserveToolPairs(recentMessages)

  return {
    messages: preserved,
    tokensFreed: estimateTokensRemoved(messages, preserved),
    boundaryMessage: createBoundaryMessage('snip', tokensFreed),
  }
}
```

**特点**：
- 零 API 消耗
- 删除时保留 tool_use/tool_result 对的完整性
- 适合消息数过多但 token 数不超的场景

### Layer 2: Microcompact（缓存友好）

**原理**：压缩单个超大的 tool_result 内容（如长文件读取），不影响其他消息，不破坏 prompt cache。

```typescript
async function microcompact(
  messages: Message[],
  toolUseContext: ToolUseContext,
  querySource: string,
): Promise<{
  messages: Message[]
  compactionInfo?: {
    pendingCacheEdits: {
      baselineCacheDeletedTokens: number
      trigger: string
      deletedToolIds: string[]
    }
  }
}> {
  const MAX_TOOL_RESULT_CHARS = 50_000
  const compressedMessages: Message[] = []

  for (const msg of messages) {
    if (msg.type === 'user' && hasLargeToolResult(msg)) {
      const compressed = compressToolResult(msg, MAX_TOOL_RESULT_CHARS)
      compressedMessages.push(compressed)
    } else {
      compressedMessages.push(msg)
    }
  }

  return { messages: compressedMessages }
}
```

**特点**：
- 不修改其他消息，prompt cache 命中率保持
- 压缩的是内容，不是结构
- 适合单次工具结果过长但上下文整体不超的场景

### Layer 3: Context Collapse（保留粒度）

**原理**：把历史段落折叠成摘要，但保留近期消息的完整形态。

```typescript
async function applyCollapsesIfNeeded(
  messages: Message[],
  toolUseContext: ToolUseContext,
  querySource: string,
): Promise<{ messages: Message[] }> {
  const collapseThreshold = getContextWindowForModel(model) * 0.9

  if (tokenCount(messages) < collapseThreshold) {
    return { messages }
  }

  // 分段折叠：每 N 条消息压缩成 1 条摘要
  const segments = segmentMessages(messages, segmentSize = 20)
  const collapsedSegments: Message[] = []

  for (const segment of segments) {
    const summary = await generateSummary(segment)  // 调用 API
    collapsedSegments.push(createSummaryMessage(segment, summary))
  }

  // 保留最近 2 段不折叠（保持近期上下文完整）
  return {
    messages: [
      ...collapsedSegments.slice(0, -2),
      ...segments.slice(-2),  // 保留最后 2 段
    ]
  }
}
```

**特点**：
- 折叠后可回滚（摘要消息保留原消息引用）
- 保留最近的完整上下文，模型仍然可以访问最新信息
- 适合中等长度对话

### Layer 4: Auto Compact（全量摘要）

**原理**：调用专门的小模型生成对话摘要，替换整个历史。

```typescript
async function autoCompactIfNeeded(
  messages: Message[],
  toolUseContext: ToolUseContext,
  ...
): Promise<{ compactionResult?: CompactionResult }> {
  const model = toolUseContext.options.mainLoopModel
  const threshold = getAutoCompactThreshold(model)  // 93% 窗口大小

  if (tokenCount(messages) < threshold) {
    return { wasCompacted: false }
  }

  // 调用摘要模型
  const summary = await compactConversation(messages, toolUseContext, {
    isAutoCompact: true,
    suppressUserQuestions: true,
  })

  return {
    compactionResult: {
      summaryMessages: [summary],
      preCompactTokenCount: tokenCount(messages),
      postCompactTokenCount: summary.tokens,
    }
  }
}
```

**特点**：
- 最高的压缩率（可从 200k token 压到 2k）
- 需要额外的 API 调用（使用便宜的小模型）
- 摘要消息保留关键决策和文件路径

### Layer 5: Reactive Compact（被动响应）

**原理**：API 返回 413 时才触发，作为其他策略失效后的最后防线。

```typescript
async function tryReactiveCompact(params): Promise<CompactionResult | null> {
  // 等待 API 返回 413（prompt_too_long）
  const response = await callModel(params)

  if (response.error !== 'prompt_too_long') {
    return null  // 不需要压缩
  }

  // 413 错误，触发紧急压缩
  return await compactConversation(messages, {
    isAutoCompact: false,
    suppressUserQuestions: true,
  })
}
```

**与 Auto Compact 的区别**：
| 方面 | Auto Compact | Reactive Compact |
|------|--------------|-----------------|
| 触发时机 | 上下文达到 93% | API 返回 413 |
| 目的 | 预防性压缩 | 补救性压缩 |
| 失败代价 | 浪费一次 API 调用 | 用户看到错误消息 |

## 熔断器设计

连续失败多次后停止重试：

```typescript
const MAX_CONSECUTIVE_FAILURES = 3

type AutoCompactTrackingState = {
  consecutiveFailures?: number  // 连续失败次数
}

// 在 autoCompactIfNeeded 中
if (tracking?.consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) {
  logForDebugging('Circuit breaker: skipping autocompact after 3 failures')
  return { wasCompacted: false }
}

// 成功后重置
return { wasCompacted: true, consecutiveFailures: 0 }

// 失败后增加
return { wasCompacted: false, consecutiveFailures: prev + 1 }
```

## Withhold 模式

错误不立即暴露，尝试内部恢复：

```typescript
// 流式输出中
if (isPromptTooLong(message)) {
  withheld = true  // 不 yield
}

// 流结束后尝试恢复
if (withheld) {
  const compacted = await tryReactiveCompact(...)
  if (compacted) {
    // 恢复成功，继续新的查询
    state = { messages: compacted.messages, transition: { reason: 'reactive_compact_retry' } }
    continue
  }
  // 恢复失败，暴露错误
  yield withheldMessage
}
```

## 各层触发条件速查

| 层 | 触发条件 | 触发时机 | API 调用 | 压缩率 |
|----|---------|---------|---------|-------|
| Snip | 消息数 > 500 | 每轮之前 | 无 | 低 |
| Microcompact | 单个结果 > 50k chars | 每轮之前 | 无 | 中 |
| Collapse | 上下文 > 90% | 每轮之前 | 是（摘要） | 高 |
| Auto Compact | 上下文 > 93% | 每轮之前 | 是（摘要） | 最高 |
| Reactive | API 413 | API 返回后 | 是（摘要） | 最高 |

## 恢复优先级

当 `prompt_too_long` 发生时，按以下顺序尝试：

1. **Collapse Drain** — 排空已 staged 的折叠（便宜，保持粒度）
2. **Reactive Compact** — 紧急全量摘要
3. **Surface Error** — 放弃，向用户展示错误

## 实现检查清单

- [ ] Snip：消息数超阈值时自动删除旧消息
- [ ] Microcompact：单个工具结果超阈值时压缩
- [ ] Collapse：上下文接近阈值时折叠历史段落
- [ ] Auto Compact：摘要生成前抑制用户问题
- [ ] Reactive Compact：API 错误时立即尝试压缩
- [ ] 熔断器：连续失败 3 次后停止
- [ ] Withhold：错误不立即暴露，尝试内部恢复
- [ ] 重置计数器：成功压缩后重置连续失败计数
