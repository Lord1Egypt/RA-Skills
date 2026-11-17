# CSS 关键帧实战（CSS Keyframes Playbook）

> `tailwind-animations` 讲 Tailwind 侧，`animation-vocabulary` 讲原理，本篇聚焦
> **裸 CSS @keyframes 的写法纪律**：哪些属性能动、哪些会卡、重复与命名怎么管。
> 这些纪律被 [lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 固化成门禁，本篇讲"为什么"。
> 子技能装不下的"CSS 关键帧反模式清单"在这里。

## 1. 只动合成属性能（铁律）

浏览器渲染管线：JS → Style → Layout → Paint → Composite。越靠后越便宜。

| 属性 | 触发 | 成本 |
|------|------|------|
| transform / opacity | 仅 Composite | 最便宜（GPU 合成） |
| filter / backdrop-filter | Paint+Composite | 中（离屏） |
| top/left/width/height | Layout+Paint | 贵（重排） |
| margin/padding/box-shadow | Layout/Paint | 贵 |

**法则**：动画只用 `transform` 与 `opacity`。位移用 `translate*`，缩放用 `scale`，旋转用 `rotate`，显隐用 `opacity`。绝不用 `top/left` 做位移动画。

## 2. 关键帧起止要用 transform/opacity

一个关键帧若起止都不用 `transform`/`opacity`，要么无动画（属性没变），要么在动 layout 属性（卡）。
`lint_css_keyframes.py` 会标出"起止未用 transform/opacity"的关键帧。

```css
/* 好：起止都是 transform + opacity */
@keyframes slideIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 坏：用 top 做位移，每帧重排 */
@keyframes slideBad {
  from { top: 8px; }
  to   { top: 0; }
}
```

检测逻辑：取关键帧的 `from/0%` 与 `to/100%` 选择器，若两者都没有 `transform` 也没有 `opacity`，判定为缺失起止 GPU 属性 → 报错。

## 3. 命名与重复

- **命名语义化**：`fadeIn` / `slideUp` / `spinSlow`，别 `anim1` / `kf-a`
- **禁止重复定义同名 @keyframes**：后者覆盖前者，行为诡异。`lint` 会报重复名
- **作用域**：全局 `@keyframes` 同名会互相覆盖；组件级动画用 CSS Modules / 前缀隔离
- **复用**：用 CSS 变量参数化时长/缓动，而非复制 N 份关键帧

```css
:root { --ease-out: cubic-bezier(0.16, 1, 0.3, 1); --dur: 300ms; }
.fade { animation: fadeIn var(--dur) var(--ease-out); }
```

## 4. will-change 与合成层

`will-change: transform` 提示浏览器提前提层，但**别滥用**：

- 只对"即将动画且频繁"的元素加，动画结束移除
- 长期挂大量 `will-change` 会吃掉显存，反而更卡
- 小动画不用 will-change，浏览器已默认优化 transform/opacity

```css
.card { will-change: transform; transition: transform 200ms; }
.card:hover { transform: scale(1.02); }
/* 离开后移除：.card:not(:hover){ will-change: auto; } */
```

## 5. 时长与缓动约定（接 design token）

- 微交互 100–200ms；页面过渡 300–500ms；入场 500–800ms（见 animation-vocabulary）
- 缓动：进场用 ease-out（快进慢出），退场用 ease-in；弹性交互用 cubic-bezier
- 不要所有动画都用 `linear`——线性最"机械"，缺生命感
- 用 CSS 变量统一，别散落魔法数字（见 references/motion-design-system.md）

## 6. 典型坑与规避

- **坑：transition-all** 过渡了 width/box-shadow，卡。*规避*：显式 `transition: transform 200ms`。
- **坑：@keyframes 重名**被覆盖。*规避*：lint 查重名；组件加前缀。
- **坑：起止无 transform/opacity**导致 jank 或无动画。*规避*：lint 查起止 GPU 属性。
- **坑：无限动画烧 CPU**（一直转圈）。*规避*：非必要不加 `infinite`；离开视口暂停。
- **坑：box-shadow 做动画**paint 重。*规避*：用伪元素 + opacity 模拟，或接受中成本。
- **坑：动画不降级**眩晕用户。*规避*：prefers-reduced-motion 关掉（见 performance-accessibility.md）。

## 7. 收口清单

- [ ] 动画只用 transform/opacity，无 top/left/width 位移动画
- [ ] 每个 @keyframes 起止都用了 transform 或 opacity（lint 通过）
- [ ] 无重复 @keyframes 名（lint 通过）
- [ ] 命名语义化，组件动画加前缀/作用域隔离
- [ ] will-change 仅用于频繁动画元素，结束即移除
- [ ] 时长/缓动走 CSS 变量 token，无散落魔法数字
- [ ] 不用 transition-all；显式指定 transition-property
- [ ] [lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 对样式文件 0 error

## 8. 滚动驱动动画（scroll-driven）

现代浏览器支持原生滚动驱动，无需 JS 监听 scroll：

```css
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
.progress {
  animation: grow auto linear;
  animation-timeline: scroll(root block);   /* 跟页面滚动 */
}
@keyframes reveal { from { opacity: 0; transform: translateY(20px);} to {opacity:1;transform:none;} }
.card { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% cover 40%; }
```
注意：滚动驱动动画仍是 transform/opacity，性能友好；老浏览器不支持时优雅降级（无动画）。lint 不会拦这类（起止用的是 transform/opacity）。

## 9. @property 与可插值性

CSS 自定义属性默认不能平滑插值（只认关键字切换）。用 `@property` 注册后可动画：

```css
@property --angle { syntax: '<angle>'; initial-value: 0deg; inherits: false; }
@keyframes spin-grad { to { --angle: 360deg; } }
```
否则 `background`/渐变角度这类"非可插值"属性做动画会跳变。规则：能动画的属性必须是浏览器可插值的（transform/opacity/数值/@property 注册值）。

## 10. 调试技巧

- DevTools → Elements → 动画面板：看关键帧、时长、缓动曲线，逐帧
- Rendering → "Paint flashing"：红色区域=每帧重绘（说明动了 layout/paint 属性）
- Performance → 录制动画：看是否掉帧、长任务是否在主线程
- 验证 lint：把样式文件跑 [lint_css_keyframes.py](../scripts/lint_css_keyframes.py)，0 error 才算纪律达标

## 11. 反模式速查表

| 反模式 | 后果 | 正解 |
|--------|------|------|
| `transition-all` | 过渡不该过渡的属性，卡 | 显式 transition-property |
| top/left 位移 | 每帧重排 | translate |
| 同名 @keyframes | 后者覆盖，行为诡异 | 语义命名+前缀，lint 查重 |
| 起止无 transform/opacity | jank/无动画 | lint 查起止 |
| 无限旋转烧 CPU | 耗电/掉帧 | 非必要不加 infinite |
| box-shadow 动画 | paint 重 | 伪元素+opacity 或接受中成本 |
| 不接 reduced-motion | 眩晕差评 | 媒体查询降级 |

## 12. 与脚本衔接

[lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 固化本篇纪律：查重名（E1）、查起止无 transform/opacity（E2）、
警告 layout 属性（W）与未定义引用（W）。CI 里跑，缺一项即红，避免"能跑但不规范"的静默劣化。

## 相关子技能与层次边界

本 playbook 负责**裸 CSS @keyframes 的写法纪律**（只动 transform/opacity、命名/重名、起止 GPU 属性、will-change/合成层），
由 [lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 固化成门禁；子技能负责各自栈的"怎么写"。层次边界：

- 原理层 → [animation-vocabulary](../skills/animation-vocabulary/SKILL.md)：缓动曲线、时长、GPU 加速属性的概念来源；本篇是这些概念在裸 CSS 上的可执行纪律。
- Tailwind 关键帧 → [tailwind-animations](../skills/tailwind-animations/SKILL.md)：在 `tailwind.config` 里定义的 `@keyframes` 同样受本篇 lint 约束（重名/起止），互补而非替代。
- 不写裸 @keyframes 的栈 → [framer-motion](../skills/framer-motion/SKILL.md) / [mobile-touch](../skills/mobile-touch/SKILL.md)：走各自库的声明式 API（variants / 手势），不适用本篇纪律。
- 兄弟参考：
  - [decision-animation-tech.md](decision-animation-tech.md)：先选"裸 CSS 关键帧"还是其它栈（决策树 §1/§9）。
  - [motion-design-system.md](motion-design-system.md)：时长/缓动 token 统一，避免散落魔法数字。
  - [performance-accessibility.md](performance-accessibility.md)：transform/opacity 与 reduced-motion 降级（性能底线）。

