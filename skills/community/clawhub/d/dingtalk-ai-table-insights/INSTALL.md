# 安装指南 - dingtalk-ai-table-insights

## 前置要求

1. **OpenClaw** 已安装并配置
2. **dingtalk-ai-table** 技能已安装并完成 MCP 配置

```bash
# 安装依赖技能
clawhub install dingtalk-ai-table

# 配置 MCP（详见 dingtalk-ai-table 的配置文档）
```

---

## 安装方式（三选一）

### 方式一：Git 克隆（推荐）

```bash
# 克隆到 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://github.com/tomray4ai/dingtalk-ai-table-insights.git
```

### 方式二：下载 ZIP

1. 访问 https://github.com/tomray4ai/dingtalk-ai-table-insights
2. 点击 **Code** → **Download ZIP**
3. 解压到 `~/.openclaw/skills/dingtalk-ai-table-insights/`

### 方式三：手动复制

将 `dingtalk-ai-table-insights` 文件夹复制到：
- `~/.openclaw/skills/dingtalk-ai-table-insights/`
- 或你的 workspace `skills/` 目录

---

## 验证安装

```bash
# 检查技能文件是否存在
ls ~/.openclaw/skills/dingtalk-ai-table-insights/

# 应该看到：
# SKILL.md  README.md  SECURITY.md  scripts/  references/
```

---

## 使用方法

```bash
# 关键词筛选分析
python3 ~/.openclaw/skills/dingtalk-ai-table-insights/scripts/analyze_tables.py --keyword "销售"

# 全量扫描
python3 ~/.openclaw/skills/dingtalk-ai-table-insights/scripts/analyze_tables.py

# 查看帮助
python3 ~/.openclaw/skills/dingtalk-ai-table-insights/scripts/analyze_tables.py --help
```

---

## 配置 MCP

本技能复用 `dingtalk-ai-table` 的 MCP 配置。

配置文件位置：`~/.openclaw/config/mcporter.json`

如果未配置，请先安装并配置 `dingtalk-ai-table` 技能。

---

## 常见问题

### Q: 为什么不能从 ClawHub 安装？
A: 技能正在等待 ClawHub 审核发布（GitHub 账号需满 14 天）。预计发布日期：2026-03-17

### Q: 安装后无法运行？
A: 确认已安装 `dingtalk-ai-table` 技能并完成 MCP 配置。

### Q: 如何更新？
A: 如果是 git 克隆安装，运行 `git pull` 即可更新。

---

## 技术支持

- GitHub Issues: https://github.com/tomray4ai/dingtalk-ai-table-insights/issues
- 钉钉讨论群：（待添加）
