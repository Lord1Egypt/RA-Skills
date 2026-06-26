---
name: dataify-google-images
description: "当用户请求“调用 Google Images”或“搜索 Google Images”，或明确提到图片以触发 dataify-google-images skill 时，使用此 skill。"
---

# Dataify Google Images

使用此 skill 将用户的 Google Images 请求转化为 Dataify Scraper API 表单提交。

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

1. 将用户请求解析为 Google Images 字段。使用 `q` 作为图片搜索查询，将 `engine` 设为 `google_images`。
2. 当用户未指定某个值时，使用文档化默认值。仅使用参数描述中声明的默认值：`json=1`、`google_domain=google.com`、`start=0`、`nfpr=0`、`filter=1`、`device=desktop` 和 `no_cache=false`。不要将 `pizza`、`us`、`en`、`radius=10`、`tbm=isch`、`render_js=true` 或 `ai_overview=true` 等示例当作默认值。
3. 在任何 API 调用前，向用户展示包含完整请求字段列表（除 `Authorization` 外）的 Markdown 表格。表格必须恰好包含以下列：`参数名`、`当前值`、`默认值`、`说明`。包含 `engine` 和每个 body 字段，即使当前值未设置。尽可能使用内置脚本生成表格：

```bash
python3 scripts/google_images.py --params-table --q "red sneakers" --json 1
```

4. 展示表格后，询问用户是否需要修改参数。用户明确确认后才能调用 API。如果用户修改了参数，重新生成表格并再次询问。
5. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
6. 使用用户请求的字段加上文档化默认值构建请求参数。脚本以表单数据（而非 JSON 请求体）提交这些参数。
7. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_images.py` 的绝对路径。

```bash
python3 scripts/google_images.py --q "red sneakers" --json 1
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_images.py --token "USER_TOKEN" --q "red sneakers" --gl us --hl en
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号。脚本仍然以表单数据形式提交给 API：

```bash
python3 scripts/google_images.py --params-json '{"q":"red sneakers","json":"1","google_domain":"google.com","gl":"us","hl":"en","device":"mobile"}'
```

8. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值、约束或示例时，请查阅 `references/google_images_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_images`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 当用户未请求某个值时，包含文档化默认值。仅当可选字段没有文档化默认值且用户未请求时才省略。
- 仅在必填的图片查询 `q` 无法推断时才提出后续问题。
- 如果 `uule` 存在，省略 `location`、`lat`、`lon` 和 `radius`。
- 如果 `location` 存在，省略 `uule`、`lat` 和 `lon`。
- `lat` 和 `lon` 需成对使用。如果只有一个可用，询问缺失的坐标。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google 域名 -> `google_domain`
- 用于 Google 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- 限制结果的国家 -> `cr`，格式如 `countryFR`
- 限制结果语言 -> `lr`，格式如 `lang_fr`
- 命名的搜索起点 -> `location`
- Google 编码位置 -> `uule`
- GPS 坐标 -> `lat` 和 `lon`
- 位置偏移半径（米） -> `radius`
- 页码 N -> `start: String((N - 1) * 10)`
- 高级图片过滤器、尺寸、颜色、类型、版权或日期 -> `tbs`
- 安全搜索开/关 -> `safe: "active"` 或 `safe: "off"`
- 桌面/平板/手机 -> `device`
- 渲染 JavaScript -> `render_js: "true"`
- 跳过缓存 -> `no_cache: "true"`
- 包含 AI 概览 -> `ai_overview: "true"`
