# blog-big-kimi-kit API 端点文档

> 基于 OpenAPI 3.1.0 文档自动生成。所有端点相对于 `{base_url}`。
> 公开 API（无认证）。

## Base URL

```
{base_url}
```

## 认证方式

无认证（公开 API），不需要 Header 或凭据。

## 端点列表

### 健康检查

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| GET | /health | 健康检查 | - |

### 文章

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| GET | /api/articles | 查询文章列表 | page(query,int,default=1), size(query,int,default=10,max=100), lid(query,int,default=0), keyword(query,string,default="") |
| POST | /api/articles | 创建文章 | body: ArticleCreate |
| GET | /api/articles/{article_id} | 查询文章详情 | article_id(path,int,required) |
| PUT | /api/articles/{article_id} | 更新文章 | article_id(path,int,required), body: ArticleUpdate |
| DELETE | /api/articles/{article_id} | 删除文章 | article_id(path,int,required), soft(query,bool,default=true) |
| GET | /api/articles/heat/top | 查询热门文章 | limit(query,int,default=5,max=20) |
| POST | /api/articles/{article_id}/restore | 恢复已删除文章 | article_id(path,int,required) |

### 标签

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| GET | /api/lables | 查询标签列表 | - |
| POST | /api/lables | 创建标签 | body: LableCreate |

> ⚠️ API 路径实际拼写为 `/api/lables`（非 labels）。

### 用户

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| GET | /api/users | 查询用户列表 | - |
| POST | /api/users | 创建用户 | body: UserCreate |

### 评论

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| GET | /api/comments/{aid} | 查询文章评论列表 | aid(path,int,required) |
| POST | /api/comments | 创建评论 | body: CommentCreate |
| DELETE | /api/comments/{comment_id} | 删除评论 | comment_id(path,int,required) |

### 留言

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| GET | /api/messages | 查询留言列表 | - |
| POST | /api/messages | 创建留言 | body: MessageCreate |
| POST | /api/messages/reply | 回复留言 | body: Message2Create |
| DELETE | /api/messages/{message_id} | 删除留言 | message_id(path,int,required) |

### 说说

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| GET | /api/moods | 查询说说列表 | - |
| POST | /api/moods | 创建说说 | body: MoodCreate |
| DELETE | /api/moods/{mood_id} | 删除说说 | mood_id(path,int,required) |

### 文件上传

| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| POST | /api/upload | 上传单个文件 | multipart: file(required) |
| POST | /api/upload/multiple | 批量上传文件 | multipart: files(required, array) |
| GET | /api/uploads/list | 查询已上传文件列表 | - |
| DELETE | /api/uploads/{filename} | 删除已上传文件 | filename(path,string,required) |

## 数据模型

### ArticleCreate
```json
{
  "title": "string (required)",
  "content": "string (required)",
  "uid": "integer (default=1)",
  "lid": "integer (default=1)",
  "img": "string|null (optional)",
  "heat": "integer (default=0)"
}
```

### ArticleUpdate
```json
{
  "title": "string|null (optional)",
  "content": "string|null (optional)",
  "lid": "integer|null (optional)",
  "img": "string|null (optional)",
  "heat": "integer|null (optional)"
}
```

### LableCreate
```json
{
  "lname": "string (required)"
}
```

### UserCreate
```json
{
  "uname": "string (required)",
  "phone": "string (default=\"\")",
  "pwd": "string (default=\"\")",
  "email": "string (default=\"\")",
  "img": "string (default=\"img/moren.jpg\")"
}
```

### CommentCreate
```json
{
  "uid": "integer (required)",
  "aid": "integer (required)",
  "content": "string (required)"
}
```

### MessageCreate
```json
{
  "uid": "integer (required)",
  "content": "string (required)"
}
```

### Message2Create（回复留言）
```json
{
  "uid": "integer (required)",
  "mid": "integer (required)",
  "content": "string (required)"
}
```

### MoodCreate
```json
{
  "title": "string (default=\"\")",
  "content": "string (required)",
  "src": "string (default=\"\")"
}
```

## 响应结构

### 列表响应
```json
{
  "code": 200,
  "data": [...],
  "total": N,
  "page": 1,
  "size": 10
}
```

### 文章详情响应
```json
{
  "code": 200,
  "data": {
    "article": {...},
    "comments": [...]
  }
}
```

### 健康检查响应
```json
{
  "status": "ok",
  "service": "blog-api",
  "version": "1.0.0"
}
```
