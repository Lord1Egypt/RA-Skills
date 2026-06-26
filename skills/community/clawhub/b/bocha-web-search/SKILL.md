---
name: bocha-web-search
description: 博查 Web 搜索工具，使用 Bocha Web Search API。适用于在线查询、事实核查、获取时效性信息以及提供带引用的回答。(Default web search tool using Bocha Web Search API. Use for online lookup, verification, time-sensitive information, and citation-based answers.)
license: MIT-0
homepage: https://open.bocha.cn
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      env:
        - BOCHA_API_KEY
    primaryEnv: BOCHA_API_KEY
---

# Bocha Web Search

本 Skill 使用 Bocha Web Search API 进行联网搜索。

This Skill performs web searches using the Bocha Web Search API.

它的主要设计目标是：

It is designed to:

- 检索最新、最及时的信息
  Retrieve up-to-date information
- 核实事实声明
  Verify factual claims
- 提供基于可靠来源的回答
  Provide source-backed answers
- 支持带有引用的回复
  Support citation-based responses

此版本避免了特定于 shell 的指令和系统级文件操作，以确保与 ClawHub 等安全环境的兼容性。

This version avoids shell-specific instructions and system-level file operations to ensure compatibility with secure environments such as ClawHub.

---

## 何时使用此 Skill (When to Use This Skill)

当用户的请求出现以下情况时，请使用此 Skill：

Use this skill whenever the user request:

- 需要对话历史中不存在的信息
  Requires information not present in the conversation
- 涉及具有时效性或不断变化的数据，如新闻、政策、财务数据、发布信息等
  Involves time-sensitive or changing data
- 需要进行事实核查或验证
  Requires fact-checking or verification
- 要求提供链接、信息来源或引用
  Requests links, sources, or citations
- 提及特定的组织、事件、人物或产品，并询问具体的事实细节
  Mentions a specific organization, event, person, or product and asks for factual details

如果不确定是否需要进行在线查询，请直接执行搜索。

If uncertain whether online lookup is required, perform a search.

---

## API 规范 (API Specification)

**请求端点 (Endpoint)**:

POST `https://api.bocha.cn/v1/web-search`

**请求头 (Headers)**:

```http
Authorization: Bearer <BOCHA_API_KEY>
Content-Type: application/json
```

**请求体参数 (Request Body)**:

| 参数名 | 类型 | 必填 | 说明 | Description |
|--------|------|------|------|-------------|
| query | string | 是 | 搜索关键词 | Search query string |
| freshness | string | 否 | 时间范围，可选值：`noLimit`(默认), `oneDay`, `oneWeek`, `oneMonth`, `oneYear` | Time filter |
| summary | boolean | 否 | 是否返回网页原文摘要，默认 `true` | Whether to include web original content |
| count | integer | 否 | 返回结果数量，默认 `10`，最大 `50` | Number of returned results |

### 工作流程 (Workflow)

#### 第一步：提取搜索参数 (Step 1: Extract Search Parameters)

从用户请求中提取搜索关键词和相关参数：

Extract search keywords and related parameters from the user's request:

1. `query`: 从用户问题中提取核心搜索词，需要保留“最近”、“今年”、“今年1月”等时间范围描述。
   Extract core search terms from the user's question, preserving time range descriptions like "recently", "this year", "January this year", etc.
2. `freshness`: 根据用户描述的时间范围确定，默认选择 `noLimit`，以便 web-search 结合 `query` 中的时间范围描述自动改写最合适的 freshness 值。
   Determine based on the user's described time range, defaulting to `noLimit` so web-search can automatically rewrite the most appropriate freshness value.
3. `summary`: 默认 `true`。
   Default is `true`.
4. `count`: 默认 `10`，如用户明确要求更多结果则进行调整。
   Default is `10`, adjust if the user explicitly requests more results.

#### 第二步：发起资源请求 (Step 2: Send API Request)

向博查 API 发起 POST 请求：

Send a POST request to the Bocha API:

```json
{
  "query": "<USER_QUERY>",
  "freshness": "noLimit",
  "summary": true,
  "count": 10
}
```

---

## 响应结构 (Response Structure)

搜索结果位于以下路径：

Search results are located at:

`data.webPages.value[]`

每个结果通常包含以下字段：

Each result typically contains:

- `name` (标题 / Title)
- `url` (链接 / URL)
- `snippet` (内容片段 / Snippet)
- `summary` (原始内容摘要 / Summary)
- `siteName` (站点名称 / Site Name)
- `datePublished` (发布日期 / Date Published)

---

## 引用规则 (Citation Rules - Mandatory)

在生成最终回答时，必须遵守以下规则：

When generating the final answer, you must adhere to the following rules:

1. 使用返回的来源来支撑你的事实性陈述。
   Support factual statements using returned sources.
2. 按出现顺序分配引用编号：[1], [2], [3]
   Assign citation numbers in order of appearance.
3. 在回答的末尾添加“参考资料”部分。
   End with a "References" section.
4. 每个参考文献必须包含标题、链接和站点名称（如果可用）。
   Each reference must include the title, URL, and site name (if available).

**输出格式示例 (Example output format)**:

回答 (Answer):

<你的回答，包含内联引用，如 [1], [2]。>
<Your answer with inline citations like [1], [2].>

参考资料 (References):

[1] `<title>`
`<url>`
来源 (Source): `<siteName>`

[2] `<title>`
`<url>`
来源 (Source): `<siteName>`

如果未找到可靠的来源，请回复：
If no reliable sources are found, reply with:
"未找到可靠的来源。(No reliable sources found.)"

---

## 错误处理 (Error Handling)

常见的 API 错误代码：

Common API error codes:

- 400: 请求错误 (Bad request)
- 401: API Key 无效 (Invalid API key)
- 403: 余额不足 (Insufficient balance)
- 429: 请求过于频繁 (Rate limit exceeded)
- 500: 服务器错误 (Server error)

如需调试，请使用 API 响应中的 `log_id`。

Use `log_id` from API responses for debugging if needed.
