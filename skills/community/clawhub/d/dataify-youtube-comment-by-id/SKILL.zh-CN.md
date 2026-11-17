---
name: dataify-youtube-comment-by-id
description: "提交 Dataify YouTube Comment by Video ID Builder 任务，用于采集 YouTube 评论信息。当用户需要 YouTube comment collection tool、采集/抓取/爬取 YouTube comments、获取或提取 YouTube comment information/data、按 video ID 采集/抓取评论、创建 youtube_comment_by-id 任务，或表达 YouTube 评论信息采集/抓取、YouTube 评论采集/抓取等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查 Dataify Builder 请求。"
---

# Dataify YouTube Comment By ID

通过 Dataify Builder 按视频 ID 提交 YouTube 评论采集任务。提交成功后，向用户提供 `task_id`、返回的或推断的状态，并告诉他们访问 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

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

2. 询问用户在运行任务前是否需要修改任何值。
3. 询问用户是否需要采集多组 YouTube 评论。如果是，要求提供多组 `video_id`、`load_replies` 和 `num_of_comments`。
4. 将最终值规范化为参数对象列表。
5. 从用户显式输入或已保存的 `DATAIFY_API_TOKEN` 解析 Dataify token。
6. 如果没有可用的 token，要求用户输入 API TOKEN，并询问是否将其保存为 `DATAIFY_API_TOKEN`。
7. 验证每个视频 ID、数值和文件名。
8. 提交 Builder 请求创建任务。
9. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
11. 告诉用户访问 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 参数清单


| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `video_id` | 是 | `8RePenzQH80` | 唯一的 YouTube 视频 ID，用于标识需要采集评论的视频。 |
| `load_replies` | 是 | `10` | 大于或等于 `0` 的整数。在页面上加载回复时使用的时间。 |
| `num_of_comments` | 是 | `10` | 大于或等于 `0` 的整数。要采集的评论数量。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。用户未修改时使用默认值。 |

然后提问："在我提交任务之前，您需要修改以上任何值吗？"

同时提问："您是否需要采集多组 YouTube 评论？如果是，请提供多组 `video_id`、`load_replies` 和 `num_of_comments`。"

如果用户已提供部分值，在表格中显示这些值替代默认值，仅询问是否需要修改剩余/默认值。

如果将来添加任何下拉式字段，在要求用户选择之前，以包含 `Label` 和 `Value` 列的 Markdown 表格展示所有允许的选项。

## 参数处理

- `video_id` 为必填项。如果用户未提供，询问该必填值；不要使用文档示例值代替用户输入。
- 去除 `video_id` 前后的空白字符。
- `video_id` 不能为空。
- `load_replies` 为必填项。默认值：`10`。必须是大于或等于 `0` 的整数。
- `num_of_comments` 为必填项。默认值：`10`。必须是大于或等于 `0` 的整数。
- `file_name` 默认值为 `{{TasksID}}`。如果用户修改了它，提交用户提供的值。
- `file_name` 不能为空。
- 将数值以字符串形式提交以匹配 Builder 示例，例如 `"load_replies":"10"` 和 `"num_of_comments":"10"`。
- 将 `spider_parameters` 以包含一个或多个对象的数组的 JSON 字符串形式提交。

单组示例：

```json
[{"video_id":"8RePenzQH80","load_replies":"10","num_of_comments":"10"}]
```

多组示例：

```json
[{"video_id":"8RePenzQH80","load_replies":"10","num_of_comments":"10"},{"video_id":"dQw4w9WgXcQ","load_replies":"10","num_of_comments":"20"}]
```

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- 授权头：`Bearer DATAIFY_API_TOKEN`
- 内容类型：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=youtube.com`
  - `spider_id=youtube_comment_by-id`
  - `spider_errors=true`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须是 JSON 字符串，不能是原始对象。

## 脚本

为确保稳定执行，建议使用 Python 3.6 或更高版本运行 `scripts/submit_dataify_youtube_comment_by_id.py`，而不是重写 Builder 流程。

```powershell
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --video-id "8RePenzQH80"
```

如果 `python3` 不可用，请使用该机器上的本地 Python 3 命令，例如 `python`。脚本会检查运行时版本，如果活动解释器版本过低，会提示用户使用 Python 3.6 或更高版本。

覆盖已保存的环境 token 或默认参数（单次运行）：

```powershell
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --video-id "8RePenzQH80" --load-replies 10 --num-of-comments 10 --file-name "{{TasksID}}"
```

提交多组数据时，传递 JSON 数组：

```powershell
python3 ".\scripts\submit_dataify_youtube_comment_by_id.py" --params-json '[{"video_id":"8RePenzQH80","load_replies":"10","num_of_comments":"10"},{"video_id":"dQw4w9WgXcQ","load_replies":"10","num_of_comments":"20"}]'
```

脚本会打印包含 `task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否将其保存为 `DATAIFY_API_TOKEN`，或告诉他们可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录获取。如果已有 token，告诉他们可以在 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角找到。

`video_id cannot be empty` 表示缺少必填的 YouTube 视频 ID。

`load_replies must be an integer greater than or equal to 0` 表示请求的回复加载值无效。

`num_of_comments must be an integer greater than or equal to 0` 表示请求的评论数量无效。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串，或某个对象缺少 `video_id`、`load_replies` 或 `num_of_comments`。

缺少 `task_id` 通常表示授权头、token、`spider_name` 或 `spider_id` 有误。

## 安全规则

- Builder 成功后不要轮询结果。
- 提及认证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要声称 Builder 响应包含 YouTube 评论结果。
- 不要编造结果字段。
- 任务创建成功后始终引导用户访问 [Dataify](https://dashboard.dataify.com?utm_source=skill)。

## 参数交互策略

- 当请求意图明确、只读、低风险且成本较低时，使用安全默认值直接执行。可以用一句话说明执行内容，但不要暂停等待确认。
- 只在缺少必填输入、存在会明显改变结果的歧义、大批量或多页采集、媒体下载、会明显增加积分消耗、不可逆操作，或用户明确要求查看参数时询问。
- 必须确认时，只展示会影响目标、范围、输出或成本的用户参数。优先使用一句简短说明；只有三个及以上关键值确实需要比较时才使用精简表格。
- 不要展示固定字段、空的可选字段、未修改的默认值、凭据或内部实现参数，例如引擎选择、响应格式开关、偏移量、spider ID 和文件名模板。
- 默认隐藏高级筛选项，除非用户主动询问或需要它们消除歧义。不得用文档示例值代替用户缺失的必填输入。
- 先返回首个结果，再提供相关的细化选项，不要在首次执行前强迫用户决定所有可选项。

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
