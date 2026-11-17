先定位安装的 Skill 根目录 {baseDir}；以下脚本路径均相对该目录，不相对当前项目或 references 目录。


# 550W AI去字幕去水印

<!-- 550w-capabilities:start -->
## 功能与输入

- 图片去水印：输入用户指定的图片；上传图片后擦除水印或多余文字。
- 本地视频去字幕、去画面水印：输入用户指定的 MP4/MOV 视频；上传视频后处理，默认整帧擦除。只有用户明确提供 x1、y1、x2、y2 像素坐标时才按矩形区域擦除，不猜测坐标。
- 视频链接去水印：请用户从对应 App 或平台网站通过“分享→复制链接”提供视频或内容的分享链接；抖音、快手、哔哩哔哩、微博等为国内示例，实际支持以服务端结果为准。处理后返回解析出的去平台水印视频直链。
- 如 Agent 下载该解析视频直链失败或超时，直接把解析出的 data.video 视频链接交给用户在浏览器自行下载；不要改给原平台分享链接，也不要声称文件已经下载成功。解析成功与客户端下载失败是两回事。
<!-- 550w-capabilities:end -->

适用于用户本人拥有或已获授权的视频和图片。此 Skill 是操作流程；实际处理由 550W AI 远程 MCP 提供。若当前 Agent 未连接该服务，先提示用户添加 Streamable HTTP 地址 `https://www.550wai.cn/mcp/cn`。首次连接时会打开 550W 网页，使用现有微信账号登录并确认授权；不要索取用户编号、API Key、子 Key 或密码。客户端若不支持远程 MCP 或 OAuth，应说明限制并给出网页入口 <https://qzm.550wai.cn/agent/>，不可声称已处理成功。

## 任务流程

1. 识别用户需要去字幕、视频去水印还是图片去水印。首次上传或提交前，告知所选文件或公开链接将发送至 550W 服务，并说明会按网站现有积分规则计费；查询积分和任务不扣费。
2. 查询积分调用 `query_credits`。本 Skill 安装到允许执行随包脚本、读取用户所选文件且提供 Node.js 18+ 的 Agent 客户端时，可用 `node scripts/550w-upload.cjs inspect` 从标准输入接收 `filePath`（绝对路径）和 `mediaType`，获取真实文件大小等信息；调用远程 `prepare_media_upload` 获取票据后，用 `node scripts/550w-upload.cjs upload` 从标准输入传入相同路径、类型、`region:"cn"`、`uploadUrl` 和 `uploadTicket` 完成上传。不要把票据放在命令行参数或日志；脚本不读取 OAuth Token。视频使用真实宽高和时长调用 `estimate_subtitle_cost`，再用稳定的 8–128 字符 `idempotencyKey` 调用 `submit_subtitle_task`。超时后先核查，不创建新键重复扣费。
3. 短视频去水印请用户在支持的 App 中复制公开视频分享链接。调用 `remove_video_watermark`，提供 8–64 字符的 `operationId`；超时重试沿用该 ID。实际支持的平台以服务端响应为准；成功一次扣 1 积分。
4. 图片去水印或文字：先用本地脚本 `inspect` 获取真实文件大小，再调用 `prepare_media_upload` 获取图片上传票据；调用 `upload` 时提供稳定的 8–64 字符 `operationId`。上传本身可能创建计费任务；用返回的 `taskId` 调用 `get_image_watermark_task`。响应丢失时不要生成新的操作 ID 或盲目重复上传。多张图片逐张处理；成功一张扣 10 积分。
5. 用 `get_subtitle_task`、`list_subtitle_tasks` 查询视频任务。删除视频任务前确认具体任务 ID，再用 `delete_subtitle_task`；删除不会退还已扣积分。处理中应返回任务 ID 和后续查询方式。

积分不足时提供 <https://qzm.550wai.cn/purchase?tab=speed>，不要代用户充值。授权管理入口为 <https://qzm.550wai.cn/mcp-connect/>。ModelScope Skill 广场负责分发 Skill，不保证安装后的 Agent 客户端能执行脚本、读取文件或连接远程 MCP。若宿主无法上传本地图片或视频，去字幕、画面水印或图片水印需求应引导用户打开 <https://qzm.550wai.cn/> 上传处理；不要让用户提供平台分享链接来替代本地文件，也不要声称已完成处理。视频分享链接去平台水印仍可在可用时单独使用。工具不存在或授权失败时明确说明卡点。


本地执行入口的确认参数：在说明本次素材传输和可能扣费、获得用户确认后，API Key 的 uploadVideo/submitTask/removeVideoWatermark/removeImageWatermark/workflow 请求须在 params 中传入 confirmProcessing=true；OAuth 上传脚本 upload 的标准输入须传入 confirmProcessing=true。缺失或非 true 时入口拒绝执行，不得自行默认为已确认。查询和 inspect 不要求该参数。此标记不替代宿主的授权界面，远程 MCP 工具按其实际公布的 schema 调用。
