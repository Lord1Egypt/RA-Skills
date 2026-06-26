---
name: cpa-calculator-ecommerce
description: Calculate allowable and break-even CPA for ecommerce offers using margin, refunds, and conversion assumptions. Use when teams need acquisition guardrails before spending harder.
---

# CPA Calculator Ecommerce

先知道你能承受多少获客成本，再谈扩量。

## 解决的问题

很多投放问题不是量不够，而是：
- CPA 早就超出利润承受范围；
- 团队只盯 ROAS，没有明确的 CPA 上限；
- 不同 offer / SKU 应该有不同的出价天花板，但没人算。

这个 skill 的目标是：
**根据商品利润结构和退款影响，算出 break-even CPA 与可接受 CPA 区间。**

## 何时使用

- 新 campaign 启动前；
- 出价策略调整前；
- 比较不同商品 / 套餐的投放可行性。

## 输入要求

- 售价
- 毛利和履约成本
- 退款 / 退货影响
- 折扣和优惠
- 当前转化率或目标转化假设
- 可选：复购贡献、附加费用

## 工作流

1. 计算单客户可贡献利润。
2. 估算 break-even CPA。
3. 结合风险给出更保守的 allowable CPA。
4. 提示提价、控折扣、提转化等优化方向。

## 输出格式

1. 假设表
2. Break-even CPA
3. Allowable CPA 区间
4. 建议动作

## 质量标准

- 明确区分理论 break-even 和建议 CPA。
- 结果要能直接指导投放出价。
- 不能忽略退款和履约成本。
- 建议动作要具体。

## 资源

参考 `references/output-template.md`。
