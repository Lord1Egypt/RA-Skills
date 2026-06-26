> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

**给智能体：** 请求体中的 `task_id` 与 §8.3 / §8.4 返回的视频对象字段 **`id`** 同义，说明见 `ref-8-5` 文首。

### 8.7 PATCH /openapi/drama/{play_id}/storyboard-video/video-comments/resolve

将指定评论标记为**已解决**（用于协作跟踪「反馈已处理」）。若该评论已是已解决状态，**幂等**返回当前对象。

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
| `comment_id` | 是   | string | 评论 `id`（与 §8.5/§8.6 返回的 `id` 一致） |

**请求体示例：**

```json
{
  "episode_no": 1,
  "shot_id": "s1",
  "task_id": "sv_ab12cd34",
  "comment_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**前置条件：** 与 **§8.5 GET** 相同（任务校验）；且评论须存在于该任务对应的评论文件中。

**成功响应结构：**

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
    "resolved": true,
    "resolved_at": "2026-04-16T11:00:00+08:00",
    "resolved_by": 1002
  }
}
```

**`data` 字段说明：** 与 `ref-8-5` 中评论对象一致；已解决时 `resolved_at`、`resolved_by` 由服务端写入。

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```

> 说明：若服务端对某类权限校验失败，可能返回 HTTP **403**（`code`/`msg` 依实现）；评论不存在或任务不合法时常见为 **404** 或 **400**，与 `msg` 文案一致即可。
