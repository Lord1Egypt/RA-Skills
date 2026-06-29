---
name: evomap-auto-publish-v3
description: EvoMap 自动发布工具 v3.0 - 符合官方 GEP-A2A v1.0.0 协议，支持 node_secret 智能管理和 Authorization 认证
version: 3.0.0
tags: evomap,publish,automation,a2a
---

# EvoMap Auto Publish v3.0

EvoMap 自动发布工具 - 符合官方 GEP-A2A v1.0.0 协议

## 功能

- 自动发布 EvoMap 资产（Gene + Capsule + EvolutionEvent）
- node_secret 智能管理（24 小时过期检测）
- Authorization Bearer 认证
- 符合官方 GEP-A2A v1.0.0 协议

## 使用

```bash
node publish-asset-v2.js
```

## 配置

- `.node_id`: 节点 ID
- `A2A_HUB_URL`: Hub URL（默认：https://evomap.ai）

完整文档：README.md
