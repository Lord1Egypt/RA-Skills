# 📊 dingtalk-ai-table-insights

> 钉钉 AI 表格跨表格洞察分析 - 让 AI 帮你从多个表格中发现洞察、识别风险、给出建议

## 快速开始

### 前提条件

⚠️ **本技能依赖 `dingtalk-ai-table` 技能及其 MCP 配置**

### 1. 安装依赖技能

```bash
# 先安装基础技能（负责 MCP 配置）
clawhub install dingtalk-ai-table

# 配置 MCP（一次配置）
# 详见：~/.openclaw/skills/dingtalk-ai-table/references/configuration.md
```

### 2. 安装本技能

**⚠️ 注意：** 由于 GitHub 账号发布限制，本技能暂未在 ClawHub 上架。请使用以下方式之一安装：

#### 方式 A：手动安装（推荐）

```bash
# 克隆或下载本仓库到本地
git clone https://github.com/tomray4ai/dingtalk-ai-table-insights.git

# 复制到 OpenClaw 技能目录
cp -r dingtalk-ai-table-insights ~/.openclaw/skills/

# 或者直接使用 workspace 中的版本（开发模式）
# 技能已位于：~/openclaw/workspace/
```

#### 方式 B：等待 ClawHub 上架（14 天后）

```bash
clawhub install dingtalk-ai-table-insights
```

### 3. 使用方式

在 OpenClaw 中直接使用自然语言对话：

```
# 分析特定项目
帮我使用 dingtalk-ai-table-insights 技能，分析一下"华东 XX 项目"相关的表格情况

# 销售数据分析
帮我分析一下销售相关的表格，看看有什么风险和机会

# 招聘进展
分析一下招聘相关的表格情况

# 全局扫描
帮我扫描所有表格，给出整体洞察
```

---

## 📋 配置说明

**MCP 配置由 `dingtalk-ai-table` 技能管理**

本技能复用其配置，无需重复配置。

详见：
- `references/architecture.md` - 架构说明
- `references/configuration.md` - 配置指南

---

## 🏗️ 架构

```
dingtalk-ai-table-insights (分析)
    ↓
dingtalk-ai-table (数据 + 配置)
    ↓
钉钉 AI 表格 MCP
```

## 核心功能

- 🔍 **关键词筛选** - 专注特定业务/项目
- 📊 **跨表格分析** - 发现单一表格看不到的关联
- 🚨 **风险预警** - 主动识别问题
- 📋 **行动建议** - 给出可执行的方案

## 使用场景

| 场景 | 示例对话 |
|------|------|
| 销售分析 | "分析一下销售相关的表格" |
| 项目追踪 | "帮我看看华东项目相关的表格情况" |
| 招聘分析 | "分析一下招聘相关的表格" |
| 全局扫描 | "扫描所有表格，给出整体洞察" |

## 安全说明

- ✅ **只读操作** - 不修改任何数据
- ✅ **本地分析** - 数据不出本地
- ✅ **权限最小化** - 仅需读取权限
- ✅ **数据抽样** - 每表最多 50 条

详细安全说明见 [SKILL.md](SKILL.md)

## 文档

- [完整技能说明](SKILL.md)
- [设计愿景](VISION.md)
- [使用示例](references/examples.md)
- [快速开始](references/quickstart.md)

## 依赖

- Python 3.7+
- **dingtalk-ai-table** skill - 钉钉 AI 表格操作技能
- 钉钉 AI 表格 MCP token

### 安装依赖技能

```bash
# 安装 dingtalk-ai-table
clawhub install dingtalk-ai-table

# 验证安装
clawhub list
```

## 许可证

MIT License
