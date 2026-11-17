---
name: blog-kimi-test-kit
version: 0.1.0
description: 博客内容发布工具，管理博客系统全部 REST API（文章/标签/用户/评论/留言/说说/文件上传/健康检查）
triggers:
  - 博客
  - 文章
  - 标签
  - 评论
  - 留言
  - 说说
  - blog
  - article
  - content
tags:
  - blog
  - content-management
  - REST-API
  - publishing
tools:
  - curl
  - python3
---

# blog-kimi-test-kit

## 安全硬约束（必须遵守）

**通用约束（所有 skill 必含）**：

1. 严禁读取 data/、configs/、sessions.db、user_accounts 等 Grape 内部数据。
2. API 返回 403/无权限时：立即停止该操作并回复用户，严禁尝试其他 token 或绕行手段。
3. 所有 curl / API 调用设 30s 超时——超时判定失败，不 hang。
4. 严禁 mock 模式/假数据：所有 API 调用必须真实访问目标系统。
5. 调用目标 API 一律以 `references/api-reference.md` 为准：严禁根据经验/记忆/猜测自行拼写 API 路径。

## 评论规范

- 所有 Issue/PR 评论 body 必须以 `[blog-kimi-test-kit]` 开头
- 引用用户原文：`> {用户评论}\n\n[blog-kimi-test-kit] {回复}`

## Configuration

目标系统 API 地址必须在使用前确定。所有命令中的 `{base_url}` 替换为实际地址（格式 `http://<host>:<port>`）。

`{base_url}` 解析优先级：

1. **项目知识** — 检查 `.project-info/` 目录下 JSON 配置文件（config.BLOG_KIMI_TEST_KIT_BASE_URL）
2. **环境变量** — `BLOG_KIMI_TEST_KIT_BASE_URL`
3. **当前上下文** — 用户直接提供或 A2A context 中已包含
4. **交互输入** — 以上都无时提示用户输入

### 配置指导

**方式一：环境变量（临时，推荐快速测试）**

```bash
export BLOG_KIMI_TEST_KIT_BASE_URL="{base_url}"
```

**方式二：项目知识 JSON 文件（持久化，推荐生产使用）**

在项目根目录下创建 `.project-info/` 目录，放入任意名称的 `.json` 文件：

```json
{
  "config": {
    "BLOG_KIMI_TEST_KIT_BASE_URL": "http://<host>:<port>"
  }
}
```

> key 必须按 `BLOG_KIMI_TEST_KIT_` 前缀命名，避免与其他系统凭据冲突。
> ⚠️ `.project-info/` 含敏感凭据，不提交到 git 仓库（加入 .gitignore）。

## 场景 / When to Use

- 用户需要管理博客系统的文章内容（CRUD 操作）
- 用户需要管理博客标签、用户、评论、留言、说说
- 用户需要上传/管理文件，查询博客系统健康状态
- 用户需要批量管理文章（后台管理功能）

Don't use for: 非博客系统的 REST API 操作，或博客系统前端页面访问。

## 知识 / Knowledge

### API Base URL

```
{base_url}
```

本系统为公开 API，无认证。API base_url 通过环境变量 `BLOG_KIMI_TEST_KIT_BASE_URL` 配置。

### Endpoints

按资源分组：

#### Health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | 健康检查 |

#### Articles
| Method | Path | Parameters | Body | Description |
|--------|------|------------|------|-------------|
| GET | /api/articles | page, size, lid, keyword | — | 分页查询文章列表 |
| POST | /api/articles | — | ArticleCreate | 发布新文章 |
| GET | /api/articles/{article_id} | article_id(path) | — | 查询文章详情 |
| PUT | /api/articles/{article_id} | article_id(path) | ArticleUpdate | 更新文章 |
| DELETE | /api/articles/{article_id} | article_id(path), soft | — | 删除文章（支持软删除） |
| POST | /api/articles/{article_id}/restore | article_id(path) | — | 恢复已软删除的文章 |
| GET | /api/articles/heat/top | limit | — | 获取热门文章排行 |

#### Labels（注意：API 路径实际为 /api/lables）
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/lables | — | 查询标签列表 |
| POST | /api/lables | LableCreate | 创建新标签 |

#### Users
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/users | — | 查询用户列表 |
| POST | /api/users | UserCreate | 创建新用户 |

#### Comments
| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /api/comments | CommentCreate | 创建评论 |
| GET | /api/comments/{aid} | — | 查询文章评论列表 |
| DELETE | /api/comments/{comment_id} | — | 删除评论 |

#### Messages
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/messages | — | 查询留言列表 |
| POST | /api/messages | MessageCreate | 创建留言 |
| POST | /api/messages/reply | Message2Create | 回复留言 |
| DELETE | /api/messages/{message_id} | — | 删除留言 |

#### Moods
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/moods | — | 查询说说列表 |
| POST | /api/moods | MoodCreate | 创建说说 |
| DELETE | /api/moods/{mood_id} | — | 删除说说 |

#### File Upload
| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /api/upload | multipart/form-data (file) | 单文件上传 |
| POST | /api/upload/multiple | multipart/form-data (files) | 批量文件上传 |
| GET | /api/uploads/list | — | 查询上传文件列表 |
| DELETE | /api/uploads/{filename} | — | 删除上传文件 |

#### Admin
| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /admin/api/delete | — | 批量删除文章 |

### 认证方式

- 无认证（公开 API）
- API 地址：`BLOG_KIMI_TEST_KIT_BASE_URL`

**凭据前缀**：由 skill name 推导（`blog-kimi-test-kit` → `BLOG_KIMI_TEST_KIT`）。

**凭据读取优先级（4 级，与 base_url 一致）**：

1. **项目知识** — 递归扫描 `.project-info/` 下所有 JSON 文件，读取 `secrets.BLOG_KIMI_TEST_KIT_*` 字段
2. **环境变量** — 项目知识缺失时扫描 `BLOG_KIMI_TEST_KIT_*` 开头变量
3. **当前上下文** — A2A context 已注入的环境变量（已包含在步骤 2）
4. **交互输入** — 以上都无时提示用户输入

### Common Pitfalls

1. **API 不可达。** 先检查 base_url 是否正确，`curl {base_url}/health` 确认可达。
2. **标签路径拼写。** API 实际路径为 `/api/lables`（拼写错误），子命令名用正确拼写 `list-labels` / `create-label`。
3. **软删除恢复。** `--soft true` 为软删除，可用 `restore-article` 恢复；不传 `--soft` 则物理删除不可恢复。
4. **文件上传参数。** 上传用 `--filepath`，批量用 `--filepaths` 接多个路径。
5. **关联 ID。** 创建评论需 `--uid` + `--aid`；回复留言需 `--uid` + `--mid`。

### 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | ✅ | — | 文章标题 |
| content | string | ✅ | — | 文章/评论/留言/说说内容 |
| uid | integer | | — | 用户 ID |
| lid | integer | | 0 | 标签 ID（筛选用） |
| lname | string | ✅ | — | 标签名称 |
| uname | string | ✅ | — | 用户名 |
| page | integer | | 1 | 分页页码 |
| size | integer | | 10 | 每页数量（≤100） |
| keyword | string | | "" | 关键词搜索 |
| soft | boolean | | false | 是否软删除 |
| limit | integer | | — | 热门文章返回数量 |

## 步骤 / Steps

### 1. 检查 API 可达性

```bash
export BLOG_KIMI_TEST_KIT_BASE_URL="{base_url}"
python3 scripts/blog-kimi-test-kit.py health-check
```

Expected: `{"status":"ok","service":"blog-api","version":"1.0.0"}`

### 2. 查询可用资源

```bash
python3 scripts/blog-kimi-test-kit.py list-articles --page 1 --size 10
python3 scripts/blog-kimi-test-kit.py list-labels
python3 scripts/blog-kimi-test-kit.py list-users
python3 scripts/blog-kimi-test-kit.py list-moods
python3 scripts/blog-kimi-test-kit.py list-messages
```

Expected: 返回各资源的列表数据（JSON 格式）

### 3. 执行操作

#### health-check
```bash
python3 scripts/blog-kimi-test-kit.py health-check
```
Expected: `{"status":"ok","service":"blog-api","version":"1.0.0"}`

#### list-articles
```bash
python3 scripts/blog-kimi-test-kit.py list-articles --page 1 --size 10
```
Expected: 返回文章列表（分页数据）
参数：`--page` `--size` `--lid` `--keyword` `--format`

#### create-article
```bash
python3 scripts/blog-kimi-test-kit.py create-article --title "标题" --content "内容"
```
Expected: 创建成功，返回文章 ID 的 JSON
参数：`--title`(必填) `--content`(必填) `--uid` `--lid` `--img` `--heat` `--format`

#### get-article
```bash
python3 scripts/blog-kimi-test-kit.py get-article --article-id 1
```
Expected: 返回文章详情 JSON

参数说明：
- `--article-id`（必填）：文章 ID

#### update-article
```bash
python3 scripts/blog-kimi-test-kit.py update-article --article-id 1 --title "新标题" --content "新内容"
```
Expected: 更新成功，返回更新后的文章 JSON

#### delete-article
```bash
python3 scripts/blog-kimi-test-kit.py delete-article --article-id 1 --soft true
```
Expected: 删除成功，返回确认信息

#### restore-article
```bash
python3 scripts/blog-kimi-test-kit.py restore-article --article-id 1
```
Expected: 恢复成功，返回确认信息

#### top-articles
```bash
python3 scripts/blog-kimi-test-kit.py top-articles --limit 5
```
Expected: 返回热门文章排行列表

#### list-labels
```bash
python3 scripts/blog-kimi-test-kit.py list-labels
```
Expected: 返回标签列表 JSON

#### create-label
```bash
python3 scripts/blog-kimi-test-kit.py create-label --lname "新标签"
```
Expected: 创建成功，返回新标签 JSON

#### list-users
```bash
python3 scripts/blog-kimi-test-kit.py list-users
```
Expected: 返回用户列表 JSON

#### create-user
```bash
python3 scripts/blog-kimi-test-kit.py create-user --uname "用户名"
```
Expected: 创建成功，返回新用户 JSON

#### create-comment
```bash
python3 scripts/blog-kimi-test-kit.py create-comment --uid 1 --aid 1 --content "评论内容"
```
Expected: 创建成功，返回新评论 JSON

#### list-comments
```bash
python3 scripts/blog-kimi-test-kit.py list-comments --aid 1
```
Expected: 返回指定文章的评论列表

#### delete-comment
```bash
python3 scripts/blog-kimi-test-kit.py delete-comment --comment-id 1
```
Expected: 删除成功

#### list-messages
```bash
python3 scripts/blog-kimi-test-kit.py list-messages
```
Expected: 返回留言列表

#### create-message
```bash
python3 scripts/blog-kimi-test-kit.py create-message --uid 1 --content "留言内容"
```
Expected: 创建成功

#### reply-message
```bash
python3 scripts/blog-kimi-test-kit.py reply-message --uid 1 --mid 1 --content "回复内容"
```
Expected: 回复成功

#### delete-message
```bash
python3 scripts/blog-kimi-test-kit.py delete-message --message-id 1
```
Expected: 删除成功

#### list-moods
```bash
python3 scripts/blog-kimi-test-kit.py list-moods
```
Expected: 返回说说列表

#### create-mood
```bash
python3 scripts/blog-kimi-test-kit.py create-mood --content "说说内容"
```
Expected: 创建成功

#### delete-mood
```bash
python3 scripts/blog-kimi-test-kit.py delete-mood --mood-id 1
```
Expected: 删除成功

#### upload-file
```bash
python3 scripts/blog-kimi-test-kit.py upload-file --filepath /path/to/file.jpg
```
Expected: 上传成功，返回文件信息

#### upload-files
```bash
python3 scripts/blog-kimi-test-kit.py upload-files --filepaths /path/a.jpg /path/b.jpg
```
Expected: 批量上传成功，返回文件信息列表

#### list-uploads
```bash
python3 scripts/blog-kimi-test-kit.py list-uploads
```
Expected: 返回已上传文件列表

#### delete-upload
```bash
python3 scripts/blog-kimi-test-kit.py delete-upload --filename example.jpg
```
Expected: 删除成功

#### admin-delete-articles
```bash
python3 scripts/blog-kimi-test-kit.py admin-delete-articles
```
Expected: 批量删除成功

#### capability-list
```bash
python3 scripts/blog-kimi-test-kit.py capability-list
```
Expected: 列出所有能力项（28 项）

```bash
python3 scripts/blog-kimi-test-kit.py capability-list --format md
```
Expected: Markdown 表格格式的能力清单

## 判断标准 / Verification

- [ ] API 可达（`health-check` 返回 200）
- [ ] 只读操作返回有效数据（非空/字段完整）
- [ ] 脚本 `--help` 无语法错误
- [ ] 退出码正确（0=成功/2=参数错误/3=缺少配置/4=API失败）
- [ ] `capability-list` 返回所有 28 项能力
- [ ] `create-article` + `delete-article` 写入和清理功能正常

## 输出规范 / Output Format

### 脚本输出

- 默认输出：JSON
- 可选输出：Markdown 表格（`--format md`）
- 使用示例：`cd skills/blog-kimi-test-kit/ && python3 scripts/blog-kimi-test-kit.py list-articles --page 1 --size 10`

### Issue 评论格式

执行完操作后，Issue 评论 body 格式：

```
[blog-kimi-test-kit] ✅ {操作名称}完成

## 操作结果

| 操作 | 状态 | 资源 ID | 详情 |
|------|------|---------|------|
| {操作名} | ✅ 成功 / 🔴 失败 | {id} | {简要说明} |

**API 地址**：{base_url}
**执行时间**：{UTC ISO}
```

失败时：

```
[blog-kimi-test-kit] 🔴 {操作名称}失败

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
- 场景：{API 操作}
- Skill：blog-kimi-test-kit v0.1.0
- 操作：{subcommand} {params}
- 结果：✅ 成功（{API 返回的关键数据摘要}）
- 必须执行：Issue 评论汇总结果 → 任务结束
```

失败时：

```
分析结论：
- 场景：{API 操作}
- Skill：blog-kimi-test-kit v0.1.0
- 操作：{subcommand} {params}
- 结果：🔴 失败（{错误原因}）
- 必须执行：Issue 评论报告错误 → 任务结束
```

## 任务结束

完成所有业务动作后，在最终答复末尾输出以下 JSON 块并结束任务：

```json
{
  "actions": ["{具体执行的操作，如 list-articles: 返回 N 篇文章}"],
  "conclusion": "{处理结论}",
  "artifacts": ["{产生的产物}"],
  "next_step": "{下一步建议}",
  "issue_summary": "{Issue 最新聚合结论，紧凑文本，用 | 分隔}"
}
```