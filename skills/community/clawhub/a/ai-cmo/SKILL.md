---
name: AI-CMO Social Media Promoter
description: Find the best social media promotion spots for any product and generate platform-tailored engagement copy
requires:
  env:
    - AICMO_API_KEY
---

# AI-CMO: Social Media Promotion Intelligence

AI-CMO analyzes any product URL or name and finds the best promotion opportunities across Reddit, YouTube, Twitter/X, Quora, Product Hunt, and Hacker News. It returns ranked posts with AI-generated engagement copy tailored to each platform's tone.

> This skill calls the AI-CMO REST API to retrieve promotion data. It does **not** require a local browser — all analysis happens server-side. The agent uses the returned data to help you engage on social media.

**Homepage:** <https://www.aicmo.site>
**API Docs:** <https://www.aicmo.site/api-docs>

## Runtime requirements

* **OS:** macOS · Linux · Windows
* **Env:** `AICMO_API_KEY` — your AI-CMO API key (get one at <https://www.aicmo.site> → Settings → API Keys)

## When to use

* You want to find high-value posts/threads to engage with for a product
* You need AI-generated comments customized per platform
* You want a CSV of promotion targets for batch processing

## When not to use

* You only need a simple Google search (use a search engine instead)
* The product has no web presence yet (AI-CMO needs existing content to find)

## Prerequisites

* An AI-CMO account — register at <https://www.aicmo.site>
* Environment variable: `AICMO_API_KEY`

### Get an API key

1. Log in to <https://aicmo.site>
2. Go to **Settings → API Keys**
3. Click **Create Key** and save the key securely

```bash
export AICMO_API_KEY="sk-cmo-your-key-here"
```

## Quick start: analyze a product

Analyze a product and get ranked promotion spots. Consumes **1 credit** per call.

> Note: Analysis takes 2–4 minutes (scraping 6 platforms + AI scoring). Set your HTTP client timeout to at least 300 seconds.

```typescript
const resp = await fetch("https://www.aicmo.site/api/v1/open/analyze", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": process.env.AICMO_API_KEY!,
  },
  body: JSON.stringify({
    product: "https://your-product.com",
    language: "en",
    max_results: 10,
  }),
});

const result = await resp.json();

for (const spot of result.promotions) {
  console.log(`#${spot.rank} [${spot.platform}] ${spot.title}`);
  console.log(`  URL: ${spot.url}`);
  console.log(`  Comment: ${spot.suggested_comment}`);
  console.log(`  Score: ${spot.composite_score} | Risk: ${spot.risk_level}`);
}
```

The response contains `promotions[]` (ranked posts with `url`, `suggested_comment`, `platform`, `composite_score`, `risk_level`, etc.) and `strategy` (action plan). For CSV output, use `/analyze/csv` instead — same request, returns a downloadable CSV file.

Base URL: `https://www.aicmo.site/api/v1/open` (always use `www.aicmo.site`).

### CSV columns

| Column | Description |
|--------|-------------|
| Rank | Priority ranking (1 = best) |
| Platform | reddit, youtube, twitter, quora, producthunt, hackernews |
| URL | Direct link to the post/thread |
| Title | Post title |
| Suggested Comment | AI-generated engagement copy for this specific post |
| Comment Strategy | Context on how to approach the conversation |
| Why Recommend | Why this post is a good promotion opportunity |
| Best Timing | Recommended engagement window |
| Risk Level | low, medium, or high |
| Estimated Exposure | Approximate reach |
| Score | Composite quality score (0–100) |

## Engaging with results

After receiving promotion spots, the agent can help you engage by:

1. **Browsing** to the post URL
2. **Reading** the existing discussion for context
3. **Composing** a reply using the `suggested_comment` as a starting point
4. **Adapting** the tone to match the thread's conversation style

> Important: Always review the suggested comment before posting. The AI provides a strong starting point, but human judgment ensures the reply feels authentic and adds genuine value to the conversation.

## References (deep dive)

* API reference: [references/api-reference.md](references/api-reference.md)
* Platform-specific engagement tips: [references/platform-tips.md](references/platform-tips.md)
* Scheduling and frequency recommendations: [references/scheduling.md](references/scheduling.md)

---

# 中文版 / Chinese Translation

---

# AI-CMO：社媒推广智能分析

AI-CMO 可分析任意产品 URL 或名称，在 Reddit、YouTube、Twitter/X、Quora、Product Hunt 和 Hacker News 上找到最佳推广机会。返回排名后的帖子列表，并为每个帖子生成匹配该平台风格的 AI 互动文案。

> 本 Skill 调用 AI-CMO REST API 获取推广数据，**不需要**本地浏览器——所有分析在服务端完成。

## 何时使用

* 为产品找到高价值的帖子/讨论串进行互动
* 获取为每个平台定制的 AI 评论文案
* 获取 CSV 格式的推广目标清单用于批量处理

## 何时不使用

* 只需要简单搜索（请直接用搜索引擎）
* 产品还没有任何网络信息（AI-CMO 需要已有内容才能分析）

## 前置条件

* AI-CMO 账号——在 <https://www.aicmo.site> 注册
* 环境变量：`AICMO_API_KEY`（在 **设置 → API 密钥** 中创建）

> 代码示例与上方英文部分一致，此处不再重复。

## 核心接口

| 接口 | 说明 | 消耗积分 |
|------|------|---------|
| `GET /quota` | 查询剩余积分 | 否 |
| `POST /analyze` | 分析产品，返回 JSON 推广位 | 1 积分 |
| `POST /analyze/csv` | 分析产品，返回 CSV 文件 | 1 积分 |
| `GET /history` | 分析历史列表 | 否 |
| `GET /history/{id}/csv` | 导出过往分析为 CSV | 否 |

## 使用结果进行互动

Agent 可以帮你：浏览帖子 URL → 阅读上下文 → 以 `suggested_comment` 为起点撰写回复 → 调整语气匹配对话风格。

> 发帖前务必审阅。AI 提供的是起点，人工判断确保回复真实自然。

## 参考文档

* API 参考：[references/api-reference.md](references/api-reference.md)
* 各平台互动技巧：[references/platform-tips.md](references/platform-tips.md)
* 频率和节奏建议：[references/scheduling.md](references/scheduling.md)
