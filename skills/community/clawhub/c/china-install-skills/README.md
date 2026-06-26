# China Install Skills 🇨🇳

[![GitHub Release](https://img.shields.io/github/v/release/5145852587/china-install-skills)](https://github.com/5145852587/china-install-skills/releases)
[![ClawHub](https://img.shields.io/badge/ClawHub-china--install--skills-blue)](https://clawhub.com/skills?q=china-install-skills)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow)](LICENSE)
[![Auto Publish](https://github.com/5145852587/china-install-skills/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/5145852587/china-install-skills/actions/workflows/auto-publish.yml)

**中国大陆专用 ClawHub 技能安装工具 - 绕过 API 限流**

## 🌟 特性

- 🚀 **绕过限流** - 直连 Convex API，不受 clawhub.com 限流影响
- 🔍 **搜索技能** - 快速搜索 ClawHub 技能市场
- 📥 **下载技能** - 自动下载技能 ZIP 包
- 📦 **安装技能** - 一键安装到指定 Agent
- ⚡ **一键安装** - 搜索 + 下载 + 安装全自动
- 🔄 **自动更新** - 支持每周自动检查更新
- ⏰ **自动配置** - 一键配置 crontab 定时任务
- 🤖 **CI/CD** - GitHub Actions 自动发布到 ClawHub

## 📦 安装

### 从 ClawHub 安装（推荐）
```bash
# 使用 clawhub CLI
clawhub install china-install-skills

# 或使用本技能自身安装（自举）
cd /path/to/china-install-skills/scripts
./quick-install.sh china-install-skills /your/agent/skills
```

### 从源码安装
```bash
git clone https://github.com/5145852587/china-install-skills.git
cd china-install-skills
cp -r . /your/agent/skills/china-install-skills/
```

## 🚀 快速开始

### 搜索技能
```bash
cd /path/to/china-install-skills/scripts
./search.sh weather 10
```

### 下载技能
```bash
./download.sh agile-toolkit
```

### 安装技能
```bash
./install.sh agile-toolkit /path/to/agent/skills --force
```

### 一键安装
```bash
./quick-install.sh "github cli" /path/to/agent/skills
```

### 自动更新检查
```bash
./auto-update.sh /path/to/workspace
```

## 📖 使用示例

### 示例 1: 安装天气技能
```bash
./quick-install.sh weather /Users/xubangbang/.openclaw/workspace/agents/MAIN/skills
```

### 示例 2: 安装 GitHub 相关技能
```bash
./quick-install.sh github-cli /Users/xubangbang/.openclaw/workspace/agents/SKILL-01/skills
./quick-install.sh github-actions /Users/xubangbang/.openclaw/workspace/agents/DEV-01/skills
```

### 示例 3: 自动配置定时任务（推荐🌟）
```bash
# 安装后自动配置每周检查更新
cd /path/to/china-install-skills/scripts
./setup-cron.sh

# 查看已配置的定时任务
crontab -l

# 移除定时任务
./setup-cron.sh --remove
```

### 示例 4: 手动设置每周自动更新
```bash
# 添加到 crontab（每周日 3:00）
crontab -e
0 3 * * 0 /path/to/china-install-skills/scripts/auto-update.sh
```

## 🔧 技术实现

### API 端点
- **搜索 API**: `https://wry-manatee-359.convex.site/api/v1/skills?q=<query>`
- **下载 API**: `https://wry-manatee-359.convex.site/api/v1/download?slug=<slug>`

### 为什么能绕过限流？
ClawHub 的前端网页和 CLI 使用 `clawhub.com` API（对中国大陆限流），但实际后端数据存储在 Convex。本技能直接访问 Convex API，绕过 clawhub.com 的限流层。

## 📁 目录结构

```
china-install-skills/
├── .github/
│   └── workflows/
│       └── auto-publish.yml    # GitHub Actions 自动发布
├── scripts/
│   ├── search.sh               # 搜索技能
│   ├── download.sh             # 下载 ZIP
│   ├── install.sh              # 安装技能
│   ├── quick-install.sh        # 一键安装
│   └── auto-update.sh          # 自动更新检查
├── SKILL.md                    # 技能使用说明
├── README.md                   # 本文件
├── _meta.json                  # 版本信息
├── PUBLISH.md                  # 发布指南
└── LICENSE                     # MIT-0 许可证
```

## 🤖 自动发布流程

本仓库配置了 GitHub Actions，当推送版本标签时自动发布到 ClawHub：

```bash
# 1. 更新版本号（编辑 _meta.json）
# 2. 提交并推送标签
git tag v1.0.1
git push origin v1.0.1

# 3. GitHub Actions 自动执行：
#    - 安装 ClawHub CLI
#    - 登录 ClawHub
#    - 发布新版本到 ClawHub
```

### 配置 Secrets

在 GitHub 仓库设置中添加：
- `CLAWHUB_TOKEN`: ClawHub API Token（通过 `clawhub login` 获取）

## 🔒 安全特性

- ✅ **只从官方域名下载** - convex.site (ClawHub 官方 CDN)
- ✅ **下载后验证 ZIP** - 确保不是 HTML 或恶意文件
- ✅ **安装前扫描** - 检查危险脚本
- ✅ **最小权限** - 不需要 sudo，只在 workspace 内操作

## 📊 与官方 clawhub CLI 对比

| 功能 | clawhub CLI | china-install-skills |
|------|-------------|----------------------|
| 搜索 | ❌ 中国大陆限流 | ✅ 直连 Convex API |
| 下载 | ❌ 中国大陆限流 | ✅ 直连 Convex CDN |
| 安装 | ✅ 自动 | ✅ 手动脚本 |
| 更新 | ✅ 自动 | ✅ 定时任务 |
| 依赖 | npm/node | bash/curl/unzip |
| CI/CD | ❌ | ✅ GitHub Actions |

## 📝 版本历史

- **v1.0.0** (2026-03-16) - 初始版本
  - 搜索功能（Convex API）
  - ZIP 下载
  - 本地安装
  - 一键安装
  - 每周自动更新检查
  - GitHub Actions 自动发布

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT-0 - 免费使用、修改、分发，无需署名

## 👤 作者

**奶龙·主理人** - 个人 AI 助理

## 🔗 链接

- [GitHub 仓库](https://github.com/5145852587/china-install-skills)
- [ClawHub 页面](https://clawhub.com/skills?q=china-install-skills)
- [OpenClaw 文档](https://docs.openclaw.ai)
