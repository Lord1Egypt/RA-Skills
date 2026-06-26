# Dataify Bing Videos API Reference

Source: `F:\Users\user\Desktop\dataify_skill\bing\bing_videos.md`

## Endpoint

- Method: `POST`
- URL: `https://scraperapi.dataify.com/request`
- Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The bundled script uses this URL directly and does not read endpoint environment variables.

## Defaults

Use defaults from parameter descriptions, not request examples:

- `engine`: `bing_videos`.
- `q`: `pizza`.
- `json`: `1`.
- `first`: `1`.
- `no_cache`: `false`.

No other request field has a default in this skill. Use `pizza` for `q` only because the field description states it as the default, not because it appears in the request example.

## Request Fields

Required:

- `engine`: always `bing_videos`.
- `q`: search keywords in any language. Default `pizza`.

Optional:

- `json`: output format. Default `1`.
  - `1`: JSON.
  - `2`: JSON plus HTML.
  - `3`: HTML.
- `mkt`: result UI market and language in `<language>-<country>` form, for example `en-US` or `zh-CN`.
- `cc`: two-letter country or region code, for example `us`, `ru`, `uk`.
- `setlang`: search language, commonly a two-letter language code such as `en`, `zh`, or `ja`.
- `first`: organic result offset. Default `1`.
- `length`: video duration.
  - `short`: short videos under 5 minutes.
  - `medium`: medium videos from 5 to 20 minutes.
  - `long`: long videos over 20 minutes.
- `date`: video freshness.
  - `lt1440`: past 24 hours.
  - `lt10080`: past week.
  - `lt43200`: past month.
  - `lt525600`: past year.
- `resolution`: video resolution.
  - `lowerthan_360p`: below 360p.
  - `360p`: 360p or higher.
  - `480p`: 480p or higher.
  - `720p`: 720p or higher.
  - `1080p`: 1080p or higher.
- `source_site`: source filter.
  - `dailymotion.com`, `vimeo.com`, `metacafe.com`, `hulu.com`, `vevo.com`, `myspace.com`, `mtv.com`, `cbsnews.com`, `foxnews.com`, `cnn.com`, `msn.com`.
- `price`: price filter.
  - `free`: free videos.
  - `paid`: paid videos.
- `no_cache`: cache behavior. Default `false`.
  - `true`: skip the five-minute cache.
  - `false`: use cache.

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
