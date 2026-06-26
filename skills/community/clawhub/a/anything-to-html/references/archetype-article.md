# Archetype · 长文 / 杂志风

## 适用场景

以**叙述和解释**为主的产物，读者从上往下读一遍，追求阅读流畅度和层次清晰：

- 调研报告、技术讲解、学习笔记
- PRD、spec、实现计划、方案说明
- PR 评审、代码讲解、事故复盘
- 会议纪要、访谈整理

典型特征：段落多、小节分明、偶尔嵌入表格/代码/插图，读者需要"通读"或"跳读"。

## 核心结构

长文排版的灵魂是**单栏中等宽度 + 清晰的分节**。不要玩多栏、不要玩花哨版式，让内容本身说话。

```
┌─────────────────────────────────────────────┐
│  Cover 区（标题 + 副标题 + 元信息）           │
│  ─────────────────────                       │
│                                              │
│  目录（可折叠，长文建议加）                    │
│  ─────────────────────                       │
│                                              │
│  Section 1                                   │
│    段落、列表、表格、代码、插图                │
│  ─────                                       │
│                                              │
│  Section 2                                   │
│    ...                                       │
│                                              │
│  Footer（生成时间、附录、引用）                │
└─────────────────────────────────────────────┘
```

容器宽度 `max-width: 760px`，左右 `margin: 0 auto`。这是经过验证的中文阅读最佳宽度（约 36-40 字/行）。

## 两种风格变体

长文有两种常用的视觉风格。根据内容性质二选一，**不要混用**。

### 变体 A · 冷静克制风（默认）

适合：PR 评审、spec、实现计划、事故复盘、内部技术文档——这些场景信息密度高、读者更关注内容而非装饰。

特征：
- 无衬线字体通贯（Inter + PingFang SC）
- 纯白背景（`--color-bg-page`）
- 主色做节号和链接，其他地方都是灰度
- 不用渐变、不用背景色块
- 表格、callout 走简洁线性风格

这是本指南里所有组件示例的默认风格。

### 变体 B · Claude 杂志风

适合：调研报告、研究总结、观点文章、分享向读物——这些场景需要"一打开就觉得是认真做的交付物"，允许一些印刷级的排版趣味。

特征：
- **衬线字体做标题**：中文用 `"Source Han Serif SC", "Noto Serif SC", "Songti SC", serif`，英文用 `Charter, "Iowan Old Style", Georgia, serif`
- **米黄纸张底**：页面 `background: #faf7f0`，内容卡片 `background: #fffdf7` 或纯白
- **暖色强调**：主色改为暖棕/琥珀 `#c2410c` 或墨红 `#9f1239`
- **首字下沉**（Drop Cap）：首段第一个字放大 3 行高度
- **封面允许深色渐变 + 暖色光晕**
- **段落之间用更大的呼吸空间**

风格切换通过在 `:root` 里覆盖少量 token 实现，不用改整套 design-tokens：

```css
:root.magazine {
  --color-bg-page: #faf7f0;
  --color-bg-soft: #f5efe0;
  --color-bg-card: #fffdf7;
  --color-border-1: #e8dfca;
  --color-primary: #c2410c;
  --color-primary-hover: #9a3412;
  --color-primary-soft: #fed7aa;
  --font-sans: "Inter", -apple-system, "PingFang SC", sans-serif;
  --font-serif: "Source Han Serif SC", "Noto Serif SC", "Songti SC", Charter, "Iowan Old Style", Georgia, serif;
}
/* 标题用衬线 */
:root.magazine h1,
:root.magazine h2,
:root.magazine h3,
:root.magazine .article-title,
:root.magazine .quote-block p {
  font-family: var(--font-serif);
  letter-spacing: 0;
}
/* 首字下沉 */
:root.magazine section > p:first-of-type::first-letter {
  font-family: var(--font-serif);
  float: left;
  font-size: 3.6em;
  line-height: 1;
  margin: 0.08em 0.08em 0 0;
  color: var(--color-primary);
  font-weight: 700;
}
```

然后在 `<html class="magazine">` 上挂这个类即可。

选哪种？默认用 A。当内容具备以下**任何一条**时切换到 B：
- 用户希望"像一篇文章/研究/分享那样好看"
- 内容是面向更广受众（不只是内部同事）
- 用户明确说"杂志风/印刷感/文艺一点/Claude 风"

## 必备组件

### 1. 封面区（Cover）

位于文档最顶部，让读者一眼明白"这是一份什么文档"：

```html
<header class="article-cover">
  <div class="article-meta">
    <span class="article-type">调研报告</span>
    <span class="article-date">2026 · 05 · 10</span>
  </div>
  <h1 class="article-title">AI 代码评审工具市场调研</h1>
  <p class="article-subtitle">
    从 Cursor、Copilot、Windsurf 到 Claude Code——主流方案的能力边界与差异化机会
  </p>
  <div class="article-byline">
    <span>产品部 · 张三</span>
    <span aria-hidden="true">·</span>
    <span>阅读约 12 分钟</span>
  </div>
</header>
```

样式建议：

```css
.article-cover {
  padding: var(--space-16) 0 var(--space-12);
  border-bottom: 1px solid var(--color-border-1);
  margin-bottom: var(--space-12);
}
.article-type {
  display: inline-block;
  padding: 2px var(--space-2);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: var(--fs-xs);
  font-weight: var(--fw-medium);
  letter-spacing: 0.02em;
}
.article-title {
  margin: var(--space-4) 0 var(--space-3);
  font-size: var(--fs-4xl);
  font-weight: var(--fw-bold);
  line-height: var(--lh-tight);
  letter-spacing: -0.01em;
}
.article-subtitle {
  margin: 0 0 var(--space-6);
  font-size: var(--fs-xl);
  color: var(--color-text-2);
  line-height: var(--lh-normal);
  font-weight: var(--fw-regular);
}
.article-byline {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  color: var(--color-text-3);
  font-size: var(--fs-sm);
}
```

### 2. 目录（TOC）

超过 3 个小节就建议加目录。用纯 CSS + `<details>` 实现折叠：

```html
<details class="toc" open>
  <summary>目录</summary>
  <ol>
    <li><a href="#背景">1. 背景与问题</a></li>
    <li><a href="#现状">2. 现状分析</a></li>
    <li><a href="#方案">3. 可选方案对比</a></li>
    <li><a href="#建议">4. 建议与下一步</a></li>
  </ol>
</details>
```

```css
.toc {
  background: var(--color-bg-soft);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-6);
  margin: var(--space-10) 0;
}
.toc summary {
  font-weight: var(--fw-semibold);
  cursor: pointer;
  user-select: none;
  font-size: var(--fs-sm);
  color: var(--color-text-3);
  letter-spacing: 0.05em;
}
.toc ol {
  margin: var(--space-4) 0 0;
  padding-left: var(--space-6);
  color: var(--color-text-2);
}
.toc li { padding: var(--space-1) 0; }
```

### 3. 小节（Section）

用真正的 `<section>` + `<h2>`（不用 `<div class="section">`），便于下轮 AI 解析。标题上方留出 `--space-12` 的呼吸空间：

```html
<section id="现状">
  <h2>现状分析</h2>
  <p>当前市场上的 AI 编码工具...</p>
  <h3>细分赛道</h3>
  <p>...</p>
</section>
```

```css
h2 {
  margin: var(--space-12) 0 var(--space-4);
  font-size: var(--fs-3xl);
  font-weight: var(--fw-bold);
  line-height: var(--lh-tight);
  letter-spacing: -0.005em;
}
h3 {
  margin: var(--space-8) 0 var(--space-3);
  font-size: var(--fs-xl);
  font-weight: var(--fw-semibold);
}
p {
  margin: 0 0 var(--space-4);
  color: var(--color-text-1);
  line-height: var(--lh-relaxed);
}
```

### 4. 引用块（Callout / Quote）

用来强调关键观点、提醒坑点、引用原文。提供三种语气：

```html
<!-- 中性引用 -->
<blockquote class="callout">
  <p>这里是被引用的一段话或关键观点。</p>
</blockquote>

<!-- 提示 -->
<aside class="callout callout-info">
  <strong>提示</strong>
  <p>这里是需要读者额外注意的信息。</p>
</aside>

<!-- 警告 -->
<aside class="callout callout-warning">
  <strong>小心</strong>
  <p>这里是容易踩的坑。</p>
</aside>
```

```css
.callout {
  margin: var(--space-6) 0;
  padding: var(--space-4) var(--space-5);
  background: var(--color-bg-soft);
  border-left: 3px solid var(--color-border-1);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
}
.callout p:last-child { margin-bottom: 0; }
.callout-info {
  background: var(--color-info-soft);
  border-left-color: var(--color-info);
}
.callout-warning {
  background: var(--color-warning-soft);
  border-left-color: var(--color-warning);
}
```

### 5. 表格

长文里的表格常用于对比或列举。用真正的 `<table>`，不要用 div 拼：

```html
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>方案</th>
        <th>定价</th>
        <th>优势</th>
        <th>适用场景</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Cursor</td>
        <td>$20/月</td>
        <td>IDE 深度整合</td>
        <td>个人开发者</td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.table-wrapper {
  margin: var(--space-6) 0;
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--fs-sm);
  line-height: var(--lh-normal);
}
thead th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-weight: var(--fw-semibold);
  color: var(--color-text-2);
  background: var(--color-bg-soft);
  border-bottom: 2px solid var(--color-border-1);
}
tbody td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border-2);
  color: var(--color-text-1);
}
tbody tr:last-child td { border-bottom: none; }
```

### 6. 代码块

代码块用 `<pre><code>` 搭配等宽字体。不必集成 Prism/highlight.js 这种重库（也不在白名单）——素色代码已经足够清晰：

```html
<pre><code class="language-typescript">interface User {
  id: string;
  name: string;
}</code></pre>
```

```css
pre {
  margin: var(--space-5) 0;
  padding: var(--space-4) var(--space-5);
  background: var(--color-bg-muted);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-md);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: var(--fs-sm);
  line-height: var(--lh-normal);
  color: var(--color-text-1);
}
pre code { font-family: inherit; }
/* 行内代码 */
:not(pre) > code {
  padding: 2px 6px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--color-text-1);
}
```

### 7. 信息图 / 架构图 / 流程图 · 全套 SVG 组件

长文里最有价值的视觉元素不是装饰，而是**把"只能靠文字讲半天"的结构一眼表达出来**。本节提供四种常用信息图的骨架模板，按需选用、按需组合。

**原则**：
- 一律用**内联 SVG**（viewBox 定义画布，SVG 自适应容器宽度）
- 色值用 `--chart-1` 到 `--chart-8` 或 `--color-primary` / 文字色，不乱配
- 每张图配 `<figcaption>` 说明图意，方便下轮 AI 引用
- 复杂度控制在"看图两秒能懂"的水平，别把图当成第二份文档

**公共样式**（所有信息图的 figure 外壳都用这个）：

```css
figure.illustration {
  margin: var(--space-8) 0;
  padding: var(--space-5);
  background: var(--color-bg-soft);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-lg);
}
figure.illustration svg { width: 100%; height: auto; }
figcaption {
  margin-top: var(--space-3);
  text-align: center;
  font-size: var(--fs-sm);
  color: var(--color-text-3);
}
```

---

#### 7.1 流程图（横向步骤 / 纵向流程）

最常用的一种。表达"A → B → C"的线性过程，或"输入 → 处理 → 输出"的简单管线。

```html
<figure class="illustration" aria-label="三步流程">
  <svg viewBox="0 0 720 140" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arr1" viewBox="0 0 10 10" refX="9" refY="5"
              markerWidth="8" markerHeight="8" orient="auto">
        <path d="M0,0 L10,5 L0,10 Z" fill="#64748b"/>
      </marker>
    </defs>
    <!-- 步骤卡片 -->
    <g fill="#ffffff" stroke="#e2e8f0" stroke-width="1">
      <rect x="10"  y="40" width="180" height="60" rx="10"/>
      <rect x="270" y="40" width="180" height="60" rx="10"/>
      <rect x="530" y="40" width="180" height="60" rx="10"/>
    </g>
    <!-- 步骤文字 -->
    <g font-family="Inter, sans-serif" text-anchor="middle">
      <g font-size="11" fill="#64748b" letter-spacing="1">
        <text x="100" y="62">STEP 01</text>
        <text x="360" y="62">STEP 02</text>
        <text x="620" y="62">STEP 03</text>
      </g>
      <g font-size="14" fill="#0f172a" font-weight="600">
        <text x="100" y="85">输入任务产物</text>
        <text x="360" y="85">判断 archetype</text>
        <text x="620" y="85">生成 HTML</text>
      </g>
    </g>
    <!-- 连接箭头 -->
    <g stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#arr1)">
      <line x1="190" y1="70" x2="270" y2="70"/>
      <line x1="450" y1="70" x2="530" y2="70"/>
    </g>
  </svg>
  <figcaption>图 X. 三步工作流</figcaption>
</figure>
```

**变体**：
- **分支流程**：用 `<path d="M... L... L...">` 画折线，箭头分叉
- **纵向流程**：把 `viewBox` 改成窄高（`0 0 400 600`），卡片竖排
- **循环**：在末尾加一条曲线回到起点，可用 `<path d="M..Q..">` 画弧

---

#### 7.2 架构图（分层堆叠）

表达"表现层 / 业务层 / 数据层"这类分层结构。每层不同颜色底，层内放组件块。

```html
<figure class="illustration" aria-label="系统架构">
  <svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg">
    <!-- 分层背景 -->
    <g opacity="0.15">
      <rect x="0"  y="10"  width="720" height="80" fill="#2563eb"/>
      <rect x="0"  y="100" width="720" height="80" fill="#10b981"/>
      <rect x="0"  y="190" width="720" height="80" fill="#f59e0b"/>
    </g>
    <!-- 层标签 -->
    <g font-family="Inter" font-size="11" font-weight="600" letter-spacing="2" text-anchor="end">
      <text x="710" y="55"  fill="#1d4ed8">PRESENTATION</text>
      <text x="710" y="145" fill="#047857">BUSINESS</text>
      <text x="710" y="235" fill="#b45309">DATA</text>
    </g>
    <!-- 表现层组件 -->
    <g fill="#ffffff" stroke="#2563eb" stroke-width="1.5">
      <rect x="20"  y="30" width="130" height="40" rx="6"/>
      <rect x="170" y="30" width="130" height="40" rx="6"/>
      <rect x="320" y="30" width="130" height="40" rx="6"/>
    </g>
    <g font-family="Inter" font-size="13" fill="#1e3a8a" text-anchor="middle" font-weight="500">
      <text x="85"  y="55">Web 前端</text>
      <text x="235" y="55">小程序</text>
      <text x="385" y="55">Open API</text>
    </g>
    <!-- 业务层组件 -->
    <g fill="#ffffff" stroke="#10b981" stroke-width="1.5">
      <rect x="20"  y="120" width="210" height="40" rx="6"/>
      <rect x="250" y="120" width="210" height="40" rx="6"/>
      <rect x="480" y="120" width="210" height="40" rx="6"/>
    </g>
    <g font-family="Inter" font-size="13" fill="#065f46" text-anchor="middle" font-weight="500">
      <text x="125" y="145">订单服务</text>
      <text x="355" y="145">用户中心</text>
      <text x="585" y="145">支付网关</text>
    </g>
    <!-- 数据层组件 -->
    <g fill="#ffffff" stroke="#f59e0b" stroke-width="1.5">
      <rect x="20"  y="210" width="210" height="40" rx="6"/>
      <rect x="250" y="210" width="210" height="40" rx="6"/>
      <rect x="480" y="210" width="210" height="40" rx="6"/>
    </g>
    <g font-family="Inter" font-size="13" fill="#78350f" text-anchor="middle" font-weight="500">
      <text x="125" y="235">MySQL · 主库</text>
      <text x="355" y="235">Redis · 缓存</text>
      <text x="585" y="235">S3 · 对象存储</text>
    </g>
    <!-- 层间连接虚线 -->
    <g stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4" fill="none">
      <line x1="85"  y1="70" x2="125" y2="120"/>
      <line x1="235" y1="70" x2="355" y2="120"/>
      <line x1="355" y1="160" x2="355" y2="210"/>
    </g>
  </svg>
  <figcaption>图 X. 三层服务架构</figcaption>
</figure>
```

**关键思路**：用"淡色背景 + 同色边框"区分层，文字颜色用深色保证可读性。避免给每个组件框都填满实色——那会让整张图糊成一块。

---

#### 7.3 对比图（A vs B）

两个方案并列，中间用箭头或 "vs" 分隔。适合方案对比、改造前后。

```html
<figure class="illustration" aria-label="方案对比">
  <svg viewBox="0 0 720 260" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arrCompare" viewBox="0 0 10 10" refX="9" refY="5"
              markerWidth="10" markerHeight="10" orient="auto">
        <path d="M0,0 L10,5 L0,10 Z" fill="#c2410c"/>
      </marker>
    </defs>
    <!-- 左侧：旧方案 -->
    <rect x="10" y="20" width="310" height="220" rx="12"
          fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <text x="165" y="50" font-family="Inter" font-size="11" font-weight="600"
          fill="#64748b" text-anchor="middle" letter-spacing="2">BEFORE</text>
    <text x="165" y="80" font-family="Inter" font-size="18" font-weight="700"
          fill="#334155" text-anchor="middle">手动脚本</text>
    <g font-family="Inter" font-size="13" fill="#475569">
      <text x="40" y="120">• 15 天接入周期</text>
      <text x="40" y="145">• 每次都要重写</text>
      <text x="40" y="170">• 运维难度高</text>
      <text x="40" y="195">• 不可观测</text>
    </g>
    <!-- 中间箭头 -->
    <path d="M 335 130 L 385 130" stroke="#c2410c" stroke-width="3"
          fill="none" stroke-linecap="round" marker-end="url(#arrCompare)"/>
    <!-- 右侧：新方案 -->
    <rect x="400" y="20" width="310" height="220" rx="12"
          fill="#fffbeb" stroke="#fbbf24" stroke-width="1.5"/>
    <text x="555" y="50" font-family="Inter" font-size="11" font-weight="600"
          fill="#b45309" text-anchor="middle" letter-spacing="2">AFTER</text>
    <text x="555" y="80" font-family="Inter" font-size="18" font-weight="700"
          fill="#0f172a" text-anchor="middle">统一平台</text>
    <g font-family="Inter" font-size="13" fill="#334155">
      <text x="430" y="120">• 2 天接入周期</text>
      <text x="430" y="145">• 模板可复用</text>
      <text x="430" y="170">• 开箱即用</text>
      <text x="430" y="195">• 指标可观测</text>
    </g>
  </svg>
  <figcaption>图 X. 平台化改造前后对比</figcaption>
</figure>
```

---

#### 7.4 时间线（水平）

长文里嵌入时间线比海报的简洁——只需要点 + 日期 + 标题即可。如果要更强的视觉效果，参考 `archetype-poster.md` 的时间线组件。

```html
<figure class="illustration" aria-label="关键里程碑">
  <svg viewBox="0 0 720 140" xmlns="http://www.w3.org/2000/svg">
    <!-- 主线 -->
    <line x1="40" y1="70" x2="680" y2="70"
          stroke="#e2e8f0" stroke-width="2"/>
    <!-- 节点 -->
    <g>
      <circle cx="80"  cy="70" r="8" fill="#ffffff" stroke="#2563eb" stroke-width="2.5"/>
      <circle cx="240" cy="70" r="8" fill="#ffffff" stroke="#2563eb" stroke-width="2.5"/>
      <circle cx="400" cy="70" r="8" fill="#ffffff" stroke="#2563eb" stroke-width="2.5"/>
      <circle cx="560" cy="70" r="8" fill="#ffffff" stroke="#2563eb" stroke-width="2.5"/>
      <circle cx="660" cy="70" r="10" fill="#2563eb"/>
    </g>
    <!-- 日期 -->
    <g font-family="Inter" font-size="11" fill="#64748b" text-anchor="middle" letter-spacing="1">
      <text x="80"  y="40">2025.10</text>
      <text x="240" y="40">2025.12</text>
      <text x="400" y="40">2026.01</text>
      <text x="560" y="40">2026.03</text>
      <text x="660" y="40">2026.05</text>
    </g>
    <!-- 标题 -->
    <g font-family="Inter" font-size="13" fill="#0f172a" text-anchor="middle" font-weight="600">
      <text x="80"  y="105">立项</text>
      <text x="240" y="105">MVP</text>
      <text x="400" y="105">首批试点</text>
      <text x="560" y="105">全量推广</text>
      <text x="660" y="105">阶段复盘</text>
    </g>
  </svg>
  <figcaption>图 X. 项目关键节点</figcaption>
</figure>
```

---

#### 7.5 数据图（趋势 / 柱状 / 饼）

长文偶尔会嵌一张辅助数据图。**如果图表多到成为主体，考虑是不是应该换成仪表盘 archetype**。

简单数据图的 SVG 实现参考 `references/archetype-dashboard.md` 第 3 节，直接复用骨架、删掉图表卡片外壳即可。

---

#### 7.6 图片 / 占位图

需要真实图片（截图、照片）时不能远程引用——这破坏单文件原则。两个选择：

1. **Base64 内嵌**（适合 < 50KB 的小图）：
   ```html
   <img src="data:image/png;base64,iVBORw0KGgo..." alt="..." />
   ```
2. **SVG 占位图**（更推荐）：
   ```html
   <svg class="img-placeholder" viewBox="0 0 400 240"
        xmlns="http://www.w3.org/2000/svg"
        role="img" aria-label="图片占位：产品截图">
     <rect width="400" height="240" fill="#f1f5f9"/>
     <g stroke="#cbd5e1" stroke-width="2" fill="none">
       <line x1="0" y1="0" x2="400" y2="240"/>
       <line x1="400" y1="0" x2="0" y2="240"/>
     </g>
     <text x="200" y="125" font-family="Inter" font-size="13"
           fill="#64748b" text-anchor="middle">图片占位 · 产品截图</text>
   </svg>
   ```

大幅面的真实图片建议由用户补充，skill 不强行内嵌大 base64。

### 8. 页脚

给出生成元信息和可追溯信息：

```html
<footer class="article-footer">
  <p>本文档由 AI 根据 2026-05-10 的任务输入生成。如需修改，可将本 HTML 作为输入重新提交。</p>
  <dl>
    <dt>生成时间</dt><dd>2026-05-10</dd>
    <dt>数据版本</dt><dd>内部文档 v3.2</dd>
  </dl>
</footer>
```

## 变体

### 长文 + 侧栏目录（1080px 容器）

如果小节特别多（>8 个）或者读者需要频繁跳转，用两栏：主内容 760px + 左侧固定目录 240px。

```html
<div class="article-layout">
  <aside class="article-sidebar">
    <nav class="toc-sticky">...</nav>
  </aside>
  <main class="article-main">...</main>
</div>
```

```css
.article-layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 760px);
  gap: var(--space-12);
  max-width: 1080px;
  margin: 0 auto;
  padding: var(--space-10) var(--space-6);
}
.article-sidebar { position: sticky; top: var(--space-6); align-self: start; }
@media (max-width: 1024px) {
  .article-layout { grid-template-columns: 1fr; }
  .article-sidebar { display: none; }
}
```

### 带 diff/评审批注的长文

用于 PR 评审类产物。批注和 diff 并排：

```html
<div class="diff-block">
  <div class="diff-side">
    <pre><code>- const foo = bar;
+ const foo = bar ?? baz;</code></pre>
  </div>
  <aside class="diff-note" data-severity="warning">
    <strong>建议</strong>
    <p>这里用 nullish 合并比 || 更安全，避免 0 和空字符串被跳过。</p>
  </aside>
</div>
```

## 常见失误

- **标题跳级**：`<h1>` 下直接出 `<h3>`。要按 h1 → h2 → h3 逐级用，搜索引擎、辅助阅读器、下轮 AI 都会按层级理解内容。
- **插图只贴图片没标题**：`<figure>` 一定配 `<figcaption>`，让图能被独立引用。
- **表格滥用居中对齐**：文字列一律左对齐，数字列右对齐，只有极少数情况需要居中（比如状态图标）。
- **代码块超宽撑破页面**：`<pre>` 要加 `overflow-x: auto`，容器要允许横向滚动。
- **段落太长没有分段**：中文每段控制在 3-5 句以内，长段落拆开，读者视线才不会疲惫。
