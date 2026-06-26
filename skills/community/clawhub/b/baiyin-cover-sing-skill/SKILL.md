---
name: baiyin-cover-sing-skill
description: 当用户希望通过百音开放平台创建 AI 歌手翻唱任务、查询翻唱任务状态，或根据已有 taskId 返回最终翻唱音频结果时使用。
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

# AI 歌手翻唱

当用户希望通过百音开放平台创建 AI 歌手翻唱任务、查询翻唱进度，或获取最终翻唱结果时，使用这个 skill。

## 前置要求

- `BAIYIN_API_KEY`

## 运行时配置

- `BASE_URL` 固定使用 `https://ai.hikoon.com`
- 只有 `BAIYIN_API_KEY` 缺失时，才向用户索要 API Key。

## 公网地址处理

- 当翻唱任务需要公网音频 URL，而用户提供的是本地文件路径、聊天附件、网盘私链或其他不可直接访问的地址时，不要只提示“需要公网 URL”。
- 直接指导用户先使用百音开放平台文件上传接口上传文件，拿到公网地址后再继续当前流程。
- 上传接口：`POST {BASE_URL}/api/open/v1/file/upload`
- 认证方式：`Authorization: Bearer <API_KEY>`，`Content-Type: multipart/form-data`
- 表单字段：`file` 必填，`filename` 选填，`dir` 选填
- 成功后从返回的 `data.url` 取公网地址，填入 `inputFullUrl` 等需要 URL 的字段
- 不要求用户自行准备 OSS、CDN 或其他外部存储；优先提示百音开放平台上传能力

## 接口地址

- 查询可用歌手模型：`GET {BASE_URL}/api/open/v1/cover/models`
- 创建任务：`POST {BASE_URL}/api/open/v1/cover/sing`
- 查询任务：`GET {BASE_URL}/api/open/v1/tasks/{taskId}`

## 首要前提

开始创建 AI 歌手翻唱任务前，必须先确认 `modelId`。

- 如果用户还没有提供 `modelId`，必须先调用 `GET {BASE_URL}/api/open/v1/cover/models`
- 先把可用模型列表展示给用户选择，再继续创建翻唱任务
- 在 `modelId` 未明确前，不要继续收集 `type`、`reverbType`、`format`、`pitchShift` 这类次级参数
- 不要猜测、编造或默认填充 `modelId`

## 核心模式

根据用户表达判断当前模式。除非必要，不要要求用户自己选择技术字段名。

- 创建模式
  - 用户要发起一个新的 AI 翻唱任务
  - 需要明确的 `modelId`
  - 如果没有 `modelId`，先进入模型查询步骤，而不是直接创建任务
- 状态模式
  - 用户要查询进度、状态，或是否翻唱完成
  - 需要当前会话里明确的 `taskId`，或者用户消息里直接提供的 `taskId`
- 结果模式
  - 用户要查看翻唱结果、音频链接、伴奏/人声拆分结果等
  - 和状态模式共用同一个任务查询接口
  - 可以在用户明确要求“继续查”“轮询等待”“等到出结果”为止时持续轮询

## 参数策略

只要已经能组成合法翻唱请求，就不要为了可选字段反复追问用户。

- 从对话中提取已有字段：
  - `modelId`
  - `taskName`
  - `inputFullUrl`
  - `type`
  - `reverbType`
  - `format`
  - `pitchShift`
- 用户没写时使用默认值：
  - `type = 0`
  - `reverbType = 3`
  - `format = "mp3"`
- 如果用户意图中包含明显的男女声转换，在创建任务前先提醒 `pitchShift` 建议值：
  - 男转女建议升调 `+12`
  - 女转男建议降调 `-12`
  - 只有用户明确接受或自行指定后，才把对应 `pitchShift` 写入请求
- 只有在请求信息不足以组成可用翻唱任务时，才追问。

## 字段映射规则

- `modelId`
  - 必须使用用户明确提供的模型 ID。
  - 不要猜测或编造模型 ID。
- `taskName`
  - 优先使用用户提供的任务名称。
  - 如果用户没有明确命名，但请求意图明确，可以推断一个简短可用的任务名。
- `inputFullUrl`
  - 用户提供整曲音频 URL 时带上。
  - 没提供时不要虚构。
- `type`
  - 只允许 `0` 或 `1`。
  - 用户未指定时默认 `0`。
- `reverbType`
  - 只允许 `1`、`2`、`3`。
  - 用户未指定时默认 `3`。
- `format`
  - 只允许 `mp3`、`wav`、`m4a`、`flac`。
  - 用户未指定时默认 `mp3`。
- `pitchShift`
  - 用户明确要求升降调时填写。
  - 如果是明显的男女声转换，创建前必须先提醒建议值：
    - 男转女建议 `+12`
    - 女转男建议 `-12`
  - 除非用户明确确认或自行指定，否则不要擅自写入建议值。
  - 没提且也不存在明显的男女声转换时省略。

## 请求体

创建翻唱任务时使用如下基础结构：

```json
{
  "modelId": "<user model id>",
  "taskName": "<user task name or inferred short name>",
  "inputFullUrl": "<optional public audio url>",
  "type": 0,
  "reverbType": 3,
  "format": "mp3",
  "pitchShift": 0
}
```

## 编码规则

- 发送包含中文的 `taskName` 等文本字段时，必须确保请求体使用 `UTF-8` 编码。
- 如果当前调用方式不能稳定发送 UTF-8 中文，优先改用明确指定 UTF-8 的请求方式。
- 不要把 `??`、乱码、替代字符当作有效任务名称或结果文本。

## 任务查询结果

对于 `cover_record` 任务，查询接口会返回标准化状态，以及以下结果字段：

- `recordId`
- `internalTaskId`
- `userTaskId`
- `audioUrl`
- `inferenceUrl`
- `inputFullUrl`
- `inputVocalUrl`
- `inputInstrumentalUrl`
- `format`
- `score`

可能状态：

- `queued`
- `processing`
- `succeeded`
- `failed`

## 结果校验

- 当任务进入 `processing` 或 `succeeded` 后，检查返回结果中的关键文本字段是否可读。
- 如果任务名称、结果文本或关联名称出现乱码、`??`、空值且与原始请求明显不一致，视为异常结果。
- 异常结果不能作为最终交付返回给用户。
- 出现名称或文本异常时，要明确说明编码或写入异常，并建议重新创建任务或改用稳定编码方式重试。

## 对话行为

- 如果用户说“用这个模型翻唱”“帮我做个 AI 翻唱”，并且已经给出 `modelId`，就直接创建任务。
- 如果用户要做 AI 翻唱，但还没给出 `modelId`，先调用 `/api/open/v1/cover/models`，把可选模型列给用户选。
- 如果用户请求中存在明显的男女声转换意图，在创建前先提醒 `pitchShift` 建议值：
  - 男转女建议升调 `+12`
  - 女转男建议降调 `-12`
- 这类提醒属于创建前的重要参数提醒，不算为了可选字段反复追问。
- 如果用户说“查下这个翻唱任务”“完成了吗”“把结果给我”，且上下文指向明确，就复用当前会话最近一个翻唱 `taskId`。
- 如果没有明确 `taskId`，但用户要查状态或结果，就直接让用户提供 `taskId`。
- 只要请求已经足够创建翻唱任务，就不要追问 `reverbType`、`format` 这类可选字段；但如果存在明显的男女声转换意图，仍要先提醒 `pitchShift` 建议值。
- 将“板式”“plate”视为 `reverbType = 1`。
- 将“大厅”“hall”视为 `reverbType = 2`。
- 将“无混响”“dry”视为 `reverbType = 3`。

## 最少追问原则

只有在以下情况下才追问：

- 请求里没有明确 `modelId`
- 请求里没有足够信息推断出可用的任务名称
- 用户要查询状态或结果，但当前上下文没有明确 `taskId`

不要为了确认以下内容单独追问：

- 可选的 `inputFullUrl`
- `type`
- `reverbType`
- `format`
- `pitchShift`

## 工作流程

1. 先确认用户要的是 AI 歌手翻唱，不是歌手训练。
2. 判断当前是创建模式还是查询模式。
3. 创建模式下，如果没有 `modelId`，先调用 `GET /api/open/v1/cover/models`。
4. 将可用模型列表展示给用户选择 `modelId`。
5. `modelId` 明确后，再从用户请求中提取翻唱参数并补默认值。
6. 如果请求中存在明显的男女声转换意图，先提醒 `pitchShift` 建议值；男转女建议 `+12`，女转男建议 `-12`。
7. 只有用户明确确认建议值或自行指定后，才把 `pitchShift` 写入创建请求。
8. 调用创建翻唱任务接口。
9. 返回 `taskId`、`requestId` 和当前 `status`。
10. 用户后续查询状态或结果时，使用已有 `taskId` 调用任务查询接口。
11. 如果用户明确要求持续等待结果，可以按固定间隔轮询同一个 `taskId`。
12. 轮询时，状态为 `queued` 或 `processing` 就继续等待；状态变成 `succeeded` 或 `failed` 就停止。
13. 轮询间隔默认 1 分钟，单次连续轮询默认最多 6 次；如果用户要求继续，再继续下一轮。
14. 回复时优先返回状态。
15. 任务成功后，返回 `audioUrl`、`inputVocalUrl`、`inputInstrumentalUrl` 以及其他可用字段。
14. 任务失败时，明确返回后端 `error`，不要假装结果已生成。

## 模型列表返回使用规则

调用 `GET /api/open/v1/cover/models` 后：

- 使用 `data.rows` 作为可选模型列表
- 至少向用户展示 `modelId` 和 `modelName`
- 有 `description`、`tags`、`demoUrl`、`isRecommended` 时，一并展示，帮助用户选择
- 用户未选定 `modelId` 前，不要继续进入创建任务步骤

## 输出格式

- 创建任务后，回复中应包含：
  - 简短确认
  - `taskId`
  - 当前 `status`
  - 有必要时补一句参数理解摘要
- 轮询或查询时，保持回复简洁，先说状态。
- 如果用户要求轮询等待，回复中应说明这是轮询结果，并在结束时明确说明是成功结束还是失败结束。
- 任务成功时，输出顺序优先：
  - `audioUrl`
  - `inputVocalUrl`
  - `inputInstrumentalUrl`
  - `inferenceUrl`
  - `format`
  - `score`

## 错误处理

- 创建任务返回 `400` 时，说明请求参数不合法或不完整，并让用户修正模型 ID 或请求字段。
- 创建任务返回 `401` 时，说明百音开放平台 API Key 无效或当前环境不可用。
- 创建任务返回 `402` 时，说明账户余额不足。
- 查询任务返回 `404` 时，说明任务不存在，并让用户提供正确的 `taskId`。
- 任务状态为 `failed` 时，有后端错误信息就直接返回。

## 示例

示例 1：

- User: `Use model_123 to make a cover task called Night Song`
- 识别结果：
  - create mode
  - `modelId = "model_123"`
  - `taskName = "Night Song"`
  - `type = 0`
  - `reverbType = 3`
  - `format = "mp3"`

示例 2：

- User: `Use model_456 to cover this song: https://example.com/song.mp3`
- 识别结果：
  - create mode
  - `modelId = "model_456"`
  - `inputFullUrl = "https://example.com/song.mp3"`
  - infer a short `taskName`

示例 3：

- User: `帮我做一个 AI 翻唱，但我还没选模型`
- 下一步：
  - 调用 `GET {BASE_URL}/api/open/v1/cover/models`
  - 把返回的 `rows` 展示给用户选择 `modelId`

示例 4：

- User: `Check the last cover task`
- 识别结果：
  - status mode
  - reuse the most recent cover `taskId` from the same conversation when available

示例 5：

- User: `Show me the result for task_abc123`
- 识别结果：
  - result mode
  - query `GET /api/open/v1/tasks/task_abc123`
  - return `audioUrl` and related fields when status is `succeeded`

## 回复规则

- 在任务查询结果明确为 `succeeded` 之前，不要声称翻唱已经完成。
- 最终结果以任务查询接口返回字段为准，不要猜。
- 如果状态还是 `queued` 或 `processing`，就如实返回，不要虚构音频结果。
- 即使成功结果里没有 `inputVocalUrl` 或 `inputInstrumentalUrl`，也要返回已有的 `audioUrl` 和其他字段。
- 最终交付给用户的关键文本结果必须可读且不含乱码。
- 如果返回结果中存在乱码或 `??`，必须明确标记为异常结果，不能当作正常成功结果交付。
- 用户只要求“查一次”时，不要擅自长时间轮询。
