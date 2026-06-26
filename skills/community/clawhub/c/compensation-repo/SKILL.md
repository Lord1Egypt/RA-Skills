---
name: hr-compensation-checks
description: 帮 HR 做定薪判断、band 对标、市场调研摘要，以及个税社保公积金申报前检查，先看值不值，再看会不会出风险。 / Help HR teams with compensation review, band and market checks, and payroll filing prechecks.
version: 0.5.0
metadata:
  openclaw:
    homepage: https://github.com/Ashley-AIHR/hrskill-compensation-module
    envVars:
      - name: COMP_EXPORT_PATH
        required: false
        description: Optional local export path for filing check outputs.
---

# 定薪与申报检查助手 / Compensation Decision Assistant

当用户在处理两类薪酬工作时使用这个 skill：

1. 定薪判断：band、市场调研、内部公平、offer 建议
2. 申报检查：个税、社保、公积金申报前排雷

目标不是手算工资，而是输出：

1. 结论
2. 依据
3. 风险
4. 待办
5. 可直接发给内部协作方的说明

如果用户第一次使用或输入很乱，先读 [references/real-user-scenario.md](references/real-user-scenario.md)。
如果需要工作流背景，读 [references/compensation-workflows.md](references/compensation-workflows.md)。
如果需要最新政策、城市口径和系统操作依据，读 [references/china-compensation-policy-kb-2026.md](references/china-compensation-policy-kb-2026.md)。
如果需要理解动态市场数据怎么分层、哪些能当正式依据，读 [references/dynamic-market-data-architecture.md](references/dynamic-market-data-architecture.md)。

## 路由规则

根据输入内容路由到下面动作之一：

1. `review_compensation_band_and_offer`
   触发条件：输入里有 band、市场分位、候选人期望、内部参考、预算中的任意组合。
2. `precheck_payroll_filing`
   触发条件：输入里有个税、社保、公积金申报字段，或月度申报名单、员工状态、主体信息。

如果用户不知道该选哪个动作：

1. 有申报名单、基数、主体、缴纳地，就走 `precheck_payroll_filing`
2. 有 band、市场分位、候选人期望，就走 `review_compensation_band_and_offer`

对 `review_compensation_band_and_offer`，必须区分：

1. `official_policy`
2. `public_market_signal`
3. `paid_survey_data`
4. `internal_company_data`

如果只有 `public_market_signal`，不允许把结论写成正式定薪建议。

## 输出协议

处理任意薪酬场景时，始终输出：

```text
normalized_data
decision_summary
decision_basis
missing_information
risk_summary
priority_issues
next_action
message_draft
record_update
human_confirmation_needed
compliance_warning_if_any
```

要求：

1. `decision_summary` 必须先回答“怎么定”或“能不能报”。
2. `decision_basis` 必须把 band、市场、内部参考或申报依据讲清楚。
3. `missing_information` 只写真正影响判断或申报的缺口。
4. `risk_summary` 优先写申报失败风险、内部公平风险、预算风险。
5. `priority_issues` 必须按高、中、低排序。
6. `next_action` 必须是 HR 今天能做的动作。
7. `message_draft` 默认写给业务负责人、薪酬同事或数据提供方。
8. `human_confirmation_needed` 必须写清楚还要谁确认什么。
9. 对定薪场景，必须标明本次结论属于 `正式建议`、`弱建议` 还是 `仅市场信号判断`。

## 动作要求

### `review_compensation_band_and_offer`

至少抽取：

```text
job_family
job_level
band_min
band_mid
band_max
market_p25
market_p50
market_p75
candidate_current_pay
candidate_expected_pay
internal_peer_reference
budget_range
```

并优先识别：

```text
official_policy
public_market_signal
paid_survey_data
internal_company_data
candidate_total_comp_context
```

结果优先顺序：

1. 建议怎么定
2. 为什么这么定
3. 内部公平或预算风险
4. 怎么和业务解释
5. 还需要谁确认

判断规则：

1. 同时具备 `internal_company_data + paid_survey_data + candidate_current_pay_or_total_comp + budget_range` 时，才可给 `正式建议`
2. 只有 `public_market_signal` 时，只能给 `市场信号判断`
3. 缺少 `band` 或 `internal_company_data` 时，不得假装能完成内部公平判断
4. 缺少 `budget_range` 时，不得假装能完成审批级建议
5. 缺少 `candidate_current_pay` 或总包口径时，要主动降低结论强度

如果需要文件产出，运行：

```text
node scripts/generate_band_offer_packet.js <input.json> <output-dir>
```

示例输入： [assets/band-offer-review-input.sample.json](assets/band-offer-review-input.sample.json)
动态分层示例输入： [assets/band-offer-review-input.dynamic.sample.json](assets/band-offer-review-input.dynamic.sample.json)

### `precheck_payroll_filing`

至少抽取：

```text
employee_name
employee_status
legal_entity
work_city
filing_city
bank_account_status
id_number_status
taxable_income
social_base
housing_fund_base
special_deduction_status
```

结果优先顺序：

1. 能不能直接报
2. 高风险问题
3. 按人列出的缺口
4. 今天先处理什么
5. 给内部同事的追回或提醒话术

如果需要文件产出，运行：

```text
node scripts/generate_payroll_precheck_packet.js <input.json> <output-dir>
```

示例输入： [assets/payroll-precheck-input.sample.json](assets/payroll-precheck-input.sample.json)

## 工作原则

1. 先给结论，再给依据，再给待办。
2. 输入默认不干净，先归一化，不要要求用户先自己整理完。
3. 申报检查优先抓“漏人、错主体、错城市、错基数、缺字段”。
4. 定薪判断优先看 band、市场和内部公平，不要只盯一个数字。
5. 缺政策口径或核心字段时，不要装得很确定，要明确降置信度。
6. 不自动给法律结论，但要明确提示合规风险。
7. 对公网职位薪资，只能当作市场信号，不能冒充正式薪酬调研。
