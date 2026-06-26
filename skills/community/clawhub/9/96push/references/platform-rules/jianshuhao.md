# jianshuhao 简书

## 支持类型

- 只支持 `article`。

## 创建数据

- 文章必须有 `title` + `markdown/content`。
- 不要传 `files`；正文图片放正文。

## 封面

- 可选 `thumb` 作为文章封面，只使用第一张。
- 无封面也可继续文章发布流程。
- `thumb` 必须是 HTTP(S) 图片 URL；本地图片先用 `upload` 或 96Push 上传入口转 pix URL，不要传本地路径或 base64/data URL。

## Settings

- 可用字段：`collection`、`vetoReprint`。
- `collection` 是文集名称，应使用账号已有或页面可选文集。
- `vetoReprint=true` 表示禁止转载。

## 限制

- 不支持图文/视频。
- 不要传定时发布、声明、可见范围等其他平台字段。
