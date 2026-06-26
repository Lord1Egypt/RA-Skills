> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 8.4 GET /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/selected-videos

获取指定剧目、指定一集下，**每个分镜当前选中的成片视频**（或等价默认的一条）；用于按集汇总「终稿/选用」视频状态。

**路径参数（Path）：**

| 参数         | 必填 | 类型   | 说明    |
|--------------|------|--------|---------|
| `play_id`    | 是   | int    | 剧目 ID |
| `episode_no` | 是   | int    | 集号    |

**请求体 / 查询参数：** 无（GET）

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "shots": [
      {
        "shot_id": "s1",
        "order": 1,
        "video": {
          "id": "sv_xxxxxxxx",
          "play_id": "123",
          "episode_no": 1,
          "shot_id": "s1",
          "mode": "reference",
          "status": "completed",
          "result_video_path": "storyboard_video/ep_001/sv_001/sv_xxxxxxxx.mp4",
          "selected": true,
          "duration": 5.0,
          "result_video_url": "https://示例域/openapi/drama/123/files/share-stream?path=storyboard_video%2Fep_001%2Fsv_001%2Fsv_xxxxxxxx.mp4&su_scene=...&su_exp=...&su_sig=..."
        }
      },
      {
        "shot_id": "s2",
        "order": 2,
        "video": null
      }
    ]
  }
}
```

**字段说明（`data`）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `shots` | array | 该集分镜列表项，顺序与分镜 `order` 一致 |

**字段说明（`data.shots[]` 每项）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `shot_id` | string | 镜头 ID |
| `order` | int\|null | 镜头顺序 |
| `video` | object\|null | 该镜当前选用的一条成片；无成片时为 `null`。成功选中时通常含 `result_video_path`、`id`、`selected` 等（与 §8.3 单条任务结构一致）；可能额外含 `duration`（秒）；**`result_video_url`** 与 §8.3 相同规则动态附加 |

> 说明：与 §8.3「单镜全部历史视频列表」不同，本接口按**整集**返回每镜**一条**选用结果，适合集维度巡检或总览。

> **给智能体：** 非空 `video` 上的 **`id`** 即该条成片任务主键；调用 §8.5～§8.7 视频评论接口时，应将该 **`id`** 作为参数 **`task_id`** 传入（同值、仅参数名不同）。

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
