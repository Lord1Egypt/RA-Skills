# baijiahao 百家号

## 支持类型

- 支持 `article`、`graph_text`、`video`。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 图文：`title` + 图片 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。

## 封面

- 文章封面容易成为硬失败。建议提供 1 或 3 张 `thumb`，或确保正文有可自动提取图片。
- 视频通常要求封面，建议提供 `autoThumb=false` + `thumb`。
- 平台提示“封面”或“请添加”时应直接视为发布失败。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`watermark`、`location`、`classify`、`activity`、`byAI`、`timerPublish`。
- `classify` 格式：`"一级/二级"` 或 `"一级/二级/三级"`。
- `watermark` 仅视频：0 不加，1 水印，2 贴片。
- AI 内容应设置 `byAI=true`。

## 限制

- 定时发布：当前时间 +1 小时到 7 天。
- 不要把 `origin`、`source` 等其他平台声明字段混进来。
