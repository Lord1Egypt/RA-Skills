---
name: "Material Library"
slug: ad-production-material-library
version: "1.0.0"
description: "素材库管理技能 - 提供素材的存储、检索、版本管理"
changelog: "初始版本"
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":[]}}}
---

# Material Library - 素材库管理

负责广告素材的存储、检索和版本管理。

## Setup

无需额外依赖，TypeScript编译后使用。

## When to Use

- 存储生成的广告素材
- 检索历史素材
- 管理素材版本
- 素材分类和标签

## Architecture

```
material-library/
├── index.ts          # 主入口，素材管理
├── package.json      # 依赖配置
└── README.md         # 详细文档
```

## Core Commands

### 存储素材
```typescript
await api.executeAction('material-library.store', {
  file: Buffer,           // 文件内容
  metadata: {            // 元数据
    name: string,
    type: string,
    tags?: string[],
    campaignId?: string
  }
});
```

### 检索素材
```typescript
await api.executeAction('material-library.search', {
  query?: string,        // 搜索关键词
  filters?: {            // 筛选条件
    type?: string,
    tags?: string[],
    dateRange?: { start: string, end: string }
  },
  limit?: number
});
```

### 获取素材
```typescript
await api.executeAction('material-library.get', {
  materialId: string     // 素材ID
});
```

### 更新版本
```typescript
await api.executeAction('material-library.update-version', {
  materialId: string,    // 素材ID
  file: Buffer,          // 新版本文件
  changelog?: string    // 版本说明
});
```

## 响应事件

- `material-library.stored` - 素材存储完成
- `material-library.updated` - 素材更新完成
- `material-library.deleted` - 素材删除