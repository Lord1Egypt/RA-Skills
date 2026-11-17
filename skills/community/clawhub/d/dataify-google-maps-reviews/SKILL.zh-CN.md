---

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.

Use this skill only for reviews of a known place URL or identifier. Use Google Maps or Google Local to discover places first.
name: dataify-google-maps-reviews
description: "通过 Dataify Scraper API 采集 Google Maps 评价/评论信息。当用户请求从 Google Maps URL gather/scrape/crawl/fetch/extract/collect Google Maps review/comment information，或 Google Maps review information、comments、URL reviews 的采集/抓取/爬取/获取/提取，或表达 Google 地图评论信息采集/抓取/爬取/获取、Google 地图评论 URL 提取，或使用 spider ID google_comment_by-url 时，使用此 skill。"
---

# Dataify Google Maps Reviews 中文版

## 采集模式

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `url` | `google_comment_by-url` | `url`, `days_limit` | `[{"url":"https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu","days_limit":"20"}]` |

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则使用该 token。
- 如果未提供 token，先检查环境变量中是否已保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用。
- 如果没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
- 没有 token 不要调用 Builder 接口。

## 设置 DATAIFY_API_TOKEN

推荐使用永久环境变量，而不是只在当前终端临时设置。

Windows PowerShell，当前用户永久设置：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "your_token_here", "User")
```

然后重新打开 PowerShell。如果当前会话也要立即生效，再执行：

```powershell
$env:DATAIFY_API_TOKEN = "your_token_here"
```

macOS 或 Linux，bash 永久设置：

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

macOS 或 Linux，zsh 永久设置：

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```
## 核心工作流程

1. 从用户请求中识别采集模式。
2. 提交前，以 Markdown 表格展示必填参数、可选参数和默认值。
4. 规范化并验证最终参数值。
5. 获取 Dataify token（用户提供或已保存的 `DATAIFY_API_TOKEN`）。
6. 如果没有 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取。
7. 提交 Builder 请求创建任务。
8. 从响应中读取 `data.task_id`。
9. 提交成功后停止，告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 脚本用法

使用 Python 运行：

```bash
python3 scripts/google_maps_reviews.py --help
```

## 注意事项

- 提交成功后不要下载结果文件，告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看。
- 如果用户已经提供了部分参数，在表格中显示这些值，只询问是否修改剩余参数。

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
