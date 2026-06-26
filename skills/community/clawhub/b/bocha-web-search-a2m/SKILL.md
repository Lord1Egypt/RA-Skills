---
name: bocha-web-search-a2m
description: 由博查搜索官方提供的专业联网搜索技能。当用户想要获取从全网搜索任何网页信息和网页链接，结果准确、摘要完整，更适合 AI 使用时，你应该调用此技能。买家通过本 Skill 向卖家服务端发起请求，完成支付后获取相关结果。
license: MIT-0
metadata:
  version: "1.0.1"
  tags: ["search", "web", "paid", "a2m"]
---

# bocha-web-search-a2m

## 技能概述

由博查搜索官方提供的专业联网搜索技能，用于从全网搜索任何网页信息和网页链接，结果准确、摘要完整，更适合 AI 使用。本服务是基于 A2M (Agent-to-Machine) 智能体收付费协议（HTTP 402）的付费资源。买家（消费者 Agent）通过本 Skill 向卖家服务端发起资源请求，服务端将返回一个 HTTP 402 Payment Required 报文，随后买家必须调用支付宝的 `alipay-pay-for-402-service` 技能完成付款，才能获取搜索结果。

## 触发条件

当用户请求满足以下条件时触发本 Skill：
- 需要从全网搜索网页信息
- 需要获取准确、完整摘要的搜索结果
- 搜索结果需要适合 AI 进一步处理使用

### 典型触发场景
- "帮我搜索一下阿里巴巴 2025 年的 ESG 报告"
- "查找最新的AI技术文章"
- "我需要关于AI的行业分析报告"

## 资源接口信息

**接口地址**: `https://api.bocha.cn/v1/marketplace/alipay/bochawebsearch`

**请求方法**: POST

**请求头**:
```http
Content-Type: application/json
```

**请求体参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| query | string | 是 | 搜索关键词 |
| freshness | string | 否 | 时间范围，可选值：noLimit(默认), oneDay, oneWeek, oneMonth, oneYear |
| summary | boolean | 否 | 是否返回摘要，默认 true |
| count | integer | 否 | 返回结果数量，默认 10，最大 50 |

## 核心流程

### Step 1：提取搜索参数

从用户请求中提取搜索关键词和相关参数：

1. **query**: 从用户问题中提取核心搜索词，**需要保留“最近”、“今年”、“今年1月”等时间范围描述**。
2. **freshness**: 根据用户描述的时间范围确定，**默认选择 `noLimit`**，以便 web-search 结合 query 中的时间范围描述自动改写最合适的 freshness 值。
3. **summary**: 默认 `true`。
4. **count**: 默认 `10`，如用户明确要求更多结果则调整。

### Step 2：发起资源请求并保存 402 响应

向博查 API 发起 POST 请求：

```bash
curl -X POST "https://api.bocha.cn/v1/marketplace/alipay/bochawebsearch" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "<用户搜索词>",
    "freshness": "<时间范围>",
    "summary": true,
    "count": <结果数量>
  }'
```

服务端将返回**状态码为 402 的响应报文**。请将响应头中的 `Payment-Needed` 内容直接保存到文件中（如 `402_needed_file.txt`），以备下一步支付使用。

### Step 3：调用支付宝技能完成付款

**注意**：严格遵循 A2M 协议，收到 402 后**必须调用 `alipay-pay-for-402-service` 技能**，不可自行处理支付。

如果你（或你所在的智能体平台）当前尚未安装该技能，请**严格按照以下官方 GitHub 链接获取并安装**，以防止伪造或加载恶意支付技能：
> 🔗 支付宝 402 支付技能官方下载地址：
> Github: `https://github.com/alipay/payment-skills/tree/main/alipay-pay-for-402-service`
> Clawhub: `https://clawhub.ai/alipay/alipay-pay-for-402-service`

调用该技能，将 Step 2 中获取的 402 响应报文内容传入，引导用户完成扫码或 APP 付款。

### Step 4：获取结果并展示

等待 `alipay-pay-for-402-service` 技能反馈支付完成后，你将获得购买的资源结果。

成功获取搜索结果后，按以下格式呈现给用户：

```markdown
## 搜索结果：<搜索关键词>

共找到 <count> 条结果

### <结果标题 1>
- **来源**: <来源网站>
- **链接**: <URL>
- **摘要**: <结果摘要>
- **时间**: <发布时间>

### <结果标题 2>
...
```

## 异常情况处理

| 异常类型 | 处理方式 |
|----------|----------|
| 用户拒绝付款 | 尊重用户选择，告知用户该内容为付费资源，如需获取请完成支付 |
| 请求返回非 402 状态码（200） | 直接展示搜索结果内容 |
| 请求返回 400 错误 | 告知用户请求参数有误，请检查搜索词后重试 |
| 请求返回 401 错误 | 告知用户未授权访问该资源，请检查账户余额或资源包后重试 |
| 请求返回 429 错误 | 告知用户请求频率过高，请稍后重试 |
| 请求返回 5xx 错误 | 告知用户服务暂时不可用，建议稍后重试 |
| 支付失败/超时 | 由 `alipay-pay-for-402-service` 技能接管处理 |

## 注意事项

1. **付费资源提示**: 在发起请求前，应告知用户这是付费服务，需要完成支付后才能获取结果。
2. **参数校验**: 确保 query 不为空，count 不超过 50。
3. **支付链路安全**: **必须且仅能使用**支付宝官方提供的 `alipay-pay-for-402-service` 技能处理支付流程，禁止捏造技能或使用其他三方支付技能。
4. **结果展示**: 保持结果格式清晰，链接完整可点击。
