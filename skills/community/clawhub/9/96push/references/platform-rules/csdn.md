# csdn CSDN

## 支持类型

- 支持 `article`、`video`。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。

## 封面

- 文章封面可选，但建议使用真实封面尺寸图片，避免太小图标导致裁剪/上传链路不稳定。
- 视频可使用 `autoThumb=false` + `thumb` 指定封面。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 文章可用字段：`labels`、`collection`、`artType`、`originLink`、`backupGitCode`、`lookScope`、`activity`、`topic`、`timerPublish`。
- `labels` 用 `/` 分隔，最多 7 个。
- `collection` 用 `/` 分隔，最多 3 个。
- `artType`：0 原创，1 转载，2 翻译。
- `artType=1` 转载时 `originLink` 必填；翻译时建议填写。
- 视频字段：`labels` 最多 3 个，`recommend` 是否推荐。

## 限制

- 定时发布：当前时间 +4 小时到 7 天。
- 不要把图文平台字段如 `source`、`hotspot` 传给 CSDN。
