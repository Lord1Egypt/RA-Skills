---
name: ecommerce-weekly-report
description: Turn messy weekly ecommerce performance data into an operator-ready report with KPI trends, winners, risks, and next-step recommendations. Use when teams need a concise weekly business review instead of raw spreadsheets.
---

# Ecommerce Weekly Report

把一周电商数据，整理成真正能拿去复盘和开会的周报。

## Problem it solves
原始报表通常只有数字，没有判断：
- GMV、订单、客单价在变，但没人解释为什么；
- 花费涨了，利润未必涨；
- 某个 SKU、渠道、达人、地区在拖后腿，但不容易一眼看出来；
- 团队最后拿到的是表，不是结论。

这个 skill 的目标是：
**把分散的周度经营数据，压缩成“核心指标 + 异动解释 + 下周动作”的管理周报。**

## Use when
- 需要做电商周报、经营复盘、例会材料
- 需要比较本周 vs 上周的关键指标变化
- 需要快速识别增长来源、利润压力和执行优先级

## Do not use when
- 用户只要单个指标计算，不需要完整周报
- 数据口径明显不一致且无法确认
- 需要财务审计级别的精细核对，而不是经营周报

## Inputs
- 本周和上周的核心经营数据
- 至少包含：销售额、订单数、客单价、广告/投放、退款、利润或毛利
- 可选维度：SKU、渠道、达人、地区、活动、流量来源
- 可选背景：本周活动、价格调整、库存、异常事件

## Workflow
1. 先确认统计周期和对比口径一致。
2. 提取核心 KPI，并计算环比变化。
3. 找出增长贡献项和拖累项。
4. 区分“表面增长”和“利润质量变化”。
5. 输出亮点、风险、原因假设和下周建议。

## Output
Return:
1. Report period and comparison basis
2. Core KPI summary
3. Highlights and problem areas
4. Key drivers / likely causes
5. Recommended actions for next week

## Quality bar
- 不只报数字，必须给经营解释
- 明确区分收入增长、效率改善、利润改善
- 结论要能支持周会讨论和动作分配
- 标明缺失数据、估算数据和低置信度判断

## Resource
See `references/output-template.md`.
