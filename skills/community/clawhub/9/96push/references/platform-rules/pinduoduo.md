# pinduoduo 拼多多

## 支持类型

- 只支持 `video`。

## 创建数据

- 视频必须有 `title` + 单个视频 `files`。
- `desc` 建议填写。
- 不要传 `markdown/content`、图文图片数组或文章字段。

## 封面

- 默认可由平台或视频帧生成。
- 若需要指定封面，使用 `autoThumb=false` + `thumb`。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`goodsId`、`source`、`timerPublish`。
- `goodsId` 是商品 ID；只有需要挂商品时传。
- `source`：0 不声明，1 AI，2 取材网络，3 可能引人不适，4 虚构演绎，5 危险行为。

## 限制

- 定时发布：当前时间 +4 小时到 7 天。
- 当前平台没有草稿能力，不要伪装草稿成功。
