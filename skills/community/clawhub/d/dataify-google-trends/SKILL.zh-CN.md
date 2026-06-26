---
name: dataify-google-trends
description: "当用户请求“调用 Google Trends”或“趋势搜索/Google Trends”，或明确提到趋势搜索字段时，触发 dataify-google-trends skill。"
---

# Dataify Google Trends

使用此 skill 将用户的 Google Trends 请求转化为 Dataify Scraper API 表单提交。

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
9. 确认并处理 token 后，使用 `python3` 调用内置 Python 脚本，并将 API 响应体直接返回，不进行总结、提取、清理、翻译或重新格式化。

尽可能使用内置的预览辅助工具从本 skill 的参考文档生成确认表格：

```bash
python3 scripts/preview_params.py --q "USER_QUERY"
```

将每个已解析的当前值通过对应的 `--field value` 参数传递给 `preview_params.py`。辅助工具从 `references/*api.md` 读取默认值和描述；如果辅助工具无法解析某个默认值，保留默认值为空，而不是编造一个。

## 工作流程

1. 将用户请求解析为 Google Trends 字段。使用 `q` 作为查询，将 `engine` 设为 `google_trends`。
2. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
3. 根据用户的请求加上必要的 API 默认值构建请求参数。不要将示例值当作默认值。特别是不要将 `q` 默认为 `pizza`；如果无法推断查询内容，请向用户询问。
4. 每次调用 API 前，展示包含完整字段列表的 Markdown 表格，仅包含以下列：`参数名`、`当前值`、`默认值`、`说明`。不要在参数表格中包含 `Authorization`。
5. 询问用户是否需要修改参数。用户确认前不要调用 API。
6. 确认后，使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_trends.py` 的绝对路径。

```bash
python3 scripts/google_trends.py --q "AI" --json 1
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_trends.py --token "USER_TOKEN" --q "AI" --geo "United+States" --hl en --data_type TIMESERIES --no_cache true
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号。脚本仍然以表单数据形式提交给 API：

```bash
python3 scripts/google_trends.py --params-json '{"q":"AI","json":"1","hl":"en","geo":"United+States","data_type":"TIMESERIES"}'
```

要从规范化的请求生成所需的调用前参数表格而不调用 API：

```bash
python3 scripts/google_trends.py --request "search Google Trends for AI in the United States, English, timeseries" --preview-table
```

将最终脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值、允许值或参数描述时，请查阅 `references/google_trends_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_trends`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 省略用户未请求的可选字段，除非 API 有文档化的默认值需要在确认表格中显示。
- 仅在必填的 `q` 无法推断时才提出后续问题。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。
- 所有文件、脚本输出和请求编码均使用 UTF-8。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 跳过缓存 / 不使用缓存 -> `no_cache: "true"`
- 使用缓存 -> `no_cache: "false"`
- 语言 / 界面语言 -> `hl`
- 国家、地区或 Google Trends 位置 -> `geo`
- 子区域级别 / 城市 / DMA / 国家-地区细分 -> `region`
- 时间趋势 / 随时间变化的兴趣 -> `data_type: "TIMESERIES"`
- 区域比较 -> `data_type: "GEO_MAP"`
- 区域兴趣分布 -> `data_type: "GEO_MAP_0"`
- 相关主题 -> `data_type: "RELATED_TOPICS"`
- 相关查询 -> `data_type: "RELATED_QUERIES"`
- 时区偏移（分钟） -> `tz`
- 类别 -> `cat`
- 图片搜索 -> `gprop: "images"`
- 新闻搜索 -> `gprop: "news"`
- Google Shopping -> `gprop: "froogle"`
- YouTube 搜索 -> `gprop: "youtube"`
- 日期范围，"过去 12 个月"、"today 5-y" 或其他 Google Trends 日期表达式 -> `date`
- CSV 结果 -> `csv: "true"`
- 包含低搜索量地区 -> `include_low_search_volume: "true"`
