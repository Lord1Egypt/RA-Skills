# 动效技术选型（Animation Tech Selection）

> 子技能 `animation-vocabulary`(原理) / `framer-motion`(React) / `mobile-touch`(移动触控) /
> `tailwind-animations`(Tailwind) 各自讲"怎么写"，本篇讲"先选哪套技术"——选错会让
> 同样的动效在不同栈里重写三遍。先决策树定性，再矩阵定量，最后清单收口。

## 1. 决策树（先定性）

```
Q0 运行环境是 React 项目吗？
├─ 是 → Q0a 需要编排/手势/共享元素动画吗？
│       ├─ 是 → Framer Motion（framer-motion），声明式最省心
│       └─ 否（单纯过渡）→ Tailwind 动画类 或 裸 CSS
└─ 否 → Q1

Q1 是纯 CSS 能覆盖的简单过渡吗？
├─ 是 → 裸 CSS @keyframes / transition（零依赖，最快）
└─ 否 → Q2

Q2 需要时间线/滚动驱动/复杂序列吗？
├─ 是 → GSAP（时间线最强）或 Web Animations API（原生）
└─ 否 → Q3

Q3 是设计交付的复杂矢量动画（插画级）吗？
├─ 是 → Lottie（Bodymovin 导出），但注意体积与交互受限
└─ 否 → 裸 CSS 或 WAAPI 足够

Q4 移动端触控手势动效？
└─ 是 → 见 mobile-touch：CSS/Framer Motion + 物理弹簧，原生质感
```

**口诀**：React 编排 → Framer Motion；简单过渡 → CSS/Tailwind；时间线复杂 → GSAP；
矢量交付 → Lottie；移动触控 → mobile-touch。

## 2. 选型矩阵（定量）

| 维度 | 裸 CSS | Tailwind 动画 | Framer Motion | GSAP | WAAPI | Lottie |
|------|--------|---------------|---------------|------|-------|--------|
| 依赖 | 无 | Tailwind | React 库 | JS 库 | 无(原生) | 渲染库 |
| 学习成本 | 低 | 低 | 中 | 中-高 | 中 | 低(用导出) |
| 编排/序列 | 弱 | 弱 | 强 | 最强 | 中 | 弱 |
| 手势 | 需手写 | 需手写 | 内置 | 需手写 | 需手写 | 无 |
| 滚动驱动 | 难 | 难 | 中 | 强 | 中 | 无 |
| 共享元素 | 难 | 难 | 内置(layoutId) | 中 | 中 | 无 |
| 体积 | 0 | 小 | 中 | 中 | 0 | 大(JSON) |
| 可访问性 | 需手写 | 需手写 | 内置 reduced | 需手写 | 需手写 | 需包一层 |
| 适合 | 简单过渡 | 快速反馈 | React 交互动效 | 时间线/滚动 | 原生无依赖 | 插画级交付 |

## 3. 何时不要上库

- 只做 hover/焦点过渡 → 裸 CSS `transition` 足矣，别引 Framer Motion
- 只做 Tailwind 内的入场 stagger → `tailwind-animations` 的 `animate-*` + delay 即可
- 性能极敏感且逻辑简单 → WAAPI 直接控制合成层，零依赖
- **反模式**：为"页面有个淡入"就装 GSAP，体积与复杂度都不值

## 4. CSS vs JS 动画的边界

- **CSS 负责**：过渡、简单关键帧、hover/焦点反馈——交给合成线程，不占主线程
- **JS 负责**：依赖状态的复杂编排、跟手手势、滚动联动、可中断动画
- **不要**用 JS 去"逐帧改 style"做本可 CSS 完成的过渡——主线程阻塞、掉帧
- **折中**：用 WAAPI（`element.animate()`）在 JS 里声明、但由浏览器合成，兼顾控制与性能

## 5. 典型坑与规避

- **坑：用 top/left/width 做动画**，触发 layout/paint 每帧重排。*规避*：用 `transform`/`opacity`（仅合成）。
- **坑：React 里用 CSS 类切换做复杂编排**，状态散落难维护。*规避*：Framer Motion 的 variants 集中管理。
- **坑：Lottie JSON 体积爆**，一个动画几百 KB。*规避*：精简图层、降帧、按需加载。
- **坑：动画不接 prefers-reduced-motion**，眩晕用户差评。*规避*：所有动效提供降级（见 references/performance-accessibility.md）。
- **坑：Tailwind 默认 `transition-all`**，过渡了不该过渡的属性。*规避*：指定 transition-property。

## 6. 收口清单

- [ ] 用 §1 决策树定出技术，并写"为何不选其它"的反向论证
- [ ] 用 §2 矩阵确认依赖/体积/编排需求与现状匹配
- [ ] 简单过渡已优先用 CSS/Tailwind，没过度引库
- [ ] React 编排/手势已选 Framer Motion；时间线复杂已选 GSAP
- [ ] 矢量交付走 Lottie 且体积可控
- [ ] CSS/JS 边界清晰：合成线程能做的不过主线程
- [ ] 所有动效接了 prefers-reduced-motion 降级
- [ ] 选型结论同步给 `framer-motion` / `tailwind-animations` / `mobile-touch`

## 7. 与子技能衔接

- 动效原理/缓动/时长 → `animation-vocabulary`
- React 声明式动画 → `framer-motion`
- Tailwind 动画类/关键帧 → `tailwind-animations`
- 移动端触控手势 → `mobile-touch`
- CSS 关键帧规范与 lint → 见 [css-keyframes-playbook.md](css-keyframes-playbook.md) + [lint_css_keyframes.py](../scripts/lint_css_keyframes.py)
- 性能与可访问性 → 见 [performance-accessibility.md](performance-accessibility.md)

## 8. WAAPI 实战（原生无依赖的折中）

需要 JS 控制但不想引库，用 Web Animations API：声明式写在 JS、由浏览器合成。

```js
el.animate(
  [{ opacity: 0, transform: 'translateY(8px)' },
   { opacity: 1, transform: 'translateY(0)' }],
  { duration: 240, easing: 'cubic-bezier(0.16,1,0.3,1)', fill: 'both' }
);
```
优势：零依赖、可控中断/反向、返回 Animation 对象可监听 `onfinish`。适合"少量需要跟状态的动效"，比 Framer Motion 轻，比裸 CSS 可控。注意：可访问性降级（prefers-reduced-motion）仍需自己在 JS 里判断。

## 9. 同一动效在三栈的实现对比

以"卡片入场（淡入+上移+stagger）"为例：

- **裸 CSS**：`@keyframes` + `animation-delay: calc(var(--i)*60ms)`，零依赖但编排散
- **Tailwind**：`motion-safe:animate-[fadeIn_240ms] [animation-delay:...]`，快速但复杂编排吃力
- **Framer Motion**：`variants` + `staggerChildren`，声明式最强、可中断、内置 reduced-motion
- **GSAP**：`timeline().from(cards, {y:8, opacity:0, stagger:0.06})`，时间线最精细

选型结论：单页少量动效 → CSS/Tailwind；React 应用多交互 → Framer Motion；时间线/滚动复杂 → GSAP。

## 10. 框架/SSR 注意点

- **Next.js / SSR**：Framer Motion 需客户端组件（`"use client"`），避免服务端渲染动画初态闪烁——用 `initial={false}` 或 `suppressHydrationWarning`
- **CSS-in-JS**：关键帧随组件加载，首屏可能闪；关键动画放全局 CSS
- **Tailwind**：自定义 `@keyframes` 写在 `tailwind.config` 的 `theme.extend.keyframes`，别散落 `<style>`
- **Vue / 其它**：多数动画库有对应封装，优先官方封装而非手搓

## 11. 反向论证模板（收口必写）

> 我选〔技术〕不选〔A〕/〔B〕：① 〔A〕在〔维度〕不满足〔约束〕；
> ② 项目是〔栈〕，〔技术〕契合；③ 〔风险〕有〔缓解〕。若未来〔触发〕，则回到 §4 重评。

## 相关子技能与层次边界

本 playbook 负责**动效技术选型决策**（先选哪套技术，决策树 + 矩阵 + 反向论证）；选完之后"某栈具体怎么写"由各子技能负责。层次边界：

- React 编排/手势 → [framer-motion](../skills/framer-motion/SKILL.md)：决策树 Q0 命中"React + 编排/手势"时落地。
- 移动端触控 → [mobile-touch](../skills/mobile-touch/SKILL.md)：决策树 Q4 命中"移动触控手势"时落地。
- Tailwind 快速反馈 → [tailwind-animations](../skills/tailwind-animations/SKILL.md)：单纯过渡/入场 stagger 走 Tailwind 动画类。
- 原理/词汇 → [animation-vocabulary](../skills/animation-vocabulary/SKILL.md)：缓动、时长、GPU 属性等选型依据的概念层。
- 兄弟参考：
  - [css-keyframes-playbook.md](css-keyframes-playbook.md)：选了"裸 CSS"后的关键帧写法纪律 + lint。
  - [motion-design-system.md](motion-design-system.md)：设计系统层的时长/缓动 token 规范。
  - [performance-accessibility.md](performance-accessibility.md)：选型时就要考虑的 GPU/reduced-motion 底线。

