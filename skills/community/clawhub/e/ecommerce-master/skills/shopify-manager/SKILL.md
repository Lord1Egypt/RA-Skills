---
name: shopify-manager
description: Shopify 产品管理：GraphQL API 创建/更新/批量导入/图片上传，支持 CSV 和 API 两种方式
source:
  type: derived
  url: https://skills.sh/jezweb/claude-skills/shopify-products
  repo: skills-repo/ecommerce-master
  path: skills/shopify-manager/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 运营
  platform: Web
  difficulty: 入门
---

# Shopify 产品管理

> 通过 Shopify Admin GraphQL API 或 CSV 导入，创建、更新和批量管理 Shopify 产品。

## 能力

- GraphQL API 创建/更新/删除产品
- 变体管理（选项、价格、SKU、库存）
- 产品图片上传（分阶段上传 + 关联）
- CSV 批量导入（20+ 产品推荐）
- 集合分配和库存设置
- 产品数据验证

## 使用方式

在 Claude Code 中使用 `/shopify-manager` 调用。

```
/shopify-manager 帮我上架 5 款新品，包括变体和图片
/shopify-manager 批量更新所有夏季产品的价格
/shopify-manager 从这份 CSV 导入产品目录
/shopify-manager 把所有 T 恤产品加入"夏季促销"集合
```

## 工作流

1. 收集产品数据（标题/描述/变体/图片/SEO）
2. 选择方式：1-5 个产品用 GraphQL，6-20 个用批量 GraphQL，20+ 用 CSV
3. 执行创建/更新操作
4. 上传图片（公开 URL 直传，或分阶段上传）
5. 分配到集合，设置库存
6. 验证：查询回产品确认，提供管理后台链接

## 适用场景

- 新店上架产品目录
- 批量更新价格和库存
- 从其他平台迁移产品到 Shopify
- 产品图片和 SEO 信息管理

## 相关参考（Playbook）

批量导入前先用 [scripts/validate_product_feed.py](../../scripts/validate_product_feed.py) 校验商品流（规则见 [assets/product-feed-rules.json](../../assets/product-feed-rules.json)）；
校验命令、缺陷判定与「商品数据进生产前」的上线清单见 [`references/storefront-launch-playbook.md`](../../references/storefront-launch-playbook.md) 第 3.4 节与第 7 节。

## 限制

- 需要 Admin API access token（通过 shopify-setup 配置）
- 每个产品最多 100 个变体、3 个选项维度
- CSV 导入最大 50MB
- 新创建的产品默认为 DRAFT 状态