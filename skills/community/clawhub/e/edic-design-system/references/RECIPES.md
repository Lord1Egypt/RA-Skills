# EDIC Scene Recipes
# 场景配方：从零搭建完整页面

> Load this file when the user asks to build a complete page or layout from scratch.
> Each recipe lists the exact sequence of sections, which Pattern to use for each,
> and the key decisions to make before writing any code.

---

## Recipe 1 — Documentation / Technical Guide Page

**Target:** `docs.html` style — sidebar nav + scrollable prose content.
**Live reference:** https://edic.cgartlab.com/docs.html

### Step 1 — Shell (Navbar + two-column docs layout)

```html
<!doctype html>
<html lang="zh-CN" data-theme="">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文档标题 — EDIC</title>
  <link rel="stylesheet" href="styles.css">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
</head>
<body>
  <a href="#ds-main" class="ds-skip">跳到主内容</a>

  <!-- Navbar (see EXAMPLES.md #3 for full structure) -->
  <nav class="ds-navbar" role="navigation" aria-label="主导航">
    <div class="ds-navbar-inner">
      <a href="/" class="ds-navbar-brand">EDIC</a>
      <div class="ds-navbar-links" id="mnav-panel">
        <a href="docs.html" class="ds-navbar-link ds-navbar-link--active" aria-current="page">文档</a>
      </div>
      <div class="ds-navbar-actions">
        <button class="ds-theme-toggle-btn" aria-label="切换主题"></button>
      </div>
    </div>
  </nav>

  <!-- Docs shell (see EXAMPLES.md #2) -->
  <div class="ds-docs">
    <aside class="ds-docs-aside">
      <!-- Sidebar nav goes here (Step 2) -->
    </aside>
    <main class="ds-docs-main ds-prose" id="ds-main">
      <!-- Article content goes here (Step 3) -->
    </main>
  </div>

  <script src="scripts.js"></script>
</body>
</html>
```

### Step 2 — Sidebar (`ds-pagenav`)

```html
<nav class="ds-pagenav" aria-label="章节导航">
  <details class="ds-pagenav-disclosure" open>
    <summary class="ds-pagenav-summary">
      <span class="ds-pagenav-chevron">▶</span> 快速开始
    </summary>
    <ol class="ds-pagenav-list">
      <li>
        <a href="#install" class="ds-pagenav-link ds-pagenav-link--active">
          <span class="ds-pagenav-num">01</span>
          <span class="ds-pagenav-text">安装</span>
        </a>
      </li>
      <li>
        <a href="#tokens" class="ds-pagenav-link">
          <span class="ds-pagenav-num">02</span>
          <span class="ds-pagenav-text">设计令牌</span>
        </a>
      </li>
    </ol>
  </details>
  <details class="ds-pagenav-disclosure">
    <summary class="ds-pagenav-summary">
      <span class="ds-pagenav-chevron">▶</span> 组件
    </summary>
    <ol class="ds-pagenav-list">
      <li>
        <a href="#buttons" class="ds-pagenav-link">
          <span class="ds-pagenav-num">01</span>
          <span class="ds-pagenav-text">按钮</span>
        </a>
      </li>
    </ol>
  </details>
</nav>
```

### Step 3 — Article body (`ds-prose`)

Use **Pattern 6** (Article / Long-Form Prose) from `PATTERNS.md`.
Key rules:
- One `<h1>` at the top of the page. Use `<h2>` for sections, `<h3>` for sub-sections.
- Wrap code samples in `<div class="ds-code"><div class="ds-code-bar">...</div><pre><code>...</code></pre></div>`.
- Use `<div class="ds-alert ds-alert--info">` for callout boxes.

---


## Recipe 2 — Company / Brand Landing Page

**Target:** `company.html` style — hero → features → stats → CTA → footer.
**Live reference:** https://edic.cgartlab.com/company.html

### Section order

```
<Navbar>
<Hero>           ← Pattern 1
<Feature Grid>   ← Pattern 2
<Stats Bar>      ← Pattern 4
<CTA Section>    ← see below
<Footer>         ← ds-footer-rich
```

### CTA Section

```html
<section class="ds-section ds-section--alt">
  <div class="ds-wrapper" style="text-align:center">
    <h2 class="ds-cta-h2 ds-mb-5 ds-text-balance">准备好开始了吗？</h2>
    <p class="ds-lead ds-text-muted ds-mb-8">
      免费使用，CC BY 4.0 许可。
    </p>
    <div class="ds-cta-actions ds-mb-0">
      <a href="/downloads.html" class="ds-btn ds-btn--primary ds-btn--lg">立即下载</a>
      <a href="/docs.html" class="ds-btn ds-btn--secondary ds-btn--lg">查看文档</a>
    </div>
  </div>
</section>
```

### Footer (`ds-footer-rich`)

```html
<footer class="ds-footer-rich">
  <div class="ds-wrapper">
    <div class="ds-footer-cols">
      <div class="ds-footer-brand">
        <span class="ds-logo">EDIC</span>
        <p class="ds-caption ds-text-muted ds-mt-3">
          为内容而生的编辑主义设计系统。
        </p>
      </div>
      <div>
        <h3 class="ds-footer-col-heading">资源</h3>
        <ul class="ds-footer-links">
          <li><a href="/docs.html">文档</a></li>
          <li><a href="/downloads.html">下载</a></li>
        </ul>
      </div>
      <div>
        <h3 class="ds-footer-col-heading">社区</h3>
        <ul class="ds-footer-links">
          <li><a href="https://github.com/cgartlab/edic-design-system" target="_blank" rel="noopener">GitHub</a></li>
        </ul>
      </div>
    </div>
    <div class="ds-footer-bottom">
      <span class="ds-caption ds-text-muted">© 2026 EDIC · CC BY 4.0</span>
    </div>
  </div>
</footer>
```

### Key decisions
- Keep hero headline ≤ 12 Chinese characters per line; use `ds-text-balance`.
- Section alternation: `ds-section` (paper bg) → `ds-section--alt` (surface bg) → repeat.
- All section-level animations use `ds-reveal` with staggered `--d` values.

---


## Recipe 3 — Blog / Article Page

**Target:** `blog.html` style — navbar + article header + TOC + prose body + footer.
**Live reference:** https://edic.cgartlab.com/blog.html

### Section order

```
<Navbar>
<Article header>   ← eyebrow + h1 + lead + meta
<TOC (optional)>   ← ds-toc-article (sticky, desktop only)
<Article body>     ← Pattern 6 (ds-prose)
<Related posts>    ← 2-col ds-grid-2 of ds-card--hoverable
<Footer>
```

### Article header

```html
<header class="ds-wrapper ds-mb-10">
  <span class="ds-eyebrow ds-block ds-mb-4">设计系统</span>
  <h1 class="ds-h1 ds-text-balance">文章标题，建议不超过 20 字</h1>
  <p class="ds-lead ds-text-muted ds-mt-4 ds-text-pretty">
    副标题或摘要，一两句话点明文章核心观点。
  </p>
  <div class="ds-cluster ds-mt-6" style="gap:var(--ds-space-4); align-items:center">
    <div class="ds-avatar ds-avatar--sm" aria-hidden="true">作</div>
    <div>
      <span class="ds-meta">作者名</span>
      <time class="ds-caption ds-text-muted ds-block">2026-06-26</time>
    </div>
    <span class="ds-badge ds-badge--default">8 分钟阅读</span>
  </div>
</header>
```

### TOC (desktop, sticky aside)

```html
<!-- Wrap article + TOC in a grid -->
<div class="ds-wrapper" style="display:grid; grid-template-columns:1fr 240px; gap:var(--ds-space-16); align-items:start;">
  <article class="ds-prose" id="ds-main">
    <!-- Pattern 6 content here -->
  </article>

  <aside style="position:sticky; top:calc(var(--ds-space-16) + var(--ds-space-8))">
    <nav class="ds-toc-article" aria-label="本文目录">
      <span class="ds-toc-article-title ds-caption">本文目录</span>
      <ol class="ds-toc-list">
        <li><a href="#section-1" class="ds-toc-link ds-toc-link--active">第一节</a></li>
        <li><a href="#section-2" class="ds-toc-link">第二节</a></li>
        <li><a href="#section-3" class="ds-toc-link ds-toc-link--h3">2.1 子节</a></li>
      </ol>
    </nav>
  </aside>
</div>
```

### Key decisions
- TOC is hidden on mobile via `ds-toc-article` responsive rules. No manual media query needed.
- Article `<h2>` and `<h3>` must have `id` attributes for TOC anchor links to work.
- Use `ds-text-indent` class on `<p>` elements inside `ds-prose` for CJK first-line indent.

---


## Recipe 4 — Printable Résumé / CV (A4)

**Target:** `resume.html` style — single-page A4, print-ready, timeline + skills.
**Live reference:** https://edic.cgartlab.com/resume.html

### Section order

```
<Header>     ← name + title + contact info
<Summary>    ← ds-lead paragraph
<Experience> ← ds-timeline
<Skills>     ← ds-grid-2 with ds-badge clusters
<Education>  ← compact ds-timeline
```

### Full skeleton

```html
<!doctype html>
<html lang="zh-CN" data-theme="">
<head>
  <meta charset="UTF-8">
  <title>张三 — 简历</title>
  <link rel="stylesheet" href="styles.css">
  <style>
    @media print {
      .ds-navbar, .ds-theme-toggle-btn { display: none !important; }
      body { background: white; }
      @page { size: A4; margin: 20mm; }
    }
  </style>
</head>
<body>
  <main class="ds-wrapper ds-prose" id="ds-main"
        style="max-width:800px; padding-top:var(--ds-space-12)">

    <!-- Header -->
    <header style="border-bottom:2px solid var(--ds-accent); padding-bottom:var(--ds-space-6); margin-bottom:var(--ds-space-8)">
      <h1 class="ds-h1" style="margin:0">张三</h1>
      <p class="ds-lead ds-text-muted ds-mt-2">高级前端工程师 · 设计系统专家</p>
      <div class="ds-cluster ds-mt-4" style="gap:var(--ds-space-6)">
        <span class="ds-caption">zhang@example.com</span>
        <span class="ds-caption">+86 138 0000 0000</span>
        <a href="https://github.com/zhangsan" class="ds-caption ds-text-accent">github.com/zhangsan</a>
      </div>
    </header>

    <!-- Summary -->
    <section class="ds-mb-8">
      <h2 class="ds-h4 ds-text-accent" style="text-transform:uppercase; letter-spacing:var(--ds-tracking-wider)">简介</h2>
      <p class="ds-mt-2">5 年前端开发经验，专注设计系统与组件库建设……</p>
    </section>

    <!-- Experience (ds-timeline) -->
    <section class="ds-mb-8">
      <h2 class="ds-h4 ds-text-accent" style="text-transform:uppercase; letter-spacing:var(--ds-tracking-wider)">工作经历</h2>
      <div class="ds-timeline ds-mt-4">
        <div class="ds-timeline-item">
          <div class="ds-timeline-dot" aria-hidden="true"></div>
          <div class="ds-timeline-content">
            <time class="ds-timeline-date ds-caption">2023 — 至今</time>
            <h3 class="ds-timeline-title">高级前端工程师</h3>
            <p class="ds-text-muted ds-caption">某科技公司 · 上海</p>
            <ul class="ds-mt-2" style="padding-left:var(--ds-space-5)">
              <li>主导设计系统从零到一的建设……</li>
              <li>将组件复用率提升至 80%……</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Skills -->
    <section class="ds-mb-8">
      <h2 class="ds-h4 ds-text-accent" style="text-transform:uppercase; letter-spacing:var(--ds-tracking-wider)">技能</h2>
      <div class="ds-grid-2 ds-mt-4" style="gap:var(--ds-space-4)">
        <div>
          <span class="ds-caption ds-text-muted ds-block ds-mb-2">前端</span>
          <div class="ds-cluster" style="flex-wrap:wrap; gap:var(--ds-space-2)">
            <span class="ds-badge ds-badge--default">React</span>
            <span class="ds-badge ds-badge--default">TypeScript</span>
            <span class="ds-badge ds-badge--default">CSS / OKLch</span>
          </div>
        </div>
        <div>
          <span class="ds-caption ds-text-muted ds-block ds-mb-2">工具</span>
          <div class="ds-cluster" style="flex-wrap:wrap; gap:var(--ds-space-2)">
            <span class="ds-badge ds-badge--default">Figma</span>
            <span class="ds-badge ds-badge--default">Git</span>
          </div>
        </div>
      </div>
    </section>

  </main>
  <script src="scripts.js"></script>
</body>
</html>
```

### Key decisions
- `@page { size: A4; margin: 20mm; }` is essential for correct print output.
- Hide navbar and theme toggle in print CSS.
- Use `ds-timeline` for both experience and education — consistent visual rhythm.
- Section headings use `ds-text-accent` + `letter-spacing` to create subtle editorial dividers.

---


## Recipe 5 — Multi-Page Report / White Paper

**Target:** `report.html` style — paginated long-form document with sidebar navigation.
**Live reference:** https://edic.cgartlab.com/report.html

### Section order

```
<Navbar>
<Report cover>    ← full-width ds-cover with title + subtitle + date
<ds-docs shell>   ← sidebar (chapter list) + main content
  <Chapter 1>     ← h1 + ds-prose content
  <Chapter 2>
  ...
<Back to top>
```

### Cover page

```html
<section class="ds-cover" style="min-height:60vh; display:flex; flex-direction:column;
                                   justify-content:center; align-items:flex-start;
                                   padding:var(--ds-space-20) var(--ds-space-8)">
  <span class="ds-eyebrow ds-block ds-mb-4">年度报告 · 2026</span>
  <h1 style="font-family:var(--ds-font-display); font-size:var(--ds-text-display);
              font-weight:700; line-height:var(--ds-leading-tight);
              color:var(--ds-color-fg-strong); max-width:16ch">
    EDIC 设计系统<br>年度总结
  </h1>
  <p class="ds-lead ds-text-muted ds-mt-6" style="max-width:50ch">
    回顾 2026 年的核心进展、数据指标与未来展望。
  </p>
  <div class="ds-cluster ds-mt-8" style="gap:var(--ds-space-6)">
    <time class="ds-caption ds-text-muted">发布日期：2026-06-26</time>
    <span class="ds-caption ds-text-muted">作者：EDIC 团队</span>
  </div>
</section>
```

### Chapter structure inside `ds-docs-main`

```html
<main class="ds-docs-main ds-prose" id="ds-main">
  <!-- Chapter 1 -->
  <section id="ch-1">
    <h1>第一章：项目概览</h1>
    <p>章节正文……</p>

    <!-- Data table -->
    <div class="ds-table-wrap">
      <table class="ds-table">
        <caption class="ds-caption ds-text-muted">表 1 · 版本发布统计</caption>
        <thead>
          <tr><th>版本</th><th>发布日期</th><th>组件数</th></tr>
        </thead>
        <tbody>
          <tr><td>v1.9</td><td>2026-06</td><td>25</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Highlight box -->
    <div class="ds-alert ds-alert--info ds-mt-6">
      <span class="ds-alert-title">关键发现</span>
      <p>AI 驱动的 Skill 集成使开发效率提升了 40%。</p>
    </div>
  </section>

  <!-- Chapter 2 -->
  <section id="ch-2" class="ds-mt-16">
    <h1>第二章：数据与指标</h1>
    <!-- Use Pattern 9 (Dashboard) for data visualizations -->
  </section>
</main>
```

### Key decisions
- Each chapter gets its own `<section id="ch-N">` for sidebar anchor linking.
- `ds-pagenav` sidebar chapter list: use `ds-pagenav-num` to show chapter numbers.
- For printed reports, add `@media print` CSS to force page breaks between chapters:
  `section { page-break-before: always; }`.
- Tables must use `ds-table-wrap` for horizontal scroll on narrow screens.

---


---

## Quick Decision Guide

When the user describes a goal, use this table to pick the right recipe:

| User says… | Use recipe | Key patterns |
|------------|-----------|--------------|
| "帮我做一个官网 / 落地页" | Recipe 2 | Hero + Feature Grid + Stats + CTA + Footer |
| "帮我做一个博客 / 文章页" | Recipe 3 | Article Header + TOC + Prose (Pattern 6) |
| "帮我做一个文档站 / 技术指南" | Recipe 1 | Docs shell + Sidebar nav + Prose |
| "帮我做一个简历 / 个人主页" | Recipe 4 | Header + Timeline + Skills grid |
| "帮我做一个报告 / 白皮书" | Recipe 5 | Cover + Docs shell + Tables + Alerts |
| "帮我做一个价格页 / 定价表" | Pattern 7 | Pricing Table (standalone) |
| "帮我做一个联系表单 / 注册页" | Pattern 5 | Contact Form (standalone) |
| "帮我做一个邮件模板" | Pattern 10 | HTML Email (inline styles only) |
| "帮我做一个仪表板 / 后台" | Pattern 9 | Dashboard (standalone) |

> If the request spans multiple pages, build each page using its recipe, then link them with a shared `ds-navbar` and `ds-footer-rich`.
