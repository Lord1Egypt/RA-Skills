---
name: dataify-google-maps
description: "当用户请求“调用 Google Maps”或“地图搜索/位置详情”，或明确提到地图搜索字段时，触发 dataify-google-maps skill。"
---

# Dataify Google Maps

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

Use this skill for explicit Google Maps searches that need map coordinates, zoom, or map pagination. Use Google Local for local-pack keyword lists, Map Details for a known Place ID, and Maps Reviews for reviews.

使用此 skill 将用户的 Google Maps 请求转化为 Dataify Scraper API 表单提交。
## 工作流程

1. 将用户请求解析为 Google Maps 字段。将 `engine` 设为固定值 `google_maps`。
2. 当用户未指定某个值时，使用参数描述中记录的默认值。对于此 API，文档化的默认值为：
   - `engine`: `google_maps`
   - `json`: `1`
   - `google_domain`: `google.com`
   - `start`: `0`
   - `no_cache`: `false`

   将所有其他字段视为无默认值，除非用户提供。切勿将 `United States`、`en`、`us`、`@40.7455096,-74.0083012,14z` 或 `true` 等示例当作默认值。

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

4. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
5. 仅使用请求字段加文档化默认值构建请求参数。脚本以表单数据（而非 JSON 请求体）提交这些参数。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_maps.py` 的绝对路径。

```bash
python3 scripts/google_maps.py --q "coffee shops near Seattle" --json 1
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号。脚本仍然会以表单数据形式提交给 API：

```bash
python3 scripts/google_maps.py --params-json '{"q":"coffee shops","json":"1","location":"Seattle","z":"14","gl":"us","hl":"en"}'
```

对于自然语言解析的备选方式，将用户的请求传递给 `--request`：

```bash
python3 scripts/google_maps.py --request "搜索 Seattle 的咖啡店，返回 JSON，gl=us，hl=en"
```


## 字段映射

需要确切的字段列表、默认值、约束或示例时，请查阅 `references/google_maps_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_maps`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 省略用户未请求的可选字段，但参数描述中有文档化默认值的除外。
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

## 结果呈现

- 默认返回精简、可直接使用的结果：最相关的标题、链接和垂类关键字段，并在必要时说明数量或截断情况。
- 普通流程不暴露传输细节、固定引擎字段、任务内部状态或完整响应包装。
- 只有用户明确要求原始输出时才返回 raw JSON 或 HTML。
- 保留来源链接，区分字段缺失与空值，不得编造数据。

## 参数交互策略

- 当请求意图明确、只读、低风险且成本较低时，使用安全默认值直接执行。可以用一句话说明执行内容，但不要暂停等待确认。
- 只在缺少必填输入、存在会明显改变结果的歧义、大批量或多页采集、媒体下载、会明显增加积分消耗、不可逆操作，或用户明确要求查看参数时询问。
- 必须确认时，只展示会影响目标、范围、输出或成本的用户参数。优先使用一句简短说明；只有三个及以上关键值确实需要比较时才使用精简表格。
- 不要展示固定字段、空的可选字段、未修改的默认值、凭据或内部实现参数，例如引擎选择、响应格式开关、偏移量、spider ID 和文件名模板。
- 默认隐藏高级筛选项，除非用户主动询问或需要它们消除歧义。不得用文档示例值代替用户缺失的必填输入。
- 先返回首个结果，再提供相关的细化选项，不要在首次执行前强迫用户决定所有可选项。

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
