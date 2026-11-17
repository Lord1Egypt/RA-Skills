---
name: dataify-google-images
description: "当用户请求“调用 Google Images”或“搜索 Google Images”，或明确提到图片以触发 dataify-google-images skill 时，使用此 skill。"
---

# Dataify Google Images

使用此 skill 将用户的 Google Images 请求转化为 Dataify Scraper API 表单提交。
## 工作流程

1. 将用户请求解析为 Google Images 字段。使用 `q` 作为图片搜索查询，将 `engine` 设为 `google_images`。
2. 当用户未指定某个值时，使用文档化默认值。仅使用参数描述中声明的默认值：`json=1`、`google_domain=google.com`、`start=0`、`nfpr=0`、`filter=1`、`device=desktop` 和 `no_cache=false`。不要将 `pizza`、`us`、`en`、`radius=10`、`tbm=isch`、`render_js=true` 或 `ai_overview=true` 等示例当作默认值。
3. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
4. 使用用户请求的字段加上文档化默认值构建请求参数。脚本以表单数据（而非 JSON 请求体）提交这些参数。
5. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_images.py` 的绝对路径。

```bash
python3 scripts/google_images.py --q "red sneakers" --json 1
```

对于多个字段，传递一个 JSON 对象并使用适当的 shell 引号。脚本仍然以表单数据形式提交给 API：

```bash
python3 scripts/google_images.py --params-json '{"q":"red sneakers","json":"1","google_domain":"google.com","gl":"us","hl":"en","device":"mobile"}'
```


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
