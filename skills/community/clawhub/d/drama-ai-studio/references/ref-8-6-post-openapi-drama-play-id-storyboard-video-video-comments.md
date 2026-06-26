> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

**给智能体：** 请求体中的 `task_id` 与 §8.3 / §8.4 返回的视频对象字段 **`id`** 同义，说明见 `ref-8-5` 文首。

### 8.6 POST /openapi/drama/{play_id}/storyboard-video/video-comments

对指定**已完成且有成片路径**的任务**新增一条视频评论**。

**路径参数（Path）：**

| 参数      | 必填 | 类型 | 说明   |
|-----------|------|------|--------|
| `play_id` | 是   | int  | 剧目 ID |

**请求体（JSON）：**

| 字段         | 必填 | 类型   | 说明 |
|--------------|------|--------|------|
| `episode_no` | 是   | int    | 集号 |
| `shot_id`    | 是   | string | 镜头 ID |
| `task_id`    | 是   | string | 成片任务 ID：**等于** §8.3 列表项或 §8.4 中 `video.id`（与参数名 `task_id` 同值不同名） |
| `content`    | 是   | string | 评论正文；去首尾空白后不能为空，**最长 4000 字符**；服务端对同一用户同一 `task_id` 有进程内发帖频控 |

**请求体示例：**

```json
{
  "episode_no": 1,
  "shot_id": "s1",
  "task_id": "sv_ab12cd34",
  "content": "背景再压暗一档，突出人物轮廓。"
}
```

**前置条件：** 与 **§8.5 GET** 相同（任务须 `completed` 且 `result_video_path` 非空等）。

**成功响应结构：**

返回**单条**新建评论对象（不在 `comments` 数组外层再包一层）。

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": "sv_ab12cd34",
    "user_id": 1001,
    "username": "张三",
    "content": "背景再压暗一档，突出人物轮廓。",
    "created_at": "2026-04-16T10:05:00+08:00",
    "resolved": false,
    "resolved_at": null,
    "resolved_by": null
  }
}
```

**`data` 字段说明：** 与 `ref-8-5` 中 `data.comments[]` 单项一致。

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
