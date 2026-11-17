---
name: caopan-baodian
description: |
  当用户询问《股票操盘宝典》相关内容，或在中国A股交易领域寻求操作指导时调用:
  市况判定(现在是什么市况/牛熊震荡)、选股(怎么选牛股/大牛股必要条件)、技术买卖点(MACD/KDJ/DMI怎么看/金叉死叉)、 风险控制与资金管理(仓位/止损/避免贪婪)、操作系统(有没有一套可执行规则)、择时vs择股分工、股市二元论决策、 缠论式结构与三类买卖点、右侧确认进场。
  不适用于: 具体个股的确定性涨跌预测、荐股、加杠杆的激进建议、以及任何把"周期尾数/天干地支"当作可靠预测工具的用法。
  Triggers: 股票操盘宝典/胡斐/A股/牛市/熊市/择时/择股/买点/卖点/仓位/止损/MACD/KDJ/DMI/大牛股
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.caopan-baodian
  cangjie.capability-count: 10
  cangjie.entrypoint-count: 1
---
# 《股票操盘宝典》 — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 具体个股的未来涨跌预测、荐股
- 加杠杆、借钱抄底等激进操作建议（本书自身也反对）
- 把天干地支/年份尾数等"股市推背图"当作可靠预测工具
- 已注册制/机构化/量化主导下的现代A股生态的全量适配（本书基于2014-2015经验）

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 判大势(市况/周期)→定思维(9类操作思维/二元论)→入牛股(选股四要素)，层层递进构成完整操盘流程。
2. 择时解决"干不干"(负责风控)，择股解决"买哪只买多少"(负责收益)，二者责任正交不可混淆。
3. 所有交易错误几乎都源于贪婪，恐惧最多至踏空/少赚；风控=把利润取出来+仓位上限+年度纪律。
4. 不同市况(牛/熊/震荡/短线)必须用不同思维，绝不混用两套打法；先定市况再谈动作。
5. 只在买点/卖点(技术指标确定的位置)动作，不处买卖点就不操作；靠系统信号而非临场感觉。

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 现在是什么市况/牛市还是熊市；判断大盘处于周期哪个阶段；该不该进场/空仓该看什么信号 | references/capabilities/market-phase-detection.md | references/capabilities/stock-selection.md、references/capabilities/buy-sell-points.md、references/capabilities/decision-paradox.md |
| 怎么选股/怎么选出大牛股；我这只看似不错的股票值不值得进自选池；建立自己的自选池 | references/capabilities/stock-selection.md | references/capabilities/buy-sell-points.md、references/capabilities/market-phase-detection.md、references/capabilities/timing-vs-selection.md |
| 现在该买还是该卖/这是买点吗；MACD/KDJ金叉能不能进；怎么判断趋势/背离 | references/capabilities/buy-sell-points.md | references/capabilities/market-phase-detection.md、references/capabilities/structural-trading.md、references/capabilities/half-position-confirm.md |
| 怎么控制风险/控制仓位；该不该止损/怎么设置止损；赚了钱要不要落袋/怎么管理资金 | references/capabilities/risk-position-management.md | references/capabilities/buy-sell-points.md、references/capabilities/decision-paradox.md、references/capabilities/trading-system.md |
| 我到底该先学择时还是择股；亏钱是择时还是择股的问题；择时和择股有什么区别 | references/capabilities/timing-vs-selection.md | references/capabilities/market-phase-detection.md、references/capabilities/stock-selection.md、references/capabilities/thinking-matrix.md |
| 我该用长线还是短线思维；定操作思路/操作周期；怎么避免高抛低吸的思维混乱 | references/capabilities/thinking-matrix.md | references/capabilities/market-phase-detection.md、references/capabilities/timing-vs-selection.md、references/capabilities/risk-position-management.md |
| 持股还是持币/该不该保留；预测还是应对/怎么取舍；双双对立该选哪个 | references/capabilities/decision-paradox.md | references/capabilities/market-phase-detection.md、references/capabilities/risk-position-management.md、references/capabilities/buy-sell-points.md |
| 怎么建立一个交易系统；我这样交易算不算有系统；系统信号/买卖点执行 | references/capabilities/trading-system.md | references/capabilities/buy-sell-points.md、references/capabilities/risk-position-management.md |
| 缠论该怎么用/分型笔中枢；三类买卖点怎么判断；一笔/线段划分 | references/capabilities/structural-trading.md | references/capabilities/buy-sell-points.md |
| 该不该抢最低点/最佳买入点；怎么确认买点成立/左侧还是右侧；熊市怎么抄底 | references/capabilities/half-position-confirm.md | references/capabilities/buy-sell-points.md、references/capabilities/stock-selection.md |

**非能力类查询**：
- 书名/作者/章节/整书概览 → references/overview.md
- 术语解释 → references/glossary.md
- 决策规则速查（不需要原文依据时） → references/cheatsheet.md
- 完整意图与关键词索引（本表未覆盖的意图先查这里） → references/capability-index.md

## 加载规则

- 每次任务先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨域时最多加载 2 张。
- 概览/书名类问题不加载能力卡，用「核心原则」与 overview.md 回答。
- 路由表与 capability-index.md 都无法命中的意图，明确告知超出本书范围，不要硬套。

## 边界与判停

- 用户套用国外大师名言(stop)时，回到"中国A股独特"前提并提醒止损纪律。
- 涉及加杠杆/重仓/满仓的激进建议→停止，强调风控仓位上限。
- 纯书信息查询(书名/作者/目录)→用概述回答后即停，不展开操作建议。
