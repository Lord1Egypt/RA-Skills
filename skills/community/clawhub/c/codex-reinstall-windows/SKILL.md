---
name: openclaw-codex-reinstall
description: 在 Windows/WorkBuddy 沙箱环境下干净卸载并重装 OpenClaw 与 Codex（含 Codex 桌面版 AppX、Codex CLI、OpenClaw CLI、OpenClaw Windows Hub、WSL OpenClawGateway 发行版），以及重装后重新接入第三方模型（DeepSeek）而无需 OpenAI 账号。触发词：卸载重装 openclaw、卸载 codex、重装 openclaw、openclaw 装不上、codex 重装、清理 openclaw 残留、OpenClawGateway WSL 问题、codex 登录不了、openai 登录不了怎么用、codex 怎么接入 deepseek、codex 需要登录吗、codex 桌面版报 model name 错误、supported API model names、gpt-5.6-sol、Model metadata not found、codex 桌面版切换模型、codex 中文界面、codex 中文回复。
agent_created: true
---

# OpenClaw / Codex 卸载重装（Windows）

## 适用场景

用户要求"把 openclaw/codex 全部卸载删除再重装"，或 OpenClaw 反复安装失败需要排查。

## 第 0 步：先做只读扫描（禁止直接删）

必查清单（任一处缺失都可能漏删）：

```bash
# PATH 与命令行
which codex openclaw
# npm 全局（注意：托管 npm 与系统 npm 的 prefix 不同！）
ls ~/AppData/Roaming/npm/node_modules/
# 用户配置目录
ls -d ~/.codex ~/.openclaw
# AppData 各分支
ls -d ~/AppData/Local/OpenClaw* ~/AppData/Local/Codex \
      ~/AppData/Roaming/OpenClaw* ~/AppData/Roaming/Codex \
      ~/.cache/codex-runtimes
# 开始菜单 / 自启动
ls "~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/" | grep -iE "claw|codex"
```

用 PowerShell 工具查注册表与 AppX（**输出必须 Out-File 到临时文件再 Read**，
此环境不回传 stdout）：

```powershell
Get-AppxPackage | Where-Object { $_.Name -match 'codex|claw' }
Get-ItemProperty @('HKCU:\...\Uninstall\*','HKLM:\...\Uninstall\*','HKLM:\...\WOW6432Node\...\Uninstall\*') |
  Where-Object { $_.DisplayName -match 'codex|claw' } |
  Select-Object DisplayName,InstallLocation,UninstallString,QuietUninstallString
Get-ScheduledTask | Where-Object { $_.TaskName -match 'codex|claw' }
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
```

**WSL 别忘查**：`wsl.exe` 在本机被安全策略禁用（Program Blacklist）。
改看 `%LOCALAPPDATA%\OpenClawTray\wsl-keepalive\OpenClawGateway.json`，
其中 `DistroName` 就是网关发行版名。

## 第 1 步：卸载

```powershell
# Codex 桌面版（AppX，当前用户级，无需管理员）
Get-AppxPackage -Name OpenAI.Codex | Remove-AppxPackage

# OpenClaw Companion（Inno Setup 卸载器，静默）
& "$env:LOCALAPPDATA\OpenClawTray\unins000.exe" /VERYSILENT /NORESTART /SUPPRESSMSGBOXES
```

- Codex CLI 用 `npm uninstall -g` **在本机可能不生效**，直接删
  `AppData\Roaming\npm\node_modules\@openai` + `codex`/`codex.cmd`/`codex.ps1` 更可靠。
- Companion 卸载后会残留少量文件，属正常；但若日志出现
  `已添加项。字典中的关键字:"https_proxy"所添加的关键字:"HTTPS_PROXY"`
  → 说明"本地网关清理"失败，WSL 发行版没被清（见第 4 步）。

## 第 2 步：删除残留（回收站在本环境不可用）

沙箱禁用 `Add-Type` / `Reflection.Assembly` / COM `WScript.Shell` → **调不到回收站**。
不要用 `rm -rf` 砸个人目录。改用**移动到隔离备份文件夹**（同盘 Move-Item 是秒级重命名）：

```powershell
$bak = "$env:USERPROFILE\_卸载备份_$(Get-Date -f yyyy-MM-dd)"
New-Item -ItemType Directory -Path $bak -Force | Out-Null
Move-Item -LiteralPath "<源目录>" -Destination (Join-Path $bak "<别名>") -Force
```

需移入的清单：`.codex`、`AppData\Roaming\Codex`、`AppData\Local\Codex`、
`.cache\codex-runtimes`、`AppData\Local\OpenClawTray`、`AppData\Roaming\OpenClawTray`、
`AppData\Local\OpenClawPortable`、开始菜单内的相关文件夹、Temp 下的残留。
自启动项：`Remove-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -Name OpenClawTray`

## 第 3 步：重装

### Codex 桌面版
用户一般已有本地 msix（如桌面上的 `Codex-windows-x64-latest.msix`）：
```powershell
Add-AppxPackage -Path "$env:USERPROFILE\Desktop\Codex-windows-x64-latest.msix"
```
⚠️ 文件名里的 "latest" **不代表版本新**，装完务必 `Get-AppxPackage -Name OpenAI.Codex`
比对版本号，若比原来旧需提示用户走应用内更新。

### Codex CLI / OpenClaw CLI（关键：绕开三个坑）
```bash
export PATH="/c/Program Files/nodejs:$PATH"          # 坑1：系统 Node 24 必须在托管 Node 22 之前
export APPDATA="$HOME\\AppData\\Roaming"
npm install -g --prefix "$HOME/AppData/Roaming/npm" --no-audit --no-fund \
  @openai/codex
npm install -g --prefix "$HOME/AppData/Roaming/npm" --no-audit --no-fund \
  --allow-scripts=openclaw,@google/genai,koffi,tree-sitter-bash,protobufjs \
  openclaw
```

三个坑：
1. **Node 版本**：`openclaw@2026.9.4` 要求 `>=24.16.0 <25 || >=26.1.0`，
   PATH 前面的托管 Node 22 会让 preinstall 直接拒绝。
2. **npm 11 拦截安装脚本**：不加 `--allow-scripts` 时 openclaw 的 postinstall 不跑，
   内置插件缺失。
3. **`npm prefix -g` 在 Git Bash 下解析不出 `${APPDATA}`**，必须显式 `--prefix`。

验证：`openclaw.cmd --version` 应输出如 `OpenClaw 2026.9.4 (3a9d69d)`。

### OpenClaw Windows Hub（托盘程序）
只在 GitHub Releases 发布，且本环境 `github.com` 与常见镜像**全部不可达**。
本环境可达的下载源：`api.github.com`（查元数据）、`registry.npmjs.org`、
`registry.npmmirror.com`、`openclaw.ai`。

→ 从 api 拿到 exe 的 `size` 与 `digest.sha256`，让**用户在浏览器**下载并校验：
```
https://github.com/openclaw/openclaw-windows-node/releases/latest/download/OpenClawCompanion-Setup-x64.exe
```
（仓库是 `openclaw/openclaw-windows-node`，不是 `openclaw/openclaw`。后者只有 macOS/Linux 包。）

## 第 4 步：WSL 网关

Windows Hub 首次启动选「本地设置」会自动新建一个应用独占的 `OpenClawGateway`
WSL 发行版并配对。但**旧发行版要先注销**，否则可能复用坏掉的状态：

```powershell
wsl --list --verbose
wsl --unregister OpenClawGateway     # 不可恢复；只注销这一个，别碰用户的 Ubuntu
```

`wsl.exe` 被本机安全策略禁用时，这部分命令只能交给用户手动执行。

## 第 5 步：验证清单

- `Get-AppxPackage -Name OpenAI.Codex` 有输出
- `codex.cmd --version` → `codex-cli 0.154.0`
- `openclaw.cmd --version` → `OpenClaw 2026.9.4`
- 7 个残留目录 `Test-Path` 全为 False
- HKCU Run 里无 `OpenClawTray`
- 重装后程序会自动重新生成 `~/.codex`（正常），但 `auth.json` 不会回来 → 见第 6 步

## 第 6 步：重装后重新接入模型（**不需要 OpenAI 账号**）

用户常问"OpenAI 网站登录不了，Codex 还能用吗"。答案：**能，且不需要登录 OpenAI**。
Codex 支持自定义 model provider，第三方 API（DeepSeek 等）与 ChatGPT 登录是两条平行路径。

⚠️ 关键：重装后程序会**自动重写 `~/.codex/config.toml`**（写入 plugins / mcp_servers /
marketplaces 等桌面版配置），把用户原有的自定义 provider 配置冲掉。所以必须**手工回填**。

### 回填方法（注意 TOML 语法陷阱）

顶层键必须放在**第一个 `[table]` 之前**；`[model_providers.xxx]` 是 table，
只能放在已有的顶层键（如 `notify = [...]`）**之后**。顺序写错会让 `notify` 被吞进
model_providers 表里，破坏原有语义。

```toml
# 插在文件最顶部（notify 之前）
model_provider = "custom"
model = "deepseek-flash"
model_reasoning_effort = "high"
model_catalog_json = "C:/Users/<你的用户名>/.codex/model-catalogs/custom-catalog.json"   # 必须写成绝对路径
disable_response_storage = true
cli_auth_credentials_store = "file"

notify = [ ... ]          # 原有的顶层键，必须留在顶层

# 插在 notify 之后、[marketplaces...] 之前
[model_providers.custom]
name = "deepseek"
base_url = "https://api.deepseek.com"
wire_api = "responses"
requires_openai_auth = true
```

同时写 `~/.codex/auth.json`：

```json
{ "OPENAI_API_KEY": "sk-..." }
```

改前先备份：`cp ~/.codex/config.toml <工作区>/备份/config.toml.重装后原始备份`

### 上线前先验证 API 侧（curl 直连，比改配置快）

```bash
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $KEY" \
  https://api.deepseek.com/v1/models
# Responses 接口是否支持（决定 wire_api 取值）
curl -s -X POST https://api.deepseek.com/v1/responses \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","input":"say OK"}'
# 注意：curl -o 在本沙箱写 Temp 目录会静默失败，直接打到 stdout 更可靠
```

模型名以 `/v1/models` 实际返回为准，不要照抄旧配置（DeepSeek 的
`deepseek-v4-flash` 会被服务端映射为 `deepseek-flash`）。

### 验证

```bash
export PATH="/c/Program Files/nodejs:$PATH"
codex.cmd login status            # → Logged in using an API key - sk-***
codex.cmd exec --skip-git-repo-check "只回答两个字：成功"
```

退出码 0 且 model/provider 显示为 `deepseek-flash` / `custom` 即通。

### 根治 `Model metadata not found` + 桌面版模型名报错

**症状**：桌面版能连上第三方 API，但一提问就回
`The supported API model names are deepseek-flash, deepseek-v4-pro, but you passed gpt-5.6-sol.`

**两个根因**（缺一不可）：

1. **桌面版有自己的模型选择器**，它把选中的 OpenAI 模型名（如 `gpt-5.6-sol`）
   **写回 `config.toml` 的 `model`**，覆盖手工配置；提交请求时也带这个名字。
   选择器只认 Codex 内置模型目录里的名字 → 第三方模型不在其中。
2. 内置目录没有第三方模型的元数据 → 触发 `Model metadata not found` 警告。

**解法：用 `model_catalog_json` 给第三方模型补元数据（官方支持）**

```toml
model_catalog_json = "C:/Users/<你的用户名>/.codex/model-catalogs/custom-catalog.json"   # 必须写成绝对路径
```

目录文件结构（顶层必须是 `models` 数组）：

```json
{ "models": [ {
  "slug": "deepseek-flash",
  "display_name": "DeepSeek Flash",
  "description": "DeepSeek 快速模型",
  "default_reasoning_level": "high",
  "supported_reasoning_levels": [ {"effort":"low","description":"快速"},
                                  {"effort":"high","description":"深度思考"} ],
  "shell_type": "shell_command",
  "visibility": "list",
  "supported_in_api": true,
  "priority": 0,
  "base_instructions": "You are Codex ... 始终使用简体中文回复。",
  "supports_reasoning_summaries": true,
  "default_reasoning_summary": "none",
  "support_verbosity": false,
  "truncation_policy": { "mode": "bytes", "limit": 10000 },
  "supports_parallel_tool_calls": true,
  "experimental_supported_tools": [],
  "input_modalities": ["text"]
} ] }
```

**第三处：桌面版 UI 的选中项单独存着**（不跟 config.toml 同步）：

`~/.codex/.codex-global-state.json` →
`electron-persisted-atom-state.composer-recent-model-configurations-v1`
（形如 `[{"model":"gpt-5.6-sol","reasoningEffort":"high","serviceTier":null}]`）
不改这里，桌面版仍会提交旧模型名。用 Python 改 JSON 比手改安全：

```python
d = json.load(open(p, encoding="utf-8"))
a = d["electron-persisted-atom-state"]
a["composer-recent-model-configurations-v1"] = [
    {"model": "deepseek-flash", "reasoningEffort": "high", "serviceTier": None}]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
```

⚠️ **改配置前必须完全退出桌面版**（进程名是 **`ChatGPT.exe`**，不是 `codex.exe`！
`codex.exe` 是后台 app-server daemon），否则退出时会覆盖 `config.toml`。

```powershell
Stop-Process -Name ChatGPT -Force; Stop-Process -Name codex -Force
# 重启：
& "$env:APPDATA\npm\codex.cmd" app
```

验证：`codex exec --skip-git-repo-check "..."` 输出里应为
`model: deepseek-flash` / `reasoning effort: high`（**没有** metadata 警告）。

### 中文界面

桌面版 `app.asar` 内置完整简体中文翻译，无需第三方汉化补丁：
**File → Settings（或 Ctrl+,）→ General → Language for the app UI → 简体中文 → 重启**。
（部分版本该选项受服务端灰度控制，需能连通 OpenAI 服务。）

"中文回复"是另一件事，靠全局指令文件实现（对所有项目生效）：

```
~/.codex/AGENTS.md   ← 写明"始终使用简体中文回复；代码/命令/路径保持原样"
```

### 排查桌面版用得上的一次性检索

```bash
# 进程路径确认桌面版版本
Get-Process | Where-Object { $_.Path -like '*OpenAI*' } | Select Id,ProcessName,Path
# app.asar 里找界面文案 / 存储键（325MB，grep 较慢，注意加 timeout）
grep -aoE '.{0,180}settings\.ide\.language\.search.{0,400}' "...\app\resources\app.asar"
```

桌面版状态库 `~/.codex/state_5.sqlite`（表 `threads` 有 model/model_provider/
title 等列）可用来核对最近会话实际用的模型。

### 桌面版需重启

配置写入前已启动的 Codex 桌面进程不会热加载，必须**关闭再打开**。
注意"关闭"要连 UI（进程名 `ChatGPT.exe`）和 daemon（`codex.exe`）一起停。
桌面版的模型选择器还会把选中模型**写回 `config.toml`**——被覆盖时按上一节回填，
并同步 `.codex-global-state.json` 里的选择项，否则它仍会提交旧模型名。

### 桌面版仍要求登录 ChatGPT / 卡在「电话号码是必填项」

官方（developers.openai.com/codex/auth）明确：桌面版支持**两种**登录方式 ——
`Sign in with ChatGPT` 与 **`Sign in another way`（输入 API key）**。
卡在**手机验证页**说明用户误入了 ChatGPT 分支（OpenAI 不支持中国大陆手机号，此路不通）。
API key 入口在**已登出的欢迎页**上 → 需先从手机验证页返回，选 `Sign in another way`，
粘贴自定义 provider 的 key 即可。

若桌面版不认已经写好的 `auth.json`，原因是 Windows 上 Codex 默认
`cli_auth_credentials_store` 走 **keyring（系统凭据管理器）**，而手动只写了文件：

```toml
cli_auth_credentials_store = "file"   # 强制从 ~/.codex/auth.json 读凭证
```

再设用户级环境变量 `OPENAI_API_KEY` 作双保险：

```powershell
[Environment]::SetEnvironmentVariable('OPENAI_API_KEY','sk-...','User')
```

验证：`codex login status` → `Logged in using an API key`。

**桌面版结构备忘（排查登录态用）**
- MSIX 数据：`AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\`
- Electron userData（Chromium profile / Cookies / Local Storage）：
  `LocalCache\Roaming\Codex\web\Codex\Default\` ← 登录中间态顽固时清这里
- 应用日志：`LocalCache\Local\Codex\Logs\`

---

## 故障：Codex 被注销 / 提示重新登录（auth.json 消失）

（2026-09-17 实测，恢复耗时约 3 分钟）

**现象**：桌面版突然回到未登录状态，或 CLI 报需要认证。检查发现
`~/.codex/auth.json` **不存在**。

**根因**：配置了 `cli_auth_credentials_store = "file"` 时，登录凭据就只存在
`~/.codex/auth.json` 这一个文件里。用户误点桌面版的
`Sign out`（或界面里的注销/退出账号）会**直接删掉该文件**——
它不是"退出 ChatGPT 账号"，而是抹掉凭据。

**关键判断：这不是配置损坏。** 注销只删凭据文件，其余都还在：
- `config.toml` 的 `model_provider = "custom"` / `[model_providers.custom]` 照旧在；
- `.codex-global-state.json` 里**没有**任何账号/登录/登出标记残留；
- 用户级环境变量 `OPENAI_API_KEY` 也还在。

所以**不要重装、不要重建 config.toml**，只需把凭据文件写回去。

**恢复流程**：

1. 确认 `~/.codex/auth.json` 缺失，同时确认 `config.toml` 顶层键未丢：
   ```bash
   ls -la ~/.codex/auth.json    # 期望 NOT EXIST
   grep -E "^(model_provider|model |cli_auth_credentials_store)" ~/.codex/config.toml
   ```
2. 写回 `~/.codex/auth.json`（只两行；内容从备份取，或用户级 `OPENAI_API_KEY` 环境变量）：
   ```json
   {
     "OPENAI_API_KEY": "sk-..."
   }
   ```
   备份位置：`<你的备份目录>\auth.json`
3. **顺手统一会话模型名**（历史遗留的非法名一起清掉，避免踩坑）：
   ```python
   import sqlite3, os
   c = sqlite3.connect(os.path.expanduser("~/.codex/state_5.sqlite"))
   c.execute("update threads set model='deepseek-flash' where model='deepseek-v4-flash'")
   c.commit(); c.execute("PRAGMA wal_checkpoint(TRUNCATE)"); c.close()
   ```
4. 备份 `config.toml` 后重启桌面版（先备份，防止启动时重写把自定义 provider 冲掉）：
   ```bash
   cp ~/.codex/config.toml "<备份目录>/config.toml.已修复-$(date +%F)"
   ```
5. 启动桌面版 —— **必须用 node 直调，不能用 `cmd //c codex.cmd app`**
   （Git Bash 下 `//c` 转义会失效，只弹一个空 cmd 就退出，进程根本没起来）：
   ```bash
   "C:/Program Files/nodejs/node.exe" \
     "$HOME/AppData/Roaming/npm/node_modules/@openai/codex/bin/codex.js" app
   ```
   期望在 10 秒内看到 8 个 `ChatGPT.exe` + 1 个 `codex.exe`。
6. 验证：
   ```bash
   codex.exe exec --skip-git-repo-check "只回复四个字：连接正常"
   ```
   头部应打印 `model: deepseek-flash` / `provider: custom`。

**正常现象，别误判成故障**：日志里会反复出现
`remote control requires ChatGPT authentication; API key auth is not supported`
和 `chatgpt authentication required for remote plugin catalog` ——
这些是 **ChatGPT 账号专属功能**（远程控制、远程插件目录），第三方 API key
接入天然不支持，**与对话能力无关**。判断登录是否真的坏掉，只看有没有
4xx/401，以及 CLI 能否跑通。

---

## 故障：桌面版提示「The supported API model names are …，but you passed gpt-5.6-sol」

（2026-09-17 实测，Codex Desktop 26.908.9136.0 + codex-cli 0.154.0）

配置、密钥、连通性全部正常（CLI 能跑），只有桌面版发请求时带 OpenAI 模型名。**两个独立根因**：

### 根因 1：桌面选择器被自己的 UI 状态控制，`model_catalog_json` 对它无效

上游 bug [openai/codex#19694](https://github.com/openai/codex/issues/19694)：
app-server 已加载 `model_catalog_json` 并经由 `model/list` 返回自定义模型，
但 Desktop 渲染层按**远程白名单**过滤，自定义模型**不会出现在选择器里**。
所以选择器只能停在默认的 `gpt-5.6-sol`。

> 反例记忆：不要试图通过改 `.codex-global-state.json` 里
> `composer-recent-model-configurations-v1` 的顺序来切换模型 ——
> 应用启动后会把 `gpt-5.6-sol` 重新插回第一位，改写无效。

**修法**：不再碰选择器，改为**清掉整份 UI 状态让它重新从 config 推导**。

1. 彻底退出（UI 进程名是 `ChatGPT.exe`，`codex.exe` 只是后台 daemon），
   用任务管理器或 `Stop-Process` 把所有同名进程杀掉；
2. 先备份、再**移走**下列两份文件（少一份都不行）：
   - `~/.codex/.codex-global-state.json`
   - `~/.codex/.codex-global-state.json.bak`
3. 重新启动：`codex app`

**成功标志**：重启后该文件重新生成且极简（≈845 字节，
`composer-recent-model-configurations-v1 == null`）。

### 根因 2：会话在创建时「钉死」模型名，旧对话永久失败

`~/.codex/state_5.sqlite` 的 `threads.model` 记录每个会话的模型。
钉成 `gpt-5.6-sol` 的会话，**怎么重发都报同样的错**，必须新建对话。

```python
import sqlite3
c = sqlite3.connect(os.path.expanduser("~/.codex/state_5.sqlite"))
c.execute("update threads set model='deepseek-flash' where model like 'gpt-5.6%'")
c.commit(); c.execute("PRAGMA wal_checkpoint(TRUNCATE)"); c.close()
```

（会话的模型**不在** rollout `.jsonl` 的 `session_meta` 里 —— 那里只有
`model_provider`，没有 `model`。所以只需改 `state_5.sqlite`。）

### 排查用的定位手法（可复用）

```python
# 1) 看最近的真实报错（日志噪声大：先按关键字过滤，再取尾部，否则全是 span 前缀）
import os, sqlite3, datetime
RO = lambda p: "file:" + os.path.expanduser(p).replace("\\", "/") + "?mode=ro"
c = sqlite3.connect(RO("~/.codex/logs_2.sqlite"), uri=True)
for ts, lv, tgt, b in c.execute(
        "select ts,level,target,feedback_log_body from logs "
        "where feedback_log_body like '%supported API model names%' order by id desc limit 5"):
    print(datetime.datetime.fromtimestamp(ts), lv, tgt, b[-300:])

# 2) 看每个会话实际用的模型
c2 = sqlite3.connect(RO("~/.codex/state_5.sqlite"), uri=True)
for r in c2.execute("select model,model_provider,title from threads order by updated_at desc limit 10"):
    print(r)
```

日志里 `codex_models_manager::model_info: Unknown model gpt-5.6-x is used` 就是
「桌面正在用内置默认模型」的信号。

### 关于界面语言（`localeOverride`）

- 应用**内置完整简体中文包**：`app.asar` → `/webview/assets/zh-CN-*.js`（约 1.39 MB），
  另有 zh-HK / zh-TW。**不需要联网、不要装第三方汉化补丁**。
- 配置方式（写进 `config.toml`，重启生效）：

  ```toml
  [desktop]
  localeOverride = "zh-CN"
  ```

- **取值必须是 `zh-CN`**（应用内部映射到 `zh-Hans` 语言块），写 `zh` / `zh-Hans` 无效。
- 界面语言异常时，先重启；无效则按上文移走 `.codex-global-state.json`
  （该文件的 UI 派生状态损坏会同时表现为「界面回英文」+「模型列表异常」）。
- 校验语言包是否存在的快速方法（无需解压 asar）：用 Python 读 asar 头部
  JSON（`struct.unpack('<4I', f.read(16))`，第 4 个值是 JSON 长度），
  遍历 `files` 树，筛名字含 `zh` / `locale` 的条目。
  文件共 9000+ 条目，别用 `grep` 逐串扫，太慢（325 MB）。

### 兜底方案（以上都无效时）

本地起一个**改名代理**：`base_url` 指向 `http://127.0.0.1:<port>`，
由代理把请求体里的 `model` 字段统一改写成 `deepseek-flash` 再转发到
`https://api.deepseek.com`。这样无论桌面选择器发什么模型名都能通。
代价是必须常驻一个进程（可放进启动文件夹自启），非必要不用。


