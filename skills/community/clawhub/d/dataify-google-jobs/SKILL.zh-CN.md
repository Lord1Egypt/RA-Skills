---
name: dataify-google-jobs
description: "当用户请求“调用 Google Jobs”或“搜索职位/招聘信息并返回原始响应”，或指定职位搜索字段时，触发 dataify-google-jobs skill。"
---

# Dataify Google Jobs

使用此 skill 将用户的 Google Jobs 请求转化为 Dataify Scraper API 表单 POST。
## 工作流程

1. 将用户请求解析为 Dataify Google Jobs 字段。使用 `q` 作为职位搜索查询，将 `engine` 设为固定值 `google_jobs`。
2. 根据用户提供的值加上仅有的文档化默认值构建请求参数。默认值必须来自 `references/google_jobs_api.md` 中的参数描述；切勿将示例当作默认值。
   - `engine`: 固定 `google_jobs`
   - `json`: 默认 `1`
   - `google_domain`: 默认 `google.com`
   - `no_cache`: 默认 `false`
   - 所有其他参数没有文档化默认值，除非用户提供否则必须保持未设置。
4. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
5. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_jobs.py` 的绝对路径。

```bash
python3 scripts/google_jobs.py --q "software engineer jobs" --location "San Francisco" --gl us --hl en
```


```bash
python3 scripts/google_jobs.py --request "搜索 java 相关工作" --preview-table
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号：

```bash
python3 scripts/google_jobs.py --params-json '{"q":"software engineer jobs","location":"San Francisco","gl":"us","hl":"en"}'
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
