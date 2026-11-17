---
name: animation-vocabulary
description: 动效词汇与动画原则，覆盖缓动曲线、时长、编排、响应式动效，帮你建立专业的动画语言体系
source:
  type: derived
  repo: skills-repo/animation-engineer
  path: skills/animation-vocabulary/SKILL.md
  version: 1.0.0
  updated: 2026-07-30
  url: https://skills.sh/emilkowalski/skills/animation-vocabulary
metadata:
  category: 动效基础
  platform: Web
  difficulty: 入门
tags:
  - animation
  - easing
  - motion-design
  - css
---

# Animation Vocabulary — 动效词汇与原理

> 动效不是「加个过渡就行」，而是一套精确的语言体系。缓动曲线决定了用户感知的速度，时长影响操作反馈的清晰度，编排定义了元素的层级关系。本技能帮你建立系统化的动画设计词汇。

## 能力

- **缓动曲线**：ease-in/ease-out/cubic-bezier 选择原则，不同场景的最佳曲线
- **时长规范**：微交互 100-200ms、页面过渡 300-500ms、入场动画 500-800ms
- **编排与延迟**：stagger 交错动画、父子元素级联、场景动画序列
- **响应式动效**：prefers-reduced-motion 适配、移动端性能优化、GPU 加速属性
- **动画属性选择**：transform/opacity 高性能 vs layout-triggering 属性的选择

## 使用方式

在 Claude Code 中使用 `/animation-vocabulary` 调用。

```
/animation-vocabulary 分析这个交互流程的动画设计，给出缓动和时长建议
/animation-vocabulary 为这个 SaaS 控制面板设计一套动效规范
/animation-vocabulary 审查这些 CSS 动画的性能和可访问性
```

## 动效设计流程

1. **分析** — 确定交互目标：引导注意力/提供反馈/增加愉悦感
2. **选择** — 为每个动作选择恰当的缓动曲线和时长
3. **编排** — 设计多元素的出场顺序和延迟关系
4. **实现** — 用 CSS/JS 实现并检查性能表现
5. **验证** — 实际设备测试、prefers-reduced-motion 检查

## 适用场景

- 独立开发者为产品建立统一的动效语言
- 从零设计 Web 应用的过渡和动画系统
- 审查和优化现有动效的性能与可访问性
- 为设计系统补充动效规范文档

## 限制

- 覆盖动效设计原则和 CSS 实现，不涉及 Lottie/Rive 等动画工具
- 聚焦 Web 平台动效，不涉及原生 App 动画（iOS/Android）
- 动效规范聚焦独立产品，非大型设计系统的完整动效库

## 相关参考（Playbook）

动效原理落到规范与工程的深度资料 →

- 选型决策（何时用裸 CSS / Framer Motion / Tailwind / 其它）→ [decision-animation-tech.md](../../references/decision-animation-tech.md)
- 裸 CSS 关键帧纪律（transform/opacity、起止、重名）+ lint → [css-keyframes-playbook.md](../../references/css-keyframes-playbook.md)
- 性能与可访问性（GPU/合成层/reduced-motion 降级）→ [performance-accessibility.md](../../references/performance-accessibility.md)
- 动效设计系统（时长/缓动 token、编排、一致性）→ [motion-design-system.md](../../references/motion-design-system.md)
