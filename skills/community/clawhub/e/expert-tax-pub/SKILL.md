---
slug: expert-tax-pub
displayName: 税务申报与筹划专家
version: 1.0.10
summary: 税务申报与筹划专家，把这一类问题一次问清楚——覆盖「农产品收购发票与进项抵扣核对、年终奖池分配与个税核对、企业所得税纳税调整核对、预缴企业所得税核对、递延所得税与暂时性差异核对、发票与单据合规技能包…」等 32 个子技能。贴一张表（表头 + 数据行）进来，自动判断属于哪类问题并给出逐条结论，每条结论都带原文出处、可被第三方复算。本机运行、无需注册、无需配置 API Key。
tags: [tax, 税务申报与筹划专家, 专家技能, 核对, 逐条结论, agri-purchase-invoice-deduction-check, bonus-pool-check, cit-adjustment-check, cit-prepay-check, deferred-tax-check, doc-compliance-pack, environmental-tax-check, export-rebate-check]
license: Proprietary
name: expert-tax-pub
display_name: 税务申报与筹划专家
display_name_en: 税务申报与筹划专家
description: 税务申报与筹划专家，一个技能覆盖这一类 32 个子技能——农产品收购发票与进项抵扣核对、年终奖池分配与个税核对、企业所得税纳税调整核对、预缴企业所得税核对、递延所得税与暂时性差异核对、发票与单据合规技能包…。贴一张表进来，自动分诊到对应的子技能并给出逐条结论（带原文行号、可复算），材料不足时如实说"缺哪些列"，绝不给结论。触发词包括 税务申报与筹划专家、农产品收购发票与进项抵扣核对、年终奖池分配与个税核对、企业所得税纳税调整核对、预缴企业所得税核对、递延所得税与暂时性差异核对、发票与单据合规技能包。
description_zh: 税务申报与筹划专家，覆盖这一类 32 个子技能（农产品收购发票与进项抵扣核对、年终奖池分配与个税核对、企业所得税纳税调整核对、预缴企业所得税核对、递延所得税与暂时性差异核对、发票与单据合规技能包…）的逐条核对，自动分诊、结论带原文、可复算。
description_en: 税务申报与筹划专家 — one skill covering all 32 sub-skills of this category.
category: business-ops
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 税务申报与筹划专家（免费版）

> 一句话：**这一类问题，一个问题一处问清楚** —— 覆盖 32 个子技能，贴一张表就自动分诊。

## 什么时候用

这一类问题共 32 个子技能；做这一类工作的人每次结账/投标/检查都要过一遍。

## 这个技能覆盖哪些子问题（32 个）

| # | 子问题（能力 id） | 它管什么 |
|---|---|---|
| 1 | `agri-purchase-invoice-deduction-check` | 农产品收购发票与进项抵扣核对 |
| 2 | `bonus-pool-check` | 年终奖池分配与个税核对 |
| 3 | `cit-adjustment-check` | 企业所得税纳税调整核对 |
| 4 | `cit-prepay-check` | 预缴企业所得税核对 |
| 5 | `deferred-tax-check` | 递延所得税与暂时性差异核对 |
| 6 | `doc-compliance-pack` | 发票与单据合规技能包 |
| 7 | `environmental-tax-check` | 环境保护税申报核对 |
| 8 | `export-rebate-check` | 出口退税核算核对 |
| 9 | `iit-annual-settlement-check` | 个税年度汇算（综合所得）核对 |
| 10 | `import-duty-check` | 进口税费核算核对 |
| 11 | `input-vat-deduction-check` | 增值税进项税额认证与抵扣核对 |
| 12 | `invoice-usage-stock-check` | 发票领用存与开票数据核对 |
| 13 | `land-appreciation-check` | 土地增值税预缴与清算核对 |
| 14 | `late-fee-check` | 税款滞纳金计算核对 |
| 15 | `property-tax-land-use-check` | 房产税与城镇土地使用税申报核对 |
| 16 | `rd-expense-check` | 研发费用加计扣除归集核对 |
| 17 | `royalty-settlement-check` | 版税与授权金结算核对 |
| 18 | `stamp-duty-base-check` | 印花税计税依据核对 |
| 19 | `surtax-check` | 增值税附加税费核对 |
| 20 | `tax-filing-pack` | 税务与涉税申报技能包 |
| 21 | `tax-incentive-eligibility-check` | 税收优惠适用条件自查核对 |
| 22 | `tax-invoice-void-check` | 发票作废与红冲核对 |
| 23 | `tax-monthly-selfcheck` | 税务月度自查包 |
| 24 | `tax-risk-benefit-pack` | 税费自查与优惠技能包 |
| 25 | `tax-risk-indicator-check` | 税务风险指标自查核对 |
| 26 | `three-way-match` | 三单匹配AI核对 |
| 27 | `ticket-revenue-check` | 票务收入与渠道结算核对 |
| 28 | `toll-processing-manual-check` | 加工贸易手册与保税料件核对 |
| 29 | `vat-burden-check` | 增值税进销项与税负率核对 |
| 30 | `vat-deduction-addon-check` | 增值税加计抵减核对 |
| 31 | `vat-filing-reconcile` | 增值税申报与账载开票三方核对 |
| 32 | `vat-input-transfer-out-check` | 进项税额转出核对 |

## 怎么用

```bash
node scripts/run.mjs --list                 # 看覆盖了哪些子问题
node scripts/run.mjs --sample               # 用内置样例跑一遍
node scripts/run.mjs --text "把表贴在这里"    # 贴材料，自动判断属于哪类问题
node scripts/run.mjs --sub-skill agri-purchase-invoice-deduction-check --input 材料.json --json
```

## 声明与实现的一致性（可逐条核对）

ClawHub 的 `skillspector` 会检查"文档声明的范围"与"真实实现"是否一致，这里把话说死：

| 声明 | 你怎样自己核对 |
|---|---|
| 覆盖 **32 个子技能**，与下表**一一对应** | `node scripts/run.mjs --list` 的条数必须等于 32 |
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
