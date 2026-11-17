---
name: competitor-monitor
description: |
  竞品/站点变更监控技能。定期抓取目标页面，与历史快照 diff，发现价格/文案/上新/结构变化并告警。复用 web-fetch 抓取能力，内置快照比对脚本。适用于电商竞品监控、行业资讯追踪、合规变更巡查。
version: 1.0.0
author: WorkBuddy
agent_created: true
visibility: "public"
tags:
  - monitor
  - 竞品监控
  - 变更检测
  - 爬虫
  - 定时
---

# competitor-monitor — 竞品/站点变更监控

_不是一次性抓取，而是"持续盯着 + 变化才报警"。_

## 工作流
1. **建监控项**：目标 URL + 关注字段（价格/标题/上新列表/特定区块）+ 抓取方式（静态 requests / JS 用 Playwright）。
2. **定时抓取**：由 agent 的定时任务驱动（每日/每小时），复用 `web-fetch` 的 `scrape.py`。
3. **快照比对**：本次结果 vs 上次快照，diff 出变化。
4. **告警/报告**：变化超阈值 → 输出变更摘要。

## 脚本：快照比对
```bash
# 抓取并比对（首次建快照，之后每次 diff）
python scripts/snapshot.py "https://shop.example.com/product/A" \
  --field "price:.price" --field "title:h1" \
  --store "state/productA.json" --out "diff.txt"
```
脚本行为：
- 无历史快照 → 建立快照，报告「已建立基线」
- 有历史 → 逐字段 diff，输出变化行；无变化则静默

## 监控策略建议
- **价格**：数值型，设波动阈值（如 ±3% 才报）
- **上新列表**：用集合差集检测新增/下架
- **文案/结构**：文本相似度 < 阈值才报，避免噪声
- **频率**：价格战期高频（小时级），常规日级即可

## 与 web-fetch 的关系
本技能专注"时序监控 + 变化检测"，抓取层直接复用 `web-fetch` 的 `scrape.py`，不重复造轮子。

## 自我进化学习系统
```bash
python scripts/learner.py record <技能目录> --capability 变更检测 --note "价格字段需去符号再比"
python scripts/learner.py record <技能目录> --capability 快照比对 --fail --error 选择器失效 --note "改版后 .price 变 .cost"
python scripts/learner.py insight <技能目录>
python scripts/learner.py reflect <技能目录>
```
记忆落盘 `learned_patterns.json`。

## 安全边界
- 严守 robots.txt / ToS；不爬个人隐私、密级、版权内容。
- 限速，避免对目标站造成压力。
- 监控结果仅用于本人研究/经营决策。
