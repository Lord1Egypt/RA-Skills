---
name: claude-code-mastery
description: Claude Code v2.1.88 深度掌握。整合架构体系、源码解析、实战模式。涵盖 Tool/Task/Agent 三层模型、Coordinator 协调、Hooks 钩子、权限系统、Context 缓存、MCP 集成。触发场景：理解 Claude Code 内部工作原理、行为异常诊断、扩展开发（Tool/Skill/Agent）、深度研究。
triggers:
  - Claude Code 源码分析
  - Claude Code 内部是怎么工作的
  - Claude Code 架构设计
  - Claude Code Tool 怎么实现
  - Claude Code Task 生命周期
  - Claude Code Agent spawn fork
  - Claude Code Coordinator 协调
  - Claude Code Hooks 钩子
  - Claude Code 权限系统
  - Claude Code Context 缓存
  - Claude Code 行为异常
  - Claude Code 扩展开发
  - Claude Code Skill 怎么写
  - Claude Code 调试排查
  - Tool 和 Task 的区别
  - Agent 是怎么 spawn 的
  - Coordinator 怎么协调
  - 权限系统怎么运作
  - Context 缓存策略
---

# Claude Code Mastery

> 源码位置：`restored-src/src/`  
> 版本：v2.1.88  
> 来源：架构分析 + 源码解析 + 实战模式（三合一）

---

## 核心理念：三层架构

Claude Code 的核心是 **Tool → ToolUse → Task** 三层递进模型：

```
Tool（定义层）     → 我是什么工具，有哪些接口
ToolUse（执行层）   → 实际调用时的完整运行时状态
Task（封装层）     → 后台任务的生命周期管理
```

理解这三层的区别和交互，就掌握了 Claude Code 的骨架。

---

## 快速导航

详细内容和源码引用见各 reference 文件：

| 主题 | 参考文件 |
|------|----------|
| 架构全景、子系统关系、源码位置 | [architecture.md](references/architecture.md) |
| Tool 接口、buildTool 工厂、ToolUseContext、Zod schema | [tool-internals.md](references/tool-internals.md) |
| Task 类型、生命周期、ID 生成、LocalShellTask | [task-system.md](references/task-system.md) |
| AgentTool、spawn/fork/continue/stop、AgentDefinition | [agent-system.md](references/agent-system.md) |
| Coordinator 协调原则、Synthesize-first、决策树 | [coordinator.md](references/coordinator.md) |
| Hooks 事件类型、执行流程、匹配规则 | [hooks.md](references/hooks.md) |
| 权限模型、SedEdit 安全设计、isConcurrencySafe | [permissions.md](references/permissions.md) |
| Context 缓存、CLAUDE.md 嵌套、fork-safe 设计 | [context-system.md](references/context-system.md) |
| SKILL.md 格式、Tool 实现模板、命令注册、Prompt 精选 | [patterns.md](references/patterns.md) |
| 设计亮点、调试线索、常见问题 Q&A | [design-highlights.md](references/design-highlights.md) |

---

## 关键概念速查

### Tool ≠ 函数

Tool 是包含**接口定义 + 执行逻辑 + 权限检查 + UI渲染**的完整对象，不是简单的函数调用。

### buildTool 默认 Fail-Closed

```typescript
const TOOL_DEFAULTS = {
  isConcurrencySafe: () => false,  // 默认不允许并发
  isReadOnly: () => false,         // 默认会修改
  isDestructive: () => false,       // 默认不破坏
  checkPermissions: () => ({ behavior: 'allow' }),
}
```

### spawn vs fork vs continue

- **spawn**：独立 session，新 context
- **fork**：复用父进程 system prompt cache，在同一 session 并行
- **continue**：复用已有 context 继续执行
- **stop**：停止但不删除 session

### Coordinator 核心原则

1. 永远先 Synthesize，不 delegation of understanding
2. 并行是默认策略
3. Worker 结果 = 内部信号，不是对话伙伴

### Fork 安全三剑客

`contentReplacementState`、`renderedSystemPrompt`、`messages` 必须在 fork 时从父进程克隆，保证上下文一致。

### SedEdit 安全关键

`_simulatedSedEdit` 在 inputSchema 中被 `omit`，模型不能自己设置这个字段——防止构造任意文件写入。

---

## 扩展开发速查

### 实现新 Tool 检查清单

```
1. inputSchema — Zod schema 定义参数
2. description() — 人类可读描述（3-10 词，无句号）
3. call() — 执行逻辑，包含错误处理
4. maxResultSizeChars — 超过→写磁盘
5. checkPermissions() — 权限逻辑，默认 allow
6. toAutoClassifierInput() — 安全分类，默认空字符串
7. renderToolResultMessage() — UI 渲染
8. isConcurrencySafe() — 并发安全，默认 false
9. isReadOnly() / isDestructive() — 操作类型
10. getPath()? — 文件路径权限检查
11. preparePermissionMatcher()? — Hook pattern 匹配
```

### 添加新 Hook 事件

1. 在 `src/types/hooks.ts` 添加事件类型
2. 在相关位置调用 `hooks(event, context)`
3. 在 SKILL.md 中配置规则

### Skill 触发方式

1. 显式：`/skill-name`
2. 自动发现：ToolSearch 根据 `description`/`whenToUse` 匹配
3. 路径过滤：`paths` 字段 glob 模式

### Skills 加载优先级

`.claude/`（项目）> `~/.claude/`（用户）> `plugin/`
