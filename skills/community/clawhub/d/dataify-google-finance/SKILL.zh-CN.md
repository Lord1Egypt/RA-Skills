---
name: dataify-google-finance
description: "当用户请求“调用 Google Finance”或“搜索 Google Finance”，或明确提到金融数据相关内容（股票、指数、基金、货币、期货）时，触发 dataify-google-finance skill。"
---

# Dataify Google Finance

使用此 skill 将用户的 Google Finance 请求转化为 Dataify Scraper API 表单 POST。

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

1. 将用户请求解析为 Dataify Google Finance 字段。使用 `q` 作为金融查询，将 `engine` 设为固定值 `google_finance`。
2. 仅使用参数描述中的文档化默认值：
   - `engine`: 固定 `google_finance`
   - `json`: 默认 `1`
   - `window`: 默认 `1D`
   - `no_cache`: 默认 `false`
   - `q`: 无默认值；如果无法推断则询问用户
   - `hl`: 无文档化默认值；除非用户指定，否则留空
3. 每次调用 API 前，使用 `python3` 以预览模式运行内置脚本，并向用户展示返回的 Markdown 表格。表格必须包含完整的请求字段列表（除 `Authorization` 外），仅包含以下列：参数名、当前值、默认值、描述。

```bash
python3 scripts/google_finance.py --request "查询 NASDAQ:GOOGL，窗口 1年，英文，返回 JSON" --preview-table
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_finance.py --params-json '{"q":"NASDAQ:GOOGL","window":"1Y","hl":"en","json":"1"}' --preview-table
```

4. 询问用户是否需要修改参数。用户确认前不要调用 API。如果用户要求修改，更新字段并再次展示预览表格。
5. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_finance.py` 的绝对路径。

```bash
python3 scripts/google_finance.py --q "NASDAQ:GOOGL" --window 1Y --hl en --json 1
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_finance.py --token "USER_TOKEN" --q "NASDAQ:GOOGL" --window 1Y
```

对于自然语言的备选方式，传递完整请求：

```bash
python3 scripts/google_finance.py --request "搜索苹果股票，图表范围 5天，不使用缓存"
```

7. 将脚本输出直接返回给用户。不要对 API 响应体进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要完整的参数描述和文档化默认值时，请查阅 `references/google_finance_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_finance`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 仅在必填的金融查询 `q` 无法推断时才提出后续问题。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。
- 不要在调用前参数表格中显示 `Authorization`。
- 不要从示例中编造默认值。仅使用参数描述中明确声明的默认值。

常用映射：

- 股票、指数、共同基金、货币或期货搜索词 -> `q`
- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 界面/搜索语言 -> `hl`
- "1天"、"1 day" 或 "1D" -> `window: "1D"`
- "5天"、"5 days" 或 "5D" -> `window: "5D"`
- "1个月"、"1 month" 或 "1M" -> `window: "1M"`
- "6个月"、"6 months" 或 "6M" -> `window: "6M"`
- "年初至今" 或 "YTD" -> `window: "YTD"`
- "1年"、"1 year" 或 "1Y" -> `window: "1Y"`
- "5年"、"5 years" 或 "5Y" -> `window: "5Y"`
- "最大"、"max" 或 "MAX" -> `window: "MAX"`
- 跳过缓存 -> `no_cache: "true"`
