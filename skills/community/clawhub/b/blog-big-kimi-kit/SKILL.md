---
name: blog-big-kimi-kit
version: 0.1.0
description: |
  博客内容发布 Skill，基于 FastAPI 博客系统 OpenAPI 文档自动生成。
  覆盖文章/标签/用户/评论/留言/说说/文件上传/健康检查全部 API。
triggers:
  - 博客文章管理
  - 博客内容发布
  - 查询博客文章
  - 博客标签管理
  - 博客留言管理
  - 博客说说管理
tags:
  - blog
  - content-publish
  - rest-api
  - fastapi
tools:
  - curl
---

# blog-big-kimi-kit

博客内容发布 Skill，覆盖文章/标签/用户/评论/留言/说说/文件上传/健康检查全部 API。公开 API（无认证）。

## 安全硬约束（必须遵守）

**通用约束（所有 skill 必含）**：

1. 严禁读取 data/、configs/、sessions.db、user_accounts 等 Grape 内部数据。
2. API 返回 403/无权限时：立即停止该操作并回复用户，严禁尝试其他 token 或绕行手段。
3. 所有 curl / API 调用设 30s 超时——超时判定失败，不 hang。
4. 严禁 mock 模式/假数据：所有 API 调用必须真实访问目标系统。
5. 调用目标 API 一律以 `references/api-reference.md` 为准：严禁根据经验/记忆/猜测自行拼写 API 路径。

## 评论规范

- 所有 Issue/PR 评论 body 必须以 `[blog-big-kimi-kit]` 开头（如果环境变量未注入，使用 skill name 作为前缀）
- 引用用户原文：`> {用户评论}\n\n[blog-big-kimi-kit] {回复}`

## Configuration

目标系统 API 地址必须在使用前确定。所有命令中的 `{base_url}` 替换为实际地址（格式 `http://<host>:<port>`）。

`{base_url}` 解析优先级：

1. **项目知识** — 检查 `.project-info/` 目录下 JSON 配置文件（config.BLOG_BIG_KIMI_KIT_BASE_URL）
2. **环境变量** — `BLOG_BIG_KIMI_KIT_BASE_URL`
3. **当前上下文** — 用户直接提供或 A2A context 中已包含
4. **交互输入** — 以上都无时提示用户输入

### 配置指导

**方式一：环境变量（临时，推荐快速测试）**

```bash
export BLOG_BIG_KIMI_KIT_BASE_URL="http://<host>:<port>"
# 本 API 为公开 API（无认证），不需要额外凭据
```

**方式二：项目知识 JSON 文件（持久化，推荐生产使用）**

在项目根目录下创建 `.project-info/` 目录，放入任意名称的 `.json` 文件（脚本会递归扫描所有 JSON 文件）：

```json
{
  "config": {
    "BLOG_BIG_KIMI_KIT_BASE_URL": "http://<host>:<port>"
  }
}
```

> key 必须按 `BLOG_BIG_KIMI_KIT_` 前缀命名（由 skill name 推导），避免与其他系统凭据冲突。
> ⚠️ `.project-info/` 含敏感凭据，不提交到 git 仓库（加入 .gitignore）。

## 场景 / When to Use

- 用户要求查询博客文章列表、文章详情、热门文章
- 用户要求创建/更新/删除/恢复博客文章
- 用户要求管理博客标签（创建/查询）
- 用户要求管理博客用户（创建/查询）
- 用户要求管理博客评论（创建/查询/删除）
- 用户要求管理博客留言（创建/查询/回复/删除）
- 用户要求管理博客说说（创建/查询/删除）
- 用户要求上传/查询/删除文件
- 用户要求检查博客系统健康状态

Don't use for: 非本博客 API 的操作；后台管理页面登录相关操作（/admin/* 端点不含明确文档定义，不在覆盖范围内）。

## 知识 / Knowledge

### API Base URL

```
{base_url}
```

All endpoints below are relative to this base. 无认证（公开 API），不需要 header。

### Endpoints

按资源分组列出端点表（从 API 文档解析）：

**健康检查**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /health | - | 健康检查 |

**文章**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/articles | - | 查询文章列表（分页+标签筛选+关键词） |
| POST | /api/articles | ArticleCreate | 创建文章 |
| GET | /api/articles/{article_id} | - | 查询文章详情（含评论） |
| PUT | /api/articles/{article_id} | ArticleUpdate | 更新文章 |
| DELETE | /api/articles/{article_id} | - | 删除文章（支持软删除） |
| GET | /api/articles/heat/top | - | 查询热门文章 |
| POST | /api/articles/{article_id}/restore | - | 恢复已删除文章 |

**标签**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/lables | - | 查询标签列表 |
| POST | /api/lables | LableCreate | 创建标签 |

> ⚠️ API 路径实际拼写为 `/api/lables`（非 labels），子命令用正确拼写 `labels`，脚本内部请求时用实际路径 `lables`。

**用户**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/users | - | 查询用户列表 |
| POST | /api/users | UserCreate | 创建用户 |

**评论**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/comments/{aid} | - | 查询文章评论列表 |
| POST | /api/comments | CommentCreate | 创建评论 |
| DELETE | /api/comments/{comment_id} | - | 删除评论 |

**留言**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/messages | - | 查询留言列表 |
| POST | /api/messages | MessageCreate | 创建留言 |
| POST | /api/messages/reply | Message2Create | 回复留言 |
| DELETE | /api/messages/{message_id} | - | 删除留言 |

**说说**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/moods | - | 查询说说列表 |
| POST | /api/moods | MoodCreate | 创建说说 |
| DELETE | /api/moods/{mood_id} | - | 删除说说 |

**文件上传**

| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /api/upload | multipart/form-data | 上传单个文件 |
| POST | /api/upload/multiple | multipart/form-data | 批量上传文件 |
| GET | /api/uploads/list | - | 查询已上传文件列表 |
| DELETE | /api/uploads/{filename} | - | 删除已上传文件 |

### 认证方式

- 无认证（公开 API）：不需要凭据
- API 地址：BLOG_BIG_KIMI_KIT_BASE_URL

**凭据前缀**：由 skill name 推导（`blog-big-kimi-kit` → `BLOG_BIG_KIMI_KIT`），skill name 转大写下划线。

### Common Pitfalls

1. **API 路径拼写 lables**。标签端点实际路径为 `/api/lables`（非 `labels`），子命令用正确拼写 `labels`，脚本内部请求时用实际路径 `lables`。
2. **文章详情返回嵌套结构**。`GET /api/articles/{id}` 返回 `{"code":200,"data":{"article":{...},"comments":[...]}}`，article 和 comments 是嵌套字段。
3. **文章删除默认软删除**。`DELETE /api/articles/{id}` 默认 `soft=true`，需用 `restore-article` 恢复。传 `--soft false` 硬删除。
4. **文件上传用 multipart/form-data**。`POST /api/upload` 字段名 `file`，`/api/upload/multiple` 字段名 `files`，不是 JSON body。脚本用 `files=` 参数传递。
5. **分页参数 page/size**。`GET /api/articles` 支持 `page`（默认1）、`size`（默认10，最大100）、`lid`（标签筛选，默认0=不限）、`keyword`（关键词搜索）。
6. **说说创建 content 必填**。`POST /api/moods` 的 `content` 字段必填，`title` 和 `src` 可选。

### 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 是（创建文章） | - | 文章标题 |
| content | string | 是（创建文章/评论/留言/说说） | - | 内容 |
| uid | integer | 否 | 1（文章）/ 必填（评论/留言） | 用户 ID |
| lid | integer | 否 | 1 | 标签 ID |
| img | string/null | 否 | null | 文章封面图 |
| heat | integer | 否 | 0 | 热度值 |
| uname | string | 是（创建用户） | - | 用户名 |
| phone | string | 否 | "" | 手机号 |
| pwd | string | 否 | "" | 密码 |
| email | string | 否 | "" | 邮箱 |
| aid | integer | 是（创建评论/查询评论） | - | 文章 ID |
| mid | integer | 是（回复留言） | - | 留言 ID |
| lname | string | 是（创建标签） | - | 标签名 |
| src | string | 否（说说） | "" | 说说来源/配图 |
| soft | boolean | 否（删除文章） | true | 是否软删除 |
| page | integer | 否（文章列表） | 1 | 页码 |
| size | integer | 否（文章列表） | 10 | 每页数量（最大100） |
| keyword | string | 否（文章列表） | "" | 关键词搜索 |
| limit | integer | 否（热门文章） | 5 | 返回数量（最大20） |

## 步骤 / Steps

### 1. 检查 API 可达性

```bash
python3 scripts/blog-big-kimi-kit.py health-check
```
Expected: `{"status":"ok","service":"blog-api","version":"1.0.0"}`

### 2. 查询可用资源

```bash
python3 scripts/blog-big-kimi-kit.py list-articles
```
Expected: `{"code":200,"data":[...],"total":N,"page":1,"size":10}`

### 3. 执行操作

所有子命令均支持 `--format json|md`（默认 json）。下表列出各子命令的专属参数（必填项标注 *）：

| 子命令 | 参数 | Expected |
|--------|------|----------|
| health-check | - | `{"status":"ok",...}` |
| list-articles | --page, --size, --lid, --keyword | `{"code":200,"data":[...],"total":N}` |
| get-article | --article-id* | `{"code":200,"data":{"article":{...},"comments":[...]}}` |
| create-article | --title*, --content*, --uid, --lid, --img, --heat | `{"code":200,"data":{"id":...}}` |
| update-article | --article-id*, --title, --content, --lid, --img, --heat | `{"code":200,"data":{...}}` |
| delete-article | --article-id*, --soft | `{"code":200,...}` |
| restore-article | --article-id* | `{"code":200,...}` |
| top-articles | --limit | `{"code":200,"data":[{"id":...,"title":...,"heat":...}]}` |
| list-labels | - | `{"code":200,"data":[{"id":1,"lname":"技术"}]}` |
| create-label | --lname* | `{"code":200,"data":{...}}` |
| list-users | - | `{"code":200,"data":[{"id":1,"uname":"admin"}]}` |
| create-user | --uname*, --phone, --pwd, --email, --img | `{"code":200,"data":{...}}` |
| list-comments | --aid* | `{"code":200,"data":[...]}` |
| create-comment | --uid*, --aid*, --content* | `{"code":200,"data":{...}}` |
| delete-comment | --comment-id* | `{"code":200,...}` |
| list-messages | - | `{"code":200,"data":[...]}` |
| create-message | --uid*, --content* | `{"code":200,"data":{...}}` |
| reply-message | --uid*, --mid*, --content* | `{"code":200,"data":{...}}` |
| delete-message | --message-id* | `{"code":200,...}` |
| list-moods | - | `{"code":200,"data":[...]}` |
| create-mood | --content*, --title, --src | `{"code":200,"data":{...}}` |
| delete-mood | --mood-id* | `{"code":200,...}` |
| upload-file | --filepath* | `{"code":200,"data":{...}}` |
| upload-files | --filepaths*（多个） | `{"code":200,"data":{...}}` |
| list-uploads | - | `{"code":200,"data":[...]}` |
| delete-upload | --filename* | `{"code":200,...}` |
| capability-list | - | `{"capability":"capability-list",...}` |

示例：
```bash
python3 scripts/blog-big-kimi-kit.py list-articles --page 1 --size 10
python3 scripts/blog-big-kimi-kit.py get-article --article-id 1
python3 scripts/blog-big-kimi-kit.py create-article --title "标题" --content "内容"
python3 scripts/blog-big-kimi-kit.py upload-file --filepath /path/to/file.png
```

## 判断标准 / Verification

- [ ] API 可达（GET /health 返回 200）
- [ ] 只读操作返回有效数据（非空/字段完整）
- [ ] 脚本 --help 无语法错误
- [ ] 退出码正确（0=成功/2=参数错误/3=缺少配置/4=API失败）

## 输出规范 / Output Format

### 脚本输出

- 默认输出：JSON
- 可选输出：Markdown 表格（--format md）
- 使用示例：`cd skills/blog-big-kimi-kit/ && python3 scripts/blog-big-kimi-kit.py list-articles`

### Issue 评论格式

执行完操作后，Issue 评论 body 格式：

```
[blog-big-kimi-kit] ✅ {操作名称}完成

## 操作结果

| 操作 | 状态 | 资源 ID | 详情 |
|------|------|---------|------|
| {操作名} | ✅ 成功 / 🔴 失败 | {id} | {简要说明} |

**API 地址**：{base_url}
**执行时间**：{UTC ISO}
```

失败时：

```
[blog-big-kimi-kit] 🔴 {操作名称}失败

## 错误分析

- **操作**：{操作名}
- **错误**：{API 返回的错误信息}
- **HTTP 状态码**：{code}
- **原因**：{分析原因}

### 修复建议
{修复步骤}
```

## 参考文档 / References

- [API 端点文档](references/api-reference.md)
- [测试用例](templates/test-vars.json)

## 分析结论示例

成功时：

```
分析结论：
- 场景：博客内容发布
- Skill：blog-big-kimi-kit v0.1.0
- 操作：list-articles
- 结果：✅ 成功（返回 N 篇文章）
- 必须执行：Issue 评论汇总结果 → 任务结束
```

失败时：

```
分析结论：
- 场景：博客内容发布
- Skill：blog-big-kimi-kit v0.1.0
- 操作：create-article
- 结果：🔴 失败（API 返回 422 参数校验错误）
- 必须执行：Issue 评论报告错误 → 任务结束
```

## 任务结束

完成所有业务动作后，在最终答复末尾输出以下 JSON 块并结束任务：

```json
{
  "actions": ["{具体执行的操作}"],
  "conclusion": "{处理结论}",
  "artifacts": ["{产生的产物}"],
  "next_step": "{下一步建议}",
  "issue_summary": "{Issue 最新聚合结论，紧凑文本，用 | 分隔}"
}
```

注意：只输出一个 JSON 块，放在答复末尾。
