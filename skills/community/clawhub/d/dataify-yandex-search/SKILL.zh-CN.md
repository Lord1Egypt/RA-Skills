---
name: dataify-yandex-search
description: "当用户想搜索 Yandex 时，使用此 skill。"
---

# Dataify Yandex Search

## 工作流程

1. 读取用户的请求并将其映射到以下 API 字段。
2. 仅从参数描述中获取默认值。不要将示例 YAML body 作为默认值来源。

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

5. 如果用户要求修改，调整参数，再次展示完整的预览表格并请求确认。
6. 确认后，检查 token。如果用户未提供 token 且 `DATAIFY_API_TOKEN` 不可用，停止操作并要求用户提供 Dataify API token 或前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 注册。
7. 使用已确认的参数调用 API：

```bash
```

8. 将脚本的标准输出直接返回给用户。不要对 API 响应进行解析、总结、翻译、过滤、重新格式化或其他处理。

## 预览表格


- `参数名`
- `当前值`
- `默认值`
- `说明`

内置脚本通过以下方式生成此表格：

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

## 默认值

当用户未指定某个字段时，使用以下文档化默认值：

- `engine`: `yandex`
- `json`: `1`
- `yandex_domain`: `yandex.com`
- `lang`: 当 `yandex_domain` 为 `yandex.com` 时为 `en`
- `family_mode`: `1`
- `fix_typo`: `true`
- `groups_on_page`: `20`
- `no_cache`: `false`

无文档化默认值：

- `text`: 必须从用户请求中获取。
- `lr`: 除非用户指定，否则留空。
- `p`: 除非用户指定，否则留空；指定时页码从 `0` 开始。

来自 API 示例 body 的重要修正：

- 不要将示例中的 `family_mode: "0"` 当作默认值。描述中的默认值为中等，因此使用 `1`。
- 不要将示例中的 `no_cache: "true"` 当作默认值。描述中说明 `false` 是默认值。

## 字段映射

- `--json`: 输出格式。使用 `1` JSON，`2` JSON+HTML，`3` HTML，或 `4` Light JSON。
- `--yandex-domain`: Yandex 域名，如 `yandex.com`、`yandex.ru`、`ya.ru`、`yandex.kz`、`yandex.com.tr` 或其他支持的域名。
- `--lang`: 搜索语言，例如 `en`、`ru`、`tr`。
- `--lr`: 国家或地区 ID。
- `--p`: 页码，从 `0` 开始。
- `--family-mode`: 安全搜索模式。使用 `0` 关闭，`1` 中等，`2` 严格。
- `--fix-typo`: `true` 或 `false`。
- `--groups-on-page`: 每页最大结果组数。
- `--no-cache`: `true` 跳过缓存，`false` 使用缓存。
- `--params-json`: 用于非常规请求的原始字段覆盖 JSON 对象。使用 `null` 省略已有默认值的字段。


## 示例

预览普通搜索的参数：

```bash
python3 scripts/yandex_search.py --text "OpenAI latest news" --preview
```


```bash
```

预览俄语 Yandex、第 2 页、HTML 输出：

```bash
python3 scripts/yandex_search.py --text "artificial intelligence news" --yandex-domain yandex.ru --lang ru --p 1 --json 3 --preview
```

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
