> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 4.2 POST /openapi/drama/create

创建新剧目。

**请求体（JSON）：**

```json
{
  "name": "新剧本名称"
}
```

| 字段   | 必填 | 类型   | 说明     |
|--------|------|--------|----------|
| `name` | 是   | string | 剧目名称 |

**成功响应示例：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "2",
    "name": "新剧本名称",
    "deleted": false,
    "operation_time": "2025-01-01T12:00:00"
  }
}
```

**错误响应示例：**

```json
{
  "code": -1,
  "msg": "name required",
  "data": {
    "error": "name required"
  }
}
```
