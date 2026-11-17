---
name: dataify-google-map-details
description: "提交 Dataify Google Map Details Builder 任务，支持四种 Google Maps 详情采集模式。当用户需要 Google map details collection tool、采集/抓取/爬取 Google Maps 详情、信息、地图数据或商家详情，按 URL、CID、location、place_id 采集 Google map details，创建 google_map-details_by-url、google_map-details_by-cid、google_map-details_by-location 或 google_map-details_by-placeid 任务，或表达 Google 地图信息/详细信息采集/抓取、Google Maps 信息采集/抓取、谷歌地图信息采集/抓取、Google 地图 URL/CID/位置/place_id/place ID/商家 ID 采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify Google Map Details

通过 Dataify Builder 提交 Google 地图详细信息采集任务。本技能是四种采集模式的引导封装：

| 模式 | 采集器 ID | 用途 |
| --- | --- | --- |
| URL | `google_map-details_by-url` | 通过 Google Maps URL 采集一条或多条 Google 地图详细记录。 |
| CID | `google_map-details_by-cid` | 通过 CID 采集一条或多条 Google 地图详细记录。 |
| 位置 | `google_map-details_by-location` | 通过关键词、国家、纬度、经度和缩放级别采集 Google 地图详细记录。 |
| Place ID | `google_map-details_by-placeid` | 通过 place ID 采集一条或多条 Google 地图详细记录。 |

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

1. 首先询问用户选择采集模式：`url`、`cid`、`location` 或 `placeid`。
2. 用户选择模式后，仅展示该模式的参数表格和默认值。
3. 对于 `location` 模式，以包含 `Label` 和 `Value` 列的 Markdown 表格展示 `country` 下拉选项。使用 `references/google_countries.md`。
4. 询问用户是否需要在运行任务前修改任何值。
5. 询问用户是否需要为所选模式采集多组 Google 地图详细信息。
6. 将最终值规范化为仅包含所选模式的参数对象列表。
7. 从显式输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
8. 如果没有可用的 token，要求用户输入 API TOKEN 并询问是否将其保存为 `DATAIFY_API_TOKEN`。
9. 验证所选模式、URL、CID、place ID、关键词、国家、数值和文件名。
10. 使用所选模式的 `spider_id` 提交 Builder 请求。
11. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
13. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 模式选择

当用户调用此技能时，首先展示以下 Markdown 表格并要求选择一种模式：

| 标签 | 值 |
| --- | --- |
| 通过 URL 采集 Google 地图详细信息 | `url` |
| 通过 CID 采集 Google 地图详细信息 | `cid` |
| 通过位置采集 Google 地图详细信息 | `location` |
| 通过 place ID 采集 Google 地图详细信息 | `placeid` |

询问："您想使用哪种采集模式：`url`、`cid`、`location` 还是 `placeid`？"

在模式明确之前不要提交 Builder 请求。

## URL 模式参数

仅当用户选择 `url` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.google.com/maps/place/Pizza+Inn+Magdeburg/data=!4m7!3m6!1s0x47a5f50c083530a3:0xfdba8746b538141!8m2!3d52.1263086!4d11.6094743!16s%2Fg%2F11kqmtk3dt!19sChIJozA1CAz1pUcRQYFTa3So2w8?authuser=0&hl=en&rclk=1` | `spider_parameters` | Google Maps URL。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

询问用户是否需要修改任何值，以及是否需要多组 URL。

提交 `spider_id=google_map-details_by-url` 和 `spider_parameters`，格式如下：

```json
[{"url":"https://www.google.com/maps/place/Pizza+Inn+Magdeburg/data=!4m7!3m6!1s0x47a5f50c083530a3:0xfdba8746b538141!8m2!3d52.1263086!4d11.6094743!16s%2Fg%2F11kqmtk3dt!19sChIJozA1CAz1pUcRQYFTa3So2w8?authuser=0&hl=en&rclk=1"}]
```

## CID 模式参数

仅当用户选择 `cid` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `CID` | 是 | `2476046430038551731` | `spider_parameters` | Google Maps CID。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

询问用户是否需要修改任何值，以及是否需要多组 CID。

提交 `spider_id=google_map-details_by-cid` 和 `spider_parameters`，格式如下：

```json
[{"CID":"2476046430038551731"}]
```

## 位置模式参数

仅当用户选择 `location` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `keyword` | 是 | `pizza` | `spider_parameters` | Google Maps 搜索关键词。 |
| `country` | 是 | `us` | `spider_parameters` | Google 国家。使用 `references/google_countries.md` 展示选项。 |
| `lat` | 否 | `38` | `spider_parameters` | 纬度。必须为数值。 |
| `long` | 否 | `77` | `spider_parameters` | 经度。必须为数值。 |
| `zoom_level` | 否 | `20` | `spider_parameters` | 缩放级别。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后展示 `references/google_countries.md` 中的完整 `country` 下拉表格。

询问用户是否需要修改任何值，以及是否需要多组位置。

提交 `spider_id=google_map-details_by-location` 和 `spider_parameters`，格式如下：

```json
[{"keyword":"pizza","country":"us","lat":"38","long":"77","zoom_level":"20"}]
```

## Place ID 模式参数

仅当用户选择 `placeid` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `place_id` | 是 | `ChIJ3S-JXmauEmsRUcIaWtf4MzE` | `spider_parameters` | Google Maps place ID。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

询问用户是否需要修改任何值，以及是否需要多组 place ID。

提交 `spider_id=google_map-details_by-placeid` 和 `spider_parameters`，格式如下：

```json
[{"place_id":"ChIJ3S-JXmauEmsRUcIaWtf4MzE"}]
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
  - `spider_name=google.com`
  - `spider_errors=true`
- 模式特定字段：
  - URL 模式：`spider_id=google_map-details_by-url`
  - CID 模式：`spider_id=google_map-details_by-cid`
  - 位置模式：`spider_id=google_map-details_by-location`
  - Place ID 模式：`spider_id=google_map-details_by-placeid`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须为 JSON 字符串数组。

## 脚本

为确保稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_google_map_details.py`，而非重写 Builder 流程。

```powershell
python3 ".\scripts\submit_dataify_google_map_details.py" --mode location --keyword "pizza" --country "us" --lat "38" --long "77" --zoom-level "20"
```

脚本支持 `--params-json` 用于多组提交，并打印包含 `mode`、`spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否将其保存为 `DATAIFY_API_TOKEN`，或告知用户可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。如果用户已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`Unsupported mode` 表示模式必须为 `url`、`cid`、`location` 或 `placeid`。

`url must start with https://www.google.com/maps/` 表示 URL 不在允许的 Google Maps URL 模式范围内。

`country must be one of the allowed Google country values` 表示国家下拉值无效。

`zoom_level must be an integer greater than or equal to 0` 表示缩放值无效。

`lat must be numeric` 或 `long must be numeric` 表示坐标无效。

`File name cannot be empty` 表示未提供可用的 `file_name`。

## 安全规则

- 不要在同一个 Builder 请求中混合 URL、CID、位置和 Place ID 模式的参数。
- 在模式明确之前不要提交 Builder 请求。
- 不要将 `file_name` 放入 `spider_parameters` 中。
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
