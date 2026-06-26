---
name: bundle-margin-calculator
description: Calculate whether a product bundle improves average order value without quietly destroying contribution margin. Use when teams want to test bundle structures with clearer economics.
---

# Bundle Margin Calculator

Compare bundle upside against margin reality so the offer is not just bigger, but smarter.

## 先交互，再计算

开始时先问：
1. bundle 结构是什么？
   - 固定套装
   - 买 A 加价购 B
   - 多件折扣
2. 你们想看的是 AOV 提升，还是 contribution margin 改善？
3. 是否要考虑 attach rate、运费变化、赠品成本、潜在自我蚕食？
4. 你们有没有现有 bundle 评估逻辑？
5. 要沿用现有逻辑，还是让我给推荐框架？

## Python script guidance

有结构化数据时：
- 生成 Python 脚本建模 bundle 方案
- 输出 baseline vs bundle scenario
- 展示 attach rate / margin sensitivity
- 返回可复用脚本

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

1. Clarify the baseline commercial setup and bundle logic.
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
