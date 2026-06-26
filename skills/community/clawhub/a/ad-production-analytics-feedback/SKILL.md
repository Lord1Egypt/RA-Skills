---
name: "Analytics Feedback"
slug: ad-production-analytics-feedback
version: "1.0.0"
description: "数据分析与反馈技能 - 投放效果数据采集、分析与模型迭代建议"
changelog: "初始版本"
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[]}}}
---

# Analytics Feedback - 数据分析与反馈

负责广告投放效果的数据采集、分析和反馈，为模型优化提供建议。

## Setup

无需额外依赖，TypeScript编译后使用。

## When to Use

- 收集广告投放数据
- 分析投放效果
- 生成数据报告
- 提供优化建议

## Architecture

```
analytics-feedback/
├── index.ts          # 主入口，数据处理和分析
├── package.json      # 依赖配置
└── README.md         # 详细文档
```

## Core Commands

### 采集数据
```typescript
await api.executeAction('analytics-feedback.collect', {
  campaignId: string,   // 广告活动ID
  startTime: string,    // 开始时间
  endTime: string,      // 结束时间
  metrics?: string[]    // 指标列表
});
```

### 分析数据
```typescript
await api.executeAction('analytics-feedback.analyze', {
  data: any[],          // 原始数据
  analysisType?: string // 分析类型
});
```

### 生成报告
```typescript
await api.executeAction('analytics-feedback.report', {
  analysisId: string,   // 分析ID
  format?: string      // 报告格式
});
```

## 响应事件

- `analytics-feedback.data-collected` - 数据采集完成
- `analytics-feedback.analysis-complete` - 分析完成
- `analytics-feedback.report-ready` - 报告就绪