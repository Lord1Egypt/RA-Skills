> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.6 POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/generate_image

资产图片生成：基于用户提示词、提示词模板与参考图调用模型生成图片，并作为新候选图写入对应资产。
该接口为**异步入队**：HTTP 立即返回 `taskId` 后，后台 worker 才会真正生成图片并落盘到候选图目录。

**请求体（JSON）示例：**

```json
{
  "user_prompt": "校园夜景，女生站在走廊窗边",
  "prompt_template": "写实风格，电影感光影",
  "reference_images": ["assets/2_角色A/general/references/1_参考图.png"],
  "reference_materials": [
    {
      "id": 12,
      "name": "走廊参考图.png",
      "path": "assets/2_角色A/general/references/1_参考图.png",
      "url": "/api/drama/1/assets/2/1/general/references/1/image",
      "source": "linked"
    }
  ],
  "prompt_mode_key": "face_closeup",
  "model": "bytedance-seed/seedream-4.5",
  "aspect_ratio": "16:9",
  "image_size": "1K"
}
```

字段说明：

| 字段               | 必填 | 类型        | 说明                                                             |
|--------------------|------|-------------|------------------------------------------------------------------|
| `user_prompt`      | 是   | string      | 用户输入的提示词                                                 |
| `prompt_template`  | 否   | string      | 提示词模板，将与 `user_prompt` 拼接成最终提示词                  |
| `reference_images` | 否   | array       | 参考图相对路径数组（相对于剧目根目录），若提供则必须实际存在     |
| `reference_materials` | 否 | array\<object> | 参考素材对象数组（`id/name/path/url/source`）；前端实际优先传该字段用于任务记录与重试 |
| `prompt_mode_key`  | 否   | string      | 当前提示词模式键（如 `face_closeup`）；用于按模式记录最近一次生图配置 |
| `model`            | 否   | string      | 生成模型；不传时使用该项目生效的默认图像模型                    |
| `aspect_ratio`     | 否   | string      | 画面宽高比，默认 `"16:9"`                                        |
| `image_size`       | 否   | string      | 图像尺寸标签，默认 `"1K"`                                       |

**成功响应结构（提交任务）：**

该接口为**异步入队**，HTTP 响应只返回任务标识；图片最终结果需要在任务完成后再查询。

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "taskId": "ci_xxxxxxxx",
    "queuePosition": 3,
    "message": "任务已提交，后台运行中，可到 AI 任务列表查看"
  }
}
```

**任务最终 `result`：**

当任务 `status=completed` 后，`GET /openapi/api/ai-tasks/tasks/<task_id>`（及任务列表中对应条目）返回的 `data.result` 通常包含：

```json
{
  "id": "候选图ID(字符串)",
  "name": "候选图文件名中的name",
  "image": "候选图原图文件名(如 1_xxx.png)",
  "image_url": "https://示例域/openapi/drama/1/assets/2/1/general/candidates/10/image/original?su_scene=...&su_exp=...&su_sig=..."
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 新候选图 ID |
| `name` | string | 候选图名称片段（与落盘命名相关） |
| `image` | string | 原图文件名 |
| `image_url` | string | **仅完成态由接口动态附加**（不落库）。与 OpenAPI 资产候选原图一致：短时 signed URL；配置了 `DOMAIN_URL` 时常为 `{base}/openapi/drama/.../image/original?...`，否则为相对路径 `/drama/...?...`。过期后需重新 `GET` 任务详情换链。若服务端未配置 `SECRET_KEY` 等导致无法签发，则可能无此字段。 |

任务查询接口详见 `{baseDir}/references/ref-8-2-get-openapi-api-ai-tasks-tasks-task-id.md`（路径、鉴权与 `data` 结构）。

**错误响应结构：**

本接口所有错误都通过简单的字符串消息返回，不包含 `data.error`，基本示例如下：

```json
{
  "code": -1,
  "msg": "错误信息"
}
```

代理在判断是否成功时，应以 `code == 1` 为准。
