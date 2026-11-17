# 550W Open API 接口契约

仅在校验输入、解释计费或处理服务响应时读取。国内 API Key 管理页面为 <https://qzm.550wai.cn/api-keys>。所有请求使用同一账号的 `userNo` 和 `apiKey` 鉴权。

## 能力与接口

| 操作 | 接口 | 输入与用途 |
|---|---|---|
| `uploadVideo` | `/open/uploadVideo` | 上传 MP4/MOV 视频 |
| `submitTask` | `/open/submitTask` | 使用视频直链、真实宽高和时长提交去字幕或画面水印擦除任务；默认整帧，可选用户指定的区域及 `subUserId` |
| `taskDetail` | `/open/taskDetail` | 查询去字幕任务；子用户任务需使用相同 `subUserId` |
| `taskList` | `/open/taskList` | 分页查询去字幕任务；可按 `subUserId` 过滤 |
| `deleteTask` | `/open/deleteTask` | 删除去字幕任务并安排媒体清理；已扣积分不退还。Skill 执行前须针对任务 ID 获得用户确认，并传 `confirmDeletion: true`；此标记不会转发给 Open API。 |
| `queryCredits` | `/open/queryCredits` | 查询账户积分 |
| `removeImageWatermark` | `/open/removeImageWatermark` | 处理单张图片；`sync` 默认 `true` |
| `imageWatermarkTaskDetail` | `/open/imageWatermarkTaskDetail` | 查询异步图片任务 |
| `removeVideoWatermark` | `/open/removeVideoWatermark` | 输入短视频分享链接或含单个链接的分享文本；可选 `operationId` |

短视频链接去水印可让用户从抖音、快手、哔哩哔哩、微博等 App 或平台网站通过“分享→复制链接”取得公开视频或内容的分享链接，再作为 `videoUrl` 提交。具体平台和链接格式以服务端实际支持情况为准；无需先下载视频。成功时从 `data.video` 读取去水印结果；若 Agent 后续下载失败或超时，把这个解析视频直链交给用户在浏览器自行下载，不以原分享链接替代，也不声称已经下载成功。

## 输入限制

- 视频：MP4/MOV，不超过 1 GB、时长 1–600 秒；最大边不超过 1920 像素，最小边不超过 1080 像素。
- 本地视频去字幕和画面水印共用视频擦除任务。默认整帧 `(0,0,0,0)`；用户明确给出区域坐标时，同时提供四个非负整数像素坐标 `x1,y1,x2,y2`，且区域须在画面内。不可猜测坐标。
- 图片：JPG、PNG、BMP、WebP、AVIF、TIFF 或 SVG，不超过 50 MB。
- 链接：仅 HTTP(S)，最长 2048 字符。分享文本只可包含一个待处理链接。
- `operationId`：8–64 位，仅允许字母、数字、点、下划线、冒号和连字符；同一 ID 只用于同一短视频链接。
- 去字幕的可选 `idempotencyKey`：8–128 位，字符集相同；相同键和相同参数返回原任务，不同参数复用会被拒绝。
- `removeAudio` 是去字幕的次要可选参数，默认 `false`，仅在用户明确要求移除音轨时启用。
- 图片 `sync=false` 时，保存任务 ID，稍后查询状态。

## 状态与计费

- 去字幕状态：`waiting`、`processing`、`success`、`failed`。
- 图片去水印状态：`processing`、`success`、`failed`、`expired`。
- 图片任务顶层 `code=200` 也可能仍在处理中或已失败；以 `task.status` 为准，只有成功且有结果链接时才提示完成。
- 去字幕：不高于 720P 按 `ceil(duration × 1.3)` 积分，高于 720P 按 `ceil(duration × 1.6)` 积分。
- 短视频分享链接去水印：成功一次 1 积分，失败不扣积分。
- 图片去水印：成功一张 10 积分。
- 各能力共用账号积分，实际扣费以服务端响应为准。

## 错误与重试

- `200`：成功。
- `-100`：鉴权或额度失败，以响应 `message` 为准。
- `-200`：参数或文件不合法。
- `-300`：业务拒绝、任务不存在、服务繁忙或平台链接暂不支持，以响应为准。
- `-100` 或 `-300` 明确提示积分不足时，Skill 返回 `purchaseUrl=https://qzm.550wai.cn/purchase?tab=speed`；普通鉴权失败不附购买链接。
- `-401` / `-402`：账号被临时或永久限制，停止提交。
- `-500`：服务异常；若不能确认任务是否提交成功，先查询任务，不直接重试。
- `-600`：视频格式不支持，提示导出兼容的 MP4/MOV。
- 对 `-200` / `-300` 的已知错误标识或幂等参数冲突给出具体下一步；计费提交遇到 `-500` 或网络超时，先核查原任务或操作结果，不直接重试。只读查询可稍后重试。

仅将用户指定的本地文件或公开链接发送到 550W Open API 处理；凭据保存在用户本地配置中。
