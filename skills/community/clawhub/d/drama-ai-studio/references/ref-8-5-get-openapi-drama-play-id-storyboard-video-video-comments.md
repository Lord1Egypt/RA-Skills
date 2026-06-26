> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

**给智能体（`task_id` 从哪来）：** Query 中的 `task_id` 与 §8.3 分镜视频列表、§8.4 按集选中视频接口里**每条成片视频对象的 `id` 字段同义**（§8.4 为 `data.shots[].video.id`）。评论链路只认这一字符串；勿用路径、物理文件名或 `taskId`（§8.1 异步返回）若与成片条目 `id` 不一致时混用——应以列表/选中接口返回的 **`id`** 为准。

### 8.5 GET /openapi/drama/{play_id}/storyboard-video/video-comments

获取指定**成片视频任务**下的评论列表，按 `created_at` **升序**（时间线从早到晚）。

**路径参数（Path）：**

| 参数      | 必填 | 类型 | 说明   |
|-----------|------|------|--------|
| `play_id` | 是   | int  | 剧目 ID |

**查询参数（Query，必填）：**

| 参数         | 必填 | 类型   | 说明 |
|--------------|------|--------|------|
| `episode_no` | 是   | int    | 集号 |
| `shot_id`    | 是   | string | 镜头 ID（如 `s1`） |
| `task_id`    | 是   | string | 成片任务 ID：**等于** §8.3 列表项或 §8.4 中 `video.id`（与参数名 `task_id` 同值不同名） |

**请求体：** 无（GET）

**前置条件：** 对应任务须存在、属于该剧目下该分镜、**未软删**、`status` 为 `completed` 且 `result_video_path` 非空；否则返回业务错误（常见为 400/404，见统一错误结构）。

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "comments": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "task_id": "sv_ab12cd34",
        "user_id": 1001,
        "username": "张三",
        "content": "口型再对齐一点",
        "created_at": "2026-04-16T10:00:00+08:00",
        "resolved": false,
        "resolved_at": null,
        "resolved_by": null
      }
    ]
  }
}
```

无评论文件或尚无评论时，`data.comments` 为 `[]`。

**`data.comments[]` 单项字段说明：**

| 字段          | 类型           | 说明 |
|---------------|----------------|------|
| `id`          | string         | 评论唯一 ID（UUID） |
| `task_id`     | string         | 冗余：所属成片任务 ID |
| `user_id`     | int \| string \| null | 发表人用户 ID（与登录上下文写入一致） |
| `username`    | string         | 发表时固化的用户名（展示口径） |
| `content`     | string         | 评论正文 |
| `created_at`  | string         | 创建时间（ISO8601，东八区） |
| `resolved`    | bool           | 是否已解决；仅当存储中显式 `resolved: false` 时视为未解决 |
| `resolved_at` | string \| null | 标记已解决时间；未解决时为 `null` |
| `resolved_by` | int \| string \| null | 执行「标记已解决」的用户 ID；未解决时为 `null` |

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
