# Context 系统

> 源码位置：`restored-src/src/context.ts` + `restored-src/src/bootstrap/state.ts`

## 两个 Memoized Context

```typescript
// context.ts
export const getSystemContext = memoize(async () => ({
  gitStatus,         // session 期间缓存，不重复读取
  cacheBreaker,      // 仅 ant debug 用
}))

export const getUserContext = memoize(async () => ({
  claudeMd,          // CLAUDE.md 内容（支持多层嵌套）
  currentDate,       // 格式化日期
}))

// memoize 缓存：session 期间只读一次磁盘
// 失效条件：setSystemPromptInjection()（ant 特有）
```

---

## CLAUDE.md 嵌套机制

```typescript
// bootstrap/state.ts — CLAUDE.md 嵌套加载
// 子目录的 CLAUDE.md 自动附加到父目录的 CLAUDE.md
// loadedNestedMemoryPaths Set：防止同一路径被注入两次
// FileStateCache eviction 后 .has() 可能漏检 → 但 Set 知道已注入

// 嵌套示例：
// /project/CLAUDE.md      → 主配置
// /project/src/CLAUDE.md   → 追加到主配置
// /project/src/utils/CLAUDE.md → 追加到 src 的配置
```

---

## renderedSystemPrompt 的 fork-safe 设计

```typescript
// ToolUseContext.renderedSystemPrompt
// 在 turn 开始时冻结（freeze），fork 时克隆给子进程

// 为什么需要 freeze：
// 因为 fork 是在同一 session 里并行
// 子进程和父进程共享同一份内存中的 system prompt
// 如果 fork 时 system prompt 还没渲染完（并发修改）
// 子进程和父进程看到的不一样
// freeze 保证 fork 时拿到的是完整的、确定的状态

// renderedSystemPrompt 包含：
// - 渲染后的字节数（用于 token 计数）
// - 冻结时间戳（用于判断是否 stale）
```

---

## contentReplacementState fork 克隆

```typescript
// fork 时的关键行为：
// fork 子进程必须克隆父进程的 contentReplacementState
// 因为如果子进程对同一内容做出不同的"是否太大"判断
// 父进程收到了 preview，子进程收到了全文 → 上下文不一致

// fork 场景：
// 主线程 REPL 初始化一次，不重置
// resumeAgentBackground 从 sidecar records 重建
```

---

## LRU 文件缓存（readFileState）

```typescript
// readFileState: FileStateCache
// - LRU 策略：最近最少使用的文件被 evict
// -  eviction 后 .has() 可能漏检
// - loadedNestedMemoryPaths Set 兜底：知道已注入的路径
```
