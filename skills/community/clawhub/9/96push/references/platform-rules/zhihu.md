# zhihu 知乎

## 支持类型

- 支持 `article`、`graph_text`、`video`。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 图文：`title` + 图片 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。

## 封面

- 文章封面可选；需要时传 `thumb`。
- 图文默认从图片内容生成。
- 视频可自动取封面，也可手动封面。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 文章/图文可用字段：`question`、`source`、`topic`、`collection`、`origin`。
- `topic` 最多 3 个，用 `/` 分隔。
- `source`：0 无声明，1 包含剧透，2 包含医疗建议，3 虚构创作，4 包含理财内容，5 包含 AI 辅助创作。
- `origin`：0 不设置，1 官方网站，2 新闻报道，3 电视媒体，4 纸质媒体。
- 视频额外字段：`classify`、`reprint`、`timerPublish`；视频 `classify` 推荐填写。

## 限制

- 视频定时发布：当前时间 +1 小时到 14 天。
- `question` 会搜索并选择第一个可选问题，别传含糊关键词。
