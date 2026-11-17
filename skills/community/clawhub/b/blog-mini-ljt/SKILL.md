---
name: blog-mini-ljt
version: 1.0.0
description: |
  管理博客系统全部 API（8 模块 28 端点：文章/评论/标签/留言/心情/用户/文件/后台）。
  无认证公开 API，base_url 内置默认地址无配置即可用。供 AI Agent 完成博客内容全流程管理。
triggers:
  - 博客发文
  - 管理文章
  - 发表评论
  - 创建标签
  - 管理留言
  - 发布说说
  - 上传文件
  - 后台管理
tags:
  - blog
  - rest-api
  - content-management
  - fastapi
tools:
  - curl
---

# blog-mini-ljt

博客系统 API 管理 skill，封装 8 模块 28 端点（FastAPI + MySQL，无认证公开 API）。

## 安全硬约束（必须遵守）

**通用约束（所有 skill 必含）**：

1. 严禁读取 data/、configs/、sessions.db、user_accounts 等 Grape 内部数据。
2. API 返回 403/无权限时：立即停止该操作并回复用户，严禁尝试其他 token 或绕行手段。
3. 所有 curl / API 调用设 30s 超时——超时判定失败，不 hang。
4. 严禁 mock 模式/假数据：所有 API 调用必须真实访问目标系统。
5. 调用目标 API 一律以 `references/api-reference.md` 为准：严禁根据经验/记忆/猜测自行拼写 API 路径。

**动态约束**：

- 本 API 为无认证公开 API，不需要凭据。Admin 模块的 admin/admin 为系统默认账号（非凭据），通过命令行参数传入，不写入文件/日志/评论。

## 评论规范

- 所有 Issue/PR 评论 body 必须以 `[blog-mini-ljt]` 开头（环境变量未注入时用 skill name 作为前缀）
- 引用用户原文：`> {用户评论}\n\n[blog-mini-ljt] {回复}`

## Configuration

目标系统 API 地址。**无认证公开 API，脚本内置默认地址，无配置即可用**。

`{base_url}` 解析优先级（4 级）：

1. **项目知识** — 检查 `.project-info/` 目录下 JSON 配置文件（`config.BLOG_MINI_LJT_BASE_URL`）
2. **环境变量** — `BLOG_MINI_LJT_BASE_URL`
3. **当前上下文** — 用户直接提供或 A2A context 中已包含
4. **内置默认地址** — 脚本内置线上 API 地址，以上都无时自动使用（无配置即可用）

### 配置指导

#### 方式一：无配置直接用（推荐）

脚本内置默认线上地址，直接运行命令即可，无需任何环境变量。

#### 方式二：环境变量（指向其他实例时）

```bash
export BLOG_MINI_LJT_BASE_URL="http://<host>:<port>"
```

#### 方式三：项目知识 JSON 文件（持久化）

在项目根目录下创建 `.project-info/` 目录，放入任意名称的 `.json` 文件：

```json
{
  "config": {
    "BLOG_MINI_LJT_BASE_URL": "http://<host>:<port>"
  }
}
```

> OpenAPI 文档地址：`{base_url}/docs` | OpenAPI JSON：`{base_url}/openapi.json`

## 场景 / When to Use

- 用户要求发布/编辑/删除博客文章
- 用户要求管理文章评论、标签、留言、说说/心情
- 用户要求上传/管理文件（图片/视频/文档）
- 用户要求管理博客用户
- 用户要求后台批量管理文章（登录 + 批量删除）
- 用户要求完成博客内容全流程（创建标签 → 发文 → 评论）

Don't use for: 非 本博客系统 API 的操作 / 页面渲染（GET / 返回 HTML）/ 数据库直连操作。

## 知识 / Knowledge

### API Base URL

```
{base_url}
```

All endpoints below are relative to this base. 无认证，不需要 header。

### Endpoints

按 8 模块分组（完整字段详见 `references/api-reference.md`，数据模型详见 `references/schemas.md`）：

| 模块 | 子命令 | Method | Path | 说明 |
|------|--------|--------|------|------|
| Articles | list-articles | GET | /api/articles | 分页查询文章（page,size,lid,keyword） |
| Articles | get-article | GET | /api/articles/{id} | 文章详情+评论（热度+1） |
| Articles | top-articles | GET | /api/articles/heat/top | 热门文章 Top N（limit） |
| Articles | create-article | POST | /api/articles | 发布文章 |
| Articles | update-article | PUT | /api/articles/{id} | 更新文章 |
| Articles | delete-article | DELETE | /api/articles/{id} | 删除文章（soft=true/false） |
| Articles | restore-article | POST | /api/articles/{id}/restore | 恢复软删除文章 |
| Comments | create-comment | POST | /api/comments | 发表评论 |
| Comments | list-comments | GET | /api/comments/{aid} | 文章评论列表 |
| Comments | delete-comment | DELETE | /api/comments/{id} | 删除评论（软删除） |
| Labels | list-labels | GET | /api/lables | 获取所有标签（路径拼写为 lables） |
| Labels | create-label | POST | /api/lables | 创建标签（路径拼写为 lables） |
| Messages | list-messages | GET | /api/messages | 留言列表（含回复） |
| Messages | create-message | POST | /api/messages | 发表留言 |
| Messages | reply-message | POST | /api/messages/reply | 回复留言 |
| Messages | delete-message | DELETE | /api/messages/{id} | 删除留言（软删除） |
| Moods | list-moods | GET | /api/moods | 说说列表 |
| Moods | create-mood | POST | /api/moods | 发布说说 |
| Moods | delete-mood | DELETE | /api/moods/{id} | 删除说说（硬删除） |
| Uploads | upload-file | POST | /api/upload | 上传单文件（multipart field=file） |
| Uploads | upload-files | POST | /api/upload/multiple | 批量上传（multipart field=files） |
| Uploads | list-uploads | GET | /api/uploads/list | 列出已上传文件 |
| Uploads | delete-upload | DELETE | /api/uploads/{filename} | 删除文件 |
| Users | list-users | GET | /api/users | 用户列表 |
| Users | create-user | POST | /api/users | 创建用户 |
| Admin | admin-login | POST | /admin/login | 后台登录（form，返回 token） |
| Admin | admin-logout | GET | /admin/logout | 退出登录（t=token） |
| Admin | admin-delete-articles | POST | /admin/api/delete | 批量删除文章（token+ids） |

> 共 28 端点 + health-check（GET /health）+ capability-list。

### 认证方式

- **无认证**：8 模块 25 端点（Articles/Comments/Labels/Messages/Moods/Uploads/Users）均为公开 API，不需要凭据。
- **Session Token**：Admin 模块 3 端点需先 `admin-login` 获取 token（默认账号 admin/admin），后续操作携带 token。token 有效期 2 小时。
- API 地址：`BLOG_MINI_LJT_BASE_URL`（可选，内置默认地址）

**凭据前缀**：由 skill name 推导（`blog-mini-ljt` → `BLOG_MINI_LJT`），skill name 转大写下划线。

### Common Pitfalls

1. **标签端点路径拼写为 `/api/lables`（非 labels）。** 子命令用正确拼写 `list-labels`/`create-label`，脚本内部自动用实际路径 `/api/lables`。
2. **get-article 会自增热度。** 每次调用 GET /api/articles/{id} 文章 heat +1，非幂等。统计热度时注意。
3. **删除语义不一致。** 文章/评论/留言/评论默认软删除（deleted=1，可恢复），但说说/Uploads/Admin批量删除为硬删除（不可恢复）。delete-article 可传 `--soft false` 硬删除。
4. **Admin 登录是 form 表单非 JSON。** POST /admin/login 用 `application/x-www-form-urlencoded`（非 JSON body），脚本已处理；登录成功返回 302 + cookie token。
5. **文件上传用 multipart 非 JSON。** upload-file/upload-files 用 `files=` 参数（非 json=），字段名分别为 `file`/`files`。
6. **upload-files 批量上传字段是列表。** 用元组列表 `[('files', f), ...]`，不能用 dict value 为列表（requests 会报错）。

### 字段说明

8 个数据模型的完整字段表见 `references/schemas.md`。关键字段速查：

| 模型 | 必填字段 | 用途 |
|------|----------|------|
| ArticleCreate | title, content | 发布文章 |
| ArticleUpdate | （至少传一个） | 更新文章 |
| LableCreate | lname | 创建标签 |
| UserCreate | uname | 创建用户 |
| CommentCreate | uid, aid, content | 发表评论 |
| MessageCreate | uid, content | 发表留言 |
| Message2Create | uid, mid, content | 回复留言 |
| MoodCreate | content | 发布说说 |

## 步骤 / Steps

主流程：检查可达性 → 查询资源 → 执行操作。完整端点文档见 `references/api-reference.md`。

### 1. 检查 API 可达性

```bash
python3 scripts/blog-mini-ljt.py health-check
```
Expected: `{"status":"ok","service":"blog-api","version":"1.0.0"}`

### 2. 查询可用资源

```bash
python3 scripts/blog-mini-ljt.py list-labels        # 标签（获取 lid）
python3 scripts/blog-mini-ljt.py list-users          # 用户（获取 uid）
python3 scripts/blog-mini-ljt.py list-articles --page 1 --size 10
```
Expected: `{"code":200,"data":[...]}`

### 3. 执行操作（按模块选择）

#### Articles 文章

```bash
# 发布文章
python3 scripts/blog-mini-ljt.py create-article --title "标题" --content "内容" --lid 1
# 查询详情（含评论）
python3 scripts/blog-mini-ljt.py get-article --id 3
# 更新文章
python3 scripts/blog-mini-ljt.py update-article --id 3 --title "新标题" --heat 10
# 删除文章（软删除）
python3 scripts/blog-mini-ljt.py delete-article --id 3 --soft true
# 恢复文章
python3 scripts/blog-mini-ljt.py restore-article --id 3
# 热门文章
python3 scripts/blog-mini-ljt.py top-articles --limit 5
```

#### Comments 评论

```bash
python3 scripts/blog-mini-ljt.py create-comment --uid 1 --aid 3 --content "评论"
python3 scripts/blog-mini-ljt.py list-comments --aid 3
python3 scripts/blog-mini-ljt.py delete-comment --id 1
```

#### Labels 标签（端点实际路径 /api/lables）

```bash
python3 scripts/blog-mini-ljt.py create-label --lname "前端"
python3 scripts/blog-mini-ljt.py list-labels
```

#### Messages 留言

```bash
python3 scripts/blog-mini-ljt.py create-message --uid 1 --content "留言"
python3 scripts/blog-mini-ljt.py reply-message --uid 2 --mid 1 --content "回复"
python3 scripts/blog-mini-ljt.py list-messages
python3 scripts/blog-mini-ljt.py delete-message --id 1
```

#### Moods 说说

```bash
python3 scripts/blog-mini-ljt.py create-mood --content "今天很好" --title "日常"
python3 scripts/blog-mini-ljt.py list-moods
python3 scripts/blog-mini-ljt.py delete-mood --id 1
```

#### Uploads 文件

```bash
python3 scripts/blog-mini-ljt.py upload-file --filepath /path/to/image.png
python3 scripts/blog-mini-ljt.py upload-files --filepaths /path/a.png /path/b.png
python3 scripts/blog-mini-ljt.py list-uploads
python3 scripts/blog-mini-ljt.py delete-upload --filename xxx.png
```
参数说明：`--filepath` 本地文件路径；`--filepaths` 多文件路径空格分隔。

#### Users 用户

```bash
python3 scripts/blog-mini-ljt.py create-user --uname alice --email alice@example.com
python3 scripts/blog-mini-ljt.py list-users
```

#### Admin 后台管理

```bash
# 1. 登录获取 token
python3 scripts/blog-mini-ljt.py admin-login --username admin --password admin
# 2. 批量删除文章（用上一步返回的 token）
python3 scripts/blog-mini-ljt.py admin-delete-articles --token <token> --ids 1 2 3
# 3. 退出登录
python3 scripts/blog-mini-ljt.py admin-logout --token <token>
```

#### 完整流程示例（创建标签 → 发文 → 评论 → 清理）

```bash
# 1. 创建标签
python3 scripts/blog-mini-ljt.py create-label --lname "测试"
# 2. 用新标签发文（lid 从上一步返回获取）
python3 scripts/blog-mini-ljt.py create-article --title "测试文" --content "内容" --lid 1
# 3. 发评论（aid 从上一步返回获取）
python3 scripts/blog-mini-ljt.py create-comment --uid 1 --aid <文章id> --content "好文"
# 4. 清理：删除评论 + 软删除文章
python3 scripts/blog-mini-ljt.py delete-comment --id <评论id>
python3 scripts/blog-mini-ljt.py delete-article --id <文章id> --soft true
```

#### capability-list

```bash
python3 scripts/blog-mini-ljt.py capability-list
```
Expected: `{"capability":"capability-list","skill":"blog-mini-ljt","subcommand_count":30,...}`

> 所有子命令支持 `--format json`（默认）/ `--format md`（Markdown 表格）。

## 判断标准 / Verification

- [ ] API 可达（health-check 返回 status=ok）
- [ ] 只读操作返回有效数据（list-articles/labels/users/moods/messages/uploads 非空或字段完整）
- [ ] 脚本 `--help` 无语法错误
- [ ] 退出码正确（0=成功 / 2=参数错误 / 3=缺少配置 / 4=API 失败）
- [ ] 完整流程通过（create-label → create-article → create-comment → cleanup）
- [ ] Admin 登录返回有效 token
- [ ] 28 端点全覆盖（capability-list 显示 endpoint_count=28）

## 输出规范 / Output Format

### 脚本输出

- 默认输出：JSON（`--format json`）
- 可选输出：Markdown 表格（`--format md`）
- 使用示例：`cd skills/blog-mini-ljt/ && python3 scripts/blog-mini-ljt.py list-articles --format md`

### Issue 评论格式

执行完操作后，Issue 评论 body 格式：

```
[blog-mini-ljt] ✅ {操作名称}完成

## 操作结果

| 操作 | 状态 | 资源 ID | 详情 |
|------|------|---------|------|
| {操作名} | ✅ 成功 / 🔴 失败 | {id} | {简要说明} |

**API 地址**：{base_url}
**执行时间**：{UTC ISO}
```

失败时：

```
[blog-mini-ljt] 🔴 {操作名称}失败

## 错误分析

- **操作**：{操作名}
- **错误**：{API 返回的错误信息}
- **HTTP 状态码**：{code}
- **原因**：{分析原因}

### 修复建议
{修复步骤}
```

## 参考文档 / References

- [API 端点文档](references/api-reference.md) — 28 端点完整 method/path/body/响应说明
- [数据模型 Schema](references/schemas.md) — 8 个请求体模型字段表
- [测试用例](templates/test-vars.json) — 13 条测试用例
- OpenAPI 文档：`{base_url}/docs`

## 分析结论示例

成功时：

```
分析结论：
- 场景：博客 API 操作
- Skill：blog-mini-ljt v1.0.0
- 操作：{subcommand} {params}
- 结果：✅ 成功（{API 返回的关键数据摘要}）
- 必须执行：Issue 评论汇总结果 → 任务结束
```

失败时：

```
分析结论：
- 场景：博客 API 操作
- Skill：blog-mini-ljt v1.0.0
- 操作：{subcommand} {params}
- 结果：🔴 失败（{错误原因}）
- 必须执行：Issue 评论报告错误 → 任务结束
```

## 任务结束

完成所有业务动作后，在最终答复末尾输出以下 JSON 块并结束任务：

```json
{
  "actions": ["{具体执行的操作，如 create-article: 发布文章 id=3}"],
  "conclusion": "{处理结论，如 发布成功，文章 id=3}",
  "artifacts": ["{产生的产物：写操作返回资源 ID 或操作结果 / 只读查询无产物填空数组}"],
  "next_step": "{下一步建议，如 无 / 等待用户下一步指令}",
  "issue_summary": "{Issue 最新聚合结论，紧凑文本，用 | 分隔}"
}
```

注意：只输出一个 JSON 块，放在答复末尾。
