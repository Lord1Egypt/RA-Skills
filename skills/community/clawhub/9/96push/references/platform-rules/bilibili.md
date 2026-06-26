# bilibili 哔哩哔哩

## 支持类型

- 支持 `article`、`video`。
- 平台列表当前未启用 `graph_text`，不要主动发布图文到 B 站。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。

## 封面

- 视频封面通常是平台必填项，建议 `autoThumb=false` + `thumb` 提供 1 张。
- 文章可通过 `thumb` 设置专栏封面，也可用 settings 的 `headerImg` 设置头图。
- `thumb/files/headerImg` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 视频可用字段：`reprint`、`partition`、`labels`、`creation`、`public`、`source`、`dynamic`、`timerPublish`。
- 视频 `partition` 很重要，尽量填写平台可选分区。
- 文章可用字段：`classify`、`origin`、`headerImg`、`labels`、`collection`、`public`、`timerPublish`。
- 文章 `labels` 最多 10 个。

## 限制

- 平台 toast 提示缺少标签、标题、分区或封面时应按平台失败处理，不要重试发布。
- 不要把视频 settings 用到文章，尤其是 `partition` 和 `reprint`。
