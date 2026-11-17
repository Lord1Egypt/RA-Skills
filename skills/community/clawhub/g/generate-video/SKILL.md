---
name: generate-video
description: >-
  通过 Flyelep 异步生成视频 API，根据文本提示词生成产品视频或创意视频。
  当用户要求生成视频、AI生成视频、文本转视频、根据描述生成视频时使用此技能。
---
# Flyelep 异步生成视频

通过 Flyelep AI Tool API 异步生成视频，支持基于文本提示词创建产品展示视频或创意视频。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**
**注意：此接口为异步接口，只返回任务ID，需要通过 queryTaskResult 接口获取最终结果。**

## API 接口信息

### 创建任务

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **超时时间**: 建议 60-120 秒

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：`secretKey` 必须放在请求头中，这是 AI 工具接口的统一鉴权要求。不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

### 查询结果

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult`
- **Content-Type**: `application/json`
- **认证方式**: 在请求 Header 中传入 `secretKey`
- **说明**: 异步接口，需轮询获取最终视频 URL（视频生成耗时较长，整体轮询超时建议 20 分钟）

## 请求 Body

创建任务：
```json
{
  "query": "为这款智能手表制作一个展示视频，突出运动监测功能",
  "platformType": "Amazon",
  "languageType": "英语",
  "videoModelType": "pro",
  "aspectRatio": "16:9",
  "needVoice": true,
  "duration": 10,
  "resolution": "720p",
  "videoTag": "主图视频",
  "referenceImageStr": "https://example.com/product1.png,https://example.com/product2.png"
}
```

查询结果：
```json
{
  "agentGenerateTaskId": "创建任务返回的任务ID"
}
```

## 响应格式

提交请求（异步）：
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
- `taskStatus`: 0-待生成，1-生成中，2-生成成功，3-生成失败
- `executeResult` 为生成的视频URL
- 将结果视频展示给用户

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | string(0,1000) | - | 视频生成的具体需求描述（最多1000个字符长度） |
| duration | Integer | - | 视频时长（单位：秒，取值 4-60；超过单段模型上限的部分由工作流拆分为多段拼接） |

> 服务端只强校验 `duration`（4-60 秒）。下表字段虽非强校验，但直接决定成片效果，调用前应与用户确认。

### 建议确认的参数

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| platformType | String | Amazon | 平台类型 |
| languageType | String | 英语 | 语言 |
| videoModelType | String | pro | 视频模型档位 |
| needVoice | Boolean | - | 是否生成配音音频 |
| resolution | String | - | 分辨率 |
| videoTag | String | - | 视频业务标签 |

### 可选参数

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| aspectRatio | String | adaptive | 画面比例 |
| needText | Boolean | false | 是否需要字幕 |
| referenceImageStr | String | - | 参考图片，多个以英文逗号分隔 |
| referenceVideoStr | String | - | 参考视频，多个以英文逗号分隔 |
| referenceAudioStr | String | - | 参考音频，多个以英文逗号分隔 |
| firstFrame | String | - | 首帧图片 URL |
| lastFrame | String | - | 尾帧图片 URL |

### 参数映射规则

#### query（需求描述）
- 用户对视频的具体生成需求
- 最多1000个字符长度
- 保留用户原始意图，不要改写成另一个主题

#### platformType（平台类型）
支持以下平台：
- 跨境电商：`Amazon`、`temu`、`Shopee`、`TikTok Shop`、`AliExpress`、`阿里巴巴国际站`、`OZON`、`Lazada`、`DHgate`、`Coupang`、`11Street`、`Wayfair`、`Etsy`、`Noon`、`eBay`
- 中文电商：`淘宝`、`京东`、`拼多多`、`1688`、`小红书`、`抖音`
- 默认值：`Amazon`

#### languageType（语言类型）
- 支持：`英语`、`中文简体`
- 默认值：`英语`

#### videoModelType（视频模型）
- `pro`：Flyelep Video 2.0 Pro（seedance 2.0，高质量，默认）
- `fast`：Flyelep Video 2.0（seedance 2.0 fast，快速生成）
- `ultra`：Flyelep Video 2.5（seedance 2.5，最高画质）
- 只接受这三个取值，大小写不敏感；不传时按 `pro` 处理，传其它值接口报「videoModelType 仅支持 pro / fast / ultra」

#### aspectRatio（画面比例）
- `adaptive`：智能比例（默认）
- `1:1`、`4:3`、`3:4`、`16:9`、`9:16`、`21:9`

#### needVoice（配音控制）
- `true`：有配音
- `false`：无配音

#### needText（字幕控制）
- `true`：生成字幕
- `false` 或不传：不生成字幕

#### duration（视频时长）
- 范围：4-60 秒，单位为秒
- 小于 4 秒报「视频时长 duration 最少为 4 秒」，大于 60 秒报「视频时长 duration 最多为 60 秒」
- 超过单段模型上限的时长由工作流自动拆分为多段分镜后拼接，因此长视频耗时明显更久，轮询超时要放宽

#### resolution（分辨率）
- 支持：`480p`、`720p`、`1080p`、`2K`、`4K`

#### videoTag（视频业务标签）
- `主图视频`：产品主图展示
- `种草视频`：产品种草推荐
- `品牌宣传`：品牌形象宣传

#### 生成方式
- 全能参考模式：使用参考图片、视频、音频生成视频，用户可以提供参考图片、视频、音频，但也可以不提供，此时视频会根据这些参考内容生成。
- 首尾帧模式：使用首帧图片、尾帧图片生成视频，用户必须提供首帧图片、尾帧图片，视频会根据这些图片生成。
- 在提交请求前，请询问用户使用哪种模式。

#### referenceImageStr（参考图片）
- 当用户指定使用全能参考模式的时候，才可以使用，但可以为空；如果是首尾帧模式的时候，此参数必须为空，不能使用
- 多个以英文逗号分隔
- 最多6张图片，单个不超过10MB
- **注意**：图片、视频和音频文件总数不能超出6个
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

#### referenceVideoStr（参考视频）
- 当用户指定使用全能参考模式的时候，才可以使用，但可以为空；如果是首尾帧模式的时候，此参数必须为空，不能使用
- 多个以英文逗号分隔
- 最多3条视频，单个不超过50MB
- 总时长不能超过15秒
- **禁止人像**
- **注意**：图片、视频和音频文件总数不能超出6个
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

#### referenceAudioStr（参考音频）
- 当用户指定使用全能参考模式的时候，才可以使用，但可以为空；如果是首尾帧模式的时候，此参数必须为空，不能使用
- 多个以英文逗号分隔
- 最多3条音频，单个不超过50MB
- 总时长不能超过15秒
- **注意**：图片、视频和音频文件总数不能超出6个
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

#### firstFrame（首帧图片）
- 当用户指定使用首尾帧模式的时候，才可以使用，此时要求该参数不能为空
- 只能上传一张图片
- **重要**：首帧图片不能同图片、视频、音频一起使用
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

#### lastFrame（尾帧图片）
- 当用户指定使用首尾帧模式的时候，才可以使用，此时要求该参数不能为空
- 只能上传一张图片
- **重要**：尾帧图片不能同图片、视频、音频一起使用
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

## 异步任务流程

> **重要**：本接口为异步接口，必须**先调用主接口获取 `agentGenerateTaskId`，然后调用 `queryTaskResult` 接口轮询任务结果**，不能省略轮询步骤。

1. 调用主接口（`generateVideo`）提交任务，从响应中获取 `agentGenerateTaskId`
2. 使用 `agentGenerateTaskId` 调用 `queryTaskResult` 接口轮询任务结果（建议每 5-10 秒查询一次，视频生成耗时较长，整体轮询超时建议 20 分钟）
3. 当 `taskStatus=2` 时，表示生成成功，获取 `executeResult` 结果
4. 当 `taskStatus=3` 时，表示生成失败

## 本地文件上传

用户提供的是本地文件路径而不是公网直链时，先把文件上传换取直链，再调用本接口。已安装 `file-upload` 技能时以该技能为准；未安装时按下面的说明直接调用上传接口。

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload`
- **请求方式**: `multipart/form-data`，文件字段名固定为 `file`，单次只能上传一个文件，多个文件并发调用多次
- **认证方式**: 请求头传 `secretKey`，与本技能使用同一个密钥
- **超时时间**: 图片建议 60-120 秒；视频、音频体积大，建议 300 秒
- **不要手动设置 `Content-Type` 请求头**，让 HTTP 客户端自动生成带 boundary 的值，手写会导致服务端解析失败
- 支持格式：图片 `bmp`、`gif`、`jpg`、`jpeg`、`png`；视频 `mp4`、`mov`、`m4v`、`webm`、`avi`、`mkv`；音频 `mp3`、`wav`、`m4a`、`aac`、`ogg`、`flac`。图片的 `webp` 不支持，需先转成 `png` 或 `jpg`
- **文件名必须带正确后缀**，服务端靠后缀判断格式。`mov`、`webm`、`mkv`、`m4v` 和全部音频格式无法靠 Content-Type 回退，缺后缀会被判为格式不支持
- 图片入桶前会先过内容审核，审核不通过整个请求失败，需换图重试；视频和音频不做审核，直接入库
- 原文件名不会出现在 URL 里，中文名、空格、特殊字符都能直接上传，不需要提前改名
- 上传不消耗算力，但服务端不做去重：同一个文件在一次任务里只上传一次，记下 `fullPath` 复用

成功响应取 `data.fullPath` 作为公网直链，永久有效、不带签名：

```json
{
  "code": 200,
  "msg": null,
  "data": {
    "relativePath": "cos_ai_agent/2026-08-11/3f2a9c1b7d84e6f5a012.mp4",
    "fullPath": "https://agent-1404002717.cos.ap-guangzhou.myqcloud.com/cos_ai_agent/2026-08-11/3f2a9c1b7d84e6f5a012.mp4",
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

上传成功的文件还要满足本技能自己的素材限制（参考图片单个不超过 10MB、参考视频单个不超过 50MB 且总时长不超过 15 秒等），详见上面的参数映射规则。

拿到 `code=9999`、`msg` 为 `服务繁忙，请稍后再试` 时，先自查三项：是否漏了 `secretKey` 请求头、表单字段名是否为 `file`、文件是否超出服务端体积上限（超限只会返回这条通用错误，此时应先压缩或裁剪再重试，不要原样重传）。密钥、格式、审核、体积类错误重试无效，只有网络超时、5xx 和存储类异常值得重试。

## 调用示例

> **跨平台调用说明**：
> - 请求头必须包含 `Content-Type: application/json; charset=utf-8` 和 `secretKey`
> - **Windows/PowerShell**：因 GBK 编码问题，必须先将 JSON 写入临时文件 `payload_temp.json`（UTF-8 无 BOM），再用 `curl.exe --% --data-binary @payload_temp.json` 发送请求。使用 Write 工具创建文件，或用 .NET API `[System.IO.File]::WriteAllText("payload_temp.json", $json, [System.Text.UTF8Encoding]::new($false))`。调用后用 `rm payload_temp.json` 清理。
> - **macOS/Linux**：bash/zsh 默认 UTF-8，可直接内联 JSON：`curl -X POST URL -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --data-binary 'JSON单行内容'`

### 示例 1：提交视频生成任务（基础）

**Windows/PowerShell**：

创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "query": "为这款智能手表制作一个展示视频，突出运动监测功能",
  "platformType": "Amazon",
  "languageType": "英语",
  "videoModelType": "pro",
  "aspectRatio": "16:9",
  "needVoice": true,
  "duration": 10,
  "resolution": "720p",
  "videoTag": "主图视频"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"query":"为这款智能手表制作一个展示视频，突出运动监测功能","platformType":"Amazon","languageType":"英语","videoModelType":"pro","aspectRatio":"16:9","needVoice":true,"duration":10,"resolution":"720p","videoTag":"主图视频"}', [System.Text.UTF8Encoding]::new($false))
```

执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"query":"为这款智能手表制作一个展示视频，突出运动监测功能","platformType":"Amazon","languageType":"英语","videoModelType":"pro","aspectRatio":"16:9","needVoice":true,"duration":10,"resolution":"720p","videoTag":"主图视频"}'
```

### 示例 2：查询任务结果

**Windows/PowerShell**：

创建 `payload_temp.json`（两种方式任选其一）：

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

执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 30 --data-binary @payload_temp.json
```

清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 30 --data-binary '{"agentGenerateTaskId":"2072923591164715009"}'
```

### 示例 3：带参考图片生成视频

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "query": "根据提供的产品图片生成展示视频",
  "platformType": "淘宝",
  "languageType": "中文简体",
  "videoModelType": "pro",
  "aspectRatio": "1:1",
  "needVoice": true,
  "duration": 8,
  "resolution": "1080p",
  "videoTag": "种草视频",
  "referenceImageStr": "https://example.com/product1.png,https://example.com/product2.png"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"query":"根据提供的产品图片生成展示视频","platformType":"淘宝","languageType":"中文简体","videoModelType":"pro","aspectRatio":"1:1","needVoice":true,"duration":8,"resolution":"1080p","videoTag":"种草视频","referenceImageStr":"https://example.com/product1.png,https://example.com/product2.png"}', [System.Text.UTF8Encoding]::new($false))
```

执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"query":"根据提供的产品图片生成展示视频","platformType":"淘宝","languageType":"中文简体","videoModelType":"pro","aspectRatio":"1:1","needVoice":true,"duration":8,"resolution":"1080p","videoTag":"种草视频","referenceImageStr":"https://example.com/product1.png,https://example.com/product2.png"}'
```

### 示例 4：快速模式生成视频（fast模型）

**Windows/PowerShell**：

创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "query": "制作一个简单的产品展示视频",
  "platformType": "Amazon",
  "languageType": "英语",
  "videoModelType": "fast",
  "aspectRatio": "9:16",
  "needVoice": false,
  "duration": 6,
  "resolution": "480p",
  "videoTag": "主图视频"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"query":"制作一个简单的产品展示视频","platformType":"Amazon","languageType":"英语","videoModelType":"fast","aspectRatio":"9:16","needVoice":false,"duration":6,"resolution":"480p","videoTag":"主图视频"}', [System.Text.UTF8Encoding]::new($false))
```

执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"query":"制作一个简单的产品展示视频","platformType":"Amazon","languageType":"英语","videoModelType":"fast","aspectRatio":"9:16","needVoice":false,"duration":6,"resolution":"480p","videoTag":"主图视频"}'
```

### 示例 5：使用首帧和尾帧图片

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "query": "制作一个产品宣传视频",
  "platformType": "京东",
  "languageType": "中文简体",
  "videoModelType": "pro",
  "aspectRatio": "16:9",
  "needVoice": true,
  "duration": 12,
  "resolution": "4K",
  "videoTag": "品牌宣传",
  "firstFrame": "https://example.com/first_frame.png",
  "lastFrame": "https://example.com/last_frame.png"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"query":"制作一个产品宣传视频","platformType":"京东","languageType":"中文简体","videoModelType":"pro","aspectRatio":"16:9","needVoice":true,"duration":12,"resolution":"4K","videoTag":"品牌宣传","firstFrame":"https://example.com/first_frame.png","lastFrame":"https://example.com/last_frame.png"}', [System.Text.UTF8Encoding]::new($false))
```

执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"query":"制作一个产品宣传视频","platformType":"京东","languageType":"中文简体","videoModelType":"pro","aspectRatio":"16:9","needVoice":true,"duration":12,"resolution":"4K","videoTag":"品牌宣传","firstFrame":"https://example.com/first_frame.png","lastFrame":"https://example.com/last_frame.png"}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| query 超过1000字符 | 缩短需求描述内容 |
| duration 超出范围 | 视频时长需在 4-60 秒之间 |
| `videoModelType 仅支持 pro / fast / ultra` | 模型档位写错，改用 `pro`、`fast` 或 `ultra` |
| referenceImageStr 图片数量超限 | 最多6张图片，且图片+视频+音频总数不超过6个 |
| referenceVideoStr 视频数量/大小超限 | 最多3条视频，单个不超过50MB，总时长不超过15秒 |
| referenceVideoStr 包含人像 | 禁止人像视频，请更换参考视频 |
| referenceAudioStr 音频数量/大小超限 | 最多3条音频，单个不超过50MB，总时长不超过15秒 |
| firstFrame/lastFrame 与参考素材同时使用 | 首帧/尾帧不能与图片、视频、音频一起使用 |
| 服务繁忙（9999错误码） | 稍后重试 |
| taskStatus=3 生成失败 | 检查提示词质量和素材，尝试简化描述或更换素材 |
| 视频生成超时 | 视频生成耗时较长，增大超时时间并继续轮询 |

## 素材使用规则

### 参考素材（referenceImageStr / referenceVideoStr / referenceAudioStr）
- 三种素材总数不能超过6个
- 参考图片：最多6张，单个不超过10MB
- 参考视频：最多3条，单个不超过50MB，总时长不超过15秒，禁止人像
- 参考音频：最多3条，单个不超过50MB，总时长不超过15秒

### 首帧/尾帧图片（firstFrame / lastFrame）
- firstFrame：视频首帧图片，只能上传1张
- lastFrame：视频尾帧图片，只能上传1张
- **重要**：首帧/尾帧图片不能与参考素材（图片、视频、音频）同时使用

### 素材选择建议
- 需要产品参考时，使用 referenceImageStr 提供产品图片
- 需要风格参考时，使用 referenceVideoStr 提供参考视频（禁止人像）
- 需要背景音乐时，使用 referenceAudioStr 提供音频素材
- 需要指定视频开头/结尾画面时，使用 firstFrame 和 lastFrame

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集用户的视频生成需求并写入 `query`
3. 确定目标平台 `platformType` 和语言 `languageType`
4. 选择视频模型 `videoModelType`：pro（高质量，默认）、fast（快速生成）或 ultra（最高画质）
5. 设置视频参数：分辨率、比例、时长、配音、业务标签等
6. 根据需求添加参考素材或首帧/尾帧图片（本地文件先按「本地文件上传」章节换取公网直链）
7. 在请求头中传入 `secretKey`
8. 调用创建任务接口提交任务，从响应中读取 `data.agentGenerateTaskId`
9. 轮询调用查询结果接口，当 `taskStatus=2` 时获取视频 URL
10. 将结果视频展示给用户

**提示词处理：**
生成视频时，query 应指导AI：
- 明确描述视频的主题和内容
- 指定产品的关键特性和卖点
- 说明视频的风格和氛围
- 提及需要的视觉元素和效果

**示例query：**
- "为这款智能手表制作一个展示视频，突出运动监测功能"
- "制作一个产品宣传片，展示咖啡机的使用方法和特点"
- "生成一个创意视频，展示智能音箱的语音交互功能"
- "创建一个品牌宣传视频，强调产品的科技感和时尚感"
