---
name: cross-terminal-sync
description: WorkBuddy 跨终端（Mac/Windows）无缝切换方案。双层架构：MCP API 直连 OneDrive 云端（优先跨终端搜索）+ 文件同步（日常主力）。支持跨终端任务搜索与接力执行。触发场景：用户提到"跨终端"、"另一台电脑"、"Windows 上做的任务在这台继续"、"同步 Skill/项目/配置"等。
visibility: public
version: 2.2.0
agent_created: true
---

# Cross-Terminal Sync v2 — 双层跨终端方案

> **两层架构**：MCP API 直连云端（快速搜索） + OneDrive 文件同步（日常主力）。
> **优先级**：日常干活走文件同步（零延迟），紧急跨终端搜索走 MCP API（毫秒级），两种方式互补。

## 架构总览

```
                        Microsoft Graph API (云端)
                              ↑ 直连
                    ┌─────────┴─────────┐
                    │  MCP Server       │  ← 快路径（跨终端紧急搜索）
                    │  (onedrive-mcp)   │
                    └───────────────────┘
                              ↑
                    ┌─────────┴─────────┐
                    │     WorkBuddy     │
                    └─────────┬─────────┘
                              │ 读写（符号链接）
              ┌───────────────┴───────────────┐
              │     OneDrive 本地文件夹        │  ← 主路径（日常干活）
              │ OneDrive 本地同步文件夹 (平台相关) │
              └───────────────┬───────────────┘
                              │ OneDrive 客户端自动同步
                        Microsoft 云端存储
```

**为什么双层？**
- 日常干活：文件同步就够了，你一般在一台机器上连续工作，不会突然切换
- 偶尔需要查另一台的成果：MCP API 直接翻云端，不等 OneDrive 客户端同步
- MCP 不需要管理员权限（纯用户态 Python 应用），公司电脑也能装

## 目录结构

```
OneDrive路径/WorkBuddySync/
├── mac/                    # Mac 终端数据（独立管理）
│   ├── IDENTITY.md         # Agent 身份（Mac 版）
│   ├── MEMORY.md           # 跨项目长期记忆（Mac 版）
│   ├── SOUL.md             # Agent 人格（Mac 版）
│   ├── USER.md             # 用户档案（Mac 版）
│   ├── skills/             # Mac 安装的 Skill
│   ├── projects/           # Mac 项目文件
│   └── workbuddy.db        # Mac 自动化任务配置
├── windows/                # Windows 终端数据（独立管理）
│   ├── IDENTITY.md         # Agent 身份（Windows 版）
│   ├── MEMORY.md           # 跨项目长期记忆（Windows 版）
│   ├── SOUL.md             # Agent 人格（Windows 版）
│   ├── USER.md             # 用户档案（Windows 版）
│   ├── skills/             # Windows 安装的 Skill
│   ├── projects/           # Windows 项目文件
│   └── workbuddy.db        # Windows 自动化任务配置
└── README.md               # 结构说明

> **注意**：Mac 和 Windows 的身份文件各自独立，不复用 shared/ 目录，
> 因为两台终端的 Agent 身份和工作偏好可能不同。
```

符号链接关系（以 Mac 为例）：
```
~/.workbuddy/skills    → OneDrive路径/WorkBuddySync/mac/skills
~/.workbuddy/projects  → OneDrive路径/WorkBuddySync/mac/projects
~/.workbuddy/MEMORY.md → OneDrive路径/WorkBuddySync/mac/MEMORY.md
~/.workbuddy/IDENTITY.md → OneDrive路径/WorkBuddySync/mac/IDENTITY.md
~/.workbuddy/USER.md   → OneDrive路径/WorkBuddySync/mac/USER.md
~/.workbuddy/SOUL.md   → OneDrive路径/WorkBuddySync/mac/SOUL.md
~/.workbuddy/workbuddy.db → OneDrive路径/WorkBuddySync/mac/workbuddy.db
```

> **Mac OneDrive 路径注意**：macOS 上 OneDrive 实际同步目录可能是
> `~/Library/CloudStorage/OneDrive-ZURUINC/` 而非 `~/OneDrive - ZURU INC/`。
> 务必先用 `ls ~/OneDrive*` 和 `ls ~/Library/CloudStorage/` 确认真实路径。

---

## 功能 0：安装 MCP Server（快速搜索通道，推荐）

MCP API 直连 OneDrive 云端，**不需要管理员权限**。

### 为什么不需要管理员权限？

MrFixit96/onedrive-mcp-server 是纯用户态 Python 应用：
- ❌ 不需要管理员权限
- ❌ 不注册系统服务
- ❌ 不修改注册表
- ❌ 不安装证书
- ✅ 作为普通进程运行，绑定高端口 (>1024)
- ✅ 使用用户自己的 OS 密钥环存储凭据（不碰系统级安全策略）

**公司电脑无管理员权限也可以装。**

### Mac 安装

```bash
# 1. 安装
pip install git+https://github.com/MrFixit96/onedrive-mcp-server.git

# 2. 配置 WorkBuddy MCP（添加到 ~/.workbuddy/mcp.json）
# HTTP 模式最省事，不需要 Azure 应用注册
```

`~/.workbuddy/mcp.json` 添加：
```json
{
  "mcpServers": {
    "onedrive": {
      "type": "http",
      "url": "http://localhost:3001/mcp"
    }
  }
}
```

启动 MCP Server：
```bash
# HTTP 模式（推荐，零配置 SSO）
onedrive-mcp --http
# 默认端口 3001，WorkBuddy 自动处理 OAuth 认证
```

### Windows 安装

```powershell
# 1. 安装（不需要管理员权限）
pip install git+https://github.com/MrFixit96/onedrive-mcp-server.git

# 2. 启动
onedrive-mcp --http
# 同样零配置，WorkBuddy 自动处理认证
```

### MCP 提供的 6 个工具

| 工具 | 功能 |
|------|------|
| `list_files` | 列出 OneDrive 任意路径的文件 |
| `search_files` | 跨文件名和内容全文搜索 |
| `get_file_metadata` | 获取文件大小、类型、修改时间 |
| `download_file` | 下载文件（带路径安全保护） |
| `upload_file` | 上传文件（>4MB 支持断点续传） |
| `create_sharing_link` | 生成分享链接 |

### 什么时候用 MCP？

```
日常干活 → 走文件同步（符号链接 → OneDrive 本地文件夹）
跨终端紧急查找 → 走 MCP API（直连云端，不等同步）
OneDrive 客户端挂了 → MCP API 兜底
```

---

## 功能 1：初始化文件同步（首次执行）

在 Windows WorkBuddy 中加载此 Skill 后，先说"初始化跨终端同步"，然后按以下步骤执行：

### Step 1: 找到 OneDrive 路径

```powershell
# 查找 OneDrive 路径
$env:OneDriveCommercial
# 或
$env:OneDrive
# 常见路径：C:\Users\<用户名>\OneDrive - ZURU INC\
```

### Step 2: 检查目录结构是否已存在

检查 `OneDrive根目录\WorkBuddySync\` 是否已存在：
- 如果已存在（Mac 端已创建），跳过创建，直接进入 Step 4
- 如果不存在，执行 Step 3

### Step 3: 创建目录结构

```powershell
$ONEDRIVE = "C:\Users\<你的用户名>\OneDrive - ZURU INC"  # 替换为实际路径
New-Item -ItemType Directory -Force -Path "$ONEDRIVE\WorkBuddySync\mac\skills"
New-Item -ItemType Directory -Force -Path "$ONEDRIVE\WorkBuddySync\mac\projects"
New-Item -ItemType Directory -Force -Path "$ONEDRIVE\WorkBuddySync\windows\skills"
New-Item -ItemType Directory -Force -Path "$ONEDRIVE\WorkBuddySync\windows\projects"
```

### Step 4: 建立符号链接

**Windows 创建符号链接的两种方式（都不需要真正的管理员权限）：**

**方式 A（推荐）：开启开发者模式**
```
设置 → 更新和安全 → 开发者选项 → 开启"开发人员模式"
开启后 mklink 无需管理员权限
```

**方式 B：使用目录联接 (Junction)**
目录联接不需要管理员权限，效果和符号链接一样：
```cmd
REM 先备份原目录
ren %USERPROFILE%\.workbuddy\skills skills.bak
ren %USERPROFILE%\.workbuddy\projects projects.bak

REM 创建目录联接（不需要管理员！）
mklink /J %USERPROFILE%\.workbuddy\skills "%ONEDRIVE%\WorkBuddySync\windows\skills"
mklink /J %USERPROFILE%\.workbuddy\projects "%ONEDRIVE%\WorkBuddySync\windows\projects"

REM 文件符号链接（身份文件放在 windows/ 下，各自独立管理）
ren %USERPROFILE%\.workbuddy\MEMORY.md MEMORY.md.bak
mklink %USERPROFILE%\.workbuddy\MEMORY.md "%ONEDRIVE%\WorkBuddySync\windows\MEMORY.md"
ren %USERPROFILE%\.workbuddy\IDENTITY.md IDENTITY.md.bak
mklink %USERPROFILE%\.workbuddy\IDENTITY.md "%ONEDRIVE%\WorkBuddySync\windows\IDENTITY.md"
ren %USERPROFILE%\.workbuddy\USER.md USER.md.bak
mklink %USERPROFILE%\.workbuddy\USER.md "%ONEDRIVE%\WorkBuddySync\windows\USER.md"
ren %USERPROFILE%\.workbuddy\SOUL.md SOUL.md.bak
mklink %USERPROFILE%\.workbuddy\SOUL.md "%ONEDRIVE%\WorkBuddySync\windows\SOUL.md"
ren %USERPROFILE%\.workbuddy\workbuddy.db workbuddy.db.bak
mklink %USERPROFILE%\.workbuddy\workbuddy.db "%ONEDRIVE%\WorkBuddySync\windows\workbuddy.db"
```

> **注意**：`mklink /J`（目录联接）不需要管理员权限。`mklink`（文件符号链接）在开启开发者模式后也不需要。

**Windows 方式 C：安全软件拦截时的 robocopy 备选**

如果公司安全软件阻止了所有文件符号链接（即使开发者模式已开启），使用定时 robocopy 同步：

1. 创建同步脚本 `~/.workbuddy/scripts/sync-onedrive.ps1`（按最后修改时间双向同步 5 个核心文件到 `windows/` 目录）
2. 创建 WorkBuddy 自动化，每小时执行一次该脚本
3. 目录联接（skills/、projects/）不受影响，继续使用方式 B

此方案同步有延迟（最长 1 小时），但对 95% 的使用场景足够。

### Step 5: 验证

```powershell
Get-Item "$env:USERPROFILE\.workbuddy\skills" | Select-Object LinkType, Target
Get-Item "$env:USERPROFILE\.workbuddy\MEMORY.md" | Select-Object LinkType, Target
```

---

## 功能 2：自动等待 OneDrive 同步

在读取 OneDrive 文件前，确保文件已同步到最新。使用信号文件机制：

### 方法：写入信号文件 + 轮询等待

```bash
# === Mac（注意：确认正确 OneDrive 路径）===
# 先检测 OneDrive 实际路径
ONEDRIVE=$(ls -d ~/Library/CloudStorage/OneDrive-* 2>/dev/null || ls -d ~/OneDrive* 2>/dev/null | head -1)
SIGNAL_FILE="$ONEDRIVE/WorkBuddySync/.sync_signal_$(hostname -s)"

# 1. 写入信号文件
echo "$(date +%s)" > "$SIGNAL_FILE"

# 2. 等待 OneDrive 上传（最多等 30 秒）
for i in $(seq 1 30); do
  # 检查文件修改时间是否被同步回（说明云端已确认）
  if [ -f "$SIGNAL_FILE" ]; then
    MOD_TIME=$(stat -f %m "$SIGNAL_FILE" 2>/dev/null)
    if [ "$MOD_TIME" -gt "$(date -v-5S +%s)" ]; then
      echo "OneDrive sync OK"
      break
    fi
  fi
  sleep 1
done
```

```powershell
# === Windows ===
$ONEDRIVE = "$env:USERPROFILE\OneDrive - ZURU INC\WorkBuddySync"
$SIGNAL_FILE = "$ONEDRIVE\.sync_signal_$env:COMPUTERNAME"

# 1. 写入信号文件
Get-Date -UFormat %s | Out-File -FilePath $SIGNAL_FILE

# 2. 等待同步（最多 30 秒）
for ($i=0; $i -lt 30; $i++) {
  if (Test-Path $SIGNAL_FILE) {
    $lastWrite = (Get-Item $SIGNAL_FILE).LastWriteTime
    if ($lastWrite -gt (Get-Date).AddSeconds(-5)) {
      Write-Host "OneDrive sync OK"
      break
    }
  }
  Start-Sleep -Seconds 1
}
```

### 关键原则

- **在任何跨终端文件读取之前**，先执行此同步等待
- 超时 30 秒后仍继续执行，但提示用户"OneDrive 同步可能未完成"
- 如果 OneDrive 客户端未运行，警告用户

---

## 功能 3：跨终端任务搜索与接力执行（双层搜索）

### 搜索优先级（核心逻辑）

```
用户说: "调用之前在 Windows 做的【多Agent生成视频工作流】的成果"

                    ┌─────────────────┐
                    │  Step 0: 本地搜索 │  ← 先搜本机（最快）
                    │  ~/.workbuddy/   │
                    └────────┬────────┘
                             │ 未找到
                    ┌────────▼─────────┐
                    │ Step 1: MCP API  │  ← 直连云端搜另一终端（毫秒级）
                    │ 如果 MCP 已安装  │
                    └────────┬────────┘
                             │ 未找到或 MCP 未装
                    ┌────────▼─────────┐
                    │ Step 2: 文件同步  │  ← 等 OneDrive 同步后搜（兜底）
                    │ 搜另一终端目录    │
                    └────────┬────────┘
                             │ 都未找到
                    ┌────────▼─────────┐
                    │ Step 3: 新任务    │  ← 从头开始
                    └──────────────────┘
```

### 详细逻辑

| 步骤 | 方式 | 速度 | 适用场景 |
|:--:|------|:--:|------|
| Step 0 | 搜索本机 `~/.workbuddy/` + workspace diary | 即时 | 日常主力路径 |
| Step 1 | MCP API `search_files` 直连云端 | 毫秒级 | 紧急跨终端查找、OneDrive 客户端挂了 |
| Step 2 | 等 OneDrive 同步后搜另一终端目录 | 秒~十秒 | MCP 未安装时的回退 |
| Step 3 | 报告"都未找到"，询问是否开始新任务 | — | 全新任务 |

### Step 1 实现：MCP API 搜索（推荐）

```python
# 伪代码：WB 通过 MCP 搜索另一终端
# MCP Server 提供的 search_files 工具直接搜 OneDrive 云端

# 假设当前在 Mac，搜索 Windows 终端做过的工作：
mcp_search(
    path="/WorkBuddySync/windows",  # 另一终端的目录
    query="多Agent 视频 工作流"       # 用户描述的关键词
)
# 返回云端文件列表，下载需要的文件到本地
```

**优势**：不依赖 OneDrive 客户端是否在运行、是否同步完成。直接问云端。

### Step 2 回退：文件同步搜索

当 MCP 未安装或不可用时，走传统文件同步路径：
- 先执行功能 2（同步等待）
- 再搜索 OneDrive 本地目录中另一终端的文件

### 搜索关键词提取

从用户输入中提取搜索关键词：
- 项目名：助农精选联盟、中登日记、1688、NeverLand、EntroCamp、虾评
- 动作词：视频、拆书、多Agent、工作流、Pipeline、自动化
- 文件类型：Skill、Project、日记、配置

### 实现参考

```bash
# Mac 端：MCP API 搜索（优先）
# 通过 MCP onedrive search_files 工具直连云端

# 回退：文件系统搜索另一终端
OTHER_TERM="windows"  # 或 "mac"
ONEDRIVE=$(ls -d ~/Library/CloudStorage/OneDrive-* 2>/dev/null || ls -d ~/OneDrive* 2>/dev/null | head -1)
grep -rl "$KEYWORD" "$ONEDRIVE/WorkBuddySync/$OTHER_TERM/" 2>/dev/null
```

---

## 功能 4：同步状态检查（补充功能）

检查两台终端的同步健康状态：

```
检查项：
├── OneDrive 客户端是否运行？
├── WorkBuddySync 目录是否存在？
├── mac/ 和 windows/ 目录内容是否最新？
├── 身份文件（IDENTITY/MEMORY/SOUL/USER）是否各终端独立？
├── 符号链接是否完好（未断链）？
└── 最近一次同步时间？
```

### 执行命令

```bash
# Mac（自动检测 OneDrive 路径）
ONEDRIVE=$(ls -d ~/Library/CloudStorage/OneDrive-* 2>/dev/null || ls -d ~/OneDrive* 2>/dev/null | head -1)
echo "=== OneDrive 状态 ===" && pgrep -l "OneDrive" && echo "=== 同步目录 ===" && ls -la "$ONEDRIVE/WorkBuddySync/" && echo "=== 符号链接 ===" && ls -la ~/.workbuddy/ | grep "^l"
```

```powershell
# Windows
Write-Host "=== OneDrive 状态 ==="; Get-Process "OneDrive" -ErrorAction SilentlyContinue
Write-Host "=== 同步目录 ==="; Get-ChildItem "$env:USERPROFILE\OneDrive - ZURU INC\WorkBuddySync\"
Write-Host "=== 符号链接 ==="; cmd /c "dir /AL $env:USERPROFILE\.workbuddy"
```

---

## 功能 5：冲突预防（补充功能）

由于用户交替使用两台终端，通常不会同时操作。但需要防护：

1. **写入前检查**：在修改身份文件前，检查另一终端的信号文件时间戳
2. **锁定机制**：写入 mac/ 或 windows/ 目录前，在对应目录创建 `.lock_<hostname>` 文件，写完后删除
3. **差异报告**：如果检测到 mac/skills/ 和 windows/skills/ 有同名 Skill 但内容不同，报告差异让用户决定以哪个为准

---

## 当前已知的终端信息

| 终端 | OneDrive 典型路径 | 角色 | Agent 名 |
|------|-------------------|------|----------|
| Mac | `~/Library/CloudStorage/OneDrive-ZURUINC/` 或 `~/OneDrive - ZURU INC/` | 私人相关内容 | 翻身 |
| Windows | `%USERPROFILE%\OneDrive - ZURU INC\` | 工作相关内容 | 咸鱼 |

> **Mac 路径确认方法**：`ls ~/Library/CloudStorage/` 找到真实 OneDrive 目录名，
> 优先使用 `CloudStorage` 下的路径（这是 macOS File Provider 的实际同步目录）。

---

## 补充考虑的场景

| 场景 | 处理方式 |
|------|------|
| 某台终端 Skill 更新了 | OneDrive 自动同步 + MCP API 可快速拉取最新版本 |
| 设备离线时做了任务 | 联网后 OneDrive 自动上传，MCP API 可主动拉取（不等客户端同步） |
| mac/MEMORY.md 和 windows/MEMORY.md 冲突 | 各自独立维护，互不影响 |
| mac/ 和 windows/ 有同名项目 | 功能 5 差异报告，用户选择合并或保留 |
| Windows 无管理员权限 | 开启开发者模式或使用 `mklink /J`（目录联接，不需要管理员） |
| OneDrive 空间不足 | 检查可用空间，建议排除 binaries/ 大文件 |
| 想新增第三台设备（如 Linux） | 在 WorkBuddySync/ 下新增 linux/ 目录 + MCP 照样用 |
| 公司防火墙拦截某些端口 | MCP 走 HTTPS (443)，与浏览器相同，不会被拦截 |
| MCP Server 进程挂了 | 自动回退到文件同步路径，不影响干活 |
| OneDrive 客户端未启动 | MCP API 不受影响，文件同步不可用但有 MCP 兜底 |
| Mac OneDrive 路径不对（符号链接指向错误位置） | 用 `ls ~/Library/CloudStorage/` 找出真实路径后重建符号链接 |
| 公司安全软件拦截文件符号链接 | 使用方式 C（robocopy 定时同步）兜底 |

---

## 使用示例

### 示例 1：Windows 上初始化
```
用户: "初始化跨终端同步"
WB: 执行功能 1 → 创建目录 → 建立符号链接 → 验证
```

### 示例 2：调用另一终端成果
```
用户: "调用之前在 Mac 做的 Seedance 视频成果"
WB: Step1 本地搜 → 未找到
     Step2 OneDrive 搜 mac/projects → 找到 → 加载 → 继续执行
```

### 示例 3：检查同步状态
```
用户: "检查下两台终端的同步状态"
WB: 执行功能 4 → 输出状态报告
```

### 示例 4：跨终端执行后的记忆写入
```
在 Windows 上完成项目 X 后：
WB 写入 memory 到 windows/MEMORY.md
下次在 Mac 执行类似任务时，可搜索 windows/ 目录找历史上下文
```

---

## 注意事项

1. **mcp.json 不参与同步**：路径因终端而异，各自维护
2. **binaries/ 不参与同步**：Node/Python 运行时平台绑定
3. **workspace memory 日记不同步**：workspace 级别的日记仅在当前 workspace 有效
4. **Windows 符号链接**：开启开发者模式或使用 `mklink /J`（目录联接），都不需要管理员权限
5. **MCP Server 是可选加速包**：没有也不影响使用，文件同步照样工作；装了能在跨终端搜索时更快
6. **OneDrive 免费空间 5GB**：WorkBuddy 核心文件（不含 binaries）通常 < 100MB，足够
7. **认证安全**：MCP Server 使用 OS 密钥环存储凭据，OAuth 范围仅 `Files.ReadWrite + User.Read`，不访问邮件/日历/联系人
8. **Mac OneDrive 路径**：macOS 上 OneDrive File Provider 的实际同步路径可能是 `~/Library/CloudStorage/OneDrive-XXX/`，务必先确认真实路径再建符号链接
9. **身份文件独立**：mac/ 和 windows/ 各有自己的 IDENTITY.md/MEMORY.md/SOUL.md/USER.md，不复用 shared/ 目录
