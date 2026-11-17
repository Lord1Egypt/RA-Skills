---
name: 2ryun-api-cn
description: 当用户想导入文档、构建知识库、搜索结构化知识、从内容生成网页或发布内容时使用。当用户提到 2Ryun、第二现实、知识库、文档管理、知识图谱、网页、发布时使用。2Ryun 是 AI 时代的知识/内容平台，文档启用知识提取后自动在后台完成提取、组织、关联——Agent 的职责是判断哪些文档应进入知识库、哪些不应进入。
---

# 2Ryun — AI 时代知识/内容底座

2Ryun（第二现实）为 AI Agent 提供文档管理、知识库、网页生成、笔记等能力。所有操作通过 REST API 调用（`Authorization: Bearer <key>` 鉴权，Key 从 2Ryun 设置页获取，格式为 `sk-` 前缀 + 多段随机字符）。

**API 技术文档**: `2ryun-api-spec-cn.md` — 完整 endpoint、参数、返回格式。

> **国内站版**：本 Skill 面向国内站 www.2ryun.wiki。海外用户请使用 2ryun.com 版（`2Ryun-skill`）。

## 核心机制：自动知识提取

**提取和组织是 2Ryun 自动完成的，Agent 不需要手动调用 extract/organize API。** Agent 只需要：

1. 创建文档时通过 `setting.wikiAutoExtract` 决定是否让这篇文档进入知识库
2. 写入后 2Ryun 自动在后台完成提取、去重、关联

### 判断标准：哪些文档该进入知识库

**✅ 适合进入知识库**（`"wikiAutoExtract": true`）：
- 用户原创的文档、笔记、研究
- 从外部导入的参考资料、报告、论文
- 包含用户自己的观点、数据、经验的内容
- 任何"新知识"——用户提供的不存在于已有知识库中的信息

**❌ 不适合进入知识库**（`"wikiAutoExtract": false`，或不设置）：
- 从知识库检索内容生成的报告、总结（没有新知识点，只是已有知识的重组）
- AI 生成的草稿、临时内容
- 会议记录草稿、待整理的随手笔记
- 任何"已有知识的衍生品"——会浪费 AI 算力和 token

**核心原则**：如果一个文档是根据知识库中的知识生成的，它就不应该再被提取回知识库。只有包含新信息的文档才值得进入。

---

## 能力一：文档管理底座

积累和管理文档，并决定哪些进入知识库。

### 场景 1.1：创建 / 导入文档

**从文本内容创建**：
```bash
curl -X POST https://www.2ryun.wiki/restapi/documents/create \
  -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "文档标题",
    "content": "Markdown 正文",
    "tags": ["标签1"],
    "setting": {"wikiAutoExtract": true}
  }'
```
`"wikiAutoExtract": true` 表示这篇文档应进入知识库。如果是衍生内容则设为 `false`。

**⚠️ 提取需要时间**：文档创建后，2Ryun 在后台异步提取和组织知识，**不会立即出现在知识库中**。单篇文档通常 1-3 分钟，批量可能更长。如果创建后立刻搜索，可能查不到刚入库的内容。告知用户稍等片刻再查询。

**从文件导入**：
```bash
curl -X POST https://www.2ryun.wiki/restapi/documents/import \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@/path/to/file.pdf" -F "title=文档标题"
```
导入的文档默认自动提取。支持 pdf、docx、xlsx、pptx、md、txt、html。

### 场景 1.2：检索文档

```bash
# 列表
curl "https://www.2ryun.wiki/restapi/documents?page=1&pageSize=20" \
  -H "Authorization: Bearer $API_KEY"
# 搜索
curl "https://www.2ryun.wiki/restapi/documents/search?q=关键词" \
  -H "Authorization: Bearer $API_KEY"
# 获取单篇
curl "https://www.2ryun.wiki/restapi/documents/:id" -H "Authorization: Bearer $API_KEY"
```

### 场景 1.3：更新 / 删除

- `PUT /restapi/documents/update/:id -d '{"title":"...","content":"..."}'`
- `DELETE /restapi/documents/delete/:id`

---

## 能力二：使用结构化知识库

知识库在文档创建时自动构建（提取→组织→关联）。Agent 只需查询和使用。

### 场景 2.1：搜索知识库

用户说："帮我查一下 XX 相关的知识" / "我的知识库里有什么关于 XX 的"

```bash
curl "https://www.2ryun.wiki/restapi/wiki/search?q=查询词&max_results=10" \
  -H "Authorization: Bearer $API_KEY"
```
返回语义相似的知识条目，按相关度排序。用于回答问题、查找背景信息、辅助写作。

### 场景 2.2：查看知识图谱

```bash
# 可视化用（节点+边）
curl "https://www.2ryun.wiki/restapi/wiki/graph?root_id=xxx" -H "Authorization: Bearer $API_KEY"
# 带元数据
curl "https://www.2ryun.wiki/restapi/wiki/graph/data?max_nodes=100" -H "Authorization: Bearer $API_KEY"
```
用于了解知识结构、发现关联、识别知识空白。

### 场景 2.3：查看知识库状态

```bash
# 条目列表
curl "https://www.2ryun.wiki/restapi/wiki/entries?limit=100" -H "Authorization: Bearer $API_KEY"
# 统计
curl "https://www.2ryun.wiki/restapi/wiki/stats" -H "Authorization: Bearer $API_KEY"
# 哪些文档已提取
curl "https://www.2ryun.wiki/restapi/wiki/extracted-status?content_ids=id1,id2" \
  -H "Authorization: Bearer $API_KEY"
```

### 场景 2.4：手动提取（仅在需要时）

当用户明确要求重新提取或手动控制时：

- `POST /restapi/wiki/extract` — 单篇提取
- `POST /restapi/wiki/extract-batch` — 批量提取
- `POST /restapi/wiki/organize` — 手动整理

**大多数情况下不需要调用这些**，因为文档创建时已自动触发。

---

## 能力三：可视化发布

将内容和知识转化为精美网页并发布。

### 场景 3.1：单篇文档生成网页

1. 获取文档：`GET /restapi/documents/:id`
2. **选择模板**：先获取可用模板列表，根据内容类型选择最合适的：
   ```bash
   curl "https://www.2ryun.wiki/restapi/gen-html/templates" -H "Authorization: Bearer $API_KEY"
   ```
   返回模板名和描述。LLM 根据文档内容判断：长文博客→`article-magazine`，技术文档→`documentation`，产品介绍→`landing-page`。**不要硬编码模板**，始终从接口获取并根据内容匹配。
3. **生成**：
   ```bash
   curl -X POST https://www.2ryun.wiki/restapi/gen-html/generate \
     -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
     -d '{"content":"Markdown 内容","title":"页面标题","template":"选定的模板名"}'
   ```
4. 发布：`POST /restapi/gen-html/generations/GEN_ID/publish`
5. URL：`https://www.2ryun.wiki/restapi/gen-html/public/GEN_ID`

### 场景 3.2：知识搜索 + 生成网页报告

1. 搜索：`GET /restapi/wiki/search?q=主题&max_results=10`
2. 汇总搜索结果为一篇 Markdown 报告
3. 生成网页：`POST /restapi/gen-html/generate`
4. 发布

**注意**：生成的报告是新文档，但内容来源于已有知识库，**不应设置 `wikiAutoExtract: true`**。

### 场景 3.4：聊天式编辑网页

已生成的网页可以通过对话方式继续编辑：

```bash
curl -X POST https://www.2ryun.wiki/restapi/gen-html/generations/GEN_ID/chat \
  -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
  -d '{"feedback": "把标题改成红色，字号加大到 48px"}'
```

支持选中页面的某个局部区域进行针对性编辑，传入选中区域的 HTML：
```bash
curl -X POST https://www.2ryun.wiki/restapi/gen-html/generations/GEN_ID/chat \
  -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
  -d '{"feedback": "把这段改成蓝色背景", "selected_html": "<div>...</div>"}'
```

---

## 能力四：轻量级笔记

笔记（Note）比文档更轻量，不提取知识库，适合日常记录、随手记、灵感备忘。

### 创建笔记
```bash
curl -X POST https://www.2ryun.wiki/restapi/note/create \
  -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
  -d '{"title": "会议备忘", "content": "Markdown 正文"}'
```

### 列表 / 搜索 / 更新 / 删除
- `GET /restapi/note?page=1&pageSize=20` — 笔记列表
- `GET /restapi/note/:id` — 获取单篇
- `PUT /restapi/note/update/:id -d '{"title":"...","content":"..."}'` — 更新
- `DELETE /restapi/note/delete/:id` — 删除

**笔记 vs 文档**：笔记**不进入知识库**，没有 `wikiAutoExtract` 设置。适合临时内容、随手记、灵感备忘。需要长期保存并进入知识库的内容用文档。

---

## 能力五：素材上传（图片 / 视频）

上传图片、视频等素材文件，返回可直接访问的 URL。

### 上传单个文件

```bash
curl -X POST https://www.2ryun.wiki/restapi/attachments/upload \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@/path/to/image.png" \
  -F "folderId=可选，素材文件夹ID"
```

返回 JSON 的 `file.path` 即文件路径，完整访问 URL = `https://www.2ryun.wiki/<path>`（无需 API Key，可直接用于 `<img>` / `<video>`）。

### 多文件上传

```bash
curl -X POST https://www.2ryun.wiki/restapi/attachments/upload/multiple \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@a.png" -F "file=@b.mp4"
```

一次最多 10 个文件。

### 列表 / 下载 / 删除

- `GET /restapi/attachments?type=image` — 列表（`type`: image/video/audio/document，支持分页、关键词、文件夹）
- `GET /restapi/attachments/file/:id` — 下载文件
- `DELETE /restapi/attachments/:id` — 删除

支持格式：图片（png/jpg/jpeg/gif/svg/webp）、视频（mp4/webm）、音频、文档等，单文件上限 20MB。

---

## 错误处理

| 状态码 | 含义 | Agent 行为 |
|--------|------|------------|
| 200 | 成功 | — |
| 400 | 参数错误 | 检查请求体，修正后重试一次 |
| 401 | API Key 无效或缺失 | 提示用户检查 Key 是否正确，或去设置页重新生成 |
| 402 | 积分/配额不足 | 告知用户，引导到 `/pricing` 升级，**不要重试** |
| 407 | Key 权限不足 | 返回 `INSUFFICIENT_SCOPE`，提示用户去设置页为 Key 勾选所需模块权限（documents/wiki/gen-html/note/attachments） |
| 404 | 资源不存在 | 确认 ID 是否正确 |
| 429 | 请求过于频繁 | 等待 `Retry-After` 秒后重试，或降低请求频率 |
| 500 | 服务端错误 | 等待 3 秒后重试一次，仍失败则告知用户稍后再试 |

---

## 快速参考

| 任务 | 端点 | 说明 |
|------|------|------|
| 创建文档 | `POST /restapi/documents/create` | `setting.wikiAutoExtract` 决定是否入知识库 |
| 导入文件 | `POST /restapi/documents/import` | 自动转换格式，导入为文档 |
| 搜索知识 | `GET /restapi/wiki/search?q=...` | 语义搜索 |
| 创建笔记 | `POST /restapi/note/create` | 轻量记录，不提取知识库 |
| 查询积分 | `GET /restapi/users/quota` | 积分、配额、有效期 |
| 生成网页 | `POST /restapi/gen-html/generate` | 30-120s |
| 聊天编辑 | `POST /restapi/gen-html/generations/:id/chat` | 对话式编辑网页 |
| 发布 | `POST /restapi/gen-html/generations/:id/publish` | 获取公开 URL |
| 上传素材 | `POST /restapi/attachments/upload` | 图片/视频/文档，返回可访问 URL |

## 重要细节

**URL 编码**：查询参数中包含中文等非 ASCII 字符时，必须 URL 编码。curl 使用 `--data-urlencode`，编程语言使用 `encodeURIComponent` / `urlencode`。

```bash
# ✅ 正确 — curl 自动编码
curl --get "https://www.2ryun.wiki/restapi/wiki/search" \
  --data-urlencode "q=迪赞文化" \
  -H "Authorization: Bearer $API_KEY"

# ❌ 错误 — 中文直接拼接
curl "https://www.2ryun.wiki/restapi/wiki/search?q=迪赞文化"
```

**文档树**：创建文档时，`rootId` 和 `parentId` 必须**同时存在**才能准确构建文档树：
- 根文档（一级文档）：`rootId` 和 `parentId` 设为**同一个值**（都等于根文档自己的 ID）
- 子文档：`rootId` 指向根文档，`parentId` 指向直接父文档
- 不传这两个字段则创建独立文档（不属于任何树）

## 重要规则

1. **先问 API Key**：用户需要从 2Ryun 设置页的「API Keys」标签创建
2. **判断是否入知识库**：创建文档前想清楚——这是新知识还是已有知识的衍生品？
3. **衍生内容不入库**：从知识库检索生成的内容，设 `wikiAutoExtract: false`
4. **笔记不提取**：笔记没有 `wikiAutoExtract` 选项，天生不进知识库。临时记录、灵感备忘用笔记
5. **不需要手动提取**：2Ryun 自动完成，Agent 只需正确设置 `setting`
6. **始终给出最终 URL**：发布后把链接给用户
7. **402 积分不足**：告知用户，引导到 `/pricing`，不重试
8. **出错不重试超过 1 次**：400 修正后可重试一次，401/402/407 不重试，429 等待后重试，500 等待 3s 后重试一次
