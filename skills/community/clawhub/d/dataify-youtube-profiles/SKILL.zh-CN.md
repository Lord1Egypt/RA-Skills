---
name: dataify-youtube-profiles
description: "用于 Dataify YouTube profile collection Builder 任务。当用户请求 YouTube profile collection tool、YouTube profiles collection、YouTube channel profile collection、YouTube profile scraping、YouTube profiles by URL、YouTube profiles by keyword，或需要在 youtube_profiles_by-url 与 youtube_profiles_by-keyword 间选择时触发；也覆盖 YouTube 个人资料采集/抓取、频道资料采集/抓取、个人主页采集/抓取、通过 URL 或关键词采集/抓取 YouTube 个人资料等中文表述。支持返回 task_id 和 status、配置或复用 DATAIFY_API_TOKEN，并排查 Dataify Builder 请求失败。"
---

# Dataify YouTube Profiles

通过 Dataify Builder 提交 YouTube 个人资料采集任务，然后停止。此技能是两种采集模式的引导式封装：

| 模式 | 采集器 ID | 用途 |
| --- | --- | --- |
| URL | `youtube_profiles_by-url` | 采集一个或多个特定的 YouTube 频道资料 URL。 |
| Keyword | `youtube_profiles_by-keyword` | 通过关键词和页数搜索 YouTube 频道资料。 |

提交成功后，向用户提供 `task_id`、返回的或推断的状态，并告诉他们访问 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则使用该 token。
- 如果未提供 token，先检查环境变量中是否已保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用。
- 如果本地没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
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

1. 首先请用户选择采集模式：URL 或 Keyword。展示模式选择表格。
2. 用户选择模式后，仅展示该模式的参数表和默认值。
3. 询问用户在运行任务前是否需要修改任何值。
4. 询问用户是否需要为所选模式采集多组 YouTube 个人资料。
5. 将最终值规范化为仅适用于所选模式的参数对象列表。
6. 从用户显式输入或已保存的 `DATAIFY_API_TOKEN` 解析 Dataify token。
7. 如果没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
8. 验证所选模式、参数和文件名。
9. 使用所选模式的 `spider_id` 提交 Builder 请求。
10. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
11. Builder 成功后停止。
12. 告诉用户访问 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 模式选择

当用户调用此技能时，首先展示以下 Markdown 表格并请他们选择一种模式：

| 标签 | 值 |
| --- | --- |
| 通过 URL 采集个人资料 | `url` |
| 通过关键词采集个人资料 | `keyword` |

提问："您想使用哪种采集模式：`url` 还是 `keyword`？"

在模式明确之前不要提交 Builder 请求。

## URL 模式参数

仅当用户选择 `url` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `url` | 是 | `https://www.youtube.com/@mrbeast` | YouTube 频道 URL。URL 必须使用 `https://www.youtube.com` 域名。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。用户未修改时使用默认值。 |

然后提问："在我提交任务之前，您需要修改以上任何值吗？"

同时提问："您是否需要采集多组 YouTube 个人资料 URL？如果是，请提供多个 `url` 值。"

URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `https://www.youtube.com/@mrbeast`。
- 仅接受协议和主机严格为 `https://www.youtube.com` 的 URL。拒绝任何其他协议、主机或子域名，视为不符合要求。
- 提交 `spider_id=youtube_profiles_by-url`。
- 将 `spider_parameters` 以包含一个或多个对象的 JSON 字符串形式提交，如：

```json
[{"url":"https://www.youtube.com/@mrbeast"}]
```

## Keyword 模式参数

仅当用户选择 `keyword` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `keyword` | 是 | `MrBeast` | 用于搜索 YouTube 频道或个人资料的关键词。 |
| `page_turning` | 是 | `1` | 大于或等于 `0` 的整数。指定要采集的搜索结果页数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。用户未修改时使用默认值。 |

然后提问："在我提交任务之前，您需要修改以上任何值吗？"

同时提问："您是否需要采集多组 YouTube 个人资料关键词？如果是，请提供多组 `keyword` 和 `page_turning`。"

Keyword 模式处理：

- `keyword` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `MrBeast`。
- 去除 `keyword` 前后的空白字符。
- `keyword` 不能为空。
- `page_turning` 为必填项。默认值：`1`。必须是大于或等于 `0` 的整数。
- 将数值以字符串形式提交以匹配 Builder 示例，例如 `"page_turning":"1"`。
- 提交 `spider_id=youtube_profiles_by-keyword`。
- 将 `spider_parameters` 以包含一个或多个对象的 JSON 字符串形式提交，如：

```json
[{"keyword":"MrBeast","page_turning":"1"}]
```

## 共享文件名处理

- `file_name` 默认值为 `{{TasksID}}`。
- 如果用户修改了 `file_name`，提交用户提供的值。
- `file_name` 不能为空。
- 将 `file_name` 作为 Builder 表单字段发送。

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- 授权头：`Bearer DATAIFY_API_TOKEN`
- 内容类型：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=youtube.com`
  - `spider_errors=true`
- 模式对应字段：
  - URL 模式：`spider_id=youtube_profiles_by-url`
  - Keyword 模式：`spider_id=youtube_profiles_by-keyword`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须是 JSON 字符串，不能是原始对象。

## 脚本

为确保稳定执行，建议使用 Python 3.6 或更高版本运行 `scripts/submit_dataify_youtube_profiles.py`，而不是重写 Builder 流程。

URL 模式：

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode url --url "https://www.youtube.com/@mrbeast"
```

Keyword 模式：

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode keyword --keyword "MrBeast" --page-turning 1
```

如果 `python3` 不可用，请使用该机器上的本地 Python 3 命令，例如 `python`。脚本会检查运行时版本，如果活动解释器版本过低，会提示用户使用 Python 3.6 或更高版本。

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode url --url "https://www.youtube.com/@mrbeast" --file-name "{{TasksID}}"
```

提交多组 URL：

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode url --params-json '[{"url":"https://www.youtube.com/@mrbeast"},{"url":"https://www.youtube.com/@YouTube"}]'
```

提交多组关键词：

```powershell
python3 ".\scripts\submit_dataify_youtube_profiles.py" --mode keyword --params-json '[{"keyword":"MrBeast","page_turning":"1"},{"keyword":"cooking","page_turning":"2"}]'
```

脚本会打印包含 `mode`、`spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。

`Unsupported mode` 表示模式必须是 `url` 或 `keyword`。

`URL must use https://www.youtube.com` 表示 URL 不符合要求。要求用户提供以 `https://www.youtube.com` 开头的 URL，例如 `https://www.youtube.com/@mrbeast`。

`keyword cannot be empty` 表示缺少关键词。

`page_turning must be an integer greater than or equal to 0` 表示请求的页数无效。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串，或所选模式的对象缺少必填字段。

缺少 `task_id` 通常表示授权头、token、`spider_name` 或所选 `spider_id` 有误。

## 安全规则

- 不要在同一个 Builder 请求中混合 URL 模式和 Keyword 模式的参数。
- 不要在 URL 模式中发送 `keyword` 或 `page_turning`。
- 不要在 Keyword 模式中发送 `url`。
- 不要编造结果字段。
- 任务创建成功后始终引导用户访问 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
