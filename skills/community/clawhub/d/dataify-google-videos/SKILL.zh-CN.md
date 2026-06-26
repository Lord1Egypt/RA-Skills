---
name: dataify-google-videos
description: "当用户请求“调用 Google Videos”或“视频搜索”，或明确提到视频字段时，触发 dataify-google-videos skill。"
---

# Dataify Google Videos

使用此 skill 将用户的 Google Videos 请求转化为 Dataify Scraper API 表单提交。

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

1. 将用户请求解析为 Google Videos 字段。使用 `q` 作为视频搜索查询，将 `engine` 强制设为 `google_videos`。
2. 仅使用用户请求的字段加上文档化默认值构建请求参数：`json: "1"`、`google_domain: "google.com"`、`no_cache: "false"`、`nfpr: "0"` 和 `filter: "0"`。不要将 `us`、`en` 或 `true` 等示例当作默认值。
3. 每次调用 API 前，向用户展示完整的参数表格并询问是否需要修改。表格只能包含以下列：参数名、当前值、默认值、描述。包含 `references/google_videos_api.md` 中的完整字段列表，包括 `Authorization` 和 `engine`。遮蔽任何 token 值，或在无 token 时显示 `missing`。
4. 如果用户要求修改，更新参数并再次展示完整表格。仅在用户确认后调用 API。
5. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_videos.py` 的绝对路径。

预览确认表格：

```bash
python3 scripts/google_videos.py --request "search Google videos for electric cars in English" --preview-table
```

确认后调用 API：

```bash
python3 scripts/google_videos.py --q "electric cars" --hl en
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_videos.py --token "USER_TOKEN" --q "electric cars" --gl us --hl en
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号。脚本仍然以表单数据形式提交给 API：

```bash
python3 scripts/google_videos.py --params-json '{"q":"electric cars","json":"1","google_domain":"google.com","gl":"us","hl":"en","no_cache":"true"}'
```

7. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值、约束或表格描述时，请查阅 `references/google_videos_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_videos`。
- 脚本源码、表单编码和显示文本均使用 UTF-8。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 仅在必填的视频查询 `q` 无法推断时才提出后续问题。
- 如果 `uule` 存在，省略 `location`。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google 域名 -> `google_domain`
- 用于 Google 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- 命名的搜索起点 -> `location`
- Google 编码位置 -> `uule`
- 页码 N -> `start: String((N - 1) * 10)`
- 高级视频过滤器、时长、画质、来源或日期 -> `tbs`
- 跳过缓存 / 不使用缓存 -> `no_cache: "true"`
- 限制结果语言 -> `lr`，格式如 `lang_fr`
- 安全搜索开/关 -> `safe: "active"` 或 `safe: "off"`
- 排除自动纠正的查询结果 -> `nfpr: "1"`
- 包含自动纠正的查询结果 -> `nfpr: "0"`
- 禁用相似/省略结果过滤 -> `filter: "1"`
- 启用相似/省略结果过滤 -> `filter: "0"`
