---
name: dataify-google-play
description: "当用户请求“调用 Google Play”或“应用商店搜索/排名”，或明确提到 Google Play 搜索字段时，触发 dataify-google-play skill。"
---

# Dataify Google Play

使用此 skill 将用户的 Google Play 请求转化为 Dataify Scraper API 调用。

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

1. 将用户请求解析为 Dataify Google Play 字段。使用 `q` 作为应用商店搜索查询，将 `engine` 设为 `google_play`。
2. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
3. 仅使用用户请求的字段加上必要的默认值构建请求参数。除非用户要求其他输出格式，否则使用 `json: "1"`。不要将 API 文档中的示例值当作默认值。
4. 调用 API 前，展示包含完整字段检查列表的 Markdown 表格，恰好包含以下列：`参数名`、`当前值`、`默认值`、`说明`。包含 `references/google_play_api.md` 中的每个请求字段（包含 `engine`）。然后询问用户是否需要修改参数。仅在用户确认后才调用 API。
5. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_play.py` 的绝对路径。

```bash
python3 scripts/google_play.py --q "meditation app" --gl us --hl en --json 1
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_play.py --params-json '{"q":"meditation app","gl":"us","hl":"en","json":"1"}'
```

要预览所需确认表格的规范化负载，使用 `--dry-run`：

```bash
python3 scripts/google_play.py --request "搜索美国 Google Play 上的冥想 app，英文，JSON" --dry-run
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_play.py --token "USER_TOKEN" --q "meditation app" --gl us --hl en
```

6. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值和参数值时，请查阅 `references/google_play_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_play`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 省略用户未请求的可选字段。
- 仅在必填的 `q` 无法推断且请求不是由用户提供的字段支持的类别/排行榜/设备查询时，才提出后续问题。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。
- 不要同时使用 `next_page_token`、`section_page_token`、`see_more_token` 和 `chart` 中的多个。
- 不要将 `store_device` 与 `apps_category` 或 `q` 一起使用。
- 仅当 `apps_category` 为 `FAMILY` 时才使用 `age`。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 应用搜索短语 -> `q`
- 用于 Google Play 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- Google Play 类别 -> `apps_category`
- 下一页 token -> `next_page_token`
- 板块页面 token -> `section_page_token`
- 热门排行 / 流行排名 -> `chart`
- 查看更多 token -> `see_more_token`
- 手机/平板/电视/Chromebook/手表/汽车设备浏览 -> `store_device`
- 儿童/家庭类别 -> `apps_category: "FAMILY"`
- 5 岁及以下 -> `age: "AGE_RANGE1"`
- 6 到 8 岁 -> `age: "AGE_RANGE2"`
- 9 到 12 岁 -> `age: "AGE_RANGE3"`
- 跳过缓存 -> `no_cache: "true"`
