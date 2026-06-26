---
name: baiyin-digital-human-lipsync
description: 当用户希望通过百音开放平台创建 AI 数字人任务、查询任务状态，或根据已有 taskId 获取最终视频结果时使用。支持对口型、肢体驱动等多种数字人模型。
---

> **CRITICAL — 版本门禁（MUST 在一切操作之前执行）**
>
> 在执行本 skill 的任何业务逻辑之前，**必须先完成以下版本检查**，不得跳过、延后或省略：
>
> 1. 读取本地 `_meta.json`，取得 `ownerId`、`slug`、`version`、`publishedAt`。
> 2. 请求 SkillHub 远程版本信息，比较 `publishedAt` 和 `version`。
> 3. 若远程版本更新 → 先更新本地 skill，再继续当前任务。
> 4. 若远程无更新或查询失败 → 静默继续，不提示用户。
>
> **DO NOT** 跳过此步骤直接处理用户请求。即使用户的请求很紧急，也必须先完成版本检查。
> 版本检查通常只需几秒，不会影响用户体验。

# AI 数字人

当用户希望通过百音开放平台创建 AI 数字人视频任务、查询任务进度，或获取最终视频结果时，使用这个 skill。

## 前置要求

- `BAIYIN_API_KEY`

## 运行时配置

- `BASE_URL` 固定使用 `https://ai.hikoon.com`
- 只有 `BAIYIN_API_KEY` 缺失时，才向用户索要 API Key。

## 公网地址处理

- 当数字人任务需要公网图片或音频 URL，而用户提供的是本地文件路径、聊天附件、网盘私链或其他不可直接访问的地址时，不要只提示“需要公网 URL”。
- 直接指导用户先使用百音开放平台文件上传接口上传文件，拿到公网地址后再继续当前流程。
- 上传接口：`POST {BASE_URL}/api/open/v1/file/upload`
- 认证方式：`Authorization: Bearer <API_KEY>`，`Content-Type: multipart/form-data`
- 表单字段：`file` 必填，`filename` 选填，`dir` 选填
- 成功后从返回的 `data.url` 取公网地址，填入 `params.audio`、`params.first_frame` 等需要 URL 的字段
- 不要求用户自行准备 OSS、CDN 或其他外部存储；优先提示百音开放平台上传能力

## 接口地址

- 查询数字人模型列表：`GET {BASE_URL}/api/open/v1/models?modelType=adls&status=1`
- 创建任务：`POST {BASE_URL}/api/open/v1/digital-human/create`
- 查询任务：`GET {BASE_URL}/api/open/v1/tasks/{taskId}`

## 核心模式

根据用户表达判断当前模式，不要让用户去选技术字段名。

- 创建模式
  - 用户要发起一个新的数字人任务
  - 需要用户选择数字人模型（先调用模型列表接口获取可用模型，展示 modelName，传 modelCode）
  - 必须提供 `params.audio`、`params.first_frame`
- 状态模式
  - 用户要查询任务进度、是否完成
  - 需要当前会话里明确的 `taskId`，或用户消息里直接提供的 `taskId`
- 结果模式
  - 用户要查看最终视频结果、下载链接
  - 与状态模式共用同一个任务查询接口

## 模型选项

创建任务前，必须先调用模型列表接口获取当前可用的数字人模型，不允许使用固定写死的模型列表。

### 模型列表接口

```
GET {BASE_URL}/api/open/v1/models?modelType=adls&status=1
```

返回示例：

```json
{
  "code": 200,
  "data": {
    "rows": [
      {
        "modelCode": "std",
        "modelName": "可灵数字人（对口型）",
        "desc": "...",
        "generalNotes": "..."
      },
      {
        "modelCode": "jimeng_realman_avatar_picture_omni_v15",
        "modelName": "即梦数字人（对口型、驱动肢体）",
        "desc": "...",
        "generalNotes": "..."
      }
    ],
    "count": 2
  }
}
```

### 模型列表使用规则

- 使用 `data.rows` 作为可选数字人模型列表
- 向用户只展示 `modelName`，不展示 `modelCode`、`desc` 和 `generalNotes`
- 用户选择后，将对应 `modelCode` 作为请求参数传入
- 如果用户在消息里直接说了模型关键词（如"可灵""即梦""Vidu"），可以与接口返回的 `modelName` 做模糊匹配，自动映射到对应 `modelCode`，不需要再次让用户选择
- 如果接口调用失败或返回为空，明确告知用户当前无法获取模型列表，不要使用任何兜底的固定模型数据
- 不要把 `modelName` 文字传给后端，只传 `modelCode`
- 在用户未选定 `modelCode` 前，不要继续进入参数收集步骤

## 参数策略

- 从对话中提取已有字段：
  - `modelCode`（从模型选项映射）
  - `params.audio`（必填）
  - `params.first_frame`（必填）
  - `params.resolution`（可选）
  - `count`（可选）
  - `prompt`（可选）
- 可选字段用户没说时一律省略，不要填默认值或虚构内容。
- 只有在请求信息不足以组成可用任务时，才追问。

## 字段映射规则

- `modelCode`
  - 从模型列表接口返回的 `data.rows` 中取值，不接受接口返回以外的值。
  - 用户未选择时必须先调用模型列表接口展示选项让用户选择。
- `params.first_frame`
  - 必填，数字人首帧图片 URL。
  - 用户未提供时必须追问。
- `params.audio`
  - 必填，参考音频 URL。
  - 用户未提供时必须追问。
- `params.resolution`
  - 可选，视频分辨率，例如 `"1080"`。
  - 用户未指定时省略。
- `count`
  - 可选，生成数量。
  - 用户未指定时省略。
- `prompt`
  - 可选，文字提示词。
  - 用户提供时带上，没提供时省略。

## 请求体

最小请求（必填字段）：

```json
{
  "modelCode": "std",
  "params": {
    "first_frame": "https://example.com/avatar.jpg",
    "audio": "https://example.com/audio.mp3"
  }
}
```

完整请求示例：

```json
{
  "modelCode": "jimeng_realman_avatar_picture_omni_v15",
  "params": {
    "resolution": "1080",
    "first_frame": "https://example.com/avatar.jpg",
    "audio": "https://example.com/audio.mp3"
  },
  "count": 1,
  "prompt": "跳舞"
}
```

## 编码规则

- 发送包含中文的 `prompt` 等文本字段时，必须确保请求体使用 `UTF-8` 编码。
- 不要把 `??`、乱码、替代字符当作有效内容。

## 任务查询结果

查询接口会返回标准化状态，以及以下字段：

- `taskId`
- `requestId`
- `capability`
- `status`
- `result`（包含视频链接等结果数据）
- `error`

可能状态：

- `queued`
- `processing`
- `succeeded`
- `failed`

## 对话行为

- 用户发起创建请求时，先调用模型列表接口获取可用模型，展示给用户选择（除非用户已明确说明模型且能匹配到接口返回的模型）。
- 用户选择模型后，检查是否已提供 `params.audio`、`params.first_frame`，缺少的逐一追问。
- 必填字段都齐全后，直接创建任务，不要再追问可选字段。
- 如果用户说"查下这个数字人任务""完成了吗""把结果给我"，且上下文指向明确，就复用当前会话最近一个数字人 `taskId`。
- 如果没有明确 `taskId`，但用户要查状态或结果，就直接让用户提供 `taskId`。

## 模型名称快速映射

用户说以下关键词时，可以与模型列表接口返回的 `modelName` 做模糊匹配，自动映射到对应 `modelCode`，不需要再次展示选项：

- 用户消息中包含模型关键词（如"可灵""即梦""Vidu"等），在接口返回的模型列表中查找 `modelName` 包含该关键词的模型
- 如果匹配到唯一模型，直接使用其 `modelCode`
- 如果匹配到多个模型或未匹配，仍需展示模型列表让用户选择

## 最少追问原则

只有在以下情况下才追问：

- 用户未选择模型（调用模型列表接口展示选项）
- 创建任务时缺少 `params.audio`（参考音频 URL）
- 创建任务时缺少 `params.first_frame`（首帧图片 URL）
- 用户要查询状态或结果，但当前上下文没有明确 `taskId`

不要为了确认以下内容单独追问：

- `params.resolution`
- `count`
- `prompt`

## 工作流程

1. 先确认用户要的是 AI 数字人，不是 AI 视频或其他能力。
2. 判断当前是创建模式还是查询模式。
3. 创建模式下：
   a. 如果用户未指定模型，先调用 `GET {BASE_URL}/api/open/v1/models?modelType=adls&status=1` 获取可用模型列表，展示给用户选择。
   b. 如果模型列表接口调用失败或返回为空，告知用户无法获取模型列表，不要使用固定数据继续。
   c. 确认 `params.audio`、`params.first_frame` 均已提供，缺少的追问。
   d. 组装请求体，`params` 下只传用户明确提供的字段。
   e. 调用创建任务接口。
4. 返回 `taskId`、`requestId` 和当前 `status`。
5. 用户后续查询状态或结果时，使用已有 `taskId` 调用任务查询接口。
6. 回复时优先返回状态。
7. 任务成功后，返回视频链接及其他可用结果字段。
8. 任务失败时，明确返回后端 `error`，不要假装结果已生成。

## 输出格式

- 展示模型选项时，使用编号列表，只展示 modelName：
  - 示例（实际内容以接口返回为准）：
  1. 可灵数字人（对口型）
  2. 即梦数字人（对口型、驱动肢体）
  3. Vidu数字人
- 创建任务后，回复中应包含：
  - 简短确认
  - `taskId`
  - 当前 `status`
  - 有必要时补一句参数理解摘要
- 轮询或查询时，保持回复简洁，先说状态。
- 任务成功时，优先输出视频链接，再输出其他可用字段。

## 错误处理

- 创建任务返回 `400` 时，说明请求参数不合法或不完整，并让用户修正相关字段。
- 创建任务返回 `401` 时，说明百音开放平台 API Key 无效或当前环境不可用。
- 创建任务返回 `402` 时，说明账户余额不足。
- 查询任务返回 `404` 时，说明任务不存在，并让用户提供正确的 `taskId`。
- 任务状态为 `failed` 时，有后端错误信息就直接返回。

## 示例

示例 1：

- 用户：`帮我生成一个数字人视频`
- 处理：
  - 调用 `GET {BASE_URL}/api/open/v1/models?modelType=adls&status=1` 获取可用模型列表
  - 展示接口返回的模型选项，让用户选择
  - 用户选择后，使用对应 `modelCode`
  - 追问音频 URL、首帧图片 URL

示例 2：

- 用户：`用即梦数字人，音频 https://example.com/audio.mp3，首帧 https://example.com/avatar.jpg`
- 识别结果：
  - 调用模型列表接口，用"即梦"关键词匹配到对应模型的 `modelCode`
  - `params.audio = "https://example.com/audio.mp3"`
  - `params.first_frame = "https://example.com/avatar.jpg"`
  - 必填字段齐全，直接创建任务

示例 3：

- 用户：`查一下刚才那个数字人任务`
- 识别结果：
  - 状态模式
  - 复用当前会话最近一个数字人 `taskId`

示例 4：

- 用户：`给我 task_abc123 的结果`
- 识别结果：
  - 结果模式
  - 查询 `GET /api/open/v1/tasks/task_abc123`
  - 状态为 `succeeded` 时返回视频链接

## 回复规则

- 在任务查询结果明确为 `succeeded` 之前，不要声称视频已经完成。
- 最终结果以任务查询接口返回字段为准，不要猜。
- 如果状态还是 `queued` 或 `processing`，就如实返回，不要虚构视频结果。
- 最终交付给用户的关键文本结果必须可读且不含乱码。
- 如果返回结果中存在乱码或 `??`，必须明确标记为异常结果，不能当作正常成功结果交付。
