# 550W Open API contract / 接口契约

Read this reference only when validating inputs, explaining billing, or handling provider responses. The domestic credential-management page is `https://qzm.550wai.cn/api-keys`. The global documentation and credential page is `https://eraser.550wai.com/api/`; supported locale routes use `https://eraser.550wai.com/{locale}/api/`. These regional surfaces configure the same shared Skill capabilities.

仅在校验输入、解释计费或处理服务响应时读取。国内凭据管理页是 `https://qzm.550wai.cn/api-keys`；全球文档与凭据页是 `https://eraser.550wai.com/api/`，支持的语言使用 `https://eraser.550wai.com/{locale}/api/`。这些地区入口配置的是同一个全球共享 Skill 能力。

## Actions / 能力

| Action | Endpoint | Scope and input / 范围与输入 |
|---|---|---|
| `uploadVideo` | `/open/uploadVideo` | MP4/MOV file / MP4、MOV 文件 |
| `submitTask` | `/open/submitTask` | Direct video URL plus actual width, height, and duration; optional `subUserId`; the skill submits full-frame coordinates / 视频直链及真实宽高、时长；可选 `subUserId`；Skill 固定提交全屏坐标 |
| `taskDetail` | `/open/taskDetail` | Subtitle-removal `taskId`; optional matching `subUserId` / 去字幕任务编号；可选且需匹配的 `subUserId` |
| `taskList` | `/open/taskList` | `page`, `size`; optional `subUserId` scope / 分页参数；可选 `subUserId` 范围 |
| `deleteTask` | `/open/deleteTask` | Subtitle task `taskId`; optional `subUserId`. Destructive and does not refund credits / 去字幕任务编号；可选 `subUserId`。删除不可撤销且不退积分 |
| `queryCredits` | `/open/queryCredits` | No business parameters / 无业务参数 |
| `removeImageWatermark` | `/open/removeImageWatermark` | One image file; `sync` defaults to `true` / 单张图片；`sync` 默认 `true` |
| `imageWatermarkTaskDetail` | `/open/imageWatermarkTaskDetail` | Image task `taskId` / 图片任务编号 |
| `removeVideoWatermark` | `/open/removeVideoWatermark` | TikTok or another supported short-video share URL copied in the platform app, or copied share text; optional `operationId` / 在平台 App 内复制的 TikTok 等短视频分享链接或分享文本；可选 `operationId` |

All remote calls authenticate with `userNo` and `apiKey`. Capabilities are shared globally; region and locale affect the credential/documentation URL and user-facing language, not tool availability.

所有远程请求使用 `userNo` 与 `apiKey` 鉴权。能力全球共享；地区和语言只影响凭据/文档入口及用户文案，不限制工具可用性。

## Input limits / 输入限制

- Video / 视频：MP4 or MOV, at most 1 GB, 1–600 seconds; maximum side at most 1920 and minimum side at most 1080 / MP4 或 MOV，最大 1GB，时长 1–600 秒；最大边不超过 1920，最小边不超过 1080。
- Image / 图片：JPG, PNG, BMP, WebP, AVIF, TIFF, or SVG; at most 50 MB / 最大 50MB。
- URL：HTTP or HTTPS only, at most 2048 characters / 仅 HTTP 或 HTTPS，最长 2048 字符。
- Video-link watermark removal accepts TikTok and other provider-supported public share links copied inside the platform app. Supply that link as `videoUrl`; no prior download is needed. Copied share text may be supplied when it contains one HTTP(S) URL. Actual platform support depends on the service response. `operationId` is 8–64 characters using letters, numbers, `.`, `_`, `:`, or `-`; reuse it only for the same URL / 在平台 App 内复制 TikTok 等短视频的公开视频分享链接，并将链接作为 `videoUrl` 输入，无需先下载。分享文本中包含一个 HTTP(S) URL 时也可使用；实际支持的平台以服务端响应为准。`operationId` 为 8–64 位，字符集同上且仅用于同一链接。
- Subtitle submission accepts an optional `idempotencyKey` of 8–128 characters using the same character set. Reusing the key with identical inputs returns the original task; different inputs are rejected / 去字幕提交支持可选的 `idempotencyKey`，长度 8–128 位且字符集同上。同一键与相同参数会返回原任务，与不同参数复用会被拒绝。
- `removeAudio` is an optional subtitle-removal parameter, defaults to `false`, and must be enabled only when the user explicitly requests removal of the audio track. It does not re-encode the video stream / `removeAudio` 是去字幕的次要可选参数，默认 `false`；仅在用户明确要求移除音轨时启用，且不重新编码视频流。
- When image `sync=false`, query the returned task ID later / 图片 `sync=false` 时按返回的任务编号查询。

## Status / 状态

- Subtitle removal / 去字幕：`waiting`, `processing`, `success`, `failed`.
- Image watermark removal / 图片去水印：`processing`, `success`, `failed`, `expired`.

## Billing / 计费

- Subtitle removal / 去字幕：up to 720p, `ceil(duration × 1.3)`; above 720p, `ceil(duration × 1.6)` / 不高于 720P 按 `ceil(duration × 1.3)`，高于 720P 按 `ceil(duration × 1.6)`。
- Video-link watermark removal / 短视频链接去水印：1 credit per successful result; failures are not charged / 成功一次 1 积分，失败不扣积分。
- Image watermark removal / 图片去水印：10 credits per successful image / 成功一张 10 积分。
- Capabilities share the account credit balance; the API response is authoritative / 各能力共用账户积分余额，以接口响应为准。

## Errors and retry safety / 错误与重试安全

- `200`: success / 成功。
- `-100`: authentication or insufficient credits; follow `message` / 鉴权或额度不足，以 `message` 为准。
- `-200`: invalid parameter or file / 参数或文件不合法。
- `-300`: business rejection, missing task, or service busy / 业务拒绝、任务不存在或服务繁忙。
- `-401` / `-402`: temporarily or permanently restricted account; stop submitting / 账号被临时或永久限制，停止提交。
- `-500`: service error. If submission may have succeeded, query task state before retrying / 服务异常；无法确认是否已提交时先查询任务，不能直接重试。
- `-600`: unsupported video format; ask the user to export a compatible MP4 or MOV / 视频格式不支持，提示用户重新导出兼容格式。

## Data handling / 数据处理

Selected local files and public media URLs are sent to the 550W Open API for processing. Credentials remain in local configuration. For global users, surface the localized privacy and terms pages when relevant: `https://eraser.550wai.com/{locale}/privacy/` and `https://eraser.550wai.com/{locale}/terms/`, with the locale segment omitted for English.

选中的本地文件和公开媒体 URL 会发送到 550W Open API 处理，凭据保存在本地配置中。面向全球用户时，按需提供对应语言的隐私政策和服务条款；英语页面省略语言路径段。
