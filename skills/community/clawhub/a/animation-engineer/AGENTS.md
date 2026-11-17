# Animation Engineer — Agent 入口

> 本仓库是 skills-repo 组织下的动画工程师技能库。面向独立开发者和前端开发者，覆盖动效原理、CSS 动画、移动端交互和 React 声明式动画，帮你为产品注入专业级动效体验。

## 架构与加载顺序（superpower）

本仓库按 skills-repo 的 **superpower 架构**组织，Agent 加载顺序如下：

1. **先读 `SKILL.md`（L1 路由层）** — 只做能力索引，不要在此找方法论正文。
2. **按需读 `references/`（L2）** — 技术选型、CSS 关键帧纪律、性能可访问性、动效设计系统，按任务类型加载，不全量读。
3. **落地具体栈时读 `skills/<name>/SKILL.md`（L3）** — 动效原理 / Tailwind / 移动触控 / Framer Motion 的细粒度能力。
4. **确定性任务用 `scripts/`（L4）** — CSS 关键帧 lint，产物可复现。
5. **模板套用看 `assets/`（L5）** — lint 规则、规范 CSS、检查清单。

渐进式加载原则：先路由、后深度；不凭记忆猜缓动曲线与关键帧写法。

## 技能清单

| 环节 | 技能 | 文件 | 用途 |
|------|------|------|------|
| 原理 | animation-vocabulary | [skills/animation-vocabulary/SKILL.md](skills/animation-vocabulary/SKILL.md) | 动效词汇与动画原则：缓动、时长、编排 |
| CSS | tailwind-animations | [skills/tailwind-animations/SKILL.md](skills/tailwind-animations/SKILL.md) | Tailwind CSS 动画工具集：内置类、自定义关键帧 |
| 移动 | mobile-touch | [skills/mobile-touch/SKILL.md](skills/mobile-touch/SKILL.md) | 移动端触控交互：手势、反馈、页面过渡 |
| React | framer-motion | [skills/framer-motion/SKILL.md](skills/framer-motion/SKILL.md) | React 声明式动画：布局动画、手势、SVG |

## 使用场景

- 独立开发者为产品注入专业级动效体验
- 前端开发者学习系统化的动画设计方法
- 从零建立产品的动效语言和交互规范
- 移动端 Web App 的触控手势和过渡设计

## 相关仓库

- `design-studio` — UI/UX 设计（设计系统、UI审查、无障碍），本仓库聚焦动效与动画
- `ai-fullstack-engineer` — 前端组件开发、性能优化（原 `frontend-engineer` 已归档并入此仓库），本仓库聚焦交互动画层面
- `accessibility-engineer` — 无障碍工程（WCAG、键盘/读屏），本仓库负责动效侧 `prefers-reduced-motion` 降级
- `indie-game-developer` — 游戏开发（Three.js 游戏），本仓库聚焦 Web/移动端 UI 动效
- `mobile-developer` — 移动端开发，本仓库提供移动端触控动效能力

> 本仓库聚焦**Web 和移动端 UI 动效的设计与实现**，与 design-studio 的 UI 设计视角互补，与 ai-fullstack-engineer 的组件开发视角协同。
