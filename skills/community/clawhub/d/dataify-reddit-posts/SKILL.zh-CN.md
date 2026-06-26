---
name: dataify-reddit-posts
description: "提交 Dataify Reddit Post Information Builder 任务，支持三种 Reddit 帖子采集模式。当用户需要 Reddit post information collection tool、采集/抓取/爬取 Reddit posts 或 post data，按 post URL、keyword、subreddit URL 采集 Reddit posts，创建 reddit_posts_by-url、reddit_posts_by-keywords 或 reddit_posts_by-subredditurl 任务，或表达 Reddit 帖子采集/抓取、帖子信息采集/抓取、帖子 URL 采集、关键词采集、subreddit url 采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify Reddit Posts

通过 Dataify Builder 提交 Reddit 帖子信息采集任务。本技能是三种采集模式的引导封装：

| 模式 | 采集器 ID | 用途 |
| --- | --- | --- |
| 帖子 URL | `reddit_posts_by-url` | 通过帖子 URL 采集一个或多个 Reddit 帖子。 |
| 关键词 | `reddit_posts_by-keywords` | 通过搜索关键词采集 Reddit 帖子。 |
| Subreddit URL | `reddit_posts_by-subredditurl` | 通过 subreddit URL 采集 Reddit 帖子，支持排序和时间选项。 |

提交成功后，向用户提供 `task_id`、返回的或推断的状态，并告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

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

1. 首先询问用户选择采集模式：`url`、`keywords` 或 `subredditurl`。
2. 用户选择模式后，仅展示该模式的参数表格和默认值。
3. 如果所选模式有下拉字段，以包含 `Label` 和 `Value` 列的 Markdown 表格展示下拉选项。
4. 询问用户是否需要在运行任务前修改任何值。
5. 询问用户是否需要为所选模式采集多组 Reddit 帖子。
6. 将最终值规范化为仅包含所选模式的参数对象列表。
7. 从显式输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
8. 如果没有可用的 token，要求用户输入 API TOKEN 并询问是否将其保存为 `DATAIFY_API_TOKEN`。
9. 验证所选模式、URL、数值、下拉值和文件名。
10. 使用所选模式的 `spider_id` 提交 Builder 请求。
11. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
12. Builder 成功后停止。
13. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 模式选择

当用户调用此技能时，首先展示以下 Markdown 表格并要求选择一种模式：

| 标签 | 值 |
| --- | --- |
| 通过帖子 URL 采集 Reddit 帖子 | `url` |
| 通过关键词采集 Reddit 帖子 | `keywords` |
| 通过 subreddit URL 采集 Reddit 帖子 | `subredditurl` |

询问："您想使用哪种采集模式：`url`、`keywords` 还是 `subredditurl`？"

在模式明确之前不要提交 Builder 请求。

## 帖子 URL 模式参数

仅当用户选择 `url` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/` | `spider_parameters` | Reddit 帖子 URL。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后询问："您是否需要在提交任务前修改这些值？"

同时询问："您是否需要采集多组 Reddit 帖子 URL？如果是，请提供多个 `url` 值。"

帖子 URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/`。
- 去除 `url` 的前后空白字符。
- `url` 不能为空。
- `url` 必须以 `https://www.reddit.com/` 开头。
- 提交 `spider_id=reddit_posts_by-url`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"url":"https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"}]
```

## 关键词模式参数

仅当用户选择 `keywords` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `keyword` | 是 | `datascience` | `spider_parameters` | Reddit 帖子搜索关键词。 |
| `num_of_posts` | 否 | `10` | `spider_parameters` | 最大采集帖子数。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后询问："您是否需要在提交任务前修改这些值？"

同时询问："您是否需要采集多组 Reddit 关键词？如果是，请提供多组 `keyword` 和 `num_of_posts`。"

关键词模式处理：

- `keyword` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `datascience`。
- 去除 `keyword` 的前后空白字符。
- `keyword` 不能为空。
- `num_of_posts` 必须为大于或等于 `0` 的整数。
- 提交 `spider_id=reddit_posts_by-keywords`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"keyword":"datascience","num_of_posts":"10"}]
```

## Subreddit URL 模式参数

仅当用户选择 `subredditurl` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.reddit.com/r/battlefield2042` | `spider_parameters` | Subreddit URL。 |
| `sort_by` | 否 | `Hot` | `spider_parameters` | 帖子排序选项。 |
| `num_of_posts` | 否 | `10` | `spider_parameters` | 最大采集帖子数。必须为大于或等于 `0` 的整数。 |
| `sort_by_time` | 否 | `Now` | `spider_parameters` | 时间排序选项。时间字段在 `Hot` 和 `New` 排序下不生效。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

`sort_by` 下拉选项：

| 标签 | 值 |
| --- | --- |
| Hot | `Hot` |
| Top | `Top` |
| New | `New` |
| Rising | `Rising` |

`sort_by_time` 下拉选项：

| 标签 | 值 |
| --- | --- |
| Now | `Now` |
| Today | `Today` |
| This Week | `This Week` |
| This Month | `This Month` |
| This Year | `This Year` |
| All Time | `All Time` |

然后询问："您是否需要在提交任务前修改这些值？"

同时询问："您是否需要采集多组 Reddit subreddit URL？如果是，请提供多组 `url`、`sort_by`、`num_of_posts` 和 `sort_by_time`。"

Subreddit URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `https://www.reddit.com/r/battlefield2042`。
- 去除 `url` 的前后空白字符。
- `url` 不能为空。
- `url` 必须以 `https://www.reddit.com/` 开头。
- `sort_by` 必须为 `Hot`、`Top`、`New` 或 `Rising` 之一。
- `sort_by_time` 必须为 `Now`、`Today`、`This Week`、`This Month`、`This Year` 或 `All Time` 之一。
- `num_of_posts` 必须为大于或等于 `0` 的整数。
- 时间字段在 `Hot` 和 `New` 排序下不生效；如果用户提供了值，仍保留提交。
- 提交 `spider_id=reddit_posts_by-subredditurl`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"url":"https://www.reddit.com/r/battlefield2042","sort_by":"Rising","num_of_posts":"10","sort_by_time":"Now"}]
```

## 共享文件名处理

- `file_name` 默认为 `{{TasksID}}`。
- 如果用户更改了 `file_name`，提交用户提供的值。
- `file_name` 不能为空。
- 将 `file_name` 作为 Builder 表单字段发送。

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- Authorization 请求头：`Bearer DATAIFY_API_TOKEN`
- Content type：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=reddit.com`
  - `spider_errors=true`
- 模式特定字段：
  - 帖子 URL 模式：`spider_id=reddit_posts_by-url`
  - 关键词模式：`spider_id=reddit_posts_by-keywords`
  - Subreddit URL 模式：`spider_id=reddit_posts_by-subredditurl`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须为 JSON 字符串数组。

## 脚本

为确保稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_reddit_posts.py`，而非重写 Builder 流程。

帖子 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode url --url "https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"
```

关键词模式：

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode keywords --keyword "datascience" --num-of-posts "10"
```

Subreddit URL 模式：

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode subredditurl --url "https://www.reddit.com/r/battlefield2042" --sort-by "Rising" --num-of-posts "10" --sort-by-time "Now"
```

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode keywords --keyword "datascience" --file-name "{{TasksID}}"
```

提交多组帖子 URL：

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode url --params-json '[{"url":"https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"},{"url":"https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"}]'
```

提交多组关键词：

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode keywords --params-json '[{"keyword":"datascience","num_of_posts":"10"},{"keyword":"machinelearning","num_of_posts":"10"}]'
```

提交多组 subreddit URL：

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode subredditurl --params-json '[{"url":"https://www.reddit.com/r/battlefield2042","sort_by":"Rising","num_of_posts":"10","sort_by_time":"Now"},{"url":"https://www.reddit.com/r/battlefield2042","sort_by":"Rising","num_of_posts":"10","sort_by_time":"Now"}]'
```

脚本会打印包含 `mode`、`spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否将其保存为 `DATAIFY_API_TOKEN`，或告知用户可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。如果用户已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`Unsupported mode` 表示模式必须为 `url`、`keywords` 或 `subredditurl`。

`url cannot be empty` 表示缺少 Reddit URL。

`url must start with https://www.reddit.com/` 表示 URL 不在允许的 Reddit 域名范围内。

`keyword cannot be empty` 表示缺少 Reddit 关键词。

`num_of_posts must be an integer greater than or equal to 0` 表示帖子数量无效。

`sort_by must be one of Hot, Top, New, Rising` 表示 subreddit 排序选项无效。

`sort_by_time must be one of Now, Today, This Week, This Month, This Year, All Time` 表示 subreddit 时间选项无效。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组，或所选模式的对象缺少必填字段。

缺少 `task_id` 通常表示 authorization 请求头、token、`spider_name`、所选 `spider_id` 或 `spider_parameters` 有误。

## 安全规则

- 不要在同一个 Builder 请求中混合帖子 URL、关键词和 Subreddit URL 模式的参数。
- 在模式明确之前不要提交 Builder 请求。
- 不要将 `file_name` 放入 `spider_parameters` 中。
- 不要使用 `https://www.reddit.com/` 以外的 Reddit URL。
- 提及身份验证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要编造结果字段。
- 任务创建成功后始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
