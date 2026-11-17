# 审查 / 评审

目标：找出最损害可用性和质感的问题，排序并附证据。先评审；只有用户要求时才改代码。

## 1. 可量化检查（实际运行，报告数字）
按项目调整路径通配。
```bash
# 不同十六进制颜色数（目标：少，且大多经由 token）
rg -o --no-filename '#[0-9a-fA-F]{3,8}\b' src | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn
# 不同字号数（目标 ≤ 6–8）
rg -o --no-filename 'font-size:\s*[^;]+|text-(xs|sm|base|lg|[0-9]?xl)|text-\[[^]]+\]' src | sort | uniq -c | sort -rn
# 圆角、阴影、z-index、Tailwind 任意值
rg -o --no-filename 'border-radius:\s*[^;]+|rounded(-[a-z0-9]+)?' src | sort | uniq -c | sort -rn
rg -o --no-filename 'box-shadow:\s*[^;]+|shadow(-[a-z]+)?' src | sort | uniq -c | sort -rn
rg -o --no-filename '\w+-\[[^]]+\]' src | sort | uniq -c | sort -rn | head -40
# 字体族、!important、内联样式
rg -o --no-filename 'font-family:\s*[^;]+' src | sort | uniq -c
rg -c '!important' src ; rg -c 'style=\{\{|style="' src
```
阈值（参考）：字面十六进制颜色 > 约 12 个、字号 > 8 档、圆角 > 3 种、阴影 > 3 种、字体族 > 2 个，或大量任意值 ⇒ 存在 token 债。

另外检查：真实文字/背景组合的对比度（WCAG AA 4.5:1 / 3:1）、Tab 键遍历看焦点是否可见、375 / 768 / 1280 视口是否溢出、`prefers-reduced-motion` 处理、图片 `alt`、表单 label。

## 2. 优先级清单

**P0 — 损坏 / 阻断（先修）**
- 文字对比度低于 AA；焦点不可见；键盘陷阱。
- 移动端布局破裂或出现横向滚动；内容重叠/被裁切。
- 主操作不清楚或被隐藏；缺少错误/加载/空状态导致用户卡住。
- 主要控件触控区 < 44px；表单没有 label。

**P1 — 质量与一致性**
- 没有清晰方向 / 通用 AI 感（见 SKILL.md 中的 slop 清单）。
- Token 债（见上方计数）；间距节奏不一致；圆角/阴影族混用。
- 层级弱：同等权重的元素太多，字号/颜色太多。
- 卡片套卡片、边框过多、装饰性渐变/毛玻璃。
- 对布局属性做动画、未处理减少动效、时长 > 500ms。

**P2 — 打磨**
- 陈词滥调文案、占位名字、emoji 图标。
- 视觉对齐、图标与文字尺寸匹配、标题 `text-wrap: balance`、等宽数字。
- 悬停/按下的微交互；图片处理方式统一。

## 3. 报告格式
```
## 摘要  （感知到的方向、总体评分 1–10、前 3 个问题）
## 指标  （颜色 N、字号 N、圆角 N、阴影 N、任意值 N、对比度不合格 N）
## P0 / P1 / P2  — 每条：是什么、在哪里（文件:行 或 屏幕区域）、为什么重要、具体修法
## 建议下一步  （如“先合并 token，再重做 Hero”）
```
