---
name: dataify-walmart-products
description: "提交 Dataify Walmart Product Information Builder 任务，支持四种 Walmart 商品采集模式。当用户需要 Walmart product information collection tool、采集/抓取/爬取 Walmart 商品信息或商品数据，按 URL、category URL、SKU、keyword 采集 Walmart products，创建 walmart_product_by-url、walmart_product_by-category-url、walmart_product_by-sku 或 walmart_product_by-keywords 任务，或表达 Walmart 产品信息采集/抓取、产品采集/抓取、产品 URL/类别 URL/SKU/关键词采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify Walmart Products

通过 Dataify Builder 提交 Walmart 产品信息采集任务。本技能是四种采集模式的引导封装：

| 模式 | 采集器 ID | 用途 |
| --- | --- | --- |
| 产品 URL | `walmart_product_by-url` | 通过产品 URL 采集一个或多个 Walmart 产品。 |
| 类别 URL | `walmart_product_by-category-url` | 通过类别 URL 采集 Walmart 产品。 |
| SKU | `walmart_product_by-sku` | 通过 SKU 采集一个或多个 Walmart 产品。 |
| 关键词 | `walmart_product_by-keywords` | 通过搜索关键词和域名采集 Walmart 产品。 |

提交成功后，向用户提供 `task_id`、返回的或推断的状态，并告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则在本次运行中使用该 token。
- 如果未提供 token，先检查环境中是否已在本地保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用，无需要求用户重新输入。
- 如果本地没有可用的 token，告诉用户：`Dataify 需要 API Token。新账号注册即得 50 免费积分，约可获得 6000 条试用结果，7 天有效，仅成功请求计费。注册完成后告诉我，我会继续当前任务。`。
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

1. 首先询问用户选择采集模式：`url`、`category-url`、`sku` 或 `keywords`。
2. 用户选择模式后，仅展示该模式的参数表格和默认值。
3. 如果所选模式有下拉字段，以包含 `Label` 和 `Value` 列的 Markdown 表格展示下拉选项。
4. 询问用户是否需要在运行任务前修改任何值。
5. 询问用户是否需要为所选模式采集多组 Walmart 产品。
6. 将最终值规范化为仅包含所选模式的参数对象列表。
7. 从显式输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
9. 验证所选模式、URL、域名、SKU、关键词、数值、下拉值和文件名。
10. 使用所选模式的 `spider_id` 提交 Builder 请求。
11. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
13. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 模式选择

当用户调用此技能时，首先展示以下 Markdown 表格并要求选择一种模式：

| 标签 | 值 |
| --- | --- |
| 通过产品 URL 采集 Walmart 产品 | `url` |
| 通过类别 URL 采集 Walmart 产品 | `category-url` |
| 通过 SKU 采集 Walmart 产品 | `sku` |
| 通过关键词采集 Walmart 产品 | `keywords` |

询问："您想使用哪种采集模式：`url`、`category-url`、`sku` 还是 `keywords`？"

在模式明确之前不要提交 Builder 请求。

## 共享下拉选项

`all_variations` 下拉选项：

| 标签 | 值 |
| --- | --- |
| true | `true` |
| false | `false` |

## 产品 URL 模式参数

仅当用户选择 `url` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true` | `spider_parameters` | Walmart 产品 URL。 |
| `all_variations` | 否 | `false` | `spider_parameters` | 是否采集所有产品变体。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后展示共享下拉选项中的 `all_variations` 下拉表格。


同时询问："您是否需要采集多组 Walmart 产品 URL？如果是，请提供多组 `url` 和 `all_variations`。"

产品 URL 模式处理：

- `url` 为必填项。如果用户未提供，询问该必填值；不要使用文档示例值代替用户输入。
- `url` 必须以 `https://www.walmart.com/` 开头。
- `all_variations` 必须为 `true` 或 `false`。
- 提交 `spider_id=walmart_product_by-url`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"url":"https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true","all_variations":"true"}]
```

## 类别 URL 模式参数

仅当用户选择 `category-url` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `category_url` | 是 | `https://www.walmart.com/shop/deals/food/` | `spider_parameters` | Walmart 类别 URL。 |
| `all_variations` | 是 | `false` | `spider_parameters` | 是否采集所有产品变体。 |
| `page_turning` | 是 | `1` | `spider_parameters` | 页数限制。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后展示共享下拉选项中的 `all_variations` 下拉表格。


同时询问："您是否需要采集多组 Walmart 类别 URL？如果是，请提供多组 `category_url`、`all_variations` 和 `page_turning`。"

类别 URL 模式处理：

- `category_url` 为必填项。如果用户未提供，询问该必填值；不要使用文档示例值代替用户输入。
- `category_url` 必须以 `https://www.walmart.com/` 开头。
- `all_variations` 必须为 `true` 或 `false`。
- `page_turning` 必须为大于或等于 `0` 的整数。
- 提交 `spider_id=walmart_product_by-category-url`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"category_url":"https://www.walmart.com/shop/deals/food/","all_variations":"false","page_turning":"1"}]
```

## SKU 模式参数

仅当用户选择 `sku` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `sku` | 是 | `439179861` | `spider_parameters` | Walmart SKU 产品代码。 |
| `all_variations` | 否 | `false` | `spider_parameters` | 是否采集所有产品变体。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后展示共享下拉选项中的 `all_variations` 下拉表格。


同时询问："您是否需要采集多组 Walmart SKU？如果是，请提供多组 `sku` 和 `all_variations`。"

SKU 模式处理：

- `sku` 为必填项。如果用户未提供，询问该必填值；不要使用文档示例值代替用户输入。
- 去除 `sku` 的前后空白字符。
- `sku` 不能为空。
- `all_variations` 必须为 `true` 或 `false`。
- 提交 `spider_id=walmart_product_by-sku`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"sku":"439179861","all_variations":"false"}]
```

## 关键词模式参数

仅当用户选择 `keywords` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `keyword` | 是 | `leggins` | `spider_parameters` | Walmart 搜索关键词。 |
| `domain` | 是 | `https://www.walmart.com/` | `spider_parameters` | Walmart 主域名。 |
| `all_variations` | 否 | `false` | `spider_parameters` | 是否采集所有产品变体。 |
| `page_turning` | 否 | `2` | `spider_parameters` | 页数限制。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后展示共享下拉选项中的 `all_variations` 下拉表格。


同时询问："您是否需要采集多组 Walmart 关键词？如果是，请提供多组 `keyword`、`domain`、`all_variations` 和 `page_turning`。"

关键词模式处理：

- `keyword` 为必填项。如果用户未提供，询问该必填值；不要使用文档示例值代替用户输入。
- `keyword` 不能为空。
- `domain` 必须以 `https://www.walmart.com/` 开头。
- `all_variations` 必须为 `true` 或 `false`。
- `page_turning` 必须为大于或等于 `0` 的整数。
- 提交 `spider_id=walmart_product_by-keywords`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"keyword":"leggins","domain":"https://www.walmart.com/","all_variations":"false","page_turning":"2"}]
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
  - `spider_name=walmart.com`
  - `spider_errors=true`
- 模式特定字段：
  - 产品 URL 模式：`spider_id=walmart_product_by-url`
  - 类别 URL 模式：`spider_id=walmart_product_by-category-url`
  - SKU 模式：`spider_id=walmart_product_by-sku`
  - 关键词模式：`spider_id=walmart_product_by-keywords`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须为 JSON 字符串数组。

## 脚本

为确保稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_walmart_products.py`，而非重写 Builder 流程。

产品 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode url --url "https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true" --all-variations "true"
```

类别 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode category-url --category-url "https://www.walmart.com/shop/deals/food/" --all-variations "false" --page-turning "1"
```

SKU 模式：

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode sku --sku "439179861" --all-variations "false"
```

关键词模式：

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode keywords --keyword "leggins" --domain "https://www.walmart.com/" --all-variations "false" --page-turning "2"
```

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode sku --sku "439179861" --file-name "{{TasksID}}"
```

提交多组产品 URL：

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode url --params-json '[{"url":"https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true","all_variations":"true"},{"url":"https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true","all_variations":"true"}]'
```

脚本会打印包含 `mode`、`spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告诉用户：`Dataify 需要 API Token。新账号注册即得 50 免费积分，约可获得 6000 条试用结果，7 天有效，仅成功请求计费。注册完成后告诉我，我会继续当前任务。`，询问是否将其保存为 `DATAIFY_API_TOKEN`，或告知用户可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。如果用户已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`Unsupported mode` 表示模式必须为 `url`、`category-url`、`sku` 或 `keywords`。

`url must start with https://www.walmart.com/` 表示产品 URL 不在允许的 Walmart 域名范围内。

`category_url must start with https://www.walmart.com/` 表示类别 URL 不在允许的 Walmart 域名范围内。

`domain must start with https://www.walmart.com/` 表示主域名不在允许的 Walmart 域名范围内。

`all_variations must be true or false` 表示变体选项无效。

`page_turning must be an integer greater than or equal to 0` 表示页数限制无效。

`sku cannot be empty` 表示缺少 SKU。

`keyword cannot be empty` 表示缺少关键词。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组，或所选模式的对象缺少必填字段。

缺少 `task_id` 通常表示 authorization 请求头、token、`spider_name`、所选 `spider_id` 或 `spider_parameters` 有误。

## 安全规则

- 不要在同一个 Builder 请求中混合产品 URL、类别 URL、SKU 和关键词模式的参数。
- 在模式明确之前不要提交 Builder 请求。
- 不要将 `file_name` 放入 `spider_parameters` 中。
- 不要使用 `https://www.walmart.com/` 以外的 Walmart URL 或域名。
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
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
