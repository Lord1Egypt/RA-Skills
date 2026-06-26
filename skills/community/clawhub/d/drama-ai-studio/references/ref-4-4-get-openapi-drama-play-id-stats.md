> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 4.4 GET /openapi/drama/{play_id}/stats

获取剧目统计信息（集数、镜头数、资产数量等）。

**路径参数（Path）：** 同 4.3。

**成功响应示例：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "episodes_total": 12,
    "shots_total": 210,
    "estimated_duration_sec": 3600,
    "assets": {
      "scenes": 15,
      "characters": 25,
      "props": 50
    }
  }
}
```

剧本不存在或已删除时返回 404：

```json
{
  "code": -1,
  "msg": "Not found",
  "data": {
    "error": "Not found"
  }
}
```
