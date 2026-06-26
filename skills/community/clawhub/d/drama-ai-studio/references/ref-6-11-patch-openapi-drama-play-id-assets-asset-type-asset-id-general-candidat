> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.11 PATCH /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/comments/{comment_id}/resolve

将指定评论标记为**已解决**。

**路径参数（Path）：**

| 参数          | 必填 | 类型   | 说明 |
|---------------|------|--------|------|
| `play_id`     | 是   | int    | 剧目 ID |
| `asset_type`  | 是   | int    | 资产类型：1 场景、2 角色、3 道具、4 平面、5 其他 |
| `asset_id`    | 是   | string | 资产 ID |
| `cand_id`     | 是   | string | 候选图 ID |
| `comment_id`  | 是   | int    | 评论 ID（与 §6.9/§6.10 返回的 `id` 一致） |

**请求体：** 无（或空 JSON，服务端不读取 body）。

**成功响应结构：**

`data` 为更新后的该条评论对象（`resolved` 为 `true`，并带 `resolved_at`、`resolved_by`）。

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": 1,
    "candidate_id": 10,
    "user_id": 1001,
    "username": "张三",
    "content": "面部光影再柔一点",
    "created_at": "2025-01-01T12:00:00+08:00",
    "resolved": true,
    "resolved_at": "2025-01-01T14:00:00+08:00",
    "resolved_by": 1002
  }
}
```

**错误响应示例：** 候选图或评论不存在、评论数据无效等。

```json
{
  "code": -1,
  "msg": "评论不存在"
}
```
