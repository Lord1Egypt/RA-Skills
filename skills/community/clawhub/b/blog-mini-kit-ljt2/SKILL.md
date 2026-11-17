---
name: blog-mini-kit-ljt2
version: 0.1.0
description: |
  博客系统 API 管理工具，覆盖文章/标签/用户/评论/留言/说说/文件上传/健康检查 8 大资源域 26 个端点。
  无认证（公开 API），提供统一的内容管理能力。
triggers:
  - 博客
  - 文章管理
  - 评论留言
  - 说说
  - 文件上传
tags:
  - blog
  - fastapi
  - content-management
  - rest-api
tools:
  - curl
---

# blog-mini-kit-ljt2

博客系统 API 管理工具（FastAPI，无认证公开 API），覆盖 8 大资源域 26 个端点。

## 安全硬约束（必须遵守）

1. 严禁读取 data/、configs/、sessions.db、user_accounts 等 Grape 内部数据。
2. API 返回 403/无权限时：立即停止该操作并回复用户，严禁尝试其他 token 或绕行手段。
3. 所有 curl / API 调用设 30s 超时——超时判定失败，不 hang。
4. 严禁 mock 模式/假数据：所有 API 调用必须真实访问目标系统。
5. 调用目标 API 一律以 `references/api-reference.md` 为准：严禁根据经验/记忆/猜测自行拼写 API 路径。

## 评论规范

- 所有 Issue/PR 评论 body 必须以 `[blog-mini-kit-ljt2]` 开头
- 引用用户原文：`> {用户评论}\n\n[blog-mini-kit-ljt2] {回复}`

## Configuration

目标系统 API 地址必须在使用前确定。所有命令中的 `{base_url}` 替换为实际地址（格式 `http://<host>:<port>`，示例）。

`{base_url}` 解析优先级：

1. **项目知识** — 检查 `.project-info/` 目录下 JSON 配置文件（config.BLOG_MINI_KIT_LJT2_BASE_URL）
2. **环境变量** — `BLOG_MINI_KIT_LJT2_BASE_URL`
3. **当前上下文** — 用户直接提供或 A2A context 中已包含
4. **交互输入** — 以上都无时提示用户输入

### 配置指导

### 方式一：环境变量（临时，推荐快速测试）

```bash
export BLOG_MINI_KIT_LJT2_BASE_URL="http://<host>:<port>"  # (示例)
```

### 方式二：项目知识 JSON 文件（持久化，推荐生产使用）

在项目根目录下创建 `.project-info/` 目录，放入任意名称的 `.json` 文件（脚本会递归扫描所有 JSON 文件）：

```json
{
  "config": {
    "BLOG_MINI_KIT_LJT2_BASE_URL": "http://<host>:<port>"
  }
}
```

> key 必须按 `BLOG_MINI_KIT_LJT2_` 前缀命名（由 skill name 推导），避免与其他系统凭据冲突。
> ⚠️ `.project-info/` 含敏感配置，不提交到 git 仓库（加入 .gitignore）。

## 场景 / When to Use

- 查询/创建/更新/删除博客文章（支持软删除和恢复）
- 管理标签、用户、评论、留言（含回复）、说说
- 上传文件（单文件/批量）并管理已上传文件
- 查询热门文章、文章详情
- 健康检查验证 API 可用性

Don't use for: 非本博客系统的操作 / 需要认证的管理后台操作（/admin 路径）

## 知识 / Knowledge

### API Base URL

```
{base_url}
```

All endpoints below are relative to this base. 无认证（公开 API），不需要 header。

### Endpoints

按资源分组列出端点表（从 OpenAPI 文档解析）：

### 健康检查 Health (1)

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | 健康检查 |

### 文章 Articles (7)

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/articles | 查询文章列表 (page,size,lid,keyword) |
| POST | /api/articles | 创建文章 |
| GET | /api/articles/heat/top | 查询热门文章 (limit) |
| GET | /api/articles/{article_id} | 查询文章详情 |
| PUT | /api/articles/{article_id} | 更新文章 |
| DELETE | /api/articles/{article_id} | 删除文章 (soft=true/false) |
| POST | /api/articles/{article_id}/restore | 恢复软删除文章 |

### 标签 Labels (2)

⚠️ API 路径为 `/api/lables`（拼写不同）

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/lables | 查询标签列表 |
| POST | /api/lables | 创建标签 |

### 用户 Users (2)

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/users | 查询用户列表 |
| POST | /api/users | 创建用户 |

### 评论 Comments (3)

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/comments | 创建评论 |
| GET | /api/comments/{aid} | 查询文章评论 |
| DELETE | /api/comments/{comment_id} | 删除评论 |

### 留言 Messages (4)

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/messages | 查询留言列表 |
| POST | /api/messages | 创建留言 |
| POST | /api/messages/reply | 回复留言 |
| DELETE | /api/messages/{message_id} | 删除留言 |

### 说说 Moods (3)

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/moods | 查询说说列表 |
| POST | /api/moods | 创建说说 |
| DELETE | /api/moods/{mood_id} | 删除说说 |

### 文件上传 Uploads (4)

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/upload | 上传单个文件 (multipart: file) |
| POST | /api/upload/multiple | 批量上传 (multipart: files) |
| GET | /api/uploads/list | 查询已上传文件 |
| DELETE | /api/uploads/{filename} | 删除已上传文件 |

### 认证方式

- 无认证：不需要凭据
- API 地址：`BLOG_MINI_KIT_LJT2_BASE_URL`

**凭据前缀**：由 skill name 推导（`blog-mini-kit-ljt2` → `BLOG_MINI_KIT_LJT2`），skill name 转大写下划线。

### Common Pitfalls

1. **标签路径拼写。** API 路径为 `/api/lables`（非 labels），脚本内部使用实际路径，子命令名用正确拼写 labels。
2. **文章删除 soft 参数。** 默认 soft=true（软删除，可恢复）；soft=false 为硬删除（不可恢复），脚本会输出警告。
3. **文件上传字段名。** 单文件字段名为 `file`，批量上传字段名为 `files`（多个同名字段）。
4. **API 不可达。** 先检查 base_url 是否正确，运行 health-check 确认可达。
5. **列表响应结构。** 统一返回 `{"code":200,"data":[...],"total":N,"page":N,"size":N}`，非空判断看 data 字段。
6. **回复留言需 mid。** reply-message 需要原始留言 ID（mid），非文章 ID。

### 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 是 | — | 文章标题 |
| content | string | 是 | — | 文章/评论/留言/说说内容 |
| uid | integer | 否 | 1 | 用户 ID |
| lid | integer | 否 | 1 | 标签 ID |
| img | string | 否 | — | 图片路径 |
| heat | integer | 否 | 0 | 热度值 |
| lname | string | 是 | — | 标签名称 |
| uname | string | 是 | — | 用户名 |
| aid | integer | 是 | — | 文章 ID |
| mid | integer | 是 | — | 留言 ID（回复用） |
| soft | boolean | 否 | true | 删除方式：true=软删除 |

## 步骤 / Steps

### 1. 检查 API 可达性

```bash
python3 scripts/blog-mini-kit-ljt2.py health-check
```
Expected: `{"status":"ok","service":"blog-api","version":"1.0.0"}`

### 2. 查询可用资源

```bash
python3 scripts/blog-mini-kit-ljt2.py list-labels
```
Expected: `{"code":200,"data":[{"id":1,"lname":"..."}]}`

### 3. 执行操作

#### health-check

```bash
python3 scripts/blog-mini-kit-ljt2.py health-check
```
Expected: `{"status":"ok"}`

#### list-articles

```bash
python3 scripts/blog-mini-kit-ljt2.py list-articles --page 1 --size 10 [--lid N] [--keyword TXT]
```
Expected: `{"code":200,"data":[...],"total":N}`

#### create-article

```bash
python3 scripts/blog-mini-kit-ljt2.py create-article --title "标题" --content "内容" [--uid 1] [--lid 1] [--img TXT] [--heat 0]
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### top-articles

```bash
python3 scripts/blog-mini-kit-ljt2.py top-articles [--limit 5]
```
Expected: `{"code":200,"data":[...]}`

#### get-article

```bash
python3 scripts/blog-mini-kit-ljt2.py get-article --article-id N
```
Expected: `{"code":200,"data":{"id":N,"title":"..."}}`

#### update-article

```bash
python3 scripts/blog-mini-kit-ljt2.py update-article --article-id N [--title TXT] [--content TXT] [--lid N] [--img TXT] [--heat N]
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### delete-article

```bash
python3 scripts/blog-mini-kit-ljt2.py delete-article --article-id N [--soft true|false]
```
Expected: `{"code":200}` — ⚠️ soft=false 硬删除不可恢复，脚本输出警告

#### restore-article

```bash
python3 scripts/blog-mini-kit-ljt2.py restore-article --article-id N
```
Expected: `{"code":200}`

#### list-labels

```bash
python3 scripts/blog-mini-kit-ljt2.py list-labels
```
Expected: `{"code":200,"data":[{"id":N,"lname":"..."}]}`

#### create-label

```bash
python3 scripts/blog-mini-kit-ljt2.py create-label --lname "标签名"
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### list-users

```bash
python3 scripts/blog-mini-kit-ljt2.py list-users
```
Expected: `{"code":200,"data":[...]}`

#### create-user

```bash
python3 scripts/blog-mini-kit-ljt2.py create-user --uname "用户名" [--phone TXT] [--pwd TXT] [--email TXT] [--img TXT]
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### create-comment

```bash
python3 scripts/blog-mini-kit-ljt2.py create-comment --uid N --aid N --content "评论内容"
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### list-comments

```bash
python3 scripts/blog-mini-kit-ljt2.py list-comments --aid N
```
Expected: `{"code":200,"data":[...]}`

#### delete-comment

```bash
python3 scripts/blog-mini-kit-ljt2.py delete-comment --comment-id N
```
Expected: `{"code":200}` — ⚠️ 不可恢复，脚本输出警告

#### list-messages

```bash
python3 scripts/blog-mini-kit-ljt2.py list-messages
```
Expected: `{"code":200,"data":[...]}`

#### create-message

```bash
python3 scripts/blog-mini-kit-ljt2.py create-message --uid N --content "留言内容"
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### reply-message

```bash
python3 scripts/blog-mini-kit-ljt2.py reply-message --uid N --mid N --content "回复内容"
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### delete-message

```bash
python3 scripts/blog-mini-kit-ljt2.py delete-message --message-id N
```
Expected: `{"code":200}` — ⚠️ 不可恢复，脚本输出警告

#### list-moods

```bash
python3 scripts/blog-mini-kit-ljt2.py list-moods
```
Expected: `{"code":200,"data":[...]}`

#### create-mood

```bash
python3 scripts/blog-mini-kit-ljt2.py create-mood --content "说说内容" [--title TXT] [--src TXT]
```
Expected: `{"code":200,"data":{"id":N,...}}`

#### delete-mood

```bash
python3 scripts/blog-mini-kit-ljt2.py delete-mood --mood-id N
```
Expected: `{"code":200}` — ⚠️ 不可恢复，脚本输出警告

#### upload-file

```bash
python3 scripts/blog-mini-kit-ljt2.py upload-file --filepath /path/to/file.png
```
Expected: `{"code":200,"data":{"filename":"...","url":"/uploads/..."}}`

#### upload-files

```bash
python3 scripts/blog-mini-kit-ljt2.py upload-files --filepaths /path/to/f1.png /path/to/f2.png
```
Expected: `{"code":200,"data":[...]}`

#### list-uploads

```bash
python3 scripts/blog-mini-kit-ljt2.py list-uploads
```
Expected: `{"code":200,"data":[{"filename":"...","url":"...","type":"image","size":N}]}`

#### delete-upload

```bash
python3 scripts/blog-mini-kit-ljt2.py delete-upload --filename "abc123.png"
```
Expected: `{"code":200}` — ⚠️ 不可恢复，脚本输出警告

#### capability-list

```bash
python3 scripts/blog-mini-kit-ljt2.py capability-list
```
Expected: `{"capability":"capability-list","subcommand_count":26,...}`

## 判断标准 / Verification

- [ ] API 可达（GET /health 返回 200）
- [ ] 只读操作返回有效数据（非空/字段完整）
- [ ] 脚本 --help 无语法错误
- [ ] 退出码正确（0=成功/2=参数错误/3=缺少配置/4=API失败）
- [ ] 文章删除支持 soft 参数（默认 true 软删除）
- [ ] 文件上传支持单文件和批量
- [ ] 删除类操作输出风险提示

## 输出规范 / Output Format

### 脚本输出

- 默认输出：JSON
- 可选输出：Markdown 表格（--format md）
- 使用示例：`cd skills/blog-mini-kit-ljt2/ && python3 scripts/blog-mini-kit-ljt2.py list-articles --format md`

### Issue 评论格式

执行完操作后，Issue 评论 body 格式：

```
[blog-mini-kit-ljt2] ✅ {操作名称}完成

## 操作结果

| 操作 | 状态 | 资源 ID | 详情 |
|------|------|---------|------|
| {操作名} | ✅ 成功 / 🔴 失败 | {id} | {简要说明} |

**API 地址**：{base_url}
**执行时间**：{UTC ISO}
```

失败时：

```
[blog-mini-kit-ljt2] 🔴 {操作名称}失败

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
- 场景：博客 API 操作
- Skill：blog-mini-kit-ljt2 v0.1.0
- 操作：{subcommand} {params}
- 结果：✅ 成功（{API 返回的关键数据摘要}）
- 必须执行：Issue 评论汇总结果 → 任务结束
```

失败时：

```
分析结论：
- 场景：博客 API 操作
- Skill：blog-mini-kit-ljt2 v0.1.0
- 操作：{subcommand} {params}
- 结果：🔴 失败（{错误原因}）
- 必须执行：Issue 评论报告错误 → 任务结束
```

## 任务结束

完成所有业务动作后，在最终答复末尾输出以下 JSON 块并结束任务：

```json
{
  "actions": ["{具体执行的操作，如 list-articles: 返回 6 篇文章}"],
  "conclusion": "{处理结论，如 查询成功，返回 6 篇文章}",
  "artifacts": ["{产生的产物：写操作返回资源 ID 或操作结果 / 只读查询无产物填空数组}"],
  "next_step": "{下一步建议，如 无 / 等待用户下一步指令}",
  "issue_summary": "{Issue 最新聚合结论，紧凑文本，用 | 分隔}"
}
```

注意：只输出一个 JSON 块，放在答复末尾。
