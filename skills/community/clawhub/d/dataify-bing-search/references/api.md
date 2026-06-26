# Dataify Bing Search API Reference

Source: `F:\Users\user\Desktop\dataify_skill\bing\bing_search.md`

## Endpoint

- Method: `POST`
- URL: `https://scraperapi.dataify.com/request`
- Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The bundled script uses this URL by default and does not read endpoint environment variables.

## Request Fields

Required:

- `engine`: Bing search engine. Default from the parameter description: `bing`.
- `q`: search keywords in any language. Default from the parameter description: `pizza`. Replace this default when the user asks for a concrete search.

Optional:

- `json`: output format.
  - `1`: JSON. This is the default when the user does not specify an output format.
  - `2`: JSON plus HTML.
  - `3`: HTML.
- `location`: named geographic search origin. If multiple locations match, the service chooses the most popular match.
- `lat`: GPS latitude.
- `lon`: GPS longitude.
- `mkt`: result UI market and language in `<language>-<country>` form, for example `en-US` or `zh-CN`. This is not a default.
- `cc`: two-letter country or region code, for example `us`, `ru`, `uk`. This is not a default.
- `first`: organic result offset. Default from the parameter description: `1`.
- `safeSearch`: adult content filtering level.
  - `Off`: include adult text, images, or videos.
  - `Moderate`: include adult text, exclude adult images and videos.
  - `Strict`: exclude adult text, images, and videos.
- `filters`: advanced Bing filter string.
- `no_cache`: `true` skips the five-minute cache, `false` uses cache. Default from the parameter description: `false`.

The source document includes sample body values, but this skill must not treat those samples as defaults. Defaults must come only from parameter descriptions. Current defaults are `engine=bing`, `q=pizza`, `json=1`, `first=1`, and `no_cache=false`. Sample body values such as `location=India`, `lat=1`, `lon=1`, `mkt=zh-cn`, and `cc=AR` are not defaults.

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
