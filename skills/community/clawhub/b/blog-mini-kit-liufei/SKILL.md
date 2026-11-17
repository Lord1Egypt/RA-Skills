---
name: blog-mini-kit-liufei
version: 0.1.0
description: |
  管理博客系统(FastAPI)全部 32 个 API 端点：文章 CRUD/恢复/热门、标签管理、用户管理、
  评论/留言/说说管理、文件上传、后台管理、前端页面、健康检查。无认证，curl+JSON 示例。
triggers:
  - 博客管理
  - 文章发布
  - blog api
  - 博客系统
tags:
  - blog
  - fastapi
  - rest-api
  - content-management
tools:
  - curl
---

# blog-mini-kit-liufei

## 安全硬约束（必须遵守）

**通用约束（所有 skill 必含）**：

1. 严禁读取 data/、configs/、sessions.db、user_accounts 等 Grape 内部数据。
2. API 返回 403/无权限时：立即停止该操作并回复用户，严禁尝试其他 token 或绕行手段。
3. 所有 curl / API 调用设 30s 超时——超时判定失败，不 hang。
4. 严禁 mock 模式/假数据：所有 API 调用必须真实访问目标系统。
5. 调用目标 API 一律以 `references/api-reference.md` 为准：严禁根据经验/记忆/猜测自行拼写 API 路径。

## 评论规范

- 所有 Issue/PR 评论 body 必须以 `[blog-mini-kit-liufei]` 开头
- 引用用户原文：`> {用户评论}\n\n[blog-mini-kit-liufei] {回复}`

## Configuration

目标系统 API 地址必须在使用前确定。所有命令中的 `{base_url}` 替换为实际地址（格式 `http://<host>:<port>`）。

`{base_url}` 解析优先级：

1. **项目知识** — 检查 `.project-info/` 目录下 JSON 配置文件（config.BLOG_MINI_KIT_LIUFEI_BASE_URL）
2. **环境变量** — `BLOG_MINI_KIT_LIUFEI_BASE_URL`
3. **当前上下文** — 用户直接提供或 A2A context 中已包含
4. **交互输入** — 以上都无时提示用户输入

### 配置指导

#### 方式一：环境变量（临时，推荐快速测试）

```bash
export BLOG_MINI_KIT_LIUFEI_BASE_URL="http://<host>:<port>"
```

#### 方式二：项目知识 JSON 文件（持久化，推荐生产使用）

在项目根目录下创建 `.project-info/` 目录，放入任意名称的 `.json` 文件：

```json
{
  "config": {
    "BLOG_MINI_KIT_LIUFEI_BASE_URL": "http://<host>:<port>"
  }
}
```

> ⚠️ `.project-info/` 含敏感配置，不提交到 git 仓库（加入 .gitignore）。

## 场景 / When to Use

- 用户要求查询/发布/编辑/删除博客文章
- 用户要求管理标签、用户、评论、留言、说说
- 用户要求上传文件到博客系统
- 用户要求查看博客健康状态或热门文章
- 用户要求批量删除文章（后台管理）
- 用户要求通过 curl 调用博客 API

Don't use for: 非本博客系统的操作 / 数据库直接操作 / 博客源码修改

## 知识 / Knowledge

### API Base URL

```
{base_url}
```

All endpoints below are relative to this base. 无认证（公开 API），不需要 header。

### Endpoints（32 个，按 10 类分组）

#### 文章 API（7）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 1 | GET | /api/articles | list-articles | 分页查询文章列表（page/size/lid/keyword） |
| 2 | GET | /api/articles/{id} | get-article | 查询单篇文章详情（含评论） |
| 3 | POST | /api/articles | create-article | 发布新文章（ArticleCreate） |
| 4 | PUT | /api/articles/{id} | update-article | 更新文章（ArticleUpdate） |
| 5 | DELETE | /api/articles/{id} | delete-article | 删除文章（soft=true/false） |
| 6 | POST | /api/articles/{id}/restore | restore-article | 恢复软删除的文章 |
| 7 | GET | /api/articles/heat/top | top-articles | 获取热门文章 Top N（limit） |

#### 标签 API（2）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 8 | GET | /api/lables | list-lables | 获取所有标签 |
| 9 | POST | /api/lables | create-lable | 创建标签（LableCreate） |

#### 用户 API（2）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 10 | GET | /api/users | list-users | 获取用户列表 |
| 11 | POST | /api/users | create-user | 创建用户（UserCreate） |

#### 评论 API（3）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 12 | POST | /api/comments | create-comment | 发表评论（CommentCreate） |
| 13 | GET | /api/comments/{aid} | list-comments | 获取文章评论列表 |
| 14 | DELETE | /api/comments/{id} | delete-comment | 删除评论（软删除） |

#### 留言 API（4）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 15 | GET | /api/messages | list-messages | 获取留言列表（含回复） |
| 16 | POST | /api/messages | create-message | 发表留言（MessageCreate） |
| 17 | POST | /api/messages/reply | reply-message | 回复留言（Message2Create） |
| 18 | DELETE | /api/messages/{id} | delete-message | 删除留言（软删除） |

#### 说说 API（3）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 19 | GET | /api/moods | list-moods | 获取说说列表 |
| 20 | POST | /api/moods | create-mood | 发布说说（MoodCreate） |
| 21 | DELETE | /api/moods/{id} | delete-mood | 删除说说 |

#### 文件上传 API（4）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 22 | POST | /api/upload | upload-file | 上传单个文件（multipart -F） |
| 23 | POST | /api/upload/multiple | upload-files | 批量上传文件（multipart -F） |
| 24 | GET | /api/uploads/list | list-uploads | 列出所有已上传文件 |
| 25 | DELETE | /api/uploads/{filename} | delete-upload | 删除已上传文件 |

#### 前端页面（2，返回 HTML，无子命令）

| # | Method | Path | 说明 |
|---|--------|------|------|
| 26 | GET | / | 博客首页（page/lid/keyword） |
| 27 | GET | /article/{id} | 文章详情页 |

#### 后台管理（4）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 28 | GET | /admin | —（HTML） | 后台管理入口 |
| 29 | POST | /admin/login | admin-login | 后台登录获取 token（form-data） |
| 30 | GET | /admin/logout | —（重定向） | 退出登录 |
| 31 | POST | /admin/api/delete | admin-delete-articles | 批量删除文章（JSON） |

#### 健康检查（1）

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 32 | GET | /health | health-check | 健康检查 |

> **端点计数：7+2+2+3+4+3+4+2+4+1 = 32**

### 认证方式

- **无认证**（公开 API）：所有 `/api/*` 端点无需 header/token
- 后台管理（/admin/*）：需 admin token（通过 admin-login 获取，默认凭据 admin/admin）
- API 地址：`BLOG_MINI_KIT_LIUFEI_BASE_URL`
- 凭据前缀：由 skill name 推导（`blog-mini-kit-liufei` → `BLOG_MINI_KIT_LIUFEI`）

### 数据模型（8 个 Schema）

| Schema | 必填字段 | 可选字段（含默认值） |
|--------|---------|---------------------|
| ArticleCreate | title(str), content(str) | uid=1, lid=1, img=null, heat=0 |
| ArticleUpdate | （至少一个字段） | title, content, lid, img, heat（全可选） |
| LableCreate | lname(str) | — |
| UserCreate | uname(str) | phone="", pwd="", email="", img="img/moren.jpg" |
| CommentCreate | uid(int), aid(int), content(str) | — |
| MessageCreate | uid(int), content(str) | — |
| Message2Create | uid(int), mid(int), content(str) | — |
| MoodCreate | content(str) | title="", src="" |

> 完整字段说明见 `references/api-reference.md`

### Common Pitfalls

1. **API 不可达。** 先 `curl {base_url}/health` 确认可达，检查 base_url 是否正确。
2. **标签路径拼写为 lables（非 labels）。** API 实际路径是 `/api/lables`，子命令用正确拼写 `create-lable` 但内部请求用 `/api/lables`。
3. **DELETE /api/articles/{id} 默认软删除。** 需要硬删除时传 `soft=false`（子命令用 `--hard` 标志）。
4. **文件上传必须用 multipart/form-data。** curl 用 `-F "file=@path"`，不能用 `-d` JSON。
5. **后台管理需 token。** 先调 `admin-login` 获取 token，再传给 `admin-delete-articles --token`。
6. **GET /api/articles/heat/top 路径冲突。** FastAPI 路由匹配 `/api/articles/heat/top` 优先于 `/api/articles/{id}`，无需担心 ID 被解析为 "heat"。
7. **upload-file 响应 filename 与 delete-upload 参数不一致。** upload-file 响应中 `filename` 为原始文件名，但 delete-upload 需要的是 UUID 生成的文件名（如 `abc123def456.jpg`）。删除文件前应先用 list-uploads 获取实际文件名。

## 步骤 / Steps

### 1. 检查 API 可达性

```bash
python3 scripts/blog-mini-kit-liufei.py health-check
```

Expected: `{"status":"ok","service":"blog-api","version":"1.0.0"}`

### 2. 查询可用资源

#### 查询文章列表

```bash
python3 scripts/blog-mini-kit-liufei.py list-articles --page 1 --size 10
```

Expected: `{"code":200,"data":[...],"total":N,"page":1,"size":10}`

#### 查询标签

```bash
python3 scripts/blog-mini-kit-liufei.py list-lables
```

Expected: `{"code":200,"data":[{"id":1,"lname":"技术"},...]}`

#### 查询用户

```bash
python3 scripts/blog-mini-kit-liufei.py list-users
```

Expected: `{"code":200,"data":[{"id":1,"uname":"admin",...}]}`

### 3. 执行操作

#### 创建文章

```bash
python3 scripts/blog-mini-kit-liufei.py create-article --title "测试文章" --content "内容"
```

Expected: `{"code":200,"message":"文章发布成功","data":{"id":N}}`

#### 更新文章

```bash
python3 scripts/blog-mini-kit-liufei.py update-article --article-id 1 --title "新标题" --heat 10
```

Expected: `{"code":200,"message":"文章更新成功"}`

#### 删除文章（软删除）

```bash
python3 scripts/blog-mini-kit-liufei.py delete-article --article-id 1
```

Expected: `{"code":200,"message":"文章已删除"}`

#### 硬删除文章

```bash
python3 scripts/blog-mini-kit-liufei.py delete-article --article-id 1 --hard
```

Expected: `{"code":200,"message":"文章已删除"}`

#### 恢复文章

```bash
python3 scripts/blog-mini-kit-liufei.py restore-article --article-id 1
```

Expected: `{"code":200,"message":"文章已恢复"}`

#### 获取热门文章

```bash
python3 scripts/blog-mini-kit-liufei.py top-articles --limit 5
```

Expected: `{"code":200,"data":[{"id":N,"title":"...","heat":N},...]}`

#### 创建标签

```bash
python3 scripts/blog-mini-kit-liufei.py create-lable --lname "新标签"
```

Expected: `{"code":200,"data":{"id":N,"lname":"新标签"}}`

#### 发表评论

```bash
python3 scripts/blog-mini-kit-liufei.py create-comment --uid 1 --aid 1 --content "好文章"
```

Expected: `{"code":200,"data":{"id":N}}`

#### 发表留言

```bash
python3 scripts/blog-mini-kit-liufei.py create-message --uid 1 --content "你好"
```

Expected: `{"code":200,"data":{"id":N}}`

#### 回复留言

```bash
python3 scripts/blog-mini-kit-liufei.py reply-message --uid 1 --mid 1 --content "谢谢"
```

Expected: `{"code":200,"data":{"id":N}}`

#### 发布说说

```bash
python3 scripts/blog-mini-kit-liufei.py create-mood --content "今天很好" --title "心情"
```

Expected: `{"code":200,"data":{"id":N}}`

#### 上传文件（multipart -F）

```bash
python3 scripts/blog-mini-kit-liufei.py upload-file --filepath /path/to/image.jpg
```

Expected: `{"code":200,"data":{"url":"/uploads/xxx.jpg","filename":"image.jpg","type":"image","size":N}}`

#### 批量上传文件

```bash
python3 scripts/blog-mini-kit-liufei.py upload-files --filepaths /path/a.jpg /path/b.png
```

Expected: `{"code":200,"data":[{...},{...}]}`

#### 后台登录获取 token

```bash
python3 scripts/blog-mini-kit-liufei.py admin-login --username admin --password admin
```

Expected: `{"code":200,"data":{"token":"xxx"}}`

#### 后台批量删除文章

```bash
python3 scripts/blog-mini-kit-liufei.py admin-delete-articles --ids 1 2 --token "your_token"
```

Expected: `{"code":200,"deleted":2,"message":"成功删除 2 篇文章"}`

#### capability-list

```bash
python3 scripts/blog-mini-kit-liufei.py capability-list
```

Expected: `{"capability":"capability-list","skill":"blog-mini-kit-liufei","subcommand_count":28,...}`

参数说明：

- `--format`：输出格式 json/md，默认 json（所有子命令通用）

## 判断标准 / Verification

- [ ] API 可达（GET /health 返回 `{"status":"ok"}`）
- [ ] 只读操作返回有效数据（list-articles / list-lables / list-users 非空/字段完整）
- [ ] 脚本 `--help` 无语法错误
- [ ] 脚本 `capability-list` 返回 28 个子命令
- [ ] 退出码正确（0=成功/2=参数错误/3=缺少配置/4=API失败）
- [ ] 32 个端点全部覆盖（7+2+2+3+4+3+4+2+4+1=32）
- [ ] 8 个数据模型覆盖（ArticleCreate/ArticleUpdate/LableCreate/UserCreate/CommentCreate/MessageCreate/Message2Create/MoodCreate）

## 输出规范 / Output Format

### 脚本输出

- 默认输出：JSON
- 可选输出：Markdown 表格（`--format md`）
- 使用示例：`cd skills/blog-mini-kit-liufei/ && python3 scripts/blog-mini-kit-liufei.py list-articles --format md`

### Issue 评论格式

执行完操作后，Issue 评论 body 格式：

```
[blog-mini-kit-liufei] ✅ {操作名称}完成

## 操作结果

| 操作 | 状态 | 资源 ID | 详情 |
|------|------|---------|------|
| {操作名} | ✅ 成功 / 🔴 失败 | {id} | {简要说明} |

**API 地址**：{base_url}
**执行时间**：{UTC ISO}
```

失败时：

```
[blog-mini-kit-liufei] 🔴 {操作名称}失败

## 错误分析

- **操作**：{操作名}
- **错误**：{API 返回的错误信息}
- **HTTP 状态码**：{code}
- **原因**：{分析原因}

### 修复建议

{修复步骤}
```

## 参考文档 / References

- [API 端点文档](references/api-reference.md) — 32 个端点完整文档（参数/schema/curl 示例/响应示例）
- [测试用例](templates/test-vars.json) — 11 个测试用例

## 分析结论示例

成功时：

```
分析结论：
- 场景：博客 API 操作
- Skill：blog-mini-kit-liufei v0.1.0
- 操作：{subcommand} {params}
- 结果：✅ 成功（{API 返回的关键数据摘要}）
- 必须执行：Issue 评论汇总结果 → 任务结束
```

失败时：

```
分析结论：
- 场景：博客 API 操作
- Skill：blog-mini-kit-liufei v0.1.0
- 操作：{subcommand} {params}
- 结果：🔴 失败（{错误原因}）
- 必须执行：Issue 评论报告错误 → 任务结束
```

## 任务结束

完成所有业务动作后，在最终答复末尾输出以下 JSON 块并结束任务：

```json
{
  "actions": ["{具体执行的操作，如 list-articles: 返回 5 篇文章}"],
  "conclusion": "{处理结论，如 查询成功，返回 5 篇文章}",
  "artifacts": ["{产生的产物：写操作返回资源 ID 或操作结果 / 文件操作返回 URL / 只读查询无产物填空数组}"],
  "next_step": "{下一步建议，如 无 / 等待用户下一步指令}",
  "issue_summary": "{Issue 最新聚合结论，紧凑文本，用 | 分隔}"
}
```

注意：只输出一个 JSON 块，放在答复末尾。
