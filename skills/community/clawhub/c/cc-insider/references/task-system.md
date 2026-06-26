# Task 系统

> 源码位置：`restored-src/src/Task.ts` + `restored-src/src/tasks/LocalShellTask/`

## Task vs ToolUse

| | ToolUse | Task |
|--|---------|------|
| 粒度 | 单次工具调用 | 长期运行的后台任务 |
| 生命周期 | call() 同步返回 | 可运行数分钟到数小时 |
| 状态 | 简单（成功/失败） | 复杂（pending/running/completed/failed/killed） |
| UI | 同步渲染 | 有进度、有通知、可 kill |
| 例子 | Read 一个文件 | 运行 `npm build` 30 分钟 |

**关系**：`Task` 包含 `ToolUse`（一个后台 bash 任务里可能有多次工具调用）

---

## Task 类型定义

```typescript
type TaskType =
  | 'local_bash'           // 本地 shell 命令
  | 'local_agent'          // 本地 agent（runAgent → LocalAgentTask）
  | 'remote_agent'         // 远程 CCR agent
  | 'in_process_teammate'  // 进程内 teammate
  | 'local_workflow'       // 工作流
  | 'monitor_mcp'          // MCP monitor
  | 'dream'                // 梦境任务

type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'killed'
```

## Task ID 生成算法

```typescript
const TASK_ID_PREFIXES = { local_bash: 'b', local_agent: 'a', remote_agent: 'r', ... }
const TASK_ID_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'  // 36进制

export function generateTaskId(type: TaskType): string {
  const prefix = TASK_ID_PREFIXES[type] ?? 'x'
  const bytes = randomBytes(8)  // 8字节 = 64bit
  let id = prefix
  for (let i = 0; i < 8; i++) {
    id += TASK_ID_ALPHABET[bytes[i] % 36]
  }
  return id  // 例如："b1a2f3c4d5e6g7h8"
  // 36^8 ≈ 2.8 万亿组合，足够抵御 symlink 攻击
}
```

## TaskStateBase（所有任务共享的基础状态）

```typescript
type TaskStateBase = {
  id: string
  type: TaskType
  status: TaskStatus
  description: string
  toolUseId?: string     // 关联的 ToolUse
  startTime: number
  endTime?: number
  totalPausedMs?: number
  outputFile: string     // 输出持久化路径：~/.claude/.task-output/{taskId}
  outputOffset: number   // 流式读取偏移
  notified: boolean      // 用户是否已收到通知
}
```

---

## LocalShellTask 生命周期

```typescript
// 关键状态机：
// running → backgrounded (Ctrl+Z) → running
// running → completed / failed / killed
// running → timeout (15秒) → auto-background
// running → 停滞 (45秒无输出) → 通知模型"可能在等交互输入"

// 1. spawnShellTask — 创建后台任务
async function spawnShellTask({ command, description, shellCommand, toolUseId, agentId }, ctx) {
  const taskId = generateTaskId('local_bash')
  const outputPath = getTaskOutputPath(taskId)

  // 注册到 AppState
  registerTask(taskId, { id: taskId, type: 'local_bash', status: 'running', ... })

  // 创建 ShellCommand（实际执行）
  const cmd = exec(command, signal, 'bash', {
    timeout: timeoutMs,
    stdoutToFile: outputPath,  // 输出直接写文件
    onProgress: (lastLines, allLines, totalLines, totalBytes) => { ... }
  })

  return { taskId, shellCommand: cmd }
}

// 2. runShellCommand — generator 函数，yield 进度
async function* runShellCommand({ input, abortController, ... }) {
  // Progress loop: 每秒轮询输出文件
  TaskOutput.startPolling(shellCommand.taskOutput.taskId)

  while (true) {
    const result = await Promise.race([resultPromise, progressSignal])
    if (result !== null) {
      yield { type: 'progress', ... }
      return result
    }
    yield { type: 'progress', fullOutput, output: lastLines, elapsedTimeSeconds }
  }
}

// 3. auto-background — 15秒超时自动后台
if (feature('KAIROS') && getKairosActive() && isMainThread && !isBackgroundTasksDisabled) {
  setTimeout(() => {
    if (shellCommand.status === 'running' && backgroundShellId === undefined) {
      assistantAutoBackgrounded = true
      startBackgrounding('tengu_bash_command_assistant_auto_backgrounded')
    }
  }, ASSISTANT_BLOCKING_BUDGET_MS).unref()  // 15秒
}

// 4. 停滞检测 — 45秒无输出且像交互提示
const STALL_THRESHOLD_MS = 45_000
// 如果输出停止增长且最后一行像提示符（y/n, Continue? 等）
// → 发通知告知模型"命令可能在等交互输入"
```

---

## Task 通知机制（XML 格式）

```typescript
function enqueueShellNotification(taskId, description, status, exitCode, setAppState, toolUseId) {
  // 原子检查：防止重复通知
  let shouldEnqueue = false
  updateTaskState(taskId, setAppState, task => {
    if (task.notified) return task
    shouldEnqueue = true
    return { ...task, notified: true }
  })

  const message = `<${TASK_NOTIFICATION_TAG}>
<${TASK_ID_TAG}>${taskId}</${TASK_ID_TAG}>
<${OUTPUT_FILE_TAG}>${outputPath}</${OUTPUT_FILE_TAG}>
<${SUMMARY_TAG}>${escapeXml(summary)}</${SUMMARY_TAG}>
</${TASK_NOTIFICATION_TAG}>`

  enqueuePendingNotification({ value: message, mode: 'task-notification', priority: 'next' })
}

// Coordinator 的 system prompt 说明：
// "Worker results and system notifications are internal signals,
//  not conversation partners — never thank or acknowledge them."
```

---

## Task 类型一览

| Task 类型 | 源码 | 说明 |
|-----------|------|------|
| local_bash | `tasks/LocalShellTask/` | 本地 shell 命令，spawnShellTask |
| local_agent | `tasks/LocalAgentTask/` | 本地 agent，runAgent |
| remote_agent | `tasks/RemoteAgentTask/` | 远程 CCR agent |
| in_process_teammate | `tasks/InProcessTeammate/` | 进程内 teammate |
| local_workflow | `tasks/WorkflowTask/` | 工作流 |
| monitor_mcp | `tasks/MonitorMcp/` | MCP 状态监控 |
| dream | `tasks/Dream/` | 梦境任务（creative mode） |
