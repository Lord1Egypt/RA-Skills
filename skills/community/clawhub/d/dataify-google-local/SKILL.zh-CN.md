---
name: dataify-google-local
description: "当用户请求“调用 Google Local”或“本地搜索/附近搜索/地点搜索”，或明确提到本地搜索字段时，触发 dataify-google-local skill。"
---

# Dataify Google Local

使用此 skill 将用户的 Google Local 请求转化为 Dataify Scraper API 表单 POST。

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

1. 将用户请求解析为 Google Local 字段。始终将 `engine` 设为固定值 `google_local`。
2. 每次调用 API 前，在可见的对话中向用户展示完整的参数预览，包含所有文档化参数（包括未赋值的字段）。包含每个字段的当前值、文档化默认值和描述。不要将示例或允许值当作默认值。优先运行 `python3 scripts/google_local.py ... --preview-params --preview-format markdown` 解析请求后将该 Markdown 表格粘贴到对话中。
3. 展示表格后，询问用户是否需要修改参数或确认调用。用户明确确认后才能调用 API。接受的确认语句包括 `确认`、`可以`、`继续`、`调用`、`yes` 或 `go`。
4. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
5. 使用用户请求的字段加上仅有的文档化默认值构建请求参数：`engine: "google_local"`、`json: "1"`、`google_domain: "google.com"` 和 `no_cache: "false"`。省略用户未请求且没有文档化默认值的可选字段。

```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --gl us --hl en
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_local.py --params-json '{"q":"coffee shops","location":"New York","gl":"us","hl":"en"}'
```

PowerShell 可能需要转义引号：

```powershell
python3 scripts/google_local.py --params-json '{\"q\":\"coffee shops\",\"location\":\"New York\",\"gl\":\"us\",\"hl\":\"en\"}'
```

使用脚本解析自然语言请求：

```bash
python3 scripts/google_local.py --request "搜索纽约咖啡店，语言英文，地区美国，不走缓存"
```

如果用户在对话中提供了 token，使用 `--token` 传递并避免回显：

```bash
python3 scripts/google_local.py --token "USER_TOKEN" --q "coffee shops" --location "New York"
```

7. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 参数说明

使用此 skill 时，在调用 API 前展示以下简明参数列表，或运行 `python3 scripts/google_local.py --describe-params` 并转发其输出：

| Field | Required | Default | Description |
|---|---:|---|---|
| `Authorization` | yes | none | 请求头中的 Dataify API token。如果 token 不以 `Bearer ` 开头，脚本会自动添加。 |
| `engine` | yes | `google_local` | Google Local 的固定引擎值。 |
| `q` | yes | none | 搜索查询内容。 |
| `json` | yes | `1` | 输出格式。`1` = JSON，`2` = JSON+HTML，`3` = HTML，`4` = Light JSON。 |
| `google_domain` | no | `google.com` | 使用的 Google 域名。 |
| `gl` | no | none | 两位字母的 Google 国家/地区代码，如 `us`、`uk` 或 `fr`。 |
| `hl` | no | none | Google 界面/搜索语言代码，如 `en`、`es` 或 `fr`。 |
| `location` | no | none | 搜索发起的地理位置。 |
| `uule` | no | none | Google 编码位置。不要与 `location` 同时使用；如果两者都存在，优先使用明确的 `uule`。 |
| `start` | no | none | 分页结果偏移量。 |
| `ludocid` | no | none | Google 地点 CID/客户标识符。 |
| `tbs` | no | none | 常规查询字段无法表示的高级搜索参数。 |
| `no_cache` | no | `false` | `true` 跳过缓存；`false` 在可用时使用缓存结果。 |

对于实际请求，展示完整的预览而不仅仅是已赋值的请求负载：

```bash
python3 scripts/google_local.py --q "coffee shops" --location "New York" --preview-params --preview-format markdown
```

预览输出必须包含用户未提供的未设置字段，如 `gl`、`hl`、`uule`、`start`、`ludocid` 和 `tbs`。
展示预览表格后，询问：`请确认是否按以上参数调用接口，或告诉我要修改哪些字段。`

## 字段映射

需要确切的参数措辞时，请查阅 `references/google_local_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_local`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 省略用户未请求的可选字段，除非该字段有文档化的默认值。
- 仅在必填搜索查询 `q` 无法推断时才提出后续问题。
- 如果 `location` 和 `uule` 同时存在，优先使用明确的 `uule` 并省略 `location`。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 用于 Google 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- 命名的搜索起点 -> `location`
- 编码位置 -> `uule`
- 页码 N -> `start: String((N - 1) * 10)`
- Google 地点 CID -> `ludocid`
- 高级搜索过滤器 -> `tbs`
- 跳过/不使用缓存 -> `no_cache: "true"`
