# CSDN 发布参数

`platform` 为 `csdn`，仅支持 `article`。以下 JSON 是批量发布任务的 `params`；可选字段无值时省略，所有字段均不接受 `null`。

### 文章 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是（运行时）** | 标题长度为 5-100 字。 |
| `content` | string | **是（运行时）** | HTML 正文，去除标签后的文本不能为空。 |
| `covers` | string[] | 否 | 封面图路径列表。 |
| `taskId` | string | 否（建议传） | 用于发布状态回调。 |
| `tags` | string | **是** | 文章标签，多个标签以逗号分隔；运行时最多 7 个；当前 HTTP Skill 未暴露推荐标签查询接口。 |
| `description` | string | 否 | 文章摘要。 |
| `categories` | string | 否 | 分类专栏，多个专栏以逗号分隔；当前 HTTP Skill 未暴露专栏查询接口。 |
| `articleType` | `"original"` \| `"repost"` \| `"translated"` | 否 | 文章类型；为 `"repost"` 时运行时必须提供完整 URL 的 `originalLink`。 |
| `readType` | `"public"` \| `"private"` \| `"fans"` \| `"vip"` | 否 | 可见范围；`"private"` 不支持定时发布。 |
| `creationStatement` | `0` \| `1` \| `2` \| `3` | 否 | 创作声明。 |
| `originalLink` | string | 否 | 转载原文链接。 |
| `creatorActivityId` | string | 否 | 创作活动 ID；当前 HTTP Skill 未暴露活动查询接口。 |
| `timing` | number | 否 | 定时发布时间戳；`0` 表示立即发布。定时需在 4 小时后至 7 天内，且分钟为 15 分钟间隔。 |
| `syncGitCode` | boolean | 否 | 是否备份到 GitCode。 |

**最小参数校验示例：**

```json
{
  "title": "CSDN文章标题",
  "content": "<p>文章正文</p>",
  "tags": "技术",
  "taskId": "csdn-article-1"
}
```
