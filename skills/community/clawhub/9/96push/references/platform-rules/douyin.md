# douyin 抖音

## 支持类型

- 支持 `graph_text`、`video`。
- 不支持文章 `article`。

## 创建数据

- 图文：`title` + 图片 `files`，图片就是内容。
- 视频：`title` + 单个视频 `files`，`desc` 建议作为视频描述。
- 不要传 `markdown/content`。

## 封面

- 默认可自动生成封面。
- 手动封面使用 `autoThumb=false` + `thumb`，只传图片 URL。
- 图文/视频的内容媒体放 `files`，不要把封面混进 `files`。

## Settings

- 可用字段：`activity`、`music`、`label`、`location`、`hotspot`、`collection`、`allowSave`、`lookScope`、`timerPublish`。
- `lookScope`：0 公开，1 好友，2 自己。
- `allowSave` 默认 true；要禁止保存时显式传 false。

## 限制

- 位置、音乐、热点、合集都依赖平台搜索结果，不要凭空传不存在的名称。
- 不要传文章字段如 `collection` 以外的专栏/分类字段。

