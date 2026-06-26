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

向用户展示预览表格。表格必须包含完整的字段列表（除 `Authorization` 外），仅包含以下列：参数名、当前值、默认值、说明。询问用户是否需要修改参数。用户确认前不要调用 API。

用户确认后，使用相同的请求和显式覆盖调用 API，并添加 `--confirmed`。如果用户在对话中提供了 token，显式传递：

```bash
python3 scripts/duckduckgo_search.py --request "<user request>" --token "<DATAIFY_API_TOKEN>" --confirmed
```

脚本在未提供 `--token` 时从环境读取 `DATAIFY_API_TOKEN`。如果没有可用的 token，停止操作并要求用户提供 Dataify API token 或前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 注册。

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
