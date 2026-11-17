---
name: storefront-builder
description: 电商前端最佳实践：组件模式、SEO 结构化数据、移动适配、后端集成，框架无关（Next.js/SvelteKit/React/Vue）
source:
  type: derived
  url: https://skills.sh/medusajs/medusa-agent-skills/storefront-best-practices
  repo: skills-repo/ecommerce-master
  path: skills/storefront-builder/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 前端
  platform: Web
  difficulty: 进阶
---

# 电商前端最佳实践

> 构建现代化、高转化率的电商前端：覆盖 UI/UX 模式、组件设计、布局结构、SEO 优化和移动端适配。

## 能力

- 电商组件模式库（导航栏/商品卡片/购物车弹窗/结账流程）
- 框架无关的布局指南（Next.js/SvelteKit/TanStack Start）
- 后端集成最佳实践（Medusa/Shopify/自定义 API）
- SEO 结构化数据（Product schema、BreadcrumbList）
- 移动端适配（安全区域、触控目标、底部导航）
- 转化率优化（信任信号、减少摩擦、清晰 CTA）

## 使用方式

在 Claude Code 中使用 `/storefront-builder` 调用。

```
/storefront-builder 从零搭建一个电商首页
/storefront-builder 实现商品详情页，包含变体选择和图片画廊
/storefront-builder 添加购物车和结账流程
/storefront-builder 优化移动端购物体验
```

## 工作流

1. 确定技术栈和框架（Next.js/SvelteKit 等）
2. 加载设计参考，确认品牌配色和设计系统
3. 按优先级实现核心组件：导航 → 商品列表 → 商品详情 → 购物车 → 结账
4. 每个组件遵循电商最佳实践（可访问性、移动适配、性能）
5. 验证 SEO 结构化数据、Core Web Vitals

## 适用场景

- 从零搭建独立电商网站
- 优化现有电商前端的转化率
- 接入 Medusa/Shopify 等电商后端
- 电商组件开发参考

## 相关参考（Playbook）

更完整的组件实现顺序决策树、渲染策略选型矩阵、性能预算门槛（LCP/INP/CLS）、可访问性清单与 i18n 落地要点，见 [`references/storefront-launch-playbook.md`](../../references/storefront-launch-playbook.md)。

## 限制

- 框架示例以 React/TypeScript 为主，但模式适用于所有现代框架
- 后端 SDK 方法需查阅官方文档确认（不猜测 API 签名）
- 不涉及支付网关的安全合规实现细节