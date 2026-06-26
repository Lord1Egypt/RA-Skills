---
name: competitor-monitor-claw
description: 实时竞品监控虾 — 持续追踪竞品价格、评价与上新动作的情报哨兵。当以下情况时使用此 Skill：(1) 需要监控竞品价格变动并设置预警阈值；(2) 需要追踪竞品上新动态；(3) 需要分析竞品评价口碑（好评/差评关键词）；(4) 需要检测竞品促销活动；(5) 需要生成竞品周报/月报；(6) 用户提到"竞品监控"、"对手价格"、"竞品上新"、"竞品评价"、"价格预警"、"竞品分析"、"对手动态"、"市场情报"、"竞品报告"、"价格对比"、"竞品促销"、"对手口碑"、"竞争态势"、"盯盘"、"竞品追踪"。
---

# 实时竞品监控虾

竞品情报的长期哨兵 — 持续追踪对手价格、评价与上新动作，在对手调价/上新/口碑变化的第一时间做出反应。

## 核心工作流

### 1. 初始化竞品列表

首先确认用户的竞品数据。支持两种输入方式：

**方式 A：用户提供 CSV 文件**
```bash
python3 scripts/price_monitor.py add --csv ./config/competitors.csv
```

CSV 格式（参考 `references/platform-scraping-rules.md` 中的字段说明）：
```
name,platform,product_url,sku_id,alert_threshold,monitor_freq,owner
竞品A,jd,https://item.jd.com/xxx.html,100012345,0.05,daily,张三
```

**方式 B：用户自然语言描述**
→ 帮用户整理成 CSV 格式，再导入

### 2. 立即检查竞品价格

```bash
python3 scripts/price_monitor.py check
```

输出：当前价格、促销价、评分、评价数，以及触发阈值的价格预警。

> ⚠️ 当前脚本使用**模拟数据**演示工作流。实际部署时，需将 `simulate_fetch()` 函数替换为真实爬虫逻辑（参考 `references/platform-scraping-rules.md` 中各平台字段路径）。

### 3. 生成竞品报告

```bash
# 近 30 天报告
python3 scripts/price_monitor.py report --days 30

# 近 7 天报告
python3 scripts/price_monitor.py report --days 7
```

### 4. 查看变化事件

```bash
python3 scripts/price_monitor.py events --limit 20
```

### 5. 深度分析与洞察

当用户需要深度解读竞品数据时：
- 读取 `references/competitor-analysis-framework.md` — 价格策略、上新节奏、口碑对比分析方法论
- 读取 `references/industry-benchmarks.md` — 各品类价格波动基准、评分健康基准、大促日历

### 6. 推送预警到飞书

检测到价格变动超过阈值时，用 `message` 工具推送到飞书：

```
⚠️ 竞品价格预警
竞品：{name} [{platform}]
变动：↓降价 8.3%  ¥299 → ¥274
时间：2026-04-09 14:30
建议：检查是否大促活动，参考行业基准判断是否跟进
```

## 数据存储

脚本使用 SQLite 存储历史数据，路径：`data/competitor_monitor.db`

表结构：`competitors`（竞品列表）、`price_history`（价格快照）、`change_events`（变化事件）

详细 schema 见 `references/platform-scraping-rules.md`。

## 与其他虾协作

- **策略顾问虾**（strategy-advisor-claw）：将竞品报告传给策略顾问，获取应对建议
- **数据分析虾**（auto-data-analysis-claw）：深度分析价格趋势数据
- **跨平台消息推送虾**（cross-platform-messenger-claw）：将预警推送到多渠道

## 局限说明

- 当前采集为模拟数据，实际部署需接入真实爬虫
- 部分平台有反爬机制，采集频率不能过高（参考 `references/platform-scraping-rules.md`）
- 价格为公开展示价，不含会员专属价或私下补贴
- 大促期间价格波动需结合 `references/industry-benchmarks.md` 中的大促日历过滤
