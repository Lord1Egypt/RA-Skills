---
name: payment-integration
description: Stripe 支付集成：订阅管理、发票自动化、催款流程、收入分析、风控规则，覆盖支付全生命周期
source:
  type: derived
  url: https://skills.sh/claude-office-skills/skills/stripe-payments
  repo: skills-repo/ecommerce-master
  path: skills/payment-integration/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 支付
  platform: Web
  difficulty: 进阶
---

# Stripe 支付集成

> 覆盖 Stripe 支付处理的完整生命周期：Checkout 接入、订阅管理、发票自动化、催款策略、收入分析和风控。

## 能力

- Checkout Session 集成（订阅/一次性支付）
- 订阅生命周期管理（创建/升级/降级/取消/续费）
- Webhook 事件处理（支付成功/失败/退款/争议）
- 发票自动化与催款（Dunning）流程
- 收入分析面板（MRR/ARR/流失率/队列分析）
- Stripe Radar 风控规则配置
- Customer Portal 自助服务配置

## 使用方式

在 Claude Code 中使用 `/payment-integration` 调用。

```
/payment-integration 帮我搭建 Stripe 订阅支付流程
/payment-integration 设计 SaaS 产品的三档定价方案
/payment-integration 配置支付失败后的自动催款流程
/payment-integration 生成本月收入分析报告
```

## 工作流

1. 确认业务模式（订阅/一次性/混合）和定价方案
2. 设计 Checkout 接入方案（Stripe Checkout / Elements）
3. 配置 Webhook 事件处理逻辑
4. 设置发票模板和催款序列
5. 搭建收入监控面板和定期报告

## 适用场景

- SaaS 产品订阅收费
- 电商网站支付接入
- 发票管理和自动化
- 支付失败催款挽回
- 收入数据分析和 MRR 追踪

## 相关参考（Playbook）

更完整的接入方式决策树、Webhook 签名校验与争议退款流程、收入指标统一口径、上线前测试场景矩阵与可勾选清单，见 [`references/payment-integration-checklist.md`](../../references/payment-integration-checklist.md)。

## 限制

- 需要 Stripe 账号和 API Key
- 建议在测试模式充分验证后再上线
- PCI 合规要求使用 Stripe Elements 而非自建表单
- 部分功能（Radar、Sigma）需额外付费