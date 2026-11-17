---
name: blog-publish
version: 1.0.0
description: 博客系统内容发布与管理 Skill——封装文章/标签/文件上传全流程 API，提供 curl 和 Python 双语言示例
triggers:
  - 发布博客文章
  - 创建标签
  - 上传文件
  - 查询文章列表
tags:
  - blog
  - publish
  - api
  - fastapi
tools:
  - curl
  - python3
---

# blog-publish

博客系统内容发布与管理 Skill。封装博客系统 API（FastAPI 实现的无认证公开接口）的文章发布、标签管理、文件上传全流程，提供 curl 和 Python 双语言调用示例。

## 安全硬约束（必须遵守）

1. 严禁读取 data/、configs/、sessions.db、user_accounts 等 Grape 内部数据。
2. API 返回 403/无权限时：立即停止该操作并回复用户，严禁尝试其他 token 或绕行手段。
3. 所有 curl / API 调用设 30s 超时——超时判定失败，不 hang。
4. 严禁 mock 模式/假数据：所有 API 调用必须真实访问目标系统。
5. 调用目标 API 一律以 `references/api-reference.md` 为准：严禁根据经验/记忆/猜测自行拼写 API 路径。

## 评论规范

- 所有 Issue/PR 评论 body 必须以 `[blog-publish]` 开头
- 引用用户原文：`> {用户评论}\n\n[blog-publish] {回复}`

## Configuration

目标系统 API 地址必须在使用前确定。所有命令中的 `{base_url}` 替换为实际地址（格式 `http://<host>:<port>`）。

`{base_url}` 解析优先级：

1. **项目知识** — 检查 `.project-info/` 目录下 JSON 配置文件（config.BLOG_PUBLISH_BASE_URL）
2. **环境变量** — `BLOG_PUBLISH_BASE_URL`
3. **当前上下文** — 用户直接提供或 A2A context 中已包含
4. **交互输入** — 以上都无时提示用户输入

### 配置指导

#### 方式一：环境变量（临时，推荐快速测试）

```bash
export BLOG_PUBLISH_BASE_URL="http://<host>:<port>"
```

#### 方式二：项目知识 JSON 文件（持久化，推荐生产使用）

在项目根目录下创建 `.project-info/` 目录，放入任意名称的 `.json` 文件：

```json
{
  "config": {
    "BLOG_PUBLISH_BASE_URL": "http://<host>:<port>"
  }
}
```

> ⚠️ `.project-info/` 含敏感配置，不提交到 git 仓库（加入 .gitignore）。

## 场景 / When to Use

- 发布新博客文章（创建文章 → 返回 ID → 验证可查询）
- 更新已有文章内容/标题/标签/封面/热度
- 删除文章（软删除可恢复 / 硬删除不可恢复）
- 恢复软删除的文章
- 查询文章列表（分页/按标签/按关键词）
- 查询文章详情（含评论）
- 获取热门文章 Top N
- 创建标签 / 查询标签列表
- 上传单个文件（图片/视频/文档）
- 批量上传文件
- 查询已上传文件列表

Don't use for: 非本博客系统 API 的操作；用户/评论/留言/说说管理（本 skill 仅覆盖文章/标签/文件上传，按 Issue #3 范围）。

## 知识 / Knowledge

### API Base URL

```
{base_url}
```

All endpoints below are relative to this base. 无认证（公开 API），不需要 header。

### Endpoints

#### 文章管理

| Method | Path | Body / Params | Description |
|--------|------|---------------|-------------|
| GET | `/api/articles` | page, size, lid, keyword | 分页查询文章列表 |
| GET | `/api/articles/{id}` | path: id | 查询文章详情（热度+1） |
| POST | `/api/articles` | ArticleCreate | 发布新文章 |
| PUT | `/api/articles/{id}` | ArticleUpdate | 更新文章（全可选） |
| DELETE | `/api/articles/{id}` | query: soft=true\|false | 删除文章 |
| POST | `/api/articles/{id}/restore` | path: id | 恢复软删除文章 |
| GET | `/api/articles/heat/top` | query: limit | 热门文章 Top N |

#### 标签管理

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | `/api/lables` | — | 获取所有标签 |
| POST | `/api/lables` | LableCreate | 创建标签 |

> ⚠️ API 路径为 `/api/lables`（非标准拼写），调用须用实际路径。

#### 文件上传

| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | `/api/upload` | multipart, field=`file` | 上传单个文件 |
| POST | `/api/upload/multiple` | multipart, field=`files` | 批量上传 |
| GET | `/api/uploads/list` | — | 列出已上传文件 |

### 认证方式

无认证（公开 API）。仅需配置 `{base_url}`。

- API 地址：`BLOG_PUBLISH_BASE_URL`

**凭据前缀**：由 skill name 推导（`blog-publish` → `BLOG_PUBLISH`）。

### Common Pitfalls

1. **API 不可达。** 先 `curl --max-time 30 {base_url}/health` 确认可达，再调其他端点。
2. **标签路径拼写。** API 用 `/api/lables`（非 labels），脚本内部已正确处理，curl 手动调用须用 `lables`。
3. **硬删除不可恢复。** `DELETE` 默认软删除（soft=true）；硬删除需显式传 `soft=false`，数据永久丢失，操作前务必确认。
4. **文件类型限制。** 上传仅允许图片(.jpg/.png/.gif/.webp/.svg 等)、视频(.mp4/.webm/.mov 等)、文档(.pdf/.doc/.txt/.zip/.md)，其他类型返回 400。
5. **GET 文章详情热度+1。** 每次调 `GET /api/articles/{id}` 都会使 heat+1，批量查询热度时注意副作用。
6. **更新文章无字段更新时报 400。** `PUT` 请求体所有字段为空时返回 400「没有需要更新的字段」，至少传一个字段。

### 字段说明

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 是(创建) | — | 文章标题 |
| content | string | 是(创建) | — | 文章内容（支持 HTML） |
| uid | int | 否 | 1 | 作者用户 ID |
| lid | int | 否 | 1 | 标签 ID |
| img | string | 否 | null | 封面图 URL |
| heat | int | 否 | 0 | 热度 |
| lname | string | 是(标签) | — | 标签名称 |

## 步骤 / Steps

### 1. 检查 API 可达性

```bash
# curl
curl -s --max-time 30 {base_url}/health
# Expected: {"status":"ok","service":"blog-api","version":"1.0.0"}

# Python
python3 scripts/blog-publish.py health-check
```

### 2. 查询可用资源（标签）

```bash
# curl
curl -s --max-time 30 {base_url}/api/lables
# Expected: {"code":200,"data":[{"id":1,"lname":"技术"},...]}

# Python
python3 scripts/blog-publish.py list-labels
```

### 3. 发布文章（创建 → 返回 ID → 验证）

#### 创建文章

```bash
# curl
curl -s --max-time 30 -X POST {base_url}/api/articles \
  -H "Content-Type: application/json" \
  -d '{"title":"我的第一篇博客","content":"<p>Hello World</p>","uid":1,"lid":1}'
# Expected: {"code":200,"message":"文章发布成功","data":{"id":3}}

# Python
python3 scripts/blog-publish.py create-article \
  --title "我的第一篇博客" --content "<p>Hello World</p>" --uid 1 --lid 1
```

#### 验证可查询

```bash
# curl（用返回的 ID）
curl -s --max-time 30 {base_url}/api/articles/3
# Expected: {"code":200,"data":{"article":{...},"comments":[...]}}

# Python
python3 scripts/blog-publish.py get-article --id 3
```

### 4. 文章管理

#### 更新文章

```bash
# curl
curl -s --max-time 30 -X PUT {base_url}/api/articles/3 \
  -H "Content-Type: application/json" \
  -d '{"title":"更新后的标题","heat":10}'
# Expected: {"code":200,"message":"文章更新成功"}

# Python
python3 scripts/blog-publish.py update-article --id 3 --title "更新后的标题" --heat 10
```

#### 删除文章（默认软删除）

```bash
# curl — 软删除（默认，可恢复）
curl -s --max-time 30 -X DELETE "{base_url}/api/articles/3?soft=true"
# Expected: {"code":200,"message":"文章已删除"}

# curl — ⚠️ 硬删除（不可恢复，需显式 opt-in）
curl -s --max-time 30 -X DELETE "{base_url}/api/articles/3?soft=false"
# Expected: {"code":200,"message":"文章已删除"}（数据永久丢失！）

# Python — 软删除
python3 scripts/blog-publish.py delete-article --id 3
# Python — 硬删除（不可恢复）
python3 scripts/blog-publish.py delete-article --id 3 --hard
```

#### 恢复软删除文章

```bash
# curl
curl -s --max-time 30 -X POST {base_url}/api/articles/3/restore
# Expected: {"code":200,"message":"文章已恢复"}

# Python
python3 scripts/blog-publish.py restore-article --id 3
```

#### 查询文章列表

```bash
# curl — 分页 + 按标签 + 关键词
curl -s --max-time 30 "{base_url}/api/articles?page=1&size=10&lid=1&keyword=博客"
# Expected: {"code":200,"data":[...],"total":N,"page":1,"size":10}

# Python
python3 scripts/blog-publish.py list-articles --page 1 --size 10 --lid 1 --keyword 博客
```

#### 热门文章

```bash
curl -s --max-time 30 "{base_url}/api/articles/heat/top?limit=5"
python3 scripts/blog-publish.py top-articles --limit 5
```

### 5. 标签管理

```bash
# 创建标签
curl -s --max-time 30 -X POST {base_url}/api/lables \
  -H "Content-Type: application/json" -d '{"lname":"新标签"}'
# Expected: {"code":200,"data":{"id":7,"lname":"新标签"}}

python3 scripts/blog-publish.py create-label --lname "新标签"

# 标签列表
curl -s --max-time 30 {base_url}/api/lables
python3 scripts/blog-publish.py list-labels
```

### 6. 文件上传

```bash
# 单文件上传（curl -F）
curl -s --max-time 30 -X POST {base_url}/api/upload \
  -F "file=@/path/to/image.jpg"
# Expected: {"code":200,"data":{"url":"/uploads/xxx.jpg","filename":"image.jpg","type":"image","size":12345}}

# Python（单文件）
python3 scripts/blog-publish.py upload-file --filepath /path/to/image.jpg

# 批量上传（curl -F 多个 file 字段）
curl -s --max-time 30 -X POST {base_url}/api/upload/multiple \
  -F "files=@/path/to/a.jpg" -F "files=@/path/to/b.png"
# Expected: {"code":200,"data":[{"url":"...","filename":"a.jpg",...},...]}}

# Python（批量）
python3 scripts/blog-publish.py upload-files --filepaths /path/to/a.jpg /path/to/b.png

# 文件列表
curl -s --max-time 30 {base_url}/api/uploads/list
python3 scripts/blog-publish.py list-uploads
```

### 7. 错误处理指引

| HTTP 状态码 | 含义 | 处理建议 |
|-------------|------|----------|
| 200 | 成功 | 正常处理返回数据 |
| 400 | 请求错误 | 检查文件类型 / 更新字段是否为空 |
| 404 | 资源不存在 | 确认 ID 正确，文章可能已被硬删除 |
| 422 | 验证错误 | 检查必填字段（title/content/lname）是否缺失或类型错误 |
| 500 | 服务异常 | API 后端异常，稍后重试或联系运维 |

## 判断标准 / Verification

- [ ] API 可达（GET /health 返回 200 + `{"status":"ok"}`）
- [ ] 创建文章返回文章 ID（POST /api/articles → data.id）
- [ ] 创建后可通过 GET /api/articles/{id} 查询到（验证发布成功）
- [ ] 软删除后文章不在列表中（deleted=0 过滤），但可通过 restore 恢复
- [ ] 硬删除（soft=false）后文章彻底消失，restore 返回 404
- [ ] 标签创建返回 ID，列表可查到
- [ ] 文件上传返回 url，可通过 {base_url}{url} 访问
- [ ] 脚本 `--help` 无语法错误
- [ ] 退出码正确（0=成功 / 2=参数错误 / 3=缺少配置 / 4=API失败）

## 输出规范 / Output Format

- 默认输出：JSON（`--format json`）
- 可选输出：Markdown 表格（`--format md`）
- curl 示例格式：`curl -s --max-time 30 {base_url}/api/...`

### Issue 评论格式（成功）

```
[blog-publish] ✅ 操作完成

| 操作 | 结果 |
|------|------|
| 创建文章 | ID=3 |
| 验证查询 | ✅ 可查 |
| 标签 | 技术类 |
```

### Issue 评论格式（失败）

```
[blog-publish] ❌ 操作失败

| 步骤 | 错误 |
|------|------|
| 创建文章 | HTTP 422: title field required |
```

## 参考文档 / References

- API 端点完整文档：`references/api-reference.md`
- 测试用例：`templates/test-vars.json`
- Python 入口：`scripts/blog-publish.py`

## 分析结论示例

成功时：

```
分析结论：
- 场景：skill 创建（A2A 触发，Issue Agent 交棒 Coding Agent）
- Skill：blog-publish v1.0.0
- 产物：SKILL.md + scripts/blog-publish.py + references/api-reference.md + templates/test-vars.json
- 验证：validate-skill.sh ✅ / API 调用 ✅（health-check + list-articles + create-article）
- 必须执行：创建 PR → A2A 交棒 QA
```

失败时：

```
分析结论：
- 场景：skill 创建
- Skill：blog-publish
- 结果：🔴 失败（validate-skill.sh 失败 / API 不可达）
- 必须执行：Issue 评论报告错误 → A2A 回 Issue Agent
```

## 任务结束

完成所有业务动作后，在最终答复末尾输出 JSON 块，然后结束任务：

```json
{
  "actions": ["做了什么"],
  "conclusion": "处理结论",
  "artifacts": ["产生的产物"],
  "next_step": "下一步建议",
  "issue_summary": "Issue 最新聚合结论（紧凑文本，用 | 分隔）"
}
```
