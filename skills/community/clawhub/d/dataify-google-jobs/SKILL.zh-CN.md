---
name: dataify-google-jobs
description: "当用户请求“调用 Google Jobs”或“搜索职位/招聘信息并返回原始响应”，或指定职位搜索字段时，触发 dataify-google-jobs skill。"
---

# Dataify Google Jobs

使用此 skill 将用户的 Google Jobs 请求转化为 Dataify Scraper API 表单 POST。

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

1. 将用户请求解析为 Dataify Google Jobs 字段。使用 `q` 作为职位搜索查询，将 `engine` 设为固定值 `google_jobs`。
2. 根据用户提供的值加上仅有的文档化默认值构建请求参数。默认值必须来自 `references/google_jobs_api.md` 中的参数描述；切勿将示例当作默认值。
   - `engine`: 固定 `google_jobs`
   - `json`: 默认 `1`
   - `google_domain`: 默认 `google.com`
   - `no_cache`: 默认 `false`
   - 所有其他参数没有文档化默认值，除非用户提供否则必须保持未设置。
3. 每次调用 API 前，展示包含完整 body 参数列表（除 `Authorization` 外）的 Markdown 表格。表格必须恰好包含以下列：参数名、当前值、默认值、描述。询问用户是否需要修改参数。如果用户要求修改，更新值并再次展示表格。仅在用户确认表格后才调用 API。
4. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
5. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_jobs.py` 的绝对路径。

```bash
python3 scripts/google_jobs.py --q "software engineer jobs" --location "San Francisco" --gl us --hl en
```

生成确认表格：

```bash
python3 scripts/google_jobs.py --request "搜索 java 相关工作" --preview-table
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_jobs.py --params-json '{"q":"software engineer jobs","location":"San Francisco","gl":"us","hl":"en"}'
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_jobs.py --token "USER_TOKEN" --q "software engineer jobs" --location "San Francisco"
```

对于自然语言的备选方式，传递完整请求：

```bash
python3 scripts/google_jobs.py --request "搜索美国旧金山的软件工程师工作，语言英文，不使用缓存"
```

6. 将脚本输出直接返回给用户。不要对 API 响应体进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要完整的参数描述和默认值时，请查阅 `references/google_jobs_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_jobs`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 仅在必填的职位搜索查询 `q` 无法推断时才提出后续问题。
- 如果 `location` 和 `uule` 同时存在，优先使用明确的 `uule` 并省略 `location`。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。
- 不要在预览表格中包含 `Authorization`。
- 用户确认预览表格前不要调用 API。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- Google 域名 -> `google_domain`
- 用于 Google 行为的国家或地区 -> `gl`
- 界面/搜索语言 -> `hl`
- 地理搜索起点 -> `location`
- 编码的 Google 位置 -> `uule`
- 下一页 -> `next_page_token`
- Google Jobs 的 chips/过滤器 token -> `chips`
- 搜索半径（公里） -> `lrad`
- 远程办公 / 仅居家工作过滤器 -> `ltype: "1"`（当请求时）
- Google 提供的过滤字符串 -> `uds`
- 跳过缓存 -> `no_cache: "true"`
