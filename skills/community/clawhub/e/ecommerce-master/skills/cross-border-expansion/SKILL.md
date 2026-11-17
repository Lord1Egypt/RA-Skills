---
name: cross-border-expansion
description: 跨境电商扩张策略：市场评分、物流方案、税务合规、支付本地化，输出分阶段扩张路线图
source:
  type: derived
  url: https://skills.sh/nexscope-ai/ecommerce-skills/cross-border-ecommerce
  repo: skills-repo/ecommerce-master
  path: skills/cross-border-expansion/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 策略
  platform: 通用
  difficulty: 进阶
---

# 跨境电商扩张策略

> 为独立卖家的国际电商扩张提供策略级指导：评估目标市场、对比物流模式、导航税务合规、制定分阶段路线图。

## 能力

- 8 维度市场评分（市场规模、电商渗透率、竞争强度、监管复杂度、物流基建、支付生态、文化距离、IP 保护）
- 5 种物流模式对比（直邮、3PL、平台仓、代发、集货），含成本与时效数据
- 按国家的税务/关税合规指南（EU VAT/IOSS、UK VAT、US Sales Tax、CA GST、AU GST、JP 消费税）
- 本地支付偏好映射与支付网关推荐
- 落地成本计算框架
- 分阶段扩张路线图（调研→试水→放量→优化）

## 使用方式

在 Claude Code 中使用 `/cross-border-expansion` 调用。

```
/cross-border-expansion 我在 Shopify 卖宠物用品，月销 $30K，想扩展到加拿大和英国
/cross-border-expansion 评估我的产品适合进入哪些国际市场
/cross-border-expansion 帮我算一下发到德国的落地成本
```

## 工作流

1. 收集信息：产品品类、平台、营收、目标市场、预算
2. 市场评分：用 8 维度矩阵打分排名
3. 深度分析：税务注册、物流方案、支付配置、本地化要求
4. 落地成本计算：产品 + 运费 + 关税 + 税费 + 支付处理费 + 退货预留
5. 输出分阶段路线图和 KPI 追踪计划

## 适用场景

- 独立卖家首次考虑跨境电商
- 已有一个市场，计划扩展到更多国家
- 评估跨境物流和税务成本
- 多平台卖家优化国际布局

## 相关参考（Playbook）

更完整的「是否触发 VAT / 销售税注册义务」决策树、清关与申报路径选型矩阵、各市场阈值速查表与落地成本建模公式，见 [`references/cross-border-compliance.md`](../../references/cross-border-compliance.md)。

## 限制

- 税率和法规变化频繁，最终决策需咨询当地税务顾问
- 运费为方向性估算，实际报价取决于产品尺寸和货量
- 市场数据来自行业报告，可能有偏差
- 提供策略规划，不构成法律或税务建议