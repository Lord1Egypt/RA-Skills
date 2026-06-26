> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.10 POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/comments

为指定候选图**新增一条评论**。`cand_id` 对应的候选图须已存在。

**路径参数（Path）：** 同 §6.9。

**请求体（JSON）：**

```json
{
  "content": "希望构图再居中一些"
}
```

| 字段      | 必填 | 类型   | 说明 |
|-----------|------|--------|------|
| `content` | 是   | string | 评论正文，不可仅为空白 |

**成功响应结构：**

`data` 为新建的单条评论对象（字段同 §6.9 中数组项）。

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": 2,
    "candidate_id": 10,
    "user_id": 1001,
    "username": "张三",
    "content": "希望构图再居中一些",
    "created_at": "2025-01-01T12:05:00+08:00",
    "resolved": false,
    "resolved_at": null,
    "resolved_by": null
  }
}
```

**错误响应示例：** 缺少 `content`、候选图不存在等。

```json
{
  "code": -1,
  "msg": "content required"
}
```
