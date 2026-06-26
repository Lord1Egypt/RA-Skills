# Dataify Bing Images API Reference

Source: `F:\Users\user\Desktop\dataify_skill\bing\bing_images.md`

## Endpoint

- Method: `POST`
- URL: `https://scraperapi.dataify.com/request`
- Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The bundled script uses this URL directly and does not read endpoint environment variables.

## Request Fields

Required:

- `engine`: 接口引擎，固定为 `bing_images`。
- `q`: 搜索关键词，必填；可以输入任意想查询的关键词，也可以是任意语言。

Optional:

- `json`: 采集结果输出格式。默认值为 `1`。
  - `1`: 返回 JSON。
  - `2`: 返回 JSON 和 HTML。
  - `3`: 返回 HTML。
- `mkt`: 搜索结果界面显示语言，采用 `<语言代码>-<国家/地区代码>` 形式，例如 `en-US`。
- `cc`: 指定搜索结果按国家或地区用户习惯展示，使用两个字母的国家/地区代码，例如 `us`、`ru`、`uk`。
- `first`: 控制自然结果的偏移量。默认值为 `1`。
- `count`: 控制每页结果数量；该值为建议值，可能无法完全反映实际返回数量。
- `imagesize`: 按图片尺寸过滤。
  - `small`: 小。
  - `medium`: 中。
  - `large`: 大。
  - `wallpaper`: 超大/壁纸。
- `color2`: 按图片颜色过滤。
  - `color`: 仅彩色。
  - `bw`: 黑白。
  - `FGcls_RED`: 红色。
  - `FGcls_ORGANGE`: 橙色。
  - `FGcls_YELLOW`: 黄色。
  - `FGcls_GREEN`: 绿色。
  - `FGcls_TEAL`: 青色。
  - `FGcls_BLUE`: 蓝色。
  - `FGcls_PURPLE`: 紫色。
  - `FGcls_PINK`: 粉色。
  - `FGcls_BROWN`: 棕色。
  - `FGcls_BLACK`: 黑色。
  - `FGcls_GRAY`: 灰色。
  - `FGcls_WHITE`: 白色。
- `photo`: 按图片类型过滤。
  - `photo`: 照片。
  - `clipart`: 剪贴画。
  - `linedrawing`: 线条画。
  - `animatedgif`: 动图。
  - `animatedgifhttps`: HTTPS 动图。
  - `transparent`: 透明。
  - `shopping`: 购物。
- `aspect`: 按图片布局过滤。
  - `square`: 方形。
  - `wide`: 宽图。
  - `tall`: 高图。
- `face`: 按人物类型过滤。
  - `face`: 仅面部。
  - `portrait`: 头肩肖像。
- `age`: 按日期过滤。
  - `lt1440`: 过去 24 小时。
  - `lt10080`: 过去一周。
  - `lt43200`: 过去一个月。
  - `lt525600`: 过去一年。
- `license`: 按使用许可过滤。
  - `Type-Any`: 所有 Creative Commons。
  - `L1`: Public Domain。
  - `L2_L3_L4_L5_L6_L7`: 免费共享和使用。
  - `L2_L3_L4`: 免费共享和商业使用。
  - `L2_L3_L5_L6`: 免费修改、共享和使用。
  - `L2_L3`: 免费修改、共享和商业使用。
- `no_cache`: 默认情况下缓存相同参数的搜索结果。`true` 跳过缓存，`false` 使用缓存。默认值为 `false`。

Do not use values from the source document's example body as defaults. Defaults are only values stated in field descriptions: `engine=bing_images`, `json=1`, `first=1`, and `no_cache=false`. Omit all other optional fields when the user has not provided or implied them.

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
