> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 8.1 POST /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/tasks

创建分镜视频生成任务（异步入队）

**路径参数（Path）：** 同 8.1。

**请求体（JSON）示例：**

```json
{
  "mode": "reference",
  "prompt": "画面提示词",
  "asset_snapshot": { "...": "..." },
  "motion": "动作描述",
  "model": "seedance1.5",
  "duration_sec": 5,
  "ratio": "16:9",
  "resolution": "720p"
}
```

请求体字段说明（与后端校验一致）：

| 字段                  | 必填 | 类型                | 说明 |
|-----------------------|------|---------------------|------|
| `mode`                | 是   | string              | 必须为 `"reference"` |
| `reference_image_paths` | 否 | array\<string>    | 可选：若不传或为空，后端会从该镜头已绑定资产生成默认参考图路径 |
| `prompt`              | 否   | string              | 可选，生成提示词 |
| `asset_snapshot`      | 否   | object              | 可选，资产快照（原样透传进任务） |
| `motion`              | 否   | string              | 可选，运动描述 |
| `model`               | 否   | string              | 可选，视频模型 |
| `duration_sec`        | 否   | number              | 可选，时长（时长≥4，同时用于计费 quantity_key） |
| `ratio`               | 否   | string              | 可选，画幅比例（默认 `"16:9"`）|
| `resolution`          | 否   | string              | 可选，分辨率（默认为 `"720p"`） |

**成功响应结构（提交任务）：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "taskId": "sv_xxxxxxxx",
    "queuePosition": 2,
    "message": "任务已提交，后台运行中，可到 AI 任务列表查看"
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

> 任务创建后，生成结果需要通过 §8.2 中的 `GET /openapi/api/ai-tasks/tasks/<task_id>` 查询任务详情，直到 `status=completed` 后从 `data.result.result_video_path` 读取最终视频相对路径，并可使用同对象上的 **`result_video_url`**（短时 signed 的可 GET 成片链，见 ref-8-2）直接拉取视频。
