> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.8 PUT /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/final

将**单张**资产候选图设为终稿或从终稿集合中移除。

**路径参数（Path）：**

| 参数          | 必填 | 类型   | 说明                                             |
|---------------|------|--------|--------------------------------------------------|
| `play_id`     | 是   | int    | 剧目 ID                                          |
| `asset_type`  | 是   | int    | 资产类型：1 场景、2 角色、3 道具、4 平面、5 其他 |
| `asset_id`    | 是   | string | 资产 ID                                          |
| `cand_id`     | 是   | string | 候选图 ID                                        |

**请求体（JSON）：**

```json
{
  "is_final": true
}
```

| 字段       | 必填 | 类型 | 说明 |
|------------|------|------|------|
| `is_final` | 是   | bool | `true` 表示加入终稿集合；`false` 表示从终稿集合移除 |

**成功响应结构：**

与 **§6.7** 相同，返回更新后的终稿配置（`data.version`、`data.items`）。

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "version": 2,
    "items": [
      {
        "candidate_id": "10",
        "image": "10_xxx.png",
        "path": "2/1_角色A/general/candidates/10_xxx.png",
        "has_unresolved_comments": false
      }
    ]
  }
}
```

**错误响应示例：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
