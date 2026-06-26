# Dataify Google AI Mode API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON.

## Form Fields

Always include:

| Field | Required | Value |
| --- | --- | --- |
| `engine` | yes | 固定使用 `google_ai_mode` 引擎 |
| `q` | yes | 用户要查询的问题或关键词 |
| `json` | yes | 输出模式，默认 `1` |

Optional fields:

| Field | Meaning | Accepted values or format |
| --- | --- | --- |
| `location` | 搜索发起位置 | 模拟搜索发起地理位置 |
| `uule` | Google 编码位置 | Google 的原始 UULE 编码位置；同时存在时优先于 `location` |
| `no_cache` | 跳过缓存 | 是否跳过缓存重新抓取，可填 `true` 或 `false` |
| `gl` | Google 国家/地区 | 两位国家或地区代码，例如 `us`、`jp`、`fr` |
| `hl` | Google 语言 | 搜索界面语言代码，例如 `en`、`zh-cn`、`ja`、`fr` |

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Examples

Ask Google AI Mode about pizza:

```json
{"q":"pizza","json":"1"}
```

Ask in English for United States behavior and bypass cache:

```json
{"q":"best pizza dough hydration","json":"1","gl":"us","hl":"en","location":"United States","no_cache":"true"}
```

Ask from Japan and return JSON plus HTML:

```json
{"q":"Tokyo pizza recommendations","json":"2","location":"Japan","gl":"jp","hl":"en"}
```
