# 📋 CodeBuddy Daily Report Skill

[中文](#中文说明) | [English](#english)

> 一键生成每日工作日报的 CodeBuddy Skill —— 自动发现所有 Git 仓库、采集多分支提交记录、汇总 AI Agent 工作记录。

---

## 中文说明

### ✨ 功能特性

- 🔍 **零配置自动发现** — 扫描整个 HOME 目录，自动找到所有 Git 仓库（实测 66+ 个仓库，< 2 秒）
- 🌿 **多仓库多分支** — `git log --all` 跨所有分支采集，不漏掉任何提交
- 📅 **灵活的日期选择** — 今天 / 昨天 / 前天 / 任意日期，一句话搞定
- 🤖 **AI 辅助记录** — 自动采集 CodeBuddy Agent session 概览
- 🖥️ **跨平台** — macOS / Linux / Windows 全兼容
- 📦 **零依赖** — 仅需 Python 3.6+ 标准库 + Git CLI

### 📦 安装

**一行命令安装：**

```bash
git clone https://github.com/disyli/codebuddy-daily-report.git ~/.codebuddy/skills/daily-report
```

**手动安装：**

1. 下载本仓库
2. 将整个目录复制到 `~/.codebuddy/skills/daily-report`
3. 确保目录结构如下：

```
~/.codebuddy/skills/daily-report/
├── SKILL.md              ← Skill 指令文件（必须）
├── scripts/
│   └── collect.py        ← 数据采集脚本
├── assets/
│   └── template.md       ← 日报模板
└── references/
    └── config.yaml       ← 可选配置
```

### 🚀 使用方式

在 CodeBuddy 对话中直接说：

| 你说的话 | 效果 |
|---------|------|
| `帮我生成今天的工作日报` | 生成今天的日报 |
| `生成昨天的工作日报` | 生成昨天的日报 |
| `帮我看看前天做了什么` | 生成前天的日报 |
| `生成 2026-03-20 的工作日报` | 生成指定日期的日报 |

### ⚙️ 可选配置

编辑 `references/config.yaml` 可以：

- 指定 Git 作者名（默认自动检测）
- 添加额外的搜索路径（如外置硬盘）
- 添加排除目录（加速扫描）
- 调整搜索深度

大部分场景 **不需要修改任何配置**。

### 📄 生成效果示例

```markdown
# 工作日报 - 2026-03-24（周二）

## 📊 今日概览
| 指标 | 数据 |
|------|------|
| 活跃仓库 | 1 个 |
| 总提交数 | 3 次 |
| 代码变更 | +670 -311，涉及 34 个文件 |

## 🔧 项目详情
### iwiki-ai-plus
| 时间 | 分支 | 提交说明 |
|------|------|---------|
| 17:24 | feature/mysql-read-write-splitting | other: 日志修复 |
| 17:06 | feature/log-fix | other: 日志修复 |
| 17:01 | — | feat: MySQL 读写分离架构改造 |

## 📝 今日总结
核心工作是 MySQL 读写分离架构改造...
```

### 🔧 脚本独立使用

采集脚本也可以脱离 CodeBuddy 独立运行：

```bash
# 今天
python3 scripts/collect.py

# 昨天
python3 scripts/collect.py --yesterday

# 指定日期
python3 scripts/collect.py --date 2026-03-20

# N 天前
python3 scripts/collect.py --days-ago 3
```

输出为结构化 JSON，可供其他工具消费。

---

## English

### ✨ Features

- 🔍 **Zero-config auto-discovery** — Scans entire HOME directory, finds all Git repos automatically (66+ repos in < 2s)
- 🌿 **Multi-repo, multi-branch** — `git log --all` across all branches, never miss a commit
- 📅 **Flexible date selection** — Today / yesterday / N days ago / any specific date
- 🤖 **AI session tracking** — Automatically collects CodeBuddy Agent session overviews
- 🖥️ **Cross-platform** — macOS / Linux / Windows
- 📦 **Zero dependencies** — Python 3.6+ stdlib only + Git CLI

### 📦 Installation

**One-liner:**

```bash
git clone https://github.com/disyli/codebuddy-daily-report.git ~/.codebuddy/skills/daily-report
```

**Manual:**

1. Download this repository
2. Copy the entire directory to `~/.codebuddy/skills/daily-report`

### 🚀 Usage

Talk to CodeBuddy naturally:

| What you say | What happens |
|-------------|-------------|
| `Generate today's daily report` | Report for today |
| `Generate yesterday's work report` | Report for yesterday |
| `What did I do 3 days ago?` | Report for 3 days ago |
| `Generate report for 2026-03-20` | Report for specific date |

### 🔧 Standalone Script

The collection script works independently:

```bash
python3 scripts/collect.py                    # today
python3 scripts/collect.py --yesterday        # yesterday
python3 scripts/collect.py --date 2026-03-20  # specific date
python3 scripts/collect.py --days-ago 3       # N days ago
```

Outputs structured JSON to stdout.

---

## 📁 Project Structure

```
├── SKILL.md              # Skill instruction file (required by CodeBuddy)
├── scripts/
│   └── collect.py        # Cross-platform data collection script
├── assets/
│   └── template.md       # Report markdown template
├── references/
│   └── config.yaml       # Optional configuration
├── README.md             # This file
└── LICENSE               # MIT License
```

## 🤝 Contributing

PRs welcome! Some ideas:

- [ ] Support more AI assistants (Cursor, Windsurf, etc.)
- [ ] HTML/PDF export
- [ ] Weekly/monthly summary mode
- [ ] Slack/DingTalk/WeCom webhook integration

## 📄 License

[MIT](LICENSE)
