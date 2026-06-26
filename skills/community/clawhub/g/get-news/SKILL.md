---
name: crypto-news
description: 加密快讯抓取与筛选技能。使用当需要：(1) 从 BlockBeats 拉取快讯数据，(2) 按关键词筛选多条资讯，(3) 输出去 HTML 标签且时间已格式化的 JSON，用于后续自动化处理。
---

# Crypto News 快讯抓取技能

从 BlockBeats 官方开放接口并发抓取最新快讯，支持按关键词筛选、数量控制，输出结构化 JSON，方便在 openclaw 流程里复用。

## 能力概览

- 🔄 **并发抓取**：从 `https://api.theblockbeats.news/v1/open-api/open-flash` 分页抓取最新快讯
- 🔍 **关键词筛选**：对标题与内容做不区分大小写的关键词匹配（支持多个关键词）
- 🧹 **内容清洗**：自动移除 `content` 等字段中的 HTML 标签，只保留纯文本
- ⏱ **时间格式化**：将 `create_time` 等 Unix 秒时间戳转换为 `YYYY-MM-DD HH:mm:ss`，并保留原始值
- 📦 **JSON 输出**：只在 stdout 输出一个 JSON 数组，方便管道处理或被其他技能消费

## 快速开始

> 运行环境：Node.js 18+（内置 `fetch`），在 workspace 根目录下执行。

### 1. 直接获取最新 N 条快讯（不按关键词过滤）

```bash
node workspace/erbai/crypto-news/new.js "" 10 1000
```

- 第 1 个参数 `""`：关键字为空，表示不过滤，直接返回最新快讯
- 第 2 个参数 `10`：`limit`，最多返回 10 条
- 第 3 个参数 `1000`：`maxLimit`，最多从接口抓取 1000 条后再截断

返回结果为 JSON 数组，每一项是清洗和格式化后的快讯对象。

### 2. 按关键词筛选（单个或多个）

```bash
# 单个关键词
node workspace/erbai/crypto-news/new.js "btc" 20 1000

# 多个关键词（逗号分隔）
node workspace/erbai/crypto-news/new.js "btc,okx,eth" 50 2000
```

- 关键词不区分大小写，会在标题、内容等文本字段里做包含匹配
- 只返回最多 `limit` 条匹配结果

## 参数说明

脚本签名：

```bash
node workspace/erbai/crypto-news/new.js {keyword} {limit} {maxLimit}
```

- **`keyword`**（字符串，可选）  
  - 说明：关键字字符串，多个用英文逗号分隔，如 `"btc,okx,eth"`  
  - 行为：为空或省略时，不做关键词过滤，直接返回最新快讯  

- **`limit`**（整数，可选，默认 `10`）  
  - 说明：最终返回的最大条数  
  - 示例：`10` 表示最多返回 10 条快讯  

- **`maxLimit`**（整数，可选，默认 `1000`）  
  - 说明：从接口抓取的最大原始条数，上限控制抓取 & 计算量  
  - 示例：`2000` 表示最多抓 2000 条，再在其中进行筛选和截断  

## 输出数据结构（示例）

```jsonc
[
  {
    "id": 335678,
    "title": "OKX Star：有些公司打造产品，有些公司组织诉讼",
    "content": "BlockBeats 消息，3 月 11 日，OKX 创始人兼 CEO Star ...",  // 已去 HTML 标签
    "link": "https://m.theblockbeats.info/flash/335678",
    "create_time": "2026-03-13 16:28:32",      // 已格式化
    "create_time_raw": "1773376185"           // 原始 Unix 秒时间戳
  }
]
```

> 注意：字段名会随官方 API 变动而略有不同，技能保证：  
> - 文本字段中的 HTML 标签会被移除  
> - `create_time` / `time` / `timestamp` 等时间戳字段会尝试格式化并保留 `_raw` 原值  

## 在 openclaw 中的典型用法

- **作为数据源技能**：在自动化流程里先调用本技能获取结构化快讯列表，再交给其他技能（例如摘要、翻译、推送等）继续处理。
- **与通知/推送技能组合**：  
  1. 使用 `crypto-news` 获取匹配某些币种的最新快讯  
  2. 将结果过滤重组后，推送到钉钉/飞书/Telegram 等渠道  

调用本技能时，只需要让代理执行对应的 `node ...` 命令，并把 stdout 解析为 JSON 即可。 