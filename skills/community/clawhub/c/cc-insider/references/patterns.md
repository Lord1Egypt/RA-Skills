# 实战模式

> 源码位置：`restored-src/src/tools/` + `restored-src/src/commands/` + `restored-src/src/skills/` + `restored-src/src/commands.ts`

---

## SKILL.md 格式详解

### 完整 frontmatter

```yaml
---
name: my-custom-skill              # 必须：唯一标识（小写+连字符）
description: 做某件事的skill      # 必须：一句话描述（触发机制）
triggers:                          # 可选：自动发现的触发词
  - 触发词1
  - 触发词2
whenToUse: 当你想X的时候使用      # 可选：显式提示词
argumentHint: [--flag value]        # 可选：参数格式（用于补全）
allowedTools:                       # 可选：允许的工具白名单
  - Read
  - Glob
  - Bash(git:*)
paths:                              # 可选：路径过滤（glob 模式）
  - "src/**/*.ts"
  - "tests/**/*.py"
model: sonnet                       # 可选：指定模型
disableModelInvocation: true        # 可选：纯规则 skill，不调模型
hooks:                              # 可选：钩子配置
  preToolUse:
    - if: "Bash(git *)"
      run: "echo 'Running git'"
---
```

### Body 格式

```markdown
# Skill标题

描述这个 skill 做什么

## 目标
清晰描述目标

## 步骤

### 步骤1
做什么。**成功标准**：什么证明完成了。

**执行**：任务 agent
**产物**：这个步骤产生的数据
**人工检查点**：什么时候暂停问用户

## 规则
- 硬规则1
- 硬规则2
```

---

## 命令注册（commands.ts）

```typescript
// commands.ts — 入口文件

// 方式1：直接 import（用于 feature flag 不启用的命令）
import addDir from './commands/add-dir/index.js'
import commit from './commands/commit.js'

// 方式2：条件导入（用于 feature-gated 命令，tree-shaking 优化）
const proactive = feature('PROACTIVE') || feature('KAIROS')
  ? require('./commands/proactive.js').default
  : null

// 命令导出后统一注册到 commands[]
// 工具系统通过 Command[] 数组访问所有命令
```

### 目录结构选择

```
// 轻量命令：单文件
commands/commit.ts        → commit: Command

// 复杂命令：目录
commands/review/
  index.ts               → 导出主命令
  review.ts               → 逻辑
  pr_comments/           → 子模块
```

---

## 实现一个 Tool 的检查清单

```markdown
1. **inputSchema** — Zod schema 定义参数
2. **description()** — 人类可读描述（3-10 词，无句号）
3. **call()** — 执行逻辑，包含错误处理
4. **maxResultSizeChars** — 超过→写磁盘，默认值是多少
5. **checkPermissions()** — 权限逻辑，默认 allow
6. **toAutoClassifierInput()** — 安全分类，默认空字符串
7. **renderToolResultMessage()** — UI 渲染，可选
8. **isConcurrencySafe()** — 并发安全，默认 false
9. **isReadOnly()** — 是否只读，默认 false
10. **isDestructive()** — 是否破坏性，默认 false
11. **getPath()?** — 如果操作文件路径，定义用于权限检查
12. **preparePermissionMatcher()?** — 如果有钩子规则，实现 pattern 匹配
```

### 最小 Tool 实现

```typescript
// tools/MyTool/index.ts
import { buildTool } from '../../Tool.js'
import type { ToolDef } from '../../Tool.js'

const MyTool = buildTool({
  name: 'my-tool',
  description: async (input, { options }) => {
    return 'Does something useful with the input.'
  },
  inputSchema: z.object({
    action: z.string(),
  }),
  maxResultSizeChars: 10_000,

  async call(args, context, canUseTool) {
    // 1. 权限检查
    // 2. 执行逻辑
    return { data: { result: 'ok' } }
  },

  checkPermissions: async (input, context) => {
    return { behavior: 'allow', updatedInput: input }
  },

  renderToolResultMessage(result, progress, { theme }) {
    return <div>{result.data.message}</div>
  },

  toAutoClassifierInput(input) {
    return `my-tool ${input.action}`
  },

  isConcurrencySafe: (input) => false,
  isReadOnly: (input) => true,
})

export default MyTool
```

---

## MCP 工具集成

```typescript
// skills/mcpSkillBuilders.ts

// MCP 工具加载流程：
// 1. MCP server 连接 → 2. 获取工具列表 → 3. 包装为 deferred Tool → 4. 注册

// MCP 工具属性：
type Tool = {
  isMcp: true
  shouldDefer: true   // 默认延迟加载
  mcpInfo: { serverName: string, toolName: string }
  // _meta['anthropic/alwaysLoad'] = true → alwaysLoad=true
}

// ToolSearch 机制：
// - defer 的工具需要先被 ToolSearch"激活"
// - ToolSearch 返回工具完整描述
// - 模型选择后真正调用
// - 避免初始 schema 过大（可能有成百上千个 MCP 工具）
```

---

## Claude Code System Prompt 精选

### 核心原则（Doing Tasks 段落）

```markdown
# Doing tasks
- 用户主要请求软件工程任务。收到不明确指令时，结合上下文理解。
- 不要对没读过的代码提建议。先读懂，再改动。
- 不要创建不必要的文件。优先编辑已有文件。
- 不要添加超出需求的功能。Bug 修复不需要周边代码清理。
- 不要添加文档注释、类型注解（除非你自己改的）。
- 避免 OWASP Top 10 安全漏洞。发现写了不安全代码，立即修复。
- 不要为假设的未来需求写抽象。只为实际需要的复杂度买单。
- 写完代码后用 TaskCreateTool 分解管理任务，完成后标记。
```

### 权限安全（Executing Actions with Care 段落）

```markdown
# 执行动作要谨慎
需要确认的危险操作：
- 破坏性操作：删除文件/分支、drop 数据库表、rm -rf
- 难逆转操作：force-push、git reset --hard、amend 已发布提交
- 影响他人的操作：push 代码、创建/关闭 PR、发消息
- 上传到第三方：先确认内容是否敏感

遇到障碍时，不要用破坏性操作当捷径。
```

### 工具使用原则（Using Your Tools 段落）

```markdown
# 使用工具
- 有专用工具时，不要用 Bash 替代：
  Read → 不要 cat/head/tail/sed
  Edit → 不要 sed/awk
  Write → 不要 cat with heredoc
  Glob → 不要 find/ls
  Grep → 不要 grep/rg
- 用 TaskCreateTool 分解管理任务，完成后标记。
- 独立工具调用可以并行，减少往返。
```
