---
name: animation-engineer
description: >-
  动画工程师技能库：覆盖动效原理（缓动/时长/编排）、Framer Motion、Tailwind 动画与移动端触控动效。
  提供动效技术选型、CSS 关键帧纪律、性能与可访问性、动效设计系统的方法论，并用脚本固化
  CSS 关键帧 lint（重名/起止 transform/opacity/layout 属性）。
  触发词："动效"、"动画"、"CSS 关键帧"、"Framer Motion"、"Tailwind 动画"、"缓动"、"prefers-reduced-motion"、
  "动效规范"、"stagger"、"移动端触控动效"、"性能动画"。
agent_created: true
metadata:
  version: 1.0.0
  category: 动画
  difficulty: 进阶
  architecture: superpower
---

# 动画工程师 (Animation Engineer)

> 把 AI 编程助手变成一名能扛下动效交付链路（选型→实现→性能→规范）的搭档：从技术选型到设计系统，并用确定性脚本守住 CSS 关键帧纪律。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 需要**选动效技术**：CSS / Tailwind / Framer Motion / GSAP / WAAPI / Lottie 怎么选
- 用 **Framer Motion** 做 React 编排动画，或用 **Tailwind** 动画类做快速反馈
- 做**移动端触控动效**（手势/弹簧/原生质感）
- 需要**CSS 关键帧纪律**：避免卡顿、重名、错用属性
- 需要**动效性能与可访问性**：GPU 属性、will-change、prefers-reduced-motion
- 需要建立**动效设计系统**：时长/缓动 token、编排与 stagger 规范
- 需要**lint CSS 关键帧**（确定性脚本）

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 动效技术选型（决策树 + 矩阵 + WAAPI） | [references/decision-animation-tech.md](references/decision-animation-tech.md) | 选型, CSS, Framer Motion, GSAP, Lottie, WAAPI |
| CSS 关键帧纪律（transform/opacity/重名） | [references/css-keyframes-playbook.md](references/css-keyframes-playbook.md) | 关键帧, transform, opacity, will-change, 重名 |
| 性能与可访问性（GPU/reduced-motion） | [references/performance-accessibility.md](references/performance-accessibility.md) | 性能, 掉帧, 合成层, reduced-motion, 眩晕 |
| 动效设计系统（token/编排/一致性） | [references/motion-design-system.md](references/motion-design-system.md) | token, 时长, 缓动, stagger, 规范, 设计系统 |
| 动效原理与词汇（细粒度调用） | [skills/animation-vocabulary/SKILL.md](skills/animation-vocabulary/SKILL.md) | 缓动, 时长, 编排, 响应式动效, 原理 |
| Framer Motion 实战（细粒度调用） | [skills/framer-motion/SKILL.md](skills/framer-motion/SKILL.md) | framer-motion, layout, 手势, variants, SVG |
| 移动端触控动效（细粒度调用） | [skills/mobile-touch/SKILL.md](skills/mobile-touch/SKILL.md) | 触控, 手势, 弹簧, 页面过渡, 原生质感 |
| Tailwind 动画（细粒度调用） | [skills/tailwind-animations/SKILL.md](skills/tailwind-animations/SKILL.md) | tailwind, animate, 关键帧, transition, motion |

> 路由规则：先判断任务属于「选型 / CSS 纪律 / 性能可访问性 / 设计规范」哪类方法论 → 读 `references/`；要落地某个具体栈的写法 → 直接调 `skills/` 对应子技能。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/lint_css_keyframes.py --css src/ --config assets/motion-rules.json` — 查 @keyframes 重名、起止是否用 transform/opacity、是否动 layout 属性、引用是否未定义

运行示例：

```bash
python3 scripts/lint_css_keyframes.py --css src/ --config assets/motion-rules.json
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/motion-rules.json](assets/motion-rules.json) — lint 规则配置（含 `_` 注释键，脚本自动跳过）
- [assets/motion-spec-template.css](assets/motion-spec-template.css) — 动效规范 CSS 模板（脚本自检 0 错误）
- [assets/motion-checklist.md](assets/motion-checklist.md) — 动效规范发布前检查清单

## 核心原则（始终遵循）

1. **技术选型先行**：先定栈再写，简单过渡用 CSS/Tailwind，React 编排用 Framer Motion，别过度引库。
2. **只动合成属性**：动画只用 transform/opacity，绝不用 top/left 触发重排。
3. **可访问性底线**：所有动效接 prefers-reduced-motion 降级，装饰关、功能留。
4. **规范即门禁**：时长/缓动走 token，CSS 纪律用 lint 守，不靠评审肉眼。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜缓动曲线。
6. **明确边界**：动效风格拍板由设计/产品做，本技能出规范与检查，不替代审美决策。

## 与其他技能协作

- 需要**移动端开发**细节 → 调用 `mobile-developer`
- 需要**独立游戏动效**场景 → 调用 `indie-game-developer`
- 需要**视觉/UI 设计** → 调用 `design-studio`
- 需要**前端组件工程化**（原 `frontend-engineer` 已归档并入）→ 调用 `ai-fullstack-engineer`
- 需要**无障碍工程**深度（WCAG/读屏，本库只负责动效侧降级）→ 调用 `accessibility-engineer`
- 需要**文档**（动效规范文档/更新日志）→ 调用 `docs-writer`
