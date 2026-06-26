> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 5.3 GET /openapi/drama/{play_id}/scripts/{episode_no}/content

获取指定集剧本原文；不存在时返回 404。

**路径参数（Path）：**

| 参数         | 必填 | 类型 | 说明    |
|--------------|------|------|---------|
| `play_id`    | 是   | int  | 剧目 ID |
| `episode_no` | 是   | int  | 集号    |

**请求体：** 无

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "content": "整集剧本文本"
  }
}
```

**错误响应示例（HTTP 404）：**

```json
{
  "code": -1,
  "msg": "该集剧本不存在"
}
```

其他错误同样以 `"code": -1, "msg": "错误描述"` 的形式返回。
