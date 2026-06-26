---
name: dataify-facebook-comment-by-url
description: "提交 Dataify Facebook Post Comment by URL Builder 任务。当用户需要 Facebook post comment collection tool、采集/抓取/爬取 Facebook 帖子评论或评论数据、按 URL 采集 Facebook 评论、创建 facebook_comment_by-comments-url 任务，或表达 Facebook 帖子评论采集/抓取、Facebook 评论采集/抓取、帖子评论采集/抓取、评论 URL 采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify Facebook Comment By URL

通过 Dataify Builder 按帖子 URL 提交 Facebook 帖子评论采集任务。提交成功后，向用户提供 `task_id`、返回或推断的状态，并告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则在本次运行中使用该 token。
- 如果未提供 token，先检查环境变量中是否已保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用，无需要求用户重新输入。
- 如果本地没有可用的 token，告知用户需要提供 Dataify API TOKEN。
- 如果用户没有 API TOKEN，告知他们可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。
- 如果用户已有 API TOKEN，告知他们可以在 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角找到。
- 用户提供 API TOKEN 后，如果本地未保存 `DATAIFY_API_TOKEN`，询问是否将其保存为 `DATAIFY_API_TOKEN` 以供将来使用。
- 如果用户想要保存，提供适合其 shell 的命令并要求用户执行；不要在未经确认的情况下静默保存 token。
- 没有 token 不要调用 Builder 接口。
- 在面向用户的说明中始终称其为 `API TOKEN`。本地保存时优先使用环境变量名 `DATAIFY_API_TOKEN`。

PowerShell 当前会话保存 token 示例：

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_DATAIFY_API_TOKEN"
```

Windows 永久用户级变量设置：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_DATAIFY_API_TOKEN", "User")
```

## 核心工作流程

1. 提交前，向用户展示参数清单中列出的必填值、可选值和默认值。
2. 对于下拉字段，以包含 `Label` 和 `Value` 列的 Markdown 表格展示所有允许的选项。
3. 询问用户在运行任务前是否要修改任何值。
4. 询问用户是否要采集多组 Facebook 帖子评论。如果是，要求提供多组 `url`、`get_all_replies`、`limit_records` 和 `comments_sort`。
5. 将最终值规范化为 `spider_parameters` 对象列表。
6. 从用户明确输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
7. 如果没有可用的 token，要求用户输入 API TOKEN 并询问是否保存为 `DATAIFY_API_TOKEN`。
8. 验证 URL、下拉值、数值和文件名。
9. 使用 `spider_id=facebook_comment_by-comments-url` 提交 Builder 请求。
10. 从 Builder 响应中读取 `data.task_id`，并读取 `data.status` 或 `status`（如果存在）。
11. Builder 成功后停止。
12. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 参数清单

当用户调用此技能时，首先告知这些值的使用情况。始终以 Markdown 表格展示提交的参数；不要使用纯文本或项目列表进行参数确认。

| 字段 | 必填 | 默认值 | 位置 | 备注 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.facebook.com/share/p/1K6xfHFkrK/` | `spider_parameters` | Facebook 帖子 URL。 |
| `get_all_replies` | 否 | `True` | `spider_parameters` | 下拉参数。是否采集所有回复。 |
| `limit_records` | 否 | `10` | `spider_parameters` | 大于等于 `0` 的整数。最大回复数量。 |
| `comments_sort` | 否 | `All comments` | `spider_parameters` | 下拉参数。评论排序方式。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未修改时使用默认值。 |

然后询问："在我提交任务之前，您是否要修改这些值？"

同时询问："您是否要采集多组 Facebook 帖子评论？如果是，请提供多组 `url`、`get_all_replies`、`limit_records` 和 `comments_sort`。"

如果用户已提供部分值，在表格中显示这些值替代默认值，只询问是否修改剩余/默认的值。

## 下拉选项

以包含 `Label` 和 `Value` 列的 Markdown 表格展示这些下拉选项。

`get_all_replies` 选项：

| Label | Value |
| --- | --- |
| True | `True` |
| Flase | `Flase` |

`comments_sort` 选项：

| Label | Value |
| --- | --- |
| 最相关 | `Most Relevent` |
| 由新到旧 | `Newest` |
| 所有评论 | `All comments` |

## 参数处理

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后使用默认值 `https://www.facebook.com/share/p/1K6xfHFkrK/`。
- 去除 `url` 前后的空格。
- `url` 不能为空。
- `url` 必须以 `https://www.facebook.com/` 开头。
- `get_all_replies` 默认为 `True`。允许的值为 `True` 和 `Flase`。
- `limit_records` 默认为 `10`。必须是大于等于 `0` 的整数。
- 数值以字符串形式提交，与 Builder 示例一致，例如 `"limit_records":"10"`。
- `comments_sort` 默认为 `All comments`。允许的值为 `Most Relevent`、`Newest` 和 `All comments`。
- `file_name` 默认为 `{{TasksID}}`。如果用户修改，则提交用户提供的值。
- `file_name` 不能为空。

单组示例：

```json
spider_parameters=[{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"}]
```

多组示例：

```json
spider_parameters=[{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"},{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"}]
```

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- 授权头：`Bearer DATAIFY_API_TOKEN`
- 内容类型：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=facebook.com`
  - `spider_id=facebook_comment_by-comments-url`
  - `spider_errors=true`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须是评论参数对象的 JSON 字符串数组。

## 脚本

为了稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_facebook_comment_by_url.py`，而不是重写 Builder 流程。

```powershell
python3 ".\scripts\submit_dataify_facebook_comment_by_url.py" --url "https://www.facebook.com/share/p/1K6xfHFkrK/"
```

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_facebook_comment_by_url.py" --api-token "YOUR_DATAIFY_API_TOKEN" --url "https://www.facebook.com/share/p/1K6xfHFkrK/" --get-all-replies "True" --limit-records "10" --comments-sort "All comments" --file-name "{{TasksID}}"
```

提交多组参数：

```powershell
python3 ".\scripts\submit_dataify_facebook_comment_by_url.py" --params-json '[{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"},{"url":"https://www.facebook.com/share/p/1K6xfHFkrK/","get_all_replies":"True","limit_records":"10","comments_sort":"All comments"}]'
```

脚本会打印包含 `spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否保存为 `DATAIFY_API_TOKEN`，或告知可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录获取。如果已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`url cannot be empty` 表示缺少必填的 Facebook 帖子 URL。

`url must start with https://www.facebook.com/` 表示 URL 不在允许的 Facebook 域名范围内。

`Unsupported get_all_replies` 表示值必须为 `True` 或 `Flase`。

`limit_records must be an integer greater than or equal to 0` 表示回复数量无效。

`Unsupported comments_sort` 表示值必须为 `Most Relevent`、`Newest` 或 `All comments`。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组，或某个 `spider_parameters` 对象缺少必填字段。

缺少 `task_id` 通常表示授权头、token、`spider_name`、`spider_id` 或 `spider_parameters` 有误。

## 安全规则

- 不要将 `file_name` 放入 `spider_parameters` 中。
- 不要使用 `https://www.facebook.com/` 之外的 Facebook URL。
- 提及身份验证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要编造结果字段。
- 任务创建成功后始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
