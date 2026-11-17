---
name: dataify-youtube-video-post
description: "用于 Dataify YouTube video post collection Builder 任务。当用户请求 YouTube video post collection tool、YouTube video collection/scraping、YouTube video post scraping、YouTube videos by URL、search filters、hashtag、podcast URL、keyword、Explore URL，或表达 YouTube 视频抓取/采集、YouTube 视频帖子采集、通过关键词/URL/标签/探索抓取 YouTube 视频等含义时触发。支持在 youtube_video-post_by-url、youtube_video-post_by-search-filters、youtube_video-post_by-hashtag、youtube_video-post_by-podcast-url、youtube_video-post_by-keyword、youtube_video-post_by-explore 之间选择，接收 task_id/status，并排查 Dataify Builder 请求。"
---

# Dataify YouTube Video Post

通过 Dataify Builder 提交 YouTube 视频帖子采集任务，然后停止。此技能是六种采集模式的引导式封装：

| 模式 | 采集器 ID | 用途 |
| --- | --- | --- |
| URL | `youtube_video-post_by-url` | 从 YouTube 频道视频 URL 采集视频帖子。 |
| Search Filters | `youtube_video-post_by-search-filters` | 通过关键词加过滤条件搜索视频帖子。 |
| Hashtag | `youtube_video-post_by-hashtag` | 通过标签采集视频帖子。 |
| Podcast URL | `youtube_video-post_by-podcast-url` | 从 YouTube 播客或播放列表 URL 采集视频帖子。 |
| Keyword | `youtube_video-post_by-keyword` | 通过关键词采集视频帖子。 |
| Explore | `youtube_video-post_by-explore` | 从 YouTube 探索 URL 采集视频帖子。 |

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

1. 首先请用户选择采集模式。展示模式选择表格。
2. 用户选择模式后，仅展示该模式的参数表和默认值。
3. 对于所选模式中的下拉式字段，以包含 `Label` 和 `Value` 列的 Markdown 表格展示所有允许的选项。
4. 询问用户在运行任务前是否需要修改任何值。
5. 询问用户是否需要为所选模式采集多组 YouTube 视频帖子。
6. 将最终值规范化为仅适用于所选模式的参数对象列表。
7. 从用户显式输入或已保存的 `DATAIFY_API_TOKEN` 解析 Dataify token。
8. 如果没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
9. 验证所选模式、参数和文件名。
10. 使用所选模式的 `spider_id` 提交 Builder 请求。
11. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
13. 告诉用户访问 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 模式选择

当用户调用此技能时，首先展示以下 Markdown 表格并请他们选择一种模式：

| 标签 | 值 |
| --- | --- |
| 通过频道视频 URL 采集视频帖子 | `url` |
| 通过搜索过滤条件采集视频帖子 | `search_filters` |
| 通过标签采集视频帖子 | `hashtag` |
| 通过播客 URL 采集视频帖子 | `podcast_url` |
| 通过关键词采集视频帖子 | `keyword` |
| 通过探索 URL 采集视频帖子 | `explore` |

提问："您想使用哪种采集模式？"

在模式明确之前不要提交 Builder 请求。

## URL 模式

仅当用户选择 `url` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `url` | 是 | `https://www.youtube.com/@stephcurry/videos` | YouTube 频道视频 URL。必须使用 `https://www.youtube.com`。 |
| `order_by` | 否 | `最新` | 下拉式选项。 |
| `start_index` | 否 | `1` | 大于或等于 `0` 的整数。 |
| `num_of_posts` | 否 | `5` | 大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。 |

`order_by` 选项：

| 标签 | 值 |
| --- | --- |
| Latest | `最新` |
| Popular | `热门` |
| Oldest | `最早` |

提交 `spider_id=youtube_video-post_by-url`，对象示例如下：

```json
[{"url":"https://www.youtube.com/@stephcurry/videos","order_by":"最新","start_index":"1","num_of_posts":"5"}]
```

如需采集多组 URL，提供多个 `url`、`order_by`、`start_index` 和 `num_of_posts` 对象。

## Search Filters 模式

仅当用户选择 `search_filters` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `keyword_search` | 是 | `popular music` | 用于搜索 YouTube 视频的关键词。 |
| `features` | 否 | `All` | 下拉式选项。 |
| `type` | 否 | `Videos` | 下拉式选项。 |
| `duration` | 否 | `Under 3 minutes` | 下拉式选项。 |
| `upload_date` | 否 | `Last hour` | 下拉式选项。 |
| `num_of_posts` | 否 | `200` | 大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。 |

`features` 选项：

| 标签 | 值 |
| --- | --- |
| All | `All` |
| Live | `Live` |
| 4K | `4K` |
| HD | `HD` |
| Subtitles/CC | `Subtitles/CC` |
| Creative Commons | `Creative Commons` |
| 360° | `360°` |
| VR180 | `VR180` |
| 3D | `3D` |
| HDR | `HDR` |

`type` 选项：

| 标签 | 值 |
| --- | --- |
| Video | `Videos` |
| Movie | `Movies` |

`duration` 选项：

| 标签 | 值 |
| --- | --- |
| 4 分钟以内 | `4 分钟以内` |
| 4-20 分钟 | `4-20 分钟` |
| 20 分钟以上 | `20 分钟以上` |
| 全部 | `None` |

`upload_date` 选项：

| 标签 | 值 |
| --- | --- |
| 上一小时 | `Last hour` |
| 今天 | `Today` |
| 本周 | `This week` |
| 本月 | `This month` |
| 今年 | `This year` |
| 全部 | `All` |

提交 `spider_id=youtube_video-post_by-search-filters`，对象示例如下：

```json
[{"keyword_search":"popular music","features":"Subtitles/CC","type":"Videos","duration":"None","upload_date":"Last hour","num_of_posts":"200"}]
```

如需采集多组搜索过滤条件，提供多个 `keyword_search`、`features`、`type`、`duration`、`upload_date` 和 `num_of_posts` 对象。

## Hashtag 模式

仅当用户选择 `hashtag` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `hashtag` | 是 | `shopping` | 用于过滤 YouTube 视频的话题标签。 |
| `num_of_posts` | 否 | `10` | 大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。 |

提交 `spider_id=youtube_video-post_by-hashtag`，对象示例如下：

```json
[{"hashtag":"shopping","num_of_posts":"10"}]
```

如需采集多组标签，提供多个 `hashtag` 和 `num_of_posts` 对象。

## Podcast URL 模式

仅当用户选择 `podcast_url` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `url` | 是 | `https://www.youtube.com/playlist?list=RDCLAK5uy_lS3E3PgpboCkZ_PfLPCkLLNPI1uH6kfc0` | YouTube 播客或播放列表 URL。必须使用 `https://www.youtube.com`。 |
| `num_of_posts` | 否 | `10` | 大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。 |

提交 `spider_id=youtube_video-post_by-podcast-url`，对象示例如下：

```json
[{"url":"https://www.youtube.com/playlist?list=RDCLAK5uy_lS3E3PgpboCkZ_PfLPCkLLNPI1uH6kfc0","num_of_posts":"10"}]
```

如需采集多组播客 URL，提供多个 `url` 和 `num_of_posts` 对象。

## Keyword 模式

仅当用户选择 `keyword` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `keyword` | 是 | `top videos` | 用于搜索 YouTube 视频的关键词。 |
| `num_of_posts` | 否 | `10` | 大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。 |

提交 `spider_id=youtube_video-post_by-keyword`，对象示例如下：

```json
[{"keyword":"top videos","num_of_posts":"10"}]
```

如需采集多组关键词，提供多个 `keyword` 和 `num_of_posts` 对象。

## Explore 模式

仅当用户选择 `explore` 时使用此部分。

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `url` | 是 | `https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D` | YouTube 探索 URL。必须使用 `https://www.youtube.com`。 |
| `all_tabs` | 否 | `true` | 下拉式选项。指定是否采集所有标签页。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。 |

`all_tabs` 选项：

| 标签 | 值 |
| --- | --- |
| 采集所有标签页 | `true` |
| 不采集所有标签页 | `false` |

提交 `spider_id=youtube_video-post_by-explore`，对象示例如下：

```json
[{"url":"https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D","all_tabs":"true"}]
```

如需采集多组探索，提供多个 `url` 和 `all_tabs` 对象。

## 共享参数处理

- `file_name` 默认值为 `{{TasksID}}`。
- 如果用户修改了 `file_name`，则提交用户提供的值。
- `file_name` 不能为空。
- 基于 URL 的模式仅接受协议和主机严格为 `https://www.youtube.com` 的 URL。
- 整数字段必须大于或等于 `0`。
- 将数值和布尔类型的值以字符串形式提交，与 Builder 示例保持一致。
- 将 `spider_parameters` 以包含一个或多个对象的数组的 JSON 字符串形式提交。

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- 授权头：`Bearer DATAIFY_API_TOKEN`
- 内容类型：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=youtube.com`
  - `spider_errors=true`
- 模式对应的 `spider_id`：
  - URL 模式：`youtube_video-post_by-url`
  - Search Filters 模式：`youtube_video-post_by-search-filters`
  - Hashtag 模式：`youtube_video-post_by-hashtag`
  - Podcast URL 模式：`youtube_video-post_by-podcast-url`
  - Keyword 模式：`youtube_video-post_by-keyword`
  - Explore 模式：`youtube_video-post_by-explore`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须是 JSON 字符串，不能是原始对象。

## 脚本

为确保稳定执行，建议使用 Python 3.6 或更高版本运行 `scripts/submit_dataify_youtube_video_post.py`，而不是重写 Builder 流程。

```powershell
python3 ".\scripts\submit_dataify_youtube_video_post.py" --mode keyword --keyword "top videos"
```

如果 `python3` 不可用，请使用该机器上的本地 Python 3 命令，例如 `python`。脚本会检查运行时版本，如果活动解释器版本过低，会提示用户使用 Python 3.6 或更高版本。

提交多组数据时，为所选模式传递 JSON 数组：

```powershell
python3 ".\scripts\submit_dataify_youtube_video_post.py" --mode hashtag --params-json '[{"hashtag":"shopping","num_of_posts":"10"},{"hashtag":"music","num_of_posts":"25"}]'
```

脚本会打印包含 `mode`、`spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。

`Unsupported mode` 表示模式必须是 `url`、`search_filters`、`hashtag`、`podcast_url`、`keyword` 或 `explore`。

`URL must use https://www.youtube.com` 表示 URL 不符合要求。

`Unsupported order_by`、`Unsupported all_tabs` 或其他不支持的下拉消息表示该值必须是该字段允许的值之一。

`File name cannot be empty` 表示未提供可用的 `file_name`。

缺少 `task_id` 通常表示授权头、token、`spider_name` 或所选 `spider_id` 有误。

## 安全规则

- 不要在同一个 Builder 请求中混合不同模式的参数。
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
