# juejin 掘金

## 支持类型

- 支持 `article`、`graph_text`。
- 不支持 `video`。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 图文/沸点：`title` + 图片 `files`，文案放 `desc`。

## 封面

- 文章封面不是主要必填项。
- 图文默认使用图片内容。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`classify`、`tag`、`collection`、`topic`、`group`、`link`。
- `tag` 必填，至少 1 个标签。
- `classify` 推荐填写平台可选分类。
- `group`、`link` 主要用于沸点/图文场景。

## 限制

- 缺少标签、分类、标题或正文时平台会失败，应在发布前补齐。
- 不要传 `timerPublish`、`source`、`lookScope` 等未支持字段。
