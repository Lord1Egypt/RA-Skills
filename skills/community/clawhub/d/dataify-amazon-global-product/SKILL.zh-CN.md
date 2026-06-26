---
name: dataify-amazon-global-product
description: "用于 Dataify Amazon 全球商品采集 Builder 任务。当用户请求 Amazon 全球产品详情采集工具、Amazon global product collection/details/scraping/harvesting/crawling，尤其包含 product URL、category URL、keyword、keyword brand、brand 或类似 Amazon global product 任务关键词时触发。支持按 product URL、category URL、keyword、keyword and brand 创建 Amazon global product 任务，返回 task_id，配置或复用 DATAIFY_API_TOKEN，并排查 Dataify Builder 请求失败。"
---

# Dataify Amazon Global Product

通过 Dataify Builder 提交 Amazon 全球产品采集任务，提交后停止。成功提交后，将 `task_id` 提供给用户，并告知他们前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

本技能涵盖四种 Amazon 全球产品采集模式：

| 模式 | 用途 | Builder `spider_id` |
| --- | --- | --- |
| `product-url` | 通过产品 URL 采集全球 Amazon 产品详情。 | `amazon_global-product_by-url` |
| `category-url` | 通过分类 URL 采集全球 Amazon 产品详情。 | `amazon_global-product_by-category-url` |
| `keyword` | 通过关键词搜索采集全球 Amazon 产品详情。 | `amazon_global-product_by-keywords` |
| `keyword-brand` | 通过关键词和品牌筛选采集全球 Amazon 产品详情。 | `amazon_global-product_by-keywords-brand` |

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则在本次运行中使用该 token。
- 如果未提供 token，先检查环境变量中是否已保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用。
- 如果本地没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
- 没有 token 不要调用 Builder 接口。
- 在面向用户的说明中始终称其为 `API TOKEN`。在本地保存使用时，优先使用环境变量名 `DATAIFY_API_TOKEN`。

PowerShell 示例，为当前会话保存 token：

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_DATAIFY_API_TOKEN"
```

在 Windows 上设置持久的用户级变量：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_DATAIFY_API_TOKEN", "User")
```

## 核心工作流程

1. 从用户请求中识别采集模式：`product-url`、`category-url`、`keyword` 或 `keyword-brand`。
2. 提交前，向用户展示该模式的必填值、可选值和默认值。
3. 始终以 Markdown 表格展示已提交的参数；不要使用纯文本句子或项目符号列表进行参数确认。
4. 询问："在我提交任务之前，您是否需要修改这些值？"
5. 规范化并验证所选模式的最终值。
6. 从用户明确提供的输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
7. 如果没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
8. 提交 Builder 请求创建任务。
9. 从 Builder 响应中读取 `data.task_id`。
10. Builder 成功后停止。
11. 告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

如果用户已经提供了部分值，在表格中显示这些值代替默认值，只询问是否需要修改剩余/使用默认值的参数。

## 参数清单

### Product URL

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `url` | 是 | `https://www.amazon.com/dp/B0CHHSFMRL/` | Amazon 产品 URL。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。可由用户修改。 |

将 `spider_parameters` 作为包含一个对象的数组提交，例如 `[{"url":"https://www.amazon.com/dp/B0CHHSFMRL/"}]`。

### Category URL

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `url` | 是 | `https://www.amazon.com/s?i=luggage-intl-ship` | Amazon 分类 URL。 |
| `maximum` | 是 | `5` | 大于等于 `0` 的整数。 |
| `sort_by` | 否 | `Best Sellers` | 下拉选项。 |
| `get_sponsored` | 否 | `true` | 下拉选项：`true` 或 `false`。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。可由用户修改。 |

在让用户选择之前，以 Markdown 表格展示所有 `sort_by` 选项，包含 `Label` 和 `Value` 两列。

| Label | Value |
| --- | --- |
| `Best Sellers` | `Best Sellers` |
| `Newest Arrivals` | `Newest Arrivals` |
| `Avg. Customer Review` | `Avg. Customer Review` |
| `Price: High to Low` | `Price: High to Low` |
| `Price: Low to High` | `Price: Low to High` |
| `Featured` | `Featured` |

在让用户选择之前，以 Markdown 表格展示所有 `get_sponsored` 选项，包含 `Label` 和 `Value` 两列。

| Label | Value |
| --- | --- |
| `Include Sponsored Products` | `true` |
| `Exclude Sponsored Products` | `false` |

接受的 `sort_by` 显示值和提交值：

- best sellers 或 `Best Sellers` -> `Best Sellers`
- newest arrivals 或 `Newest Arrivals` -> `Newest Arrivals`
- average customer review 或 `Avg. Customer Review` -> `Avg. Customer Review`
- price high to low 或 `Price: High to Low` -> `Price: High to Low`
- price low to high 或 `Price: Low to High` -> `Price: Low to High`
- featured recommendations 或 `Featured` -> `Featured`

### Keyword

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `keyword` | 是 | `coffee` | Amazon 搜索关键词。 |
| `domain` | 是 | `https://www.amazon.com` | Amazon 域名。 |
| `lowest_price` | 否 | `20` | 大于等于 `0` 的整数。 |
| `highest_price` | 否 | `50` | 大于等于 `0` 的整数，且不得小于 `lowest_price`。 |
| `page_turning` | 否 | `2` | 大于等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。可由用户修改。 |

要求 `highest_price >= lowest_price`。

### Keyword Brand

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `keyword` | 是 | `shirts` | Amazon 搜索关键词。 |
| `brands` | 是 | `Adidas` | 品牌筛选。 |
| `page_turning` | 是 | `2` | 大于等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。可由用户修改。 |

## Dataify Builder 请求

使用表单字段而不是手动构建的 URL 编码字符串。

- 方法：`POST`
- Authorization 头：`Bearer DATAIFY_API_TOKEN`
- Content type：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=amazon.com`
  - `spider_errors=true`
- 动态字段：
  - Builder URL 取决于所选模式。
  - `spider_id` 必须与所选模式匹配。
  - `spider_parameters` 必须是 JSON 字符串，不能是原始对象。
  - `file_name` 默认为 `{{TasksID}}`，可由用户修改。
- 将 `file_name` 作为 Builder 表单字段发送，而不是作为下载输出名称。

各模式的 Builder URL：

| 模式 | URL |
| --- | --- |
| `product-url` | `https://scraperapi.dataify.com/builder` |
| `category-url` | `https://scraperapi.dataify.com/builder?platform=1` |
| `keyword` | `https://scraperapi.dataify.com/builder?platform=1` |
| `keyword-brand` | `https://scraperapi.dataify.com/builder?platform=1` |

## 脚本

为确保稳定执行，建议使用 Python 3.6 或更新版本运行 `scripts/submit_amazon_global_product.py`，而不是重写 Builder 流程。脚本使用 UTF-8 编码进行读写。

```powershell
python3 ".\scripts\submit_amazon_global_product.py" product-url
python3 ".\scripts\submit_amazon_global_product.py" category-url --url "https://www.amazon.com/s?i=luggage-intl-ship" --maximum 5 --sort-by "Best Sellers" --get-sponsored true
python3 ".\scripts\submit_amazon_global_product.py" keyword --keyword "coffee" --domain "https://www.amazon.com"
python3 ".\scripts\submit_amazon_global_product.py" keyword-brand --keyword "shirts" --brands "Adidas" --page-turning 2
```

如果 `python3` 不可用，请使用该机器上的本地 Python 3 命令，例如 `python`。脚本会检查运行时版本，如果当前解释器版本过低，会提示用户使用 Python 3.6 或更新版本。

要在单次运行中覆盖已保存的环境 token 或默认文件名：

```powershell
python3 ".\scripts\submit_amazon_global_product.py" keyword --api-token "YOUR_DATAIFY_API_TOKEN" --keyword "coffee" --file-name "amazon-global-coffee"
```

脚本会输出包含 `task_id`、已提交参数、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示没有传入明确的 token 且本地未保存 `DATAIFY_API_TOKEN`。提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。

`URL cannot be empty` 表示没有提供有效的 URL。

`Keyword cannot be empty` 表示没有提供有效的关键词。

`Brands cannot be empty` 表示没有提供有效的品牌值。

`Domain cannot be empty` 表示没有提供有效的域名。

`Maximum must be greater than or equal to 0` 表示请求的最大数量无效。

`Page turning must be greater than or equal to 0` 表示请求的页数无效。

`Lowest price must be greater than or equal to 0` 表示请求的最低价格无效。

`Highest price must be greater than or equal to 0` 表示请求的最高价格无效。

`Highest price cannot be less than lowest price` 表示价格范围需要在提交前修正。

`Unsupported sort_by` 表示分类排序选项必须是接受的显示值或提交值之一。

`get_sponsored must be true or false` 表示赞助选项需要在提交前修正。

`File name cannot be empty` 表示没有提供有效的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段形式提交、`spider_parameters` 不是 JSON 字符串，或者对象缺少该模式所需的参数。

缺少 `task_id` 通常表示 authorization 头、token、`spider_name` 或 `spider_id` 有误。

## 注意事项

- 不要编造结果字段。
- 成功创建任务后，始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
