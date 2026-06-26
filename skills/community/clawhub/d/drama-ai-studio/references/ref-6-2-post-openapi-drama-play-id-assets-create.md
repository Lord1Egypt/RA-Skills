> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.2 POST /openapi/drama/{play_id}/assets/create

创建新资产。

**路径参数（Path）：** 同 6.1。

**请求体（JSON）：**

```json
{
  "type": 2,
  "name": "角色A",
  "description": "女主，高中生..."
}
```

| 字段          | 必填 | 类型   | 说明                                         |
|---------------|------|--------|----------------------------------------------|
| `type`        | 是   | int    | 资产类型：1 场景, 2 角色, 3 道具, 4 平面     |
| `name`        | 是   | string | 资产名称                                     |
| `description` | 否   | string | 资产描述，可为空或省略                      |

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "2",
    "type": 2,
    "name": "角色A",
    "description": "女主，高中生...",
    "deleted": false,
    "operation_time": "2025-01-01T12:00:00"
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
