# 动效设计规范系统（Motion Design System）

> `animation-vocabulary` 给了缓动/时长原则，本篇把"原则"落成"可落地的设计规范"：
> 时长/缓动 token、编排与 stagger、跨组件一致性、检查清单。让一个产品的动效
> 像同一套语言，而不是每人各写各的。这是 design system 团队的核心交付。

## 1. 为什么需要动效 token

散落的魔法数字（`transition: 250ms ease`）会导致：同一产品里按钮 200ms、卡片 400ms、
弹窗 300ms，节奏混乱。用 token 统一，改一处全局调。

```css
:root {
  --motion-duration-fast: 120ms;   /* 微交互：hover/焦点 */
  --motion-duration-base: 240ms;   /* 常规过渡 */
  --motion-duration-slow: 400ms;   /* 页面/模态 */
  --motion-duration-enter: 600ms;  /* 大入场 */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in:      cubic-bezier(0.4, 0, 1, 1);
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1); /* 回弹 */
}
```

## 2. 时长分级规范

| 级别 | token | 范围 | 用途 |
|------|-------|------|------|
| 微交互 | fast | 100–150ms | hover、toggle、焦点环 |
| 常规 | base | 200–280ms | 按钮、卡片、tooltip |
| 慢 | slow | 350–500ms | 模态、抽屉、页面切换 |
| 入场 | enter | 500–800ms | 列表/页面大入场 |
| 编排单位 | — | 40–80ms | stagger 单步间隔 |

原则：越小的元素越快；位移越大、元素越重要，时长可适当加。但同一级内必须一致。

## 3. 缓动语义

- **ease-out（快进慢出）**：进场、出现类——用户期待"快速响应、柔和落定"
- **ease-in（慢进快出）**：退场、消失类
- **标准（对称）**：属性切换、状态变化
- **spring（回弹）**：物理质感交互（拖动、点赞）——但要克制，过多显廉价
- 禁止：所有动画 `linear`（机械），所有动画同一曲线（无层次）

## 4. 编排与 stagger（多元素出场）

多元素同时出现要有秩序，而非齐刷刷闪现：

```css
/* stagger：用 --i 变量错开 */
.item { animation: enter var(--dur-enter) var(--ease-out); animation-delay: calc(var(--i) * 60ms); }
```
```js
// Framer Motion variants 编排
const container = { hidden: {}, show: { transition: { staggerChildren: 0.06 } } };
const item = { hidden: { opacity: 0, y: 8 }, show: { opacity: 1, y: 0 } };
```
规则：
- stagger 间隔 40–80ms，过多显拖沓
- 出场顺序符合视觉阅读顺序（左→右、上→下）
- 离开动画比进入快（用户更没耐心等消失）
- 不要对超过 ~12 个元素做 stagger，否则像瀑布卡顿

## 5. 跨组件一致性清单

- [ ] 所有时长走 token，无散落魔法数字（grep 查 `ms` 硬编码）
- [ ] 缓动语义统一（进场 ease-out、退场 ease-in）
- [ ] hover/焦点反馈时长一致（用 fast token）
- [ ] 模态/抽屉用 slow token，不忽快忽慢
- [ ] stagger 间隔统一，顺序符合阅读流
- [ ] 同类型交互（如所有"展开"）动效一致
- [ ] 动效规范写入 design system 文档，新组件照表实现

## 6. 规范落地与校验

把 token 放进 design system 的 CSS 变量/主题，组件库默认引用。配合：
- [css-keyframes-playbook.md](css-keyframes-playbook.md) 的 CSS 纪律
- [lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 守关键帧起止与重名
- 代码评审 grep `transition:.*\d+ms` 看是否走了 token

## 7. 常见坑与规避

- **坑：时长各写各的**导致节奏乱。*规避*：token 强制统一。
- **坑：stagger 间隔太大**像卡顿。*规避*：40–80ms，元素 >12 不 stagger。
- **坑：缓动全用 linear**机械。*规避*：语义化 ease-out/in。
- **坑：动效规范只写在文档没人用**。*规避*：落成 token + lint 门禁。
- **坑：入场动画遮挡内容阅读**。*规避*：入场 ≤800ms，重要内容优先可见。

## 8. 收口清单（设计系统交付）

- [ ] 已定义时长 token（fast/base/slow/enter）与缓动 token
- [ ] 时长分级规范文档化，范围明确
- [ ] 缓动语义约定（进场/退场/标准/回弹）
- [ ] stagger 间隔与顺序规则已定
- [ ] 跨组件一致性清单（§5）逐项过
- [ ] token 进主题，组件库默认引用，新组件照表
- [ ] lint + grep 门禁守 CSS 纪律
- [ ] [assets/motion-checklist.md](../assets/motion-checklist.md) 已作为发布前动效检查清单

## 9. 与组件库集成

token 不是孤立变量，要落地进组件库的默认样式：

```css
/* 按钮：默认走 base token，hover 走 fast token */
.btn { transition: transform var(--motion-duration-base) var(--ease-standard); }
.btn:hover { transform: translateY(-1px); transition-duration: var(--motion-duration-fast); }
/* 模态：slow token + ease-out */
.modal { animation: modalIn var(--motion-duration-slow) var(--ease-out); }
```
组件库文档写明"动效必须引用 token，禁止硬编码 ms"，新组件 PR 用 lint/grep 守门。

## 10. 与 Figma 动效标注对接

设计给的动效标注要能直接映射 token，避免开发二次发挥：

- Figma 的 Smart Animate 时长/缓动 → 对应 `--motion-duration-*` / `--ease-*`
- 标注模板：`[元素] [触发] [时长token] [缓动token] [属性]`
- 例：`卡片 hover 120ms fast ease-standard translateY(-1px)`
- 设计交付物含"动效规范表"，与开发 token 一一对应

## 11. 规范的版本演进

动效规范随产品成长，要版本化：

- v1：时长/缓动 token + 基础 stagger 规则
- v2：加入编排语义（父子级联、离开快于进入）、reduced-motion 分级
- v3：滚动驱动、共享元素等高级模式
- 每次演进同步更新 token 与 [assets/motion-checklist.md](../assets/motion-checklist.md)，旧组件逐步迁移

## 12. 完整 token 示例（可直接抄）

```css
:root {
  --motion-duration-fast: 120ms;
  --motion-duration-base: 240ms;
  --motion-duration-slow: 400ms;
  --motion-duration-enter: 600ms;
  --motion-stagger: 60ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in:      cubic-bezier(0.4, 0, 0, 1);
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1);
}
@media (prefers-reduced-motion: reduce) {
  :root { --motion-duration-fast: 0.01ms; --motion-duration-base: 0.01ms;
          --motion-duration-slow: 0.01ms; --motion-duration-enter: 0.01ms; }
}
```
这样 reduced-motion 自动把时长压到近乎 0，全站降级无需逐个改。

## 13. 动效评审 PR 清单（落地守门）

组件/页面动效上线前，评审按此卡过：

- [ ] 时长引用了 token（无 `120ms` 这类硬编码散落）
- [ ] 缓动符合语义（进场 ease-out / 退场 ease-in / 标准对称）
- [ ] 仅用 transform/opacity（lint 0 error）
- [ ] stagger 间隔 40–80ms，顺序符合阅读流
- [ ] 同类型交互动效与既有一致（不另起炉灶）
- [ ] reduced-motion 下装饰动效关闭、功能反馈保留
- [ ] 动效未进首屏关键渲染路径（LCP 不受影响）
- [ ] 时长/缓动变更同步更新 design system 文档

任一项不过，PR 打回——动效规范是"规范"不是"建议"，靠评审 + lint 双守才不会漂移。

## 相关子技能与层次边界

本 playbook 负责**动效设计规范系统**（时长/缓动 token、编排与 stagger、跨组件一致性），
把 `animation-vocabulary` 的原理落成可落地的 token 与评审门禁；各子技能是规范的具体落地栈。层次边界：

- 原理 → token → [animation-vocabulary](../skills/animation-vocabulary/SKILL.md)：缓动/时长/编排原则在此落成 `--motion-*` token 与分级规范。
- React 落地 → [framer-motion](../skills/framer-motion/SKILL.md)：variants 编排、staggerChildren 直接消费本篇 token。
- Tailwind 落地 → [tailwind-animations](../skills/tailwind-animations/SKILL.md)：`animate-*` 类引用 token，避免硬编码 ms。
- 移动端落地 → [mobile-touch](../skills/mobile-touch/SKILL.md)：触控反馈时长/弹簧也走同一套 token，保持跨端一致。
- 兄弟参考：
  - [css-keyframes-playbook.md](css-keyframes-playbook.md)：token 之外的裸 CSS 关键帧纪律。
  - [performance-accessibility.md](performance-accessibility.md)：规范里的 reduced-motion 降级分级。
  - [decision-animation-tech.md](decision-animation-tech.md)：先选型、再套规范。


