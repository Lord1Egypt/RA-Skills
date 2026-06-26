# Dataify Bing News API Reference

Source: `F:\Users\user\Desktop\dataify_skill\bing\bing_news.md`

## Endpoint

- Method: `POST`
- URL: `https://scraperapi.dataify.com/request`
- Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The bundled script uses this URL directly and does not read endpoint environment variables.

## Request Fields

Required:

- `engine`: always `bing_news`.
- `q`: news search keywords in any language. The parameter description says the default value is `pizza`.

Optional:

- `json`: output format.
  - `1`: JSON. The parameter description says JSON is the default output format.
  - `2`: JSON plus HTML.
  - `3`: HTML.
- `mkt`: result UI market and language in `<language>-<country>` form, for example `en-US` or `zh-CN`. The parameter description gives examples but no default value.
- `cc`: two-letter country or region code, for example `us`, `ru`, or `uk`. The parameter description gives examples but no default value.
- `first`: result offset. The parameter description says the default value is `1`.
- `count`: requested result count. This is a suggested count and may not exactly match the returned result count. The parameter description gives no default value.
- `qft`: Bing query filter string for date sorting/filtering. The parameter description gives no default value.
- `safeSearch`: adult-content filter level.
  - `Off`
  - `Moderate`
  - `Strict`
  - The parameter description gives allowed values but no default value.
- `no_cache`: cache behavior.
  - `true`: skip the five-minute cache.
  - `false`: use cached results when available. The parameter description says `false` is the default.

Do not send optional fields with sample values from the source document. Defaults used by the skill are only: `engine=bing_news`, `q=pizza`, `json=1`, `first=1`, and `no_cache=false`.

Before every live API call, show all body fields in a table with only these columns: 参数名, 当前值, 默认值, 说明. Do not include `Authorization`.

## Response Shape

HTTP 200 response:

```json
{
  "code": 200,
  "data": {
    "task_id": "43",
    "result": {
      "html": "...",
      "json": "...",
      "response_time": 1809570193201
    }
  }
}
```

Notes:

- `data.task_id` is the task ID.
- `data.result.json` can be a string containing JSON data.
- `data.result.html` contains HTML when requested.
- `data.result.response_time` is the response time.
