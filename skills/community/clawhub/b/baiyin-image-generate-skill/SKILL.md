---
name: baiyin-image-generate-skill
description: 图片生成能力，支持百音开放平台文生图和图生图调用。Use when: (1) 用户希望通过百音开放平台生成图片，(2) 用户希望基于参考图生成变体或重绘，(3) 用户希望查询图片任务进度并返回最终图片链接。
metadata:
  capability: "image.generate"
  api_endpoint: "/api/open/v1/image/generate"
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

# Image Generate Skill

图片生成能力，支持通过百音开放平台发起图片生成任务、查询任务状态，并返回最终图片链接。

## 前置要求

- `BAIYIN_API_KEY`

## 运行时配置

- `BASE_URL` 固定使用 `https://ai.hikoon.com`
- 只有 `BAIYIN_API_KEY` 缺失时，才向用户索要 API Key。

## 公网地址处理

- 当图生图或其他参数需要公网图片 URL，而用户提供的是本地文件路径、聊天附件、网盘私链或其他不可直接访问的地址时，不要只提示“需要公网 URL”。
- 直接指导用户先使用百音开放平台文件上传接口上传文件，拿到公网地址后再继续当前流程。
- 上传接口：`POST {BASE_URL}/api/open/v1/file/upload`
- 认证方式：`Authorization: Bearer <API_KEY>`，`Content-Type: multipart/form-data`
- 表单字段：`file` 必填
- 开放平台上传接口不支持自定义文件名，也不支持自定义文件夹；文件名与目录均由服务端自动处理
- 成功后从返回的 `data.url` 取公网地址，填入当前模型真实支持的参考图字段
- 不要求用户自行准备 OSS、CDN 或其他外部存储；优先提示百音开放平台上传能力

## 认证方式

使用 API Key 认证：

```http
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

## 接口列表

- 创建任务：`POST {BASE_URL}/api/open/v1/image/generate`
- 查询任务：`GET {BASE_URL}/api/open/v1/tasks/{taskId}`

## 固定模型

图片生成只使用以下两个固定 `modelCode`：

- `nano-banana-2`
- `kling_v3_omni_image`

如果用户未指定 `modelCode`，只允许在这两个固定值里引导用户选择，不要再去查询模型列表。

## 固定参数

### `nano-banana-2`

- `prompt`
  - 必填
- `modelCode`
  - 固定传 `nano-banana-2`
- `resolution`
  - 必填
  - 只允许：`1`、`2`、`4`
- `aspect_ratio`
  - 必填
  - 只允许：`1:1`、`4:3`、`3:2`、`16:9`、`21:9`、`3:4`、`9:16`、`2:3`、`5:4`、`4:5`、`auto`
- `multi_image`
  - 选填
  - 必须是图片 URL 数组
  - 每个元素都必须是公网可访问的图片地址
  - 不允许 `base64`
  - 不允许本地图片路径

### `kling_v3_omni_image`

- `prompt`
  - 必填
- `modelCode`
  - 固定传 `kling_v3_omni_image`
- `resolution`
  - 必填
  - 只允许：`1`、`2`、`4`
- `aspect_ratio`
  - 必填
  - 只允许：`1:1`、`4:3`、`3:2`、`16:9`、`21:9`、`3:4`、`9:16`、`2:3`
- `multi_image`
  - 选填
  - 必须是图片 URL 数组
  - 每个元素都必须是公网可访问的图片地址
  - 不允许 `base64`
  - 不允许本地图片路径

## 参数交互规则

- 参数收集只围绕固定字段进行：`modelCode`、`prompt`、`resolution`、`aspect_ratio`、`multi_image`
- 不要再扩展其他模式字段，不要再引入额外的图片参数名
- `modelCode`、`prompt`、`resolution`、`aspect_ratio` 都确认后再创建任务
- `multi_image` 只有在用户明确提供参考图时才传
- `resolution` 和 `aspect_ratio` 只允许使用当前固定枚举值；如果用户没有明确指定，必须先让用户选择
- `multi_image` 必须是图片 URL 数组，不能传单个字符串，也不能把多个 URL 拼成逗号分隔字符串
- `multi_image` 中每个 URL 都必须是公网可访问地址，不允许 `base64` 和本地图片路径
- 在所有必填参数和用户关心的可选参数确认前，不要创建任务

## 请求体

对外使用时，`modelCode` 只能是 `nano-banana-2` 或 `kling_v3_omni_image`。

```json
{
  "prompt": "a white cat sitting by the window, warm morning light, cinematic",
  "modelCode": "nano-banana-2",
  "multi_image": [
    "https://example.com/reference-1.jpg",
    "https://example.com/reference-2.jpg"
  ],
  "aspect_ratio": "1:1",
  "resolution": "2"
}
```

## 参数说明

- `prompt`
  - 必填
  - 图片生成提示词
- `modelCode`
  - 必填
  - 只允许 `nano-banana-2` 或 `kling_v3_omni_image`
- `multi_image`
  - 选填
  - 必须是可公网访问的图片 URL 数组
  - 不允许 `base64`
  - 不允许本地图片路径
- `aspect_ratio`
  - 必填
  - 取值必须符合当前固定模型支持的枚举列表
- `resolution`
  - 必填
  - 只允许：`1`、`2`、`4`

## URL 校验规则

当 `multi_image` 有值时，收到用户回复后按顺序校验：

1. **本地文件检测与自动上传**
   - 判断逻辑采用反向检测
   - 若值以 `http://` 或 `https://` 开头，跳过上传，直接进入下一步格式校验
   - 否则，一律视为本地路径，调用文件上传
   - 从返回 JSON 的 `data.url` 取公网地址
   - 上传成功后，自动替换为公网 URL 再继续后续流程，无需用户再次操作
   - 上传失败时，提示错误并重新索要

2. **格式校验**
   - 最终 URL 必须以 `http://` 或 `https://` 开头

3. **数量校验**
   - `multi_image` 最多允许 3 张参考图

## 参数策略

- 始终保留用户在 `prompt` 里的核心视觉意图。
- 如果用户没给 `modelCode`，只允许在 `nano-banana-2` 和 `kling_v3_omni_image` 之间引导选择。
- `resolution` 和 `aspect_ratio` 都是必填，必须让用户在固定枚举内明确选择。
- 用户明确需要参考图时，才传 `multi_image`。
- 不要虚构参考图 URL。
- 不要把多个参考图 URL 拼成一个字符串。
- `multi_image` 有值时，先按 URL 校验规则处理；本地路径需要先自动上传，再替换为公网 URL。

## 映射规则

- 场景、风格、情绪、灯光、构图、镜头语言、时代感、材质和画风要合并成一条干净的 `prompt`。
- 用户指定具体模型时，`modelCode` 只能是两个固定值之一。
- 用户请求海报、壁纸、竖版封面、横幅等内容时，根据固定枚举设置 `aspect_ratio`。
- 用户说“参考这几张图”“用多张图融合”“多图参考”时，提交时必须传 URL 数组，例如 `"multi_image": ["url1", "url2"]`，不要传 `"multi_image": "url1,url2"`。

## 追问最小化

只有在以下情况才追问：

- 用户尚未提供 `modelCode`
- 用户输入不足以形成可执行的 `prompt`
- 用户缺少 `resolution`
- 用户缺少 `aspect_ratio`
- 用户要做参考图生成，但没有提供可公网访问的图片 URL
- 用户要查进度或取结果，但上下文里没有可用的 `taskId`

以下情况不要追问：

- `modelCode`、`resolution`、`aspect_ratio` 已明确后，直接进入创建任务
- 不要跳回去查询模型列表或参数接口

## 工作流

1. 判断用户要的是图片生成，而不是视频生成或数字人能力。
2. 如果用户未提供 `modelCode`，引导用户在 `nano-banana-2` 和 `kling_v3_omni_image` 之间选择。
3. 收集 `prompt`、`resolution`、`aspect_ratio`。
4. 如果用户需要参考图生成，再收集 `multi_image`。
5. 按 URL 校验规则处理 `multi_image`：本地路径先自动上传，再校验格式与数量。
6. 按固定字段组装请求体并创建任务。
7. 返回 `taskId`、`requestId` 和当前 `status`。
8. 用户追问进度或结果时，调用任务查询接口。
9. 任务成功后，优先返回 `imageUrl`，有多张时再返回完整 `images`。

## 创建任务返回示例

```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    "requestId": "req_xxx",
    "taskId": "task_xxx",
    "capability": "image.generate",
    "status": "queued"
  }
}
```

## 查询任务返回示例

图片任务成功后会归一化为如下结构：

```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    "requestId": "req_xxx",
    "taskId": "task_xxx",
    "capability": "image.generate",
    "status": "succeeded",
    "result": {
      "taskId": 1903,
      "internalTaskId": "hk_ai_task_001",
      "modelId": 701,
      "imageUrl": "https://cdn.example.com/image/result-1.jpg",
      "images": [
        "https://cdn.example.com/image/result-1.jpg",
        "https://cdn.example.com/image/result-2.jpg"
      ],
      "progress": 100,
      "raw": [
        {
          "image": "https://cdn.example.com/image/result-1.jpg"
        }
      ]
    },
    "error": null,
    "billing": null
  }
}
```

## 状态说明

- `queued`：已受理，等待执行
- `processing`：生成中
- `succeeded`：生成成功
- `failed`：生成失败

轮询时回复要简短，优先返回状态。

## 输出格式

- 创建任务后返回：
  - 简短确认语
  - `taskId`
  - 当前 `status`
  - 必要时补充本次解析出的关键参数
- 轮询时返回：
  - 当前 `status`
  - 可用时返回 `progress`
- 成功后返回：
  - 优先返回 `imageUrl`
  - 多图时再返回完整 `images`

## 错误处理

- 创建任务返回 `400` 时，说明请求参数不合法或当前模型不支持这些参数。
- 创建任务返回 `401` 时，说明 Open API Key 无效或当前环境未配置。
- 查询任务返回 `404` 或 `TASK_NOT_FOUND` 时，说明任务不存在，或不属于当前 API Key 所属用户。
- 后端提示模型不存在或未启用时，提示调用方更换 `modelId` 或 `modelCode`。
- 任务状态为 `failed` 时，优先透传后端 `error` 字段。

## 交互约束

- 用户第一次提出图片生成需求时，优先检查是否已经提供 `modelCode`。
- 如果没有 `modelCode`，只允许在两个固定模型里让用户选。
- `modelCode` 确认后，继续收集 `resolution` 和 `aspect_ratio`。
- 在 `resolution` 和 `aspect_ratio` 未确认前，不要创建任务。
- 在 `modelCode` 缺失时，不要擅自用默认模型继续执行。
- 不要再查询图片模型列表接口。
- 不要再查询图片模型参数接口。

## 示例

示例 1：

- 用户：`生成一张日出时白猫坐在窗边的电影感海报`
- 正确回复：
  - `请先在两个固定模型里选一个 modelCode：nano-banana-2 或 kling_v3_omni_image。选好后我再继续收集 resolution 和 aspect_ratio。`

示例 2：

- 用户：`modelCode 用 nano-banana-2，生成一张日出时白猫坐在窗边的电影感海报`
- 正确回复：
  - `已确认 modelCode = nano-banana-2。请再确认 resolution（1/2/4）和 aspect_ratio（1:1、4:3、3:2、16:9、21:9、3:4、9:16、2:3、5:4、4:5、auto）。`

示例 3：

- 用户：`用这张商品图生成一张干净的电商主图`
- 正确回复：
  - `请先在两个固定模型里选一个 modelCode：nano-banana-2 或 kling_v3_omni_image。若要带参考图，请提供公网可访问的图片 URL 数组，不要传 base64 或本地路径。`

示例 4：

- 用户：`modelCode 用 kling_v3_omni_image，用这几张商品图生成一张干净的电商主图`
- 正确回复：
  - `已确认 modelCode = kling_v3_omni_image。请再确认 resolution（1/2/4）、aspect_ratio（1:1、4:3、3:2、16:9、21:9、3:4、9:16、2:3），并提供 multi_image 数组。`

示例 5：

- 用户：`modelCode 用 flux-dev`
- 正确回复：
  - `当前图片生成只支持两个固定 modelCode：nano-banana-2 和 kling_v3_omni_image，请改为其中一个。`

示例 6：

- 用户：`我要生成图片，但是不知道选哪个模型`
- 下一步：
  - 告知用户只支持 `nano-banana-2` 和 `kling_v3_omni_image`
  - 让用户二选一

示例 7：

- 用户：`modelCode 用 nano-banana-2`
- 下一步：
  - 继续收集 `resolution`
  - 继续收集 `aspect_ratio`

示例 8：

- 用户：`帮我查询 task_123456 的最终图片`
- 操作：
  - 调用 `GET {BASE_URL}/api/open/v1/tasks/task_123456`
  - 如果 `status = succeeded`，返回 `imageUrl` 和 `images`
