> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 8.8 PUT /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/videos/{task_id}/selected

将指定视频设为该分镜当前**选中/终稿**视频。

**路径参数（Path）：**

| 参数         | 必填 | 类型   | 说明 |
|--------------|------|--------|------|
| `play_id`    | 是   | int    | 剧目 ID |
| `episode_no` | 是   | int    | 集号 |
| `shot_id`    | 是   | string | 镜头 ID（如 `s1`） |
| `task_id`    | 是   | string | 要设为选中的视频任务 ID（可从 §8.3 的 `id` 或 §8.4 的 `video.id` 获取） |

**请求体 / 查询参数：** 无（PUT）

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "sv_xxxxxxxx",
    "play_id": "123",
    "episode_no": 1,
    "shot_id": "s1",
    "mode": "reference",
    "status": "completed",
    "result_video_path": "storyboard_video/ep_001/sv_001/sv_xxxxxxxx.mp4",
    "selected": true
  }
}
```

**`data` 字段说明：**

返回被设为选中的视频任务对象（与 §8.3 列表单项结构一致，常见字段包括 `id`、`shot_id`、`status`、`result_video_path`、`selected` 等）。

**前置条件与行为说明：**

- 目标 `task_id` 需属于路径中的 `episode_no`、`shot_id`，且任务记录有效（未删除）。
- 设为选中后，同一镜头下其它视频会自动取消选中，保证单镜头最多一条 `selected=true`。
- 建议调用后通过 §8.3 或 §8.4 再次读取，确认最终选中状态。

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```

> 常见错误：`task_id` 不存在、任务不属于该镜头、参数与路径不匹配等，通常返回 HTTP 400/500（以网关与服务端实际实现为准）。
