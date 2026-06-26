<div align="center">

<img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows only" />
<img src="https://img.shields.io/badge/Version-5.4.0-orange?style=for-the-badge" alt="v5.4.0" />
<img src="https://img.shields.io/badge/License-MIT--0-green?style=for-the-badge" alt="MIT-0" />
<img src="https://img.shields.io/badge/ClawHub-ready-blueviolet?style=for-the-badge" alt="ClawHub" />
<br>
<img src="https://img.shields.io/badge/WorkBuddy-✅-blue?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHJ4PSI0IiBmaWxsPSIjZmZmIi8+PHRleHQgeD0iNCIgeT0iMTYiIGZpbGw9IiMwMDAiIGZvbnQtc2l6ZT0iOCI+V0I8L3RleHQ+PC9zdmc+" alt="WorkBuddy" />
<img src="https://img.shields.io/badge/OpenClaw_compatible-✅-purple?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHJ4PSI0IiBmaWxsPSIjZmZmIi8+PHRleHQgeD0iNCIgeT0iMTYiIGZpbGw9IiMwMDAiIGZvbnQtc2l6ZT0iOCI+T0M8L3RleHQ+PC9zdmc+" alt="OpenClaw" />

# 🛡️ Download Guard

### AI Agent 下载管理 · 位置透明 · C盘保护 · 自动清理 · 永不落C盘

*Download Guard — Transparent AI Agent download management. Track every download, protect your C: drive, auto-cleanup logs. Works with pip, npm, cargo, go, docker, ollama, huggingface, and more.*

</div>

---

## 📖 中文导读

> **TL;DR**：装了 Download Guard 之后，AI Agent 每次下载都会告诉你下到哪、盘还剩多少空间、出问题宁可阻止也不偷偷写 C 盘。日志自动清理，缓存一键迁移。装完就不用管了。

---

## 😩 你的 AI Agent 是不是也这样？

| 痛点 | 真实场景 |
|------|----------|
| 🤷 **"刚才下的东西去哪了？"** | 让 Agent 装个 PyTorch，装完找不到文件在哪 |
| 💥 **C 盘又红了** | 大模型 2-14 GB、npm 全局包、pip 缓存默默堆在 C 盘 |
| 🔄 **重复下载** | Agent 忘了之前下过，同一个模型又下一遍 |
| 🗑️ **垃圾只增不减** | 一年下来的下载日志几百 MB，从来没人清 |
| 💿 **移动硬盘拔了** | 下载目录不可用，Agent 静默切回 C 盘继续写（最坑！） |
| ⚠️ **装完用不了** | 改了 npm prefix 后 PATH 丢了，命令直接 404 |

**Download Guard = 上面六个问题的系统性解药。**

---

## ✨ 装了之后长这样

### 📦 每次下载，实时告知

```
┌──────────────────────────────────────────────┐
│  🛡️ Download Guard                           │
│                                               │
│  📦 文件     : pytorch-2.3.0.whl              │
│  📏 大小     : 2.1 GB                         │
│  📂 写入至   : F:\AI-Downloads\2026-05-26\    │
│  💾 目标盘   : 132 GB 可用  ✅ OK              │
│  💿 C 盘     : 58 GB 可用   ✅ OK              │
│  🔒 路径可用 : ✅ OK                           │
│                                               │
│  ▶ 继续执行...                                │
└──────────────────────────────────────────────┘
```

### ✅ 下载完成，验证 + 记录

```
┌──────────────────────────────────────────────┐
│  ✅ Download Guard · 完成                     │
│                                               │
│  📦 文件   : pytorch-2.3.0.whl  (2.1 GB)      │
│  📍 位置   : F:\AI-Downloads\2026-05-26\      │
│  📝 已记录 : download-log.md                  │
└──────────────────────────────────────────────┘
```

### 🌅 每天第一次交互，自动环境快报

```
┌──────────────────────────────────────────────┐
│  🛡️ Download Guard · 今日首次 · 环境快报       │
│                                               │
│  📂 下载目录   : F:\AI-Downloads (132 GB)      │
│  🔒 路径可用   : ✅ OK                         │
│  💿 C 盘       : 58 GB ✅ OK                   │
│  🗄️ 工具缓存   : 全部 OK                      │
│  📝 日志条数   : 47 条                         │
└──────────────────────────────────────────────┘
```

### 🚫 路径不可用 → 宁可阻止，绝不回退 C 盘

```
┌──────────────────────────────────────────────┐
│  🚫 Download Guard · BLOCKED                  │
│                                               │
│  ❌ 路径不可用 : F:\AI-Downloads               │
│  ⚠️ 原因       : Drive F: not found           │
│  🛑 操作       : 已阻止下载，未回退 C 盘       │
│                                               │
│  💡 请重新连接磁盘或修改下载目录               │
└──────────────────────────────────────────────┘
```

> 🛡️ **核心铁则：路径不可用 → 直接阻止，绝不静默切 C 盘。**

---

## 🚀 一键安装

### ClawHub（推荐）

```bash
clawhub install download-guard
```

### 手动安装

```bash
# 1. clone 仓库
git clone https://github.com/nihaoljx/download-guard.git

# 2. 复制到 WorkBuddy / OpenClaw skills 目录
# Windows:
xcopy download-guard %USERPROFILE%\.workbuddy\skills\download-guard\ /E /I

# macOS/Linux: (注意：仅 check-space 等脚本依赖 PowerShell，macOS 需装 PowerShell Core)
cp -r download-guard ~/.workbuddy/skills/download-guard/
```

### 首次配置（全自动引导）

安装后第一次触发下载时，Skill 自动扫描磁盘并推荐最优路径：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🛡️ Download Guard · 首次配置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

磁盘扫描结果：

  F:  132 GB 可用  ← 推荐（空间最大）
  E:   97 GB 可用
  D:   39 GB 可用
  C:   58 GB 可用  [系统盘 - 不推荐]

推荐：F:\AI-Downloads
确认？或输入其他路径：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**你只需要说一个路径，剩下全自动。** 确认后自动：创建目录 → 写入配置 → 扫描 C 盘缓存 → 输出状态卡。

---

## 🗣️ 对 AI 说这些话

| 说 | 功能 |
|----|------|
| `下载了什么` `download log` | 最近 20 条下载记录 |
| `缓存在哪` `scan cache` | 扫描所有工具缓存位置 |
| `迁移缓存` `migrate cache` | C 盘缓存一键迁走 |
| `磁盘空间` `disk space` | 查看各盘空间 |
| `刚才下的在哪` `where's my download` | 最近一次下载的位置 |
| `检查路径` `check path` | 验证下载目录是否健康 |
| `帮我修复` `fix warnings` | 自动修复所有警告 |
| `修改下载目录` `change download dir` | 换下载目录 |
| `下载版本` `download guard version` | 当前版本号 |
| `重置配置` `reset config` | 重新走首次配置 |
| `卸载 download guard` | 显示清理说明 |

---

## 🔌 覆盖 14 种工具

| 类别 | 工具 |
|------|------|
| **Python** | `pip install` · `uv pip install` · `conda install` |
| **Node.js** | `npm install -g` · `pnpm add -g` · `bun install -g` |
| **Rust / Go** | `cargo install` · `go install` |
| **版控** | `git clone` |
| **AI 模型** | `ollama pull` · `huggingface-cli download` |
| **容器** | `docker pull` |
| **系统包** | `winget install` · `choco install` · `scoop install` |
| **通用** | `curl` · `wget` |

> 🧠 智能跳过 venv 内的 `pip install` — 不影响项目本地环境。

---

## ⚙️ 一个配置文件

`~/.workbuddy/skills/download-guard/config.md`

| 参数 | 默认 | 说明 |
|------|------|------|
| `DOWNLOAD_ROOT` | 首次配置设定 | 下载目标目录 |
| `MIN_FREE_GB` | `0.5` | 低于此值 → 阻止 |
| `WARN_FREE_GB` | `2` | 低于此值 → 警告 |
| `C_DRIVE_WARN_GB` | `5` | C 盘低于此值 → 额外提醒 |
| `LOG_RETENTION_DAYS` | `30` | 日志归档天数 |
| `LOG_ARCHIVE_MAX_MB` | `10` | 归档超此 → 删除 |

---

## 🔄 工作流

```
触发下载
  │
  ├─ 首次使用？ ──→ 引导配置（扫描磁盘→推荐最优路径→写配置→扫C盘缓存）
  │
  ├─ ① 读配置 → 验证配置完整性
  ├─ ② 路径分类 → 缓存(A) / 安装目录(B·需同步PATH) / 文件(C)
  ├─ ③ 重复检测 → 已存在 → 询问是否重下
  ├─ ④ 可用性检查 → 盘不存在 → 🚫 BLOCK（不走C盘）
  │               → 空间不足 → 🚫 BLOCK
  │               → 大文件   → ⚠️ WARN
  ├─ ⑤ 告知用户 → 文件+路径+磁盘状态
  ├─ ⑥ 执行下载
  └─ ⑦ 验证+记录 → 确认文件存在 → 写日志(自动清理) → 告知完成
```

---

## 🧰 脚本速览

| 脚本 | 功能 |
|------|------|
| `check-space.ps1` | 磁盘空间 + 路径可用性校验（盘不存在/不可写→exit 2 BLOCK） |
| `log-download.ps1` | 日志记录 + 超过30天自动归档 + 超10MB自动删除 |
| `scan-tool-cache.ps1` | 扫描 12+ 种工具缓存，标记 C 盘危险项 |
| `migrate-cache.ps1` | 一键迁移 C 盘缓存到目标盘 |

---

## ⚠️ 已知局限

| 局限 | 说明 |
|------|------|
| 仅 Windows | PowerShell 脚本，macOS/Linux 需装 PowerShell Core |
| nvm 管理的 Node | 切版本可能重置路径（nvm 自身机制） |
| `pip install --user` | 装到 C 盘用户 site-packages — 建议 venv |
| Docker 镜像 | Docker Desktop 用 WSL2 VHDX 管理 |
| 编译产物 | `cmake build`、`cargo build` 不在范围 |

---

## 🏗️ 项目结构

```
download-guard/
├── SKILL.md                ← 核心规则（Agent 加载）
├── reference.md             ← 详细参考
├── config.md                ← 用户配置（模板）
├── README.md                ← 本文件
├── CHANGELOG.md             ← 版本历史
├── LICENSE                  ← MIT-0
└── scripts/
    ├── check-space.ps1      ← 磁盘空间 + 路径校验
    ├── log-download.ps1     ← 日志 + 清理
    ├── scan-tool-cache.ps1  ← 缓存扫描
    └── migrate-cache.ps1    ← 缓存迁移
```

---

## 📜 版本历史

[CHANGELOG.md](CHANGELOG.md) — v1.0 到 v5.4 的完整迭代记录。

---

## 📄 许可证

[MIT-0](LICENSE) — 随便用，不署名也行。

---

## 🌟 如果这个 Skill 帮到了你

⭐ **Star 这个仓库** — 让更多被 C 盘困扰的人看到它

🐛 **遇到问题？** [开 Issue](https://github.com/nihaoljx/download-guard/issues)

💡 **有想法？** 欢迎 PR

📢 **帮忙推广？** 把这篇 README 分享给用 AI Agent 的朋友
