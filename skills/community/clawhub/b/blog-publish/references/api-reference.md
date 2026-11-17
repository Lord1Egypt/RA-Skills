# API Reference — Blog System API

> 博客系统 RESTful API，无需认证（公开接口）。
> 所有端点基于 `{base_url}`，格式 `http://<host>:<port>`。
> 健康检查：`GET {base_url}/health` → `{"status":"ok"}`

## 认证方式

无认证（公开 API）。仅需配置 `{base_url}` 即可调用所有端点。

## 端点列表

### 健康检查

| Method | Path | Description |
|--------|------|-------------|
| GET | `{base_url}/health` | 检查 API 可达性，返回 `{"status":"ok","service":"blog-api","version":"1.0.0"}` |

### 文章管理

| Method | Path | Body / Params | Description |
|--------|------|---------------|-------------|
| GET | `{base_url}/api/articles` | query: page(默认1), size(默认10,≤100), lid(默认0=不过滤), keyword(默认空) | 分页查询文章列表（关联用户名和标签名） |
| GET | `{base_url}/api/articles/{article_id}` | path: article_id | 查询单篇文章详情（含评论），热度 +1 |
| POST | `{base_url}/api/articles` | body: ArticleCreate | 发布新文章 |
| PUT | `{base_url}/api/articles/{article_id}` | body: ArticleUpdate | 更新文章（所有字段可选） |
| DELETE | `{base_url}/api/articles/{article_id}` | query: soft(默认true) | 删除文章（soft=true 软删除 / soft=false 硬删除不可恢复） |
| POST | `{base_url}/api/articles/{article_id}/restore` | path: article_id | 恢复软删除的文章 |
| GET | `{base_url}/api/articles/heat/top` | query: limit(默认5,1-20) | 获取热门文章 Top N |

### 标签管理

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | `{base_url}/api/lables` | — | 获取所有标签 |
| POST | `{base_url}/api/lables` | body: LableCreate | 创建标签 |

> ⚠️ 注意：API 路径为 `/api/lables`（非标准拼写 labels），调用时须使用实际路径。

### 文件上传

| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | `{base_url}/api/upload` | multipart/form-data, field=`file` | 上传单个文件 |
| POST | `{base_url}/api/upload/multiple` | multipart/form-data, field=`files`（数组） | 批量上传文件 |
| GET | `{base_url}/api/uploads/list` | — | 列出所有已上传文件 |
| DELETE | `{base_url}/api/uploads/{filename}` | path: filename | 删除已上传文件 |

## 数据模型

### ArticleCreate（创建文章）

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 是 | — | 文章标题 |
| content | string | 是 | — | 文章内容（支持 HTML） |
| uid | int | 否 | 1 | 作者用户 ID |
| lid | int | 否 | 1 | 标签 ID |
| img | string | 否 | null | 封面图 URL |
| heat | int | 否 | 0 | 初始热度 |

### ArticleUpdate（更新文章，全部可选）

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 否 | null | 新标题 |
| content | string | 否 | null | 新内容 |
| lid | int | 否 | null | 新标签 ID |
| img | string | 否 | null | 新封面图 URL |
| heat | int | 否 | null | 新热度值 |

### LableCreate（创建标签）

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| lname | string | 是 | — | 标签名称 |

## 响应格式

所有 API 返回 JSON，统一格式：

- 查询类：`{"code": 200, "data": <数据>, ...}`
- 文章列表：`{"code": 200, "data": [...], "total": N, "page": N, "size": N}`
- 创建类：`{"code": 200, "message": "...", "data": {"id": N}}`
- 错误类：HTTP 4xx/5xx + `{"detail": "错误信息"}`

## 允许上传的文件类型

- 图片：.jpg .jpeg .png .gif .webp .bmp .svg
- 视频：.mp4 .webm .ogg .mov .avi .mkv
- 文档：.pdf .doc .docx .txt .zip .tar .gz .md

## 错误处理

| HTTP 状态码 | 含义 | 处理建议 |
|-------------|------|----------|
| 200 | 成功 | 正常处理返回数据 |
| 400 | 请求错误 | 检查文件类型 / 请求体格式 |
| 404 | 资源不存在 | 确认 ID 是否正确 |
| 422 | 验证错误 | 检查必填字段（title/content/lname） |
| 500 | 服务异常 | API 后端异常，稍后重试或联系运维 |
