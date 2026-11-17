# Blog System API 端点文档（总索引）

> Blog System (FastAPI) · v1.0.0 · 无认证公开 API · 共 32 个端点
>
> 所有路径相对于 `{base_url}`（配置方式见 SKILL.md Configuration 段落）。
> OpenAPI 文档：`{base_url}/openapi.json` · Swagger UI：`{base_url}/docs`

## 端点分类索引（10 类 / 32 端点）

| 分类 | 文档 | 端点数 | 端点概览 |
|------|------|--------|----------|
| 文章 | [articles.md](articles.md) | 7 | 列表/详情/创建/更新/删除/恢复/热门 |
| 标签 | [tags.md](tags.md) | 2 | 列表/创建 |
| 用户 | [users.md](users.md) | 2 | 列表/创建 |
| 评论 | [comments.md](comments.md) | 3 | 创建/列表/删除 |
| 留言 | [messages.md](messages.md) | 4 | 列表/创建/回复/删除 |
| 说说 | [moods.md](moods.md) | 3 | 列表/创建/删除 |
| 文件上传 | [uploads.md](uploads.md) | 4 | 单传/批传/列表/删除 |
| 健康检查 | [health.md](health.md) | 1 | 健康状态 |
| 博客页面 | [pages.md](pages.md) | 2 | 首页/文章详情（HTML） |
| 后台管理 | [admin.md](admin.md) | 4 | 页面/登录/登出/批量删除 |

## 全量端点表

| # | Method | Path | 子命令 | 说明 |
|---|--------|------|--------|------|
| 1 | GET | /api/articles | list-articles | 分页查询文章列表 |
| 2 | POST | /api/articles | create-article | 发布新文章 |
| 3 | GET | /api/articles/{article_id} | get-article | 文章详情（含评论） |
| 4 | PUT | /api/articles/{article_id} | update-article | 更新文章 |
| 5 | DELETE | /api/articles/{article_id} | delete-article | 删除文章（软/硬） |
| 6 | POST | /api/articles/{article_id}/restore | restore-article | 恢复软删除文章 |
| 7 | GET | /api/articles/heat/top | top-articles | 热门文章 Top N |
| 8 | GET | /api/lables | list-labels | 获取所有标签 |
| 9 | POST | /api/lables | create-label | 创建标签 |
| 10 | GET | /api/users | list-users | 获取用户列表 |
| 11 | POST | /api/users | create-user | 创建用户 |
| 12 | POST | /api/comments | create-comment | 发表评论 |
| 13 | GET | /api/comments/{aid} | list-comments | 文章评论列表 |
| 14 | DELETE | /api/comments/{comment_id} | delete-comment | 删除评论（软删除） |
| 15 | GET | /api/messages | list-messages | 留言列表（含回复） |
| 16 | POST | /api/messages | create-message | 发表留言 |
| 17 | POST | /api/messages/reply | reply-message | 回复留言 |
| 18 | DELETE | /api/messages/{message_id} | delete-message | 删除留言（软删除） |
| 19 | GET | /api/moods | list-moods | 说说列表 |
| 20 | POST | /api/moods | create-mood | 发布说说 |
| 21 | DELETE | /api/moods/{mood_id} | delete-mood | 删除说说 |
| 22 | POST | /api/upload | upload-file | 上传单个文件 |
| 23 | POST | /api/upload/multiple | upload-files | 批量上传文件 |
| 24 | GET | /api/uploads/list | list-uploads | 列出已上传文件 |
| 25 | DELETE | /api/uploads/{filename} | delete-upload | 删除已上传文件 |
| 26 | GET | /health | health-check | 健康检查 |
| 27 | GET | / | blog-home | 博客首页（HTML） |
| 28 | GET | /article/{article_id} | blog-article | 文章详情页（HTML） |
| 29 | GET | /admin | admin-page | 后台管理页面（HTML） |
| 30 | POST | /admin/login | admin-login | 后台登录（获取 token） |
| 31 | GET | /admin/logout | admin-logout | 退出后台登录 |
| 32 | POST | /admin/api/delete | admin-delete-articles | 后台批量删除文章 |

## 通用响应格式

所有 JSON API 端点统一返回：

```json
{"code": 200, "data": ..., "message": "..."}
```

- `code`：200=成功，400=参数错误，401=未授权（后台），404=资源不存在
- `data`：业务数据（对象/数组/ID）
- `message`：操作结果描述（写操作返回）

## 认证说明

- 端点 1-26：**无认证**（公开 API，直接调用）
- 端点 27-29：HTML 页面，浏览器访问
- 端点 30-32：**后台管理**，需先 `admin-login` 获取 token（默认账号 admin/admin，以实际部署为准）

## 拼写说明

API 路径 `/api/lables` 为原系统拼写（labels 误写为 lables）。子命令使用正确拼写 `labels`，脚本内部请求时使用 API 实际路径 `lables`。
