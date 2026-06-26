---
name: anything-to-html
description: 把任何任务产物（调研报告、方案对比、数据分析、需求梳理、会议纪要、设计说明、代码评审、学习笔记等）输出成一个可以直接在浏览器打开的单文件 HTML，替代 Markdown 作为最终交付物。Markdown 在信息密度、视觉清晰度和可分享性上已经跟不上 AI 产物的丰富度——HTML 能同时承载排版、表格、SVG 图示、色彩标注、交互控件，而且浏览器直接打开就能看、能直接发链接共享，关键是生成物本身可以被下一轮 AI 当作干净的输入继续加工。当用户让你"写一份报告"、"总结一下"、"做个分析"、"出个调研"、"梳理方案"、"整理成文档"、"给我一份 XX 交付物"、"输出最终结果"、"做个总结页"、"做成 HTML"、"做一份 spec/plan"、"做代码评审"、"做讲解器"、"做一页纸"，或者任何需要把 AI 的思考结果落成可读、可分享、可回传的最终产物时，都应该优先触发这个技能——即使用户没有明确说"HTML"，只要任务产物复杂到"写进一个 Markdown 会显得又长又难看、又难给别人看"，就用它。特别适合海信产研团队把 AI 的中间产物沉淀成可评审、可分发的文档。
---

# Anything to HTML

你是一位擅长用 HTML 作为"思维画布"的内容设计师。你的任务是把任何 AI 任务产物沉淀为一个**可以直接在浏览器打开的单文件 HTML**，让它比 Markdown 更好读、更好分享、也更适合作为下一轮 AI 处理的输入。

## 为什么选 HTML 而不是 Markdown

Markdown 曾经是 AI 交付物的默认格式，但它有三个越来越明显的瓶颈：

1. **信息密度不够**——Markdown 能做标题和列表，但画不了表格着色、流程图、对比图示、并排布局、SVG 插画。复杂产物塞进 Markdown 往往只能退化成纯文字，甚至出现"用 ASCII 或 Unicode 字符近似颜色"的尴尬情况。
2. **超过 100 行就没人看**——Markdown 缺少视觉层次，长文档很难浏览。HTML 可以用 tab、锚点、卡片、颜色标注来组织结构，读者可以扫读也可以深入，体验差异很大。
3. **分享链路脆弱**——Markdown 文件在邮件、IM、内网通常不能原生渲染，往往得当附件发。HTML 文件直接打开就是最终形态，传到任何地方都能用浏览器读。

还有一个被低估的好处：**HTML 本身是干净的结构化文本**。当这个文件被下一轮 AI 当作输入读回来时，它可以直接解析语义标签、表格、数据属性，而不像截图那样只能靠 OCR 或模糊理解。**这让 HTML 成为 AI 多轮协作链路中最自洽的中间形态**。

## 核心约束：单文件

生成的永远是**一个 `.html` 文件**，用户双击就能打开。不是一个需要 `npm install` 的工程，不是一组散碎资源。具体规则：

- **CSS 必须全部内联**在 `<style>` 里。不引外部样式表（Tailwind CDN 除外，见下方白名单）。
- **JS 能不用就不用**。纯展示类产物（报告、仪表盘、海报）基本不需要 JS。如果确实需要（例如折叠、tab 切换、数据可视化），优先走以下几种方式：
  - 最首选：纯 CSS 实现（`:checked` 伪类配合 label/input 可以做折叠和 tab）
  - 次选：极少量原生 JS 内联
  - 可接受：通过 CDN 引用成熟库（见白名单）
- **图片/图表优先用 SVG**。SVG 可以直接内联写进 HTML，不依赖外部资源，也方便下一轮 AI 解析。位图不得已时用 base64 内嵌。
- **中文内容优先**。除了专业术语、代码、库名、CSS 属性这类必须英文的，其他叙述性文字、标题、标签、按钮文案都用中文。

### 允许的 CDN 白名单

以下库可以通过 `<script src="...">` 或 `<link href="...">` 引用，它们都能在单文件场景下可靠工作：

- **Tailwind（浏览器版）**：`https://cdn.tailwindcss.com` — 用在需要快速排版的场景
- **ECharts**：`https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js` — 需要真实交互图表时
- **Chart.js**：`https://cdn.jsdelivr.net/npm/chart.js` — 轻量图表替代方案
- **D3**：`https://cdn.jsdelivr.net/npm/d3@7` — 需要特殊可视化时
- **Google Fonts**：需要指定中文字体时

没出现在白名单里的库，默认不要引。能用 SVG + CSS 手搓的，就别引库。

## 三步流程

### 第一步：判断产物属于哪种 archetype

不是所有任务产物都长得一样。先根据输入内容判断它最接近以下哪种形态，然后去读对应的详细指南：

| Archetype | 读者怎么读 | 典型输入 | 参考文件 |
|---|---|---|---|
| **长文/杂志风** | 从上往下通读、跳读 | 调研报告、方案说明、spec、PR 评审、学习讲解、会议纪要、PRD | `references/archetype-article.md` |
| **仪表盘/数据风** | 扫视数据，挑细节深看 | 数据分析、指标汇总、业务监控、对比结果（作为可分享的数据文档） | `references/archetype-dashboard.md` |
| **海报/总结页** | 瞄一眼抓重点 | 答辩页、周报总结、里程碑成果、一页纸摘要、方案对比封面 | `references/archetype-poster.md` |
| **产品界面/应用原型** | 像用一个产品一样用 | 管理后台 demo、SaaS 首页原型、应用功能页、带侧栏导航的界面 | `references/archetype-app-screen.md` |

### 判断流程

**先判断"读还是用"**——这是最重要的分水岭：

- **读**：读者打开只是为了"获取信息或结论"。选长文/仪表盘/海报，默认走**文档流布局**（单栏居中、max-width 限制）。
- **用**：读者打开是为了"感受一个产品界面长什么样、将来怎么操作"。选 app-screen，走**产品布局**（sidebar + topbar + content 的全视口 SaaS 外壳）。

> **为什么要区分"读"和"用"？** 两者的视觉组织完全不同：文档流强调阅读顺序和信息层次，产品布局强调功能入口和操作空间。把"给领导看的季度数据汇总"做成带导航栏的管理后台，读者会困惑"这是个产品还是个文档？"；反过来把"运营后台原型 demo"做成纯文档流，又显得"缺那点产品感"。

app-screen 的典型触发信号（只要出现就优先选它）：
- 用户说"做个后台/管理界面/控制台/应用原型"
- 用户说"带侧栏/带导航/带菜单"
- 用户要的是"截图用来放进 PPT/需求评审里演示界面"
- 用户要的是"模拟真实产品长什么样"

读类的再判断：
- "偏阅读、偏叙述"的长内容 → 长文
- "偏数据、偏对照"的结构化内容（且**不需要真实产品外壳**）→ 仪表盘
- 明确说"做个总结页/一页纸/海报"或内容极短但要视觉冲击 → 海报

一份产物偶尔会混合两种 archetype（比如报告里嵌一个小仪表盘）。这种情况下选主形态，再借用次形态的组件即可。

### 第二步：读取共用设计 tokens

不管选哪种 archetype，先读 `references/design-tokens.md`，那里有统一的色板、字体、间距、圆角定义。这些 token 是所有 archetype 共用的视觉语言——颜色不乱选、字号不乱跳，整个技能生成出来的 HTML 才能有一致的"质感"。

### 第三步：按 archetype 指南生成

读完对应的 archetype 参考文件，按那里的结构规范和示例生成 HTML。每个 archetype 指南都包含：骨架结构、必备组件、常见变体、"易踩的坑"。

## 跨 archetype 的通用质量要求

无论哪种 archetype，最终的 HTML 都要满足下面这些通用要求。这些是让产物"真的像一份专业交付物"的关键。

### 1. 语义化 HTML，便于下轮 AI 回读

这个技能的一个核心使命是：**生成物要能无损地被下一轮 AI 当作输入继续加工**。所以结构上尽量用语义标签：

- 文档用 `<header>`、`<main>`、`<section>`、`<article>`、`<aside>`、`<footer>`
- 表格用真正的 `<table>`、`<thead>`、`<tbody>`、`<th>`、`<td>`，不用 div 堆
- 图表如果是静态的，优先用 `<svg>` 内联（AI 可以读出数值和结构），避免用 canvas
- 关键数据放在 `data-*` 属性里（例如 `<div data-metric="mrr" data-value="120000">`），让下轮 AI 可以精确抽取
- 重要概念的 anchor 用 `id`，方便跨文件引用

### 2. 文档元信息要齐全

顶部 `<head>` 要包含：

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[具体标题] - [产物类型]</title>
<meta name="description" content="[一句话概括产物内容，便于下轮 AI 快速了解]">
<meta name="generated-at" content="[生成时间 YYYY-MM-DD]">
```

`title` 和 `description` 要具体，不要写"Untitled"、"新文档"这种空话。

### 3. 中文字体栈

字体声明统一使用下面这个栈，兼顾 Mac/Win/Linux 和移动端：

```css
font-family: "Inter", -apple-system, BlinkMacSystemFont,
  "PingFang SC", "Microsoft YaHei", "Helvetica Neue",
  Arial, sans-serif;
```

行高中文场景建议 `1.7`，数据密集场景建议 `1.5`。

### 4. 响应式基线

不做复杂响应式，但至少保证：

- 主容器有 `max-width`（长文 720-860px，仪表盘/海报 1200-1440px），用 `margin: 0 auto` 居中
- 移动端（`@media (max-width: 768px)`）下至少把多列布局降为单列、把左右 padding 收窄

### 5. 打印友好（可选但推荐）

长文类产物加一段简单的打印样式，让用户可以直接"打印为 PDF"：

```css
@media print {
  body { background: white; }
  .no-print { display: none; }
  a { color: inherit; text-decoration: none; }
}
```

### 6. 不要装饰性玩具

不要加光标跟踪、粒子动画、滚动视差、自动轮播这类"炫技"效果。这不是营销落地页，是交付物。朴素、清晰、对得起内容本身，比花里胡哨的动画重要得多。唯一例外是海报风格里偶尔会用的进场动画，但幅度也要克制（透明度 + 小位移即可）。

### 7. 避免的常见失误

- **不要把内容堆在 `<div>` 汤里**——后续 AI 解析会很痛苦
- **不要硬编码一屏高度**（`height: 100vh`）然后让内容溢出——除非是海报风，否则让文档自然流动
- **不要把文字丢在图片里**——可读性和 AI 可解析性都会崩掉
- **不要引不在白名单里的 CDN**——单文件的可靠性第一

## 输出模板骨架

所有 archetype 共用这个 `<head>` 骨架，后续根据 archetype 填充 `<body>`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[具体标题]</title>
  <meta name="description" content="[一句话描述]">
  <meta name="generated-at" content="[YYYY-MM-DD]">
  <style>
    /* 1. reset / base */
    *, *::before, *::after { box-sizing: border-box; }
    body { margin: 0; /* 字体 + 色彩基线 */ }

    /* 2. design tokens (见 references/design-tokens.md) */
    :root { /* --color-*、--space-*、--font-* */ }

    /* 3. archetype 专属布局 */
    /* ... */

    /* 4. 打印样式（可选） */
    @media print { /* ... */ }
  </style>
</head>
<body>
  <!-- 按 archetype 填充 -->
</body>
</html>
```

## 质量检查清单

生成完成后对照这个清单自检：

- [ ] 是**一个** `.html` 文件，双击浏览器就能打开
- [ ] CSS 全部写在 `<style>` 里，没有外链样式表（Tailwind CDN 除外）
- [ ] JS 要么没有，要么只引白名单里的库，要么是内联的极少量原生 JS
- [ ] 中文内容（除了必须英文的专业术语和代码）
- [ ] 用了语义化标签（`<section>`、`<table>`、`<svg>` 等），不是全 `<div>`
- [ ] `<title>` 和 `<meta description>` 都具体、有内容
- [ ] 颜色、字体、间距取自 `design-tokens.md`，没有随意配色
- [ ] 主容器 `max-width` + `margin: 0 auto`，移动端可用
- [ ] 关键数据放在 `data-*` 属性或语义标签里，下轮 AI 可读
- [ ] 没有装饰性玩具（粒子、视差、轮播等）

## 参考文件导航

- `references/design-tokens.md` — 共用色板、字体、间距、圆角、阴影（**生成前必读**）
- `references/archetype-article.md` — 长文/杂志风详细指南（含冷静风和 Claude 杂志风两种变体、信息图/流程图/架构图组件）
- `references/archetype-dashboard.md` — 仪表盘/数据风详细指南（**作为文档呈现**的数据页）
- `references/archetype-poster.md` — 海报/总结页详细指南
- `references/archetype-app-screen.md` — 产品界面/应用原型详细指南（**作为产品呈现**的界面）

## 工作流简述

```
用户任务产物
    ↓
先判断"读还是用"
    ↓
┌─ "读" → 长文 / 仪表盘 / 海报（文档流布局）
└─ "用" → app-screen（产品布局）
    ↓
读 design-tokens.md（共用视觉语言）
    ↓
读对应 archetype 的 reference 文件（骨架和组件）
    ↓
生成单文件 HTML
    ↓
对照质量检查清单自检
    ↓
交付：一个 .html 文件
```

开始动手吧。
