---
name: gen-hot-video
description: >-
  通过 Flyelep 爆款视频复刻 API，基于爆款视频风格生成产品复刻视频。
  当用户要求复刻爆款视频、模仿参考视频风格生成产品视频时使用此技能。
---
# Flyelep 爆款视频复刻
通过 Flyelep AI Tool API 复刻爆款视频风格，将产品素材融合到爆款参考视频的视觉风格中。支持两种复刻模式：创意复刻（参考爆款风格和分镜重新生成）和 1:1 复刻（照搬原片镜头、动作与节奏，只替换商品、模特、服饰、人脸或背景）。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**
**注意：此接口为异步接口，只返回任务ID，需要通过 queryTaskResult 接口获取最终结果。**

## API 接口信息

- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **Content-Type**: `application/json`

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

### 创建任务

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo`
- **超时时间**: 建议 60-120 秒（获取任务结果需额外轮询，视频生成可能需要更长时间）

### 查询结果

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult`
- **超时时间**: 建议 30 秒

### 爆款链接识别（可选）

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/parseShortVideo`
- **说明**: 同步接口，把抖音、TikTok、小红书的分享链接转成可直接访问的视频地址，返回的 `videoUrl` 可直接作为 `sourceUrl`，详见下方「爆款链接识别」章节
- **超时时间**: 建议 120 秒

## 请求 Body

创建任务：
```json
{
  "replicaMode": "creative",
  "replaceUrl": "https://example.com/product_video.mp4",
  "sourceUrl": "https://example.com/hot_video.mp4",
  "prompt": "突出产品功能，增强视觉冲击力",
  "additionalPrompt": "展示产品使用场景",
  "modelType": "pro",
  "resolution": "720p",
  "ratio": "1:1",
  "duration": 10,
  "subtitle": true,
  "language": "中文简体"
}
```

查询结果：
```json
{
  "agentGenerateTaskId": "任务ID"
}
```

## 响应格式

创建任务（异步）：
```json
{
  "code": 200,
  "data": {
    "agentGenerateTaskId": "2072923591164715009"
  }
}
```

查询任务结果：
```json
{
  "code": 200,
  "data": {
    "agentGenerateTaskId": "2072923591164715009",
    "status": 2,
    "taskList": [
      {
        "taskStatus": 2,
        "executeResult": "https://example.com/result_video.mp4"
      }
    ]
  }
}
```

- `code=200` 表示调用成功
- `agentGenerateTaskId` 为异步任务ID，用于后续查询结果
- `status`（总状态）: 1-进行中，2-全部成功，3-全部失败，4-部分成功
- `taskStatus`: 0-待生成，1-生成中，2-生成成功，3-生成失败
- `executeResult`：`taskStatus=2` 时为生成的视频URL，`taskStatus=3` 时为失败原因
- 查询结果中还会返回 `estimatedPoints`（预计消耗算力）、`consumePoints`（实际消耗算力）、`createTime`、`startTime`、`finishTime`
- 将结果视频展示给用户

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| replaceUrl | - | 产品素材地址（图片/视频/音频），多个以英文逗号分隔 |
| sourceUrl | - | 爆款参考视频地址 |
| modelType | - | 模型类型：`pro`、`fast`、`ultra`、`mini` |
| resolution | - | 分辨率 |
| prompt | - | 提示词；创意复刻必填，1:1 复刻可选 |
| duration | - | 视频时长（秒），4-15秒；创意复刻必填，1:1 复刻可不传 |
| language | - | 生成语言；创意复刻必填，1:1 复刻不使用 |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| replicaMode | creative | 复刻模式：`creative`（创意复刻）/ `oneToOne`（1:1 复刻） |
| replaceType | product | 图片类型，决定把参考图里的什么换到原视频里；仅 1:1 复刻生效 |
| productSubject | - | 商品主体，如「上衣」「裤子」，最多10个字；仅 1:1 复刻生效 |
| keepMusicRhythm | true | 是否保留原视频的音乐和节奏；仅 1:1 复刻生效 |
| oralBroadcast | false | 是否口播视频；仅 1:1 复刻生效 |
| additionalPrompt | - | 补充提示词（可选） |
| ratio | - | 视频生成比例；1:1 复刻固定跟随原视频 |
| subtitle | - | 是否添加字幕，`true`/`false`；仅创意复刻生效 |

### 参数映射规则

**replicaMode**（复刻模式）：
- `creative`：创意复刻（默认），解析爆款视频的风格和分镜脚本后结合产品素材重新生成，需要 `prompt`、`duration`、`language`
- `oneToOne`：1:1 复刻，原视频直接作为参考，严格照搬镜头、动作与节奏，只把 `replaceType` 指定的内容换成参考图；不使用 `language`、`subtitle`，成片比例和时长跟随原视频
- 传其它值报「复刻模式不支持，仅支持 creative / oneToOne」

**modelType**（模型类型）：
- `pro`：Flyelep Dance 2.0（高质量）
- `fast`：Flyelep Dance 2.0 Fast（快速生成）
- `ultra`：Flyelep Dance 2.5（最高画质）
- `mini`：Flyelep Dance 2.0 Mini（轻量）
- 只接受这四个取值，大小写不敏感；传其它值报「模型类型不支持，仅支持 pro / fast / ultra」

**resolution**（分辨率）：
- 支持：`480p`、`720p`、`1080p`、`2K`、`4K`，大小写不敏感
- 不传或传其它值报「分辨率(resolution)仅支持 480p / 720p / 1080p / 2K / 4K」

**ratio**（视频比例）：
- 支持：`1:1`、`3:4`、`4:3`、`16:9`、`9:16`、`21:9`
- 1:1 复刻时传了也不生效，成片比例自动跟随原视频

**duration**（视频时长）：
- 范围：4-15秒，超出报「视频时长(duration)仅支持 4-15 秒」
- 创意复刻必填；1:1 复刻可不传，服务端按原视频真实时长成片（4-60 秒）

**language**（生成语言）：
- 仅支持：中文简体、中文繁体、英文、马来语、葡萄牙语、韩语、日语、西班牙语、俄语
- 必须原样使用上面的中文标签（例如是 `英文` 而不是 `英语`），传其它写法会被拒绝
- 创意复刻不传报「语言不能为空」；1:1 复刻不使用

**prompt / additionalPrompt**（提示词）：
- 创意复刻 `prompt` 必填，建议不超过1000个字符
- 1:1 复刻使用固定模板，`additionalPrompt`（未传时取 `prompt`）作为补充要求追加在模板后

**replaceUrl**（产品素材）：
- 产品素材地址，用于替换爆款视频中的产品，多个以英文逗号分隔，必须是 http/https 链接
- 支持图片、视频、音频，按文件后缀自动识别，**链接必须带可识别的后缀**（图片 `jpg`/`jpeg`/`png`/`gif`/`webp`/`bmp`，视频 `mp4`/`mov`/`m4v`/`webm`/`avi`/`mkv`，音频 `mp3`/`wav`/`m4a`/`aac`/`ogg`/`flac`），否则报「replaceUrl包含无法识别的参考素材格式」
- 数量上限：图片最多9张、视频最多3个、音频最多3个
- 1:1 复刻时图片张数还受 `replaceType` 限制（见下方）
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**sourceUrl**（爆款参考）：
- 爆款参考视频地址，必须是 http/https 链接
- 创意复刻：用于解析风格与分镜脚本，成片时长由 `duration` 决定
- 1:1 复刻：原视频最长 60 秒（超过单次生成上限的部分自动分段生成后拼接），单条不能短于 2 秒；`replaceUrl` 里另带参考视频时，所有参考视频总时长不能超过 15 秒（`ultra` 为 30 秒）
- 用户给的是抖音、TikTok、小红书分享链接时，先按「爆款链接识别」章节转成视频地址
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**replaceType**（图片类型，仅 1:1 复刻生效）：
- `product`：商品（默认），参考图最多1张
- `preciseProduct`：精准商品，可传多角度图，最多3张
- `model`：模特，整体替换出镜人物，最多1张
- `precisePerson`：精准人物，替换人物、保留原服装，最多1张
- `face`：人脸，只替换五官、脸型和发型，最多1张
- `clothing`：服饰，只换衣服，最多2张（正反面）
- `background`：背景，只换主体之外的环境，最多1张
- 每次只能传一个取值，传其它值报「图片类型不支持，仅支持 model / clothing / face / background / product / preciseProduct / precisePerson」

**productSubject / keepMusicRhythm / oralBroadcast**（仅 1:1 复刻生效）：
- `productSubject`：直接指定商品主体（最多10个字），不传时由服务端识图得出
- `keepMusicRhythm`：默认 `true`，舞蹈、卡点、BGM 类视频建议保留
- `oralBroadcast`：默认 `false`，为 `true` 时要求人物对镜讲解且口型与语音同步

**subtitle**（字幕控制，仅创意复刻生效）：
- `true`：添加字幕
- `false` 或不传：不添加字幕
- 通过追加提示词可控制字幕内容

## 异步任务流程

> **重要**：本接口为异步接口，必须**先调用主接口获取 `agentGenerateTaskId`，然后调用 `queryTaskResult` 接口轮询任务结果**，不能省略轮询步骤。

1. 调用主接口（`generateHotVideo`）提交任务，从响应中获取 `agentGenerateTaskId`
2. 使用 `agentGenerateTaskId` 调用 `queryTaskResult` 接口轮询任务结果（建议每5-10秒查询一次）
3. 当 `taskStatus=2` 时，表示生成成功，获取 `executeResult` 结果
4. 当 `taskStatus=3` 时，表示生成失败，`executeResult` 为失败原因

> **轮询策略**：视频生成耗时较长，超时时间建议设置为10分钟；1:1 复刻长视频需分段生成，可适当放宽

## 爆款链接识别

用户给的是抖音、TikTok、小红书的分享链接或整段分享文案，而不是可直接下载的视频地址时，先调用本接口换取视频地址，再填入 `sourceUrl`。

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/parseShortVideo`
- **认证方式**: 请求头传 `secretKey`，与本技能使用同一个密钥
- **请求 Body**: `{"url": "分享链接或包含链接的分享文案"}`，`url` 必填，不传报「链接不能为空」
- 同步返回，识别并转存成功才扣一次算力，失败不扣；只支持抖音、TikTok、小红书链接

成功响应：
```json
{
  "code": 200,
  "data": {
    "videoUrl": "https://example.com/parsed_video.mp4",
    "thumbnailUrl": "https://example.com/parsed_cover.jpg"
  }
}
```

- `videoUrl`：转存后的视频地址，直接作为 `generateHotVideo` 的 `sourceUrl`
- `thumbnailUrl`：视频封面，可能为空

```bash
# macOS/Linux（Windows 按「调用示例」的说明先写入 payload_temp.json 再发送）
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/parseShortVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"url":"https://v.douyin.com/xxxxxx/"}'
```

## 本地文件上传

用户提供的是本地文件路径而不是公网直链时，先把文件上传换取直链，再调用本接口。已安装 `file-upload` 技能时以该技能为准；未安装时按下面的说明直接调用上传接口。

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload`
- **请求方式**: `multipart/form-data`，文件字段名固定为 `file`，单次只能上传一个文件，多个文件并发调用多次
- **认证方式**: 请求头传 `secretKey`，与本技能使用同一个密钥
- **超时时间**: 视频体积大、上传耗时长，建议 300 秒
- **不要手动设置 `Content-Type` 请求头**，让 HTTP 客户端自动生成带 boundary 的值，手写会导致服务端解析失败
- 视频仅支持 `mp4`、`mov`、`m4v`、`webm`、`avi`、`mkv`。**文件名必须带正确后缀**，服务端靠后缀判断格式，`mov`、`webm`、`mkv`、`m4v` 缺后缀时无法靠 Content-Type 回退，会被判为格式不支持
- 视频不做内容审核，直接入库，不要上传来源不明的内容
- 原文件名不会出现在 URL 里，中文名、空格、特殊字符都能直接上传，不需要提前改名
- 上传不消耗算力，但服务端不做去重：同一个文件在一次任务里只上传一次，记下 `fullPath` 复用

成功响应取 `data.fullPath` 作为公网直链（不带签名，按 24 小时限时链接对待，拿到后直接用于本次调用，不要长期保存）：

```json
{
  "code": 200,
  "msg": null,
  "data": {
    "relativePath": "oss_ai_agent_h_24/2026-11-12/3f2a9c1b7d84e6f5a0123b4c5d6e7f80.mp4",
    "fullPath": "https://oss-agent-7346.flyelep.cn/oss_ai_agent_h_24/2026-11-12/3f2a9c1b7d84e6f5a0123b4c5d6e7f80.mp4",
    "serviceProvider": null
  }
}
```

判断成功只看 `code`，业务失败时 HTTP 状态码仍是 200，`code` 为 500 或 9999，原因在 `msg` 里。

```bash
# Windows/PowerShell（用 curl.exe，PowerShell 里的 curl 是 Invoke-WebRequest 的别名）
curl.exe -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload" -H "secretKey: 你的密钥" --max-time 300 -F "file=@C:/path/to/reference.mp4"

# macOS/Linux
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload" -H "secretKey: 你的密钥" --max-time 300 -F "file=@./reference.mp4"
```

拿到 `code=9999`、`msg` 为 `服务繁忙，请稍后再试` 时，先自查三项：是否漏了 `secretKey` 请求头、表单字段名是否为 `file`、文件是否超出服务端体积上限（超限只会返回这条通用错误，此时应先压缩或裁剪再重试，不要原样重传）。密钥、格式、体积类错误重试无效，只有网络超时、5xx 和存储类异常值得重试。

## 调用示例

> **跨平台调用说明**：
> - 请求头必须包含 `Content-Type: application/json; charset=utf-8` 和 `secretKey`
> - **Windows/PowerShell**：因 GBK 编码问题，必须先将 JSON 写入临时文件 `payload_temp.json`（UTF-8 无 BOM），再用 `curl.exe --% --data-binary @payload_temp.json` 发送请求。使用 Write 工具创建文件，或用 .NET API `[System.IO.File]::WriteAllText("payload_temp.json", $json, [System.Text.UTF8Encoding]::new($false))`。调用后用 `rm payload_temp.json` 清理。
> - **macOS/Linux**：bash/zsh 默认 UTF-8，可直接内联 JSON：`curl -X POST URL -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --data-binary 'JSON单行内容'`

### 示例 1：完整流程 - 提交任务并查询结果

**前置步骤**：向用户索取产品素材视频和爆款参考视频的路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "replaceUrl": "https://example.com/product_video.mp4",
  "sourceUrl": "https://example.com/hot_video.mp4",
  "prompt": "突出产品功能，增强视觉冲击力",
  "modelType": "pro",
  "resolution": "720p",
  "ratio": "1:1",
  "duration": 10,
  "subtitle": true,
  "language": "中文简体"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"replaceUrl":"https://example.com/product_video.mp4","sourceUrl":"https://example.com/hot_video.mp4","prompt":"突出产品功能，增强视觉冲击力","modelType":"pro","resolution":"720p","ratio":"1:1","duration":10,"subtitle":true,"language":"中文简体"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行创建任务请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

步骤 4：使用返回的 `agentGenerateTaskId` 创建查询请求 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "agentGenerateTaskId": "2072923591164715009"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"agentGenerateTaskId":"2072923591164715009"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 5：执行查询请求（每5-10秒轮询，直到 `taskStatus=2`）：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 30 --data-binary @payload_temp.json
```

步骤 6：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：

创建任务：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"replaceUrl":"https://example.com/product_video.mp4","sourceUrl":"https://example.com/hot_video.mp4","prompt":"突出产品功能，增强视觉冲击力","modelType":"pro","resolution":"720p","ratio":"1:1","duration":10,"subtitle":true,"language":"中文简体"}'
```

查询结果（每5-10秒轮询，直到 `taskStatus=2`）：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 30 --data-binary '{"agentGenerateTaskId":"2072923591164715009"}'
```

### 示例 2：快速模式复刻（fast模型）

**前置步骤**：向用户索取产品素材视频和爆款参考视频的路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "replaceUrl": "https://example.com/product_video.mp4",
  "sourceUrl": "https://example.com/hot_video.mp4",
  "prompt": "展示产品卖点，节奏紧凑",
  "additionalPrompt": "快节奏剪辑，突出关键特性",
  "modelType": "fast",
  "resolution": "480p",
  "ratio": "9:16",
  "duration": 6,
  "subtitle": true,
  "language": "英文"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"replaceUrl":"https://example.com/product_video.mp4","sourceUrl":"https://example.com/hot_video.mp4","prompt":"展示产品卖点，节奏紧凑","additionalPrompt":"快节奏剪辑，突出关键特性","modelType":"fast","resolution":"480p","ratio":"9:16","duration":6,"subtitle":true,"language":"英文"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行创建任务请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

步骤 4：使用返回的 `agentGenerateTaskId` 查询结果（参考示例 1 步骤 4-6）

**macOS/Linux**：

创建任务：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"replaceUrl":"https://example.com/product_video.mp4","sourceUrl":"https://example.com/hot_video.mp4","prompt":"展示产品卖点，节奏紧凑","additionalPrompt":"快节奏剪辑，突出关键特性","modelType":"fast","resolution":"480p","ratio":"9:16","duration":6,"subtitle":true,"language":"英文"}'
```

查询结果（参考示例 1 的查询结果命令，替换 `agentGenerateTaskId`）

### 示例 3：1:1 复刻（替换商品）

**前置步骤**：向用户索取商品图片和爆款原视频的路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链；如用户提供的是分享链接，先按「爆款链接识别」章节换取视频地址。

1:1 复刻不需要 `language`，`duration` 可不传（按原视频时长成片），`ratio` 跟随原视频。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "replicaMode": "oneToOne",
  "replaceType": "product",
  "replaceUrl": "https://example.com/product.png",
  "sourceUrl": "https://example.com/hot_video.mp4",
  "productSubject": "保温杯",
  "modelType": "pro",
  "resolution": "720p"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"replicaMode":"oneToOne","replaceType":"product","replaceUrl":"https://example.com/product.png","sourceUrl":"https://example.com/hot_video.mp4","productSubject":"保温杯","modelType":"pro","resolution":"720p"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行创建任务请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

步骤 4：使用返回的 `agentGenerateTaskId` 查询结果（参考示例 1 步骤 4-6）

**macOS/Linux**：

创建任务：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"replicaMode":"oneToOne","replaceType":"product","replaceUrl":"https://example.com/product.png","sourceUrl":"https://example.com/hot_video.mp4","productSubject":"保温杯","modelType":"pro","resolution":"720p"}'
```

查询结果（参考示例 1 的查询结果命令，替换 `agentGenerateTaskId`）

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `参考素材不能为空` / `原视频不能为空` / `...地址格式不合法，必须为 http/https 链接` | 补传 `replaceUrl`、`sourceUrl`，且必须是 http/https 公网链接 |
| `replaceUrl包含无法识别的参考素材格式` | 素材链接缺少可识别的文件后缀，重新上传或换用带后缀的直链 |
| `参考图片(replaceUrl)最多支持9张` / `参考视频(replaceUrl)最多支持3个` / `参考音频(replaceUrl)最多支持3个` | 减少素材数量 |
| `xx类型的参考图片(replaceUrl)最多支持N张` | 1:1 复刻按 `replaceType` 限制参考图张数，减少图片 |
| `1:1复刻的参考视频总时长不能超过60秒` / `不能短于2秒` / `带额外参考视频时，参考视频总时长不能超过N秒` | 裁剪或更换原视频，或去掉 `replaceUrl` 里的额外视频 |
| `模型类型不能为空` / `模型类型不支持` | 改用 `pro`、`fast`、`ultra` 或 `mini` |
| `分辨率(resolution)仅支持 480p / 720p / 1080p / 2K / 4K` | 补传或改正分辨率 |
| `视频时长(duration)仅支持 4-15 秒` / `视频时长(duration)必须大于0` | 视频时长需在4-15秒之间；创意复刻必须传 |
| `语言不能为空` / `语言不支持` | 创意复刻必须传 `language`，并使用支持的中文标签 |
| `提示词不能为空` | 创意复刻必须传 `prompt` |
| 服务繁忙（9999错误码） | 稍后重试 |
| taskStatus=3 生成失败 | 查看 `executeResult` 中的失败原因（如「原片中未识别到需要替换的商品」），尝试更换素材、替换类型或调整prompt |
| 视频生成超时 | 视频生成耗时较长，增大超时时间并继续轮询 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集产品素材 URL 和爆款参考视频 URL（如用户提供本地文件，先按「本地文件上传」章节换取公网直链；如提供分享链接，先按「爆款链接识别」章节换取视频地址）
3. 与用户确认复刻模式 `replicaMode`：创意复刻构造 `prompt` 和 `additionalPrompt`，选择 `modelType`、`resolution`、`ratio`、`duration`、`language`；1:1 复刻确认 `replaceType`，选择 `modelType`、`resolution`
4. 在请求头中传入 `secretKey`，调用创建任务接口，获取 `agentGenerateTaskId`
5. 使用 `agentGenerateTaskId` 轮询查询结果接口（每5-10秒一次），直到 `taskStatus=2`
6. 将返回的结果视频展示给用户

复刻时，prompt 应指导AI：
- 保持爆款视频的整体风格、节奏和视觉效果
- 将产品自然地融入到场景中
- 突出产品卖点和关键信息
- 保持流畅的动态效果

**示例prompt：**
- "保持爆款视频的节奏感，将产品自然融入场景"
- "突出产品功能展示，配合动态视觉效果"
- "延续原视频的电商促销风格，产品主体突出"
- "展示产品使用场景，营造氛围感染力"

**additionalPrompt 示例（补充提示词）：**
- "快节奏剪辑，突出关键特性"
- "配合字幕和品牌logo"
- "转场流畅，视觉冲击力强"
