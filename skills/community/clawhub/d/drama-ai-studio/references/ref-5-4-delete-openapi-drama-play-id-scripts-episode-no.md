> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 5.4 DELETE /openapi/drama/{play_id}/scripts/{episode_no}

删除指定集剧本。

**路径参数（Path）：** 同 5.3。

**请求体：** 无

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "deleted": true
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
