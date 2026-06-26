> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 4.1 GET /openapi/drama/list

获取剧目列表。

**查询参数（Query）：**

| 参数              | 必填 | 类型   | 说明                                         |
|-------------------|------|--------|----------------------------------------------|
| `include_deleted` | 否   | string | `'true'` 时包含已软删除剧目，默认 `'false'` |

**成功响应示例（与后端统一响应结构一致）：**

```json
{
  "code": 1,
  "msg": "success",
  "data": [
    {
      "id": "1",
      "name": "校园奇妙夜",
      "deleted": false,
      "operation_time": "2025-01-01T10:00:00"
    }
  ]
}
```

**错误响应示例：**

```json
{
  "code": -1,
  "msg": "错误描述",
  "data": {
    "error": "错误描述"
  }
}
```
