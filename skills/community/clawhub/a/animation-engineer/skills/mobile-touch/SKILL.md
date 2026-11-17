---
name: mobile-touch
description: 移动端触控交互动效，覆盖手势动画、触控反馈、页面过渡和原生质感交互
source:
  type: derived
  repo: skills-repo/animation-engineer
  path: skills/mobile-touch/SKILL.md
  version: 1.0.0
  updated: 2026-07-30
  url: https://skills.sh/dylantarre/animation-principles/mobile-touch
metadata:
  category: 移动端动效
  platform: 移动端
  difficulty: 进阶
tags:
  - mobile
  - touch
  - gesture
  - interaction
  - animation
---

# Mobile Touch — 移动端触控交互动效

> 移动端的交互语言不是桌面端的缩小版。触控手势、物理惯性和即时反馈是移动体验的核心。本技能帮你设计「有触感」的移动端交互动效。

## 能力

- **手势动效**：滑动删除、下拉刷新、侧滑返回、捏合缩放的标准动画
- **触控反馈**：点击缩放（ripple）、长按振动反馈、拖拽跟随的动效策略
- **页面过渡**：push/pop 导航动画、Modal 弹出、底部弹出 Sheet 的惯性动效
- **物理质感**：弹簧动画、惯性滚动、橡皮筋效果的原生实现
- **性能适配**：60fps 触控响应、passive event listener、requestAnimationFrame 编排

## 使用方式

在 Claude Code 中使用 `/mobile-touch` 调用。

```
/mobile-touch 为这个列表设计滑动删除的交互动效
/mobile-touch 设计一个原生质感的底部 Sheet 弹出动画
/mobile-touch 优化这个手势操作的响应延迟和动画帧率
```

## 移动端动效流程

1. **识别** — 确定手势类型（tap/swipe/pinch/drag/long-press）
2. **原型** — 用 CSS/Framer Motion 快速实现手势动效原型
3. **物理调优** — 调整弹簧参数、摩擦力、惯性衰减
4. **设备测试** — 真机触摸测试，调整帧率和响应延迟
5. **无障碍** — reduced-motion 模式下的降级方案

## 适用场景

- 移动端 Web App 的触控交互设计
- PWA 的原生质感手势动效实现
- 从桌面端到移动端的交互动效适配
- 独立开发者提升移动端产品的交互品质

## 限制

- 覆盖移动端 Web（PWA/H5），不涉及 iOS/Android 原生 SDK 动画
- 手势动效聚焦通用模式，不涉及游戏级的手势系统
- 复杂物理引擎（如多体碰撞）建议用专用的物理库

## 相关参考（Playbook）

移动端触控动效之外的决策与底线 →

- 何时选 mobile-touch（移动触控手势 vs 其它栈）→ [decision-animation-tech.md](../../references/decision-animation-tech.md)
- 性能与可访问性（60fps 触控、reduced-motion 降级）→ [performance-accessibility.md](../../references/performance-accessibility.md)
- 动效设计系统（触控反馈时长走 token、跨端一致）→ [motion-design-system.md](../../references/motion-design-system.md)
