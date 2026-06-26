# Tool 接口与执行上下文

> 源码位置：`restored-src/src/Tool.ts`

## Tool 的本质

Tool 不是函数，是包含**接口定义 + 执行逻辑 + 权限检查 + UI渲染**的完整对象：

```typescript
type Tool = {
  name: string

  // 四个核心方法
  call(args, context: ToolUseContext, canUseTool?, parentMessage?, onProgress?): Promise<ToolResult>
  description(input, options): Promise<string>    // 模型看到什么
  prompt(options): Promise<string>               // system prompt 描述
  checkPermissions(input, context): Promise<PermissionResult>  // 权限

  // UI 渲染（React 组件）
  renderToolResultMessage(content, progress, options): React.ReactNode
  renderToolUseMessage(input, options): React.ReactNode
  renderToolUseProgressMessage?(progress, options): React.ReactNode

  // 元数据
  maxResultSizeChars: number   // 超过→写磁盘，不塞 context
  aliases?: string[]           // 向后兼容
  searchHint?: string         // 3-10 词，用于 ToolSearch
  isMcp?: boolean
  shouldDefer?: boolean      // 延迟加载（MCP 默认 true）
}
```

---

## buildTool 工厂（Fail-Closed 默认值）

```typescript
const TOOL_DEFAULTS = {
  isEnabled: () => true,
  isConcurrencySafe: (_input) => false,    // 默认：不允许并发
  isReadOnly: (_input) => false,           // 默认：会修改
  isDestructive: (_input) => false,         // 默认：不破坏
  checkPermissions: (input, ctx) => ({ behavior: 'allow', updatedInput: input }),
  toAutoClassifierInput: (_input) => '',   // 默认不进入安全分类器
  userFacingName: (_input) => '',          // 默认用 name
}

export function buildTool<D extends ToolDef>(def: D): BuiltTool<D> {
  return { ...TOOL_DEFAULTS, userFacingName: () => def.name, ...def } as BuiltTool<D>
}
```

**设计原则**：默认值永远 fail-closed。`isConcurrencySafe=false` 意味着默认情况下模型不能同时运行两个写操作。

---

## inputSchema / outputSchema（Zod 驱动）

```typescript
// BashTool.tsx — 实际例子
const fullInputSchema = lazySchema(() => z.strictObject({
  command: z.string(),
  timeout: semanticNumber(z.number().optional()),
  description: z.string().optional(),
  run_in_background: semanticBoolean(z.boolean().optional()),
  dangerouslyDisableSandbox: semanticBoolean(z.boolean().optional()),
  _simulatedSedEdit: z.object({...}).optional()  // 内部：sed 预览结果
}))

// 对外 schema 去掉内部字段（安全）
const inputSchema = lazySchema(() => fullInputSchema().omit({ _simulatedSedEdit: true }))

// GrowthBook 条件控制：后台任务禁用时从 schema 里拿掉 run_in_background
const inputSchema = lazySchema(() => {
  return isBackgroundTasksDisabled
    ? inputSchema().omit({ run_in_background: true, _simulatedSedEdit: true })
    : inputSchema().omit({ _simulatedSedEdit: true })
})
```

`lazySchema()` 是延迟解析，schema 在第一次调用时才解析成 Zod 对象。优势：避免模块加载时的循环依赖问题。

---

## ToolUseContext（执行运行时）

```typescript
type ToolUseContext = {
  options: {
    tools: Tools                           // 工具池
    commands: Command[]                     // 所有命令/skills
    agentDefinitions: AgentDefinitionsResult
    mcpClients: MCPServerConnection[]
    maxBudgetUsd?: number
    customSystemPrompt?: string
    appendSystemPrompt?: string
  }
  abortController: AbortController          // 可取消
  messages: Message[]                       // 对话历史

  // 状态读写
  getAppState(): AppState
  setAppState(f: (prev: AppState) => AppState): void
  setAppStateForTasks?: (f: (prev: AppState) => AppState) => void  // 永远到达根 store

  // 路径去重（防止同一 CLAUDE.md 被多次注入）
  loadedNestedMemoryPaths?: Set<string>
  nestedMemoryAttachmentTriggers?: Set<string>
  dynamicSkillDirTriggers?: Set<string>
  discoveredSkillNames?: Set<string>

  // Token 预算控制
  contentReplacementState?: ContentReplacementState

  // System Prompt 缓存（fork 安全）
  renderedSystemPrompt?: SystemPrompt  // 冻结于 turn 开始

  // LRU 文件缓存
  readFileState: FileStateCache

  // Hooks
  onCompactProgress?: (event: CompactProgressEvent) => void

  // 安全审计
  toolDecisions?: Map<string, { source: string, decision: 'accept' | 'reject', timestamp: number }>
}
```

### ContentReplacementState（Token 预算控制）

```typescript
type ContentReplacementState = {
  decisions: Map<string, {
    content: string | null   // null = 已替换为磁盘路径
    charCount: number
    tokenCount: number
    replacedAt?: number
  }>
  totalTokenCount: number
  totalCharCount: number
}

// 替换触发时机：
// 1. compact 时（session 太长）
// 2. 单次 tool result 超过阈值（maxResultSizeChars）
// 3. fork 时克隆（保证 fork 和父进程决策一致）
```

### Fork 安全的关键设计

`contentReplacementState` 在 fork 时必须从父进程克隆。因为如果子进程对同一内容做出不同的"是否太大"判断：
- 父进程收到 preview（前 512 字节 + 文件路径）
- 子进程收到全文
- → 上下文不一致，模型行为错乱

`renderedSystemPrompt` 也需要 freeze 于 turn 开始：fork 时如果 prompt 还没渲染完（并发修改），子进程和父进程看到的不一样。

---

## 大结果写磁盘策略

```typescript
// 超过 maxResultSizeChars 时：
// - BashTool: 30_000 chars
// - 大多数工具: 10_000 chars

// 工具结果处理（BashTool.tsx）：
if (persistedOutputPath) {
  const preview = generatePreview(processedStdout, PREVIEW_SIZE_BYTES)
  processedStdout = buildLargeToolResultMessage({
    filepath: persistedOutputPath,
    originalSize: processedStdSize ?? 0,
    preview: preview.preview,
    hasMore: preview.hasMore
  })
}
// 模型收到：预览（前512字节）+ 文件路径
// UI 渲染：用 data.stdout（原始数据），路径对 UI 不可见
```

---

## ToolDef 可选属性

```typescript
type Tool = {
  // 延迟加载
  shouldDefer?: boolean   // MCP 工具默认 true
  alwaysLoad?: boolean    // 即使 MCP 也第一轮加载（AgentTool 需要）

  // 权限相关
  validateInput?(input, context): Promise<ValidationResult>
  getPath?(input): string  // 路径权限检查
  preparePermissionMatcher?(input): Promise<(pattern: string) => boolean>

  // UI 渲染
  renderToolUseTag?(input): React.ReactNode
  renderToolUseErrorMessage?(result, options): React.ReactNode
  renderGroupedToolUse?(toolUses, options): React.ReactNode | null

  // 安全分类
  isSearchOrReadCommand?(input): { isSearch: boolean, isRead: boolean, isList?: boolean }
}
```
