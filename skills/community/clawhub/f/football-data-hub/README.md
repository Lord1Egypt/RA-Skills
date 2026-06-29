# ⚽ Football Data Hub

零配置足球数据查询技能 — 积分榜、赛程赛果、球队信息，开箱即用无需 API Key。

## 🚀 零配置，立即可用

无需注册、无需 API Key。基于 [OpenLigaDB](https://api.openligadb.de/) 免费公开数据。

```bash
# 德甲积分榜
python scripts/fetch_football_data.py --endpoint standings --league "德甲" --season 2025

# 德甲最新赛果（自动显示最新完成的轮次）
python scripts/fetch_football_data.py --endpoint fixtures --league "德甲" --season 2025

# 指定轮次
python scripts/fetch_football_data.py --endpoint fixtures --league "德甲" --matchday 1

# 球队搜索
python scripts/fetch_football_data.py --endpoint teams --search "Bayern"

# 联赛列表
python scripts/fetch_football_data.py --endpoint leagues --search "Champions"
```

## 📦 安装

```bash
pip install requests pyyaml
```

## 📊 支持的功能

| 功能 | 零配置 | API Key |
|------|--------|---------|
| 积分榜（德甲/德乙/德丙/欧冠/欧联） | ✅ | ✅ |
| 赛程赛果 | ✅ | ✅ |
| 联赛列表 | ✅ | ✅ |
| 球队搜索 | ✅ | ✅ |
| 球员数据 | ❌ | ✅ |
| H2H 历史交锋 | ❌ | ✅ |
| 实时比分 | ❌ | ✅ |
| 英超/西甲/意甲/法甲/中超等 | ❌ | ✅ |

## 🔑 升级（可选）

配置 API Key 可解锁 1200+ 联赛 + 球员数据 + H2H：

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml 填入 RapidAPI Key
# 注册: https://rapidapi.com/api-sports/api/api-football
```

## 🏗️ 架构

```
football-data/
├── SKILL.md                # WorkBuddy 技能定义
├── README.md
├── config.example.yaml     # API Key 配置模板
├── requirements.txt
├── references/
│   └── leagues.md          # 100+ 联赛映射表
└── scripts/
    ├── fetch_football_data.py  # 核心数据获取（三级数据源降级）
    └── match_preview.py        # H2H 赛前预览分析
```

三级数据源自动降级：`OpenLigaDB → API-Football → football-data.org`

## 🎯 与 soccer-lottery 的区别

- **football-data**: 纯信息查询，不涉及博彩预测
- **soccer-lottery**: 足彩分析助手，赔率分析 + 信心指数

## 📄 License

MIT
