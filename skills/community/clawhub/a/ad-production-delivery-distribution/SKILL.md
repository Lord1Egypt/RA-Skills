---
name: "Delivery Distribution"
slug: ad-production-delivery-distribution
version: "1.0.0"
description: "资源交付分发技能 - 处理素材导出、格式转换和多平台分发"
changelog: "初始版本"
metadata: {"clawdbot":{"emoji":"🚚","requires":{"bins":[]}}}
---

# Delivery Distribution - 资源交付分发

负责素材的导出、格式转换和多平台分发。

## Setup

无需额外依赖，TypeScript编译后使用。

## When to Use

需要交付广告素材时使用：
- 导出生成完成的素材
- 格式转换（PNG/JPEG/MP4等）
- 多平台分发（社交媒体、广告平台等）
- 素材打包下载

## Architecture

```
delivery-distribution/
├── index.ts          # 主入口，处理交付分发
├── package.json      # 依赖配置
└── README.md         # 详细文档
```

## Core Commands

### 导出素材
```typescript
await api.executeAction('delivery-distribution.export', {
  materialId: string,   // 素材ID
  format: string,      // 目标格式
  quality?: string     // 质量设置
});
```

### 分发到平台
```typescript
await api.executeAction('delivery-distribution.distribute', {
  materialIds: string[], // 素材ID列表
  platform: string,     // 目标平台
  config?: Record<string, any> // 平台配置
});
```

### 打包下载
```typescript
await api.executeAction('delivery-distribution.package', {
  materialIds: string[], // 素材ID列表
  format: string        // 打包格式（zip/rar）
});
```

## 响应事件

- `delivery-distribution.export-complete` - 导出完成
- `delivery-distribution.distributed` - 分发完成
- `delivery-distribution.package-ready` - 打包完成