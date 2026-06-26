---
name: dataify-google-patents
description: "当用户请求“调用 Google Patents”或“专利搜索”，或明确提到专利搜索字段时，触发 dataify-google-patents skill。"
---

# Dataify Google Patents

使用此 skill 将用户的 Google Patents 请求转化为 Dataify Scraper API 调用。

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

1. 将用户请求解析为 Dataify Google Patents 字段。始终将 `engine` 设为 `google_patents`。
2. 仅使用参数描述中明确声明的默认值：
   - `json: "1"`
   - `page: "0"`
   - `dups: "family"`
   - `patents: "true"`
   - `scholar: "false"`
   - `no_cache: "false"`
   - `sort` 默认为相关性排序（省略该字段）。
3. 不要将示例值当作默认值。省略没有文档化默认值且用户未请求的可选字段。
4. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
5. 每次调用 API 前，使用 `python3` 运行内置 Python 脚本并加上 `--print-table` 生成完整的参数审查表格：

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents" --print-table
```

向用户展示表格，恰好包含以下列：参数名、当前值、默认值、描述。询问是否需要修改参数。用户确认前不要调用 API。

6. 如果用户修改了参数，使用显式标志或 `--params-json` 传递编辑后的值，再次展示表格并请求确认。
7. 确认后，调用脚本时不加 `--print-table`：

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents"
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_patents.py --params-json '{"q":"battery recycling","status":"GRANT","country":"US","json":"1"}'
```

如果用户在对话中提供了 token 而非环境变量，使用 `--token` 传递并避免在最终回答中回显：

```bash
python3 scripts/google_patents.py --token "USER_TOKEN" --q "battery recycling"
```

8. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

## 字段映射

需要确切的字段列表、默认值、允许值和映射提示时，请查阅 `references/google_patents_api.md`。

核心规则：

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 以表单数据形式提交 API 请求。
- 始终使用 UTF-8 编码。
- 始终将 `engine` 强制设为 `google_patents`；忽略用户提供的任何冲突引擎值。
- 保持请求值为字符串类型，除非脚本接受并规范化布尔值。
- 当无法推断出有意义的搜索查询或过滤条件时才提出后续问题。
- 在脚本中规范化 token 值。不带 `Bearer ` 的 token 会被自动添加前缀。
- 不要在参数审查表格中暴露完整的 token。

常用映射：

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- 第一页 -> `page: "0"`，第二页 -> `page: "1"`
- 最新/最近 -> `sort: "new"`
- 最旧/最早 -> `sort: "old"`
- 相关性/默认相关性 -> 省略 `sort`
- 分组/聚类结果 -> `clustered: "true"`
- 专利族去重 -> `dups: "family"`
- 出版物去重 -> `dups: "language"`
- 包含专利结果 -> `patents: "true"`
- 包含 Google Scholar 结果 -> `scholar: "true"`
- 之前/之后日期 -> `before` 或 `after`，格式为 `priority:YYYYMMDD`、`filing:YYYYMMDD` 或 `publication:YYYYMMDD`
- 发明人姓名 -> `inventor`
- 受让人、申请人或所有人名称 -> `assignee`
- 国家/地区专利代码 -> `country`
- 结果语言过滤 -> `language`
- 已授权专利 -> `status: "GRANT"`
- 申请 -> `status: "APPLICATION"`
- 专利类型 -> `type: "PATENT"`
- 外观设计类型 -> `type: "DESIGN"`
- 涉诉是/否 -> `litigation: "YES"` 或 `litigation: "NO"`
- 跳过缓存 -> `no_cache: "true"`
