---
name: dataify-ebay-products
description: "提交 Dataify eBay Product Information Builder 任务，支持四种 eBay 商品采集模式。当用户需要 eBay product information collection tool、采集/抓取/爬取 eBay 商品信息，按 URL、category URL、keyword、store URL 采集 eBay 商品，创建 ebay_ebay_by-url、ebay_ebay_by-category-url、ebay_ebay_by-keywords 或 ebay_ebay_by-listurl 任务，或表达 eBay 产品信息采集/抓取、产品 URL/类别 URL/关键词/店铺网址采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify eBay Products

通过 Dataify Builder 提交 eBay 产品信息采集任务。本技能是四种采集模式的引导封装：

| 模式 | 采集器 ID | 用途 |
| --- | --- | --- |
| 产品 URL | `ebay_ebay_by-url` | 通过产品 URL 采集一个或多个 eBay 产品。 |
| 类别 URL | `ebay_ebay_by-category-url` | 通过类别 URL 采集 eBay 产品。 |
| 关键词 | `ebay_ebay_by-keywords` | 通过搜索关键词采集 eBay 产品。 |
| 店铺 URL | `ebay_ebay_by-listurl` | 通过店铺 URL 采集 eBay 产品。 |

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

1. 首先询问用户选择采集模式：`url`、`category-url`、`keywords` 或 `listurl`。
2. 用户选择模式后，仅展示该模式的参数表格和默认值。
3. 询问用户是否需要在运行任务前修改任何值。
4. 询问用户是否需要为所选模式采集多组 eBay 产品。
5. 将最终值规范化为仅包含所选模式的参数对象列表。
6. 从显式输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
7. 如果没有可用的 token，要求用户输入 API TOKEN 并询问是否将其保存为 `DATAIFY_API_TOKEN`。
8. 验证所选模式、URL、关键词、数值和文件名。
9. 使用所选模式的 `spider_id` 提交 Builder 请求。
10. 从 Builder 响应中读取 `data.task_id`，并在存在时读取 `data.status` 或 `status`。
11. Builder 成功后停止。
12. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 模式选择

当用户调用此技能时，首先展示以下 Markdown 表格并要求选择一种模式：

| 标签 | 值 |
| --- | --- |
| 通过产品 URL 采集 eBay 产品 | `url` |
| 通过类别 URL 采集 eBay 产品 | `category-url` |
| 通过关键词采集 eBay 产品 | `keywords` |
| 通过店铺 URL 采集 eBay 产品 | `listurl` |

询问："您想使用哪种采集模式：`url`、`category-url`、`keywords` 还是 `listurl`？"

在模式明确之前不要提交 Builder 请求。

## 产品 URL 模式参数

仅当用户选择 `url` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm` | `spider_parameters` | eBay 产品 URL。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后询问："您是否需要在提交任务前修改这些值？"

同时询问："您是否需要采集多组 eBay 产品 URL？如果是，请提供多个 `url` 值。"

产品 URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值。
- `url` 必须以 `https://www.ebay.com/` 开头。
- 提交 `spider_id=ebay_ebay_by-url`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"url":"https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"}]
```

## 类别 URL 模式参数

仅当用户选择 `category-url` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829` | `spider_parameters` | eBay 类别 URL。 |
| `Count` | 否 | `60` | `spider_parameters` | 此采集器要求的 Count 字段。必须为大于或等于 `0` 的整数。 |
| `count` | 否 | `60` | `spider_parameters` | 数量字段。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后询问："您是否需要在提交任务前修改这些值？"

同时询问："您是否需要采集多组 eBay 类别 URL？如果是，请提供多组 `url`、`Count` 和 `count`。"

类别 URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829`。
- `url` 必须以 `https://www.ebay.com/` 开头。
- `Count` 必须为大于或等于 `0` 的整数。
- `count` 必须为大于或等于 `0` 的整数。
- 必须将 `Count` 和 `count` 作为独立字段分别提交。
- 提交 `spider_id=ebay_ebay_by-category-url`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"url":"https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829","Count":"60","count":"60"}]
```

## 关键词模式参数

仅当用户选择 `keywords` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `keywords` | 是 | `baby toys` | `spider_parameters` | eBay 搜索关键词。 |
| `count` | 否 | `60` | `spider_parameters` | 数量字段。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后询问："您是否需要在提交任务前修改这些值？"

同时询问："您是否需要采集多组 eBay 关键词？如果是，请提供多组 `keywords` 和 `count`。"

关键词模式处理：

- `keywords` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `baby toys`。
- `keywords` 不能为空。
- `count` 必须为大于或等于 `0` 的整数。
- 提交 `spider_id=ebay_ebay_by-keywords`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"keywords":"baby toys","count":"60"}]
```

## 店铺 URL 模式参数

仅当用户选择 `listurl` 时使用本节。

| 字段 | 必填 | 默认值 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `url` | 是 | `https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086` | `spider_parameters` | eBay 店铺 URL。 |
| `count` | 否 | `60` | `spider_parameters` | 数量字段。必须为大于或等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未更改时使用默认值。 |

然后询问："您是否需要在提交任务前修改这些值？"

同时询问："您是否需要采集多组 eBay 店铺 URL？如果是，请提供多组 `url` 和 `count`。"

店铺 URL 模式处理：

- `url` 为必填项。如果用户未提供，仅在参数确认表格中展示后才使用默认值 `https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086`。
- `url` 必须以 `https://www.ebay.com/` 开头。
- `count` 必须为大于或等于 `0` 的整数。
- 提交 `spider_id=ebay_ebay_by-listurl`。
- 将 `spider_parameters` 作为包含一个或多个对象的 JSON 字符串提交，格式如下：

```json
[{"url":"https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086","count":"60"}]
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
  - `spider_name=ebay.com`
  - `spider_errors=true`
- 模式特定字段：
  - 产品 URL 模式：`spider_id=ebay_ebay_by-url`
  - 类别 URL 模式：`spider_id=ebay_ebay_by-category-url`
  - 关键词模式：`spider_id=ebay_ebay_by-keywords`
  - 店铺 URL 模式：`spider_id=ebay_ebay_by-listurl`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须为 JSON 字符串数组。

## 脚本

为确保稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_ebay_products.py`，而非重写 Builder 流程。

产品 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode url --url "https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"
```

类别 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode category-url --url "https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829" --count "60"
```

关键词模式：

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode keywords --keywords "baby toys" --count "60"
```

店铺 URL 模式：

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode listurl --url "https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086" --count "60"
```

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode keywords --keywords "baby toys" --file-name "{{TasksID}}"
```

提交多组产品 URL：

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode url --params-json '[{"url":"https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"},{"url":"https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"}]'
```

脚本会打印包含 `mode`、`spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否将其保存为 `DATAIFY_API_TOKEN`，或告知用户可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。如果用户已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`Unsupported mode` 表示模式必须为 `url`、`category-url`、`keywords` 或 `listurl`。

`url must start with https://www.ebay.com/` 表示 URL 不在允许的 eBay 域名范围内。

`keywords cannot be empty` 表示缺少关键词。

`Count must be an integer greater than or equal to 0` 表示类别 Count 字段无效。

`count must be an integer greater than or equal to 0` 表示数量字段无效。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组，或所选模式的对象缺少必填字段。

缺少 `task_id` 通常表示 authorization 请求头、token、`spider_name`、所选 `spider_id` 或 `spider_parameters` 有误。

## 安全规则

- 不要在同一个 Builder 请求中混合产品 URL、类别 URL、关键词和店铺 URL 模式的参数。
- 在模式明确之前不要提交 Builder 请求。
- 不要将 `file_name` 放入 `spider_parameters` 中。
- 不要使用 `https://www.ebay.com/` 以外的 eBay URL。
- 提及身份验证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要编造结果字段。
- 任务创建成功后始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
