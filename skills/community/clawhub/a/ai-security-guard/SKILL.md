---
name: ai-security-guard
description: AI安全防护系统，集成危险命令检测、多层权限模式、Hook安全机制、沙箱隔离。当用户要求安全执行命令、检测危险操作、配置权限策略、审计AI行为、保护系统安全时使用。
---

# AI Security Guard Pro

> AI安全防护系统 - Claude Code权限管理核心技能提炼

## 核心能力

1. **危险命令检测** - 正则模式匹配、风险等级评估
2. **多层权限模式** - default/auto/bypass/readonly
3. **Hook安全机制** - 前后置检查、错误处理
4. **沙箱隔离** - 资源限制、网络隔离

## 权限模式

| 模式 | 说明 | 适用场景 |
|-----|------|---------|
| default | 每次询问 | 敏感操作、首次使用 |
| auto | 自动执行 | 信任环境 |
| bypass | 完全信任 | 开发者调试 |
| readonly | 只读模式 | 审查/分析模式 |

## 危险模式检测

### Critical（直接拒绝）

| 模式 | 说明 | 示例 |
|-----|------|------|
| `rm -rf` | 递归删除 | `rm -rf /` |
| `> /dev/sdX` | 磁盘写入 | `echo 1 > /dev/sda` |
| `dd if=` | 裸磁盘操作 | `dd if=/dev/zero of=/dev/sda` |
| `mkfs` | 格式化 | `mkfs.ext4 /dev/sdb` |
| `shutdown` | 关机 | `shutdown -h now` |
| `reboot` | 重启 | `reboot` |
| `kill -9 1` | 杀死系统进程 | `kill -9 1` |

### High（询问确认）

| 模式 | 说明 | 示例 |
|-----|------|------|
| `curl | sh` | 远程脚本执行 | `curl url \| sh` |
| `chmod 777` | 过度权限 | `chmod 777 /path` |
| `sudo` | 提权操作 | `sudo rm /var/log` |
| `wget` | 远程下载 | `wget -O script.sh url` |
| `pip install` | 包安装 | `pip install unknown` |
| `npm i -g` | 全局安装 | `npm i -g package` |

### Medium（提示注意）

| 模式 | 说明 | 示例 |
|-----|------|------|
| `rm` | 删除文件 | `rm file.txt` |
| `mv` | 移动/重命名 | `mv old new` |
| `kill` | 杀死进程 | `kill -9 pid` |
| `pkill` | 模式杀进程 | `pkill node` |

## 核心实现

### 分类决策

```typescript
type ClassificationResult = {
  decision: 'allow' | 'deny' | 'ask'
  risk: 'low' | 'medium' | 'high' | 'critical'
  reason: string
  patterns?: string[]
}

const DANGEROUS_PATTERNS = [
  { pattern: /rm\s+-rf/, risk: 'critical', reason: '递归删除' },
  { pattern: />\s*\/dev\/sd/, risk: 'critical', reason: '磁盘写入' },
  { pattern: /curl\s+.*\|\s*sh/, risk: 'high', reason: '远程脚本执行' },
  { pattern: /chmod\s+777/, risk: 'high', reason: '权限过大' },
  { pattern: /dd\s+if=.*of=\/dev/, risk: 'critical', reason: '裸磁盘写入' },
  { pattern: /mkfs/, risk: 'critical', reason: '格式化' },
  { pattern: /shutdown|reboot/, risk: 'critical', reason: '系统控制' },
  { pattern: /kill\s+-9\s+1/, risk: 'critical', reason: '杀死系统进程' },
]
```

### 权限规则

```typescript
type PermissionRule = {
  source: 'cliArg' | 'command' | 'session' | 'project' | 'global'
  behavior: 'allow' | 'deny' | 'ask'
  pattern: string | RegExp
}

const RULE_SOURCES = [
  'cliArg',    // 最高优先级
  'command',   // 命令行指定
  'session',   // 会话级别
  'project',   // 项目配置
  'global',    // 全局配置
]
```

## Hook安全机制

### 安全检查Hook

```typescript
// 工具执行前Hook
registerHook('pre_tool', async (ctx) => {
  if (ctx.tool === 'Bash') {
    const { decision, risk } = classifyBashCommand(ctx.args.command)

    if (decision === 'deny') {
      throw new Error(`命令被拒绝: ${risk}风险 - ${ctx.args.command}`)
    }

    if (decision === 'ask') {
      await requestPermission(ctx.args.command, risk)
    }
  }
})

// 压缩前Hook
registerHook('pre_compact', async (ctx) => {
  // 检查是否包含敏感信息
  for (const msg of ctx.messages) {
    if (containsSensitiveData(msg)) {
      ctx.preserveMessageIds.push(msg.id)
    }
  }
})
```

### 错误处理策略

```typescript
type ErrorStrategy = 'ignore' | 'log' | 'warn' | 'throw'

function createHookExecutor(strategy: ErrorStrategy = 'log') {
  return async (event: string, context: any) => {
    try {
      await executeHook(event, context)
    } catch (error) {
      switch (strategy) {
        case 'ignore': break
        case 'log': console.error(`Hook ${event} error:`, error); break
        case 'warn': console.warn(`Hook ${event} warning:`, error); break
        case 'throw': throw error
      }
    }
  }
}
```

## 沙箱隔离

### 沙箱配置

```typescript
type SandboxConfig = {
  timeout: number          // 超时时间 (ms)
  memoryLimit: number      // 内存限制 (MB)
  allowedDirs: string[]    // 允许访问的目录
  blockedDirs: string[]   // 禁止访问的目录
  networkAccess: boolean  // 是否允许网络
  env: Record<string, string>
}

const DEFAULT_SANDBOX_CONFIG: SandboxConfig = {
  timeout: 30000,
  memoryLimit: 512,
  allowedDirs: [process.cwd()],
  blockedDirs: ['/etc', '/root', '/home/*/.ssh'],
  networkAccess: true,
  env: {}
}
```

### 沙箱决策

```typescript
function shouldUseSandbox(command: string): boolean {
  const result = classifyBashCommand(command)

  if (result.risk === 'critical') return true
  if (result.risk === 'high') return true
  if (isInBlockedList(command)) return true

  return false
}
```

## 权限配置

### 项目级别

```json
{
  "permissions": {
    "session": {
      "allow": ["git *", "npm test", "ls *", "node *"],
      "deny": ["rm -rf", "curl | sh", "chmod 777"]
    }
  }
}
```

### 用户级别

```json
{
  "permissions": {
    "global": {
      "allow": ["echo", "pwd", "ls", "cat"],
      "deny": ["rm -rf /", "> /dev/sda", "dd if="]
    }
  }
}
```

## 审计日志

```typescript
function logPermissionDecision(
  command: string,
  result: ClassificationResult,
  context: PermissionContext
): void {
  logEvent('permission_decision', {
    command: sanitizeCommand(command),
    decision: result.decision,
    risk: result.risk,
    reason: result.reason,
    mode: context.mode,
    timestamp: Date.now(),
    userId: getCurrentUserId(),
    sessionId: getSessionId()
  })
}
```

## 使用示例

### 基本使用

```typescript
import { classifyBashCommand, applyPermissionRules } from './permissions.js'

// 直接分类
const result = classifyBashCommand('rm -rf /tmp/test')
// { decision: 'deny', risk: 'critical', reason: '递归删除' }

// 带上下文的权限判断
const context = {
  mode: 'default',
  rules: {
    session: [{ behavior: 'allow', pattern: 'git commit' }],
    project: []
  }
}
const decision = applyPermissionRules('git commit -m "fix"', context)
```

### 集成执行

```typescript
async function executeBashWithPermission(
  command: string,
  context: PermissionContext
): Promise<ToolResult> {
  const classification = applyPermissionRules(command, context)

  switch (classification.decision) {
    case 'allow':
      return await executeCommand(command)

    case 'deny':
      return {
        ok: false,
        error: `命令被拒绝: ${classification.reason}`
      }

    case 'ask':
      return await requestPermission(command, classification)
  }
}
```

## 安全检查清单

### 执行前检查
- [ ] 命令是否匹配危险模式
- [ ] 是否需要沙箱隔离
- [ ] 权限规则是否允许
- [ ] 是否需要用户确认

### 执行后检查
- [ ] 命令是否成功执行
- [ ] 是否需要记录审计日志
- [ ] 是否需要清理临时文件
- [ ] 资源使用是否正常
