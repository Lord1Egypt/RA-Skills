# wechat 微信公众号

## 支持类型

- 支持 `article`、`graph_text`。
- 当前平台列表不启用公众号 `video`，视频内容应优先发到 `wechat-video`。

## 创建数据

- 文章必须有 `title` 和 `markdown` 或 `content`；不要传 `files`。
- 图文使用 `files` 图片 URL；不要传正文 `markdown/content`。
- 封面只放 `thumb`，正文图片放正文或图文 `files`。

## 封面

- 公众号文章封面是硬要求。`autoThumb=true` 时正文必须有可选图片；否则用 `autoThumb=false` + `thumb` 传 1 张封面。
- `thumb` 必须是 HTTP(S) 图片 URL。
- 文章正文内嵌本地图片先用 `upload` 或 96Push 上传入口转 pix URL；不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`author`、`link`、`leave`、`origin`、`reprint`、`publishType`、`collection`、`source`、`timerPublish`。
- 推荐设置：`publishType` 明确传 `"publish"` 或 `"mass"`；未确认群发能力时用 `"publish"`。
- `leave` 默认 true，`origin` 默认 false；不要为非原创内容传 `origin=true`。
- `source`：0 不声明，1 AI生成，2 官方媒体/网络新闻，3 剧情演绎，4 个人观点。

## 限制

- 定时发布：当前时间 +5 分钟到 7 天。
- 平台 settings 不要混入抖音/头条等字段，例如 `lookScope`、`hotspot`、`starter`。
