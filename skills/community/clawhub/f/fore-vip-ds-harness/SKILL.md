---
name: fore-vip-ds-harness
display_name: DSH 傻瓜式启动
display_name_en: DeepSeek Harness One-Click
description: DeepSeek Harness（dsh）傻瓜式本地启动助手。一句话讲清 DSH 是什么，引导在 DeepSeek 开放平台获取 API Key，按本机系统（macOS/Windows/Linux）实时装好 Node、配置 npm 国内镜像、安装并启动 dsh，并就地生成桌面快捷方式（启动服务并打开 http://localhost:3080）。运行脚本由 Agent 按系统环境实时写出，不依赖任何随包文件。触发词：DSH、DeepSeek Harness、dsh、本地部署 DeepSeek、DeepSeek Agent 框架、傻瓜式启动。
category: devtools
version: 1.0.0
author: WISE
---

# DSH 傻瓜式启动

## 这是什么（一句话版）

**DeepSeek Harness（命令行叫 `dsh`）是 DeepSeek 开源的 AI Agent 运行框架。** 用一个公式记：

> **Agent = 模型（大脑） + Harness（手脚 / 工作台 / 安全带）**

模型只会聊天，Harness 负责读文件、跑命令、拆任务、管会话、走权限审批——让 AI 真正把活干完。本地优先，一条命令起 Web 界面，数据全在本地。

- 开源协议：MIT（免费、可改、可商用，无订阅）
- 官方仓库：https://github.com/deepseek-ai/deepseek-harness
- npm 包：`@deepseek-ai/dsh`
- 当前状态：v0.1 开发者预览版（接口可能变动，**不建议直接当生产依赖**）

## 触发与适用

| 用户说法 | 处理 |
|---------|------|
| DSH / dsh 是什么、DeepSeek Harness 怎么用 | 先讲「这是什么」，再进入启动流程 |
| 帮我装 dsh、本地跑 DeepSeek Agent、傻瓜式启动 | 直接走启动流程 |
| 只问概念不装 | 仅科普，不执行安装 |

## 傻瓜式启动流程（Agent 运行时执行）

> 核心约束：**本 SKILL 不携带任何运行脚本文件**。所有安装命令与启动脚本，都由你（Agent）在用户机器上**按检测到的系统环境实时生成并执行**。
> 执行原则：先检测现有环境，能复用就复用；每步只做必要动作。

### 0. 检测系统（第一步先确定 OS）
用 Bash 判断系统，决定走哪条分支：
- **macOS**：`uname -s` 返回 `Darwin`
- **Linux**：`uname -s` 返回 `Linux`
- **Windows**：`uname -s` 不可用或返回 `MINGW*/CYGWIN*/MSYS*`，或检测到 `powershell`/`cmd`

### 1. 讲清楚 DSH 是什么
用「这是什么」一节的话术，1–2 句说明，不展开论文式长篇。

### 2. 拿 DeepSeek API Key
引导用户到 **https://platform.deepseek.com** → 「API keys」→ 创建密钥（以 `sk-` 开头）。
两种用法，告诉用户二选一：
- **Web UI 填**（推荐，最直观）：启动后 `Settings → Models` 粘贴保存
- **环境变量**（启动前）：`export DEEPSEEK_API_KEY="sk-..."`（Windows 用 `set`）

> 安全：Key 仅留在本地配置或环境变量，绝不写进文档 / 日志 / 对外回复。

### 3. 装运行环境（按 OS 分支执行）
先用 `command -v node` 检测 Node；已装且版本 ≥ v22.19（或 ≥ v24）则跳过安装，仅做镜像与 dsh 安装。

**macOS：**
```bash
# 无 Node 时
brew install node            # 无 brew 则引导去 https://nodejs.cn 下 LTS
npm config set registry https://registry.npmmirror.com
npm install -g @deepseek-ai/dsh
dsh --version
```

**Linux：**
```bash
# 无 Node 时（按发行版二选一）
sudo apt update && sudo apt install -y nodejs npm      # Debian/Ubuntu
# sudo dnf install -y nodejs npm                       # Fedora
npm config set registry https://registry.npmmirror.com
npm install -g @deepseek-ai/dsh
dsh --version
```

**Windows（PowerShell）：**
```powershell
# 无 Node 时
winget install OpenJS.NodeJS.LTS      # 无 winget 则引导去 https://nodejs.cn 下 LTS
npm config set registry https://registry.npmmirror.com
npm install -g @deepseek-ai/dsh
dsh --version
```

> 不想全局装可改用 `npx -y @deepseek-ai/dsh web`（无需 install）。

### 4. 生成启动脚本 + 桌面快捷方式（用 Write 工具实时写出）
按 OS 用你的 **Write 工具**把下列文件写到用户桌面；随后用 Bash 赋可执行权限（Windows 无需）。

**macOS** — 写 `~/Desktop/DeepSeek Harness.command`：
```bash
#!/usr/bin/env bash
export PATH="$HOME/.npm-global/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"
dsh web &
sleep 4
open http://localhost:3080
wait
```
写完后执行：`chmod +x ~/Desktop/DeepSeek\ Harness.command`

**Linux** — 写 `~/Desktop/DeepSeekHarness.desktop`：
```ini
[Desktop Entry]
Type=Application
Name=DeepSeek Harness
Comment=启动 dsh web 并打开 http://localhost:3080
Exec=bash -c 'dsh web & sleep 4; xdg-open http://localhost:3080; wait'
Terminal=true
Categories=Development;
```
写完后执行：`chmod +x ~/Desktop/DeepSeekHarness.desktop`

**Windows** — 写 `桌面\DeepSeek Harness.bat`：
```bat
@echo off
start "" http://localhost:3080
dsh web
```
再在 PowerShell 中创建 `.lnk` 快捷方式（用 Write 写一段临时 ps1 并运行，或用 `-Command` 内联）：
```powershell
$WshShell = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = $WshShell.CreateShortcut("$desktop\DeepSeek Harness.lnk")
$lnk.TargetPath = "$desktop\DeepSeek Harness.bat"
$lnk.WorkingDirectory = $desktop
$lnk.Description = "启动 DeepSeek Harness 并打开 http://localhost:3080"
$lnk.Save()
```

> 快捷方式行为统一为：**启动 `dsh web` 服务 → 等待 → 打开 http://localhost:3080**。

### 5. 收尾提示
完成后告知用户：双击桌面快捷方式即可启动；首次打开 Web UI 需
1. `Settings → Models` 填入 API Key
2. 选择工作区目录
3. 直接派活，敏感操作会弹审批

## 常用命令

| 命令 | 作用 |
|------|------|
| `dsh web` | 启动 Web UI（默认 http://127.0.0.1:3080） |
| `npx -y @deepseek-ai/dsh web` | 免安装直接体验 |
| `dsh web --port 8080` | 指定端口 |
| `dsh --version` | 查看版本 |
| `dsh --profile web --dump-config` | 打印当前插件树（排错用） |

## 注意事项（事实）
- 仅本地回环 `127.0.0.1`，不对外暴露。
- 预览版，后续可能有破坏性变更；生产请等稳定版。
- 工作区外访问需逐次确认，无「总是允许」；本机勿存密钥文件（官方提示「谨慎，不叫边界」）。
- 费用：框架免费，成本来自模型 API 调用（按 token，普通任务几分钱）。
- 运行脚本与快捷方式均在你（Agent）执行本流程时**实时生成**于用户桌面，SKILL 包本身不含可执行文件，可安全发布到任意 SKILL 平台。

## 引用来源
- GitHub: deepseek-ai/deepseek-harness
- npm: @deepseek-ai/dsh
- 开放平台: https://platform.deepseek.com
- 教程实测：阿里云 / 腾讯云开发者社区相关文章（2026-08）
