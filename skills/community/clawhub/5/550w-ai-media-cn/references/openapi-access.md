先定位安装的 Skill 根目录 {baseDir}；以下脚本路径均相对该目录，不相对当前项目或 references 目录。


# 550W AI去字幕去水印

<!-- 550w-capabilities:start -->
## 功能与输入

- 图片去水印：输入用户指定的图片；上传图片后擦除水印或多余文字。
- 本地视频去字幕、去画面水印：输入用户指定的 MP4/MOV 视频；上传视频后处理，默认整帧擦除。只有用户明确提供 x1、y1、x2、y2 像素坐标时才按矩形区域擦除，不猜测坐标。
- 视频链接去水印：请用户从对应 App 或平台网站通过“分享→复制链接”提供视频或内容的分享链接；抖音、快手、哔哩哔哩、微博等为国内示例，实际支持以服务端结果为准。处理后返回解析出的去平台水印视频直链。
- 如 Agent 下载该解析视频直链失败或超时，直接把解析出的 data.video 视频链接交给用户在浏览器自行下载；不要改给原平台分享链接，也不要声称文件已经下载成功。解析成功与客户端下载失败是两回事。
<!-- 550w-capabilities:end -->

选择最符合用户意图的高级工具。国内版固定使用国内服务，以中文交互，无需用户配置服务区域。

## 凭据与数据

- 未配置凭据时，引导用户前往 <https://qzm.550wai.cn/api-keys>，取得同一账号的用户 ID 和 API Key。
- 本 OpenAPI 版本使用 `SUBTITLE_REMOVER_USER_NO`、`SUBTITLE_REMOVER_API_KEY`；WorkBuddy 的独立连接器使用网页 OAuth 授权。使用 `configureCredentials` 前说明：凭据发送至 550W 验证后会写入本机用户配置目录；用户同意后才传入 `confirmCredentialStorage=true`。共享宿主优先使用环境凭据或 OAuth。不要展示完整 API Key。
- 首次处理媒体前，说明选中的文件或公开链接会发送到 550W Open API。只使用用户明确指定或选中的文件，不自行遍历文件系统寻找媒体。

## 能力

- 去除本地 MP4/MOV 视频或公网视频文件直链中的硬字幕、画面水印：`remove_video_subtitles`（命令行操作名 `workflow`）。本地视频的宽高和时长由工具读取。`removeAudio` 仅在用户明确要求时作为可选参数使用。
- 短视频去水印：让用户在对应 App 内复制视频分享链接，并提供该链接；含单个链接的分享文本也可使用。国内平台示例包括抖音、快手、Bilibili、微博、小红书等，实际以服务端支持的公开链接为准。调用 `remove_video_watermark`（命令行操作名 `removeVideoWatermark`）；不必先下载视频。可用时传入稳定的 `operationId`。
- 去除用户选中图片中的水印或多余文字：`remove_image_watermark`（命令行操作名 `removeImageWatermark`）。多张图片逐张处理。
- 查询去字幕或图片任务状态、去字幕任务历史和积分：`get_subtitle_task`、`get_image_task`、`list_subtitle_tasks`、`query_credits`。
- 删除本人一项去字幕任务：`delete_subtitle_task`。说明媒体将进入清理流程、已扣积分不退还；针对具体任务 ID 再次确认后才传 `confirmDeletion: true`。不可从原处理请求推定删除授权。
- 输入或计费操作不明确时，先问一个必要问题。

若客户端未注册工具，且允许执行 Node.js 18+ 并读取用户所选文件，可通过标准输入向 `node {baseDir}/dist/550w-skill.cjs` 发送单条 JSON 请求；本地文件使用绝对 `params.filePath`，解析单条 JSON 响应。安装此 Skill 不等于宿主已开放脚本执行和文件权限。若不能读取或上传本地图片、视频，引导用户到 <https://qzm.550wai.cn/> 上传处理；不要让用户提供平台分享链接来替代本地文件，也不要声称文件已处理。可用时仍可单独处理视频分享链接。

## 处理与计费

- 视频擦除默认整帧处理；只有用户明确给出四个坐标时才按区域处理。公网视频文件直链须用 `ffprobe` 获取真实宽高和时长；仅在调用方已提供全部三个真实值时可跳过。拒绝内网和带凭据的链接；探测链接时拒绝重定向，并请用户提供最终公网视频文件直链。若已提供全部元数据，Skill 仍检查链接的公网地址，但不探测跳转；服务端仍会校验提交的视频来源。不猜测元数据。
- 代子用户提交时，在提交、查询、列表过滤和删除时使用同一 `subUserId`。去字幕流程最多轮询 10 分钟；超时或重复查询失败时返回任务 ID，供稍后查询。
- 图片去除默认同步，但也可能返回处理中任务；保留任务 ID 并稍后查询。只有 `success` 且有结果链接才展示完成；说明 `failed`、`expired`，未知状态不可当作完成。
- 去字幕按时长和分辨率计费；分享链接去水印成功一次 1 积分；图片去除成功一张 10 积分。批量处理前说明计费单位，只处理用户指定的项目。
- 超时或服务异常不能证明计费提交失败。先查现有任务或原操作结果，不盲目重复付费提交；只读查询可稍后重试。去字幕的 `idempotencyKey` 仅能对完全相同的输入复用。失败时以服务端 `refundStatus` 报告退款状态。
- 服务端明确提示积分不足时，把响应中的 `purchaseUrl` 提供给用户；国内购买页为 <https://qzm.550wai.cn/purchase?tab=speed>。普通凭据错误不可误判为积分不足，也不要替用户自动购买。
- 每次向用户返回处理结果或可操作的错误信息。

输入限制、状态、计费公式和错误码见 [接口契约](api-contract.md)；其他客户端的安装说明见 [Agent 兼容性](agent-compatibility.md)。


本地执行入口的确认参数：在说明本次素材传输和可能扣费、获得用户确认后，API Key 的 uploadVideo/submitTask/removeVideoWatermark/removeImageWatermark/workflow 请求须在 params 中传入 confirmProcessing=true；OAuth 上传脚本 upload 的标准输入须传入 confirmProcessing=true。缺失或非 true 时入口拒绝执行，不得自行默认为已确认。查询和 inspect 不要求该参数。此标记不替代宿主的授权界面，远程 MCP 工具按其实际公布的 schema 调用。
