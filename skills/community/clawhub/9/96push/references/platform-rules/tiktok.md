# tiktok TikTok

## 支持类型

- 只支持 `video`。

## 创建数据

- 视频必须有 `title` + 单个视频 `files`。
- `desc` 建议填写；不要传 `markdown/content`。

## 封面

- 默认可自动取封面。
- 手动封面使用 `autoThumb=false` + `thumb`。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`location`、`lookScope`、`comment`、`creation`、`reveal`、`yourBrand`、`brandContent`、`aigc`、`timerPublish`。
- `lookScope`：0 所有人，1 好友，2 自己。
- `comment` 控制是否允许评论。
- `aigc` 表示 AI 生成内容；涉及合成/品牌时按平台要求同时设置披露字段。

## 限制

- 品牌内容作品在部分组合下不能设为私密；当前实现会阻止 `lookScope=2` 且 `reveal=true` 且 `brandContent=true` 的组合。
- 定时发布：当前时间 +2 小时到 30 天。
