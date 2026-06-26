# 架构全景

> 源码位置：`restored-src/src/`

## 三层核心模型

```
用户输入
    ↓
QueryEngine
    ↓
Tools (Tool[])  ← 工具定义（buildTool 工厂）
    ↓
Tool.call()    ← 执行层（ToolUseContext 包含所有运行时状态）
    ↓
Task           ← 后台任务封装（local_bash/local_agent/remote_agent/in_process_teammate）
    ↓
outputFile     ← 结果持久化到磁盘（超过 maxResultSizeChars 时）
    ↓
renderToolResultMessage()  ← React UI 渲染
    ↓
ToolResultBlockParam  ← 返回给模型
```

**核心三层**：
- **Tool**：接口定义 + buildTool 工厂（只管"是什么工具"）
- **ToolUse**：Tool.call() 的执行上下文，包含 abortController、messages、contentReplacementState 等运行时状态
- **Task**：后台任务的封装，追踪状态（pending/running/completed/failed/killed）

---

## 子系统关系图

```
ToolUseContext
├── options.tools          ← 所有可用工具
├── options.commands       ← 所有命令/skills（MCP 也在这里）
├── messages               ← 对话历史
├── contentReplacementState ← Token 预算控制
├── renderedSystemPrompt   ← fork 时克隆
└── readFileState          ← LRU 文件缓存

Tool.call()
├── Hooks('PreToolUse')
├── checkPermissions()
├── 实际执行
├── Hooks('PostToolUse')
└── 返回 ToolResult

Task（封装层）
├── local_bash    → LocalShellTask
├── local_agent   → runAgent → LocalAgentTask
├── remote_agent  → RemoteAgentTask
├── in_process_teammate → 进程内通信
└── monitor_mcp   → MCP 状态监控
```

---

## 扩展机制：Skills / Commands / MCP

三者底层是同一个类型 `Command`：

```typescript
type Command = {
  type: 'command' | 'skill'
  name: string
  prompt?: string
  description?: string
  whenToUse?: string       // ToolSearch 自动发现
  argumentHint?: string
  allowedTools?: string[]
  paths?: string[]         // glob 模式路径过滤
  hooks?: HooksSettings
}
```

**加载优先级**（高→低）：`.claude/`（项目）> `~/.claude/`（用户）> `plugin/`

**Skills 触发方式**：
1. 显式：`/skill-name`
2. 自动发现：ToolSearch 根据 `description`/`whenToUse` 匹配
3. 路径过滤：`paths` 下自动激活

---

## 各子系统源码位置

| 子系统 | 源码位置 |
|--------|----------|
| Tool 接口 | `src/Tool.ts` |
| ToolUseContext | `src/Tool.ts` |
| Task 系统 | `src/Task.ts` |
| LocalShellTask | `src/tasks/LocalShellTask/` |
| AgentTool | `src/tools/AgentTool/` |
| Coordinator | `src/coordinator/` |
| Hooks | `src/types/hooks.ts` |
| Context | `src/context.ts` |
| BashTool | `src/tools/BashTool/` |
| MCP 集成 | `src/skills/mcpSkillBuilders.ts` |
| 命令注册 | `src/commands.ts` |
| Agent 定义加载 | `src/tools/AgentTool/loadAgentsDir.ts` |
