# 2Ryun REST API 技术说明书 v1.0

> 版本：1.1 | 最后更新：2026-08-11 | 包含 5 大类 50 端点（文档/Wiki/建站/用户/笔记）

## 概述

| 项目 | 值 |
|------|-----|
| Base URL | `https://www.2ryun.wiki/restapi` |
| 鉴权方式 | HTTP Header `Authorization: Bearer sk-xxxxxxxx-xxxxxxxx-...` |
| 请求格式 | `application/json`（文件导入为 `multipart/form-data`） |
| 响应格式 | `application/json` |
| 成功响应 | HTTP 200（查询/更新）、HTTP 201（创建） |
| 错误响应 | `{ "error": "错误描述字符串" }` |
| 超时建议 | extract: 180s, organize: 300s, generate: 120s, 其他: 30s |

### 获取 API Key

登录 2Ryun → 设置 → API Keys → 创建新 Key。Key 格式为 `sk-` 前缀 + 多段随机字符串。使用时放在 `Authorization: Bearer <key>` Header 中。

### API Key 权限（模块级）

每个 API Key 有一组模块权限，格式 `{module}:read` / `{module}:write`（模块内 write 包含 read）。模块：`documents`、`wiki`、`gen-html`、`note`、`attachments`、`users`（仅 read）。新 Key 默认全部模块读写；可在设置页收窄。

权限不足时返回：
```json
{ "error": "API Key 权限不足", "code": "INSUFFICIENT_SCOPE", "required": "documents:write" }
```
状态码 **407**。

### 内容访问 URL 规则

以下 URL 用于向用户展示已发布的内容，**无需 API Key**，可直接在浏览器打开。

| 内容类型 | URL 模式 | 说明 |
|---------|---------|------|
| 已发布网页 | `https://www.2ryun.wiki/restapi/gen-html/public/:generation_id` | 单页生成结果 |
| 文档页面 | `https://www.2ryun.wiki/app/:doc_id` | 2Ryun 内部文档页（需登录） |
| 封面图 | `https://www.2ryun.wiki/restapi/gen-html/generations/:id/cover` | JPEG，可嵌入 `<img>` |
| 模板预览 | `https://www.2ryun.wiki/restapi/gen-html/templates/:name/example` | 模板示例 HTML |
| 上传的文件 | `https://www.2ryun.wiki/:path` | 图片/视频等素材，`path` 为上传接口返回的 `path` 字段 |

**API → URL 映射**：

- `POST /generate` → `generation_id` → 发布后: `restapi/genhtml/public/GEN_ID`
- `POST /documents/create` → `document`（即 `_id`） → 文档页: `/app/DOC_ID`

**预览（未发布）**：`GET /restapi/gen-html/generations/:id/html` 返回 JSON `{ "html": "..." }`，可自行渲染。

---

## 1. 文档管理 (Documents)

### 1.1 文档列表

```
GET /restapi/documents
```

列出当前用户的所有文档，支持分页和筛选。

**查询参数**

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| page | number | 否 | 1 | 页码 |
| pageSize | number | 否 | 50 | 每页数量 |
| tag | string | 否 | — | 按标签筛选 |
| since | string | 否 | — | 筛选该时间之后更新的文档 (ISO 8601) |
| root | string | 否 | — | `true` 只返回根文档 |
| root_id | string | 否 | — | 按根文档 ID 筛选子树 |
| fields | string | 否 | — | 逗号分隔的返回字段（如 `title,tags`），不传返回全部 |

**返回**

```json
{
  "documents": [
    {
      "_id": "6a69810fef276a17f2fb089f",
      "title": "产品白皮书",
      "content": "# 产品概述\n\n这是产品白皮书的正文内容...",
      "summary": "产品概述简介",
      "tags": ["产品", "技术"],
      "board": "",
      "parentId": "6a69810fef276a17f2fb089e",
      "rootId": "6a69810fef276a17f2fb089e",
      "createdBy": "6a66b4a939b7b51cc8dc3b16",
      "createdAt": "2026-07-29T03:00:00.000Z",
      "updatedAt": "2026-07-29T03:00:00.000Z"
    }
  ],
  "total": 42
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| documents | array | 文档对象数组 |
| documents[]._id | string | 文档唯一 ID |
| documents[].title | string | 文档标题 |
| documents[].content | string | Markdown 格式正文（可能为空） |
| documents[].summary | string | 文档摘要 |
| documents[].tags | string[] | 标签数组 |
| documents[].board | string | 所属画板 |
| documents[].parentId | string\|null | 父文档 ID |
| documents[].rootId | string | 根文档 ID |
| documents[].createdBy | string | 创建者用户 ID |
| documents[].createdAt | string | 创建时间 ISO 8601 |
| documents[].updatedAt | string | 更新时间 ISO 8601 |
| total | number | 符合条件的文档总数 |

---

### 1.2 获取单个文档

```
GET /restapi/documents/:id
```

**路径参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | string | 文档 ID |

**返回**：单个文档完整对象（字段同 1.1 documents 数组元素），包含 `content` 正文。

---

### 1.3 搜索文档

```
GET /restapi/documents/search
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |

**返回**：格式同 1.1，返回匹配的文档列表。

---

### 1.4 创建文档

```
POST /restapi/documents/create
```

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 文档标题 |
| content | string | 否 | Markdown 格式正文，默认空字符串 |
| parentId | string | 否 | 父文档 ID，不传则为根文档 |
| rootId | string | 否 | 根文档 ID，不传自动设为自身 |
| tags | string[] | 否 | 标签数组 |
| board | string | 否 | 所属画板名称 |
| setting | object | 否 | 文档设置，如 `{"autoExtractWiki": false}` |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/documents/create \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "新文档",
    "content": "# 第一章\n\n正文内容...",
    "tags": ["技术", "AI"],
    "parentId": "6a69810fef276a17f2fb089e",
    "rootId": "6a69810fef276a17f2fb089e",
    "setting": {"autoExtractWiki": true}
  }'
```

**返回**

```json
{
  "message": "Document created successfully",
  "document": "6a69810fef276a17f2fb089f"
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| message | string | 操作结果描述 |
| document | string | 新创建的文档 ID |

---

### 1.5 导入文件

```
POST /restapi/documents/import
```

上传文件并自动转换为 Markdown。支持 pdf、docx、xlsx、pptx、md、markdown、txt、html、htm、csv。

**请求格式**：`multipart/form-data`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 要上传的文件 |
| title | string | 否 | 文档标题，默认使用文件名（不含扩展名） |
| parentId | string | 否 | 父文档 ID |
| rootId | string | 否 | 根文档 ID |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/documents/import \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@report.pdf" \
  -F "title=季度报告" \
  -F "parentId=6a69810fef276a17f2fb089e"
```

**返回**：同 1.4 创建文档的返回格式。文档已自动创建，content 为转换后的 Markdown。

---

### 1.6 更新文档

```
PUT /restapi/documents/update/:id
```

**路径参数**：`id` — 文档 ID

**请求体 (JSON)**：所有字段均为可选，只传需要更新的字段。

| 参数 | 类型 | 说明 |
|------|------|------|
| title | string | 新标题 |
| content | string | 新正文 |
| tags | string[] | 新标签 |
| board | string | 所属画板 |
| parentId | string | 父文档 ID |
| rootId | string | 根文档 ID |
| sortId | number | 排序位置 |
| icon | string | 图标 |
| cover | string | 封面图 |
| sharing | string | 分享设置 |
| setting | object | 文档设置 |

**请求示例**

```bash
curl -X PUT https://www.2ryun.wiki/restapi/documents/update/6a69810fef276a17f2fb089f \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "更新后的标题", "content": "更新后的内容", "tags": ["新标签"]}'
```

**返回**：更新后的完整文档对象（格式同 1.1 返回的 documents 数组元素）。

---

### 1.7 删除文档

```
DELETE /restapi/documents/delete/:id
```

**返回**

```json
{ "message": "Document deleted successfully" }
```

---

### 1.8 批量获取文档

```
POST /restapi/documents/batch
```

一次请求获取多篇文档的完整内容。适合批量操作场景。

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ids | string[] | 是 | 文档 ID 数组 |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/documents/batch \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["6a69810fef276a17f2fb089f", "6a69810fef276a17f2fb08a0"]}'
```

**返回**

```json
[
  {
    "_id": "6a69810fef276a17f2fb089f",
    "title": "文档一",
    "content": "# 文档一\n\n正文...",
    "tags": ["tag1"],
    "createdAt": "2026-07-29T03:00:00.000Z"
  },
  {
    "_id": "6a69810fef276a17f2fb08a0",
    "title": "文档二",
    "content": "# 文档二\n\n正文...",
    "tags": ["tag2"],
    "createdAt": "2026-07-29T04:00:00.000Z"
  }
]
```

返回文档数组，每个元素格式同 1.1。

---

### 1.9 复制文档

```
POST /restapi/documents/duplicate/:id
```

复制指定文档及其内容。新文档标题为原标题 + " (Copy)"。

---

### 1.10 获取文档树

```
GET /restapi/documents/fulltree/:rootId
```

获取以 `:rootId` 为根的完整文档树结构，返回嵌套的子文档数组。

**返回**

```json
{
  "_id": "rootId",
  "title": "根文档",
  "children": [
    {
      "_id": "child1",
      "title": "子文档1",
      "children": []
    }
  ]
}
```

---

### 1.11 公开文档

```
GET /restapi/documents/public/:id
```

访问设置为公开的文档。**无需 API Key**。

### 1.12 文档概要

```
GET /restapi/documents/simple/:id
```

获取文档基本信息（不含完整 content）。无需文档所有权检查。

### 1.13 获取文档（别名）

```
GET /restapi/documents/get/:id
```

同 1.2，获取完整文档内容。使用 `checkDocumentAccess` 中间件（不强制 API Key 认证，但检查访问权限）。

### 1.14 分享文档

```
POST /restapi/documents/share/:id
```

将文档分享给指定用户。

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | string | 是 | 目标用户 ID |
| permission | string | 否 | 权限：read\|write，默认 read |

### 1.15 更新分享权限

```
PUT /restapi/documents/sharing/:id
```

更新已分享文档的访问权限设置。

### 1.16 获取分享记录

```
GET /restapi/documents/shares/:id
```

返回该文档的所有分享记录列表。

### 1.17 取消分享

```
DELETE /restapi/documents/share/:id/:userId
```

取消对特定用户的文档分享。

### 1.18 分享文档树

```
POST /restapi/documents/tree/sharing/:id
```

将整个文档树分享出去。

### 1.19 更新文档树

```
POST /restapi/documents/tree/:id
```

**请求体 (JSON)**：`{ "tree": [...] }` — 新的树结构数据。

---

## 2. 知识库 (Wiki)

### 2.1 知识提取

```
POST /restapi/wiki/extract
```

调用 AI 从文档正文中提取结构化知识条目。**同步操作，耗时 1-3 分钟。**

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 文档的 Markdown 正文，最少 20 字符 |
| title | string | 否 | 文档标题（提高提取质量） |
| content_id | string | 否 | 关联的 2Ryun 文档 ID（用于跟踪、去重） |
| tags | string[] | 否 | 文档标签（辅助知识分类） |
| board | string | 否 | 所属画板名称 |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/wiki/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 人工智能概述\n\n人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个重要分支...",
    "title": "AI Overview",
    "content_id": "6a69810fef276a17f2fb089f",
    "tags": ["AI", "技术"]
  }'
```

**成功返回 (200)**

```json
{
  "entries_created": 3,
  "entries": [
    {
      "id": "6a69810fef276a17f2fb0900",
      "title": "人工智能",
      "content": "人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个重要分支，旨在创建能够执行通常需要人类智能的任务的系统。",
      "summary": "人工智能是计算机科学中研究智能系统的分支",
      "category": "concept",
      "confidence_score": 0.95,
      "confidence_tier": "extracted",
      "tags": ["AI", "技术", "计算机科学"],
      "relations": [
        {
          "related_entry": "6a69810fef276a17f2fb0901",
          "label": "核心技术"
        }
      ],
      "enrichments": [
        {
          "type": "background_context",
          "content": "AI 的概念最早由 John McCarthy 在 1956 年提出",
          "target_text": "人工智能",
          "confidence": 0.9
        }
      ],
      "sources": [
        {
          "type": "document",
          "name": "AI Overview",
          "content_id": "6a69810fef276a17f2fb089f"
        }
      ]
    },
    {
      "id": "6a69810fef276a17f2fb0901",
      "title": "机器学习",
      "content": "机器学习是人工智能的子领域，专注于从数据中学习的算法...",
      "summary": "机器学习是 AI 中从数据学习的子领域",
      "category": "concept",
      "confidence_score": 0.92,
      "confidence_tier": "extracted",
      "tags": ["AI", "机器学习", "算法"],
      "relations": [],
      "enrichments": [],
      "sources": [{"type": "document", "name": "AI Overview", "content_id": "6a69810fef276a17f2fb089f"}]
    }
  ]
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| entries_created | number | 提取出的条目数量 |
| entries | array | 知识条目对象数组 |
| entries[].id | string | 条目唯一 ID |
| entries[].title | string | 条目标题 |
| entries[].content | string | 条目的 Markdown 正文（仅包含文档中有的事实，不编造） |
| entries[].summary | string | 一句话摘要 |
| entries[].category | string | 分类：concept\|person\|project\|event\|location\|organization\|technology\|tool\|methodology\|product\|process\|terminology |
| entries[].confidence_score | number | 置信度 (0.0–1.0)，≥0.9=直接在文档中找到 |
| entries[].confidence_tier | string | 置信等级：extracted\|inferred\|ambiguous |
| entries[].tags | string[] | 2-5 个关键词 |
| entries[].relations | array | 与本条目相关的其他条目链接 |
| entries[].enrichments | array | AI 补充的背景知识和修正建议 |
| entries[].sources | array | 来源追踪（关联到源文档） |

**enrichments 子字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | detail_supplement\|background_context\|terminology_clarification\|relation_extension\|best_practice\|correction_challenge\|timeliness_note\|data_discrepancy\|source_gap |
| content | string | 补充/修正的内容 |
| target_text | string | 文档中与此相关的原文片段 |
| confidence | number | AI 对此补充的置信度 (0.0–1.0) |

---

### 2.2 批量提取

```
POST /restapi/wiki/extract-batch
```

一次提取多篇文档。自动跳过已提取的文档（当 `skip_if_extracted=true`）。

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| docs | array | 是 | 文档对象数组 |
| docs[].content | string | 是 | 文档正文 |
| docs[].content_id | string | 否 | 文档 ID |
| docs[].title | string | 否 | 文档标题 |
| docs[].tags | string[] | 否 | 标签 |
| skip_if_extracted | boolean | 否 | 跳过已提取的文档，默认 true |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/wiki/extract-batch \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "docs": [
      {"content": "# 文档一\n正文...", "content_id": "id1", "title": "文档一"},
      {"content": "# 文档二\n正文...", "content_id": "id2", "title": "文档二"}
    ],
    "skip_if_extracted": true
  }'
```

**返回**

```json
{
  "results": [
    {"docId": "id1", "created": 5},
    {"docId": "id2", "created": 0}
  ],
  "errors": [
    {"docId": "id3", "error": "content too short"}
  ],
  "total": 2,
  "extracted": 1,
  "skipped": 1
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| results | array | 每条文档的提取结果 |
| results[].docId | string | 文档 ID |
| results[].created | number | 该文档创建的知识条目数（0=已跳过） |
| errors | array | 提取失败的文档列表 |
| errors[].docId | string | 失败的文档 ID |
| errors[].error | string | 失败原因 |
| total | number | 传入的文档总数 |
| extracted | number | 实际提取的文档数 |
| skipped | number | 因已提取而跳过的文档数 |

---

### 2.3 整理知识

```
POST /restapi/wiki/organize
```

对用户的知识库执行去重、聚类、关联发现。**同步操作，耗时 1-5 分钟。** 建议在批量提取后执行一次。

**无请求体**（参数从 API Key 推断用户身份）。

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/wiki/organize \
  -H "Authorization: Bearer $API_KEY"
```

**返回**

```json
{
  "merged": 3,
  "linked": 15,
  "new_clusters": 4,
  "stale_flagged": 1,
  "insights": [
    {
      "insight": "「人工智能」「机器学习」「深度学习」三个条目形成紧密的知识群，覆盖了从基础到应用递进的层次结构",
      "supporting_entries": [
        {"id": "6a69...01", "title": "人工智能"},
        {"id": "6a69...02", "title": "机器学习"},
        {"id": "6a69...03", "title": "深度学习"}
      ]
    },
    {
      "insight": "产品相关的 5 篇文档中反复出现「用户体验」主题，建议创建专题页面汇总",
      "supporting_entries": [
        {"id": "6a69...04", "title": "产品设计原则"},
        {"id": "6a69...05", "title": "用户调研报告"}
      ]
    }
  ]
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| merged | number | 合并的重复条目数 |
| linked | number | 新建的语义链接数 |
| new_clusters | number | 发现的知识聚类数 |
| stale_flagged | number | 标记为过时的条目数 |
| insights | array | AI 生成的知识洞察 |
| insights[].insight | string | 洞察内容描述 |
| insights[].supporting_entries | array | 支撑该洞察的条目引用 |
| insights[].supporting_entries[].id | string | 条目 ID |
| insights[].supporting_entries[].title | string | 条目标题 |

---

### 2.4 条目列表

```
GET /restapi/wiki/entries
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | number | 否 | 返回数量上限 |
| offset | number | 否 | 偏移量 |
| category | string | 否 | 按分类筛选 |
| board | string | 否 | 按画板筛选 |
| status | string | 否 | 按状态筛选：active\|disabled\|deleted |
| content_ids | string | 否 | 逗号分隔的文档 ID，获取指定文档的条目 |

**返回**

```json
{
  "entries": [ { "id":"...", "title":"...", "summary":"...", "category":"...", "status":"active" } ],
  "total": 128
}
```

---

### 2.5 获取单条知识

```
GET /restapi/wiki/entries/:id
```

返回完整的条目对象（格式同 2.1 返回的 entries 数组元素）。

---

### 2.6 创建条目

```
POST /restapi/wiki/entries
```

手动创建知识条目。

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 条目标题 |
| content | string | 否 | Markdown 正文 |
| summary | string | 否 | 一句话摘要 |
| category | string | 否 | 分类 |
| tags | string[] | 否 | 标签 |
| content_ids | string[] | 否 | 关联的文档 ID 列表 |

---

### 2.7 更新条目

```
PUT /restapi/wiki/entries/:id
```

**请求体**：同 2.6，所有字段可选。

---

### 2.8 删除条目

```
DELETE /restapi/wiki/entries/:id
```

### 2.9 审核 Enrichment

```
PATCH /restapi/wiki/entries/:entryId/enrichments/:enrichmentId
```

AI 提取知识时会生成 enrichment（背景知识补充/修正建议）。通过此接口接受或拒绝。

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | 是 | `accept` 或 `reject` |
| merge | boolean | 否 | 接受时是否合入条目正文 |
| modified_content | string | 否 | 修改后的 enrichment 内容 |

---

### 2.10 知识搜索

```
GET /restapi/wiki/search
```

通过语义搜索（向量 + 关键词混合）查找相关知识条目。

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索查询 |
| max_results | number | 否 | 返回数量上限（默认 10） |
| root_id | string | 否 | 限定在某个文档树范围内搜索 |

**请求示例**

```bash
curl "https://www.2ryun.wiki/restapi/wiki/search?q=人工智能&max_results=5" \
  -H "Authorization: Bearer $API_KEY"
```

**返回**

```json
[
  {
    "id": "6a69810fef276a17f2fb0900",
    "title": "人工智能",
    "summary": "人工智能是计算机科学中研究智能系统的分支",
    "content": "人工智能（AI）是...",
    "category": "concept",
    "confidence_score": 0.95,
    "tags": ["AI", "技术"],
    "score": 0.987,
    "match_type": "semantic"
  }
]
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| [].id | string | 条目 ID |
| [].title | string | 条目标题 |
| [].summary | string | 条目摘要 |
| [].content | string | 条目正文 |
| [].category | string | 分类 |
| [].confidence_score | number | 置信度 |
| [].tags | string[] | 标签 |
| [].score | number | 与查询的相似度 (0–1) |
| [].match_type | string | 匹配方式：semantic\|keyword\|hybrid |

---

### 2.11 语义链接

```
POST /restapi/wiki/semantic-link
```

自动计算条目间的语义相似度并创建链接。

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| threshold | number | 否 | 相似度阈值，默认 0.65（0–1） |
| content_ids | string[] | 否 | 限定计算范围（指定文档的条目） |

**返回**

```json
{ "links_created": 42 }
```

---

### 2.12 知识图谱

```
GET /restapi/wiki/graph
GET /restapi/wiki/graph/data
```

`/graph` 返回可视化用的简化结构（节点+边）。  
`/graph/data` 返回带元数据的完整图谱数据。

**查询参数**：`root_id`（可选，限定范围）、`max_nodes`（可选，默认 200）

---

### 2.13 提取状态

```
GET /restapi/wiki/extracted-status
```

查询哪些文档已经被提取过。

**查询参数**：`content_ids` — 逗号分隔的文档 ID 列表

**请求示例**

```bash
curl "https://www.2ryun.wiki/restapi/wiki/extracted-status?content_ids=id1,id2,id3,id4" \
  -H "Authorization: Bearer $API_KEY"
```

**返回**

```json
{
  "extracted": ["id1", "id3"],
  "not_extracted": ["id2", "id4"]
}
```

---

### 2.14 知识库统计

```
GET /restapi/wiki/stats
```

返回用户的条目总数、各分类分布、各状态计数等汇总数据。

**返回**

```json
{
  "total_entries": 256,
  "by_category": {"concept": 120, "person": 30, "technology": 45},
  "by_status": {"active": 230, "disabled": 26},
  "by_confidence": {"extracted": 180, "inferred": 60, "ambiguous": 16},
  "total_links": 512,
  "total_clusters": 28
}
```

---

### 2.15 操作日志

```
GET /restapi/wiki/operation-log
```

**查询参数**：`limit`（默认 50）、`entry_id`（可选，筛选特定条目）

**返回**：操作记录数组，每条包含操作类型、时间、详情。

---

## 3. 网页生成 (Gen-HTML)

### 3.1 生成网页

```
POST /restapi/gen-html/generate
```

将 Markdown 文档转换为完整的 HTML 网页。**同步操作，耗时 30-120 秒。**

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 文档的 Markdown 正文 |
| title | string | 否 | 页面标题（默认 "Untitled"） |
| template | string | 否 | 模板名，默认 `article-magazine` |
| content_id | string | 否 | 关联的文档 ID |

**可用模板**：可通过 `GET /restapi/gen-html/templates` 获取完整列表。常用：
- `article-magazine` — 文章/博客类
- `documentation` — 技术文档
- `landing-page` — 产品落地页
- `magazine-minimal` — 极简站点

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/gen-html/generate \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Hello World\n\n这是我的第一篇 AI 生成网页。",
    "title": "My First Page",
    "template": "article-magazine"
  }'
```

**返回**

```json
{
  "generation_id": "6a69810fef276a17f2fb0900",
  "template": "article-magazine",
  "title": "My First Page",
  "size": 12580,
  "created_at": "2026-07-29T03:00:00.000Z"
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| generation_id | string | 生成记录唯一 ID |
| template | string | 使用的模板名 |
| title | string | 页面标题 |
| size | number | HTML 字节数 |
| created_at | string | 创建时间 |

---

### 3.2 模板列表

```
GET /restapi/gen-html/templates
```

**返回**

```json
{
  "templates": [
    {"name": "article-magazine", "label": "杂志文章", "description": "Substack / Medium 高级感长文排版", "category": "article", "has_example": true},
    {"name": "documentation", "label": "技术文档页", "description": "三栏文档页: 侧导航 + 正文 + 右 TOC", "category": "doc", "has_example": true},
    {"name": "landing-page", "label": "SaaS Landing", "description": "单页落地页", "category": "prototype", "has_example": true},
    {"name": "magazine-minimal", "label": "杂志风海报", "description": "极简杂志站点", "category": "poster", "has_example": true}
  ],
  "user_templates": []
}
```

---

### 3.3 模板预览

```
GET /restapi/gen-html/templates/:name/example
```

返回该模板的示例 HTML（**无需 API Key**）。

---

### 3.4 生成记录列表

```
GET /restapi/gen-html/generations
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content_id | string | 否 | 按源文档 ID 筛选 |
| limit | number | 否 | 返回数量上限 |
| offset | number | 否 | 偏移量 |

**返回**

```json
{
  "generations": [
    {
      "generation_id": "6a69810fef276a17f2fb0900",
      "title": "My First Page",
      "template": "article-magazine",
      "content_id": "6a69810fef276a17f2fb089f",
      "size": 12580,
      "visibility": "private",
      "created_at": "2026-07-29T03:00:00.000Z"
    }
  ],
  "total": 15
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| generations[].generation_id | string | 生成记录 ID |
| generations[].visibility | string | private\|published |

---

### 3.5 获取生成记录详情

```
GET /restapi/gen-html/generations/:id
```

返回单条记录元信息（不含 HTML，格式同 3.4 的数组元素）。

---

### 3.6 获取生成的 HTML

```
GET /restapi/gen-html/generations/:id/html
```

**返回**

```json
{ "html": "<!DOCTYPE html>\n<html>...完整的 HTML 页面...</html>" }
```

---

### 3.7 编辑 HTML

```
PUT /restapi/gen-html/generations/:id/html
```

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| html | string | 是 | 修改后的完整 HTML |
| overwrite | string | 否 | "true" 创建新版本，否则覆盖当前版本 |

---

### 3.8 删除生成记录

```
DELETE /restapi/gen-html/generations/:id
```

---

### 3.9 AI 对话编辑

```
POST /restapi/gen-html/generations/:id/chat
```

通过自然语言指令修改网页（如"把标题改为红色"）。

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| feedback | string | 是 | 编辑指令，用自然语言描述想要的修改 |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/gen-html/generations/xxx/chat \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"feedback": "请把页面标题颜色改为深蓝色，字号增大到 32px"}'
```

**返回**：更新后的 `{ generation_id, template, size }` 同 3.1。

---

### 3.10 发布 / 取消发布

```
POST /restapi/gen-html/generations/:id/publish
POST /restapi/gen-html/generations/:id/unpublish
```

发布后获得公开 URL。无需 API Key 即可通过 `GET /restapi/gen-html/public/:generation_id` 访问。

**返回**

```json
{ "message": "published", "generation_id": "xxx" }
```

---

### 3.11 保存封面

```
PATCH /restapi/gen-html/generations/:id/cover
```

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cover | string | 是 | base64 编码的图片数据（JPEG/PNG） |

---

### 3.12 公开访问（无需 API Key）

```
GET /restapi/gen-html/public/:generation_id
```

返回已发布的 HTML 页面。可直接在浏览器中打开。

---

## 4. 用户信息 (Users)

### 4.1 查询积分和配额

```
GET /restapi/users/quota
```

返回当前用户的积分、存储、文件、站点配额及使用情况。

**请求示例**

```bash
curl "https://www.2ryun.wiki/restapi/users/quota" \
  -H "Authorization: Bearer $API_KEY"
```

**返回**

```json
{
  "plan": "pro",
  "credits": {
    "current": 1850,
    "limit": 2000,
    "low": false,
    "expired": false,
    "expires_at": "2026-08-28T00:00:00.000Z",
    "days_left": 27
  },
  "storage": {
    "used": 5242880,
    "limit": 1073741824,
    "usage_percent": 0
  },
  "files": {
    "used": 15,
    "limit": 1000
  },
  "sites": {
    "used": 2,
    "limit": 10
  },
  "tokens": {
    "used": 450000,
    "limit": 100000
  }
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| plan | string | 套餐：free/pro/enterprise |
| credits.current | number | 当前剩余积分 |
| credits.limit | number | 积分上限 |
| credits.low | boolean | 积分 ≤ 0 |
| credits.expired | boolean | 积分已过期 |
| credits.expires_at | string\|null | 到期时间 ISO 8601，null=永不过期 |
| credits.days_left | number\|null | 剩余天数 |
| storage.used | number | 已用存储（字节） |
| storage.limit | number | 存储上限（字节） |
| storage.usage_percent | number | 使用百分比 |
| files.used | number | 已用文件数 |
| files.limit | number | 文件数上限 |
| sites.used | number | 已用站点数 |
| sites.limit | number | 站点数上限 |
| tokens.used | number | 累计消耗 token |
| tokens.limit | number | token 上限 |

---

## 5. 笔记 (Notes)

笔记（Note）是比文档更轻量的记录方式。与文档的关键区别：**笔记不进入知识库**，没有 Wiki 提取功能。适合随手记、灵感备忘、临时记录。

### 5.1 笔记列表

```
GET /restapi/note
```

列出当前用户的所有笔记。

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | number | 否 | 页码，默认 1 |
| pageSize | number | 否 | 每页数量，默认 20 |

**返回**

```json
{
  "notes": [
    {
      "_id": "6a69810fef276a17f2fb0900",
      "title": "会议备忘",
      "content": "# 今日会议\n\n1. 确认下周排期\n2. 整理需求文档",
      "createdAt": "2026-07-29T03:00:00.000Z",
      "updatedAt": "2026-07-29T03:00:00.000Z"
    }
  ],
  "total": 15
}
```

---

### 5.2 创建笔记

```
POST /restapi/note/create
```

**请求体 (JSON)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 笔记标题 |
| content | string | 否 | Markdown 格式正文，默认空字符串 |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/note/create \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "灵感备忘", "content": "想到一个好点子..."}'
```

**返回**

```json
{
  "message": "Note created successfully",
  "note": { "_id": "...", "title": "灵感备忘", "content": "..." }
}
```

---

### 5.3 获取笔记

```
GET /restapi/note/:id
```

返回单篇笔记的完整内容。格式同 5.1 返回的 notes 数组元素。

---

### 5.4 更新笔记

```
PUT /restapi/note/:id
```

**请求体 (JSON)**：所有字段均可选

| 参数 | 类型 | 说明 |
|------|------|------|
| title | string | 新标题 |
| content | string | 新正文 |

**请求示例**

```bash
curl -X PUT https://www.2ryun.wiki/restapi/note/6a69810fef276a17f2fb0900 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "更新后的备忘", "content": "补充了更多细节"}'
```

---

### 5.5 删除笔记

```
DELETE /restapi/note/:id
```

**返回**

```json
{ "message": "Note deleted successfully" }
```

---

### 5.6 复制笔记

```
POST /restapi/note/duplicate/:id
```

复制指定笔记。新笔记标题为原标题 + " (Copy)"。

---

## 6. 附件管理 (Attachments)

上传和管理图片、视频、文档等素材文件。与素材库共用同一套 Attachment 数据，通过该接口上传的文件可在 2Ryun 素材库中查看。

### 6.1 上传文件

```
POST /restapi/attachments/upload
```

上传单个文件（图片/视频/文档，multipart 字段名 `file`）。支持扩展名：`jpeg` `jpg` `png` `gif` `svg` `webp` `webm` `mp4` `mp3` `pdf` `docx` `xlsx` `ppt` `pptx` `xls` `doc` `txt` `md` `markdown` `csv` `html` `htm` `ico` `zip` `rar` `ogg` `wav`。单文件上限 20MB。

**请求格式**：`multipart/form-data`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 要上传的文件 |
| folderId | string | 否 | 素材文件夹 ID（不传则归入"未分组"） |

**请求示例**

```bash
curl -X POST https://www.2ryun.wiki/restapi/attachments/upload \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@cover.png" \
  -F "folderId=64f0a2b3c4d5e6f7a8b9c0d1"
```

**返回示例**

```json
{
  "message": "Attachment uploaded successfully",
  "file": {
    "_id": "64f0a2b3c4d5e6f7a8b9c0d1",
    "filename": "cover.png",
    "path": "uploads/2026/08/1692388-cover.png",
    "thumbnail": "uploads/2026/08/thumbnails/1692388-cover-thumb.jpg",
    "size": 20480,
    "mineType": "image/png",
    "fileType": ".png",
    "folderId": null,
    "createdBy": "64e0a2b3c4d5e6f7a8b9c0d2",
    "createdAt": "2026-08-19T08:00:00.000Z"
  }
}
```

文件访问 URL：`https://www.2ryun.wiki/<path>`（无需 API Key，可直接用于 `<img>` / `<video>`）。

### 6.2 多文件上传

```
POST /restapi/attachments/upload/multiple
```

一次上传最多 10 个文件（multipart 字段名 `file`，可重复）。

**返回**：`{ "message": "Attachments uploaded successfully", "files": [...], "success": true }`

### 6.3 附件列表

```
GET /restapi/attachments
```

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 筛选类型：`image` / `video` / `audio` / `document` |
| folderId | string | 否 | 按文件夹筛选（`null` 或空表示未分组） |
| keyword | string | 否 | 按文件名模糊搜索 |
| page | number | 否 | 页码，默认 1 |
| pageSize | number | 否 | 每页数量，默认 20 |

**返回**：`{ "success": true, "data": { "list": [...], "pagination": { "page", "pageSize", "total", "totalPages" } } }`

### 6.4 下载文件

```
GET /restapi/attachments/file/:id
```

返回附件文件流（`Content-Disposition: attachment`），`Content-Type` 为文件的 MIME。

### 6.5 删除附件

```
DELETE /restapi/attachments/:id
```

删除附件（同时删除物理文件与缩略图），并释放存储配额。

---

## 通用错误码

| 状态码 | 含义 | 常见原因 |
|--------|------|---------|
| 200 | 成功 | — |
| 201 | 创建成功 | — |
| 400 | 参数错误 | 缺少必填字段、content 过短 |
| 401 | 鉴权失败 | API Key 缺失或无效 |
| 402 | 积分不足 | 需充值后才能使用 AI 功能 |
| 403 | 无权访问 | 不是文档所有者、配额超限 |
| 404 | 资源不存在 | 文档/条目/生成记录 ID 无效 |
| 407 | Key 权限不足 | 该 Key 缺少 required 模块权限，去设置页调整 |
| 429 | 频率限制 | 请求太频繁，稍后重试 |
| 500 | 服务器错误 | 内部异常 |

### 积分不足（402）处理

涉及 AI 调用的接口在用户积分不足时会返回 402。Agent 应正确处理此错误。

**涉及的接口**：`wiki/extract`、`wiki/extract-batch`、`wiki/organize`、`genhtml/generate`。

**402 错误响应**：

```json
{
  "error": "积分不足，请充值"
}
```

**Agent 收到 402 时应**：
1. 告知用户积分已用完，引导到 `/pricing` 页面充值
2. 不要重试（积分不会自动恢复）
3. 已完成的非 AI 操作（如文档创建）仍然有效
