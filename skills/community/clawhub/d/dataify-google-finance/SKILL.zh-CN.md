---
name: dataify-google-finance
description: "当用户请求“调用 Google Finance”或“搜索 Google Finance”，或明确提到金融数据相关内容（股票、指数、基金、货币、期货）时，触发 dataify-google-finance skill。"
---

# Dataify Google Finance

使用此 skill 将用户的 Google Finance 请求转化为 Dataify Scraper API 表单 POST。
## 工作流程

1. 将用户请求解析为 Dataify Google Finance 字段。使用 `q` 作为金融查询，将 `engine` 设为固定值 `google_finance`。
2. 仅使用参数描述中的文档化默认值：
   - `engine`: 固定 `google_finance`
   - `json`: 默认 `1`
   - `window`: 默认 `1D`
   - `no_cache`: 默认 `false`
   - `q`: 无默认值；如果无法推断则询问用户
   - `hl`: 无文档化默认值；除非用户指定，否则留空

```bash
python3 scripts/google_finance.py --request "查询 NASDAQ:GOOGL，窗口 1年，英文，返回 JSON" --preview-table
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_finance.py --params-json '{"q":"NASDAQ:GOOGL","window":"1Y","hl":"en","json":"1"}' --preview-table
```

5. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_finance.py` 的绝对路径。

```bash
python3 scripts/google_finance.py --q "NASDAQ:GOOGL" --window 1Y --hl en --json 1
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
