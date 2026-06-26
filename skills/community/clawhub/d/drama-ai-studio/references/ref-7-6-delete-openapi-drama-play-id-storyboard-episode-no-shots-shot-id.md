> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 7.6 DELETE /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}

删除指定镜头。

**请求体：** 无

**成功响应结构：**

本接口成功时返回 `data=null`，由于后端统一响应实现会省略 `data` 字段，实际响应形如：

```json
{
  "code": 1,
  "msg": "success"
}
```

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
