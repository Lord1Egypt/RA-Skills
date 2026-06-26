# 发布到 feima-lab 后端的完整流程

本 skill 从 v1.1 起支持把本地 `posts/<slug>/` 推到 feima-lab 后端，v1.2 起支持 tags 闭环 + 列表搜索 + 取消发布。下面描述的是 **Claude 调用脚本的路径**——不是用户手工跑的流程，除非用户明确说"我自己跑命令"。

## 前置：API Key

调用任何 api 脚本前，shell 必须已设置 `FX_AI_API_KEY`，且 **key 必须是 `internal` 类型**：

    export FX_AI_API_KEY=<your-internal-key>

**重要**：ContentApiController 标注了 `@ExternalApiAuth(level = ApiAuthLevel.INTERNAL)`。
`normal` 类型的 key 会被直接拒绝。从 https://platform.fenxiang-ai.com/ 登录后申请 internal key。

脚本第一次调用时如果 env 缺失，会输出：

    {"status":"error","error_type":"missing_api_key",...}

此时必须停下来告诉用户设置 env 后重新运行，**不要**尝试绕过或把 key 写到 MEMORY.md。

## 脚本全集（v1.2）

| 脚本 | 端点 | 用途 |
|---|---|---|
| `scripts/api/list-categories.mjs` | GET `/content/api/category/list` | 列分类，支持 `--route BLOG\|NEWS` 过滤 |
| `scripts/api/list-articles.mjs` | GET `/content/api/article/list` | 查文章列表，支持全部筛选条件 + 分页 |
| `scripts/api/list-tags.mjs` | GET `/content/api/tag/list` | 列所有已启用标签 |
| `scripts/api/get-article.mjs` | GET `/content/api/article/by-slug/{slug}` | 按 slug 查详情 |
| `scripts/api/upload-file.mjs` | POST `/content/api/upload` | 上传文件到 OSS |
| `scripts/api/save-article.mjs` | POST `/content/api/article/save` | 创建 / 更新文章（自动闭环 category + cover + tags） |
| `scripts/api/save-tag.mjs` | POST `/content/api/tag/save` | 创建单个标签 |
| `scripts/api/publish-article.mjs` | POST `/content/api/article/publish/{id}` | 发布草稿 |
| `scripts/api/unpublish-article.mjs` | POST `/content/api/article/unpublish/{id}` | 取消发布回草稿 |

## 完整发布路径（从零到已发布）

```
                              ┌──────────────────────────────┐
  render.mjs 成功生成           │ 本地 posts/<slug>/            │
  article.mdx + preview.html   │  ├── article.mdx              │
      ─────────────────►       │  ├── meta.json (draft)        │
                              │  ├── images/cover.webp        │
                              │  └── preview.html             │
                              └──────────────┬────────────────┘
                                             │
                               save-article.mjs --post-dir <path>
                                             │
                              ┌──────────────▼────────────────┐
                              │ 自动步骤（都在一次调用内）：     │
                              │ 1. 读 meta.json + article.mdx │
                              │ 2. 如果 categoryId 空 →        │
                              │    GET /category/list?        │
                              │    routeCode=<meta.route> 按  │
                              │    category 名字查 id         │
                              │ 3. 如果 coverImageUrl 空 →     │
                              │    POST /upload 上传          │
                              │    coverImage 本地路径        │
                              │ 4. 如果 tags 非空 →            │
                              │    GET /tag/list 查已有，     │
                              │    缺失的 POST /tag/save 建，  │
                              │    收集 tagIds                │
                              │ 5. POST /article/save         │
                              │    带 categoryId +            │
                              │    coverImageUrl + tagIds     │
                              │ 6. 写回 meta.publish.*        │
                              └──────────────┬────────────────┘
                                             │
                              publish-article.mjs --post-dir <path>
                                             │
                              ┌──────────────▼────────────────┐
                              │ 1. 从 meta.publish.remote_id  │
                              │    读 articleId               │
                              │ 2. POST /article/publish/{id} │
                              │ 3. meta.publish.status =      │
                              │    "published"                │
                              │    meta.publish.published_at  │
                              └───────────────────────────────┘
```

## 典型调用序列

### 首次创建 + 发布

    node <skill>/scripts/api/save-article.mjs    --post-dir posts/2026-04-10-xxx
    # → stdout: {"articleId":123,"slug":"2026-04-10-xxx","mode":"create","tagIds":[1,3]}

    node <skill>/scripts/api/publish-article.mjs --post-dir posts/2026-04-10-xxx
    # → stdout: {"articleId":123,"status":"published","slug":"2026-04-10-xxx"}

### 更新已发布的文章

    # 改动 article.mdx 或 meta.json 后
    node <skill>/scripts/api/save-article.mjs    --post-dir posts/2026-04-10-xxx
    # → mode: "update"（因为 meta.publish.remote_id 已有值）
    # 注意：update 不会自动重新发布。如果该文章原本是"已发布"状态，
    # 后端会根据 save 的逻辑决定是否需要再调 publish（v1 保持保守，
    # 让 Claude 显式决定是否要再次 publish）

### 下线已发布的文章

    node <skill>/scripts/api/unpublish-article.mjs --post-dir posts/2026-04-10-xxx
    # → {"articleId":123,"status":"draft",...}
    # 语义：前端不再展示，但 publishTime 保留

### 查远程状态

    node <skill>/scripts/api/get-article.mjs --post-dir posts/2026-04-10-xxx
    # 或
    node <skill>/scripts/api/get-article.mjs --slug 2026-04-10-xxx
    # 不存在：exit 2 + error_type=not_found

### 判断 slug 是否被占用

    node <skill>/scripts/api/list-articles.mjs --slug 2026-04-10-xxx
    # → totalCount=0 说明未占用，>0 已占用
    # （这个接口在传 slug 时会忽略其他筛选，专门用于查重）

### 列已发布博客 / 按标签浏览

    node <skill>/scripts/api/list-articles.mjs --route BLOG --publish-status 1 --format table
    node <skill>/scripts/api/list-articles.mjs --tag Agent --format table

### 列出所有分类 / 标签

    node <skill>/scripts/api/list-categories.mjs --route BLOG --format table
    node <skill>/scripts/api/list-tags.mjs --format table

### 手工创建一个标签

    node <skill>/scripts/api/save-tag.mjs --name "LangChain4j"
    # 一般不用手工调，save-article 内部会自动建

## 路由建议（Claude 决策）

| 用户意图 | 动作 |
|---|---|
| "发布这篇文章" / "推到 feima-lab" / "上线" | save-article → publish-article 串联跑 |
| "写一篇博客" / "技术文章" | meta.route = "BLOG" |
| "发公告" / "动态" / "新闻" | meta.route = "NEWS" |
| "更新已发布文章" / "改了重推" | save-article（会自动进 update mode） |
| "下线这篇" / "撤回" / "取消发布" | unpublish-article |
| "查远程版本" / "后端是什么状态" | get-article |
| "这个 slug 能用吗" / "有重名吗" | list-articles --slug `<slug>` |
| "列一下我发过的所有博客" | list-articles --route BLOG |
| "列一下某标签下的文章" | list-articles --tag `<name>` |
| "后端有哪些分类" | list-categories --format table |
| "后端有哪些标签" | list-tags --format table |
| "上传一张图" | upload-file --file `<path>`（save-article 内部会自动调） |
| "API 报错了怎么处理" | （查 stderr 的 error_type，Read `api-error-handling.md`） |
| "删掉这篇文章" | **v1.2 不支持**，告诉用户 v2 再做（防止误操作） |

**强制规则**：
- 调用 API 脚本前**必须 Read** `references/api-publish-workflow.md` 和按需 Read `references/api-error-handling.md`
- 如果 stderr 返回 `{"error_type": "missing_api_key"}` → 立刻停下告诉用户设 env var，**禁止**自动把 key 写 MEMORY.md
- save-article / publish-article / unpublish-article 的结果（articleId / tagIds / published_at）会自动回写 meta.json，**不要手工修改** `publish.remote_id` / `publish.published_at` / `publish.last_saved_tag_ids`

## 渐进式输出规则

每一步完成后立即告知用户进度，不要攒到最后：

    1. "正在查询 category id (route=BLOG)..."（list-categories）
    2. "正在上传封面图..."（upload）
    3. "正在处理 tags: Agent, LangChain4j..."（list-tags + save-tag if needed）
    4. "save 完成，articleId=123, tagIds=[1,3]"（save）
    5. "publish 完成，状态已变为 published"（publish）

## 错误时的处理

遇到 `error_type`：

| 类型 | 立即动作 |
|---|---|
| `missing_api_key` | 停下，告诉用户设置 internal 类型的 env var |
| `invalid_meta` | 根据错误信息补全 meta.json 缺的字段，重试 |
| `file_not_found` | 告诉用户先跑 image-localize.mjs 或写 article.mdx |
| `api_unavailable` | 告诉用户服务可能暂时不可用；不要自动重试超过 1 次 |
| `api_error` | 读 message 字段，按后端描述的问题修正 |
| `not_found` (get-article 专属, exit 2) | 告诉用户"后端没这篇文章"，按意图改走 save 路径 |

详见 `api-error-handling.md`。

## v1.2 不做的事

- **不自动 delete**：破坏性操作一律让用户手动跑（v2 再加相应脚本）
- **不自动重试**：save/publish/unpublish 失败就报错，让用户看日志决定要不要再跑
- **不支持 tag 删除**：`POST /tag/delete/{id}` 本 skill 不包装（已关联的 tag 关系不会清理，语义较怪）
- **不做本地 ↔ 远程 diff**：没有 sync 能力，用户要自己清楚本地是最新还是远程是最新
- **不处理 subCategory**：API 无对应字段，本地字段保留但不上传
