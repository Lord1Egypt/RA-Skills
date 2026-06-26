> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 4.3 GET /openapi/drama/{play_id}

获取单个剧目详情；找不到返回 404。

**路径参数（Path）：**

| 参数      | 必填 | 类型 | 说明   |
|-----------|------|------|--------|
| `play_id` | 是   | int  | 剧目 ID |

**成功响应示例：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "1",
    "name": "短剧实例",
    "deleted": false,
    "operation_time": "2025-01-01T12:00:00"
  }
}
```

**未找到时（HTTP 404）：**

```json
{
  "code": -1,
  "msg": "Not found",
  "data": {
    "error": "Not found"
  }
}
```
