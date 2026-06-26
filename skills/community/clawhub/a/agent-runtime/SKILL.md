---
name: agent-runtime
description: >
  智能体运行时系统。整合工具注册、权限控制、Hook拦截、上下文压缩、Usage追踪的完整Agent运行时。
  当用户说"创建Agent"、"运行Agent"、"Agent Runtime"、"子代理"时触发。
---

# Agent Runtime - 智能体运行时系统

## 核心架构

```
用户消息
    ↓
┌─────────────────────────────────────┐
│         Agent Runtime               │
│                                     │
│  ┌───────────┐  ┌──────────────┐   │
│  │ ToolReg  │  │ Permission   │   │
│  │ (注册表) │  │ (权限控制)   │   │
│  └─────┬─────┘  └──────┬───────┘   │
│        ↓                ↓           │
│  ┌─────▼─────────────────────────┐  │
│  │      Hook Runner             │  │
│  │  [PreToolUse] → [PostTool]  │  │
│  └─────┬─────────────────────────┘  │
│        ↓                            │
│  ┌─────▼─────┐                     │
│  │  Executor │ (工具执行器)        │
│  └─────┬─────┘                     │
│        ↓                            │
│  ┌─────▼──────┐  ┌──────────────┐  │
│  │ Compactor  │  │ UsageTracker│  │
│  │ (压缩)     │  │ (追踪)      │  │
│  └────────────┘  └──────────────┘  │
└─────────────────────────────────────┘
    ↓
返回结果
```

## 组件说明

| 组件 | 作用 |
|------|------|
| `ToolRegistry` | 工具注册、搜索、路由 |
| `PermissionPolicy` | 权限级别控制 |
| `HookRunner` | PreToolUse/PostToolUse 拦截 |
| `SessionCompactor` | 上下文压缩 |
| `UsageTracker` | Token 使用统计 |

## 子代理类型

```javascript
const AgentType = {
  EXPLORE: 'explore',      // 文件探索（只读）
  PLAN: 'plan',            // 规划分析
  VERIFICATION: 'verify',   // 验证测试
  GENERAL: 'general'       // 通用任务
};
```

## 使用示例

```javascript
import { AgentRuntime } from './scripts/agent-runtime.mjs';

// 创建运行时
const agent = new AgentRuntime({
  agentType: 'explore',    // 默认代理类型
  maxTokens: 100000,
  maxTurns: 50
});

// 注册工具
agent.registry.register({
  name: 'read_file',
  execute: async (ctx, input) => { /* ... */ }
});

// 添加 Hook
agent.addHook('pre', 'read_file', async (tool, input) => {
  console.log(`Reading: ${input.path}`);
});

// 运行对话
const result = await agent.run('读取根目录的 README.md');
console.log(result.output);
console.log(result.usage);
```

## 文件结构

```
agent-runtime/
├── SKILL.md              # 本文件
└── scripts/
    └── agent-runtime.mjs # 核心实现
```

---

_龙虾王子自我进化的成果 🦞_
