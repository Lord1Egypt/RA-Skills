# 简书发布参数

`platform` 为 `jianshu`，仅支持 `article`。以下 JSON 是批量发布任务的 `params`；可选字段无值时省略，所有字段均不接受 `null`。

### 文章 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是（运行时）** | 文章标题不能为空。 |
| `content` | string | **是（运行时）** | 正文可为 HTML 或 Markdown，去除标记后的文本不能为空。 |
| `covers` | string[] | 否 | 封面图路径列表。 |
| `taskId` | string | 否（建议传） | 用于发布状态回调。 |
| `notebookId` | string | 否 | 文集 ID；省略时使用账号的第一个文集；当前 HTTP Skill 未暴露文集查询接口。 |

**最小参数校验示例：**

```json
{
  "title": "简书文章标题",
  "content": "<p>文章正文</p>",
  "taskId": "jianshu-article-1"
}
```
