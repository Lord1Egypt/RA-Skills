> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 7.2 POST /openapi/drama/{play_id}/storyboard/{episode_no}/analyze

触发该集分镜分析：读取该集剧本 → AI 拆分为镜头序列并关联资产。

**路径参数（Path）：** 同 7.1。

**请求体：** 无

**成功响应结构：**

返回分析后分镜对象（字段同 7.1），并额外包含：

| 字段                 | 类型 | 说明 |
|----------------------|------|------|
| `related_assets_count` | int | 本集相关资产数量（供前端可选展示） |

响应示例：

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "play_id": "1",
    "episode_no": 1,
    "analyzed_at": "2025-01-01T12:00:00",
    "shots": [],
    "related_assets_count": 123
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
