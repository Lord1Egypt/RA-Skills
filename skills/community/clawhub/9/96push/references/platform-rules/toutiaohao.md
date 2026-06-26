# toutiaohao 今日头条

## 支持类型

- 支持 `article`、`graph_text`、`video`。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 图文：`title` + 图片 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。

## 封面

- 文章封面建议显式提供 1 或 3 张，使用 `autoThumb=false` + `thumb`。
- 文章封面必须是 JPEG/PNG，不能是 webp；尺寸至少 `450x300`。
- 未提供手动封面时会尝试页面自动封面或无封面，但这不如手动封面稳定。
- 视频可自动取帧，也可 `autoThumb=false` + `thumb`。

## Settings

- 文章/图文可用字段：`location`、`placeAD`、`starter`、`collection`、`syncPublish`、`source`、`timerPublish`。
- 图文额外字段：`openBgm`。
- 视频可用字段：`gtEnable`、`gtSyncPub`、`collection`、`stickers`、`source`、`link`、`lookScope`、`timerPublish`。
- `source` 常用值：0 不声明，1 取材网络，3 个人观点，4 引用AI，5 虚构演绎，6 投资观点，7 健康分享。

## 限制

- 定时发布：当前时间 +2 小时到 7 天。
- 文章设置 `collection` 后不要同时定时发布。
- 不要传小红书/抖音字段如 `origin`、`hotspot`。

