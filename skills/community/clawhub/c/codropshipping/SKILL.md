---
name: product-query-helper
description: 帮助在CoDropshipping平台查询商品信息、库存、价格、规格等，自动抓取搜索结果并以表格形式展示
version: 1.0.0
author: Bob.Wang
permissions:
  - network: true
  - browser: true
---

# 商品查询助手技能

## Trigger（触发条件）
- 查询类：查商品、搜产品、找货、商品信息、产品详情、找找、帮我找
- 品类词：T恤、袜子、鞋子、服装、配饰等商品品类

## 执行步骤
1. 提取搜索关键词 → 转为英文
2. 访问 CoDropshipping 搜索
3. 点击搜索按钮
4. 抓取产品信息（名称、价格、月销量、评分）
5. 整理成 Markdown 表格返回

## Edge Cases
- 页面加载失败：提示稍后重试
- 搜索无结果：建议换关键词
- 遇到反爬：提示稍后再试