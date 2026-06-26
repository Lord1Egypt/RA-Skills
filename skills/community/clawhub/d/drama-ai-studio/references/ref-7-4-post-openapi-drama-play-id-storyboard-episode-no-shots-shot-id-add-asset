> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 7.4 POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/add-asset

为镜头添加资产（补标），可新建或关联已有资产。

**请求体（JSON）：**

| 字段         | 必填 | 类型        | 说明 |
|--------------|------|-------------|------|
| `asset_type` | 是   | int         | 资产类型：1=场景 2=角色 3=道具 4=平面 5=其他 |
| `name`       | 否   | string      | 新建资产时提供（与 `asset_id` 二选一） |
| `asset_id`   | 否   | string      | 绑定已有资产时提供（与 `name` 二选一） |

请求体示例：

```json
{
  "asset_type": 2,
  "name": "新角色名"
}
```

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "asset": {
      "id": "10",
      "type": 2,
      "name": "新角色名",
      "deleted": false,
      "operation_time": "2025-01-01T12:00:00"
    },
    "shot": {
      "id": "s1",
      "order": 1,
      "scene_ids": [],
      "character_ids": ["10"],
      "prop_ids": [],
      "surface_ids": [],
      "other_ids": []
    }
  }
}
```

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
