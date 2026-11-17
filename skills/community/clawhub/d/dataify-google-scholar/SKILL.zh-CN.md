---
name: dataify-google-scholar
description: "当用户请求“调用 Google Scholar”或“学术搜索/论文搜索”，或明确提到学术搜索字段时，触发 dataify-google-scholar skill。"
---

# Dataify Google Scholar

使用此 skill 将用户的 Google Scholar 请求转化为 Dataify Scraper API 调用。
## 工作流程

1. 将用户请求解析为 Dataify Google Scholar 字段。始终将 `engine` 设为 `google_scholar`。
2. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
3. 根据用户的请求加上文档化默认值构建请求参数。默认值必须仅来自 `references/google_scholar_api.md` 中的参数描述；切勿将示例值当作默认值。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_scholar.py` 的绝对路径。

按需预览高级参数：

```bash
python3 scripts/google_scholar.py --request "搜索 large language model，2020 到 2024，返回 20 条" --preview
```


```bash
python3 scripts/google_scholar.py --q "large language model" --as_ylo 2020 --as_yhi 2024 --num 20
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_scholar.py --params-json '{"q":"large language model","as_ylo":"2020","as_yhi":"2024","num":"20"}'
```


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
