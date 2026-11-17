---
name: blog-mini-kit-mys
version: 1.0.0
description: |
  管理 Blog System (FastAPI) 全部 32 个 API 端点：文章/标签/用户/评论/留言/说说/
  文件上传/健康检查/博客页面/后台管理。无认证公开 API，支持 CLI 子命令调用。
triggers:
  - 博客管理
  - blog api
  - 文章发布
  - 博客系统
tags:
  - blog
  - fastapi
  - rest-api
  - content-management
tools:
  - curl
  - python3
---

# blog-mini-kit-mys

管理 Blog System (FastAPI) 全部 32 个 API 端点。

## 安全硬约束（必须遵守）

1. 严禁读取 data/、configs/、sessions.db、user_accounts 等 Grape 内部数据。
2. API 返回 403/无权限时：立即停止该操作并回复用户，严禁尝试其他 token 或绕行手段。
3. 所有 curl / API 调用设 30s 超时——超时判定失败，不 hang。
4. 严禁 mock 模式/假数据：所有 API 调用必须真实访问目标系统。
5. 调用目标 API 一律以 `references/api-reference.md` 为准：严禁根据经验/记忆/猜测自行拼写 API 路径。

## 评论规范

- 所有 Issue/PR 评论 body 必须以 `[blog-mini-kit-mys]` 开头（环境变量未注入时用 skill name）
- 引用用户原文：`> {用户评论}\n\n[blog-mini-kit-mys] {回复}`

## Configuration

目标系统 API 地址必须在使用前确定。所有命令中的 `{base_url}` 替换为实际地址（格式 `http://<host>:<port>`，实际地址见 `.project-info/` 配置或环境变量）。

`{base_url}` 解析优先级：

1. **项目知识** — 检查 `.project-info/` 目录下 JSON 配置文件（`config.BLOG_MINI_KIT_MYS_BASE_URL`）
2. **环境变量** — `BLOG_MINI_KIT_MYS_BASE_URL`
3. **当前上下文** — 用户直接提供或 A2A context 中已包含
4. **交互输入** — 以上都无时提示用户输入

### 配置指导

**方式一：环境变量（临时，推荐快速测试）**

```bash
export BLOG_MINI_KIT_MYS_BASE_URL="http://<host:port>"
```

**方式二：项目知识 JSON 文件（持久化，推荐生产使用）**

在项目根目录下创建 `.project-info/` 目录，放入任意名称的 `.json` 文件（脚本递归扫描）：

```json
{
  "config": {
    "BLOG_MINI_KIT_MYS_BASE_URL": "http://<host:port>"
  }
}
```

> key 必须按 `BLOG_MINI_KIT_MYS_` 前缀命名（由 skill name 推导），避免与其他系统凭据冲突。
> ⚠️ `.project-info/` 含敏感配置，不提交到 git 仓库（加入 .gitignore）。

## 场景 / When to Use

- 用户要求查询/发布/编辑/删除博客文章
- 用户要求管理标签、用户、评论、留言、说说
- 用户要求上传/删除文件（图片/视频/文档）
- 用户要求查看博客健康状态、前端页面
- 用户要求后台批量管理文章（需 admin 登录）

Don't use for: 非本 Blog System 的操作 / 数据库直连操作 / 服务器运维

## 知识 / Knowledge

### API Base URL

```
{base_url}
```

All endpoints below are relative to this base. 无认证（none）不需要 header。后台管理端点需 admin token。

### Endpoints（32 个，10 类）

详细文档见 `references/` 下分类文件。端点总览：

| 类别 | 端点数 | 子命令 |
|------|--------|--------|
| 文章 | 7 | list-articles, create-article, get-article, update-article, delete-article, restore-article, top-articles |
| 标签 | 2 | list-labels, create-label |
| 用户 | 2 | list-users, create-user |
| 评论 | 3 | create-comment, list-comments, delete-comment |
| 留言 | 4 | list-messages, create-message, reply-message, delete-message |
| 说说 | 3 | list-moods, create-mood, delete-mood |
| 文件上传 | 4 | upload-file, upload-files, list-uploads, delete-upload |
| 健康检查 | 1 | health-check |
| 博客页面 | 2 | blog-home, blog-article |
| 后台管理 | 4 | admin-page, admin-login, admin-logout, admin-delete-articles |

> ⚠️ 标签 API 实际路径为 `/api/lables`（原系统拼写），子命令用正确拼写 `labels`，脚本内部请求用 `lables`。

### 认证方式

- 公开 API（端点 1-26）：无认证，直接调用
- 后台管理（端点 29-32）：需 `admin-login` 获取 token（默认 admin/admin，以实际部署为准）
- API 地址：`BLOG_MINI_KIT_MYS_BASE_URL`

**凭据前缀**：由 skill name 推导（`blog-mini-kit-mys` → `BLOG_MINI_KIT_MYS`），skill name 转大写下划线。

### Common Pitfalls

1. **API 不可达。** 先 `health-check` 确认可达，检查 base_url 是否正确。
2. **标签路径拼写。** API 路径是 `/api/lables`（非 labels），脚本已处理映射，直接调 curl 时注意用 `lables`。
3. **删除操作不可逆性差异。** 文章删除默认软删除（可 restore）；评论/留言软删除不可恢复；说说硬删除不可恢复；后台批量删除硬删除不可恢复。
4. **文件上传必须用 multipart。** `upload-file` 字段名 `file`，`upload-files` 字段名 `files`（多值），不能用 JSON body。
5. **后台 token 获取方式。** token 通过 `admin-login` 表单提交后从 Set-Cookie 提取，非 JSON 返回；token 放入 `admin-delete-articles` 的 JSON body（非 header）。
6. **get-article 会增加热度。** 每次调用 `get-article` / `blog-article` 文章 heat +1，测试时注意。

### 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title (article) | string | 是 | - | 文章标题 |
| content (article) | string | 是 | - | 文章内容（支持 HTML） |
| uid | int | 否 | 1 | 用户 ID |
| lid | int | 否 | 1 | 标签 ID |
| lname | string | 是 | - | 标签名称 |
| uname | string | 是 | - | 用户名 |
| aid | int | 是 | - | 文章 ID（评论/留言关联） |
| mid | int | 是 | - | 留言 ID（回复关联） |
| soft (delete) | bool | 否 | true | true=软删除 false=硬删除 |
| limit (top) | int | 否 | 5 | 热门返回数量（1-20） |

## 步骤 / Steps

主流程：检查可达性 → 查询资源 → 执行操作。

### 1. 检查 API 可达性

```bash
python3 scripts/blog-mini-kit-mys.py health-check
```
Expected: `{"status":"ok","service":"blog-api","version":"1.0.0"}`

### 2. 查询可用资源

```bash
python3 scripts/blog-mini-kit-mys.py list-articles --page 1 --size 10
python3 scripts/blog-mini-kit-mys.py list-labels
python3 scripts/blog-mini-kit-mys.py list-users
```
Expected: `{"code":200,"data":[...]}`

### 3. 执行操作（按类别选择）

#### 文章管理
```bash
# 创建
python3 scripts/blog-mini-kit-mys.py create-article --title "标题" --content "内容"
# 详情
python3 scripts/blog-mini-kit-mys.py get-article --article-id 1
# 更新
python3 scripts/blog-mini-kit-mys.py update-article --article-id 1 --title "新标题"
# 删除（软删除）
python3 scripts/blog-mini-kit-mys.py delete-article --article-id 1
# 恢复
python3 scripts/blog-mini-kit-mys.py restore-article --article-id 1
# 热门
python3 scripts/blog-mini-kit-mys.py top-articles --limit 5
```

#### 标签 / 用户 / 评论 / 留言 / 说说
```bash
python3 scripts/blog-mini-kit-mys.py create-label --lname "新标签"
python3 scripts/blog-mini-kit-mys.py create-user --uname "newuser" --pwd "123456"
python3 scripts/blog-mini-kit-mys.py create-comment --uid 1 --aid 1 --content "评论"
python3 scripts/blog-mini-kit-mys.py list-comments --aid 1
python3 scripts/blog-mini-kit-mys.py create-message --uid 1 --content "留言"
python3 scripts/blog-mini-kit-mys.py reply-message --uid 1 --mid 1 --content "回复"
python3 scripts/blog-mini-kit-mys.py create-mood --content "今天很开心"
```

#### 文件上传
```bash
python3 scripts/blog-mini-kit-mys.py upload-file --file /path/to/image.jpg
python3 scripts/blog-mini-kit-mys.py upload-files --files a.jpg b.png
python3 scripts/blog-mini-kit-mys.py list-uploads
python3 scripts/blog-mini-kit-mys.py delete-upload --filename abc123.jpg
```

#### 博客页面 / 后台管理
```bash
python3 scripts/blog-mini-kit-mys.py blog-home --page 1
python3 scripts/blog-mini-kit-mys.py blog-article --article-id 1
python3 scripts/blog-mini-kit-mys.py admin-login --username admin --password admin
python3 scripts/blog-mini-kit-mys.py admin-delete-articles --token <token> --ids 1 2
```

#### capability-list
```bash
python3 scripts/blog-mini-kit-mys.py capability-list
```
Expected: `{"capability":"capability-list","skill":"blog-mini-kit-mys","endpoint_count":32,...}`

> 每个子命令支持 `--format json|md` 切换输出格式。完整参数说明见 `references/` 分类文档。

## 判断标准 / Verification

- [ ] API 可达（health-check 返回 `{"status":"ok"}`）
- [ ] 只读操作返回有效数据（list-articles / list-labels / list-users 非空）
- [ ] 脚本 `--help` 无语法错误
- [ ] 退出码正确（0=成功 / 2=参数错误 / 3=缺少配置 / 4=API失败）
- [ ] capability-list 返回 endpoint_count=32

## 输出规范 / Output Format

### 脚本输出

- 默认输出：JSON
- 可选输出：Markdown 表格（`--format md`）
- 使用示例：`cd skills/blog-mini-kit-mys/ && python3 scripts/blog-mini-kit-mys.py list-articles --format md`

### Issue 评论格式

```
[blog-mini-kit-mys] ✅ {操作名称}完成

## 操作结果

| 操作 | 状态 | 资源 ID | 详情 |
|------|------|---------|------|
| {操作名} | ✅ 成功 / 🔴 失败 | {id} | {简要说明} |

**API 地址**：{base_url}
**执行时间**：{UTC ISO}
```

失败时：

```
[blog-mini-kit-mys] 🔴 {操作名称}失败

## 错误分析

- **操作**：{操作名}
- **错误**：{API 返回的错误信息}
- **HTTP 状态码**：{code}
- **原因**：{分析原因}

### 修复建议
{修复步骤}
```

## 参考文档 / References

- [API 端点总索引](references/api-reference.md) — 32 端点全量表
- [文章 API](references/articles.md) — 7 端点
- [标签 API](references/tags.md) — 2 端点
- [用户 API](references/users.md) — 2 端点
- [评论 API](references/comments.md) — 3 端点
- [留言 API](references/messages.md) — 4 端点
- [说说 API](references/moods.md) — 3 端点
- [文件上传 API](references/uploads.md) — 4 端点
- [健康检查 API](references/health.md) — 1 端点
- [博客页面 API](references/pages.md) — 2 端点
- [后台管理 API](references/admin.md) — 4 端点
- [测试用例](templates/test-vars.json)

## 分析结论示例

成功时：

```
分析结论：
- 场景：博客 API 操作
- Skill：blog-mini-kit-mys v1.0.0
- 操作：{subcommand} {params}
- 结果：✅ 成功（{API 返回的关键数据摘要}）
- 必须执行：Issue 评论汇总结果 → 任务结束
```

失败时：

```
分析结论：
- 场景：博客 API 操作
- Skill：blog-mini-kit-mys v1.0.0
- 操作：{subcommand} {params}
- 结果：🔴 失败（{错误原因}）
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
