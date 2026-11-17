---
name: dataify-google-shopping
description: "当用户请求“调用 Google Shopping”或“购物搜索/商品搜索/价格比较”，或明确提到购物搜索字段时，触发 dataify-google-shopping skill。"
---

# Dataify Google Shopping

使用此 skill 将用户的 Google Shopping 请求转化为 Dataify Scraper API 调用。
## 工作流程

1. 将用户请求解析为 Dataify Google Shopping 字段。使用 `q` 作为购物搜索查询，并始终将 `engine` 设为 `google_shopping`。
2. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
3. 仅使用用户请求的字段加上必要的文档化默认值构建请求参数。除非用户要求其他值，否则使用 `json: "1"` 和 `google_domain: "google.com"`。不要将 API 文档中的示例值当作默认值。
5. 如果用户修改了任何参数，更新值并在调用前再次展示完整表格。
6. 确认后，使用 `python3` 运行内置 Python 脚本。脚本会以表单数据形式提交到硬编码的端点 `https://scraperapi.dataify.com/request`。

## 脚本使用

从此 skill 目录运行命令，或使用 `scripts/google_shopping.py` 的绝对路径。

按需预览高级参数：

```bash
python3 scripts/google_shopping.py --q "wireless headphones" --gl us --hl en --max_price 100 --free_shipping true --table
```


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
