---
name: "dataify-web-unlocker"
description: "依托Dataify网页解锁API抓取受限网页，输入任意URL即可智能识别破解验证码、全自动JS页面渲染，支持返回完整网页HTML源码或PNG全屏截图，适配动态网页、SPA单页应用等各类高难度数据采集场景。"
---

# Dataify Web Unlocker 中文版

这个 skill 用于通过 Dataify Web Unlocker API 抓取或解锁网页内容。

## 工作流程

1. 在 macOS/Linux 或强调跨平台时，优先使用 `scripts/invoke-dataify-web-unlocker.py`。
2. 在 Windows 下可使用 `scripts/invoke-dataify-web-unlocker.ps1`。
3. 只有当用户明确要求原始请求时，才使用 `curl` 命令。
4. `url` 是唯一必须先确认的参数；如果用户没有明确给出目标地址，不要猜。
5. 其余参数都视为可选覆盖项；除非用户明确要求，否则保持默认值。
6. 脚本会从环境变量中读取 `DATAIFY_API_TOKEN`。
7. 如果缺少 token，提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 获取 `DATAIFY_API_TOKEN`。
8. 除非用户要求额外处理，否则直接返回接口响应内容。

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

## 默认请求体

除非用户明确要求不同取值，否则使用以下默认值。真正发起请求前，只必须先拿到 `url`：

```json
{
  "url": "https://www.google.com",
  "type": "html",
  "js_render": "True",
  "block_resources": "",
  "clean_content": "",
  "country": "us",
  "headers": "",
  "cookies": "",
  "wait": "",
  "wait_for": "",
  "follow_redirect": "True",
  "isjson": "1"
}
```

## 常用命令

如果用户没提供 URL，先询问 URL。最小调用只传 `url`，其他参数走默认值。

Python：

```bash
python scripts/invoke-dataify-web-unlocker.py --url "https://www.google.com"
```

PowerShell：

```powershell
& ".\scripts\invoke-dataify-web-unlocker.ps1" -Url "https://www.google.com"
```

Python 覆盖参数示例：

```bash
python scripts/invoke-dataify-web-unlocker.py \
  --url "https://example.com" \
  --js-render "True" \
  --country "us" \
  --wait "3000" \
  --wait-for ".main-content"
```

PowerShell 覆盖参数示例：

```powershell
& ".\scripts\invoke-dataify-web-unlocker.ps1" `
  -Url "https://example.com" `
  -JsRender "True" `
  -Country "us" `
  -Wait "3000" `
  -WaitFor ".main-content"
```

只预览请求而不实际发起网络调用：

```bash
python scripts/invoke-dataify-web-unlocker.py --url "https://example.com" --dry-run
```

```powershell
& ".\scripts\invoke-dataify-web-unlocker.ps1" -Url "https://example.com" -DryRun
```

## 原始 curl 回退方式

如果用户明确要求原始请求，在 PowerShell 中请使用 `curl.exe`，避免命中 PowerShell 的 `curl` 别名。

先检查 token：

```powershell
if (-not $env:DATAIFY_API_TOKEN) {
  Write-Error "DATAIFY_API_TOKEN is not set. Sign in at https://dashboard.dataify.com?utm_source=skill to obtain it."
  exit 1
}
```

然后发起请求：

```powershell
curl.exe -X POST "https://webunlocker.dataify.com/request" `
  -H "Authorization: Bearer $env:DATAIFY_API_TOKEN" `
  -H "Content-Type: application/json" `
  -d "{\"url\":\"https://www.google.com\",\"type\":\"html\",\"js_render\":\"True\",\"block_resources\":\"\",\"clean_content\":\"\",\"country\":\"us\",\"headers\":\"\",\"cookies\":\"\",\"wait\":\"\",\"wait_for\":\"\",\"follow_redirect\":\"True\",\"isjson\":\"1\"}"
```

## 参数说明

- `url` 是唯一必须从用户处确认的参数。
- 如果 `url` 缺失或有歧义，必须先向用户确认。
- `headers` 和 `cookies` 会按字符串原样传给接口。
- 类似 `"True"` 这类布尔值风格字段，保持字符串形式。
- 除非用户明确要求其他模式，否则 `isjson` 保持 `"1"`。
- 除非用户明确要求，否则不要擅自增加 headers、cookies、wait、render 设置或 country 覆盖值。
- Python 版本仅使用标准库，因此更适合跨平台使用。

## 参数交互策略

- 当请求意图明确、只读、低风险且成本较低时，使用安全默认值直接执行。可以用一句话说明执行内容，但不要暂停等待确认。
- 只在缺少必填输入、存在会明显改变结果的歧义、大批量或多页采集、媒体下载、会明显增加积分消耗、不可逆操作，或用户明确要求查看参数时询问。
- 必须确认时，只展示会影响目标、范围、输出或成本的用户参数。优先使用一句简短说明；只有三个及以上关键值确实需要比较时才使用精简表格。
- 不要展示固定字段、空的可选字段、未修改的默认值、凭据或内部实现参数，例如引擎选择、响应格式开关、偏移量、spider ID 和文件名模板。
- 默认隐藏高级筛选项，除非用户主动询问或需要它们消除歧义。不得用文档示例值代替用户缺失的必填输入。
- 先返回首个结果，再提供相关的细化选项，不要在首次执行前强迫用户决定所有可选项。

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
