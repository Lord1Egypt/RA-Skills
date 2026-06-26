---
name: dataify-youtube-product-by-id
description: "提交 Dataify YouTube Video Basic Information by Video ID Builder 任务。当用户需要 YouTube video basic information collection tool、采集/抓取/爬取 YouTube 视频信息或视频详情、获取 YouTube video basic data、按 video ID 采集 video info、创建 youtube_product_by-id 任务，或表达 YouTube 视频基本信息采集/抓取、视频信息采集/抓取、视频详情采集/抓取、视频基本信息采集/抓取等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify YouTube Product By ID

通过 Dataify Builder 按视频 ID 提交 YouTube 视频基本信息采集任务。提交成功后，向用户提供 `task_id`、返回的或推断的状态，并告诉他们访问 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则使用该 token。
- 如果未提供 token，先检查环境变量中是否已保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用，无需要求用户重新输入 token。
- 如果本地没有可用的 token，告知用户需要提供 Dataify API TOKEN。
- 如果用户没有 API TOKEN，告诉他们可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录获取。
- 如果用户已有 API TOKEN，告诉他们可以在 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角找到。
- 用户提供 API TOKEN 且本地未保存 `DATAIFY_API_TOKEN` 后，询问是否希望将其本地保存为 `DATAIFY_API_TOKEN` 以便将来使用。
- 如果用户希望保存，提供适合其 shell 的命令并要求他们执行；不要在未确认的情况下静默持久化 token。
- 没有 token 不要调用 Builder 接口。
- 在面向用户的说明中始终称其为 `API TOKEN`。本地保存时优先使用环境变量名 `DATAIFY_API_TOKEN`。

PowerShell 示例，为当前会话保存 token：

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_DATAIFY_API_TOKEN"
```

Windows 上持久化用户级变量：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_DATAIFY_API_TOKEN", "User")
```

## 核心工作流程

1. 提交前，向用户展示参数清单中列出的必填值、共享值、可选值和默认值。
2. 对于下拉字段，以包含 `Label` 和 `Value` 列的 Markdown 表格展示所有允许的选项。使用 `scripts/submit_dataify_youtube_product_by_id.py --list-options` 打印完整的下拉表格。
3. 询问用户在运行任务前是否需要修改任何值。
4. 询问用户是否需要采集多条 YouTube 视频基本信息记录。如果是，要求提供多个 `video_id` 值。
5. 将最终的 `video_id` 值规范化为 `spider_parameters` 对象列表。
6. 将 `subtitles_language`、`subtitles_type` 和 `selected_only` 规范化为一个共享的 `spider_universal` 对象。
7. 从用户显式输入或已保存的 `DATAIFY_API_TOKEN` 解析 Dataify token。
8. 如果没有可用的 token，要求用户输入 API TOKEN，并询问是否将其保存为 `DATAIFY_API_TOKEN`。
9. 验证每个视频 ID、下拉值和文件名。
10. 提交 Builder 请求创建任务。
11. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
12. Builder 成功后停止。
13. 告诉用户访问 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 参数清单

当用户调用此技能时，首先告知他们使用了以下值。始终以 Markdown 表格展示提交的参数；不要使用纯文本或项目列表进行参数确认。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `video_id` | 是 | `8RePenzQH80` | `spider_parameters` | 唯一的 YouTube 视频 ID，用于标识需要采集基本信息的视频。 |
| `subtitles_language` | 否 | `ab` | `spider_universal` | 下拉式共享参数。字幕语言。 |
| `subtitles_type` | 否 | `auto_generated` | `spider_universal` | 下拉式共享参数。字幕类型。 |
| `selected_only` | 否 | `false` | `spider_universal` | 下拉式共享参数。是否仅使用选定的规格。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未修改时使用默认值。 |

然后提问："在我提交任务之前，您需要修改以上任何值吗？"

同时提问："您是否需要采集多条 YouTube 视频基本信息记录？如果是，请提供多个 `video_id` 值。"

如果用户已提供部分值，在表格中显示这些值替代默认值，仅询问是否需要修改剩余/默认值。

## 下拉选项

在要求用户选择下拉值之前，以包含 `Label` 和 `Value` 列的 Markdown 表格展示所有允许的选项。

使用以下命令打印完整表格：

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --list-options
```

如果 `python3` 不可用，请使用该机器上的本地 Python 3 命令，例如 `python`。

脚本会打印：

- `subtitles_language` 选项，使用提供的 `cn` 值作为 `Label`，`typeValue` 作为 `Value`。
- `subtitles_type` 选项。
- `selected_only` 选项。

## 参数处理

- `video_id` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `8RePenzQH80`。
- 去除 `video_id` 前后的空白字符。
- `video_id` 不能为空。
- 多组采集时仅在 `spider_parameters` 内重复 `video_id`。
- `subtitles_language`、`subtitles_type` 和 `selected_only` 是共享参数。将它们放在 `spider_universal` 中发送，不要放在每个 `spider_parameters` 对象内。
- `subtitles_language` 默认值为 `ab`。
- `subtitles_type` 默认值为 `auto_generated`。
- `selected_only` 默认值为 `false`。
- `file_name` 默认值为 `{{TasksID}}`。如果用户修改了它，提交用户提供的值。
- `file_name` 不能为空。

单组示例：

```json
spider_parameters=[{"video_id":"8RePenzQH80"}]
spider_universal={"subtitles_language":"ab","subtitles_type":"auto_generated","selected_only":"false"}
```

多组示例：

```json
spider_parameters=[{"video_id":"8RePenzQH80"},{"video_id":"dQw4w9WgXcQ"}]
spider_universal={"subtitles_language":"ab","subtitles_type":"auto_generated","selected_only":"false"}
```

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- 授权头：`Bearer DATAIFY_API_TOKEN`
- 内容类型：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=youtube.com`
  - `spider_id=youtube_product_by-id`
  - `spider_errors=true`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须是包含视频 ID 对象的 JSON 字符串数组。
  - `spider_universal` 必须是包含共享字幕设置的 JSON 字符串对象。

## 脚本

为确保稳定执行，建议使用 Python 3.6 或更高版本运行 `scripts/submit_dataify_youtube_product_by_id.py`，而不是重写 Builder 流程。

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --video-id "8RePenzQH80"
```

覆盖已保存的环境 token 或默认共享参数（单次运行）：

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --api-token "YOUR_DATAIFY_API_TOKEN" --video-id "8RePenzQH80" --subtitles-language "ab" --subtitles-type "auto_generated" --selected-only "false" --file-name "{{TasksID}}"
```

提交多个视频 ID：

```powershell
python3 ".\scripts\submit_dataify_youtube_product_by_id.py" --params-json '[{"video_id":"8RePenzQH80"},{"video_id":"dQw4w9WgXcQ"}]'
```

脚本会打印包含 `task_id`、`status`、`parameters`、`spider_universal`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否将其保存为 `DATAIFY_API_TOKEN`，或告诉他们可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录获取。如果已有 token，告诉他们可以在 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角找到。

`video_id cannot be empty` 表示缺少必填的 YouTube 视频 ID。

`Unsupported subtitles_language` 表示该值必须是允许的字幕语言代码之一。

`Unsupported subtitles_type` 表示该值必须是 `auto_generated` 或 `uploader_provided`。

`Unsupported selected_only` 表示该值必须是 `false` 或 `true`。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组、`spider_universal` 不是 JSON 字符串对象，或某个 `spider_parameters` 对象缺少 `video_id`。

缺少 `task_id` 通常表示授权头、token、`spider_name`、`spider_id`、`spider_parameters` 或 `spider_universal` 有误。

## 安全规则

- 不要将 `subtitles_language`、`subtitles_type` 或 `selected_only` 放入 `spider_parameters` 中。
- 不要省略 `spider_universal`。
- Builder 成功后不要轮询结果。
- 提及认证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要声称 Builder 响应包含 YouTube 视频数据文件。
- 不要编造结果字段。
- 任务创建成功后始终引导用户访问 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
