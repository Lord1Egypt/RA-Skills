# Blog System REST API Reference

API base_url: `{base_url}` (无认证)

## Endpoints

### Health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | 健康检查 |

### Articles
| Method | Path | Parameters | Body | Description |
|--------|------|------------|------|-------------|
| GET | /api/articles | page(optional, int), size(optional, int), lid(optional, int), keyword(optional, string) | — | 分页查询文章列表 |
| POST | /api/articles | — | ArticleCreate | 发布新文章 |
| GET | /api/articles/{article_id} | article_id(path, int) | — | 查询文章详情 |
| PUT | /api/articles/{article_id} | article_id(path, int) | ArticleUpdate | 更新文章 |
| DELETE | /api/articles/{article_id} | article_id(path, int), soft(optional, bool) | — | 删除文章（支持软删除） |
| POST | /api/articles/{article_id}/restore | article_id(path, int) | — | 恢复已软删除的文章 |
| GET | /api/articles/heat/top | limit(optional, int) | — | 获取热门文章排行 |

### Labels
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/lables | — | 查询标签列表 |
| POST | /api/lables | LableCreate | 创建新标签 |

### Users
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/users | — | 查询用户列表 |
| POST | /api/users | UserCreate | 创建新用户 |

### Comments
| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /api/comments | CommentCreate | 创建评论 |
| GET | /api/comments/{aid} | — | 查询文章评论列表 |
| DELETE | /api/comments/{comment_id} | — | 删除评论 |

### Messages
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/messages | — | 查询留言列表 |
| POST | /api/messages | MessageCreate | 创建留言 |
| POST | /api/messages/reply | Message2Create | 回复留言 |
| DELETE | /api/messages/{message_id} | — | 删除留言 |

### Moods
| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /api/moods | — | 查询说说列表 |
| POST | /api/moods | MoodCreate | 创建说说 |
| DELETE | /api/moods/{mood_id} | — | 删除说说 |

### File Upload
| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /api/upload | multipart/form-data (file) | 单文件上传 |
| POST | /api/upload/multiple | multipart/form-data (files) | 批量文件上传 |
| GET | /api/uploads/list | — | 查询上传文件列表 |
| DELETE | /api/uploads/{filename} | — | 删除上传文件 |

### Admin
| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | /admin/api/delete | — | 批量删除文章 |

## Request Body Schemas

### ArticleCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | ✅ | 文章标题 |
| content | string | ✅ | 文章内容 |
| uid | integer | | 用户 ID |
| lid | integer | | 标签 ID |
| img | unknown | | 文章图片 |
| heat | integer | | 热度值 |

### ArticleUpdate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | unknown | | 文章标题 |
| content | unknown | | 文章内容 |
| lid | unknown | | 标签 ID |
| img | unknown | | 文章图片 |
| heat | unknown | | 热度值 |

### LableCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| lname | string | ✅ | 标签名称 |

### UserCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| uname | string | ✅ | 用户名 |
| phone | string | | 手机号 |
| pwd | string | | 密码 |
| email | string | | 邮箱 |
| img | string | | 头像 |

### CommentCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| uid | integer | ✅ | 用户 ID |
| aid | integer | ✅ | 文章 ID |
| content | string | ✅ | 评论内容 |

### MessageCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| uid | integer | ✅ | 用户 ID |
| content | string | ✅ | 留言内容 |

### Message2Create (Reply)
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| uid | integer | ✅ | 用户 ID |
| mid | integer | ✅ | 被回复的留言 ID |
| content | string | ✅ | 回复内容 |

### MoodCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | | 说说标题 |
| content | string | ✅ | 说说内容 |
| src | string | | 来源 |