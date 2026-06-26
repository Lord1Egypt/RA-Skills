# Bocha API 详细规范（浩鲸科技大模型网关代理版）

## 基础信息

- 代理基址：`https://lab.iwhalecloud.com/gpt-proxy/bocha/v1/`
- 认证方式：`Authorization: Bearer <浩鲸大模型网关APIKEY>`
- Content-Type：`application/json`

## 网页搜索 API

### 端点

```
POST https://lab.iwhalecloud.com/gpt-proxy/bocha/v1/web-search
```

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | ✅ | - | 搜索关键词 |
| freshness | string | ❌ | noLimit | noLimit / oneDay / oneWeek / oneMonth / oneYear |
| count | integer | ❌ | 10 | 返回结果数，1-50 |
| summary | boolean | ❌ | false | 是否返回网页摘要 |
| include | string | ❌ | - | 仅搜索指定域名，\| 分隔，最多100个 |
| exclude | string | ❌ | - | 排除指定域名，\| 分隔，最多100个 |

### 请求示例

```json
{
  "query": "阿里巴巴2024年的esg报告",
  "freshness": "noLimit",
  "summary": true,
  "count": 50
}
```

### 响应结构

```json
{
  "code": 200,
  "log_id": "e02ce8d18c71d14f",
  "msg": null,
  "data": {
    "_type": "SearchResponse",
    "queryContext": {
      "originalQuery": "阿里巴巴2024年的esg报告"
    },
    "webPages": {
      "webSearchUrl": "https://bochaai.com/search?q=...",
      "totalEstimatedMatches": 10000000,
      "value": [
        {
          "id": "https://api.bochaai.com/v1/#WebPages.0",
          "name": "网页标题",
          "url": "https://example.com/article",
          "displayUrl": "https://example.com/article",
          "snippet": "简短描述...",
          "summary": "详细摘要内容...",
          "siteName": "来源网站",
          "siteIcon": "https://th.bochaai.com/favicon?domain_url=...",
          "datePublished": "2024-07-22T11:58:00+08:00",
          "dateLastCrawled": "2024-07-22T11:58:00Z",
          "cachedPageUrl": null,
          "language": null
        }
      ],
      "someResultsRemoved": true
    },
    "images": {
      "value": [
        {
          "name": null,
          "thumbnailUrl": "https://example.com/thumb.jpg",
          "contentUrl": "https://example.com/image.jpg",
          "hostPageUrl": "https://example.com/article",
          "width": 0,
          "height": 0
        }
      ]
    },
    "videos": null
  }
}
```

## AI 搜索 API

### 端点

```
POST https://lab.iwhalecloud.com/gpt-proxy/bocha/v1/ai-search
```

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | ✅ | - | 搜索关键词 |
| freshness | string | ❌ | noLimit | noLimit / oneDay / oneWeek / oneMonth / oneYear |
| count | integer | ❌ | 10 | 返回结果数，1-50 |
| answer | boolean | ❌ | true | 是否用大模型生成答案 |
| include | string | ❌ | - | 仅搜索指定域名，\| 分隔 |
| stream | boolean | ❌ | false | 是否启用流式返回 |

### 请求示例

```json
{
  "query": "西瓜的功效与作用",
  "freshness": "noLimit",
  "count": 10,
  "answer": true
}
```

### 响应结构

与 web-search 类似，额外包含：
- `data.answer`：大模型自动生成的总结答案
- `data.followUpQuestions`：推荐的追问问题
- 模态卡数据：天气、百科、医疗、万年历、火车、星座属相、贵金属、汇率、油价、手机、股票、汽车等

## 域名过滤用法

```json
{
  "query": "AI最新进展",
  "include": "zhihu.com|36kr.com|weixin.qq.com",
  "exclude": "baidu.com"
}
```

## 错误响应

```json
{
  "code": 401,
  "message": "Invalid API KEY",
  "log_id": "request_trace_id"
}
```

使用 log_id 联系运维排查问题。
