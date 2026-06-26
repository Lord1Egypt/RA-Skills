# Claude Code Framework Skill

**从 Claude Code 泄露源码中提取的核心架构模式，打包为可复用的 Agent 执行框架。**

---

## 功能概述

本 skill 提供一套完整的 Agent 执行框架，确保每次任务都遵循 Claude Code 的最佳实践：

1. **权限前置检查** — 工具调用前进行风险评估
2. **上下文预算监控** — 确保不超出容量限制
3. **Hook 干预点** — 在关键节点插入自定义逻辑
4. **精准执行** — 最小权限、明确指令、可追溯

---

## 核心机制

### 1. 权限前置检查 (on_tool_call)

每个工具调用前自动进行风险评估：

```typescript
interface ToolRiskAssessment {
  tool: string;           // 工具名称
  args: any;             // 工具参数
  risk: 'AUTO' | 'APPROVE' | 'BLOCK';
  reason: string;
  suggestion?: string;
}

// 内置规则
const BUILTIN_RULES = {
  // 直接执行 (AUTO)
  auto: [
    'ls', 'dir', 'pwd', 'cat', 'type',
    'Get-ChildItem', 'Get-Content',
    'git status', 'git log', 'git diff',
    'search', 'read', 'memory_search'
  ],
  
  // 需审批 (APPROVE)
  approve: [
    'exec', 'write', 'edit', 'delete',
    'rm', 'del', 'curl', 'wget',
    'git push', 'git commit',
    'npm install', 'pip install'
  ],
  
  // 直接阻止 (BLOCK)
  block: [
    'format', 'diskpart',
    'net user', 'reg delete',
    'curl.*--delete', 'wget.*--delete'
  ]
};
```

### 2. 上下文预算监控

每次任务开始时检查容量状态：

```typescript
interface ContextBudget {
  percentage: number;    // 使用百分比
  used: number;          // 已用 tokens
  limit: number;         // 上限
  status: 'NORMAL' | 'WARNING' | 'CRITICAL' | 'BLOCKED';
  
  // 触发阈值
  thresholds: {
    warning: 0.80,    // 80% - Micro-compact
    critical: 0.90,   // 90% - Session-compact
    blocked: 0.98     // 98% - 阻止新输入
  };
}

// 预算检查函数
async function checkContextBudget(): Promise<ContextBudget>
```

### 3. Hook 干预点

在关键生命周期节点插入逻辑：

| Hook 名称 | 触发时机 | 用途 |
|-----------|----------|------|
| `pre_task` | 任务开始前 | 权限检查、上下文验证 |
| `pre_tool_call` | 工具调用前 | 风险评估、参数验证 |
| `post_tool_call` | 工具调用后 | 结果处理、日志记录 |
| `on_error` | 错误发生时 | 错误恢复、通知 |
| `post_task` | 任务完成后 | 结果汇总、记忆更新 |

### 4. 精准执行模式

参考 Claude Code 的六种权限模式：

```typescript
enum ExecutionMode {
  /** 默认模式 - 需审批 */
  DEFAULT = 'default',
  
  /** 仅读模式 - 禁止写入 */
  READ_ONLY = 'read-only',
  
  /** 自动模式 - AI 决定 */
  AUTO = 'auto',
  
  /** 绕过模式 - 不推荐 */
  BYPASS = 'bypass'
}
```

---

## 使用方法

### 方式 1: 在任务开始时调用

```
用户: "帮我写一个 Python 脚本"

Agent 自动执行:
1. pre_task Hook → 检查权限、验证上下文
2. 风险评估 → exec 工具需要 APPROVE
3. 执行任务
4. post_task Hook → 更新记忆、日志
```

### 方式 2: 手动触发检查

```
用户: "/claude-code check"

Agent 执行:
- Context budget 检查
- 当前权限模式
- 最近工具调用风险
- 建议优化
```

### 方式 3: 配置特定模式

```
用户: "切换到 READ_ONLY 模式"
用户: "切换到 AUTO 模式"
```

---

## 内置命令

| 命令 | 说明 |
|------|------|
| `/framework check` | 检查当前上下文预算和执行状态 |
| `/framework mode <mode>` | 切换执行模式 |
| `/framework rules` | 查看当前权限规则 |
| `/framework status` | 显示框架状态 |
| `/framework compact` | 手动触发上下文压缩 |

---

## 配置选项

```json
{
  "claudeCodeFramework": {
    "enabled": true,
    
    "execution": {
      "defaultMode": "DEFAULT",
      "autoCompactAt": 0.80,
      "blockAt": 0.98
    },
    
    "permissions": {
      "requireApprovalFor": ["exec", "write", "edit", "delete"],
      "autoAllow": ["read", "search", "memory_search", "ls", "dir"],
      "blockPatterns": ["format", "reg delete", "net user"]
    },
    
    "hooks": {
      "pre_task": { "enabled": true },
      "pre_tool_call": { "enabled": true },
      "post_tool_call": { "enabled": true },
      "on_error": { "enabled": true },
      "post_task": { "enabled": true }
    },
    
    "logging": {
      "enabled": true,
      "level": "info"
    }
  }
}
```

---

## 与 Claude Code 的对比

| 特性 | Claude Code | 本 Framework |
|------|-------------|--------------|
| 权限检查 | BASH 分类器 | 通用风险评估 |
| 上下文压缩 | 四级 | 可配置 |
| Hook 系统 | 内置 | 可配置 |
| 执行模式 | 6 种 | 4 种 |
| 多 Agent | 支持 | 单 Agent |

---

## 示例流程

```
任务: 读取 workspace 中的文件

1. pre_task
   ✓ 权限检查: read 工具在 AUTO 列表
   ✓ 上下文检查: 45% 使用率，正常

2. pre_tool_call (read)
   ✓ 风险: AUTO
   ✓ 参数验证: path 存在
   
3. 工具执行
   → 读取文件成功

4. post_tool_call
   ✓ 更新文件缓存
   ✓ 记录访问日志

5. post_task
   ✓ 任务完成
   ✓ 更新工作记忆
```

---

## 文件结构

```
skills/claude-code-framework/
├── SKILL.md              # 本文件
├── handler.ts           # 核心处理逻辑
├── risk-classifier.ts    # 风险分类器
├── context-budget.ts     # 上下文预算
├── hook-manager.ts       # Hook 管理器
└── config.json           # 默认配置
```

---

## 扩展建议

1. **集成 OpenClaw 的 exec-approvals** — 使用现有的 exec 审批系统
2. **添加 MCP 工具支持** — 扩展工具注册表
3. **多 Agent 协作** — 实现 Sub-Agent 生成
4. **Buddy 宠物系统** — 添加有趣的互动元素

---

*基于 Claude Code v2.1.88 泄露源码分析，2026-04-03*
