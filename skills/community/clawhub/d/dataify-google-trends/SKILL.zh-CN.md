---
name: dataify-google-trends
description: "当用户请求“调用 Google Trends”或“趋势搜索/Google Trends”，或明确提到趋势搜索字段时，触发 dataify-google-trends skill。"
---

# Dataify Google Trends

使用此 skill 将用户的 Google Trends 请求转化为 Dataify Scraper API 表单提交。
## 工作流程

1. 将用户请求解析为 Google Trends 字段。使用 `q` 作为查询，将 `engine` 设为 `google_trends`。
2. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
3. 根据用户的请求加上必要的 API 默认值构建请求参数。不要将示例值当作默认值。特别是不要将 `q` 默认为 `pizza`；如果无法推断查询内容，请向用户询问。
6. 确认后，使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_trends.py` 的绝对路径。

```bash
python3 scripts/google_trends.py --q "AI" --json 1
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

## 结果呈现

- 默认返回精简、可直接使用的结果：最相关的标题、链接和垂类关键字段，并在必要时说明数量或截断情况。
- 普通流程不暴露传输细节、固定引擎字段、任务内部状态或完整响应包装。
- 只有用户明确要求原始输出时才返回 raw JSON 或 HTML。
- 保留来源链接，区分字段缺失与空值，不得编造数据。

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
