---
name: football-data
description: 足球数据库查询助手。查询积分榜、赛程赛果、球队球员数据、赛前H2H预览。纯信息查询不涉及博彩。触发词：足球积分榜、查赛程、球队信息、球员数据、足球数据、H2H、赛前分析、football standings、查排名、联赛数据。
agent_created: true
allowed-tools: Read, Write, Edit, Bash, WebFetch, WebSearch, Grep
---

# Football Data Hub - 足球数据库

⚽ 零配置足球数据查询技能。**立即可用**，无需任何 API Key。

## 数据源策略（三级降级）

1. **OpenLigaDB**（默认，零配置）— 完全免费无需认证，覆盖德甲/德乙/德丙/欧冠/欧联等主要联赛
2. **API-Football**（需配置 RapidAPI Key）— 1200+ 联赛，球员数据，实时比分，H2H
3. **football-data.org**（需配置 Key）— 12 大联赛，射手榜，比赛详情

## 零配置直接可用

```bash
# 积分榜
python scripts/fetch_football_data.py --endpoint standings --league "德甲" --season 2025

# 赛程/赛果
python scripts/fetch_football_data.py --endpoint fixtures --league "德甲" --season 2025
python scripts/fetch_football_data.py --endpoint fixtures --league "德甲" --matchday 1

# 球队搜索
python scripts/fetch_football_data.py --endpoint teams --search "Bayern"

# 球队列表
python scripts/fetch_football_data.py --endpoint teams --league "德甲"

# 联赛列表
python scripts/fetch_football_data.py --endpoint leagues --search "Champions"
```

## 支持联赛 (OpenLigaDB)

| 快捷名 | 联赛 | 状态 |
|--------|------|------|
| `bl1` / `德甲` | 德甲 2025/26 | ✅ 积分榜+赛程完整 |
| `bl2` | 德乙 | ✅ |
| `bl3` | 德丙 | ✅ |
| `dfb` | 德国杯 | ✅ |
| `ucl` / `欧冠` | 欧冠 | ✅ |
| `el` / `欧联` | 欧联 | ✅ |

💡 用 `--endpoint leagues` 查看完整列表

## 升级到 API-Football（可选）

配置 `config.yaml` 后可解锁：
- ✅ 球员数据（射手、助攻统计）
- ✅ H2H 历史交锋分析
- ✅ 英超、西甲、意甲、法甲等全球 1200+ 联赛
- ✅ 实时比分

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml 填入 RapidAPI Key
```

## 核心原则

- **纯信息查询，不涉及博彩预测** — 与 soccer-lottery 明确区分
- **零配置优先** — OpenLigaDB 无需任何 Key，开箱即用
- **中文友好** — 支持 `德甲` `欧冠` `欧联` 等中文名直接查询

## 触发词

查积分榜、查赛程、球队信息、球员数据、H2H、赛前分析、足球数据、查排名、联赛数据、football standings
