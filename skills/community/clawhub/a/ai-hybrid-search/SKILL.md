---
name: ai-hybrid-search
description: 梓享AI双擎搜索平台官方付费技能，通过POST请求调用搜索接口，支持中国区/全球双引擎，返回结构化JSON搜索结果，按调用次数计费。
homepage: https://open.zixiangai.com/
repository: https://open.zixiangai.com/api/web-search/
metadata:
  clawd bot:
    emoji: "🔍💰"
    requires:
      env:
        - name: "ZIXIANGAI_API_KEY"
          description:
            "梓享AI开放平台 API
            Key，用于鉴权与扣费。在控制台获取：https://open.zixiangai.com/dashboard/index.html"
      files:
        - "scripts/search.sh"
---

# 梓享 AI 双擎搜索（付费版）

## 🔌 平台与接口信息

| 项目              | 地址 / 说明                                     |
| ----------------- | ----------------------------------------------- |
| 平台官网 / 控制台 | https://open.zixiangai.com/                     |
| API Key 获取      | https://open.zixiangai.com/dashboard/index.html |
| 搜索接口地址      | https://search.aiserver.cloud/v1/api            |
| 请求方式          | POST (JSON)                                     |
| 鉴权方式          | `Authorization: Bearer <API_KEY>`               |
| 计费模式          | 按调用次数扣费，中国区 / 全球引擎额度独立统计   |

## ⚙️ 配置说明

1. 在 OpenClaw 后台设置环境变量 `ZIXIANGAI_API_KEY`，值为梓享 AI 控制台获取的官
   方 API Key；
2. 每次调用自动携带鉴权信息，扣费逻辑由梓享 AI 官方服务统一处理；
3. 可通过接口返回的 `balance` 字段实时查看剩余调用次数与账户余额。

## 📌 使用示例

### 基础用法（仅传搜索词，使用默认参数）

```
使用梓享AI双擎搜索，查询：2026年AI行业动态
```

> 默认参数：engine=china、max_results=10、无时间过滤、无域名限制

### 高级用法（自定义全量参数）

```
使用梓享AI双擎搜索，查询：2026年AI行业动态，引擎：global，返回条数：20，时间过滤：month，指定域名：baidu.com、zhihu.com，排除域名：xxx.com
```

## 📋 完整参数说明

| 参数              | 类型   | 必填 | 默认值  | 说明                                          |
| ----------------- | ------ | :--: | ------- | --------------------------------------------- |
| `query`           | string |  ✅  | —       | 搜索词，支持自然语言，建议 ≤500 字符          |
| `engine`          | string |  ❌  | `china` | 引擎类型：`china`（中国区）/ `global`（全球） |
| `max_results`     | number |  ❌  | `10`    | 返回结果条数，范围 1–20                       |
| `time_filter`     | string |  ❌  | 空      | 时间过滤：`day` / `week` / `month` / `year`   |
| `include_domains` | array  |  ❌  | `[]`    | 指定搜索的域名范围，最多 20 个，JSON 数组格式 |
| `exclude_domains` | array  |  ❌  | `[]`    | 排除搜索的域名范围，最多 20 个，JSON 数组格式 |

## 📊 响应示例

```json
{
  "code": 0,
  "msg": "",
  "engine": "china",
  "balance": {
    "times": { "china": 990, "global": 1000 },
    "amount": 100.0
  },
  "log_id": "LOG202412271234abcdef",
  "searchParams": {
    "engine": "china",
    "query": "2026年AI行业动态",
    "max_results": 10,
    "time_filter": "",
    "include_domains": [],
    "exclude_domains": []
  },
  "data": {
    "images": [{ "url": "https://example.com/image.jpg" }],
    "results": [
      {
        "title": "页面标题",
        "url": "https://example.com/page",
        "content": "页面摘要内容..."
      }
    ]
  }
}
```

**返回字段说明：**

| 字段           | 说明                                      |
| -------------- | ----------------------------------------- |
| `code`         | `0` 表示成功，非 `0` 表示错误             |
| `msg`          | 错误描述（成功时为空字符串）              |
| `engine`       | 实际使用的引擎类型                        |
| `balance`      | 账户剩余调用次数（按引擎分类）及余额      |
| `log_id`       | 唯一请求 ID，便于问题排查                 |
| `searchParams` | 本次搜索实际使用的参数                    |
| `data.results` | 搜索文本结果列表（title / url / content） |
| `data.images`  | 搜索图片结果列表                          |

## ⚠️ 注意事项

- `include_domains` / `exclude_domains` 须为合法 JSON 数组，如 `[]` 或
  `["baidu.com"]`；
- 中国区（`china`）与全球（`global`）引擎的调用额度**独立计费**，请按需选择；
- API Key 请勿泄露，可在控制台随时重新生成。
