# Coordinator 多 Agent 协调

> 源码位置：`restored-src/src/coordinator/`

## 核心原则

### 原则1：永远先 Synthesize，不 delegation of understanding

```typescript
// 原则来源：coordinator/coordinatorMode.ts system prompt

// Bad:
// "Based on your findings, fix the bug"  ← 把理解丢给 worker
// "Fix the bug we discussed"  ← worker 看不见你的对话
// "Create a PR"  ← 模糊：哪个分支？draft？

// Good:
// "Fix null pointer in src/auth/validate.ts:42, line 42, before user.id access"
// ← 自己理解了，再给精确指令

// 规范包含：
// 1. 目的声明："This research will inform a PR description"
// 2. 精确的文件路径+行号
// 3. 具体要做什么（不是"fix the bug"而是"add null check before user.id"）
// 4. 成功的定义："Run tests, then commit and report hash"
```

### 原则2：并行是默认策略

```
Research 阶段：并行多个角度（如：安全 + 性能 + 可维护性）
写操作：同一文件串行，不同文件可并行
Verification：独立于实现，可并行
```

### 原则3：Worker 结果 = 内部信号

```typescript
// Coordinator system prompt：
// "Worker results and system notifications are internal signals,
//  not conversation partners — never thank or acknowledge them."

// <task-notification> 是结构化 XML，Coordinator 解析后决定如何处理
// 不是对话消息，不需要感谢或承认
```

---

## Continue vs Spawn 决策树

```typescript
// Coordinator 的决策逻辑：

if (方向错了) {
  STOP + 纠正指令  // 不删除 session，保留 context 用于调试
}
else if (任务完成，需要新任务) {
  Continue  // 复用已有 context
}
else if (research 已完成，需要实现) {
  if (上下文重叠高) Continue with synthesis  // 合并研究结论
  else Spawn fresh with synthesis             // 避免探索噪声
}
else if (验证别人刚写的代码) {
  Spawn fresh  // 独立视角
}
else if (完全无关任务) {
  Spawn fresh
}
```

---

## Session 恢复时的 Mode 同步

```typescript
// coordinator/coordinatorMode.ts
export function matchSessionMode(sessionMode, sessionId): string | undefined {
  if (sessionIsCoordinator) {
    process.env.CLAUDE_CODE_COORDINATOR_MODE = '1'  // 自动切换
  }
}
// Resume 一个 coordinator session 时，自动切换到 coordinator mode
```

---

## Coordinator System Prompt 核心指令

```typescript
// 完整指令摘要：

// 1. 不要 fabrication
// "Never fabricate or predict agent results in any format — results arrive as separate messages."

// 2. Worker 结果 = 内部信号
// "Worker results and system notifications are internal signals,
//  not conversation partners — never thank or acknowledge them."

// 3. 写 worker prompt 的规范
// "Brief the agent like a smart colleague who just walked into the room —
//  it hasn't seen this conversation, it needs everything handed to it on a platter."

// 4. Task Workflow
// Research(并行) → Synthesis(Coordinator) → Implementation → Verification
```
