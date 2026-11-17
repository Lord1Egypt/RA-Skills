# 动效性能与可访问性（Animation Performance & A11y）

> `animation-vocabulary` 提了"GPU 加速属性"与 `prefers-reduced-motion` 的概念，
> 本篇把"性能不卡 + 人人可用"展开成可执行规范：合成层、主线程、降级策略、眩晕防护。
> 这是动效上线前最容易漏、却最影响口碑的一环。

## 1. 性能：守住主线程

动画卡顿的根因几乎都是"动了主线程"：

| 现象 | 根因 | 解法 |
|------|------|------|
| 滚动时动画掉帧 | 动画触发 Layout/Paint | 改 transform/opacity（见 css-keyframes-playbook） |
| 输入卡顿 | JS 逐帧改 style | 用 WAAPI/CSS，别 rAF 手写样式 |
| 内存涨 | 长期 will-change / 离屏层 | 动画结束移除 will-change |
| 首屏慢 | 动画库/JSON 过大 | 按需加载、精简 Lottie |

**测量优先**：Chrome DevTools → Performance 录一段，看长任务与帧率；FPS 表长期 <55 即有问题。别凭"感觉顺"。

## 2. 合成层与 GPU

- transform/opacity 走合成线程，不阻塞主线程，是动效的性能底线
- `will-change` 提层但耗显存，节制使用（见 css-keyframes-playbook §4）
- 大列表滚动动画：用 `content-visibility: auto` + transform，避免整列表重绘
- 3D 变换 `translateZ(0)` 老手法已大多被浏览器自动优化，不必硬加

## 3. prefers-reduced-motion（可访问性硬底线）

约 1/3 用户对动效敏感，强动效会引发眩晕/恶心。必须提供降级：

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

JS 侧（Framer Motion 等）也要读这个偏好：
```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// reduce 时禁用非必要动画，仅保留 opacity 淡入等温和过渡
```

Framer Motion 自带 `useReducedMotion()` hook；Tailwind 有 `motion-reduce:` / `motion-safe:` 变体：
```html
<div class="motion-safe:animate-spin motion-reduce:animate-none">…</div>
```

## 4. 降级策略分级

不是"全关"或"全开"，按敏感度分级：

| 级别 | 动效 | 降级做法 |
|------|------|----------|
| 必要反馈 | 按钮态、焦点环 | 保留（opacity 即可），不删 |
| 装饰 | 背景粒子、视差 | reduced-motion 时关闭 |
| 强动效 | 大位移、旋转、视差滚动 | reduced-motion 时改为淡入/直出 |
| 滚动劫持 | 整页滚动动画 | reduced-motion 时禁用，改普通滚动 |

原则：**功能反馈保留，装饰强动效降级**。别一刀切关掉所有动效（那体验也差）。

## 5. 眩晕防护清单

- [ ] 所有非必要动画在 `prefers-reduced-motion: reduce` 下关闭或弱化
- [ ] 不用"滚动劫持"（强制滚动动画绑定滚动位置）
- [ ] 背景视差幅度克制，避免前后景速度差过大
- [ ] 不长时间 `infinite` 旋转/闪烁（光敏性癫痫风险，避免高频闪烁）
- [ ] 焦点/状态反馈用 opacity 而非大幅位移，眩晕友好
- [ ] Framer Motion / Tailwind 用内置 reduced-motion 变体，不手判

## 6. 性能收口清单

- [ ] 动画仅 transform/opacity，无主线程 Layout/Paint（DevTools 验证）
- [ ] 滚动/输入期间帧率稳定 ≥55fps
- [ ] will-change 仅用于频繁动画，结束移除
- [ ] 动画库/Lottie 体积可控，按需加载
- [ ] `prefers-reduced-motion` 降级就位（CSS + JS 双保险）
- [ ] 降级分级合理：功能反馈保留、装饰强动效关闭
- [ ] 无高频闪烁、无滚动劫持
- [ ] 用 [lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 守 CSS 关键帧纪律

## 7. 与子技能衔接

- 原理/缓动/时长 → `animation-vocabulary`
- React 降级 → `framer-motion`（useReducedMotion）
- Tailwind 降级 → `tailwind-animations`（motion-reduce/motion-safe）
- 移动触控 → `mobile-touch`（触控反馈降级）
- CSS 纪律 → [css-keyframes-playbook.md](css-keyframes-playbook.md) + [lint_css_keyframes.py](../scripts/lint_css_keyframes.py)

## 8. 具体测量步骤（DevTools）

性能不是玄学，按步量化：

1. 打开 DevTools → Performance → 勾选 "Screenshots" 与 "Web Vitals"
2. 点录制，操作触发动画（hover/滚动/入场），停录
3. 看 FPS 表：绿色长条=60fps，红色=掉帧；长任务（主线程阻塞）标红
4. 看 Summary：若 "Rendering"/"Painting" 占比高，说明动了 layout/paint 属性
5. 用 Rendering → "Paint flashing" 实时看红色重绘区域
6. 移动端用远程调试（Chrome 测 Android / Safari 测 iOS），真机帧率才是真相

**门禁**：滚动/输入期间 FPS 稳定 ≥55；无 >50ms 主线程长任务在动画路径上。

## 9. 合成层可视化

- DevTools → Rendering → "Layer borders"：青色边框=合成层
- 过多层（滥用 will-change）会显存暴涨，反而掉帧
- 理想：只有"正在动画"的元素是合成层，动画结束回到普通层
- 用 `will-change` 临时提层，离开即 `auto`

## 10. Web 之外的对应

动效性能/可访问性原则跨栈通用：

| 平台 | 性能要点 | reduced-motion 对应 |
|------|----------|---------------------|
| React Native | 用 `useNativeDriver: true`，动画走原生线程 | 读系统"减少动态"设置降级 |
| Flutter | 用 transform/opacity；`AnimatedBuilder` 谨慎 | `MediaQuery.of(ctx).disableAnimations` |
| iOS SwiftUI | `.animation` 走 Core Animation；避免主线程 | `AccessibilityReducerMotion` |
| 游戏/CSS | 见本篇 + css-keyframes-playbook | `@media (prefers-reduced-motion)` |

## 11. 指标目标（发布前）

- 常规过渡：主线程占用 <2ms/帧
- 列表滚动动画：稳定 60fps（低端机 ≥30fps）
- 入场动画：不阻塞首屏可交互时间（LCP 不受影响）
- 可访问性：reduced-motion 下所有装饰动效关闭，功能反馈保留
- 体积：动效相关 JS/JSON（Lottie/GSAP）不进首屏关键路径

## 12. 收口补充清单（测量侧）

- [ ] 已用 DevTools Performance 实测动画帧率并截图留证
- [ ] FPS 稳定 ≥55，无动画路径长任务 >50ms
- [ ] 合成层数量合理（无 will-change 滥用），显存可控
- [ ] 低端真机（Android/iOS）实测达标
- [ ] Lottie/GSAP 体积未进首屏关键路径
- [ ] reduced-motion 降级在 CSS + JS 双保险通过

## 13. 实战：一个掉帧动画的修复过程

症状：列表项 hover 时整行"抖一下"，滚动时掉到 40fps。

排查（按 §8 步骤）：
1. Performance 录制 → 长任务在动画路径，Summary 里 "Rendering" 占 35%
2. Paint flashing → 整行变红（每帧重绘）
3. 看代码：`transition: all 200ms`，hover 改了 `box-shadow` + `top`

修复：
- `transition: all` → `transition: transform 200ms var(--ease-standard)`
- hover 改 `top` → 改 `transform: translateY(-2px)`
- `box-shadow` 改为伪元素 `opacity` 过渡（paint 成本降）
- 结果：Rendering 占比降到 <5%，FPS 稳定 60，长任务消失

要点：**先量后改**，Paint flashing 一眼定位"动了什么属性"，换成 transform/opacity 即解。

## 相关子技能与层次边界

本 playbook 负责**动效性能与可访问性**（合成层/GPU、主线程、reduced-motion 降级、眩晕防护）的跨栈底线；
各子技能在各自写法上接入这条底线。层次边界：

- 原理（GPU 属性/reduced-motion 概念）→ [animation-vocabulary](../skills/animation-vocabulary/SKILL.md)：transform/opacity 与降级的概念来源。
- React 降级 → [framer-motion](../skills/framer-motion/SKILL.md)：用 `useReducedMotion()` 在 JS 侧接 reduced-motion。
- Tailwind 降级 → [tailwind-animations](../skills/tailwind-animations/SKILL.md)：`motion-reduce:` / `motion-safe:` 变体直接套用。
- 移动端降级 → [mobile-touch](../skills/mobile-touch/SKILL.md)：触控反馈 60fps 与 reduced-motion 下的物理动效降级。
- 兄弟参考：
  - [css-keyframes-playbook.md](css-keyframes-playbook.md)：transform/opacity 纪律是性能底线的具体写法。
  - [motion-design-system.md](motion-design-system.md)：reduced-motion 在 token 层统一降级（§12）。
  - [decision-animation-tech.md](decision-animation-tech.md)：选型时就避开主线程动画（§4 CSS/JS 边界）。


