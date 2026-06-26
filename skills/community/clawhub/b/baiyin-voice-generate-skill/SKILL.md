---
name: baiyin-voice-generate-skill
description: 使用百音开放平台创建 AI 语音任务，支持文本转语音、音色克隆，并在同一 skill 内继续查询任务状态和结果链接。用于用户要生成语音、克隆音色、查询语音任务进度或下载结果时。
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

# 百音 AI 语音

把自然语言请求稳定映射为百音开放平台的语音任务请求。不要猜模型、不要猜字段类型、不要猜边界值；只使用本文明确列出的模型、枚举和规则。

## 前置要求

- `BAIYIN_API_KEY`

## 运行时配置

- `BASE_URL` 固定使用 `https://ai.hikoon.com`
- 只有 `BAIYIN_API_KEY` 缺失时，才向用户索要 API Key。

## 公网地址处理

- 当语音生成需要公网音频 URL，而用户提供的是本地文件路径、聊天附件、网盘私链或其他不可直接访问的地址时，不要只提示"需要公网 URL"。
- 直接指导用户先使用百音开放平台文件上传接口上传文件，拿到公网地址后再继续当前流程。
- 上传接口：`POST {BASE_URL}/api/open/v1/file/upload`
- 认证方式：`Authorization: Bearer <API_KEY>`，`Content-Type: multipart/form-data`
- 表单字段：`file` 必填，`filename` 选填，`dir` 选填
- 成功后从返回的 `data.url` 取公网地址，填入 `voice_url` 等需要 URL 的字段
- 不要求用户自行准备 OSS、CDN 或其他外部存储；优先提示百音开放平台上传能力

## 接口地址

- 获取音色列表：`GET {BASE_URL}/api/open/v1/voice/tones`
- 获取语音模型列表：`GET {BASE_URL}/api/open/v1/models?modelType=voice&status=1`
- 创建任务：`POST {BASE_URL}/api/open/v1/voice/generate`
- 查询任务：`GET {BASE_URL}/api/open/v1/tasks/{taskId}`

## 强约束

- `prompt` 必须是非空字符串。空字符串或缺失都会触发 `400`。
- 数值字段必须传 number，不要传 string。
- `voice_url` 只接受可访问的 `http://` 或 `https://` 公网链接。不要传本地路径、`file://`、`../` 这类路径。
- 音色列表必须静默获取，用户完全不可感知。

## 字段清单

### 顶层字段

| 字段 | 类型 | 是否必填 | 允许值 / 边界 | 说明 |
|---|---|---|---|---|
| `prompt` | string | 是 | 非空字符串 | 要合成的文本内容 |
| `modelCode` | string | 是 | 来自模型列表接口 | 语音模型标识 |

### `params` 对象字段

| 字段 | 类型 | 是否必填 | 允许值 / 边界 | 说明 |
|---|---|---|---|---|
| `params.voice_url` | string | 是 | 可访问的 `http/https` 链接 | 参考音频 URL，用于音色克隆 |
| `params.speed_level` | number | 是 | 整数 1-5 | 语速级别 |
| `params.pitch_level` | number | 是 | 整数 1-5 | 音调级别 |
| `params.emotion` | string | 是 | 开朗、沉稳、温柔、严肃、活泼、冷静、治愈 | 情感风格 |

## 字段组装规则

### `prompt`

- 用户说"帮我把这段话转成语音""朗读这段文字""配个音"时，从用户消息中提取需要合成的文本
- 如果用户没有给出具体文本内容，必须追问
- 不允许传空字符串

### `modelCode`

- 从模型列表接口 `GET {BASE_URL}/api/open/v1/models?modelType=voice&status=1` 获取
- 向用户只展示 `modelName`，不展示 `modelCode`
- 用户选择后，将对应 `modelCode` 作为请求参数传入
- 如果用户在消息里直接说了模型关键词，可以与接口返回的 `modelName` 做模糊匹配，自动映射到对应 `modelCode`
- 如果接口调用失败或返回为空，明确告知用户当前无法获取模型列表，不要使用任何兜底的固定模型数据
- 在用户未选定 `modelCode` 前，不要继续进入参数收集步骤

### `params.voice_url`

- 静默调用 `GET {BASE_URL}/api/open/v1/voice/tones` 获取音色列表，取第一条的 `audioUrl` 作为默认值
- 用户通过名称指定音色时（如"用知性女声"），从音色列表按 `name` 匹配并使用对应 `audioUrl`
- 用户说"用这个声音""参考这段音频""克隆这个音色"并提供了自定义 URL 时，使用用户提供的 URL
- 必须为可公网访问的音频文件链接

### 音色列表静默规则（重要）

- 获取音色列表必须静默进行，用户完全不可感知
- 不要在调用前、调用中、调用后向用户输出任何与"获取音色列表""查询音色""加载音色"相关的文字、提示、进度、状态或解释
- 不要把音色列表的原始数据、字段、条数暴露给用户
- 除非用户主动询问，否则最终回复中也不要主动提及本次使用的音色名称或 `voice_url`
- 音色列表调用失败时，也不要向用户报告"音色列表获取失败"

### `params.pitch_level`

- 必填，音调级别，整数 1-5
- 用户说"声音高一点""低沉一点"时映射：
  - "低沉"/"低音"→1
  - "正常"/"中音"→3
  - "高一点"/"高音"→5
- 用户未指定时默认填 3

### `params.emotion`

- 必填，情感风格
- 可选值仅限于：开朗、沉稳、温柔、严肃、活泼、冷静、治愈
- 用户未指定时默认填"冷静"
- 用户提到类似情感时映射到最接近的选项

### `params.speed_level`

- 必填，语速级别，整数 1-5
- 用户说"快一点""慢一点""正常语速"时映射：
  - "很慢"/"缓慢"→1
  - "慢速"→2
  - "正常"/"默认"/"中速"→3
  - "快一点"/"偏快"→4
  - "很快"/"快速"→5
- 用户未指定时默认填 3

## 默认值

除非用户明确指定，否则使用：

```json
{
  "params": {
    "voice_url": "<音色列表第一条的 audioUrl>",
    "speed_level": 3,
    "pitch_level": 3,
    "emotion": "冷静"
  }
}
```

## 最小安全请求体

```json
{
  "prompt": "<非空字符串>",
  "modelCode": "<来自模型列表>",
  "params": {
    "voice_url": "<可访问的音频 URL>",
    "speed_level": 3,
    "pitch_level": 3,
    "emotion": "冷静"
  }
}
```

完整请求示例：

```json
{
  "prompt": "我每天都很开心",
  "modelCode": "VoiceClone",
  "params": {
    "voice_url": "https://example.com/reference-voice.mp3",
    "speed_level": 5,
    "pitch_level": 1,
    "emotion": "治愈"
  }
}
```

## 明确的校验规则

- `prompt`
  - 必填
  - 非空字符串
- `modelCode`
  - 必填
  - 必须来自模型列表接口
- `params.voice_url`
  - 必填
  - 必须是可访问的 `http/https` 链接
- `params.speed_level`
  - 必填
  - 类型：number
  - 范围：整数 1-5
- `params.pitch_level`
  - 必填
  - 类型：number
  - 范围：整数 1-5
- `params.emotion`
  - 必填
  - 只能是：开朗、沉稳、温柔、严肃、活泼、冷静、治愈

## 模式判定

### 创建模式

适用：

- "帮我生成一段语音"
- "把这段话转成语音"
- "用这个声音朗读"

请求特征：

- 需要提供 `prompt` 和 `modelCode`
- 可选提供 `params` 中的音色、语速、音调、情感等参数

### 状态模式

适用：

- "查一下刚才那个语音任务"
- "任务进度怎么样了"

请求特征：

- 复用当前会话最近一个语音 `taskId`

### 结果模式

适用：

- "给我 task_xxx 的结果"
- "把音频链接发我"

请求特征：

- 使用用户提供的 `taskId` 查询任务
- 状态为 `succeeded` 时返回音频链接

## 最少追问原则

只有这些情况才追问：

- 用户未提供要合成的文本（`prompt` 为空）
- 用户未选择语音模型（调用模型列表接口展示选项）
- 用户要查询状态或结果，但当前上下文没有明确 `taskId`

不要为了这些事情打断用户：

- `params.voice_url`（未指定时默认取音色列表第一条）
- `params.speed_level`（未指定时默认填 3）
- `params.pitch_level`（未指定时默认填 3）
- `params.emotion`（未指定时默认填"冷静"）

## 编码规则

- 发送包含中文的 `prompt` 等文本字段时，必须确保请求体使用 `UTF-8` 编码
- 不要把 `??`、乱码、替代字符当作有效内容

## 任务状态

- `queued`：已受理，等待执行
- `processing`：生成中
- `succeeded`：生成成功
- `failed`：生成失败

轮询时回复要简短，优先返回状态。

## 错误处理

- `400`：参数不合法或不完整，让用户修正相关字段
- `401`：百音开放平台 API Key 无效或当前环境不可用
- `402`：账户余额不足
- `404` 查询任务：`taskId` 不存在，或不属于当前 API Key 所属用户
- 任务状态为 `failed` 时，优先透传后端 `error` 字段

## 示例

### 示例 1：基础生成

- 用户：`帮我生成一段语音`
- 处理：
  - 调用 `GET {BASE_URL}/api/open/v1/models?modelType=voice&status=1` 获取可用模型列表
  - 展示接口返回的模型选项，让用户选择
  - 用户选择后，使用对应 `modelCode`
  - 追问要合成的文本内容

### 示例 2：带模型指定

- 用户：`帮我把"欢迎来到百音引擎"转成语音，用基础语音模型 V1`
- 结果：
  - `prompt = "欢迎来到百音引擎"`
  - 调用模型列表接口，用"基础语音模型 V1"关键词匹配到对应 `modelCode`
  - 必填字段齐全，直接创建任务

### 示例 3：完整参数

- 用户：`生成一段治愈风格的语音，内容是"今天天气真好，适合出去走走"，语速慢一点，参考这个音频 https://example.com/voice.mp3，用情感语音模型`
- 结果：
  - `prompt = "今天天气真好，适合出去走走"`
  - 调用模型列表接口，用"情感语音模型"关键词匹配到对应 `modelCode`
  - `params.voice_url = "https://example.com/voice.mp3"`
  - `params.speed_level = 2`（慢一点）
  - `params.emotion = "治愈"`
  - 直接创建任务

### 示例 4：查询状态

- 用户：`查一下刚才那个语音任务`
- 结果：
  - 状态模式
  - 复用当前会话最近一个语音 `taskId`

### 示例 5：获取结果

- 用户：`给我 task_abc123 的结果`
- 结果：
  - 结果模式
  - 查询 `GET {BASE_URL}/api/open/v1/tasks/task_abc123`
  - 状态为 `succeeded` 时返回音频链接

## 回复约束

- 在任务查询结果明确为 `succeeded` 之前，不要声称音频已经完成
- 最终结果以任务查询接口返回字段为准，不要猜
- 如果状态还是 `queued` 或 `processing`，就如实返回，不要虚构音频结果
- 最终交付给用户的关键文本结果必须可读且不含乱码
- 不要虚构参考音频 URL
