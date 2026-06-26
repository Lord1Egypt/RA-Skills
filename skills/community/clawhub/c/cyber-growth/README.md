# Cyber Growth - 神经成长协议

赛博朋克风格的成长追踪系统，量化你的每一次进步。

## 快速开始

```bash
# 记录一次成长
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh record "学会了飞书 Bitable API" --domain api --xp 50 --type new-chrome

# 查看状态
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh status

# 查看技能树
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh tree
```

## 效果预览

```
╔══════════════════════════════════════════╗
║  🔮 NEURAL INTERFACE v1.0               ║
╠══════════════════════════════════════════╣
║  Host: Boss  Title: 网格潜行者
║  Chrome Level: 6  ██████░░░░  58%
║  Neural Load: 1,240 XP  │  DataStream: 3 days
╠══════════════════════════════════════════╣
║  🧠 CORTEX AUGMENTS
║  Automation Rig     Lv.6  ████████░░  820XP
║  Security Shell     Lv.4  █████░░░░░  280XP
║  API Protocol       Lv.3  ████░░░░░░  140XP
╠══════════════════════════════════════════╣
║  📡 RECENT TRANSMISSIONS
║  +80XP | 发布 privacy-scanner v1.1.0 | [NEW CHROME]
║  +40XP | 端口冲突修复 → gateway-start | [PATCH]
╚══════════════════════════════════════════╝
```

## 文件结构

```
cyber-growth/
├── SKILL.md              # 触发逻辑 + 使用说明
├── README.md             # 本文件
├── scripts/
│   └── grow.sh           # 主脚本
└── references/
    ├── skill-tree.md     # 技能树定义
    ├── protocols.md      # 里程碑协议
    └── cyber-lexicon.md  # 赛博词汇表
```

## 数据文件

`~/.openclaw/memory/cyber-growth.json` — JSON 格式，包含所有成长记录、XP、领域等级。
