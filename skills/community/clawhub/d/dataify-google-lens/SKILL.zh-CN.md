---
name: dataify-google-lens
description: "当用户请求“调用 Google Lens”或“按图搜索”时，触发 dataify-google-lens skill。"
---

# Dataify Google Lens

使用此 skill 将用户的 Google Lens 或反向图片搜索请求转化为 Dataify Scraper API 表单提交。

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

1. 将用户请求解析为 Google Lens 字段。使用 `url` 作为图片 URL，将 `engine` 设为 `google_lens`，仅在用户要求时推断可选字段。
2. 根据用户的请求构建请求参数。如果用户未指定某个字段，仅使用参数描述中的文档化默认值：
   - `engine`: `google_lens`
   - `json`: `1`
   - `type`: `all`
   - `no_cache`: `false`
   没有文档化默认值的字段保持未设置。不要将 `us`、`en`、`active` 或 `true` 等示例当作默认值。
3. 每次调用 API 前，展示完整的请求参数表格并询问用户是否需要修改。不要在表格中包含 `Authorization`。使用内置脚本的预览模式，然后直接展示其 Markdown 表格：

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us --preview
```

询问用户：`请确认是否需要修改这些参数；确认无误后我再调用接口。`

4. 如果用户修改了参数，更新值并再次展示预览表格。用户确认前不要调用 API。
5. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_lens.py` 的绝对路径。脚本以表单数据形式提交到硬编码的 API 端点；不会发送 JSON body。

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us
```

需要时可使用自然语言备选方式：

```bash
python3 scripts/google_lens.py --request "Search Google Lens for https://example.com/image.jpg, products, country US, safe on, no cache"
```

7. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值、约束或示例时，请查阅 `references/google_lens_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终使用 UTF-8 编码请求数据。
- 始终将 `engine` 强制设为 `google_lens`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 当用户未指定某个值时使用文档化默认值。省略没有文档化默认值且未被请求的字段。
- 仅在必填的图片 `url` 无法从用户请求中推断时才提出后续问题。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。
- 切勿在预览表格中包含 `Authorization`，也不要在最终说明中打印 token 值。

常用映射：

- 图片 URL、图片地址、反向图片搜索目标 -> `url`
- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 界面/搜索语言 -> `hl`
- 用于 Lens 行为的国家或地区 -> `country`
- 所有结果 -> `type: "all"`
- 商品结果 -> `type: "products"`
- 关于此图片 -> `type: "about_this_image"`
- 精确匹配 -> `type: "exact_matches"`
- 视觉匹配或相似图片 -> `type: "visual_matches"`
- 额外查询/关键词/与 `all`、`visual_matches` 或 `products` 一起使用的细化词 -> `q`
- 安全搜索开/关 -> `safe: "active"` 或 `safe: "off"`
- 跳过缓存 -> `no_cache: "true"`
