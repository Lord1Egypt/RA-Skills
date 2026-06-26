# 通用发布规则

这份规则适用于所有平台，平台专属限制以同目录下对应平台文件为准。

## 创建数据

- `thumb` 和 `files` 只能传 `http://`/`https://` URL；本地图片先通过 `upload --file ... --confirm` 或 96Push 上传入口转成 pix URL；不要传本地路径、base64、data URL。
- `upload` 返回的是 96Push 本地 pix URL，本身已经落在桌面端；发布时才会按平台需要把 `thumb/files` 下载成任务本地文件，正文 pix 图片转临时公网 URL 时会按图片 hash 缓存约 47 小时。
- 文章 `article`：只传 `title`、`markdown` 或 `content`，可选 `desc`、`autoThumb`、`thumb`；不要传 `files`。
- 图文 `graph_text`：只传 `title`、`files` 图片 URL 数组，可选 `desc`、`autoThumb`、`thumb`；不要传 `markdown` 或 `content`。
- 视频 `video`：只传 `title`、`files` 单个视频 URL，可选 `desc`、`autoThumb`、`thumb`；不要传 `markdown` 或 `content`。
- `desc` 对视频和 X/TikTok/YouTube 等平台更重要；文章摘要可选，按平台需要补。

## 封面

- 默认优先使用 `autoThumb=true`，但正文或视频无法稳定提取封面时，要显式提供 `thumb`。
- 手动封面使用 `autoThumb=false` 并传 `thumb`；多数平台只使用第一张，头条/百家号/网易号文章可使用 1 或 3 张。
- 封面图片尽量使用 JPEG/PNG，尺寸不要太小；今日头条文章封面至少 `450x300`，且不支持 webp。
- 图文内容图片放在 `files`；文章正文图片放在 `markdown/content`；封面图片只放 `thumb`。

## Settings

- `postAccounts[].settings` 只放目标平台支持的字段，不要把别的平台字段混进去。
- 没有明确要求时，不要臆造 `classify`、`labels`、`topic`、`source` 等字段；先查询平台规则或平台配置模板。
- 定时发布统一使用 `timerPublish: {"enable": true, "timer": "YYYY-MM-DD HH:MM:SS"}`，但每个平台的最早/最晚时间不同。
- 真实发布前必须确认账号和平台；发布命令每批内容只调用一次。
