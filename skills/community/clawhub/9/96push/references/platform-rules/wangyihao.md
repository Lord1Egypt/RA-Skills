# wangyihao 网易号

## 支持类型

- 对最终用户只开放 `article`。
- 仓库内有视频实验代码，但当前规则不要引导最终用户发布网易号视频。

## 创建数据

- 文章必须有 `title` + `markdown/content`。
- 不要传 `files`；正文图片应写入正文。

## 封面

- 未设置 `thumb`：选择平台“自动”封面。
- 设置 1 张 `thumb`：选择单图封面。
- 设置 3 张及以上 `thumb`：选择三图封面，只取前 3 张。
- 手动封面失败时实现会尝试回退自动封面。
- `thumb` 必须是 HTTP(S) 图片 URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`declaration`、`topic`、`autoCommentText`、`timerPublish`。
- `topic` 多个用 `/` 分隔，必须匹配页面可见话题。
- `autoCommentText` 必须匹配网易号预置作者跟贴文案。

## 限制

- 不要误点正文区域的 `上传图片` 作为正文图片入口；网易号文章页该入口当前用于封面。
- 不要传视频或图文字段。
