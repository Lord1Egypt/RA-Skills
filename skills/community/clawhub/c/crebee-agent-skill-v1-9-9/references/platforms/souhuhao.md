# 搜狐号发布参数

`platform` 为 `souhuhao`。以下 JSON 是批量发布任务的 `params`；可选字段无值时省略，所有字段均不接受 `null`。

### 图文 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | 否 | 动态标题可为空。 |
| `desc` | string | **是** | 动态正文，至少 1 个字符。 |
| `images` | string[] | **是** | 本地图片路径列表，至少 1 张。 |
| `taskId` | string | 否（建议传） | 用于发布状态回调。 |
| `infoResource` | `0` \| `1` \| `2` \| `3` | 否 | 信息来源：0 无特别声明，1 引用声明，2 AI 创作内容，3 虚构创作。 |
| `sourceUrl` | string | 否 | `infoResource` 为 `1` 时运行时必填。 |
| `visibleToLoginedUsers` | boolean | 否 | 是否必须登录才能查看全文；为 `true` 时正文需超过 100 字。 |

**最小参数校验示例：**

```json
{
  "desc": "搜狐号动态正文",
  "images": ["/tmp/image.jpg"],
  "taskId": "souhuhao-image-1"
}
```

### 文章 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是** | 标题长度为 5-72 字。 |
| `content` | string | **是** | 文章正文，至少 1 个字符。 |
| `covers` | string[] | 否 | 封面图路径列表。 |
| `taskId` | string | 否（建议传） | 用于发布状态回调。 |
| `brief` | string | 否 | 文章摘要，最多 120 字。 |
| `timing` | number | 否 | 秒级定时发布时间戳；`0` 或省略表示立即发布，定时需在 30 分钟后至 3 天 30 分钟内。 |
| `infoResource` | `0` \| `1` \| `2` \| `3` | 否 | 信息来源：0 无特别声明，1 引用声明，2 AI 创作内容，3 虚构创作。 |
| `sourceUrl` | string | 否 | `infoResource` 为 `1` 时运行时必填。 |
| `visibleToLoginedUsers` | boolean | 否 | 是否必须登录才能查看全文；为 `true` 时正文需超过 100 字。 |
| `columnNewsIds` | string[] | 否 | 关联栏目 `newsId` 列表；当前 HTTP Skill 未暴露栏目查询接口。 |
| `userLabels` | object[] | 否 | 话题列表；每项含必填 `id`、`name`、`type`，以及可选 `uid`；当前 HTTP Skill 未暴露话题查询接口。 |
| `attrIds` | number[] | 否 | 文章属性 ID 列表；当前 HTTP Skill 未暴露属性查询接口。 |

**最小参数校验示例：**

```json
{
  "title": "搜狐号文章标题",
  "content": "<p>文章正文</p>",
  "taskId": "souhuhao-article-1"
}
```
