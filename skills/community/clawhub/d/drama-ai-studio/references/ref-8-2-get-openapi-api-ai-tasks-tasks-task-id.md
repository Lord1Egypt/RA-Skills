> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 8.2 GET /openapi/api/ai-tasks/tasks/<task_id>
查询 AI 任务状态与最终执行结果（异步任务通用）

该接口用于配合 §6.6、§7.5、§8.1：
当你调用这些接口的**异步模式 POST**后会得到 `taskId`，随后轮询本接口直到任务完成。

**路径参数（Path）：**

| 参数      | 必填 | 类型   | 说明     |
|-----------|------|--------|----------|
| `task_id` | 是   | string | 任务 ID |

**请求体：** 无（GET）

**成功响应示例：**
```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "taskId": "ci_xxxxxxxx",
    "userId": "123",
    "taskType": "asset_candidate_image",
    "status": "completed",
    "queuePosition": 3,
    "createdAt": "2025-01-01T10:00:00.000Z",
    "startedAt": "2025-01-01T10:00:10.000Z",
    "finishedAt": "2025-01-01T10:00:20.000Z",
    "durationSec": 10,
    "result": { "...": "..." },
    "errorMessage": null,
    "isRead": false,
    "readAt": null,
    "cancelledAt": null,
    "operationContent": "任务列表展示用描述"
  }
}
```

**字段说明（`data`）：**

| 字段              | 类型            | 说明 |
|-------------------|-----------------|------|
| `taskId`          | string          | 任务 ID |
| `taskType`        | string          | 任务类型（如 `asset_candidate_image` / `shot_prompt_gen` / `shot_video_gen`） |
| `status`          | string          | 任务状态：`pending` / `running` / `completed` / `failed`（也可能为 `timeout` / `cancelled`） |
| `params`          | object\|null    | 入队参数（用于排查） |
| `resultRoute`     | object\|null   | 提交任务时透传的回调/路由信息 |
| `queuePosition`  | number          | 全局队列位置 |
| `result`          | object\|null   | 成功时的执行结果（失败时通常为 null） |
| `errorMessage`   | string\|null   | 失败原因 |

**任务队列处理机制（创建 -> 查询状态 -> 获取结果）：**

1. **创建任务（提交 POST）**：调用 §6.6（候选图）、§7.5（`optimize-prompt` 异步）、§8.1（分镜视频）后，服务端写入队列并立即返回 `taskId`。
2. **查询任务状态（轮询 GET）**：客户端轮询 `GET /openapi/api/ai-tasks/tasks/<task_id>`，观察 `status`：
   - `pending`：排队中
   - `running`：后台 worker 正在执行
   - `completed`：成功完成
   - `failed`：执行失败（可读取 `errorMessage`）
3. **获得最终执行结果（读取 result）**：当 `status=completed` 时，读取 `data.result`：
   - `asset_candidate_image`：`result.id/name/image`，以及动态附加的 **`result.image_url`**（候选原图短时 signed URL，见 ref-6-6）
   - `shot_prompt_gen`：`result.prompt` / `result.saved`
   - `shot_video_gen`：`result.result_video_path`，以及动态附加的 **`result.result_video_url`**（`GET /drama/{play_id}/files/share-stream?path=...` 短时 signed，与 §8.3/§8.4 成片链一致；不落库，过期需重新轮询本接口）
