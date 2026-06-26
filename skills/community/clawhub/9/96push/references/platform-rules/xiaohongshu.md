# xiaohongshu 小红书

## 支持类型

- 支持 `graph_text`、`video`。
- 不支持文章 `article`。

## 创建数据

- 图文：`title` + 图片 `files`；正文描述放 `desc`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。
- 不要传 `markdown/content`。

## 封面

- 图文默认使用图片内容生成封面。
- 视频可自动取封面；需要指定时用 `autoThumb=false` + `thumb`。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`location`、`collection`、`group`、`mark`、`origin`、`source`、`reprint`、`lookScope`、`timerPublish`。
- `mark` 格式：`{"user": true, "search": "关键词"}`，`user=false` 表示标记地点。
- `source`：0 不声明，1 虚构演绎，2 AI合成，3 已在正文自主标注，4 自主拍摄，5 来源转载。
- `lookScope`：0 公开，1 好友，2 自己。

## 限制

- `origin=true` 不能同时使用 `source=5` 来源转载。
- `source=5` 时应填写 `reprint` 来源媒体。
- 定时发布：当前时间 +1 小时到 14 天。
