# 数据模型 Schema — blog-mini-ljt

> 8 个请求体数据模型，字段表含：字段 / 类型 / 必填 / 默认值 / 说明。
> 字段定义来源于 `blog_api.py` 的 Pydantic BaseModel，与线上 API 一致。

## 1. ArticleCreate — 发布文章

用于 `POST /api/articles`（子命令 `create-article`）。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 是 | — | 文章标题 |
| content | string | 是 | — | 文章内容（支持 HTML） |
| uid | int | 否 | 1 | 作者用户 ID |
| lid | int | 否 | 1 | 标签 ID |
| img | string | 否 | null | 封面图 URL |
| heat | int | 否 | 0 | 热度初始值 |

**示例**：
```json
{"title":"我的第一篇博客","content":"<p>Hello World</p>","uid":1,"lid":1,"img":"/uploads/cover.png","heat":0}
```

## 2. ArticleUpdate — 更新文章

用于 `PUT /api/articles/{id}`（子命令 `update-article`）。所有字段可选，至少传一个。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 否 | null | 新标题 |
| content | string | 否 | null | 新内容（支持 HTML） |
| lid | int | 否 | null | 新标签 ID |
| img | string | 否 | null | 新封面图 URL |
| heat | int | 否 | null | 新热度值 |

**示例**：
```json
{"title":"更新后的标题","heat":10}
```

## 3. LableCreate — 创建标签

用于 `POST /api/lables`（子命令 `create-label`，端点实际路径 `/api/lables`）。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| lname | string | 是 | — | 标签名称 |

**示例**：
```json
{"lname":"前端"}
```

## 4. UserCreate — 创建用户

用于 `POST /api/users`（子命令 `create-user`）。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uname | string | 是 | — | 用户名 |
| phone | string | 否 | "" | 手机号 |
| pwd | string | 否 | "" | 密码 |
| email | string | 否 | "" | 邮箱 |
| img | string | 否 | "img/moren.jpg" | 头像 URL |

**示例**：
```json
{"uname":"alice","phone":"13800000000","pwd":"secret","email":"alice@example.com"}
```

## 5. CommentCreate — 发表评论

用于 `POST /api/comments`（子命令 `create-comment`）。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | int | 是 | — | 评论者用户 ID |
| aid | int | 是 | — | 文章 ID |
| content | string | 是 | — | 评论内容 |

**示例**：
```json
{"uid":1,"aid":3,"content":"写得不错！"}
```

## 6. MessageCreate — 发表留言

用于 `POST /api/messages`（子命令 `create-message`）。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | int | 是 | — | 留言者用户 ID |
| content | string | 是 | — | 留言内容 |

**示例**：
```json
{"uid":1,"content":"欢迎访问我的博客！"}
```

## 7. Message2Create — 回复留言

用于 `POST /api/messages/reply`（子命令 `reply-message`）。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | int | 是 | — | 回复者用户 ID |
| mid | int | 是 | — | 被回复的留言 ID |
| content | string | 是 | — | 回复内容 |

**示例**：
```json
{"uid":2,"mid":1,"content":"谢谢留言！"}
```

## 8. MoodCreate — 发布说说

用于 `POST /api/moods`（子命令 `create-mood`）。

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 否 | "" | 标题 |
| content | string | 是 | — | 说说内容 |
| src | string | 否 | "" | 来源/配图 URL |

**示例**：
```json
{"content":"今天天气真好","title":"日常","src":"/uploads/sun.png"}
```

---

## Schema 汇总

| # | 模型 | 用途 | 必填字段 |
|---|------|------|----------|
| 1 | ArticleCreate | 发布文章 | title, content |
| 2 | ArticleUpdate | 更新文章 | （无，至少传一个） |
| 3 | LableCreate | 创建标签 | lname |
| 4 | UserCreate | 创建用户 | uname |
| 5 | CommentCreate | 发表评论 | uid, aid, content |
| 6 | MessageCreate | 发表留言 | uid, content |
| 7 | Message2Create | 回复留言 | uid, mid, content |
| 8 | MoodCreate | 发布说说 | content |
