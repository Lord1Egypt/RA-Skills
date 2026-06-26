# weishi 微视

## 支持类型

- 只支持 `video`。

## 创建数据

- 视频必须有 `title` + 单个视频 `files`。
- `desc` 建议填写。
- 不要传 `markdown/content` 或图文图片数组。

## 封面

- 默认可自动取帧。
- 手动封面使用 `autoThumb=false` + `thumb`，只使用第一张。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`source`、`lookScope`、`timerPublish`。
- `source`：0 不声明，1 AI生成，2 剧情演绎，3 个人观点，4 取材网络。
- `lookScope`：0 公开，1 自己。

## 限制

- 当前平台没有草稿能力，不要把保存草稿当成成功发布前置。
- 不要传图文或文章字段。
