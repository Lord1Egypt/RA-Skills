# API 端点文档 — blog-mini-kit-ljt2

> 来源：博客系统 OpenAPI 文档（{base_url}/openapi.json）
> 认证方式：无认证（公开 API）
> 所有路径相对于 `{base_url}`

## 端点总览

共 26 个 API 端点，覆盖 8 大资源域。

## 健康检查 Health

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /health | — | 健康检查，返回 `{"status":"ok","service":"blog-api","version":"1.0.0"}` |

## 文章 Articles

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/articles | — | 查询文章列表（params: page=1, size=10, lid=0, keyword） |
| POST | /api/articles | ArticleCreate | 创建文章 |
| GET | /api/articles/heat/top | — | 查询热门文章（params: limit=5） |
| GET | /api/articles/{article_id} | — | 查询文章详情 |
| PUT | /api/articles/{article_id} | ArticleUpdate | 更新文章 |
| DELETE | /api/articles/{article_id} | — | 删除文章（params: soft=true/false，默认 true 软删除） |
| POST | /api/articles/{article_id}/restore | — | 恢复软删除的文章 |

### ArticleCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 是 | — | 标题 |
| content | string | 是 | — | 内容 |
| uid | integer | 否 | 1 | 作者 ID |
| lid | integer | 否 | 1 | 标签 ID |
| img | string | 否 | — | 封面图片路径 |
| heat | integer | 否 | 0 | 热度值 |

### ArticleUpdate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 否 | — | 标题 |
| content | string | 否 | — | 内容 |
| lid | integer | 否 | — | 标签 ID |
| img | string | 否 | — | 封面图片路径 |
| heat | integer | 否 | — | 热度值 |

## 标签 Labels

> ⚠️ API 路径为 `/api/lables`（拼写与 labels 不同），脚本内部使用实际路径，子命令名用正确拼写 labels。

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/lables | — | 查询标签列表 |
| POST | /api/lables | LableCreate | 创建标签 |

### LableCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| lname | string | 是 | — | 标签名称 |

## 用户 Users

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/users | — | 查询用户列表 |
| POST | /api/users | UserCreate | 创建用户 |

### UserCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uname | string | 是 | — | 用户名 |
| phone | string | 否 | — | 手机号 |
| pwd | string | 否 | — | 密码 |
| email | string | 否 | — | 邮箱 |
| img | string | 否 | img/moren.jpg | 头像路径 |

## 评论 Comments

| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /api/comments | CommentCreate | 创建评论 |
| GET | /api/comments/{aid} | — | 查询文章评论列表 |
| DELETE | /api/comments/{comment_id} | — | 删除评论 |

### CommentCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | integer | 是 | — | 用户 ID |
| aid | integer | 是 | — | 文章 ID |
| content | string | 是 | — | 评论内容 |

## 留言 Messages

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/messages | — | 查询留言列表 |
| POST | /api/messages | MessageCreate | 创建留言 |
| POST | /api/messages/reply | Message2Create | 回复留言 |
| DELETE | /api/messages/{message_id} | — | 删除留言 |

### MessageCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | integer | 是 | — | 用户 ID |
| content | string | 是 | — | 留言内容 |

### Message2Create（回复留言）
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | integer | 是 | — | 用户 ID |
| mid | integer | 是 | — | 留言 ID |
| content | string | 是 | — | 回复内容 |

## 说说 Moods

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/moods | — | 查询说说列表 |
| POST | /api/moods | MoodCreate | 创建说说 |
| DELETE | /api/moods/{mood_id} | — | 删除说说 |

### MoodCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| content | string | 是 | — | 说说内容 |
| title | string | 否 | — | 标题 |
| src | string | 否 | — | 来源/媒体路径 |

## 文件上传 Uploads

| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /api/upload | multipart/form-data (file) | 上传单个文件 |
| POST | /api/upload/multiple | multipart/form-data (files) | 批量上传文件 |
| GET | /api/uploads/list | — | 查询已上传文件列表 |
| DELETE | /api/uploads/{filename} | — | 删除已上传文件 |

### 上传请求体
- 单文件上传：`multipart/form-data`，字段名 `file`（单个文件）
- 批量上传：`multipart/form-data`，字段名 `files`（多个文件，同名字段）

## 响应结构

列表类端点统一返回：
```json
{"code": 200, "data": [...], "total": N, "page": N, "size": N}
```

健康检查返回：
```json
{"status": "ok", "service": "blog-api", "version": "1.0.0"}
```
