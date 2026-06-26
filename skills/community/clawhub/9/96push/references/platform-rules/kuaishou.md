# kuaishou 快手

## 支持类型

- 支持 `graph_text`、`video`。
- 不支持文章 `article`。

## 创建数据

- 图文：`title` + 图片 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。
- 不要传 `markdown/content`。

## 封面

- 默认可自动使用内容图或视频帧。
- 手动封面使用 `autoThumb=false` + `thumb`。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`music`、`linkApplet`、`source`、`collection`、`location`、`sameFrame`、`download`、`sameCity`、`lookScope`、`timerPublish`。
- `source`：0 不声明，1 AI生成，2 演绎情节，3 个人观点，4 素材来源网络。
- `lookScope`：0 公开，1 好友，2 自己。
- `sameFrame`、`download`、`sameCity` 默认 true；需要关闭时显式传 false。

## 限制

- `music` 仅图文使用。
- 小程序、合集、位置都依赖平台搜索结果。
