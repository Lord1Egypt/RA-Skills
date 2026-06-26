---
name: coinmeta
description: 查询加密货币快讯。触发场景：查询币圈快讯、获取加密货币新闻、crypto news、币圈资讯。
metadata:
  openclaw:
    emoji: "📰"
    primaryEnv: COINMETA_API_KEY
    requires:
      bins:
        - curl
      env:
        - COINMETA_API_KEY
    os:
      - darwin
      - linux
      - win32
    tags:
      - crypto
      - news
      - 快讯
    version: 1.0.0
---

# CoinMeta API

查询加密货币快讯数据。

**Base URL**: `https://api.coinmeta.com`
**Auth**: Header `X-Api-Key: $COINMETA_API_KEY`
**Response format**: `{"code": 200, "data": [...], "msg": "success"}` — code 200 = success

---

## 快讯列表

**Endpoint:** `POST https://api.coinmeta.com/open/v1/newsflash/list`

**curl示例:**
```bash
curl -s -X POST -H "Accept:*/*" \
  -H "X-Api-Key: ${COINMETA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"size":10}' \
  "https://api.coinmeta.com/open/v1/newsflash/list"
```

**请求参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认1 |
| size | int | 每页数量，默认10 |

**响应字段:**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 快讯ID |
| views | int | 浏览量 |
| title | string | 标题 |
| content | string | 内容（HTML） |
| createdAt | int | 创建时间戳 |

---

## 关键词搜索

**Endpoint:** `POST https://www.coinmeta.com/open/v1/newsflash/search`

```bash
curl -s -X POST -H "Accept:*/*" \
  -H "X-Api-Key: ${COINMETA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"size":10,"keyword":"btc"}' \
  "https://www.coinmeta.com/open/v1/newsflash/search"
```

**请求参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认1 |
| size | int | 每页数量，默认10 |
| keyword | string | 搜索关键词，必填 |

**输出格式:**
```
📰 加密货币快讯 · 第[N]页

1. [标题]
   浏览: [views] · [时间]
   [摘要...]

2. [标题]
   浏览: [views] · [时间]
   [摘要...]
...
```

**解析规则:**
- `createdAt` 是Unix时间戳，转换为可读时间
- `content` 包含HTML标签，需去除标签显示纯文本

---

## Error Handling

| code | msg | 说明 |
|------|-----|------|
| 401 | Missing API key | API key未设置，请设置COINMETA_API_KEY环境变量 |
| 401 | Invalid API key | API key无效，请检查是否正确 |
| 422 | 参数错误 | 请求参数有误，检查page/size等参数 |
| != 200 | 其他 | 请求失败，显示msg内容 |
| network error | - | 提示重试 |
