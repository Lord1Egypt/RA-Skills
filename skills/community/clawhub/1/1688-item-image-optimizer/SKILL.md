---
name: 1688-item-image-optimizer
description: |
  1688 商品图片智能优化助手 —— 打开图片优化页面，为商品主图增加热卖元素。
  触发词：优化图片、图片优化、主图优化、商品图片、改图。
metadata:
  openclaw:
    emoji: "🖼️"
  interactions:
    - name: open_tab_image_optimize
      type: open_tab
      selectionType: shop_backend
      description: "根据上下文是否包含商品ID，输出对应的open_tab JSON唤起图片优化页面，流程结束，禁止反问用户"
      required_data:
        url: "图片优化页面URL，有商品ID时拼接offerId参数"
        pageTitle: "图片优化"
        pageDescription: "自动为商品主图增加热卖元素，以获取更多的买家点击与下单"
        icon: "图标URL"
---

# 1688-item-image-optimizer — 商品图片智能优化

## 技能概述

1688 商品图片智能优化助手。根据上下文是否包含商品 ID，打开对应的图片优化页面。

## Agent 执行规范

**禁止反问用户、禁止调用任何 CLI 命令、禁止执行任何额外逻辑。** 仅根据上下文判断是否包含商品 ID，直接按 [`references/interaction-specs.md`](./references/interaction-specs.md) 中 `open_tab_image_optimize` 的数据结构返回对应的 JSON 即可，流程到此结束，无需任何后续步骤。
