> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 5.1 GET /openapi/drama/{play_id}/scripts

获取剧本集列表。

**路径参数（Path）：**

| 参数      | 必填 | 类型 | 说明    |
|-----------|------|------|---------|
| `play_id` | 是   | int  | 剧目 ID |

**请求体 / 查询参数：** 无

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "episodes": [
      {
        "episode_no": 1,
        "file": "ep01.txt",
        "title": "第1集",
        "uploaded_at": "2025-01-01T12:00:00"
      }
    ]
  }
}
```

**错误响应：**

当剧目不存在或文件结构异常时，会返回：

```json
{
  "code": -1,
  "msg": "错误描述字符串"
}
```
