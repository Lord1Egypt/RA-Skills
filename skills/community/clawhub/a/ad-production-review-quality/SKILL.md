---
name: "Review Quality"
slug: ad-production-review-quality
version: "1.0.0"
description: "审核质检技能 - 自动化质量评估和人工审核工作流"
changelog: "初始版本"
metadata: {"clawdbot":{"emoji":"✅","requires":{"bins":[]}}}
---

# Review Quality - 审核质检

负责广告素材的质量评估和审核工作流。

## Setup

无需额外依赖，TypeScript编译后使用。

## When to Use

- 自动审核广告素材质量
- 人工审核流程管理
- 质量评估和打分
- 合规性检查

## Architecture

```
review-quality/
├── index.ts          # 主入口，审核质检逻辑
├── package.json      # 依赖配置
└── README.md         # 详细文档
```

## Core Commands

### 自动审核
```typescript
await api.executeAction('review-quality.auto-review', {
  materialId: string,    // 素材ID
  criteria?: {          // 审核标准
    resolution?: { minWidth: number, minHeight: number },
    format?: string[],
    maxFileSize?: number
  }
});
```

### 人工审核
```typescript
await api.executeAction('review-quality.manual-review', {
  materialId: string,    // 素材ID
  reviewer: string,      // 审核人
  decision: 'approved' | 'rejected' | 'revise',
  comments?: string
});
```

### 质量评估
```typescript
await api.executeAction('review-quality.assess', {
  materialId: string,    // 素材ID
  dimensions: string[]   // 评估维度
});
```

### 获取审核状态
```typescript
await api.executeAction('review-quality.get-status', {
  materialId: string     // 素材ID
});
```

## 响应事件

- `review-quality.auto-reviewed` - 自动审核完成
- `review-quality.manual-reviewed` - 人工审核完成
- `review-quality.assessed` - 质量评估完成