---
name: followin-openapi
description: Documents Followin OpenAPI endpoints for agent integration. Use when calling feed APIs, channel feeds, trending, category feeds, or integrating with Followin OpenAPI.
metadata:
  {
    "openclaw":
      {
        "emoji": "🚀",
        "os": ["darwin", "linux", "win32"],
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "curl",
              "kind": "brew",
              "formula": "curl",
              "label": "curl (HTTP client)"
            },
          ]
      },
      "version": "1.0.0"
  }
---

# Followin OpenAPI

Agent 调用 Followin 信息流接口时使用本 skill。

> **说明**：「频道」也称为「情报」或「情报中心」。

## Base URL

```
https://api.followin.io
```

## 鉴权

所有 OpenAPI 请求需携带 API Key，支持两种方式：

| 方式 | 示例 |
|------|------|
| Query 参数 | `?apikey=YOUR_API_KEY` |
| Header | `Authorization: YOUR_API_KEY` |

## 支持的语言

以下接口的 `lang` 参数支持以下语言代码：

| 代码 | 说明 |
|------|------|
| `zh-Hans` | 简体中文 |
| `zh-Hant` | 繁体中文 |
| `en` | 英语 |
| `vi` | 越南语 |
| `ko` | 韩语 |

## 接口列表

### 1. 热榜

获取今日热榜 feed 列表。

**请求**  
`GET /open/feed/list/trending`

| 参数 | 必填 | 说明 |
|------|------|------|
| type | 否 | 类型：`hot_news`（默认）、`pop_info` |
| count | 否 | 数量，默认 15 |
| need_bind_tag | 否 | 是否仅返回有标签的，默认 `false` |
| lang | 否 | 语言：`zh-Hans`、`zh-Hant`、`en`、`vi`、`ko` |

**响应**

```json
{
  "list": [ { "id", "title", "content", "publish_time", "page_url", "related_feeds", ... } ],
  "update_time": 1234567890
}
```

### 2. 分类推荐

按分类获取推荐 feed 列表。

**请求**  
`GET /open/feed/:category_name`

| 路径参数 | 说明 |
|----------|------|
| category_name | 分类名：`news`（快讯）、`articles`（文章） |

| Query 参数 | 必填 | 说明 |
|------------|------|------|
| count | 否 | 每页数量，默认 10，最大 30 |
| last_cursor | 否 | 分页游标（时间戳），默认 0 |
| only_important | 否 | 仅重要快讯（news 有效），默认 `false` |
| no_ad | 否 | 不展示广告，默认 `false` |
| lang | 否 | 语言：`zh-Hans`、`zh-Hant`、`en`、`vi`、`ko` |

**响应**

```json
{
  "list": [ { "id", "title", "content", "publish_time", "page_url", ... } ],
  "has_more": true,
  "last_cursor": "1234567890",
  "last_source": "biz",
  "rec_request_id": ""
}
```

### 3. 指定频道信息流

获取单个频道（情报/情报中心）的信息流。

**请求**  
`GET /open/channel/feeds`

| 参数 | 必填 | 说明 |
|------|------|------|
| code | 是 | 频道 code |
| count | 否 | 每页数量，默认 20，最大 30 |
| last_cursor | 否 | 分页游标，默认 0 |
| lang | 否 | 语言：`zh-Hans`、`zh-Hant`、`en`、`vi`、`ko` |

**支持的频道 code**

- `macro` - 宏观
- `listing_delisting` - 上币/下币
- `altcoin_update` - 山寨币更新
- `quant_signal` - 量化信号
- `live_trading_signal` - 实盘信号
- `token_unlock` - 代币解锁
- `fund_movement` - 资金异动
- `all_potential_airdrop` - 空投教程
- `airdrop_issue` - 领取通知
- `kol_post` - KOL 动态
- `trading_signal` - 点位喊单
- `trading_strategy` - 交易策略
- `meme_discover` - 发现 meme
- `meme_opportunity` - meme 交易机会
- `alpha_aggregator` - Alpha 聚合器
- `exchange_coin_update` - 交易所上币动态

**响应**

```json
{
  "list": [ { "id", "title", "content", "publish_time", "page_url", ... } ],
  "has_more": true,
  "last_cursor": "20"
}
```

### 4. 所有频道 feed_card 信息流

获取支持 feed_card 的频道（情报/情报中心）混合信息流（含卡片）。

**请求**  
`GET /open/channel/feeds/card`

| 参数 | 必填 | 说明 |
|------|------|------|
| count | 否 | 每页数量，默认 20，最大 30 |
| last_cursor | 否 | 分页游标，默认 0 |
| lang | 否 | 语言：`zh-Hans`、`zh-Hant`、`en`、`vi`、`ko` |

**响应**

```json
{
  "list": [
    {
      "id": 123,
      "title": "...",
      "content": "...",
      "publish_time": 1234567890,
      "page_url": "https://...",
      "feed_card": {
        "card_type": "f1_news",
        "fields": [ { "key", "value", "key_text", "value_text" } ],
        "show_feed": true
      }
    }
  ],
  "has_more": true,
  "last_cursor": "20"
}
```

## 分页

- 首次请求：`last_cursor=0` 或不传
- 后续请求：使用上一页返回的 `last_cursor`
- `has_more=false` 表示无更多数据

## curl 示例

```bash
# 1. 热榜
curl -X GET "https://api.followin.io/open/feed/list/trending?type=hot_news&count=15&lang=en&apikey=YOUR_API_KEY"

# 2. 分类推荐（快讯 / 文章）
curl -X GET "https://api.followin.io/open/feed/news?count=20&lang=en&apikey=YOUR_API_KEY"
curl -X GET "https://api.followin.io/open/feed/articles?count=20&last_cursor=0&lang=zh-Hans" \
  -H "Authorization: YOUR_API_KEY"

# 3. 指定频道（macro）
curl -X GET "https://api.followin.io/open/channel/feeds?code=macro&count=20&last_cursor=0&lang=en&apikey=YOUR_API_KEY"

# 4. 所有频道 feed_card
curl -X GET "https://api.followin.io/open/channel/feeds/card?count=20&last_cursor=0&lang=en&apikey=YOUR_API_KEY"

# 5. 分页（使用上一页返回的 last_cursor）
curl -X GET "https://api.followin.io/open/channel/feeds/card?count=20&last_cursor=20&lang=zh-Hans" \
  -H "Authorization: YOUR_API_KEY"
```