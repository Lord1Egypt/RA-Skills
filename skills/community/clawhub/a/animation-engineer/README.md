# Animation Engineer — 动画工程师技能库

> 面向独立开发者和前端开发者的动画与动效技能集合。覆盖动效原理、CSS 动画、移动端交互和 React 声明式动画，帮你为产品注入专业级动效体验。

## 架构说明（superpower）

本仓库采用 skills-repo 的 **superpower 架构**（五层）：

- `SKILL.md` — L1 路由层，只做能力索引，不写方法论
- `references/` — L2 深层 playbook（技术选型、CSS 关键帧纪律、性能可访问性、动效设计系统），按需加载
- `skills/` — L3 细粒度子技能（动效原理 / Tailwind / 移动触控 / Framer Motion），可单独安装
- `scripts/` — L4 确定性脚本（CSS 关键帧 lint）
- `assets/` — L5 可复用模板（lint 规则、规范 CSS、检查清单）

## 技能清单

| 技能 | 描述 | 来源 |
|------|------|------|
| [animation-vocabulary](skills/animation-vocabulary/SKILL.md) | 动效词汇与动画原则：缓动曲线、时长规范、编排策略、响应式动效 | [skills.sh](https://skills.sh/emilkowalski/skills/animation-vocabulary) |
| [tailwind-animations](skills/tailwind-animations/SKILL.md) | Tailwind CSS 动画工具集：内置动画类、自定义关键帧、过渡效果 | [skills.sh](https://skills.sh/josiahsiegel/claude-plugin-marketplace/tailwindcss-animations) |
| [mobile-touch](skills/mobile-touch/SKILL.md) | 移动端触控交互动效：手势动画、触控反馈、页面过渡、物理质感 | [skills.sh](https://skills.sh/dylantarre/animation-principles/mobile-touch) |
| [framer-motion](skills/framer-motion/SKILL.md) | React 声明式动画：布局动画、手势系统、SVG 动画、编排与变体 | [skills.sh](https://skills.sh/mindrally/skills/framer-motion) |

## 工作流

```
动效词汇 ──→ Tailwind 动画 / Framer Motion
 (设计原则)     (CSS 实现 / React 实现)
     └──→ 移动端触控
          (手势交互)
```

## 安装

```bash
# 整库安装（推荐）—— 拿到路由层 + 全部 references/scripts/assets
npx skills add skills-repo/animation-engineer -g -y

# 单技能安装 —— 只要某一个细粒度能力，例如只要 Framer Motion
npx skills add skills-repo/animation-engineer@framer-motion -g -y
```

## 内置脚本与模板

```bash
# 校验 CSS 关键帧纪律（期望 0 error）
python3 scripts/lint_css_keyframes.py --css src/ --config assets/motion-rules.json
```

详见 `SKILL.md` 的「内置脚本」与「模板资源」两节。

## 与本组织其他仓库的关系

- **design-studio** — UI/UX 设计（设计系统、UI审查），本仓库聚焦动效与动画实现
- **ai-fullstack-engineer** — 前端组件开发与性能优化（原 frontend-engineer 已归档并入此仓库），本仓库聚焦交互动画层面
- **accessibility-engineer** — 无障碍工程（WCAG、键盘/读屏），本仓库负责动效侧的 `prefers-reduced-motion` 降级
- **indie-game-developer** — 游戏开发（Three.js），本仓库聚焦 Web/移动端 UI 动效
- **mobile-developer** — 移动端开发，本仓库提供移动端触控动效能力
