---
name: tailwind-animations
description: Tailwind CSS 动画工具集，覆盖内置动画类、自定义关键帧、过渡效果和交互动画配置
source:
  type: derived
  repo: skills-repo/animation-engineer
  path: skills/tailwind-animations/SKILL.md
  version: 1.0.0
  updated: 2026-07-30
  url: https://skills.sh/josiahsiegel/claude-plugin-marketplace/tailwindcss-animations
metadata:
  category: CSS 动画
  platform: Web
  difficulty: 入门
tags:
  - tailwind
  - css
  - animation
  - transition
  - keyframes
---

# Tailwind Animations — Tailwind CSS 动画工具集

> Tailwind CSS 内置了丰富的动画和过渡类，但大多数人只用 `animate-spin` 和 `transition-all`。本技能帮你解锁 Tailwind 的完整动画能力，从内置类到自定义关键帧。

## 能力

- **内置动画类**：animate-spin/ping/pulse/bounce 的正确使用场景
- **自定义关键帧**：tailwind.config.js 中扩展动画，定义复杂多阶段动画
- **过渡系统**：transition-property/duration/timing-function/delay 的组合策略
- **交互状态**：hover/focus/group-hover/motion-safe/motion-reduce 与动画的结合
- **性能优化**：will-change、transform-gpu、避免 layout thrashing

## 使用方式

在 Claude Code 中使用 `/tailwind-animations` 调用。

```
/tailwind-animations 为这个按钮添加 hover 和点击动效
/tailwind-animations 设计一个卡片列表的入场 stagger 动画
/tailwind-animations 配置 tailwind.config 自定义弹跳动画
```

## Tailwind 动画流程

1. **选择** — 从内置动画类中选择最接近效果的
2. **调整** — 通过 duration/delay/ease 调整动画参数
3. **自定义** — 内置类不满足时在 config 中定义 @keyframes
4. **交互** — 绑定 hover/focus/group 等触发条件
5. **优化** — 确保 GPU 加速和无障碍适配

## 适用场景

- 用 Tailwind 快速为页面添加交互反馈动效
- 创建产品 Landing Page 的滚动入场动画
- 为组件库定义统一的 Tailwind 动画预设
- 在不引入 Framer Motion/GSAP 的情况下实现交互动效

## 限制

- 聚焦 Tailwind CSS 动画生态，不涉及 JS 动画库
- 复杂编排动画（如 Scroll-Linked）建议用 Framer Motion 补充
- 支持 Tailwind v3/v4 语法，不覆盖 Tailwind v2

## 相关参考（Playbook）

Tailwind 动画之外的决策与底线 →

- 何时选 Tailwind 动画（快速反馈 vs Framer Motion/GSAP）→ [decision-animation-tech.md](../../references/decision-animation-tech.md)
- 裸 CSS 关键帧纪律（Tailwind 配置的 @keyframes 也受 lint 约束）→ [css-keyframes-playbook.md](../../references/css-keyframes-playbook.md)
- 性能与可访问性（motion-reduce/motion-safe 降级）→ [performance-accessibility.md](../../references/performance-accessibility.md)
- 动效设计系统（animate 类引用 token、避免硬编码 ms）→ [motion-design-system.md](../../references/motion-design-system.md)
