# Dataify Bing Shopping API Reference

Source: `F:\Users\user\Desktop\dataify_skill\bing\bing_shopping.md`

## Endpoint

- Method: `POST`
- URL: `https://scraperapi.dataify.com/request`
- Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The bundled script uses this URL directly and does not read endpoint environment variables.

## Request Fields

Required:

- `engine`: always `bing_shopping`.
- `q`: Bing Shopping search query. Any product keyword or phrase normally used in Bing Shopping search is valid.

Optional:

Use defaults only when the field description explicitly states a default. Do not treat example request body values as defaults. Values shown in the source API document, including `pizza`, `en-US`, `us`, empty strings, and sample filters, are examples only and must not be copied into normal requests.

- `json`: output format.
  - `1`: JSON. This is the default when the user does not specify output format.
  - `2`: JSON plus HTML.
  - `3`: HTML.
- `mkt`: display language and market in `<language>-<country/region>` form. No documented default.
- `cc`: two-letter country or region code. No documented default.
- `efirst`: shopping result offset. No documented default.
- `filters`: advanced Bing filter string copied from Bing search URLs or built for precise filtering. No documented default.
- `no_cache`: `true` skips the five-minute cache, `false` uses cache. The field description says `false` is the default.

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
