---
name: dataify-instagram-reels
description: "提交 Dataify Instagram Reel Information Builder 任务，支持三种 Instagram Reel 采集模式。当用户需要 Instagram Reel information collection tool、采集/抓取/爬取 Instagram Reel information、Reels 或 Reel data，按 detail URL、list URL、website URL 采集 Instagram Reel 信息，创建 ins_reel_by-url、ins_allreel_by-url 或 ins_reel_by-listurl 任务，或表达 Instagram Reel 信息采集/抓取、Instagram Reels 采集/抓取、Instagram 短视频采集/抓取、Reel 详情 URL/列表 URL/网址采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify Instagram Reels

通过 Dataify Builder 提交 Instagram Reel 信息采集任务。此技能是三种采集模式的引导式封装：

| 模式 | 采集器 ID | 用途 |
| --- | --- | --- |
| 详情 URL | `ins_reel_by-url` | 按 Reel 详情 URL 采集一个或多个 Instagram Reels。 |
| 列表 URL | `ins_allreel_by-url` | 从 Instagram 列表/个人主页 URL 采集 Reels，支持数量和日期过滤。 |
| 网站 URL | `ins_reel_by-listurl` | 从 Instagram 网站/列表 URL 采集 Reels，支持数量和日期过滤。 |

提交成功后，向用户提供 `task_id`、返回或推断的状态，并告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

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

1. 首先要求用户选择采集模式：`detail-url`、`allreel-url` 或 `listurl`。
2. 用户选择模式后，仅展示该模式的参数表格和默认值。
3. 询问用户在运行任务前是否要修改任何值。
4. 询问用户是否要为所选模式采集多组 Instagram Reel。
5. 将最终值规范化为仅适用于所选模式的参数对象列表。
6. 从用户明确输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
7. 如果没有可用的 token，要求用户输入 API TOKEN 并询问是否保存为 `DATAIFY_API_TOKEN`。
8. 验证所选模式、Instagram URL、数值、日期和文件名。
9. 使用所选模式的 `spider_id` 提交 Builder 请求。
10. 从 Builder 响应中读取 `data.task_id`，并读取 `data.status` 或 `status`（如果存在）。
11. Builder 成功后停止。
12. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 模式选择

当用户调用此技能时，首先展示此 Markdown 表格并要求选择一种模式：

| 标签 | 值 |
| --- | --- |
| 按详情 URL 采集 Reel 信息 | `detail-url` |
| 按列表 URL 采集 Reel 信息 | `allreel-url` |
| 按网站 URL 采集 Reel 信息 | `listurl` |

询问："您要使用哪种采集模式：`detail-url`、`allreel-url` 还是 `listurl`？"

在模式明确之前不要提交 Builder 请求。

## 详情 URL 模式参数

仅当用户选择 `detail-url` 时使用此部分。

| 字段 | 必填 | 默认值 | 位置 | 备注 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.instagram.com/reel/C5Rdyj_q7YN/` | `spider_parameters` | Instagram Reel 详情 URL。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未修改时使用默认值。 |

然后询问："在我提交任务之前，您是否要修改这些值？"

同时询问："您是否要采集多组 Instagram Reel 详情 URL？如果是，请提供多个 `url` 值。"

详情 URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后使用默认值 `https://www.instagram.com/reel/C5Rdyj_q7YN/`。
- 去除 `url` 前后的空格。
- `url` 不能为空。
- `url` 必须以 `https://www.instagram.com/` 开头。
- 提交 `spider_id=ins_reel_by-url`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，例如：

```json
[{"url":"https://www.instagram.com/reel/C5Rdyj_q7YN/"}]
```

## 列表 URL 模式参数

仅当用户选择 `allreel-url` 时使用此部分。

| 字段 | 必填 | 默认值 | 位置 | 备注 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.instagram.com/billieeilish` | `spider_parameters` | Instagram 列表/个人主页 URL。 |
| `num_of_posts` | 否 | `10` | `spider_parameters` | 最大采集 Reel 数量。必须是大于等于 `0` 的整数。 |
| `posts_to_not_include` | 否 | `DP861NijuwE` | `spider_parameters` | 要排除的 Reel 帖子 ID 或 PK 值。多个值用英文逗号分隔。 |
| `start_date` | 否 | `01-28-2025` | `spider_parameters` | 开始日期，格式为 `mm-dd-yyyy`。必须在 `end_date` 之前或当天。 |
| `end_date` | 否 | `01-28-2026` | `spider_parameters` | 结束日期，格式为 `mm-dd-yyyy`。必须在 `start_date` 之后或当天。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未修改时使用默认值。 |

然后询问："在我提交任务之前，您是否要修改这些值？"

同时询问："您是否要采集多组 Instagram Reel 列表 URL？如果是，请提供多组 `url`、`num_of_posts`、`posts_to_not_include`、`start_date` 和 `end_date`。"

列表 URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后使用默认值 `https://www.instagram.com/billieeilish`。
- `url` 必须以 `https://www.instagram.com/` 开头。
- `num_of_posts` 必须是大于等于 `0` 的整数。
- `start_date` 和 `end_date` 必须使用 `mm-dd-yyyy` 格式。
- `start_date` 必须在 `end_date` 之前或当天。
- 提交 `spider_id=ins_allreel_by-url`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，例如：

```json
[{"url":"https://www.instagram.com/billieeilish","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]
```

## 网站 URL 模式参数

仅当用户选择 `listurl` 时使用此部分。

| 字段 | 必填 | 默认值 | 位置 | 备注 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.instagram.com/espn` | `spider_parameters` | Instagram 网站/列表 URL。 |
| `num_of_posts` | 否 | `10` | `spider_parameters` | 最大采集 Reel 数量。必须是大于等于 `0` 的整数。 |
| `posts_to_not_include` | 否 | `DP861NijuwE` | `spider_parameters` | 要排除的 Reel 帖子 ID 或 PK 值。多个值用英文逗号分隔。 |
| `start_date` | 否 | `01-28-2025` | `spider_parameters` | 开始日期，格式为 `mm-dd-yyyy`。必须在 `end_date` 之前或当天。 |
| `end_date` | 否 | `01-28-2026` | `spider_parameters` | 结束日期，格式为 `mm-dd-yyyy`。必须在 `start_date` 之后或当天。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未修改时使用默认值。 |

然后询问："在我提交任务之前，您是否要修改这些值？"

同时询问："您是否要采集多组 Instagram Reel 网站 URL？如果是，请提供多组 `url`、`num_of_posts`、`posts_to_not_include`、`start_date` 和 `end_date`。"

网站 URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后使用默认值 `https://www.instagram.com/espn`。
- `url` 必须以 `https://www.instagram.com/` 开头。
- `num_of_posts` 必须是大于等于 `0` 的整数。
- `start_date` 和 `end_date` 必须使用 `mm-dd-yyyy` 格式。
- `start_date` 必须在 `end_date` 之前或当天。
- 提交 `spider_id=ins_reel_by-listurl`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，例如：

```json
[{"url":"https://www.instagram.com/espn","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]
```

## 共享文件名处理

- `file_name` 默认为 `{{TasksID}}`。
- 如果用户修改 `file_name`，则提交用户提供的值。
- `file_name` 不能为空。
- 将 `file_name` 作为 Builder 表单字段发送。

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- 授权头：`Bearer DATAIFY_API_TOKEN`
- 内容类型：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=instagram.com`
  - `spider_errors=true`
- 模式特定字段：
  - 详情 URL 模式：`spider_id=ins_reel_by-url`
  - 列表 URL 模式：`spider_id=ins_allreel_by-url`
  - 网站 URL 模式：`spider_id=ins_reel_by-listurl`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须是 JSON 字符串数组。

## 脚本

为了稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_instagram_reels.py`，而不是重写 Builder 流程。

详情 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode detail-url --url "https://www.instagram.com/reel/C5Rdyj_q7YN/"
```

列表 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode allreel-url --url "https://www.instagram.com/billieeilish" --num-of-posts "10" --posts-to-not-include "DP861NijuwE" --start-date "01-28-2025" --end-date "01-28-2026"
```

网站 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode listurl --url "https://www.instagram.com/espn" --num-of-posts "10" --posts-to-not-include "DP861NijuwE" --start-date "01-28-2025" --end-date "01-28-2026"
```

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode detail-url --url "https://www.instagram.com/reel/C5Rdyj_q7YN/" --file-name "{{TasksID}}"
```

提交多组详情 URL：

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode detail-url --params-json '[{"url":"https://www.instagram.com/reel/C5Rdyj_q7YN/"},{"url":"https://www.instagram.com/reel/C5Rdyj_q7YN/"}]'
```

提交多组列表 URL：

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode allreel-url --params-json '[{"url":"https://www.instagram.com/billieeilish","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"},{"url":"https://www.instagram.com/billieeilish","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]'
```

提交多组网站 URL：

```powershell
python3 ".\scripts\submit_dataify_instagram_reels.py" --mode listurl --params-json '[{"url":"https://www.instagram.com/espn","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"},{"url":"https://www.instagram.com/espn","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]'
```

脚本会打印包含 `mode`、`spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否保存为 `DATAIFY_API_TOKEN`，或告知可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录获取。如果已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`Unsupported mode` 表示模式必须为 `detail-url`、`allreel-url` 或 `listurl`。

`url cannot be empty` 表示缺少 Instagram URL。

`url must start with https://www.instagram.com/` 表示 URL 不在允许的 Instagram 域名范围内。

`num_of_posts must be an integer greater than or equal to 0` 表示 Reel 数量无效。

`start_date must use mm-dd-yyyy format` 表示开始日期格式无效。

`end_date must use mm-dd-yyyy format` 表示结束日期格式无效。

`start_date must be on or before end_date` 表示日期范围无效。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组，或所选模式的对象缺少必填字段。

缺少 `task_id` 通常表示授权头、token、`spider_name`、所选 `spider_id` 或 `spider_parameters` 有误。

## 安全规则

- 不要在同一个 Builder 请求中混合详情 URL、列表 URL 和网站 URL 模式的参数。
- 在模式明确之前不要提交 Builder 请求。
- 不要将 `file_name` 放入 `spider_parameters` 中。
- 不要使用 `https://www.instagram.com/` 之外的 Instagram URL。
- 提及身份验证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要编造结果字段。
- 任务创建成功后始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
