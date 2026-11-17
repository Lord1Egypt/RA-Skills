# Blog System API v1.0.0 端点文档

> 来源：OpenAPI 文档自动解析 + curl 真实探测验证。
> Base URL：运行时动态获取（项目知识 / `BLOG_TOOLKIT_BASE_URL` 环境变量 / 交互输入）
> 认证方式：无认证（公开 API）
> 响应信封：列表/对象类端点统一 `{"code":200,"data":...}`；健康检查 `{"status":"ok",...}`；错误 `{"detail":"..."}`

## 文章管理

### 1. GET /api/articles — 分页查询文章列表
- 参数（query）：`page`(int,默认1)、`size`(int,默认10,最大100)、`lid`(int,默认0,标签筛选)、`keyword`(str,默认"")
- 响应：`{"code":200,"data":[{id,img,uid,title,lid,content,heat,deleted,createtime,uname,lname}]}`
- 子命令：`list-articles`

### 2. POST /api/articles — 发布新文章
- 参数（body）：`title*(str)`、`content*(str)`、`uid(int,默认1)`、`lid(int,默认1)`、`img(str|null)`、`heat(int,默认0)`
- 响应：`{"code":200,"data":{id,...}}`
- 子命令：`create-article`

### 3. GET /api/articles/{article_id} — 查询单篇文章详情（含评论）
- 参数（path）：`article_id*(int)`
- 响应：`{"code":200,"data":{"article":{id,img,uid,title,lid,content,heat,deleted,createtime,uname,lname},"comments":[...]}}`
- 子命令：`get-article`

### 4. PUT /api/articles/{article_id} — 更新文章
- 参数（path）：`article_id*(int)`；（body）：`title(str|null)`、`content(str|null)`、`lid(int|null)`、`img(str|null)`、`heat(int|null)`
- 响应：`{"code":200,"data":{...}}`
- 子命令：`update-article`

### 5. DELETE /api/articles/{article_id} — 删除文章
- 参数（path）：`article_id*(int)`；（query）：`soft(bool,默认true)`，soft=false 硬删除
- 响应：`{"code":200,"data":{...}}`
- 子命令：`delete-article`

### 6. POST /api/articles/{article_id}/restore — 恢复软删除的文章
- 参数（path）：`article_id*(int)`
- 响应：`{"code":200,"data":{...}}`
- 子命令：`restore-article`

### 7. GET /api/articles/heat/top — 获取热门文章 Top N
- 参数（query）：`limit(int,默认5,范围1-20)`
- 响应：`{"code":200,"data":[{id,title,heat}]}`
- 子命令：`top-articles`

## 标签管理

> API 路径拼写为 `/api/lables`（原文如此），子命令使用正确拼写 `labels`。

### 8. GET /api/lables — 获取所有标签
- 参数：无
- 响应：`{"code":200,"data":[{id,lname}]}`
- 子命令：`list-labels`

### 9. POST /api/lables — 创建标签
- 参数（body）：`lname*(str)`
- 响应：`{"code":200,"data":{id,lname}}`
- 子命令：`create-label`

## 用户管理

### 10. GET /api/users — 获取用户列表
- 参数：无
- 响应：`{"code":200,"data":[{id,uname,phone,img,email,address,profession,createtime}]}`
- 子命令：`list-users`

### 11. POST /api/users — 创建用户
- 参数（body）：`uname*(str)`、`phone(str,默认"")`、`pwd(str,默认"")`、`email(str,默认"")`、`img(str,默认"img/moren.jpg")`
- 响应：`{"code":200,"data":{id,...}}`
- 子命令：`create-user`

## 评论管理

### 12. GET /api/comments/{aid} — 获取文章的评论列表
- 参数（path）：`aid*(int)`
- 响应：`{"code":200,"data":[{id,uid,aid,content,deleted,createtime,uname,img}]}`
- 子命令：`list-comments`

### 13. POST /api/comments — 发表评论
- 参数（body）：`uid*(int)`、`aid*(int)`、`content*(str)`
- 响应：`{"code":200,"data":{id,...}}`
- 子命令：`create-comment`

### 14. DELETE /api/comments/{comment_id} — 删除评论（软删除）
- 参数（path）：`comment_id*(int)`
- 响应：`{"code":200,"data":{...}}`
- 子命令：`delete-comment`

## 留言管理

### 15. GET /api/messages — 获取留言列表（含回复）
- 参数：无
- 响应：`{"code":200,"data":[{id,uid,content,deleted,createtime,uname,img,replies:[...]}]}`
- 子命令：`list-messages`

### 16. POST /api/messages — 发表留言
- 参数（body）：`uid*(int)`、`content*(str)`
- 响应：`{"code":200,"data":{id,...}}`
- 子命令：`create-message`

### 17. POST /api/messages/reply — 回复留言
- 参数（body）：`uid*(int)`、`mid*(int)`、`content*(str)`
- 响应：`{"code":200,"data":{id,...}}`
- 子命令：`reply-message`

### 18. DELETE /api/messages/{message_id} — 删除留言（软删除）
- 参数（path）：`message_id*(int)`
- 响应：`{"code":200,"data":{...}}`
- 子命令：`delete-message`

## 说说管理

### 19. GET /api/moods — 获取说说列表
- 参数：无
- 响应：`{"code":200,"data":[{id,title,content,src,createtime}]}`
- 子命令：`list-moods`

### 20. POST /api/moods — 发布说说
- 参数（body）：`title(str,默认"")`、`content*(str)`、`src(str,默认"")`
- 响应：`{"code":200,"data":{id,...}}`
- 子命令：`create-mood`

### 21. DELETE /api/moods/{mood_id} — 删除说说
- 参数（path）：`mood_id*(int)`
- 响应：`{"code":200,"data":{...}}`
- 子命令：`delete-mood`

## 文件上传

### 22. POST /api/upload — 上传单个文件
- 参数（multipart/form-data）：`file*(binary)`
- 响应：`{"code":200,"data":{"url":"/uploads/{hash文件名}","filename":"原始文件名","type":"...","size":N}}`
- 子命令：`upload-file`（脚本用 `files=` 参数）
- 注意：返回 `filename` 为原始文件名；存储文件名（hash）在 `url` 字段路径末段，删除时使用该 hash 文件名

### 23. POST /api/upload/multiple — 批量上传文件
- 参数（multipart/form-data）：`files*(array[binary])`
- 响应：`{"code":200,"data":[{"url":"/uploads/{hash文件名}","filename":"原始文件名",...}]}`
- 子命令：`upload-files`（脚本用 `files=` 参数）
- 注意：删除时使用 `url` 字段路径末段的 hash 文件名

### 24. GET /api/uploads/list — 列出所有已上传文件
- 参数：无
- 响应：`{"code":200,"data":[{filename,url,type,size}]}`
- 子命令：`list-uploads`
- 注意：列表项的 `filename` 即存储文件名（hash），可直接用于 delete-upload

### 25. DELETE /api/uploads/{filename} — 删除已上传文件
- 参数（path）：`filename*(str)` — 存储文件名（hash，即 upload 返回 `data.url` 路径末段，或 list-uploads 返回的 `filename`）
- 响应：`{"code":200,"message":"文件已删除"}`
- 子命令：`delete-upload`

## 健康检查

### 26. GET /health — 健康检查
- 参数：无
- 响应：`{"status":"ok","service":"blog-api","version":"1.0.0"}`
- 子命令：`health-check`

## 排除端点（Web 页面，非 API）

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | / | 博客首页（HTML 页面） |
| GET | /article/{article_id} | 文章详情页（HTML 页面） |

## 子命令汇总

共 26 个 API 子命令 + 1 个 capability-list = 27 个子命令。
分类：文章 7 / 标签 2 / 用户 2 / 评论 3 / 留言 4 / 说说 3 / 文件上传 4 / 健康检查 1 / capability-list 1。
