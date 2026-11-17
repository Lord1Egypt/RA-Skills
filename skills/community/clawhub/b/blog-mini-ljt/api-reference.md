# API 端点文档 — blog-mini-ljt

> 博客系统 API（8 模块 28 端点），无认证公开 API。
> 所有路径相对于 `{base_url}`（默认 `http://<host>:<port>`，脚本内置默认地址，可被环境变量 `BLOG_MINI_LJT_BASE_URL` 或 `.project-info/` JSON 配置覆盖）。
> OpenAPI 文档地址：`{base_url}/docs` | OpenAPI JSON：`{base_url}/openapi.json`

## 通用响应结构

所有 API 返回 JSON，统一格式：

```json
{"code": 200, "data": ..., "message": "..."}
```

- `code: 200` = 成功
- 错误时 FastAPI 返回 4xx + `{"detail": "..."}`

---

## 模块 1：Articles（文章，7 端点）

### 1.1 GET /api/articles — 分页查询文章列表

| 项 | 值 |
|---|---|
| 子命令 | `list-articles` |
| Method | GET |
| Path | `/api/articles` |
| Query | `page`(int,默认1,≥1), `size`(int,默认10,1-100), `lid`(int,默认0,按标签筛选), `keyword`(str,默认"",标题搜索) |

**响应**：
```json
{"code":200,"data":[{"id":2,"img":null,"uid":1,"title":"...","lid":1,"content":"...","heat":0,"deleted":0,"createtime":"2026-08-25T00:21:20","uname":"admin","lname":"技术"}],"total":2,"page":1,"size":10}
```

**示例**：`python3 scripts/blog-mini-ljt.py list-articles --page 1 --size 10 --lid 1 --keyword "测试"`

### 1.2 GET /api/articles/heat/top — 获取热门文章 Top N

| 项 | 值 |
|---|---|
| 子命令 | `top-articles` |
| Method | GET |
| Path | `/api/articles/heat/top` |
| Query | `limit`(int,默认5,1-20) |

**响应**：`{"code":200,"data":[{"id":1,"title":"...","heat":5}]}`

### 1.3 GET /api/articles/{id} — 查询单篇文章详情（含评论）

| 项 | 值 |
|---|---|
| 子命令 | `get-article` |
| Method | GET |
| Path | `/api/articles/{article_id}` |
| Path 参数 | `article_id`(int,必填) |

**说明**：每次调用文章热度 +1。响应含文章详情 + 评论列表。
**响应**：`{"code":200,"data":{"article":{...},"comments":[{...}]}}`

### 1.4 POST /api/articles — 发布新文章

| 项 | 值 |
|---|---|
| 子命令 | `create-article` |
| Method | POST |
| Path | `/api/articles` |
| Body | `ArticleCreate`（见 schemas.md） |

**Body 字段**：`title`(str,必填), `content`(str,必填), `uid`(int,默认1), `lid`(int,默认1), `img`(str,可选), `heat`(int,默认0)
**响应**：`{"code":200,"message":"文章发布成功","data":{"id":3}}`

### 1.5 PUT /api/articles/{id} — 更新文章

| 项 | 值 |
|---|---|
| 子命令 | `update-article` |
| Method | PUT |
| Path | `/api/articles/{article_id}` |
| Path 参数 | `article_id`(int,必填) |
| Body | `ArticleUpdate`（见 schemas.md） |

**Body 字段**：`title`(str,可选), `content`(str,可选), `lid`(int,可选), `img`(str,可选), `heat`(int,可选)。至少传一个字段。
**响应**：`{"code":200,"message":"文章更新成功"}`

### 1.6 DELETE /api/articles/{id} — 删除文章

| 项 | 值 |
|---|---|
| 子命令 | `delete-article` |
| Method | DELETE |
| Path | `/api/articles/{article_id}` |
| Path 参数 | `article_id`(int,必填) |
| Query | `soft`(bool,默认true。true=软删除deleted=1，false=硬删除) |

**响应**：`{"code":200,"message":"文章已删除"}`

### 1.7 POST /api/articles/{id}/restore — 恢复软删除的文章

| 项 | 值 |
|---|---|
| 子命令 | `restore-article` |
| Method | POST |
| Path | `/api/articles/{article_id}/restore` |
| Path 参数 | `article_id`(int,必填) |

**响应**：`{"code":200,"message":"文章已恢复"}`

---

## 模块 2：Comments（评论，3 端点）

### 2.1 POST /api/comments — 发表评论

| 项 | 值 |
|---|---|
| 子命令 | `create-comment` |
| Method | POST |
| Path | `/api/comments` |
| Body | `CommentCreate`（见 schemas.md） |

**Body 字段**：`uid`(int,必填), `aid`(int,必填), `content`(str,必填)
**响应**：`{"code":200,"data":{"id":1}}`

### 2.2 GET /api/comments/{aid} — 获取文章评论列表

| 项 | 值 |
|---|---|
| 子命令 | `list-comments` |
| Method | GET |
| Path | `/api/comments/{aid}` |
| Path 参数 | `aid`(int,必填,文章 ID) |

**响应**：`{"code":200,"data":[{"id":1,"uid":1,"aid":3,"content":"...","deleted":0,"createtime":"...","uname":"admin","img":"img/moren.jpg"}]}`

### 2.3 DELETE /api/comments/{id} — 删除评论（软删除）

| 项 | 值 |
|---|---|
| 子命令 | `delete-comment` |
| Method | DELETE |
| Path | `/api/comments/{comment_id}` |
| Path 参数 | `comment_id`(int,必填) |

**响应**：`{"code":200,"message":"评论已删除"}`

---

## 模块 3：Labels（标签，2 端点）

> ⚠️ 端点实际路径为 `/api/lables`（原项目拼写，API 已固化）。子命令用正确拼写 `labels`，脚本内部请求时用 API 实际路径 `/api/lables`。

### 3.1 GET /api/lables — 获取所有标签

| 项 | 值 |
|---|---|
| 子命令 | `list-labels` |
| Method | GET |
| Path | `/api/lables`（实际路径，注意拼写） |

**响应**：`{"code":200,"data":[{"id":1,"lname":"技术"},{"id":2,"lname":"生活"}]}`

### 3.2 POST /api/lables — 创建标签

| 项 | 值 |
|---|---|
| 子命令 | `create-label` |
| Method | POST |
| Path | `/api/lables`（实际路径，注意拼写） |
| Body | `LableCreate`（见 schemas.md） |

**Body 字段**：`lname`(str,必填)
**响应**：`{"code":200,"data":{"id":5,"lname":"测试标签"}}`

---

## 模块 4：Messages（留言，4 端点）

### 4.1 GET /api/messages — 获取留言列表（含回复）

| 项 | 值 |
|---|---|
| 子命令 | `list-messages` |
| Method | GET |
| Path | `/api/messages` |

**响应**：`{"code":200,"data":[{"id":1,"uid":1,"content":"...","deleted":0,"createtime":"...","uname":"admin","img":"...","replies":[{...}]}]}`

### 4.2 POST /api/messages — 发表留言

| 项 | 值 |
|---|---|
| 子命令 | `create-message` |
| Method | POST |
| Path | `/api/messages` |
| Body | `MessageCreate`（见 schemas.md） |

**Body 字段**：`uid`(int,必填), `content`(str,必填)
**响应**：`{"code":200,"data":{"id":1}}`

### 4.3 POST /api/messages/reply — 回复留言

| 项 | 值 |
|---|---|
| 子命令 | `reply-message` |
| Method | POST |
| Path | `/api/messages/reply` |
| Body | `Message2Create`（见 schemas.md） |

**Body 字段**：`uid`(int,必填), `mid`(int,必填,被回复的留言 ID), `content`(str,必填)
**响应**：`{"code":200,"data":{"id":1}}`

### 4.4 DELETE /api/messages/{id} — 删除留言（软删除）

| 项 | 值 |
|---|---|
| 子命令 | `delete-message` |
| Method | DELETE |
| Path | `/api/messages/{message_id}` |
| Path 参数 | `message_id`(int,必填) |

**响应**：`{"code":200,"message":"留言已删除"}`

---

## 模块 5：Moods（说说/心情，3 端点）

### 5.1 GET /api/moods — 获取说说列表

| 项 | 值 |
|---|---|
| 子命令 | `list-moods` |
| Method | GET |
| Path | `/api/moods` |

**响应**：`{"code":200,"data":[{"id":1,"title":"","content":"...","src":"","createtime":"..."}]}`

### 5.2 POST /api/moods — 发布说说

| 项 | 值 |
|---|---|
| 子命令 | `create-mood` |
| Method | POST |
| Path | `/api/moods` |
| Body | `MoodCreate`（见 schemas.md） |

**Body 字段**：`content`(str,必填), `title`(str,默认""), `src`(str,默认"")
**响应**：`{"code":200,"data":{"id":1}}`

### 5.3 DELETE /api/moods/{id} — 删除说说

| 项 | 值 |
|---|---|
| 子命令 | `delete-mood` |
| Method | DELETE |
| Path | `/api/moods/{mood_id}` |
| Path 参数 | `mood_id`(int,必填) |

**说明**：硬删除（不可恢复）。
**响应**：`{"code":200,"message":"说说已删除"}`

---

## 模块 6：Uploads（文件上传，4 端点）

> 支持的文件扩展名：图片(.jpg/.jpeg/.png/.gif/.webp/.bmp/.svg)、视频(.mp4/.webm/.ogg/.mov/.avi/.mkv)、文档(.pdf/.doc/.docx/.txt/.zip/.tar/.gz/.md)

### 6.1 POST /api/upload — 上传单个文件

| 项 | 值 |
|---|---|
| 子命令 | `upload-file` |
| Method | POST |
| Path | `/api/upload` |
| Content-Type | `multipart/form-data` |
| Form 字段 | `file`(file,必填,单文件) |

**响应**：`{"code":200,"data":{"url":"/uploads/xxx.png","filename":"原文件名.png","type":"image","size":12345}}`

### 6.2 POST /api/upload/multiple — 批量上传文件

| 项 | 值 |
|---|---|
| 子命令 | `upload-files` |
| Method | POST |
| Path | `/api/upload/multiple` |
| Content-Type | `multipart/form-data` |
| Form 字段 | `files`(file[],必填,多文件) |

**响应**：`{"code":200,"data":[{"url":"...","filename":"...","type":"image","size":123},...]}`

### 6.3 GET /api/uploads/list — 列出所有已上传文件

| 项 | 值 |
|---|---|
| 子命令 | `list-uploads` |
| Method | GET |
| Path | `/api/uploads/list` |

**响应**：`{"code":200,"data":[{"filename":"xxx.png","url":"/uploads/xxx.png","type":"image","size":12345}]}`

### 6.4 DELETE /api/uploads/{filename} — 删除已上传文件

| 项 | 值 |
|---|---|
| 子命令 | `delete-upload` |
| Method | DELETE |
| Path | `/api/uploads/{filename}` |
| Path 参数 | `filename`(str,必填,文件名) |

**响应**：`{"code":200,"message":"文件已删除"}`

---

## 模块 7：Users（用户，2 端点）

### 7.1 GET /api/users — 获取用户列表

| 项 | 值 |
|---|---|
| 子命令 | `list-users` |
| Method | GET |
| Path | `/api/users` |

**响应**：`{"code":200,"data":[{"id":1,"uname":"admin","phone":"admin","img":"img/moren.jpg","email":"admin@blog.com","address":"","profession":"","createtime":"..."}]}`

### 7.2 POST /api/users — 创建用户

| 项 | 值 |
|---|---|
| 子命令 | `create-user` |
| Method | POST |
| Path | `/api/users` |
| Body | `UserCreate`（见 schemas.md） |

**Body 字段**：`uname`(str,必填), `phone`(str,默认""), `pwd`(str,默认""), `email`(str,默认""), `img`(str,默认"img/moren.jpg")
**响应**：`{"code":200,"data":{"id":2}}`

---

## 模块 8：Admin（后台管理，3 端点）

> 后台管理使用 session token 认证（非 API 无认证）。默认账号 admin/admin。先调 `admin-login` 获取 token，后续操作携带 token。

### 8.1 POST /admin/login — 后台登录

| 项 | 值 |
|---|---|
| 子命令 | `admin-login` |
| Method | POST |
| Path | `/admin/login` |
| Content-Type | `application/x-www-form-urlencoded` |
| Form 字段 | `username`(str,必填), `password`(str,必填) |

**说明**：登录成功返回 302 重定向 + `Set-Cookie: admin_token=<token>`。脚本自动提取 token 返回。
**响应**：`{"code":200,"data":{"token":"467413ed48aa3394ba442e0613e5ba18"},"message":"登录成功"}`
**失败**：`{"code":401,"message":"账号或密码错误"}`

### 8.2 GET /admin/logout — 退出登录

| 项 | 值 |
|---|---|
| 子命令 | `admin-logout` |
| Method | GET |
| Path | `/admin/logout` |
| Query | `t`(str,必填,登录 token) |

**响应**：`{"code":200,"message":"已退出登录"}`

### 8.3 POST /admin/api/delete — 后台批量删除文章

| 项 | 值 |
|---|---|
| 子命令 | `admin-delete-articles` |
| Method | POST |
| Path | `/admin/api/delete` |
| Body | `{"token":"<token>","ids":[1,2,3]}` |

**说明**：需先登录获取 token。硬删除（不可恢复）。
**响应**：`{"code":200,"deleted":2,"message":"成功删除 2 篇文章"}`
**未登录**：`{"code":401,"message":"未登录或登录已过期"}`

---

## 补充端点

### GET /health — 健康检查

| 项 | 值 |
|---|---|
| 子命令 | `health-check` |
| Method | GET |
| Path | `/health` |

**响应**：`{"status":"ok","service":"blog-api","version":"1.0.0"}`

> 页面渲染端点（GET /, GET /article/{id}, GET /admin）返回 HTML，非 API 端点，已排除。

---

## 端点总数统计

| 模块 | 端点数 |
|---|---|
| Articles | 7 |
| Comments | 3 |
| Labels | 2 |
| Messages | 4 |
| Moods | 3 |
| Uploads | 4 |
| Users | 2 |
| Admin | 3 |
| **合计** | **28** |
