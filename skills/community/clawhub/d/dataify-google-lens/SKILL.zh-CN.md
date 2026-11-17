---
name: dataify-google-lens
description: "当用户请求“调用 Google Lens”或“按图搜索”时，触发 dataify-google-lens skill。"
---

# Dataify Google Lens

使用此 skill 将用户的 Google Lens 或反向图片搜索请求转化为 Dataify Scraper API 表单提交。
## 工作流程

1. 将用户请求解析为 Google Lens 字段。使用 `url` 作为图片 URL，将 `engine` 设为 `google_lens`，仅在用户要求时推断可选字段。
2. 根据用户的请求构建请求参数。如果用户未指定某个字段，仅使用参数描述中的文档化默认值：
   - `engine`: `google_lens`
   - `json`: `1`
   - `type`: `all`
   - `no_cache`: `false`
   没有文档化默认值的字段保持未设置。不要将 `us`、`en`、`active` 或 `true` 等示例当作默认值。

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us --preview
```

询问用户：`请确认是否需要修改这些参数；确认无误后我再调用接口。`

5. 如果 token 缺失，停止操作并提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 登录以获取 `DATAIFY_API_TOKEN`。
6. 使用 `python3` 运行内置 Python 脚本。从此 skill 目录运行，或使用 `scripts/google_lens.py` 的绝对路径。脚本以表单数据形式提交到硬编码的 API 端点；不会发送 JSON body。

```bash
python3 scripts/google_lens.py --url "https://example.com/image.jpg" --json 1 --type all --country us
```

需要时可使用自然语言备选方式：

```bash
python3 scripts/google_lens.py --request "Search Google Lens for https://example.com/image.jpg, products, country US, safe on, no cache"
```


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
