---
name: "AI Generation"
slug: ad-production-ai-generation
version: "1.0.0"
description: "AI生成技能 - 负责广告创意的AI生成处理"
changelog: "初始版本"
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":[]}}}
---

# AI Generation - 广告创意AI生成

负责广告创意的AI生成处理，包括文案生成、图像生成、视频生成等功能。

## Setup

无需额外依赖，TypeScript编译后使用。

## When to Use

需要生成广告创意内容时使用：
- 广告文案生成
- 营销图片生成
- 视频素材制作
- 创意素材批量生成

## Architecture

```
ai-generation/
├── index.ts          # 主入口，处理生成任务
└── package.json      # 依赖配置
```

## Core Commands

### 创建生成任务
```typescript
await api.executeAction('ai-generation.create', {
  demandId?: string,     // 关联的需求ID
  prompt: string,        // 生成提示词
  model?: string,        // 使用的模型（默认flux）
  params?: Record<string, any>,  // 额外参数
  count: number          // 生成数量
});
```

### 查询生成任务
```typescript
await api.executeAction('ai-generation.get', {
  taskId: string         // 任务ID
});
```

### 取消生成任务
```typescript
await api.executeAction('ai-generation.cancel', {
  taskId: string         // 任务ID
});
```

## 响应事件

- `ai-generation.completed` - 生成完成
- `ai-generation.failed` - 生成失败
- `ai-generation.progress` - 进度更新

## Configuration

配置项（通过OpenClaw配置系统）：
- `defaultModel`: 默认使用的AI模型
- `maxConcurrent`: 最大并发数
- `timeout`: 超时时间（秒）