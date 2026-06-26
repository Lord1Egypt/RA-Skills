# AI-CMO API Reference

Base URL: `https://www.aicmo.site/api/v1/open`

All endpoints require the `x-api-key` header.

## GET /quota

Check remaining credits.

```typescript
const data = await aicmoFetch("/quota").then(r => r.json());
// { credits_remaining: 15, username: "you", is_premium: false }
```

## POST /analyze

Analyze a product and return ranked promotion spots as JSON. Consumes 1 credit.

**Request body:**

```json
{
  "product": "https://yoursite.com",
  "language": "en",
  "max_results": 10
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| product | string | yes | Product URL or name (1–500 chars) |
| language | string | no | Response language: en, zh, ja, ko, es, fr, de, pt, ru, ar. Default: en |
| max_results | integer | no | Number of results (1–20). Default: 10 |

**Response:** See `AnalyzeResponse` in SKILL.md.

## POST /analyze/csv

Same as `/analyze` but returns CSV directly. Consumes 1 credit.

Same request body as `/analyze`. Response is a CSV file with BOM for Excel compatibility.

```typescript
const resp = await aicmoFetch("/analyze/csv", {
  method: "POST",
  body: JSON.stringify({ product: "mysite.com", language: "en", max_results: 8 }),
});
const csvText = await resp.text();
```

## GET /history

List recent analysis sessions.

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| limit | integer | 20 | Max results |

```typescript
const data = await aicmoFetch("/history?limit=5").then(r => r.json());
// { conversations: [{ id, title, status, created_at }, ...] }
```

## GET /history/{id}

Get full results from a past analysis.

```typescript
const data = await aicmoFetch(`/history/${conversationId}`).then(r => r.json());
// { input_value, recommendations: [...], strategy: {...} }
```

## GET /history/{id}/csv

Export a past analysis as CSV. Does **not** consume credits.

```typescript
const csv = await aicmoFetch(`/history/${conversationId}/csv`).then(r => r.text());
```

## Rate limits

* No explicit rate limit on reads (`/quota`, `/history`)
* Analysis endpoints (`/analyze`, `/analyze/csv`) are gated by credits — each call costs 1 credit
* If an analysis fails server-side, the credit is automatically refunded

## Promotion spot fields

Each item in the `promotions` array contains:

| Field | Type | Description |
|-------|------|-------------|
| rank | integer | Priority ranking |
| platform | string | Platform name (reddit, youtube, twitter, quora, producthunt, hackernews) |
| url | string | Direct URL to the post |
| title | string | Post title |
| suggested_comment | string | AI-crafted comment tailored to this post and platform |
| comment_strategy | string | How to frame the reply (helpful, comparative, etc.) |
| why_recommend | string | Why this post is a good opportunity |
| best_timing | string | When to engage for max visibility |
| risk_level | string | low / medium / high |
| risk_note | string | Explanation of the risk assessment |
| estimated_exposure | string | Expected reach (e.g. "~5K views") |
| composite_score | float | Quality score 0–100 |
| engagement_stats | object | Platform metrics: upvotes, comments, views |

---

# 中文版 / Chinese Translation

---

# AI-CMO API 参考

Base URL：`https://www.aicmo.site/api/v1/open`。所有接口需要 `x-api-key` 请求头。代码示例同上方英文部分。

## 接口一览

| 接口 | 说明 | 消耗积分 |
|------|------|---------|
| `GET /quota` | 查询剩余积分 | 否 |
| `POST /analyze` | 分析产品，返回 JSON 格式排名推广位 | 1 积分 |
| `POST /analyze/csv` | 分析产品，直接返回 CSV 文件（Excel 兼容） | 1 积分 |
| `GET /history` | 列出最近的分析记录 | 否 |
| `GET /history/{id}` | 获取某次分析的完整结果 | 否 |
| `GET /history/{id}/csv` | 将过往分析导出为 CSV | 否 |

## 请求参数（`/analyze` 和 `/analyze/csv`）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product | string | 是 | 产品 URL 或名称（1–500 字符） |
| language | string | 否 | 响应语言：en、zh、ja、ko、es、fr、de、pt、ru、ar。默认 en |
| max_results | integer | 否 | 返回结果数量（1–20）。默认 10 |

## 速率限制

* 读取接口（`/quota`、`/history`）无显式速率限制
* 分析接口通过积分控制——每次调用消耗 1 积分
* 如果分析在服务端失败，积分自动退回

## 推广位字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| rank | integer | 优先级排名 |
| platform | string | 平台名（reddit、youtube、twitter、quora、producthunt、hackernews） |
| url | string | 帖子直链 |
| title | string | 帖子标题 |
| suggested_comment | string | 为该帖和平台定制的 AI 评论文案 |
| comment_strategy | string | 回复切入方式（帮助型、对比型等） |
| why_recommend | string | 推荐理由 |
| best_timing | string | 最佳互动时间窗口 |
| risk_level | string | low / medium / high |
| risk_note | string | 风险评估说明 |
| estimated_exposure | string | 预估曝光量 |
| composite_score | float | 综合质量评分 0–100 |
| engagement_stats | object | 平台指标：点赞数、评论数、浏览量 |
