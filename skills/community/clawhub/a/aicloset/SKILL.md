---
name: aicloset
description: AI智能衣橱 — 衣橱管理、AI搭配推荐、知识库搜索、虚拟试衣
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - AICLOSET_API_KEY
      bins:
        - curl
    primaryEnv: AICLOSET_API_KEY
---

# AI Closet（爱搭衣橱）

AI 驱动的智能衣橱管理平台。管理衣橱和单品、获取 AI 搭配推荐、搜索服饰知识库、体验虚拟试衣。

## 鉴权

所有接口需要 API Key，支持两种方式传递：

| 方式 | 示例 |
|------|------|
| HTTP Header | `x-api-key: YOUR_API_KEY` |
| Query 参数 | `?api_key=YOUR_API_KEY` |

API Key 通过环境变量 `AICLOSET_API_KEY` 获取。

API Key 已绑定特定用户身份，所有接口自动使用绑定用户的数据，无需传 user_id。

## Base URL

```
https://aicloset-dev.wxbjq.top
```

可通过环境变量 `AICLOSET_API_URL` 覆盖。

## 通用响应格式

所有接口统一返回 JSON：

```json
{"code": 0, "msg": "ok", "data": {...}}
```

- `code = 0` 表示成功
- `code != 0` 表示错误，`msg` 包含错误描述

常见错误码：

| 错误码 | 含义 |
|--------|------|
| 40000 | 参数校验失败 |
| 40008 | 系统错误 |
| 43100 | 鉴权失败 / API Key 无效 |
| 43600 | 衣橱错误（如名称重复） |

## 能力概要

所有接口均为 `POST` 方法。大部分接口使用 `application/x-www-form-urlencoded` 或 `application/json`，`product/add` 支持 `multipart/form-data` 文件上传。

| 接口 | 路径 | 说明 |
|------|------|------|
| 衣橱列表 | `/skill/wardrobe/list` | 查询用户衣橱列表，支持分页 |
| 创建衣橱 | `/skill/wardrobe/create` | 创建新衣橱 |
| 录入单品 | `/skill/product/add` | 上传服饰图片，AI 自动识别分类 |
| 编辑单品 | `/skill/product/edit` | 修改单品名称 |
| 搭配列表 | `/skill/outfit/list` | 查询用户搭配列表，支持分页 |
| 推荐搭配 | `/skill/outfit/recommend` | 按使用频率推荐搭配方案 |
| OOTD 记录照片 | `/skill/ootd/record-photo` | 记录每日穿搭照片 |
| OOTD 记录搭配 | `/skill/ootd/record-outfit` | 记录每日穿搭搭配方案 |
| AI 搭配推荐 | `/skill/ai/outfit-recommend` | 根据场景、风格、天气智能推荐搭配 |
| 知识库搜索 | `/skill/ai/kb-search` | 搜索服饰知识库，支持品类和风格过滤 |
| 虚拟试衣 | `/skill/ai/virtual-tryon` | 将服饰图片合成到模特身上 |

## 使用场景

**衣橱管理**：创建衣橱 → 上传服饰图片录入单品 → 查看和编辑单品信息

**搭配推荐**：查询已有搭配 → 获取使用频率推荐 → 使用 AI 根据场景生成新搭配

**每日穿搭**：选择搭配或拍照 → 记录 OOTD → 关联日期和天气信息

**AI 能力**：搜索知识库找灵感 → AI 推荐搭配方案 → 虚拟试衣预览效果

## 详细 API 文档

- [衣橱与单品管理](api-wardrobe.md) — wardrobe/list, wardrobe/create, product/add, product/edit
- [搭配与 OOTD](api-outfit.md) — outfit/list, outfit/recommend, ootd/record-photo, ootd/record-outfit
- [AI 能力](api-ai.md) — ai/outfit-recommend, ai/kb-search, ai/virtual-tryon
