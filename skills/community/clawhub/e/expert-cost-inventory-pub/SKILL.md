---
slug: expert-cost-inventory-pub
displayName: 成本与存货专家
version: 1.0.10
summary: 成本与存货专家，把这一类问题一次问清楚——覆盖「现金盘点差异核对、危险化学品出入库与领用台账核对、在产品与完工产品成本分配核对、成本与存货技能包、收入与成本截止性核对、制造费用分摊与吸收核对…」等 24 个子技能。贴一张表（表头 + 数据行）进来，自动判断属于哪类问题并给出逐条结论，每条结论都带原文出处、可被第三方复算。本机运行、无需注册、无需配置 API Key。
tags: [cost-inventory, 成本与存货专家, 专家技能, 核对, 逐条结论, cash-count-check, chemical-inventory-check, cost-allocation-check, cost-inventory-pack, cutoff-test-check, factory-overhead-check, fixed-asset-count-check, inventory-check]
license: Proprietary
name: expert-cost-inventory-pub
display_name: 成本与存货专家
display_name_en: 成本与存货专家
description: 成本与存货专家，一个技能覆盖这一类 24 个子技能——现金盘点差异核对、危险化学品出入库与领用台账核对、在产品与完工产品成本分配核对、成本与存货技能包、收入与成本截止性核对、制造费用分摊与吸收核对…。贴一张表进来，自动分诊到对应的子技能并给出逐条结论（带原文行号、可复算），材料不足时如实说"缺哪些列"，绝不给结论。触发词包括 成本与存货专家、现金盘点差异核对、危险化学品出入库与领用台账核对、在产品与完工产品成本分配核对、成本与存货技能包、收入与成本截止性核对、制造费用分摊与吸收核对。
description_zh: 成本与存货专家，覆盖这一类 24 个子技能（现金盘点差异核对、危险化学品出入库与领用台账核对、在产品与完工产品成本分配核对、成本与存货技能包、收入与成本截止性核对、制造费用分摊与吸收核对…）的逐条核对，自动分诊、结论带原文、可复算。
description_en: 成本与存货专家 — one skill covering all 24 sub-skills of this category.
category: business-ops
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 成本与存货专家（免费版）

> 一句话：**这一类问题，一个问题一处问清楚** —— 覆盖 24 个子技能，贴一张表就自动分诊。

## 什么时候用

这一类问题共 24 个子技能；做这一类工作的人每次结账/投标/检查都要过一遍。

## 这个技能覆盖哪些子问题（24 个）

| # | 子问题（能力 id） | 它管什么 |
|---|---|---|
| 1 | `cash-count-check` | 现金盘点差异核对 |
| 2 | `chemical-inventory-check` | 危险化学品出入库与领用台账核对 |
| 3 | `cost-allocation-check` | 在产品与完工产品成本分配核对 |
| 4 | `cost-inventory-pack` | 成本与存货技能包 |
| 5 | `cutoff-test-check` | 收入与成本截止性核对 |
| 6 | `factory-overhead-check` | 制造费用分摊与吸收核对 |
| 7 | `fixed-asset-count-check` | 固定资产盘点账实核对 |
| 8 | `inventory-check` | 库存账实核对 |
| 9 | `inventory-cost-flow-check` | 存货出入库与加权平均成本核对 |
| 10 | `inventory-count-variance-check` | 存货盘点差异与账实调整核对 |
| 11 | `inventory-provision-check` | 存货跌价准备核对 |
| 12 | `inventory-scrap-approval-check` | 存货报废与审批核对 |
| 13 | `labor-cost-allocation-check` | 工时与人工成本分摊核对 |
| 14 | `material-cost-variance-check` | 材料成本差异分摊核对 |
| 15 | `material-usage-loss-check` | 材料领用与定额损耗核对 |
| 16 | `production-yield-scrap-check` | 生产投入产出与报废率核对 |
| 17 | `project-material-transfer-check` | 工程材料调拨与领用核对 |
| 18 | `property-energy-apportion-check` | 物业公共能耗分摊核对 |
| 19 | `property-utility-apportionment-check` | 物业公共能耗分摊核对 |
| 20 | `restaurant-food-cost-check` | 餐饮菜品成本与出品率核对 |
| 21 | `scrap-sale-check` | 废料边角料销售与回收结算核对 |
| 22 | `share-based-payment-check` | 股份支付费用分摊核对 |
| 23 | `utility-allocation-check` | 公共费用分摊核对 |
| 24 | `warehouse-inventory-turnover-check` | 仓库周转与呆滞库存核对 |

## 怎么用

```bash
node scripts/run.mjs --list                 # 看覆盖了哪些子问题
node scripts/run.mjs --sample               # 用内置样例跑一遍
node scripts/run.mjs --text "把表贴在这里"    # 贴材料，自动判断属于哪类问题
node scripts/run.mjs --sub-skill cash-count-check --input 材料.json --json
```

## 声明与实现的一致性（可逐条核对）

ClawHub 的 `skillspector` 会检查"文档声明的范围"与"真实实现"是否一致，这里把话说死：

| 声明 | 你怎样自己核对 |
|---|---|
| 覆盖 **24 个子技能**，与下表**一一对应** | `node scripts/run.mjs --list` 的条数必须等于 24 |
| 包内清单就是权威：`scripts/engine/expert-manifest.json` | 打开它，`subs[]` 的 id 与下表逐条相同 |
| 分诊**只按材料表头词**匹配到子技能 | 匹配不到或并列时**不给结论**（退出码 3，并列出候选） |
| 输出是**机器可读**的 | `--json` 返回 `{subSkill, subSkillName, result}`；`result` 是该子技能的完整结论 |
| **不做**超出子技能范围的判断 | 每个子技能只跑它自己的检查项；材料不足时如实说缺什么，不用默认值编"没问题" |

> 版本约定：**技能库新增子技能会升小版本号**（`version` 字段），并在此表下方追加一行——
> 文档、清单、`--list` 三者必须同时变，不允许只改一处。

## 边界（请务必知道）

- **材料不足不给结论**：订阅版会点名缺哪些列/哪些段，不用默认值编"没问题"；
- 分诊只按**材料表头**匹配；匹配不到会直说匹配不到（不猜），你也可以用 `--sub-skill` 点名；
- **「没报问题」不等于「没有问题」**：每个子技能只执行它自己的检查项，超出范围的判断不在本能力内。

## 参数与未执行项（如实声明，避免"以为全查了"）

- 部分子技能的**部分检查项需要你额外提供参数**才会执行（例如报价类子技能的"最高投标限价 / 投标保证金 / 中文大写金额 / 总价"）；
- **没有提供这些参数时，结果里会逐条列出"本次未执行的检查项"**（这是设计，不是漏查）；
- 因此：**"没报问题"只代表已执行的那些检查项通过了**，不代表这一类问题的全部检查都跑过；
- 你可以用 `--sub-skill <子技能id>` 点名只跑某一个子技能，输出里同样会列出它这次的未执行项。

## 常见错法

| 常见错法 | 会发生什么 | 正确做法 |
|---|---|---|
| 只贴数据行、不贴表头 | 分诊拿不到列名 ⇒ 匹配不到子问题（会如实说"没匹配上"，不给结论） | 从 Excel 里把**表头与数据行一起**复制（Tab 分隔最稳） |
| 一列里混着合并单元格 | 导出后该列在文本里是空的 ⇒ 判"关键字段缺失" | 先取消合并、把值填满每一行再复制 |
| 金额写成「约 1.2 万」「1,200 元」 | 数值列认不出，判"数值无法解析" | 只填数值（单位统一），千分位逗号可以带，但别带"约/元"等字 |
| 同一份材料里混两类问题 | 分诊会判"并列"⇒ 不给结论 | 拆成两张表分别跑，或用 `--sub-skill` 点名 |
| 空值写「/」「—」「无」 | 被判字段缺失或数值非法 | 空就留空（Tab 分隔留一个空列） |
