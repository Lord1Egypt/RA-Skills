# 动效规范检查清单（Motion Checklist）

> 动效上线前逐条过。性能与可访问性是被忽略却最影响口碑的底线。
> 可配合 [scripts/lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 自动校验 CSS 关键帧纪律（见下方「脚本自检」）。

## 一、性能（守住主线程）

- [ ] 动画只用 `transform` / `opacity`，无 `top/left/width` 位移动画
- [ ] 不用 `transition: all`，显式指定 `transition-property`
- [ ] `will-change` 仅用于频繁动画元素，结束即移除
- [ ] 滚动/输入期间实测 FPS ≥55（DevTools Performance）
- [ ] 无动画路径上的主线程长任务 >50ms
- [ ] 动画库/Lottie 体积未进首屏关键路径

## 二、CSS 关键帧纪律（lint 门禁）

- [ ] 无重复 `@keyframes` 同名
- [ ] 每个 `@keyframes` 起止都用了 `transform` 或 `opacity`
- [ ] 命名语义化（fadeIn/slideUp），组件动画加前缀或作用域隔离
- [ ] 时长/缓动走 CSS 变量 token，无散落魔法数字
- [ ] 跑 [scripts/lint_css_keyframes.py](../scripts/lint_css_keyframes.py) 对样式文件 **0 error**

```bash
python3 scripts/lint_css_keyframes.py --css src/ --config assets/motion-rules.json
```

## 三、可访问性（reduced-motion）

- [ ] `prefers-reduced-motion: reduce` 下装饰动效关闭/弱化
- [ ] 功能反馈（焦点环/按钮态）保留，仅降级为 opacity 淡入
- [ ] Framer Motion 用 `useReducedMotion()`，Tailwind 用 `motion-reduce:` 变体
- [ ] 无高频闪烁、无滚动劫持

## 四、设计规范（一致性）

- [ ] 时长走 token（fast/base/slow/enter），同级别一致
- [ ] 缓动语义统一：进场 ease-out、退场 ease-in
- [ ] stagger 间隔 40–80ms，顺序符合阅读流
- [ ] 同类型交互动效与既有一致，未另起炉灶
- [ ] 动效规范与 design system 文档/ token 对应（见 references/motion-design-system.md）

## 五、发布前回顾

- [ ] [assets/motion-spec-template.css](motion-spec-template.css) 作为规范范本已对齐
- [ ] CI 里 lint 门禁通过，无静默劣化
- [ ] 真机（Android/iOS）实测动画流畅、无眩晕反馈
- [ ] 动效未影响 LCP / 首屏可交互时间
