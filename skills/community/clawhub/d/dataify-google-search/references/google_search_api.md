# Dataify Google Search API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON.

## Form Fields

Always include:

| Field | Required | Value |
| --- | --- | --- |
| `engine` | yes | 固定使用 `google` 搜索引擎 |
| `q` | yes | 用户要搜索的关键词 |
| `json` | yes | 输出模式，默认 `1` |

Optional fields:

| Field | Meaning | Accepted values or format |
| --- | --- | --- |
| `google_domain` | Google 域名 | Google 搜索使用的域名，例如 `google.com`、`google.co.jp`、`google.co.uk` |
| `gl` | Google 国家/地区 | 两位国家或地区代码，例如 `us`、`jp`、`fr` |
| `hl` | Google 语言 | 搜索界面语言代码，例如 `en`、`zh-cn`、`ja`、`fr` |
| `cr` | 限制结果国家/地区 | 限制搜索结果所属国家或地区，格式为 `country` 加大写国家代码 |
| `lr` | 限制结果语言 | 限制搜索结果语言，格式为 `lang_` 加语言代码 |
| `location` | 搜索发起位置 | 模拟搜索发起地理位置 |
| `uule` | Google 编码位置 | Google 的原始 UULE 编码位置；同时存在时优先于 `location` |
| `start` | 结果偏移量 | 搜索结果起始偏移量，`0` 为第一页，`10` 为第二页，`20` 为第三页 |
| `tbs` | 高级搜索参数 | Google 原始 `tbs` 高级搜索参数 |
| `safe` | 安全搜索 | 安全搜索开关，可填 `active` 或 `off` |
| `nfpr` | 排除自动更正结果 | 是否排除 Google 自动更正查询后的结果，可填 `0` 或 `1` |
| `filter` | 类似/省略结果过滤 | 是否启用类似结果或省略结果过滤，可填 `0` 或 `1`，默认 `1` |
| `device` | 设备类型 | 模拟访问设备类型，可填 `desktop`、`tablet` 或 `mobile` |
| `render_js` | 渲染 JavaScript | 是否渲染 JavaScript，可填 `true` 或 `false` |
| `no_cache` | 跳过缓存 | 是否跳过缓存重新抓取，可填 `true` 或 `false` |
| `ai_overview` | 包含 AI Overview | 是否包含 Google AI Overview，可填 `true` 或 `false` |

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Examples

Search Google in English from the United States:

```json
{"q":"OpenAI news","json":"1","gl":"us","hl":"en","location":"United States"}
```

Search Japanese Google on mobile and include rendered HTML:

```json
{"q":"東京 天気","json":"2","google_domain":"google.co.jp","gl":"jp","hl":"ja","device":"mobile","render_js":"true"}
```

Get the second page with safe search off:

```json
{"q":"pizza","json":"1","start":"10","safe":"off"}
```
