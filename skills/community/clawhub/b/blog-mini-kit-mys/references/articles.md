# 文章 API（7 端点）

路径前缀：`{base_url}` · 无认证

## 1. GET /api/articles — 分页查询文章列表

**子命令**：`list-articles`

| 参数 | 位置 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|------|
| page | query | int | 否 | 1 | 页码（≥1） |
| size | query | int | 否 | 10 | 每页数量（1-100） |
| lid | query | int | 否 | 0 | 标签 ID 筛选，0=不限 |
| keyword | query | string | 否 | "" | 标题关键词（LIKE 模糊匹配） |

```bash
curl -s --max-time 30 "{base_url}/api/articles?page=1&size=10"
```

响应：
```json
{"code":200,"data":[{"id":4,"title":"...","uid":1,"lid":1,"content":"...","heat":0,"uname":"admin","lname":"技术","createtime":"2026-08-25T02:47:23"}],"total":4,"page":1,"size":10}
```

## 2. POST /api/articles — 发布新文章

**子命令**：`create-article`

Body（JSON，`ArticleCreate`）：

| 字段 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| title | string | 是 | - | 标题 |
| content | string | 是 | - | 内容（支持 HTML） |
| uid | int | 否 | 1 | 作者用户 ID |
| lid | int | 否 | 1 | 标签 ID |
| img | string\|null | 否 | null | 封面图 URL |
| heat | int | 否 | 0 | 热度初始值 |

```bash
curl -s --max-time 30 -X POST -H "Content-Type: application/json" \
  -d '{"title":"新文章","content":"内容"}' "{base_url}/api/articles"
```

响应：`{"code":200,"message":"文章发布成功","data":{"id":5}}`

## 3. GET /api/articles/{article_id} — 文章详情（含评论）

**子命令**：`get-article`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| article_id | path | int | 是 | 文章 ID |

> 调用后文章热度 +1。

响应：`{"code":200,"data":{"article":{...},"comments":[...]}}` · 404 文章不存在

## 4. PUT /api/articles/{article_id} — 更新文章

**子命令**：`update-article`

Body（JSON，`ArticleUpdate`，所有字段可选）：title / content / lid / img / heat

响应：`{"code":200,"message":"文章更新成功"}` · 404 文章不存在 · 400 无更新字段

## 5. DELETE /api/articles/{article_id} — 删除文章

**子命令**：`delete-article`

| 参数 | 位置 | 类型 | 默认 | 说明 |
|------|------|------|------|------|
| article_id | path | int | - | 文章 ID |
| soft | query | bool | true | true=软删除（deleted=1），false=硬删除（DELETE） |

响应：`{"code":200,"message":"文章已删除"}` · 404 文章不存在

## 6. POST /api/articles/{article_id}/restore — 恢复软删除文章

**子命令**：`restore-article`

响应：`{"code":200,"message":"文章已恢复"}` · 404 文章不存在

## 7. GET /api/articles/heat/top — 热门文章 Top N

**子命令**：`top-articles`

| 参数 | 位置 | 类型 | 默认 | 说明 |
|------|------|------|------|------|
| limit | query | int | 5 | 返回数量（1-20） |

响应：`{"code":200,"data":[{"id":1,"title":"...","heat":0}]}`
