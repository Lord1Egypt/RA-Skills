# sohuhao 搜狐号

## 支持类型

- 支持 `article`、`graph_text`、`video`。

## 创建数据

- 文章：`title` + `markdown/content`；不要传 `files`。
- 图文：`title` + 图片 `files`。
- 视频：`title` + 单个视频 `files`，`desc` 建议填写。

## 封面

- 搜狐号允许无封面发布。
- 手动封面：`autoThumb=false` + `thumb`，会自动上传到搜狐号。
- 自动提取：`autoThumb=true` 且文章正文有图片时，平台可从正文提取。
- `thumb/files` 必须是 HTTP(S) URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`classify`、`declaration`、`topic`、`loginView`、`timerPublish`。
- `classify` 文章/视频属性常用值：观点评论、故事传记、消息资讯、八卦爆料、经验教程、知识科普、测评盘点、见闻记录、运势、搞笑段子、美图、美文。
- `declaration`：0 无特别声明，1 引用声明，2 包含AI创作内容，3 包含虚构创作。
- `loginView=true` 表示必须登录才能查看全文。

## 限制

- 定时发布：当前时间 +1 小时到 7 天。
- `topic` 是平台搜索型话题，留空表示不设置。
