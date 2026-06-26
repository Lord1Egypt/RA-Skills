---
name: bundle-offer-generator
description: Generate ecommerce bundle ideas using product mix, margin logic, and customer intent. Use when teams want stronger offer packaging without random discounting.
---

# Bundle Offer Generator

bundle 不是把几个产品硬绑在一起，而是把购买理由组合得更强。

## 解决的问题

很多 bundle 做不起来，通常是因为：
- 只是打折，没有更清楚的购买逻辑；
- 组合虽然便宜，但用户不知道为什么要一起买；
- AOV 上去了，利润却掉得太多；
- 套餐层级不清楚，反而增加选择负担。

这个 skill 的目标是：
**基于商品关系、利润空间和用户场景，生成更好卖的 bundle 方案。**

## 何时使用

- 想拉高 AOV；
- 有多个关联商品，但不知道如何组合；
- 促销期想推出更有结构的套餐而不是单纯降价。

## 输入要求

- 商品列表与价格
- 毛利空间
- 商品搭配关系 / 使用顺序
- 目标客群和购买场景
- 可选：折扣边界、库存限制、平台限制

## 工作流

1. 找出自然搭配组合。
2. 设计基础款 / 进阶款 / 高价值款层级。
3. 检查 margin 和折扣空间。
4. 输出可销售的命名和定位建议。

## 输出格式

1. Bundle 方案列表
2. 定价逻辑
3. Margin 风险提示
4. 建议使用场景

## 质量标准

- 组合要有明确购买逻辑。
- 不只是“便宜了多少”，还要说明为什么一起买。
- 不能牺牲太多 margin。
- 输出要可直接用于商品页或活动页。

## 资源

参考 `references/output-template.md`。
