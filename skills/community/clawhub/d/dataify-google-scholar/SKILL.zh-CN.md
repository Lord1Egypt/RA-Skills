---
name: dataify-google-scholar
description: "当用户请求“调用 Google Scholar”或“学术搜索/论文搜索”，或明确提到学术搜索字段时，触发 dataify-google-scholar skill。"
---

# Dataify Google Scholar

使用此 skill 将用户的 Google Scholar 请求转化为 Dataify Scraper API 调用。

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

1. 将用户请求解析为 Dataify Google Scholar 字段。始终将 `engine` 设为 `google_scholar`。
2. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
3. 根据用户的请求加上文档化默认值构建请求参数。默认值必须仅来自 `references/google_scholar_api.md` 中的参数描述；切勿将示例值当作默认值。
4. 调用 API 前，向用户展示包含完整字段列表（除 `Authorization` 外）的 Markdown 表格。表格只能包含以下列：`参数名`、`当前值`、`默认值`、`说明`。
5. 询问用户是否需要修改参数。仅在用户确认后才调用 API。如果用户修改了值，在调用前更新表格或请求负载。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_scholar.py` 的绝对路径。

预览完整的参数表格：

```bash
python3 scripts/google_scholar.py --request "搜索 large language model，2020 到 2024，返回 20 条" --preview
```

用户确认后调用 API：

```bash
python3 scripts/google_scholar.py --q "large language model" --as_ylo 2020 --as_yhi 2024 --num 20
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_scholar.py --params-json '{"q":"large language model","as_ylo":"2020","as_yhi":"2024","num":"20"}'
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_scholar.py --token "USER_TOKEN" --q "large language model"
```

7. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值或允许值时，请查阅 `references/google_scholar_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终将 `engine` 强制设为 `google_scholar`。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 当用户未指定某个字段时，包含文档化默认值。
- 省略没有文档化默认值且无用户值的可选字段。
- 仅在无法推断出可用搜索条件时才提出后续问题。可用搜索条件为 `q`、`cites` 或 `cluster`。
- 不要将 `cluster` 与 `q` 或 `cites` 组合使用；`cluster` 必须单独使用。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 界面/搜索语言 -> `hl`
- 限制结果语言 -> `lr`，格式如 `lang_fr` 或 `lang_fr|lang_de`
- 页码 N -> `start: String((N - 1) * 10)`
- 结果数量 -> `num`，范围 `1` 到 `20`
- 引用搜索 -> `cites`
- 所有版本搜索 -> `cluster`
- 年份范围下限 -> `as_ylo`
- 年份范围上限 -> `as_yhi`
- 最近/日期排序 -> `scisbd: "1"`（仅摘要）或 `scisbd: "2"`（全部内容）
- 包含专利 -> `as_sdt: "7"`
- 排除专利 -> `as_sdt: "0"`
- 美国判例法 -> `as_sdt: "4"`
- 安全搜索开/关 -> `safe: "active"` 或 `safe: "off"`
- 禁用相似/省略结果过滤 -> `filter: "0"`
- 排除引用 -> `as_vis: "1"`
- 包含引用 -> `as_vis: "0"`
- 仅综述文章 -> `as_rr: "1"`
- 跳过缓存 -> `no_cache: "true"`
