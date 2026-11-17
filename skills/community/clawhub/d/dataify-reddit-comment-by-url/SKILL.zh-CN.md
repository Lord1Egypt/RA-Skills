---
name: dataify-reddit-comment-by-url
description: "提交 Dataify Reddit Post Comment by URL Builder 任务。当用户需要 Reddit post comment collection tool、采集/抓取/爬取 Reddit 帖子评论或评论数据、按 URL 采集 Reddit comments、创建 reddit_comment_by-url 任务，或表达 Reddit 帖子评论采集/抓取、Reddit 评论采集/抓取、Reddit 帖子 URL 评论采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify Reddit Comment By URL

通过 Dataify Builder 按 Reddit URL 提交 Reddit 帖子评论采集任务。提交成功后，向用户提供 `task_id`、返回的或推断的状态，并告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则在本次运行中使用该 token。
- 如果未提供 token，先检查环境中是否已在本地保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用，无需要求用户重新输入。
- 如果本地没有可用的 token，告知用户需要提供 Dataify API TOKEN。
- 如果用户没有 API TOKEN，告知用户可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。
- 如果用户已有 API TOKEN，告知用户可以在 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角找到。
- 用户提供 API TOKEN 后，如果本地未保存 `DATAIFY_API_TOKEN`，询问是否将其保存为 `DATAIFY_API_TOKEN` 以供后续使用。
- 如果用户希望保存，提供适合其 shell 的命令并要求其执行；不要在未经确认的情况下静默保存 token。
- 没有 token 不要调用 Builder 接口。
- 在面向用户的说明中始终称其为 `API TOKEN`。保存到本地时优先使用环境变量名 `DATAIFY_API_TOKEN`。

PowerShell 示例，为当前会话保存 token：

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_DATAIFY_API_TOKEN"
```

在 Windows 上设置持久的用户级变量：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_DATAIFY_API_TOKEN", "User")
```

## 核心工作流程

2. 询问用户是否需要在运行任务前修改任何值。
3. 询问用户是否需要采集多组 Reddit 评论。如果是，要求提供多组 `url`、`days_back` 和 `comment_limit`。
4. 将最终值规范化为 `spider_parameters` 对象列表。
5. 从显式输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
6. 如果没有可用的 token，要求用户输入 API TOKEN 并询问是否将其保存为 `DATAIFY_API_TOKEN`。
7. 验证 Reddit URL、数值和文件名。
8. 使用 `spider_id=reddit_comment_by-url` 提交 Builder 请求。
9. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
11. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 参数清单


| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button` | `spider_parameters` | Reddit URL。 |
| `days_back` | 否 | `10` | `spider_parameters` | 评论回溯天数。必须为大于或等于 `0` 的整数。 |
| `comment_limit` | 否 | `5` | `spider_parameters` | 回复评论限制数。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |


同时询问："您是否需要采集多组 Reddit 评论？如果是，请提供多组 `url`、`days_back` 和 `comment_limit`。"

如果用户已提供部分值，在表格中显示这些值替代默认值，仅询问是否需要修改剩余/默认值。

## 参数处理

- `url` 为必填项。如果用户未提供，询问该必填值；不要使用文档示例值代替用户输入。
- 去除 `url` 的前后空白字符。
- `url` 不能为空。
- `url` 必须以 `https://www.reddit.com/` 开头。
- `days_back` 必须为大于或等于 `0` 的整数。
- `comment_limit` 必须为大于或等于 `0` 的整数。
- 多组采集在 `spider_parameters` 中重复 `url`、`days_back` 和 `comment_limit`。
- `file_name` 默认为 `{{TasksID}}`。如果用户更改了，提交用户提供的值。
- `file_name` 不能为空。

单组示例：

```json
spider_parameters=[{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"}]
```

多组示例：

```json
spider_parameters=[{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"},{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"}]
```

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- Authorization 请求头：`Bearer DATAIFY_API_TOKEN`
- Content type：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=reddit.com`
  - `spider_id=reddit_comment_by-url`
  - `spider_errors=true`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须为 Reddit 评论对象的 JSON 字符串数组。

## 脚本

为确保稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_reddit_comment_by_url.py`，而非重写 Builder 流程。

```powershell
python3 ".\scripts\submit_dataify_reddit_comment_by_url.py" --url "https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button" --days-back "10" --comment-limit "5"
```

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_reddit_comment_by_url.py" --url "https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button" --file-name "{{TasksID}}"
```

提交多组 Reddit 评论：

```powershell
python3 ".\scripts\submit_dataify_reddit_comment_by_url.py" --params-json '[{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"},{"url":"https://www.reddit.com/r/datascience/comments/1cmnf0m/comment/l32204i/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button","days_back":"10","comment_limit":"5"}]'
```

脚本会打印包含 `spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否将其保存为 `DATAIFY_API_TOKEN`，或告知用户可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。如果用户已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`url cannot be empty` 表示缺少 Reddit URL。

`url must start with https://www.reddit.com/` 表示 URL 不在允许的 Reddit 域名范围内。

`days_back must be an integer greater than or equal to 0` 表示天数限制无效。

`comment_limit must be an integer greater than or equal to 0` 表示回复评论限制无效。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组，或某个 `spider_parameters` 对象缺少必填字段。

缺少 `task_id` 通常表示 authorization 请求头、token、`spider_name`、`spider_id` 或 `spider_parameters` 有误。

## 安全规则

- 不要将 `file_name` 放入 `spider_parameters` 中。
- 不要使用 `https://www.reddit.com/` 以外的 Reddit URL。
- 提及身份验证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要编造结果字段。
- 任务创建成功后始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。

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
