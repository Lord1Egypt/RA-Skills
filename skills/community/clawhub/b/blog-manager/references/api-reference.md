# Blog System API v1.0.0 端点文档

> 共 26 个 API 端点（排除 2 个 Web 页面端点）。无认证。路径前缀 `/api`（健康检查 `/health` 在根路径）。

## 文章管理（7 端点）

### GET /api/articles

分页列出文章。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| page | query | int | 页码，默认 1 |
| size | query | int | 每页条数，默认 10 |
| lid | query | int | 标签 ID（0=全部），默认 0 |
| keyword | query | string | 搜索关键词 |

响应：`{code: 200, data: [...], total: N, page: N, size: N}`

### POST /api/articles

创建文章。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| title | body | string | 标题（必填） |
| content | body | string | 内容（必填） |
| uid | body | int | 用户 ID，默认 1 |
| lid | body | int | 标签 ID，默认 1 |
| img | body | string | 封面图路径 |
| heat | body | int | 热度值，默认 0 |

响应：`{code: 200, data: {id: N}}`

### GET /api/articles/{article_id}

获取文章详情及评论。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| article_id | path | int | 文章 ID |

响应：`{code: 200, data: {article: {...}, comments: [...]}}`

### PUT /api/articles/{article_id}

更新文章。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| article_id | path | int | 文章 ID |
| title | body | string | 新标题 |
| content | body | string | 新内容 |
| lid | body | int | 标签 ID |
| img | body | string | 封面图路径 |
| heat | body | int | 热度值 |

响应：`{code: 200, message: "..."}`

### DELETE /api/articles/{article_id}

删除文章（支持软删除）。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| article_id | path | int | 文章 ID |
| soft | query | string | 软删除 true/false，默认 true |

响应：`{code: 200, message: "..."}`

### POST /api/articles/{article_id}/restore

恢复软删除的文章。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| article_id | path | int | 文章 ID |

响应：`{code: 200, message: "..."}`

### GET /api/articles/heat/top

获取热门文章。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| limit | query | int | 返回条数，默认 5 |

响应：`{code: 200, data: [{id, title, heat}, ...]}`

## 标签管理（2 端点）

### GET /api/lables

列出所有标签。

响应：`{code: 200, data: [{id, lname}, ...]}`

### POST /api/lables

创建标签。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| lname | body | string | 标签名称（必填） |

响应：`{code: 200, data: {id, lname}}`

## 用户管理（2 端点）

### GET /api/users

列出所有用户。

响应：`{code: 200, data: [{id, uname, phone, email, img, createtime}, ...]}`

### POST /api/users

创建用户。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| uname | body | string | 用户名（必填） |
| phone | body | string | 手机号 |
| pwd | body | string | 密码 |
| email | body | string | 邮箱 |
| img | body | string | 头像路径，默认 img/moren.jpg |

响应：`{code: 200, data: {id}}`

## 评论管理（3 端点）

### POST /api/comments

创建评论。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| uid | body | int | 用户 ID（必填） |
| aid | body | int | 文章 ID（必填） |
| content | body | string | 评论内容（必填） |

响应：`{code: 200, data: {id}}`

### GET /api/comments/{aid}

列出文章评论。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| aid | path | int | 文章 ID |

响应：`{code: 200, data: [{id, uname, content, createtime}, ...]}`

### DELETE /api/comments/{comment_id}

删除评论。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| comment_id | path | int | 评论 ID |

响应：`{code: 200, message: "..."}`

## 留言管理（4 端点）

### GET /api/messages

列出留言及回复。

响应：`{code: 200, data: [{id, uname, content, createtime, replies: [...]}, ...]}`

### POST /api/messages

创建留言。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| uid | body | int | 用户 ID（必填） |
| content | body | string | 留言内容（必填） |

响应：`{code: 200, data: {id}}`

### POST /api/messages/reply

回复留言。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| uid | body | int | 用户 ID（必填） |
| mid | body | int | 留言 ID（必填） |
| content | body | string | 回复内容（必填） |

响应：`{code: 200, data: {id}}`

### DELETE /api/messages/{message_id}

删除留言。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| message_id | path | int | 留言 ID |

响应：`{code: 200, message: "..."}`

## 说说管理（3 端点）

### GET /api/moods

列出说说。

响应：`{code: 200, data: [{id, title, content, src, createtime}, ...]}`

### POST /api/moods

创建说说。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| content | body | string | 说说内容（必填） |
| title | body | string | 标题 |
| src | body | string | 媒体路径 |

响应：`{code: 200, data: {id}}`

### DELETE /api/moods/{mood_id}

删除说说。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| mood_id | path | int | 说说 ID |

响应：`{code: 200, message: "..."}`

## 文件上传（4 端点）

### POST /api/upload

上传单个文件（multipart）。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| file | multipart | file | 文件（必填，字段名 `file`） |

响应：`{code: 200, data: {url, ...}}`

### POST /api/upload/multiple

批量上传文件（multipart）。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| files | multipart | file[] | 文件列表（必填，字段名 `files`） |

响应：`{code: 200, data: [{url, filename, type, size}, ...]}`

### GET /api/uploads/list

列出已上传文件。

响应：`{code: 200, data: [{filename, url, type, size}, ...]}`

### DELETE /api/uploads/{filename}

删除已上传文件。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| filename | path | string | 文件名（URL 编码） |

响应：`{code: 200, message: "..."}`

## 健康检查（1 端点）

### GET /health

健康检查（注意：端点在根路径，非 `/api` 前缀）。

响应：`{status: "ok", service: "blog-api", version: "1.0.0"}`

## 排除的端点

| # | 端点 | 原因 |
|---|------|------|
| 26 | GET / | Web 页面（博客首页） |
| 27 | GET /article/{id} | Web 页面（文章详情页） |
