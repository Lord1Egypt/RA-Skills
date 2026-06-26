# wechat-video 微信视频号

## 支持类型

- 支持 `graph_text`、`video`。
- 不支持普通文章 `article`。

## 创建数据

- 图文：`title` + `files` 图片 URL 数组。
- 视频：`title` + `files` 单个视频 URL，`desc` 建议填写。
- 不要传 `markdown/content`。

## 封面

- 视频可自动取帧；需要指定封面时使用 `autoThumb=false` + `thumb`。
- 图文默认从图片内容生成封面。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`location`、`collection`、`linkType`、`linkAddr`、`music`、`activity`、`origin`、`timerPublish`。
- `linkType`：0 不设置，1 公众号文章，2 红包封面；设置非 0 时要配套 `linkAddr`。
- `origin` 只对视频原创声明生效，并受账号能力限制。

## 限制

- 不要传公众号文章字段如 `author`、`publishType`。
- 选择音乐、活动、合集时必须使用平台页面可搜索/可选的名称。
