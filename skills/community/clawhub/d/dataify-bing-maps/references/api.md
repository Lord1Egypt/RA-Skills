# Dataify Bing Maps API Reference

Source: `F:\Users\user\Desktop\dataify_skill\bing\bing_maps.md`

## Endpoint

- Method: `POST`
- URL: `https://scraperapi.dataify.com/request`
- Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The bundled script uses this URL by default and does not read endpoint environment variables.

## Request Fields

Required:

- `engine`: always `bing_maps`.
- `q`: Bing Maps 搜索关键词。可以使用常规 Bing Maps 搜索中的任意查询内容。

Optional:

- `json`: 输出格式。
  - `1`: JSON。默认值为 `1`。
  - `2`: JSON+HTML。
  - `3`: HTML。
- `cp`: 查询中心点 GPS 坐标，顺序为 `纬度~经度`。仅当用户提供坐标时传入，不要把文档示例坐标当默认值。
- `setlang`: 两位语言/地区值，例如 `us`、`de`、`gb`。仅当用户要求时传入。
- `place_id`: Bing Maps 地点唯一引用。仅当用户提供时传入。
- `first`: 本地结果偏移量。默认值为 `0`。
- `count`: 每页建议返回结果数量，最大值为 `30`；最大值不是默认值。仅当用户要求结果数量时传入。
- `no_cache`: `true` 表示跳过五分钟缓存，`false` 表示使用缓存。默认值为 `false`。

Use defaults from parameter descriptions only. Do not use sample values as defaults.

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
