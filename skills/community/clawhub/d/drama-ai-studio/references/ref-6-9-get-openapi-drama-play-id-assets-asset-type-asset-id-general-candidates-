> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.9 GET /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/comments

获取指定候选图下的评论列表，按创建时间**正序**排列。

**路径参数（Path）：**

| 参数          | 必填 | 类型   | 说明                                             |
|---------------|------|--------|--------------------------------------------------|
| `play_id`     | 是   | int    | 剧目 ID                                          |
| `asset_type`  | 是   | int    | 资产类型：1 场景、2 角色、3 道具、4 平面、5 其他 |
| `asset_id`    | 是   | string | 资产 ID                                          |
| `cand_id`     | 是   | string | 候选图 ID                                        |

**请求体 / 查询参数：** 无

**成功响应结构：**

`data` 为评论对象数组；无评论文件或尚无评论时为 `[]`。

```json
{
  "code": 1,
  "msg": "success",
  "data": [
    {
      "id": 1,
      "candidate_id": 10,
      "user_id": 1001,
      "username": "张三",
      "content": "面部光影再柔一点",
      "created_at": "2025-01-01T12:00:00+08:00",
      "resolved": false,
      "resolved_at": null,
      "resolved_by": null
    }
  ]
}
```

`data[]` 单项字段说明：

| 字段          | 类型              | 说明 |
|---------------|-------------------|------|
| `id`          | int               | 评论 ID |
| `candidate_id`| int \| string     | 所属候选图 ID |
| `user_id`     | int \| null       | 发表评论的用户 ID |
| `username`    | string            | 发表评论的用户名 |
| `content`     | string            | 评论正文 |
| `created_at`  | string            | 创建时间 |
| `resolved`    | bool              | 是否已解决 |
| `resolved_at` | string \| null    | 解决时间；未解决为 `null` |
| `resolved_by` | int \| null       | 标记为已解决的操作者用户 ID |

**错误响应示例：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
