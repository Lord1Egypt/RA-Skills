# EDIC Page-Level Patterns
# 页面级组合模式

> Load this file when building full sections or complete pages.
> Each pattern shows the complete HTML skeleton with correct nesting order,
> semantic landmarks, and which tokens/components to use.

---

## Pattern 1 — Hero Section

Use for: homepage above-the-fold, landing page opener.
Stack: eyebrow → headline → lead → actions. Background blobs are decorative.

```html
<section class="ds-hero-section">
  <!-- Decorative background blobs (aria-hidden) -->
  <div class="ds-bg-blob ds-bg-blob--1" aria-hidden="true"></div>
  <div class="ds-bg-blob ds-bg-blob--2" aria-hidden="true"></div>

  <div class="ds-hero-inner ds-wrapper">
    <!-- Eyebrow label -->
    <span class="ds-eyebrow ds-block ds-mb-4 ds-reveal">v1.9 · 现已发布</span>

    <!-- Headline: display font, tight leading, balanced wrap -->
    <h1 class="ds-hero-title ds-reveal ds-text-balance">
      为内容而生的<br>编辑主义设计系统
    </h1>

    <!-- Lead paragraph: constrained measure, pretty wrap -->
    <p class="ds-lead ds-mb-10 ds-text-pretty ds-mx-auto ds-reveal">
      OKLch 色彩科学 · 318 条结构化令牌 · 无运行时依赖
    </p>

    <!-- CTA row -->
    <div class="ds-hero-actions ds-reveal">
      <a href="/docs.html" class="ds-btn ds-btn--primary ds-btn--lg">开始使用</a>
      <a href="/downloads.html" class="ds-btn ds-btn--secondary ds-btn--lg">下载资源</a>
    </div>
  </div>
</section>
```


---

## Pattern 2 — Feature Grid Section

Use for: homepage feature list, product overview, "why choose" sections.
3-column grid of icon + title + description cards, stagger-revealed.

```html
<section class="ds-section">
  <div class="ds-wrapper">
    <div class="ds-section-head ds-section-head--center ds-reveal">
      <span class="ds-eyebrow">核心特性</span>
      <h2 class="ds-h2 ds-text-balance">专为内容而设计</h2>
      <p class="ds-lead ds-text-muted">每一个令牌都经过精心调校。</p>
    </div>

    <div class="ds-feature-grid">
      <article class="ds-feature-card ds-reveal" style="--d:.05s">
        <div class="ds-feature-ico" aria-hidden="true">
          <!-- 24×24 SVG icon -->
        </div>
        <h3>OKLch 色彩</h3>
        <p class="ds-text-muted">感知均匀，暗色模式自适配，无需猜测。</p>
      </article>

      <article class="ds-feature-card ds-reveal" style="--d:.1s">
        <div class="ds-feature-ico" aria-hidden="true"><!-- icon --></div>
        <h3>无运行时依赖</h3>
        <p class="ds-text-muted">纯 CSS + JS，React、Vue 与打印可直接使用；邮件按兼容样式适配。</p>
      </article>

      <article class="ds-feature-card ds-reveal" style="--d:.15s">
        <div class="ds-feature-ico" aria-hidden="true"><!-- icon --></div>
        <h3>AI 就绪</h3>
        <p class="ds-text-muted">Skill 包让 AI 直接产出规范输出。</p>
      </article>
    </div>
  </div>
</section>
```


---

## Pattern 3 — Blog / Article Card Feed

Use for: blog index, news list, article collection pages.
Cards in a 2-col or 3-col grid. Each card: badge + title + excerpt + meta + CTA.

```html
<section class="ds-section">
  <div class="ds-wrapper">
    <h2 class="ds-h2 ds-mb-8">最新文章</h2>

    <div class="ds-grid-3">
      <article class="ds-card ds-card--hoverable ds-reveal" style="--d:.05s">
        <header>
          <span class="ds-badge ds-badge--accent">设计</span>
          <h3 class="ds-serif ds-mt-3">
            <a href="/blog/article.html" class="ds-text-accent">
              OKLch 色彩科学入门
            </a>
          </h3>
        </header>
        <p class="ds-text-muted ds-mt-2">
          了解感知均匀色彩空间如何让设计决策更可靠。
        </p>
        <footer class="ds-cluster ds-mt-4" style="justify-content:space-between;align-items:center;">
          <span class="ds-caption ds-text-muted">2026-06-01</span>
          <a href="/blog/article.html" class="ds-btn ds-btn--ghost ds-btn--sm">阅读全文</a>
        </footer>
      </article>

      <!-- Repeat for additional cards -->
    </div>
  </div>
</section>
```

**Token notes:**
- Card hover lift uses `--ds-shadow-md` + `translateY(-2px)` — built into `ds-card--hoverable`.
- Eyebrow date: `ds-caption` (0.75rem, uppercase, wide tracking).
- Keep excerpt ≤ 3 lines; use `ds-text-pretty` to avoid orphaned words.


---

## Pattern 4 — Stats / Social Proof Bar

Use for: trust section, metrics showcase, "by the numbers" row.

```html
<section class="ds-section ds-section--alt">
  <div class="ds-wrapper">
    <div class="ds-stat-grid">
      <div class="ds-stat ds-reveal" style="--d:.0s">
        <span class="ds-stat-num">318</span>
        <span class="ds-stat-label">结构化令牌</span>
      </div>
      <div class="ds-stat ds-reveal" style="--d:.08s">
        <span class="ds-stat-num">39</span>
        <span class="ds-stat-label">核心组件</span>
      </div>
      <div class="ds-stat ds-reveal" style="--d:.16s">
        <span class="ds-stat-num">209</span>
        <span class="ds-stat-label">SVG 图标</span>
      </div>
      <div class="ds-stat ds-reveal" style="--d:.24s">
        <span class="ds-stat-num">0</span>
        <span class="ds-stat-label">运行时依赖</span>
      </div>
    </div>
  </div>
</section>
```

**Token notes:**
- `ds-section--alt` uses `--ds-color-surface` background to create visual rhythm.
- `ds-stat-num` uses display font, `--ds-text-display` (3.75rem), olive accent color.
- Stagger delay `--d` increments ≈ 0.08s per item.


---

## Pattern 5 — Contact / Lead-Capture Form

Use for: contact page, newsletter signup, request demo.

```html
<section class="ds-section">
  <div class="ds-wrapper">
    <div class="ds-grid-2 ds-items-center ds-gap-16">

      <!-- Left: copy -->
      <div class="ds-reveal">
        <span class="ds-eyebrow">联系我们</span>
        <h2 class="ds-h2 ds-mt-2">让我们来聊聊</h2>
        <p class="ds-lead ds-text-muted ds-mt-3">
          无论是合作还是咨询，我们都很乐意回复。
        </p>
      </div>

      <!-- Right: form -->
      <form class="ds-stack ds-reveal" style="--d:.1s" novalidate>
        <div class="ds-form-group">
          <label class="ds-form-label" for="name">
            姓名 <span class="ds-form-required" aria-hidden="true">*</span>
          </label>
          <input class="ds-form-input" id="name" name="name"
                 type="text" autocomplete="name" required>
        </div>

        <div class="ds-form-group">
          <label class="ds-form-label" for="email">
            邮箱 <span class="ds-form-required" aria-hidden="true">*</span>
          </label>
          <input class="ds-form-input" id="email" name="email"
                 type="email" autocomplete="email" required>
        </div>

        <div class="ds-form-group">
          <label class="ds-form-label" for="message">留言</label>
          <textarea class="ds-form-textarea" id="message" name="message"
                    rows="4"></textarea>
        </div>

        <button class="ds-form-submit ds-btn ds-btn--primary" type="submit">
          发送消息
        </button>
      </form>

    </div>
  </div>
</section>
```


---

## Pattern 6 — Article / Long-Form Prose

Use for: blog post body, documentation page, essay, tutorial.

```html
<article class="ds-wrapper ds-prose" id="ds-main">
  <!-- Article header -->
  <header class="ds-mb-10">
    <span class="ds-eyebrow">设计系统</span>
    <h1 class="ds-h1 ds-mt-3 ds-text-balance">理解 OKLch 色彩空间</h1>
    <p class="ds-lead ds-text-muted ds-mt-4">
      一篇关于感知均匀色彩的深度指南。
    </p>
    <div class="ds-cluster ds-mt-6" style="gap:var(--ds-space-4)">
      <span class="ds-caption ds-text-muted">2026-06-01</span>
      <span class="ds-badge ds-badge--default">10 分钟阅读</span>
    </div>
  </header>

  <!-- Body: ds-prose handles paragraph, heading, list, code spacing -->
  <p>正文段落。<code>ds-prose</code> 自动控制行宽（65–75 字符），
  调整 h2/h3 间距，处理 CJK 标点。</p>

  <h2>第一节标题</h2>
  <p>段落内容……</p>

  <blockquote class="ds-quote-cjk">
    <p>引用内容，使用 CJK 引用样式。</p>
  </blockquote>

  <pre><code class="ds-code language-css">
.example { color: var(--ds-accent); }
  </code></pre>

  <!-- Article footer -->
  <footer class="ds-mt-16 ds-pt-8" style="border-top:1px solid var(--ds-color-border)">
    <a href="/blog.html" class="ds-btn ds-btn--ghost">← 返回博客</a>
  </footer>
</article>
```

**Token notes:**
- `ds-prose` must wrap the entire article body. Do **not** nest `ds-wrapper` inside `ds-prose`.
- Heading order: one `h1` per article, then `h2` → `h3`. Never skip levels.
- `ds-text-indent` adds first-line indent for CJK paragraphs.


---

## Pattern 7 — Pricing / Comparison Table

Use for: pricing tiers, feature comparison, plan selection.

```html
<section class="ds-section">
  <div class="ds-wrapper">
    <div class="ds-section-head ds-section-head--center ds-mb-10">
      <h2 class="ds-h2">选择方案</h2>
    </div>

    <div class="ds-grid-3">
      <!-- Free tier -->
      <div class="ds-card ds-reveal" style="--d:.0s">
        <span class="ds-eyebrow">免费</span>
        <div class="ds-mt-3">
          <span class="ds-display" style="font-size:var(--ds-text-h1)">¥0</span>
          <span class="ds-text-muted">/月</span>
        </div>
        <ul class="ds-stack ds-mt-4" style="list-style:none;padding:0;--stack-gap:var(--ds-space-3)">
          <li class="ds-text-muted">✓ 核心组件</li>
          <li class="ds-text-muted">✓ 基础令牌</li>
          <li class="ds-text-muted" style="opacity:.4">✗ 优先支持</li>
        </ul>
        <a href="#" class="ds-btn ds-btn--secondary ds-mt-6" style="width:100%;justify-content:center">
          立即开始
        </a>
      </div>

      <!-- Pro tier (highlighted) -->
      <div class="ds-card ds-reveal"
           style="--d:.08s; border-color:var(--ds-accent); box-shadow:var(--ds-shadow-lg)">
        <div class="ds-cluster" style="justify-content:space-between">
          <span class="ds-eyebrow">专业版</span>
          <span class="ds-badge ds-badge--accent">推荐</span>
        </div>
        <div class="ds-mt-3">
          <span class="ds-display" style="font-size:var(--ds-text-h1)">¥99</span>
          <span class="ds-text-muted">/月</span>
        </div>
        <ul class="ds-stack ds-mt-4" style="list-style:none;padding:0;--stack-gap:var(--ds-space-3)">
          <li>✓ 核心组件家族</li>
          <li>✓ 设计文件</li>
          <li>✓ 优先支持</li>
        </ul>
        <a href="#" class="ds-btn ds-btn--primary ds-mt-6" style="width:100%;justify-content:center">
          升级专业版
        </a>
      </div>

      <!-- Enterprise tier -->
      <div class="ds-card ds-reveal" style="--d:.16s">
        <span class="ds-eyebrow">企业版</span>
        <div class="ds-mt-3">
          <span class="ds-h2">联系我们</span>
        </div>
        <ul class="ds-stack ds-mt-4" style="list-style:none;padding:0;--stack-gap:var(--ds-space-3)">
          <li>✓ 定制开发</li>
          <li>✓ 私有部署</li>
          <li>✓ 专属支持</li>
        </ul>
        <a href="#contact" class="ds-btn ds-btn--ghost ds-mt-6" style="width:100%;justify-content:center">
          联系销售
        </a>
      </div>
    </div>
  </div>
</section>
```


---

## Pattern 8 — Timeline / History Section

Use for: company history, product roadmap, personal career timeline, changelog.

```html
<section class="ds-section">
  <div class="ds-wrapper">
    <h2 class="ds-h2 ds-mb-10">发展历程</h2>

    <div class="ds-timeline">
      <div class="ds-timeline-item ds-reveal" style="--d:.0s">
        <div class="ds-timeline-dot" aria-hidden="true"></div>
        <div class="ds-timeline-content">
          <time class="ds-timeline-date ds-caption">2024 · Q1</time>
          <h3 class="ds-timeline-title">项目启动</h3>
          <p class="ds-text-muted">确立 OKLch 色彩体系与令牌架构。</p>
          <span class="ds-timeline-tag ds-badge ds-badge--default">里程碑</span>
        </div>
      </div>

      <div class="ds-timeline-item ds-reveal" style="--d:.1s">
        <div class="ds-timeline-dot" aria-hidden="true"></div>
        <div class="ds-timeline-content">
          <time class="ds-timeline-date ds-caption">2024 · Q3</time>
          <h3 class="ds-timeline-title">v1.0 发布</h3>
          <p class="ds-text-muted">44 个核心组件家族，暗色令牌覆盖。</p>
          <span class="ds-timeline-tag ds-badge ds-badge--accent">发布</span>
        </div>
      </div>

      <div class="ds-timeline-item ds-reveal" style="--d:.2s">
        <div class="ds-timeline-dot" aria-hidden="true"></div>
        <div class="ds-timeline-content">
          <time class="ds-timeline-date ds-caption">2026 · 现在</time>
          <h3 class="ds-timeline-title">AI Skill 集成</h3>
          <p class="ds-text-muted">Claude Code Skill 包，让 AI 原生理解设计规范。</p>
          <span class="ds-timeline-tag ds-badge ds-badge--success">进行中</span>
        </div>
      </div>
    </div>
  </div>
</section>
```


---

## Pattern 9 — Dashboard / Data Panel

Use for: admin panel summary, analytics overview, monitoring dashboard.

```html
<div class="ds-wrapper">
  <!-- Top stat row -->
  <div class="ds-grid-4 ds-mb-8">
    <div class="ds-card">
      <span class="ds-caption ds-text-muted">总用户</span>
      <div class="ds-h2 ds-mt-2" style="color:var(--ds-accent)">12,480</div>
      <span class="ds-caption" style="color:var(--ds-color-success)">↑ 8.2% 本月</span>
    </div>
    <div class="ds-card">
      <span class="ds-caption ds-text-muted">活跃项目</span>
      <div class="ds-h2 ds-mt-2">342</div>
      <span class="ds-caption ds-text-muted">较上月持平</span>
    </div>
    <div class="ds-card">
      <span class="ds-caption ds-text-muted">待处理</span>
      <div class="ds-h2 ds-mt-2" style="color:var(--ds-color-warning)">17</div>
      <span class="ds-badge ds-badge--warning ds-mt-2">需关注</span>
    </div>
    <div class="ds-card">
      <span class="ds-caption ds-text-muted">完成率</span>
      <div class="ds-h2 ds-mt-2">94%</div>
      <div class="ds-progress ds-mt-3">
        <div class="ds-progress-bar">
          <div class="ds-progress-fill" style="width:94%"
               role="progressbar" aria-valuenow="94" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- Main content + sidebar -->
  <div class="ds-grid-2 ds-gap-16" style="grid-template-columns:1fr 320px">
    <!-- Main table panel -->
    <div class="ds-card">
      <div class="ds-cluster ds-mb-4" style="justify-content:space-between">
        <h2 class="ds-h4">最近活动</h2>
        <button class="ds-btn ds-btn--ghost ds-btn--sm">查看全部</button>
      </div>
      <div class="ds-table-wrap">
        <table class="ds-table">
          <thead>
            <tr><th>项目</th><th>状态</th><th>更新时间</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>EDIC v2.0</td>
              <td><span class="ds-badge ds-badge--success">进行中</span></td>
              <td class="ds-text-muted ds-caption">2 小时前</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Sidebar alerts -->
    <div class="ds-stack">
      <div class="ds-alert ds-alert--info">
        <span class="ds-alert-title">系统更新</span>
        <p>定时维护将于今晚 22:00 进行。</p>
      </div>
      <div class="ds-alert ds-alert--warning">
        <span class="ds-alert-title">令牌即将过期</span>
        <p>API 密钥将在 3 天后失效。</p>
      </div>
    </div>
  </div>
</div>
```


---

## Pattern 10 — HTML Email Body

Use for: transactional email, newsletter, notification email.
**Rules:** no `backdrop-filter`, no CSS variables (email clients strip them),
use inline styles with OKLch equivalents as sRGB fallbacks.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>邮件标题</title>
</head>
<body style="margin:0;padding:0;background:#f7f5f0;font-family:'Noto Sans SC',-apple-system,sans-serif;">

  <!-- Outer wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" role="presentation">
    <tr>
      <td align="center" style="padding:32px 16px;">

        <!-- Email card -->
        <table width="600" cellpadding="0" cellspacing="0" role="presentation"
               style="max-width:600px;width:100%;background:#fff;border-radius:8px;
                      box-shadow:0 4px 24px rgba(0,0,0,.06);">

          <!-- Header -->
          <tr>
            <td style="padding:32px 40px 24px;border-bottom:1px solid #e6e2d9;">
              <span style="font-family:Georgia,serif;font-size:20px;font-weight:700;
                           color:#1a1814;letter-spacing:.04em;">EDIC</span>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:32px 40px;">
              <h1 style="font-family:Georgia,serif;font-size:28px;font-weight:700;
                         color:#1a1814;line-height:1.2;margin:0 0 16px;">
                邮件主标题
              </h1>
              <p style="font-size:16px;line-height:1.6;color:#4a453d;margin:0 0 24px;">
                正文内容。保持简洁，一个核心信息。
              </p>

              <!-- CTA button -->
              <table cellpadding="0" cellspacing="0" role="presentation">
                <tr>
                  <td style="border-radius:4px;background:#5a6e2a;">
                    <a href="#" style="display:inline-block;padding:12px 24px;
                                      font-size:14px;font-weight:600;color:#fff;
                                      text-decoration:none;letter-spacing:.02em;">
                      立即查看
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:24px 40px;border-top:1px solid #e6e2d9;">
              <p style="font-size:12px;color:#8c8077;margin:0;line-height:1.5;">
                © 2026 EDIC Design System · CC BY 4.0
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

**Email-specific rules:**
- Use `sRGB` hex/rgba, NOT `var(--ds-*)` or `oklch()` — email clients don't support either.
- Inline all styles. No external stylesheets.
- Table-based layout for maximum client compatibility.
- Test in Gmail, Outlook, Apple Mail before sending.
- Olive accent `#5a6e2a` ≈ sRGB equivalent of `oklch(52% 0.08 115)`.
