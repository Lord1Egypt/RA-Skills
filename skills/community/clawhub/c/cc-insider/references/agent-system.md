# Agent 系统

> 源码位置：`restored-src/src/tools/AgentTool/` + `restored-src/src/tools/AgentTool/loadAgentsDir.ts`

## AgentTool.call() 完整流程

```typescript
async function call({ prompt, subagent_type, description, model, run_in_background, name, team_name, mode, isolation, cwd }, toolUseContext, canUseTool, assistantMessage, onProgress) {

  // === 阶段1：路由 ===
  // 1a. team_name + name → spawnTeammate（进程内或 tmux）
  if (teamName && name) {
    return spawnTeammate({ name, prompt, team_name, ... })
  }

  // 1b. subagent_type=undefined + fork gate on → fork 路径
  const isForkPath = effectiveType === undefined
  if (isForkPath) {
    selectedAgent = FORK_AGENT  // 内置 fork agent
  }

  // === 阶段2：MCP 服务器检查 ===
  if (requiredMcpServers?.length) {
    // 等待 pending 的 MCP 服务器连接（最多等30秒）
    while (hasPendingRequiredServers && withinDeadline) {
      await sleep(500)
      refreshAppState()
    }
    // 验证工具是否真的可用（连接≠认证通过）
    const missing = requiredMcpServers.filter(s => !serversWithTools.includes(s))
    if (missing.length) {
      throw new Error(`Agent requires MCP servers that don't have tools available: ${missing.join(', ')}`)
    }
  }

  // === 阶段3：Worktree 隔离 ===
  if (isolation === 'worktree') {
    const worktreePath = await createAgentWorktree(cwd || getCwd())
    // agent 在隔离的 worktree 里工作，不影响主分支
  }

  // === 阶段4：执行路由 ===
  if (isRemoteAgent(selectedAgent)) {
    const { taskId, sessionUrl } = await registerRemoteAgentTask(...)
    return { status: 'remote_launched', taskId, sessionUrl, ... }
  }

  if (isInProcessTeammate()) {
    throw new Error('In-process teammates cannot spawn agents')
  }

  // === 本地 agent ===
  if (isForkPath) {
    const forkedMessages = buildForkedMessages(toolUseContext.messages, selectedAgent)
    return runAgent({ prompt, messages: forkedMessages, systemPrompt, ... })
  }

  const agentId = createAgentId()
  const sessionId = await createSessionForAgent(agentId, selectedAgent)
  return runAgent({ agentId, sessionId, prompt, systemPrompt, ... })
}
```

---

## spawn vs fork vs continue vs stop

### spawn（重量隔离）

```typescript
// 创建全新 session，从空白 context 开始
// 用于：独立任务、长期后台任务、避免上下文污染
const sessionId = await createSessionForAgent(agentId, selectedAgent)
return runAgent({ agentId, sessionId, prompt, systemPrompt, ... })
```

### fork（轻量并行）

```typescript
// 复用父进程的 system prompt cache + messages
// 不创建新 session ID，在同一 session 内并行
// 用于：多个研究角度需要紧密协作

// fork 时 prompt 是"directive"（指示），不是完整 briefing
// buildForkedMessages() 做两件事：
// 1. 克隆 contentReplacementState（保证决策一致性）
// 2. 注入 fork-specific system prompt（说明这是 fork）
```

### continue（延续上下文）

```typescript
// 向已存在的 agent 发消息，复用其 context
// 用于：research 结果→implementation，需要已有 context
${SEND_MESSAGE_TOOL_NAME}({ to: "xyz-456", message: "Fix null pointer in..." })
// worker 看到消息后继续执行，有之前所有文件 context
```

### stop（停止但不删除）

```typescript
// 停止 worker 但不删除 session
// 用于：方向错了，需要重新规划，但保留 context 用于调试
${TASK_STOP_TOOL_NAME}({ task_id: "xyz-456" })
${SEND_MESSAGE_TOOL_NAME}({ to: "xyz-456", message: "Stop JWT refactor. Fix null pointer..." })
```

---

## AgentDefinition（Agent 定义）

```typescript
type AgentDefinition = {
  agentType: string
  description: string           // 简短描述（ToolSearch 用）
  whenToUse?: string             // 何时使用（显式提示）
  prompt: string                // system prompt
  tools?: string[]               // 白名单
  disallowedTools?: string[]    // 黑名单
  model?: string                 // 'inherit' = 继承父 agent
  effort?: EffortValue
  permissionMode?: PermissionMode
  mcpServers?: AgentMcpServerSpec[]
  hooks?: HooksSettings
  maxTurns?: number             // 最大对话轮次
  skills?: string[]             // 附加 skills
  initialPrompt?: string        // 初始消息
  memory?: 'user' | 'project' | 'local'  // memory scope
  background?: boolean          // 是否默认后台
  isolation?: 'worktree' | 'remote'  // 隔离模式
}

// 工具过滤逻辑（双重保险）
if (hasAllowlist && hasDenylist) {
  tools.filter(t => !disallowedTools.has(t))
} else if (hasAllowlist) {
  tools
} else if (hasDenylist) {
  'All tools except ' + disallowedTools
} else {
  'All tools'
}
// 即使父 agent 允许某个工具，AgentDefinition 还能二次过滤
```

### AgentDefinition JSON 示例

```json
{
  "agentType": "code-reviewer",
  "description": "Review code changes and provide feedback",
  "whenToUse": "When you want an expert review of code changes",
  "prompt": "You are a code reviewer...",
  "tools": ["Read", "Glob", "Grep"],
  "disallowedTools": ["Bash(git push)", "Bash(git force-push)"],
  "effort": "medium",
  "maxTurns": 50,
  "memory": "project"
}
```
