---
name: "Demand Management"
slug: ad-production-demand-management
version: "1.0.0"
description: "广告创意需求管理技能 - 处理需求发起、评审、拆解全流程"
changelog: "初始版本"
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":[]}}}
---

# Demand Management - 需求管理

负责广告创意需求的全流程管理，包括需求发起、评审和拆解。

## Setup

无需额外依赖，TypeScript编译后使用。

## When to Use

- 创建新的广告创意需求
- 需求评审和确认
- 需求拆解为子任务
- 跟踪需求状态

## Architecture

```
demand-management/
├── index.ts          # 主入口，需求管理逻辑
├── package.json      # 依赖配置
├── README.md         # 详细文档
└── scripts/          # 辅助脚本
```

## Core Commands

### 创建需求
```typescript
await api.executeAction('demand-management.create', {
  title: string,           // 需求标题
  description: string,     // 需求描述
  requester: string,       // 需求方
  priority?: 'low' | 'medium' | 'high',
  deadline?: string       // 截止时间
});
```

### 评审需求
```typescript
await api.executeAction('demand-management.review', {
  demandId: string,        // 需求ID
  status: 'approved' | 'rejected' | 'revised',
  comments?: string       // 评审意见
});
```

### 拆解需求
```typescript
await api.executeAction('demand-management.breakdown', {
  demandId: string,        // 需求ID
  tasks: Array<{          // 任务列表
    title: string,
    description: string,
    assignee?: string,
    estimatedHours?: number
  }>
});
```

### 更新状态
```typescript
await api.executeAction('demand-management.update-status', {
  demandId: string,        // 需求ID
  status: string          // 新状态
});
```

## 响应事件

- `demand-management.created` - 需求创建完成
- `demand-management.reviewed` - 需求评审完成
- `demand-management.broken-down` - 需求拆解完成