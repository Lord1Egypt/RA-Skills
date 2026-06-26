> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 8.3 GET /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/videos

获取该分镜下历史视频列表（生成 + 上传），仅返回存在 `result_video_path` 的记录。

**路径参数（Path）：**

| 参数         | 必填 | 类型   | 说明 |
|--------------|------|--------|------|
| `play_id`    | 是   | int    | 剧目 ID |
| `episode_no` | 是   | int    | 集号 |
| `shot_id`    | 是   | string | 镜头 ID（如 `s1`） |

**请求体：** 无（GET）

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": [
    {
      "id": "sv_xxxxxxxx",
      "play_id": "123",
      "episode_no": 1,
      "shot_id": "s1",
      "mode": "reference",
      "status": "completed",
      "result_video_path": "storyboard_video/ep_001/sv_001/sv_xxxxxxxx.mp4",
      "created_at": "2025-01-01T10:00:20",
      "selected": true,
      "order": 1,
      "duration_sec": 5,
      "name": "版本A",
      "result_video_url": "https://示例域/openapi/drama/123/files/share-stream?path=storyboard_video%2Fep_001%2Fsv_001%2Fsv_xxxxxxxx.mp4&su_scene=...&su_exp=...&su_sig=..."
    }
  ]
}
```

**字段说明（`data[]` 每项）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 视频任务 ID |
| `play_id` | string | 剧目 ID |
| `episode_no` | int | 集号 |
| `shot_id` | string | 镜头 ID |
| `mode` | string | 任务模式（如 `reference` / `head_tail` / `first_frame` / `upload`） |
| `status` | string | 任务状态（通常为 `completed`） |
| `result_video_path` | string | 最终视频相对路径（核心字段） |
| `created_at` | string | 创建时间（ISO 风格字符串） |
| `selected` | bool | 是否当前镜头选中视频 |
| `order` | int\|null | 镜头顺序（来自 storyboard 对应镜头） |
| `duration_sec` | number\|null | 视频时长（秒，部分来源可能缺失） |
| `name` | string\|null | 视频显示名称（为空时前端常显示“未命名”） |
| `result_video_url` | string | **仅 `status=completed` 且存在 `result_video_path` 时由接口动态附加**（不落库）。剧目文件 **`share-stream`** 短时 signed URL；配置了 `DOMAIN_URL` 时常为 `{base}/openapi/drama/.../files/share-stream?path=...&su_*`；过期后需重新 GET 本列表换链。无法签发时可能无此键。 |

> 说明：
> 1. 返回列表按 `created_at` 倒序（最新在前）。
> 2. 该接口适合“按分镜直接读取已有视频结果”；如需查看异步执行过程（`pending/running/failed`），可结合 §8.1 + §8.2 的任务查询接口。

> **给智能体：** 列表项中的 **`id`** 即成片任务主键；调用 §8.5～§8.7 评论接口时将该值作为 **`task_id`** 传入（同值、仅参数名不同）。勿用 `result_video_path` 代替。

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
