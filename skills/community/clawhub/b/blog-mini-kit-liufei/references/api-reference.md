# API Reference — Blog System API

> Base URL: `{base_url}`（解析优先级见 SKILL.md Configuration 段落）
> 认证：无认证（公开 API）
> 所有端点相对 `{base_url}` 路径

## 数据模型（8 个 Schema）

### ArticleCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | ✅ | — | 文章标题 |
| content | string | ✅ | — | 文章内容（支持 HTML） |
| uid | int | ❌ | 1 | 作者用户 ID |
| lid | int | ❌ | 1 | 标签 ID |
| img | string | ❌ | null | 封面图 URL |
| heat | int | ❌ | 0 | 初始热度 |

### ArticleUpdate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | ❌ | null | 新标题 |
| content | string | ❌ | null | 新内容 |
| lid | int | ❌ | null | 新标签 ID |
| img | string | ❌ | null | 新封面图 URL |
| heat | int | ❌ | null | 新热度值 |

### LableCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| lname | string | ✅ | — | 标签名称 |

### UserCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uname | string | ✅ | — | 用户名 |
| phone | string | ❌ | "" | 手机号 |
| pwd | string | ❌ | "" | 密码 |
| email | string | ❌ | "" | 邮箱 |
| img | string | ❌ | img/moren.jpg | 头像路径 |

### CommentCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | int | ✅ | — | 用户 ID |
| aid | int | ✅ | — | 文章 ID |
| content | string | ✅ | — | 评论内容 |

### MessageCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | int | ✅ | — | 用户 ID |
| content | string | ✅ | — | 留言内容 |

### Message2Create
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| uid | int | ✅ | — | 用户 ID |
| mid | int | ✅ | — | 留言 ID（被回复的留言） |
| content | string | ✅ | — | 回复内容 |

### MoodCreate
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | ❌ | "" | 标题 |
| content | string | ✅ | — | 内容 |
| src | string | ❌ | "" | 媒体 URL |

---

## 端点清单（32 个）

### 一、文章 API（7 个）

#### 1. GET /api/articles — 分页查询文章列表

**Query 参数：**
| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| page | int | ❌ | 1 | 页码（≥1） |
| size | int | ❌ | 10 | 每页数量（1-100） |
| lid | int | ❌ | 0 | 标签 ID 筛选（0=不筛选） |
| keyword | string | ❌ | "" | 标题关键词搜索 |

**响应：** `{"code":200,"data":[{...}],"total":N,"page":1,"size":10}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/articles?page=1&size=10&lid=0&keyword="
```

**响应示例：**
```json
{"code":200,"data":[{"id":1,"img":null,"uid":1,"title":"部署测试文章","lid":1,"content":"...","heat":5,"deleted":0,"createtime":"2026-08-24T12:00:00","uname":"admin","lname":"技术"}],"total":1,"page":1,"size":10}
```

#### 2. GET /api/articles/{article_id} — 查询单篇文章详情（含评论）

**Path 参数：** `article_id` (int, 必填) — 文章 ID

**响应：** `{"code":200,"data":{"article":{...},"comments":[{...}]}}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/articles/1"
```

**响应示例：**
```json
{"code":200,"data":{"article":{"id":1,"title":"...","content":"...","heat":6,"uname":"admin","lname":"技术"},"comments":[{"id":1,"uid":1,"aid":1,"content":"不错","uname":"admin","img":"img/moren.jpg"}]}}
```

#### 3. POST /api/articles — 发布新文章

**请求体：** ArticleCreate schema

**响应：** `{"code":200,"message":"文章发布成功","data":{"id":N}}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/articles" \
  -H "Content-Type: application/json" \
  -d '{"title":"我的第一篇博客","content":"Hello World","uid":1,"lid":1,"heat":0}'
```

**响应示例：**
```json
{"code":200,"message":"文章发布成功","data":{"id":2}}
```

#### 4. PUT /api/articles/{article_id} — 更新文章

**Path 参数：** `article_id` (int, 必填)
**请求体：** ArticleUpdate schema（至少一个字段）

**响应：** `{"code":200,"message":"文章更新成功"}`

**curl 示例：**
```bash
curl -s --max-time 30 -X PUT "{base_url}/api/articles/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"更新后的标题","heat":10}'
```

**响应示例：**
```json
{"code":200,"message":"文章更新成功"}
```

#### 5. DELETE /api/articles/{article_id} — 删除文章（支持软删/硬删）

**Path 参数：** `article_id` (int, 必填)
**Query 参数：**
| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| soft | bool | true | true=软删除（标记 deleted=1），false=硬删除（物理删除） |

**响应：** `{"code":200,"message":"文章已删除"}`

**curl 示例（软删除）：**
```bash
curl -s --max-time 30 -X DELETE "{base_url}/api/articles/1?soft=true"
```

**curl 示例（硬删除）：**
```bash
curl -s --max-time 30 -X DELETE "{base_url}/api/articles/1?soft=false"
```

**响应示例：**
```json
{"code":200,"message":"文章已删除"}
```

#### 6. POST /api/articles/{article_id}/restore — 恢复软删除的文章

**Path 参数：** `article_id` (int, 必填)

**响应：** `{"code":200,"message":"文章已恢复"}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/articles/1/restore"
```

**响应示例：**
```json
{"code":200,"message":"文章已恢复"}
```

#### 7. GET /api/articles/heat/top — 获取热门文章 Top N

**Query 参数：**
| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| limit | int | ❌ | 5 | 返回数量（1-20） |

**响应：** `{"code":200,"data":[{"id":N,"title":"...","heat":N},...]}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/articles/heat/top?limit=5"
```

**响应示例：**
```json
{"code":200,"data":[{"id":1,"title":"部署测试文章","heat":10}]}
```

### 二、标签 API（2 个）

#### 8. GET /api/lables — 获取所有标签

**响应：** `{"code":200,"data":[{"id":N,"lname":"..."},...]}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/lables"
```

**响应示例：**
```json
{"code":200,"data":[{"id":1,"lname":"技术"},{"id":2,"lname":"生活"},{"id":3,"lname":"随笔"},{"id":4,"lname":"教程"}]}
```

#### 9. POST /api/lables — 创建标签

**请求体：** LableCreate schema

**响应：** `{"code":200,"data":{"id":N,"lname":"..."}}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/lables" \
  -H "Content-Type: application/json" \
  -d '{"lname":"新标签"}'
```

**响应示例：**
```json
{"code":200,"data":{"id":5,"lname":"新标签"}}
```

### 三、用户 API（2 个）

#### 10. GET /api/users — 获取用户列表

**响应：** `{"code":200,"data":[{"id":N,"uname":"...","phone":"...","img":"...","email":"..."},...]}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/users"
```

**响应示例：**
```json
{"code":200,"data":[{"id":1,"uname":"admin","phone":"admin","img":"img/moren.jpg","email":"admin@blog.com","address":"","profession":"","createtime":"2026-08-24T12:00:00"}]}
```

#### 11. POST /api/users — 创建用户

**请求体：** UserCreate schema

**响应：** `{"code":200,"data":{"id":N}}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/users" \
  -H "Content-Type: application/json" \
  -d '{"uname":"newuser","phone":"13800000000","pwd":"pass123","email":"user@example.com"}'
```

**响应示例：**
```json
{"code":200,"data":{"id":2}}
```

### 四、评论 API（3 个）

#### 12. POST /api/comments — 发表评论

**请求体：** CommentCreate schema

**响应：** `{"code":200,"data":{"id":N}}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/comments" \
  -H "Content-Type: application/json" \
  -d '{"uid":1,"aid":1,"content":"写得好！"}'
```

**响应示例：**
```json
{"code":200,"data":{"id":1}}
```

#### 13. GET /api/comments/{aid} — 获取文章的评论列表

**Path 参数：** `aid` (int, 必填) — 文章 ID

**响应：** `{"code":200,"data":[{"id":N,"uid":N,"aid":N,"content":"...","uname":"...","img":"..."},...]}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/comments/1"
```

**响应示例：**
```json
{"code":200,"data":[{"id":1,"uid":1,"aid":1,"content":"写得好！","deleted":0,"createtime":"2026-08-24T12:00:00","uname":"admin","img":"img/moren.jpg"}]}
```

#### 14. DELETE /api/comments/{comment_id} — 删除评论（软删除）

**Path 参数：** `comment_id` (int, 必填)

**响应：** `{"code":200,"message":"评论已删除"}`

**curl 示例：**
```bash
curl -s --max-time 30 -X DELETE "{base_url}/api/comments/1"
```

**响应示例：**
```json
{"code":200,"message":"评论已删除"}
```

### 五、留言 API（4 个）

#### 15. GET /api/messages — 获取留言列表（含回复）

**响应：** `{"code":200,"data":[{"id":N,"uid":N,"content":"...","uname":"...","img":"...","replies":[{...}]},...]}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/messages"
```

**响应示例：**
```json
{"code":200,"data":[{"id":1,"uid":1,"content":"你好","deleted":0,"createtime":"2026-08-24T12:00:00","uname":"admin","img":"img/moren.jpg","replies":[{"id":1,"uid":1,"mid":1,"content":"回复你好","uname":"admin","img":"img/moren.jpg"}]}]}
```

#### 16. POST /api/messages — 发表留言

**请求体：** MessageCreate schema

**响应：** `{"code":200,"data":{"id":N}}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"uid":1,"content":"你好，博客很好！"}'
```

**响应示例：**
```json
{"code":200,"data":{"id":1}}
```

#### 17. POST /api/messages/reply — 回复留言

**请求体：** Message2Create schema

**响应：** `{"code":200,"data":{"id":N}}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/messages/reply" \
  -H "Content-Type: application/json" \
  -d '{"uid":1,"mid":1,"content":"谢谢你的留言！"}'
```

**响应示例：**
```json
{"code":200,"data":{"id":1}}
```

#### 18. DELETE /api/messages/{message_id} — 删除留言（软删除）

**Path 参数：** `message_id` (int, 必填)

**响应：** `{"code":200,"message":"留言已删除"}`

**curl 示例：**
```bash
curl -s --max-time 30 -X DELETE "{base_url}/api/messages/1"
```

**响应示例：**
```json
{"code":200,"message":"留言已删除"}
```

### 六、说说 API（3 个）

#### 19. GET /api/moods — 获取说说列表

**响应：** `{"code":200,"data":[{"id":N,"title":"...","content":"...","src":"...","createtime":"..."},...]}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/moods"
```

**响应示例：**
```json
{"code":200,"data":[{"id":1,"title":"今日心情","content":"今天天气真好","src":"","createtime":"2026-08-24T12:00:00"}]}
```

#### 20. POST /api/moods — 发布说说

**请求体：** MoodCreate schema

**响应：** `{"code":200,"data":{"id":N}}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/moods" \
  -H "Content-Type: application/json" \
  -d '{"title":"今日心情","content":"今天天气真好","src":""}'
```

**响应示例：**
```json
{"code":200,"data":{"id":1}}
```

#### 21. DELETE /api/moods/{mood_id} — 删除说说

**Path 参数：** `mood_id` (int, 必填)

**响应：** `{"code":200,"message":"说说已删除"}`

**curl 示例：**
```bash
curl -s --max-time 30 -X DELETE "{base_url}/api/moods/1"
```

**响应示例：**
```json
{"code":200,"message":"说说已删除"}
```

### 七、文件上传 API（4 个）

#### 22. POST /api/upload — 上传单个文件

**请求体：** multipart/form-data，字段 `file`（文件）

**允许类型：** .jpg .jpeg .png .gif .webp .bmp .svg .mp4 .webm .ogg .mov .avi .mkv .pdf .doc .docx .txt .zip .tar .gz .md

**响应：** `{"code":200,"data":{"url":"/uploads/xxx","filename":"原始文件名","type":"image|video|file","size":N}}`

**curl 示例（-F 上传）：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/upload" \
  -F "file=@/path/to/image.jpg"
```

**响应示例：**
```json
{"code":200,"data":{"url":"/uploads/abc123def456.jpg","filename":"image.jpg","type":"image","size":102400}}
```

#### 23. POST /api/upload/multiple — 批量上传文件

**请求体：** multipart/form-data，字段 `files`（多文件）

**响应：** `{"code":200,"data":[{"url":"...","filename":"...","type":"...","size":N},...]}`

**curl 示例（-F 批量上传）：**
```bash
curl -s --max-time 30 -X POST "{base_url}/api/upload/multiple" \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.png"
```

**响应示例：**
```json
{"code":200,"data":[{"url":"/uploads/aaa.jpg","filename":"image1.jpg","type":"image","size":51200},{"url":"/uploads/bbb.png","filename":"image2.png","type":"image","size":81920}]}
```

#### 24. GET /api/uploads/list — 列出所有已上传文件

**响应：** `{"code":200,"data":[{"filename":"...","url":"/uploads/...","type":"image|video|file","size":N},...]}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/api/uploads/list"
```

**响应示例：**
```json
{"code":200,"data":[{"filename":"abc123def456.jpg","url":"/uploads/abc123def456.jpg","type":"image","size":102400}]}
```

#### 25. DELETE /api/uploads/{filename} — 删除已上传文件

**Path 参数：** `filename` (string, 必填) — 文件名

**响应：** `{"code":200,"message":"文件已删除"}`

**curl 示例：**
```bash
curl -s --max-time 30 -X DELETE "{base_url}/api/uploads/abc123def456.jpg"
```

**响应示例：**
```json
{"code":200,"message":"文件已删除"}
```

### 八、前端页面（2 个，返回 HTML）

#### 26. GET / — 博客首页

**Query 参数：** page (int, 默认 1), lid (int, 默认 0), keyword (string, 默认 "")

**响应：** HTML 页面（文章列表 + 侧边栏）

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/?page=1&lid=0&keyword="
```

#### 27. GET /article/{article_id} — 文章详情页

**Path 参数：** `article_id` (int, 必填)

**响应：** HTML 页面（文章详情 + 评论）

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/article/1"
```

### 九、后台管理（4 个）

#### 28. GET /admin — 后台管理入口

**Cookie：** admin_token（可选，有效则显示管理页，无效则显示登录页）

**响应：** HTML 页面（登录表单或管理界面）

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/admin"
```

#### 29. POST /admin/login — 后台登录

**请求体：** form-data（username, password）

**默认凭据：** admin / admin

**响应：** 302 重定向到 /admin，Set-Cookie: admin_token=xxx

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/admin/login" \
  -d "username=admin&password=admin"
```

#### 30. GET /admin/logout — 退出登录

**Query 参数：** `t` (string, admin token)

**响应：** 302 重定向到 /admin

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/admin/logout?t=your_token_here"
```

#### 31. POST /admin/api/delete — 后台批量删除文章

**请求体：** JSON `{"ids":[1,2,3],"token":"admin_token"}`

**响应：** `{"code":200,"deleted":N,"message":"成功删除 N 篇文章"}`

**curl 示例：**
```bash
curl -s --max-time 30 -X POST "{base_url}/admin/api/delete" \
  -H "Content-Type: application/json" \
  -d '{"ids":[1,2],"token":"your_admin_token"}'
```

**响应示例：**
```json
{"code":200,"deleted":2,"message":"成功删除 2 篇文章"}
```

### 十、健康检查（1 个）

#### 32. GET /health — 健康检查

**响应：** `{"status":"ok","service":"blog-api","version":"1.0.0"}`

**curl 示例：**
```bash
curl -s --max-time 30 "{base_url}/health"
```

**响应示例：**
```json
{"status":"ok","service":"blog-api","version":"1.0.0"}
```

---

## 端点计数

| 分类 | 数量 | 端点 |
|------|------|------|
| 文章 API | 7 | list/get/create/update/delete/restore/top |
| 标签 API | 2 | list/create |
| 用户 API | 2 | list/create |
| 评论 API | 3 | create/list/delete |
| 留言 API | 4 | list/create/reply/delete |
| 说说 API | 3 | list/create/delete |
| 文件上传 | 4 | upload/multiple-upload/list/delete |
| 前端页面 | 2 | home/article-detail |
| 后台管理 | 4 | admin-page/login/logout/batch-delete |
| 健康检查 | 1 | health |
| **合计** | **32** | |
