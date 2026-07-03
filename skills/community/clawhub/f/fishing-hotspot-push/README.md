# 🎣 Fishing Hotspot Push

钓鱼热点智能推送 — 多渠道聚合钓鱼情报，结合天气与位置，推送周边最佳钓点及实时鱼情。

## 核心能力

- 🌐 **多源聚合**: 高德POI + 和风天气 + 社交媒体文本NLP
- 🧠 **NLP引擎**: 钓鱼黑话识别、鱼种提取、情感分析
- 📊 **智能排序**: 距离 × 鱼获质量 × 天气条件 × 情报热度
- 📱 **可视化报告**: 深色主题HTML，热点卡片 + 天气条 + 评分可视化
- 🤝 **技能联动**: 与 [fishing-trip-planner](https://github.com/bettermen/fishing-trip-planner) 一键联动

## 快速开始

```bash
# 首次配置（自动共享 fishing-trip-planner 的 API Key）
python scripts/hotspot_push.py --setup

# 方式A: Agent搜索 + 脚本分析（推荐）
python scripts/hotspot_push.py --run --city "深圳" --input "搜索结果..."

# 方式B: 仅API数据
python scripts/hotspot_push.py --run --city "深圳"

# 查看历史
python scripts/hotspot_push.py --history
python scripts/hotspot_push.py --view 1
```

## 数据源

| 来源 | 用途 | 说明 |
|------|------|------|
| 高德地图 | 城市定位、周边水域POI | 需 API Key |
| 和风天气 | 钓鱼指数、7天预报 | 需 API Key |
| 社交文本 | 钓友分享、鱼获情报 | 通过 Agent WebSearch 传入 |

## 与 fishing-trip-planner 联动

```
fishing-hotspot-push → 发现"哪在出鱼" → 推荐Top 5钓点
        ↓
fishing-trip-planner → 用户选钓点 → 路线+天气+潮汐完整规划
```

## 配置共享

两个技能共用同一套 API Key（高德 + 和风）。如果已配置过 `fishing-trip-planner`，`fishing-hotspot-push` 会自动读取。

## 评分算法

```
综合评分 = 距离(30分) + 鱼获情报(35分) + 天气条件(25分) + 情报热度(10分)

≥80: 🔥 强烈推荐
≥60: 👍 推荐
≥40: 🤔 一般
<40: ⚠️ 暂不推荐
```

## 技能文件

```
fishing-hotspot-push/
├── SKILL.md              # WorkBuddy 技能定义
├── README.md
├── scripts/
│   └── hotspot_push.py   # 核心脚本 (~650行)
└── references/
    └── api_guide.md       # API 申请指南
```

## 技术栈

- Python 3.8+
- requests (HTTP)
- 高德地图 Web API
- 和风天气 API

## License

MIT
