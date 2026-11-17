# 评论 API（3 端点）

路径前缀：`{base_url}` · 无认证

## 1. POST /api/comments — 发表评论

**子命令**：`create-comment`

Body（JSON，`CommentCreate`）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uid | int | 是 | 用户 ID |
| aid | int | 是 | 文章 ID |
| content | string | 是 | 评论内容 |

```bash
curl -s --max-time 30 -X POST -H "Content-Type: application/json" \
  -d '{"uid":1,"aid":1,"content":"好文章"}' "{base_url}/api/comments"
```

响应：`{"code":200,"data":{"id":3}}`

## 2. GET /api/comments/{aid} — 文章评论列表

**子命令**：`list-comments`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| aid | path | int | 是 | 文章 ID |

响应：
```json
{"code":200,"data":[{"id":1,"uid":1,"aid":1,"content":"好文章","deleted":0,"uname":"admin","img":"img/moren.jpg","createtime":"2026-08-25T03:00:00"}]}
```

## 3. DELETE /api/comments/{comment_id} — 删除评论

**子命令**：`delete-comment`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| comment_id | path | int | 是 | 评论 ID |

> 软删除（deleted=1），不可恢复。

响应：`{"code":200,"message":"评论已删除"}`
