---
name: dataify-google-local
description: "当用户请求“调用 Google Local”或“本地搜索/附近搜索/地点搜索”，或明确提到本地搜索字段时，触发 dataify-google-local skill。"
---

# Dataify Google Local

使用此 skill 将用户的 Google Local 请求转化为 Dataify Scraper API 表单 POST。
## 工作流程

1. 将用户请求解析为 Google Local 字段。始终将 `engine` 设为固定值 `google_local`。
4. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
5. 使用用户请求的字段加上仅有的文档化默认值构建请求参数：`engine: "google_local"`、`json: "1"`、`google_domain: "google.com"` 和 `no_cache: "false"`。省略用户未请求且没有文档化默认值的可选字段。

```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --gl us --hl en
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_local.py --params-json '{"q":"coffee shops","location":"New York","gl":"us","hl":"en"}'
```

PowerShell 可能需要转义引号：

```powershell
python3 scripts/google_local.py --params-json '{\"q\":\"coffee shops\",\"location\":\"New York\",\"gl\":\"us\",\"hl\":\"en\"}'
```

使用脚本解析自然语言请求：

```bash
python3 scripts/google_local.py --request "搜索纽约咖啡店，语言英文，地区美国，不走缓存"
```


## 参数说明

使用此 skill 时，在调用 API 前展示以下简明参数列表，或运行 `python3 scripts/google_local.py --describe-params` 并转发其输出：

| Field | Required | Default | Description |
|---|---:|---|---|
| `Authorization` | yes | none | 请求头中的 Dataify API token。如果 token 不以 `Bearer ` 开头，脚本会自动添加。 |
| `engine` | yes | `google_local` | Google Local 的固定引擎值。 |
| `q` | yes | none | 搜索查询内容。 |
| `json` | yes | `1` | 输出格式。`1` = JSON，`2` = JSON+HTML，`3` = HTML，`4` = Light JSON。 |
| `google_domain` | no | `google.com` | 使用的 Google 域名。 |
| `gl` | no | none | 两位字母的 Google 国家/地区代码，如 `us`、`uk` 或 `fr`。 |
| `hl` | no | none | Google 界面/搜索语言代码，如 `en`、`es` 或 `fr`。 |
| `location` | no | none | 搜索发起的地理位置。 |
| `uule` | no | none | Google 编码位置。不要与 `location` 同时使用；如果两者都存在，优先使用明确的 `uule`。 |
| `start` | no | none | 分页结果偏移量。 |
| `ludocid` | no | none | Google 地点 CID/客户标识符。 |
| `tbs` | no | none | 常规查询字段无法表示的高级搜索参数。 |
| `no_cache` | no | `false` | `true` 跳过缓存；`false` 在可用时使用缓存结果。 |

对于实际请求，展示完整的预览而不仅仅是已赋值的请求负载：

```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --preview-params --preview-format markdown
```

预览输出必须包含用户未提供的未设置字段，如 `gl`、`hl`、`uule`、`start`、`ludocid` 和 `tbs`。
展示预览表格后，询问：`请确认是否按以上参数调用接口，或告诉我要修改哪些字段。`

## 字段映射

需要确切的参数措辞时，请查阅 `references/google_local_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_local`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 省略用户未请求的可选字段，除非该字段有文档化的默认值。
- 仅在必填搜索查询 `q` 无法推断时才提出后续问题。
- 如果 `location` 和 `uule` 同时存在，优先使用明确的 `uule` 并省略 `location`。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 用于 Google 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- 命名的搜索起点 -> `location`
- 编码位置 -> `uule`
- 页码 N -> `start: String((N - 1) * 10)`
- Google 地点 CID -> `ludocid`
- 高级搜索过滤器 -> `tbs`
- 跳过/不使用缓存 -> `no_cache: "true"`

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
