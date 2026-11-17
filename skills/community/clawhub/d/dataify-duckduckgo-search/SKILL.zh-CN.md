---
name: dataify-duckduckgo-search
description: "当用户要求搜索 DuckDuckGo 或获取 DuckDuckGo 结果时，使用此 skill。"
---

# Dataify DuckDuckGo Search

## 工作流程

使用 `python3` 运行内置脚本完成整个流程。除非脚本需要维护，否则不要手动构建 HTTP 请求。

每次调用 API 前必须先预览参数：

```bash
python3 scripts/duckduckgo_search.py --request "<user request>" --preview
```

在 `python3` 别名不可用的 Windows 工作区上，使用已安装的 Python 3 启动器运行同一脚本，例如 `python scripts/duckduckgo_search.py ...`。



```bash
```


## 字段映射

将用户的完整请求传递给 `--request`；脚本会自动将自然语言提示和显式赋值映射到 Dataify 字段：

| Field | Behavior |
| --- | --- |
| `engine` | 始终为 `duckduckgo`。 |
| `q` | 从用户请求或 `--q` 解析的搜索查询。必填。 |
| `json` | 输出格式：`1` JSON，`2` JSON+HTML，`3` HTML，`4` Light JSON。默认为 `1`。 |
| `kl` | DuckDuckGo 地区代码，如 `us-en`、`uk-en` 或 `fr-fr`；无默认值。 |
| `search_assist` | `true` 或 `false`；默认为 `false`；不能与 `m` 同时发送。如果启用，脚本会省略 `m`。 |
| `safe` | `1` 严格，`-1` 中等（默认），`-2` 关闭。 |
| `df` | `d`、`w`、`m`、`y`，或日期范围如 `2021-06-15..2024-06-16`。 |
| `start` | 结果偏移量；根据 API 描述默认为 `0` 或空。 |
| `m` | 最大结果数，默认为 `50`，限制在 `1..50`；当 `search_assist=true` 时省略。 |
| `no_cache` | `true` 跳过缓存；`false` 默认使用缓存。 |

当用户未指定某个字段时，使用参数描述中的默认值：`engine=duckduckgo`、`json=1`、`search_assist=false`、`safe=-1`、`start=0`、`m=50` 和 `no_cache=false`。`q`、`kl` 和 `df` 无默认值。不要将 API 文档示例当作默认值：切勿使用 `q=pizza`、`kl=us-en`、`search_assist=true`、`safe=1`、`df=d`、仅因示例中出现就使用 `start=0`、`m=10` 或 `no_cache=true`，除非用户请求或文档化默认值如此规定。

对于精确控制，传递显式标志如 `--q`、`--json`、`--kl`、`--safe`、`--df`、`--start`、`--m`、`--no-cache` 和 `--search-assist`；显式标志会覆盖自然语言解析器。

## 响应处理

脚本以 `application/x-www-form-urlencoded` 表单数据形式提交请求，而非 JSON。

将脚本的标准输出直接返回给用户。不要对 API 响应进行总结、翻译、美化打印、过滤或其他处理。

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
