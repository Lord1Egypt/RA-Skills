---
name: framer-motion
description: React 动画库 Framer Motion 实战，覆盖布局动画、手势、SVG 动画和编排
source:
  type: derived
  repo: skills-repo/animation-engineer
  path: skills/framer-motion/SKILL.md
  version: 1.0.0
  updated: 2026-07-30
  url: https://skills.sh/mindrally/skills/framer-motion
metadata:
  category: React 动画
  platform: Web
  difficulty: 进阶
tags:
  - react
  - framer-motion
  - animation
  - layout
  - gesture
---

# Framer Motion — React 声明式动画

> Framer Motion 是 React 生态中最流行的声明式动画库。它的 layout 动画和手势系统让你用几行代码实现原生质感的交互。本技能覆盖从基础到进阶的实战模式。

## 能力

- **基础动画**：motion 组件、animate 属性、initial/exit 生命周期的完整用法
- **布局动画**：layout prop 自动过渡、layoutId 共享元素动画、AnimatePresence 退出动画
- **手势系统**：whileHover/whileTap/whileDrag/whileInView 等手势驱动的动画
- **SVG 动画**：pathLength 描边动画、路径 morphing、SVG 路径绘制
- **编排与变体**：variants 模式、staggerChildren、父子动画编排策略

## 使用方式

在 Claude Code 中使用 `/framer-motion` 调用。

```
/framer-motion 用 layoutId 实现列表到详情的共享元素过渡
/framer-motion 为这个 Dashboard 卡片添加拖拽排序和移除动效
/framer-motion 设计一个 SVG Logo 的描边绘制入场动画
```

## Framer Motion 开发流程

1. **分析** — 确定哪个 UI 元素需要动画，要解决什么交互问题
2. **方案** — 选择最合适的 motion 模式（基础/layout/手势/变体）
3. **实现** — 编写 motion 组件代码，设置动画参数
4. **调优** — 调整弹簧参数、时长、缓动，在设备上测试
5. **无障碍** — 适配 prefers-reduced-motion 的降级方案

## 适用场景

- React 项目的交互动效和页面过渡
- 列表排序/增删的布局动画
- SVG 图形的描边动画和图标动效
- 独立 React 开发者替代 CSS transition 的更强方案

## 限制

- 覆盖 Framer Motion 核心功能，不涉及 motion-plus 和高级 3D
- 需要 React 项目环境，不适用于非 React 技术栈
- 复杂 3D 动画建议用 Three.js + React Three Fiber 补充

## 相关参考（Playbook）

React 动效落地之外的决策与底线 →

- 何时选 Framer Motion（React 编排/手势 vs 其它栈）→ [decision-animation-tech.md](../../references/decision-animation-tech.md)
- 性能与可访问性（useReducedMotion 降级、GPU 属性）→ [performance-accessibility.md](../../references/performance-accessibility.md)
- 动效设计系统（variants 编排、时长/缓动 token）→ [motion-design-system.md](../../references/motion-design-system.md)
