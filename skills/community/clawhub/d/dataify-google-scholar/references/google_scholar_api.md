# Dataify Google Scholar API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON.

## Form Fields

Show this complete field list before every call, excluding `Authorization`.

| 参数名 | 必选 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `engine` | 是 | `google_scholar` | Google 学术接口固定值。 |
| `q` | 否 |  | 搜索查询内容。 |
| `json` | 是 | `1` | 输出格式。`1` 为 JSON，`2` 为 JSON+HTML，`3` 为 HTML，`4` 为 Light JSON。 |
| `hl` | 否 |  | Google 学术要使用的界面语言，两位或带地区的语言代码，例如 `en`、`es`、`fr`、`zh-cn`。 |
| `lr` | 否 |  | 限制结果语言，格式为 `lang_{语言代码}`，多个语言用 `|` 分隔，例如 `lang_fr|lang_de`。 |
| `start` | 否 | `0` | 结果偏移量，用于分页。`0` 为第一页，`10` 为第二页，`20` 为第三页。 |
| `num` | 否 | `10` | 返回的最大结果数量，范围 `1` 到 `20`。 |
| `cites` | 否 |  | 文章唯一 ID，用于触发“被引”搜索；可与 `q` 同时使用以在引用文献中搜索。 |
| `as_ylo` | 否 |  | 结果起始年份；可与 `as_yhi` 结合使用。 |
| `as_yhi` | 否 |  | 结果结束年份；可与 `as_ylo` 结合使用。 |
| `scisbd` | 否 | `0` | 过去一年添加的文献和排序。`0` 表示按相关性排序，`1` 表示过去一年且仅包含摘要，`2` 表示过去一年且包含全部内容。 |
| `cluster` | 否 |  | 文章唯一 ID，用于触发“所有版本”搜索。禁止与 `q` 和 `cites` 一起使用。 |
| `as_sdt` | 否 | `0` | 搜索类型或专利过滤器。`0` 排除专利，`7` 包含专利，`4` 选择美国法院判例法。 |
| `safe` | 否 |  | 成人内容过滤级别，可为 `active` 或 `off`。文档未给出明确参数默认值。 |
| `filter` | 否 | `1` | “类似结果”和“省略结果”过滤器。`1` 启用，`0` 禁用。 |
| `as_vis` | 否 | `0` | 是否排除引用。`1` 排除引用，`0` 包含引用。 |
| `as_rr` | 否 | `0` | 是否仅显示综述文章。`1` 启用，`0` 显示所有结果。 |
| `no_cache` | 否 | `false` | 是否跳过 5 分钟相同参数缓存。`true` 跳过缓存，`false` 使用缓存。 |

## Default Rules

Use only defaults explicitly stated in the parameter descriptions:

| 参数名 | 默认值来源 |
| --- | --- |
| `engine` | 固定值 `google_scholar` |
| `json` | “默认为 JSON”，对应 `1` |
| `start` | “`0`（默认）是第一页结果” |
| `num` | “默认为 `10`” |
| `scisbd` | “默认值为 `0`” |
| `as_sdt` | “`0` - 排除专利（默认）” |
| `filter` | “`1`（默认）以启用这些过滤器” |
| `as_vis` | “`0`（默认）以包含它们” |
| `as_rr` | “`0`（默认）以显示所有结果” |
| `no_cache` | “`false`（默认）则使用缓存结果” |

Do not treat values inside examples, such as `cites=1275980731835430123` or `cluster=1275980731835430123`, as defaults.

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Examples

Search Google Scholar for papers from 2020 to 2024:

```json
{"q":"large language model","json":"1","as_ylo":"2020","as_yhi":"2024","num":"10"}
```

Search cited-by results:

```json
{"cites":"1275980731835430123","q":"transformer","json":"1"}
```

Search all versions for one article:

```json
{"cluster":"1275980731835430123","json":"1"}
```
