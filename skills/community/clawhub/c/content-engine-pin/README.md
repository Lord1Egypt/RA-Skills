# Content Engine 内容工厂

用 OpenClaw + Obsidian 搭建系统化的内容生产工厂。

## 快速开始

### 1. 安装依赖

```bash
# 安装 Obsidian
https://obsidian.md

# 安装 OpenClaw
clawdhub install openclaw-multiagent

# 安装本技能
ln -sf /path/to/content-engine ~/.claude/skills/content-engine
```

### 2. 初始化 Obsidian 库

```bash
# 创建目录结构
mkdir -p Content-Factory/{001-Inbox,002-Ideas,003-Templates,004-Drafts,005-Scheduled,006-Published,007-Analytics,008-Assets,009-Archive}
```

### 3. 启动创作

```bash
# 使用技能命令
/content-create 选题标题

# 或
/content-daily-scan

# 或
/content-weekly-review
```

## 核心工作流

```
选题 → 创作 → 分发 → 数据分析 → 复盘优化
  ↑                                    ↓
  └────────── 知识库沉淀 ←─────────────┘
```

## 目录

- **选题系统**: 热点追踪、选题库、竞品分析
- **创作系统**: 爆文框架、AI 辅助、人工润色
- **Obsidian 架构**: 知识库结构、模板
- **分发系统**: 多平台适配、排期管理
- **数据系统**: 核心指标、A/B 测试
- **OpenClaw 集成**: 自动化工作流

## 爆文公式

```
热点 + 痛点 + 独特视角 = 爆款
```

## 技能命令

| 命令 | 功能 |
|------|------|
| `/content-create` | 创建新内容 |
| `/content-daily-scan` | 每日热点扫描 |
| `/content-weekly-review` | 周数据复盘 |
| `/content-idea` | 添加选题到库 |

## 参考

- Obsidian 插件: Dataview, Templater, Periodic Notes
- 对标工具: 新榜、蝉妈妈、5118
- 设计工具: Canva、稿定设计

---

*让爆文从偶然变成必然。*
