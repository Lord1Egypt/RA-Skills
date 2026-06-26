---
name: discount-impact-calculator
description: Calculate how discounts affect revenue, margin, conversion assumptions, and allowable acquisition cost so teams can see whether a promotion is actually worth running.
---

# Discount Impact Calculator

See the real commercial effect of a discount before launching it.

## 先交互，再计算

开始时先问：
1. 这次 discount 是什么形式？
   - 直接打折
   - coupon
   - 满减
   - second-unit discount
2. 你们平时 discount impact 怎么算？
3. 这次要不要把 conversion uplift 假设一起算进去？
4. 是否要一起考虑退款率、AOV 变化、CAC 容忍度？
5. 你想沿用现有逻辑，还是让我给推荐分析框架？

如果用户没有成型口径，先给推荐框架，再确认后计算。

## Python script guidance

当用户给出结构化数字后：
- 生成 Python 脚本做 discount scenario 分析
- 输出 baseline vs discount scenario
- 返回 break-even / margin / CAC 变化
- 最后附上可复用脚本

## Solves

Many ecommerce teams make pricing or offer decisions with incomplete economics:
- they see revenue upside but not margin drag;
- they model one variable but ignore knock-on effects;
- they test offers without clear guardrails;
- they scale offers before checking break-even logic.

Goal:
**Turn offer assumptions into a clearer economic view that is easier to evaluate and act on.**

## Use when

- You want to compare offer scenarios before launching
- A discount, bundle, or upsell idea sounds good but needs economic validation
- Growth teams need a faster way to pressure-test merchandising decisions
- Teams want clearer go / watch / no-go logic before scale

## Inputs

- Core commercial assumptions relevant to the scenario
- Price and cost structure
- Margin or refund assumptions
- Traffic / conversion or attach-rate assumptions
- Constraints or guardrails

## Workflow

1. Clarify the baseline commercial setup and discount logic.
2. Model the scenario inputs that change order economics.
3. Surface upside, downside, and sensitivity.
4. Identify the biggest weak points or break-even pressure.
5. Recommend whether to test, revise, or avoid the scenario.
6. Return reusable Python script.

## Output

1. Baseline view
2. Scenario result
3. Margin / break-even implications
4. Key risks and weak points
5. Recommendation
6. Python script

## Quality bar

- Output should be commercially interpretable, not just a raw formula dump.
- Recommendations should stay grounded in ecommerce economics.
- Weak points should be clearly separated from upside assumptions.
- The result should help a team decide what to test next.

## Resource

See `references/output-template.md`.
