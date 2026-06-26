---
name: dataify-amazon-product-list
description: "用于 Dataify Amazon 商品列表采集 Builder 任务。当用户说到或请求 Amazon 产品列表采集工具、Amazon product list collection/tool/scraping，或按 keyword and domain 采集 Amazon product list 时触发。支持创建 amazon_product-list_by-keywords-domain 任务、返回 task_id、配置或复用 DATAIFY_API_TOKEN，并排查 Dataify Builder 请求失败。"
---

# Dataify Amazon Product List

通过 Dataify Builder 按关键词和域名提交 Amazon 产品列表采集任务，提交后停止。成功提交后，将 `task_id` 提供给用户，并告知他们前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

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

1. 提交前，向用户展示参数清单中列出的必填值、可选值和默认值。
2. 始终以 Markdown 表格展示已提交的参数；不要使用纯文本句子或项目符号列表进行参数确认。
3. 询问："在我提交任务之前，您是否需要修改这些值？"
4. 将最终值规范化为 `keyword`、`domain`、`page_turning` 和 `file_name`。
5. 从用户明确提供的输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
6. 如果没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
7. 验证必填字段和数值约束。
8. 提交 Builder 请求创建任务。
9. 从 Builder 响应中读取 `data.task_id`。
10. 告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 参数清单

| 字段 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `keyword` | 是 | `https://www.amazon.com/sp?ie=UTF8&seller=ADZ7LD48GVFQJ&asin=B07H56J7K1&ref_=dp_merchant_link&isAmazonFulfilled=1` | Amazon 产品列表关键词查询。 |
| `domain` | 是 | `https://www.amazon.com/` | Amazon 域名。 |
| `page_turning` | 否 | `1` | 采集的页数。必须是大于等于 `0` 的整数。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段。可由用户修改。 |

如果用户已经提供了部分值，在表格中显示这些值代替默认值，只询问是否需要修改剩余/使用默认值的参数。

## Dataify Builder 请求

使用表单字段而不是手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder`
- 方法：`POST`
- Authorization 头：`Bearer DATAIFY_API_TOKEN`
- Content type：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=amazon.com`
  - `spider_id=amazon_product-list_by-keywords-domain`
  - `spider_errors=true`
- 动态字段：
  - `spider_parameters` 必须是 JSON 字符串，不能是原始对象。
  - `file_name` 默认为 `{{TasksID}}`，可由用户修改。

## 脚本

为确保稳定执行，建议使用 Python 3.6 或更新版本运行 `scripts/submit_amazon_product_list.py`，而不是重写 Builder 流程。脚本使用 UTF-8 编码进行读写。

```powershell
python3 ".\scripts\submit_amazon_product_list.py"
python3 ".\scripts\submit_amazon_product_list.py" --keyword "coffee" --domain "https://www.amazon.com/" --page-turning 1 --file-name "amazon-product-list"
```

脚本会输出包含 `task_id`、`keyword`、`domain`、`page_turning`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示没有传入明确的 token 且本地未保存 `DATAIFY_API_TOKEN`。提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。

`Keyword cannot be empty` 表示没有提供有效的关键词查询。

`Domain cannot be empty` 表示没有提供有效的域名。

`Page turning must be greater than or equal to 0` 表示页数数值无效。

`File name cannot be empty` 表示没有提供有效的 `file_name`。

缺少 `task_id` 通常表示 authorization 头、token、`spider_name` 或 `spider_id` 有误。

## 注意事项

- 不要编造结果字段。
- 成功创建任务后，始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
