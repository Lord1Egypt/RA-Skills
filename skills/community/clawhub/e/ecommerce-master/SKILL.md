---
name: ecommerce-master
description: "电商全链路 AI Agent 技能库：跨境扩张策略（市场评分/税务合规/物流/支付本地化）、Stripe 支付集成（订阅/发票/风控/对账）、Shopify 产品管理（GraphQL/CSV 批量）、电商前端搭建（组件/SEO/移动适配）、淘宝/闲鱼运营（商品发布内容包/交易对账/评价维护/选品定价复盘）。当用户要做跨境电商选品与落地、接入 Stripe 订阅与催款、批量管理 Shopify 商品、运营淘宝或闲鱼店铺、或搭建高转化电商前端时调用本技能，并据路由表进入对应子技能。"
agent_created: true
metadata:
  architecture: superpower
  category: 电商
  difficulty: 进阶
  platform: skills-repo
  version: 1.2.0
  created: 2026-08-09
  updated: 2026-10-29
tags:
  - ecommerce
  - cross-border
  - payment
  - storefront
  - shopify
  - stripe
  - taobao
  - xianyu
---

# Ecommerce Master（电商大师 · 超级技能路由）

> 覆盖「市场策略 → 前端搭建 → 支付集成 → 店铺运营」的电商全链路。
> 本文件只做路由与判断，完整方法论下沉到 `references/`，重复确定性任务交给 `scripts/`。

## 何时使用

在以下任一情况触发本技能，并按路由表进入对应子技能：

- 规划跨境电商扩张：选市场、算落地成本、做税务/海关合规
- 接入或优化支付：Stripe 订阅、发票、催款（dunning）、风控、对账
- 上架 / 批量管理 Shopify 商品与变体
- 从零搭建或优化电商前端（组件、SEO、移动适配、性能）
- 运营淘宝/闲鱼店铺：商品发布、交易对账、评价维护、选品定价复盘

## 能力索引（渐进式路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列条目，避免一次性占满上下文。

### 深层 playbook（`references/`，决策与上线门槛）

| 任务 | 读取 | 关键词（grep 线索） |
|------|------|---------------------|
| 跨境合规：注册义务决策树、清关与 VAT 申报路径选型、落地成本建模、各市场阈值速查 | [references/cross-border-compliance.md](references/cross-border-compliance.md) | `VAT` `IOSS` `阈值` `清关` `HS 编码` `落地成本` |
| 支付上线清单：接入方式决策树、Webhook 验签、争议退款、收入指标口径、测试场景矩阵 | [references/payment-integration-checklist.md](references/payment-integration-checklist.md) | `Checkout` `webhook` `验签` `dispute` `MRR` `对账` |
| 前端上线手册：组件优先级决策树、渲染策略选型、性能预算、可访问性、i18n | [references/storefront-launch-playbook.md](references/storefront-launch-playbook.md) | `JSON-LD` `Product schema` `LCP` `INP` `安全区` `i18n` |

### 细粒度子技能（`skills/`，可独立安装调用）

| 任务 | 进入 | 关键词（grep 线索） |
|------|------|---------------------|
| 跨境扩张策略 | [skills/cross-border-expansion](skills/cross-border-expansion/SKILL.md) | cross-border, 跨境, 市场评分, VAT, IOSS, 物流, 关税 |
| 支付集成 | [skills/payment-integration](skills/payment-integration/SKILL.md) | stripe, 订阅, 发票, 催款, dunning, 对账, 风控, Radar |
| 店铺管理 | [skills/shopify-manager](skills/shopify-manager/SKILL.md) | shopify, 产品, GraphQL, 变体, CSV 导入, 批量上架 |
| 前端搭建 | [skills/storefront-builder](skills/storefront-builder/SKILL.md) | storefront, 前端, 组件, SEO, 结构化数据, 移动适配, 转化 |
| 淘宝商品发布 | [skills/taobao-product-ops](skills/taobao-product-ops/SKILL.md) | taobao, 淘宝, 商品发布, 内容包, item.add, 类目属性, 闲鱼, 双通道 |
| 淘宝交易管理 | [skills/taobao-trade-ops](skills/taobao-trade-ops/SKILL.md) | 淘宝, 订单, 发货, 退款, trades.sold, 对账, logistics |
| 淘宝评价维护 | [skills/taobao-review-ops](skills/taobao-review-ops/SKILL.md) | 淘宝, 评价, traderate, 差评, DSR, 回评 |
| 淘宝运营方案 | [skills/taobao-operations](skills/taobao-operations/SKILL.md) | 运营, 选品, 定价, 上新节奏, 复盘, 转化漏斗 |

> **路由规则**：要判断「该不该做、代价多少、上线前还差什么」→ 读 `references/`；
> 要具体平台的具体写法与命令 → 调 `skills/`；要对现有商品流下客观判断 → 先跑 `scripts/`。

## 内置脚本（确定性、可复现）

放在 `scripts/`，纯标准库、可独立运行、`--help` 可用，不改被检文件、不联网：

- `scripts/validate_product_feed.py --feed <file.csv|json>` — 按 [assets/product-feed-rules.json](assets/product-feed-rules.json)
  校验商品信息流的必填字段、缺失令牌、数字/枚举约束，输出缺陷清单与计数。

用法示例：

```bash
python3 scripts/validate_product_feed.py --feed export/products.csv
python3 scripts/validate_product_feed.py            # 仅自检规则模板（应 0 错误）
```

## 模板资源（assets/）

- [assets/product-feed-rules.json](assets/product-feed-rules.json) — 商品信息流校验规则（含 `_comment`/`_note` 注释键）
- [assets/sample-product-feed.csv](assets/sample-product-feed.csv) — 合规样例商品流（0 缺陷，用作对照）

## 适用场景

- 独立开发者/中小卖家从零搭建跨境电商业务
- 评估目标市场并制定分阶段扩张路线图
- SaaS / 电商接入 Stripe 订阅、发票与收入分析
- 通过 Shopify API 或 CSV 批量管理产品目录
- 构建高转化率、移动友好、SEO 就绪的电商前端
- 淘宝企业店 / 闲鱼个人闲置的双渠道日常运营（家庭副业量级）

## 限制

- 税率与法规变化频繁，最终决策需咨询当地持牌税务/法律顾问
- 运费、落地成本为方向性估算，实际取决于尺寸、货量与承运商报价
- Stripe 相关功能需对应账号、API Key，部分（Radar、Sigma）需额外付费
- Shopify 单个产品上限 100 变体 / 3 选项维度；CSV 导入最大 50MB
- 支付网关的安全合规实现细节以官方文档为准，不猜测 API 签名
- 淘宝交易类 API 需个体工商户/企业资质；游戏账号/代练类目淘宝禁售，不纳入任何自动化
