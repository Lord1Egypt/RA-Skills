---
name: dataify-google-patents
description: "当用户请求“调用 Google Patents”或“专利搜索”，或明确提到专利搜索字段时，触发 dataify-google-patents skill。"
---

# Dataify Google Patents

使用此 skill 将用户的 Google Patents 请求转化为 Dataify Scraper API 调用。
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

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents" --print-table
```


6. 如果用户修改了参数，使用显式标志或 `--params-json` 传递编辑后的值，再次展示表格并请求确认。
7. 确认后，调用脚本时不加 `--print-table`：

```bash
python3 scripts/google_patents.py --request "search Google Patents for battery recycling patents"
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_patents.py --params-json '{"q":"battery recycling","status":"GRANT","country":"US","json":"1"}'
```


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
