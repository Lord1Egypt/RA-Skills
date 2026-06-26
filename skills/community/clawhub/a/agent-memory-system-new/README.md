# Agent Memory System 🧠

OpenClaw Agent 长期记忆系统 - 温度模型 + 自动归档 + 知识提炼

## 功能

- 🔥 **温度模型**: 热(<7天) / 温(7-30天) / 冷(>30天)
- 🗄️ **自动归档**: 每周日 00:00 执行 GC
- 💭 **夜间反思**: 每日 23:45 验证 + 统计
- 🔧 **技能提炼**: 从教训中提取可复用技能

## 安装

### 方式 1：一键安装（推荐）

```bash
# 1. 安装技能
clawhub install agent-memory-system

# 2. 运行安装脚本（自动配置）
cd ~/.openclaw/workspace/skills/agent-memory-system/scripts
./install.sh
```

安装脚本会：
- ✅ 自动创建记忆目录
- ✅ 复制模板文件
- ✅ 配置定时任务（可选）

### 方式 2：手动安装

```bash
clawhub install agent-memory-system

# 手动创建目录
mkdir -p ~/.openclaw/workspace/memory/{lessons,decisions,people,reflections,.archive}

# 手动配置 cron
crontab -e
# 添加:
# 0 0 * * 0 ~/.openclaw/workspace/skills/agent-memory-system/scripts/memory-gc.sh
# 45 23 * * * ~/.openclaw/workspace/skills/agent-memory-system/scripts/nightly-reflection.sh
```

## 文件结构

```
agent-memory-system/
├── .clawhub/origin.json    # Clawhub 元数据
├── _meta.json              # 技能元数据
├── SKILL.md                # 详细文档
├── README.md               # 本文件
├── scripts/
│   ├── memory-gc.sh        # 垃圾回收脚本
│   ├── nightly-reflection.sh  # 夜间反思脚本
│   └── extract-skill.sh    # 技能提取脚本
└── templates/
    ├── MEMORY-template.md  # MEMORY.md 模板
    ├── daily-log-template.md  # 每日日志模板
    └── lesson-template.md  # 教训模板
```

## 许可证

MIT