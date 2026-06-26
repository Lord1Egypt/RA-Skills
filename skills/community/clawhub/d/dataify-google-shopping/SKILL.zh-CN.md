---
name: dataify-google-shopping
description: "当用户请求“调用 Google Shopping”或“购物搜索/商品搜索/价格比较”，或明确提到购物搜索字段时，触发 dataify-google-shopping skill。"
---

# Dataify Google Shopping

使用此 skill 将用户的 Google Shopping 请求转化为 Dataify Scraper API 调用。

## 调用前确认（必须）

每次真正调用 API 之前，必须遵循以下确认流程。这些规则优先于本 skill 中任何旧的工作流程顺序。

1. 将用户请求解析为 API body 字段和固定的 `engine` 值。
2. 仅在参数描述明确标注默认值时才使用默认值。不要将示例 YAML 值、示例提示词、占位符值或示例（如 `pizza`、`us`、`en`、日期、机场代码或 token）作为默认值。
3. 如果必填参数没有文档化的默认值且无法从用户请求中推断，先询问该参数再构建表格。
4. 调用 API 前展示 Markdown 表格。不要包含 `Authorization`。包含本 skill 参考文档中的完整 body 字段列表（包含 `engine`），即使某个字段当前为空也要列出。
5. 表格必须恰好包含以下列：`参数名`、`当前值`、`默认值`、`说明`。
6. 展示表格后询问用户是否需要修改参数。用户明确确认后才能调用 API。
7. 如果用户修改了参数，重新生成表格并再次确认。
8. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。

尽可能使用内置的预览辅助工具从本 skill 的参考文档生成确认表格：

```bash
python3 scripts/preview_params.py --params-json '{"q":"USER_QUERY"}'
```

将每个已解析的当前值通过 `--params-json` 或对应的 `--field value` 参数传递给 `preview_params.py`。辅助工具从 `references/*api.md` 读取默认值和描述；如果辅助工具无法解析某个默认值，保留默认值为空，而不是编造一个。
9. 确认并处理 token 后，使用 `python3` 调用内置 Python 脚本，并将 API 响应体直接返回，不进行总结、提取、清理、翻译或重新格式化。

## 工作流程

1. 将用户请求解析为 Dataify Google Shopping 字段。使用 `q` 作为购物搜索查询，并始终将 `engine` 设为 `google_shopping`。
2. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
3. 仅使用用户请求的字段加上必要的文档化默认值构建请求参数。除非用户要求其他值，否则使用 `json: "1"` 和 `google_domain: "google.com"`。不要将 API 文档中的示例值当作默认值。
4. 每次调用 API 前，向用户展示包含完整字段列表的 Markdown 表格，恰好包含以下列：`参数名`、`当前值`、`默认值`、`说明`。将 token 状态标记为 `已提供` 或 `未提供`；不要显示 token。询问用户是否需要修改参数，用户确认前不要调用 API。
5. 如果用户修改了任何参数，更新值并在调用前再次展示完整表格。
6. 确认后，使用 `python3` 运行内置 Python 脚本。脚本会以表单数据形式提交到硬编码的端点 `https://scraperapi.dataify.com/request`。
7. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 脚本使用

从此 skill 目录运行命令，或使用 `scripts/google_shopping.py` 的绝对路径。

预览完整的参数表格：

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true --table
```

用户确认后调用 API：

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true
```

对于自然语言解析，传递用户的请求：

```bash
python3 scripts/google_shopping.py --request "搜索美国 Google Shopping 上 100 美元以下包邮的无线耳机，英文，返回 JSON" --table
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_shopping.py --params-json '{"q":"wireless headphones","gl":"us","hl":"en","max_price":"100","free_shipping":"true"}' --table
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_shopping.py --token "USER_TOKEN" --q "wireless headphones" --gl us --hl en
```

仅在内部验证时使用 `--dry-run`。它打印规范化的负载 JSON 而不调用 API。

## 字段映射

需要完整的字段列表、默认值或预览表格的确切描述时，请查阅 `references/google_shopping_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_shopping`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 省略用户未请求的可选字段，除非 API 文档给出了真正的默认值。
- 仅在必填的购物查询 `q` 无法推断时才提出后续问题。
- 如果 `location` 和 `uule` 同时存在，优先使用明确的 `uule` 并省略 `location`。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 用于 Google 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- 页码 N -> `start: String((N - 1) * 10)`
- 原始 Google Shopping 过滤器 token -> `shoprs`
- 最低价格 -> `min_price`
- 最高价格 -> `max_price`
- 价格从低到高 -> `sort_by: "1"`
- 价格从高到低 -> `sort_by: "2"`
- 仅包邮 -> `free_shipping: "true"`
- 仅折扣/促销商品 -> `on_sale: "true"`
- 仅小型商家商品 -> `small_business: "true"`
- 跳过缓存 -> `no_cache: "true"`
