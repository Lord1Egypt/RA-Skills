# omtencent 腾讯内容开放平台

## 支持类型

- 支持 `article`、`video`。
- 不支持 `graph_text`。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。

## 封面

- 文章可手动上传封面；传 3 张及以上会按三图处理，否则按单图处理。
- 视频默认可自动取封面；需要指定时用 `autoThumb=false` + `thumb`。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`classify`、`labels`、`activity`、`source`、`timerPublish`。
- 推荐文章 `classify` 使用平台可选分类，例如稳定测试常用 `科技`。
- `labels` 使用 `/` 分隔，最多 9 个，每个最多 8 个中文字符。
- `source`：1 AI生成，2 剧情演绎，3 取材网络，4 个人观点，5 旧闻；为空或 0 时当前实现默认 4。

## 限制

- 定时发布：当前时间 +5 分钟到 7 天。
- 平台可能出现 AIGC 声明弹窗，自动化会先提交弹窗后重新发布。
