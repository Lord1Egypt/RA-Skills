---
slug: expert-retail-pub
displayName: 零售与门店经营专家
version: 1.0.10
summary: 零售与门店经营专家，把这一类问题一次问清楚——覆盖「广告代理返点与框架返点核对、连锁加盟门店结算核对、寄售代销结算核对、加盟保证金与费项结算核对、加盟抽成与最低保底核对、酒店夜审与房费收入核对…」等 17 个子技能。贴一张表（表头 + 数据行）进来，自动判断属于哪类问题并给出逐条结论，每条结论都带原文出处、可被第三方复算。本机运行、无需注册、无需配置 API Key。
tags: [retail, 零售与门店经营专家, 专家技能, 核对, 逐条结论, ad-agency-rebate-check, chain-store-settlement-check, consignment-settlement-check, franchise-deposit-check, franchise-royalty-check, hotel-night-audit-check, membership-liability-check, oem-rebate-policy-check]
license: Proprietary
name: expert-retail-pub
display_name: 零售与门店经营专家
display_name_en: 零售与门店经营专家
description: 零售与门店经营专家，一个技能覆盖这一类 17 个子技能——广告代理返点与框架返点核对、连锁加盟门店结算核对、寄售代销结算核对、加盟保证金与费项结算核对、加盟抽成与最低保底核对、酒店夜审与房费收入核对…。贴一张表进来，自动分诊到对应的子技能并给出逐条结论（带原文行号、可复算），材料不足时如实说"缺哪些列"，绝不给结论。触发词包括 零售与门店经营专家、广告代理返点与框架返点核对、连锁加盟门店结算核对、寄售代销结算核对、加盟保证金与费项结算核对、加盟抽成与最低保底核对、酒店夜审与房费收入核对。
description_zh: 零售与门店经营专家，覆盖这一类 17 个子技能（广告代理返点与框架返点核对、连锁加盟门店结算核对、寄售代销结算核对、加盟保证金与费项结算核对、加盟抽成与最低保底核对、酒店夜审与房费收入核对…）的逐条核对，自动分诊、结论带原文、可复算。
description_en: 零售与门店经营专家 — one skill covering all 17 sub-skills of this category.
category: business-ops
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 零售与门店经营专家（免费版）

> 一句话：**这一类问题，一个问题一处问清楚** —— 覆盖 17 个子技能，贴一张表就自动分诊。

## 什么时候用

这一类问题共 17 个子技能；做这一类工作的人每次结账/投标/检查都要过一遍。

## 这个技能覆盖哪些子问题（17 个）

| # | 子问题（能力 id） | 它管什么 |
|---|---|---|
| 1 | `ad-agency-rebate-check` | 广告代理返点与框架返点核对 |
| 2 | `chain-store-settlement-check` | 连锁加盟门店结算核对 |
| 3 | `consignment-settlement-check` | 寄售代销结算核对 |
| 4 | `franchise-deposit-check` | 加盟保证金与费项结算核对 |
| 5 | `franchise-royalty-check` | 加盟抽成与最低保底核对 |
| 6 | `hotel-night-audit-check` | 酒店夜审与房费收入核对 |
| 7 | `membership-liability-check` | 会员卡预收与履约负债核对 |
| 8 | `oem-rebate-policy-check` | 整车厂返利与商务政策核对 |
| 9 | `prepaid-card-consumption-check` | 预付卡消费核销核对 |
| 10 | `promo-subsidy-check` | 促销补贴与核销核对 |
| 11 | `purchase-rebate-check` | 采购返利与阶梯核算核对 |
| 12 | `restaurant-daily-sales-check` | 餐饮门店日营业款核对 |
| 13 | `retail-member-points-check` | 会员积分与储值卡核销核对 |
| 14 | `sales-rebate-check` | 销售返利与渠道返点核对 |
| 15 | `store-gross-margin-check` | 门店毛利与损耗核对 |
| 16 | `store-sales-report-check` | 门店营收上报核对 |
| 17 | `store-transfer-check` | 连锁门店调拨与库存核对 |

## 怎么用

```bash
node scripts/run.mjs --list                 # 看覆盖了哪些子问题
node scripts/run.mjs --sample               # 用内置样例跑一遍
node scripts/run.mjs --text "把表贴在这里"    # 贴材料，自动判断属于哪类问题
node scripts/run.mjs --sub-skill ad-agency-rebate-check --input 材料.json --json
```

## 声明与实现的一致性（可逐条核对）

ClawHub 的 `skillspector` 会检查"文档声明的范围"与"真实实现"是否一致，这里把话说死：

| 声明 | 你怎样自己核对 |
|---|---|
| 覆盖 **17 个子技能**，与下表**一一对应** | `node scripts/run.mjs --list` 的条数必须等于 17 |
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
