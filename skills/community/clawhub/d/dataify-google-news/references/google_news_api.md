# Dataify Google News API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON.

## Form Fields

Always include:

| Field | Required | Value |
| --- | --- | --- |
| `engine` | yes | 固定使用 `google_news` 引擎 |
| `q` | yes | 用户要查询的新闻关键词 |
| `json` | yes | 输出模式，默认 `1` |

Optional fields:

| Field | Meaning | Accepted values or format |
| --- | --- | --- |
| `no_cache` | 跳过缓存 | 是否跳过缓存重新抓取，可填 `true` 或 `false` |
| `gl` | Google 国家/地区 | 两位国家或地区代码，例如 `us`、`uk`、`fr` |
| `hl` | Google 语言 | Google News 界面语言代码，例如 `en`、`zh-cn`、`es`、`fr` |
| `topic_token` | Google News 主题 token | Google News 的原始主题 token |
| `kgmid` | 知识图谱 MID | 主题或地点对应的 Knowledge Graph MID，通常以 `/m/` 或 `/g/` 开头 |
| `publication_token` | Google News 出版方 token | Google News 的原始出版方 token |
| `section_token` | Google News 栏目 token | Google News 的原始栏目 token |
| `story_token` | Google News 故事 token | Google News 的原始故事 token |
| `so` | 排序方式 | 排序方式，`0` 表示相关度，`1` 表示时间 |

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Examples

Search Google News for pizza:

```json
{"q":"pizza","json":"1"}
```

Search United States English news and bypass cache:

```json
{"q":"pizza","json":"1","gl":"us","hl":"en","no_cache":"true"}
```

Search latest technology news:

```json
{"q":"technology","json":"1","so":"1"}
```

Search by a Google News topic token:

```json
{"q":"technology","json":"1","topic_token":"TOPIC_TOKEN"}
```
