# 电商大师技能库

> AI Agent Skills for Ecommerce —— 跨境扩张、支付集成、前端搭建、店铺管理、淘宝/闲鱼运营

## 定位

为独立开发者和中小卖家提供一套可安装的 AI Agent 电商技能，覆盖从市场策略到店铺运营的全链路（跨境电商 + 国内淘宝/闲鱼双体系）。

## 核心理念

> 不建站则已，建站则专业。让 AI 帮你做电商决策，你只需专注产品和客户。

- **策略先行**——先评估市场再行动，数据驱动跨境扩张
- **支付闭环**——Stripe 集成覆盖订阅、发票、风控全流程
- **前端专业**——遵循 ecommerce 最佳实践，不做低转化率的页面
- **店铺提效**——Shopify API 自动化产品管理
- **双渠道运营**——淘宝企业店（API 优先）与闲鱼个人闲置（浏览器半自动兜底）双通道

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 🌍 跨境策略 | `cross-border-expansion` | 跨境电商扩张：市场评分、物流方案、税务合规、支付本地化 | [衍生](https://skills.sh/nexscope-ai/ecommerce-skills/cross-border-ecommerce) |
| 💳 支付集成 | `payment-integration` | Stripe 支付集成：订阅管理、发票自动化、收入分析、风控 | [衍生](https://skills.sh/claude-office-skills/skills/stripe-payments) |
| 🏪 前端搭建 | `storefront-builder` | 电商前端最佳实践：组件模式、SEO、移动适配、后端集成 | [衍生](https://skills.sh/medusajs/medusa-agent-skills/storefront-best-practices) |
| 🛒 店铺管理 | `shopify-manager` | Shopify 产品管理：GraphQL API 创建/更新/批量导入 | [衍生](https://skills.sh/jezweb/claude-skills/shopify-products) |
| 🇨🇳 淘宝商品 | `taobao-product-ops` | 淘宝商品发布：内容包结构、TOP API/浏览器双通道、资质判断 | 原创 |
| 🇨🇳 淘宝交易 | `taobao-trade-ops` | 淘宝交易管理：订单/发货/退款 API 面、对账 SOP | [改编](https://open.taobao.com) 自淘宝开放平台文档 |
| 🇨🇳 淘宝评价 | `taobao-review-ops` | 淘宝评价维护：traderate API、差评应对、DSR 维护 | [改编](https://open.taobao.com) 自淘宝开放平台文档 |
| 🇨🇳 运营方案 | `taobao-operations` | 淘宝/闲鱼运营方法论：选品四问、定价三层、上新节奏、复盘三表 | 原创 |

## 安装

整库安装（推荐）：

```bash
npx skills add skills-repo/ecommerce-master -g -y
```

单技能安装（子路径 URL 语法，⚠️ 勿用 `repo@skill` 语法——skills CLI 根技能遮蔽下不可用，见 skills-repo-admin D115）：

```bash
npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/cross-border-expansion" -g -y
```

## 子技能目录

本仓库每个子技能可单独安装，路径长期稳定、不会改名：

| 子技能 | 安装命令 | 适用 |
|--------|----------|------|
| cross-border-expansion | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/cross-border-expansion" -g -y` | 跨境电商扩张：市场评分、物流、税务合规、支付本地化 |
| payment-integration | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/payment-integration" -g -y` | Stripe 支付集成：订阅、发票、催款、收入分析、风控 |
| storefront-builder | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/storefront-builder" -g -y` | 电商前端最佳实践：组件、SEO、移动适配、后端集成 |
| shopify-manager | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/shopify-manager" -g -y` | Shopify 产品管理：GraphQL API、变体、CSV 批量导入 |
| taobao-product-ops | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-product-ops" -g -y` | 淘宝商品发布：内容包、双通道、资质判断 |
| taobao-trade-ops | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-trade-ops" -g -y` | 淘宝交易管理：订单/发货/退款、对账 SOP |
| taobao-review-ops | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-review-ops" -g -y` | 淘宝评价维护：差评应对、DSR |
| taobao-operations | `npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-operations" -g -y` | 运营方法论：选品、定价、上新、复盘 |

## 快速开始

```bash
npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-operations" -g -y
npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-product-ops" -g -y
npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-trade-ops" -g -y
npx skills add "https://github.com/skills-repo/ecommerce-master/tree/main/skills/taobao-review-ops" -g -y
```

## 推荐工作流

```
跨境：市场评估 → 前端搭建 → 支付集成 → 店铺运营
      cross-      storefront-   payment-     shopify-
      border      builder       integration  manager

淘宝/闲鱼：选品定价 → 商品发布 → 交易对账 → 评价维护（周复盘回到选品）
          taobao-     taobao-       taobao-      taobao-review-ops
          operations  product-ops   trade-ops
```

## 许可

MIT