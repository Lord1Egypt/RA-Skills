---
name: dataify-google-maps
description: "当用户请求“调用 Google Maps”或“地图搜索/位置详情”，或明确提到地图搜索字段时，触发 dataify-google-maps skill。"
---

# Dataify Google Maps

使用此 skill 将用户的 Google Maps 请求转化为 Dataify Scraper API 表单提交。

## 调用前确认（必须）

每次真正调用 API 之前，必须遵循以下确认流程。这些规则优先于本 skill 中任何旧的工作流程顺序。

1. 将用户请求解析为 API body 字段和固定的 `engine` 值。
2. 仅在参数描述明确标注默认值时才使用默认值。不要将示例 YAML 值、示例提示词、占位符值或示例（如 `pizza`、`us`、`en`、日期、机场代码或 token）作为默认值。
3. 如果必填参数没有文档化的默认值且无法从用户请求中推断，先询问该参数再构建表格。
4. 调用 API 前展示 Markdown 表格。不要包含 `Authorization`。包含本 skill 参考文档中的完整 body 字段列表（包含 `engine`），即使某个字段当前为空也要列出。
5. 表格必须恰好包含以下列：`参数名`、`当前值`、`默认值`、`说明`。
6. 展示表格后询问用户是否需要修改参数。用户明确确认后才能调用 API。
7. 如果用户修改了参数，重新生成表格并再次确认。
8. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。

尽可能使用内置的预览辅助工具从本 skill 的参考文档生成确认表格：

```bash
python3 scripts/preview_params.py --params-json '{"q":"USER_QUERY"}'
```

将每个已解析的当前值通过 `--params-json` 或对应的 `--field value` 参数传递给 `preview_params.py`。辅助工具从 `references/*api.md` 读取默认值和描述；如果辅助工具无法解析某个默认值，保留默认值为空，而不是编造一个。
9. 确认并处理 token 后，使用 `python3` 调用内置 Python 脚本，并将 API 响应体直接返回，不进行总结、提取、清理、翻译或重新格式化。

## 工作流程

1. 将用户请求解析为 Google Maps 字段。将 `engine` 设为固定值 `google_maps`。
2. 当用户未指定某个值时，使用参数描述中记录的默认值。对于此 API，文档化的默认值为：
   - `engine`: `google_maps`
   - `json`: `1`
   - `google_domain`: `google.com`
   - `start`: `0`
   - `no_cache`: `false`

   将所有其他字段视为无默认值，除非用户提供。切勿将 `United States`、`en`、`us`、`@40.7455096,-74.0083012,14z` 或 `true` 等示例当作默认值。
3. 每次真正调用 API 前，向用户展示完整的请求参数表格并询问是否需要修改。不要在表格中显示 `Authorization`。用户确认前不要调用 API。

使用以下表格格式，包含每个 body 字段：

```text
请确认是否要修改参数；你确认后我再调用接口。

| 参数名 | 当前值 | 默认值 | 说明 |
|---|---|---|---|
| `engine` | `google_maps` | `google_maps` | 固定引擎值。 |
| `q` | `<从用户需求解析出的值；无值则询问>` | 无 | Google Maps 搜索关键词。 |
| `json` | `<用户指定值或 1>` | `1` | 返回格式：1=JSON，2=JSON+HTML，3=HTML，4=Light JSON。 |
| `ll` | `<用户指定值或空>` | 无 | 完整地图坐标起点，格式为 `@纬度,经度,缩放z` 或 `@纬度,经度,高度m`。不能和 `location`、`lat`、`lon`、`z`、`m` 同用。 |
| `location` | `<用户指定值或空>` | 无 | 文字地点起点；需配合 `z` 或 `m`。不能和 `ll`、`lat`、`lon` 同用。 |
| `lat` | `<用户指定值或空>` | 无 | 搜索起点纬度；必须和 `lon` 成对使用，并配合 `z` 或 `m`。 |
| `lon` | `<用户指定值或空>` | 无 | 搜索起点经度；必须和 `lat` 成对使用，并配合 `z` 或 `m`。 |
| `z` | `<用户指定值或空>` | 无 | 地图缩放级别；不能和 `m` 同用。 |
| `m` | `<用户指定值或空>` | 无 | 地图高度，单位米；不能和 `z` 同用。 |
| `nearby` | `<用户指定值或空>` | 无 | 是否强制返回更接近指定起点的结果；应与 `ll`、`location` 或 `lat`/`lon` 一起使用。 |
| `google_domain` | `<用户指定值或 google.com>` | `google.com` | Google 域名。 |
| `hl` | `<用户指定值或空>` | 无 | Google Maps 搜索语言代码。 |
| `gl` | `<用户指定值或空>` | 无 | Google Maps 搜索国家/地区代码。 |
| `start` | `<用户指定值或 0>` | `0` | 分页偏移量。 |
| `type` | `<用户指定值或空>` | 无 | 搜索类型：`search` 或 `place`。 |
| `data` | `<用户指定值或空>` | 无 | 已废弃的结果过滤参数，优先使用 `place_id` 或 `data_cid`。 |
| `place_id` | `<用户指定值或空>` | 无 | Google Maps 地点唯一 ID。 |
| `data_cid` | `<用户指定值或空>` | 无 | Google Maps CID，不能和 `place_id` 同用。 |
| `no_cache` | `<用户指定值或 false>` | `false` | 是否跳过缓存；`true` 跳过缓存，`false` 使用缓存。 |
```

如果用户要求修改参数，更新当前值并再次展示完整表格。仅在用户明确确认（如"确认"、"可以"、"调用"、"继续"、"yes"等）后才调用 API。
4. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
5. 仅使用请求字段加文档化默认值构建请求参数。脚本以表单数据（而非 JSON 请求体）提交这些参数。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_maps.py` 的绝对路径。

```bash
python3 scripts/google_maps.py --q "coffee shops near Seattle" --json 1
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递，并避免在最终回答中回显该 token：

```bash
python3 scripts/google_maps.py --token "USER_TOKEN" --q "coffee shops near Seattle" --gl us --hl en
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号。脚本仍然会以表单数据形式提交给 API：

```bash
python3 scripts/google_maps.py --params-json '{"q":"coffee shops","json":"1","location":"Seattle","z":"14","gl":"us","hl":"en"}'
```

对于自然语言解析的备选方式，将用户的请求传递给 `--request`：

```bash
python3 scripts/google_maps.py --request "搜索 Seattle 的咖啡店，返回 JSON，gl=us，hl=en"
```

7. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值、约束或示例时，请查阅 `references/google_maps_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_maps`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 省略用户未请求的可选字段，但参数描述中有文档化默认值的除外。
- 每次真正调用 API 前，展示完整的 body 参数表格（从 `engine` 到 `no_cache`），省略 `Authorization`，并等待用户确认。
- 仅在必填的 `q` 或必填的配对参数无法推断时才提出后续问题。
- 对于完整的 Google Maps 坐标字符串（如 `@lat,lon,14z` 或 `@lat,lon,10410m`），单独使用 `ll`；不要将其与 `location`、`lat`、`lon`、`z` 或 `m` 组合使用。
- `lat` 和 `lon` 需成对使用。如果只有一个可用，询问缺失的坐标。
- 使用 `z` 或 `m` 其中之一，不要同时使用。使用 `location` 或 `lat`/`lon` 时，如果用户提供了搜索起点，应包含 `z` 或 `m` 之一。
- `nearby` 仅与 `ll`、`location` 或 `lat`/`lon` 一起使用。对于没有位置锚点的"附近"请求，询问用户提供 Maps 起点。
- 不要同时使用 `place_id` 和 `data_cid`。
- 优先使用 `place_id` 或 `data_cid`，而非已废弃的 `data` 字段。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google 域名 -> `google_domain`
- 用于 Google 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- 页码 N -> `start: String((N - 1) * 20)`
- 完整的 Maps 坐标字符串 -> `ll`
- 命名的搜索起点 -> `location`
- GPS 坐标 -> `lat` 和 `lon`
- 缩放级别 -> `z`
- 地图高度（米） -> `m`
- 强制返回更近的结果 / 带起点的"附近" -> `nearby: "true"`
- 结果列表搜索 -> `type: "search"`
- 地点详情 -> `type: "place"`（使用 `data` 时）；使用 `place_id` 或 `data_cid` 时省略 `type`，除非用户明确要求
- Google Maps 地点标识符 -> `place_id`
- Google Maps CID -> `data_cid`
- 跳过缓存 -> `no_cache: "true"`
