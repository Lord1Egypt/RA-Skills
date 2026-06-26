---
name: "Workflow Orchestrator"
slug: ad-production-workflow-orchestrator
version: "1.0.0"
description: "工作流编排中心 - 协调全流程，管理任务依赖和状态"
changelog: "初始版本"
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":[]}}}
---

# Workflow Orchestrator - 工作流编排

负责协调广告创意生产的全流程，管理任务依赖和状态。

## Setup

无需额外依赖，TypeScript编译后使用。

## When to Use

- 创建和管理工作流
- 协调多个技能协作
- 管理任务依赖关系
- 监控工作流状态

## Architecture

```
workflow-orchestrator/
├── index.ts          # 主入口，工作流编排逻辑
├── package.json      # 依赖配置
└── README.md         # 详细文档
```

## Core Commands

### 创建工作流
```typescript
await api.executeAction('workflow-orchestrator.create', {
  name: string,           // 工作流名称
  steps: Array<{          // 步骤定义
    skill: string,        // 使用的技能
    action: string,       // 动作
    input?: any,          // 输入数据
    dependsOn?: string[]  // 依赖的步骤
  }>
});
```

### 启动工作流
```typescript
await api.executeAction('workflow-orchestrator.start', {
  workflowId: string      // 工作流ID
});
```

### 暂停工作流
```typescript
await api.executeAction('workflow-orchestrator.pause', {
  workflowId: string      // 工作流ID
});
```

### 恢复工作流
```typescript
await api.executeAction('workflow-orchestrator.resume', {
  workflowId: string      // 工作流ID
});
```

### 获取状态
```typescript
await api.executeAction('workflow-orchestrator.get-status', {
  workflowId: string      // 工作流ID
});
```

### 终止工作流
```typescript
await api.executeAction('workflow-orchestrator.terminate', {
  workflowId: string      // 工作流ID
});
```

## 响应事件

- `workflow-orchestrator.started` - 工作流启动
- `workflow-orchestrator.paused` - 工作流暂停
- `workflow-orchestrator.resumed` - 工作流恢复
- `workflow-orchestrator.completed` - 工作流完成
- `workflow-orchestrator.failed` - 工作流失败
- `workflow-orchestrator.step-completed` - 步骤完成

## Configuration

工作流配置示例：
```json
{
  "timeout": 3600,        // 超时时间（秒）
  "maxRetries": 3,        // 最大重试次数
  "parallelLimit": 5      // 最大并行数
}
```