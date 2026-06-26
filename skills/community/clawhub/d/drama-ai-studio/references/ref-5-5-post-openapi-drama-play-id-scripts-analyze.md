> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 5.5 POST /openapi/drama/{play_id}/scripts/analyze

剧本资产智能分析，从原文中抽取场景/角色/道具并更新资产库。

**请求体（JSON，可选）：**

```json
{
  "episode_nos": [1, 2],
  "asset_types": [1, 2, 3]
}
```

| 字段          | 类型 | 说明                                                                 |
|---------------|------|----------------------------------------------------------------------|
| `episode_nos` | 数组 | 要分析的集号列表；不传则分析所有已有集                              |
| `asset_types` | 数组 | 要分析的资产类型 ID：1=场景,2=角色,3=道具；不传或空表示三类全部分析 |

类型约束：

- `episode_nos` 存在但不是数组 → 400，`msg: "episode_nos 须为数组"`
- `asset_types` 存在但不是数组 → 400，`msg: "asset_types 须为数组"`

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "created": [
      {
        "id": "10",
        "type": 2,
        "name": "角色A",
        "description": "人物小传...",
        "deleted": false,
        "operation_time": "2025-01-01T12:00:00"
      }
    ],
    "merged": [
      {
        "name": "角色B",
        "type": 2,
        "id": "5"
      }
    ]
  }
}
```

其中：

- `created`：本次分析新建的资产列表（结构与资产对象一致）。
- `merged`：与已有资产合并的条目列表，至少包含 `name`、`type`、`id`。

**错误响应示例：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
