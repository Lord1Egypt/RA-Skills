---
name: edic-design-system
slug: edic-design-system
displayName: EDIC 设计系统
version: 1.9.1
description: >-
  Generate UI components, full pages, documents, emails, and assets that
  strictly follow the EDIC design system (Editorial × Olive Green, OKLch
  tokens, dark-mode ready, CJK-optimized). Use this skill whenever the user asks
  to build, style, or refactor anything for EDIC, or explicitly requests the
  EDIC / "editorial olive" design system. Output token-driven, accessible,
  framework-agnostic HTML/CSS.
license: MIT-0
---

# EDIC Design System Skill

When this skill is active, every visual artifact you produce — components, pages,
landing sections, documentation, emails, reports — must conform to the EDIC
design system. **Prefer design tokens (CSS custom properties). Never hard-code
magic numbers.**

## Design character
- **Editorial × Olive Green**: magazine-grade restraint, generous whitespace,
  serif headings + sans body, a warm paper background, and a confident — never
  loud — olive-green accent.
- Reference moods: Monocle (typographic restraint), Stripe (warm utility),
  Mercury (refined calm).

## Hard rules (anti-patterns)
- Define all colors in **OKLch**; mix with `color-mix(in oklch, …)`.
- Use `var(--ds-*)` tokens for every visual value. No hard-coded `#fff` / `16px`.
- Dark mode never uses pure black `#000` — use warm grey `oklch(15% 0.008 75)`.
- In dark mode, lighten the accent ~5–10% vs. light mode.
- Components use base + modifier: `ds-btn` / `ds-btn--primary`.
- No inline `style=` except genuinely dynamic values (e.g. stagger `--d`).
- Icon-only buttons need `aria-label`; decorative SVGs need `aria-hidden="true"`.

## Color tokens (core)
Light (`:root`):
```
--ds-color-bg: oklch(97% 0.012 80)          /* warm paper background */
--ds-color-surface: oklch(99% 0.005 80)
--ds-color-surface-raised: oklch(100% 0 0)  /* popovers / modals */
--ds-color-border: oklch(89% 0.012 80)
--ds-color-muted: oklch(48% 0.015 60)       /* secondary text */
--ds-color-fg: oklch(20% 0.02 60)           /* body text */
--ds-color-fg-strong: oklch(14% 0.025 60)   /* headings */
```
Olive ramp `--ds-color-olive-50…900`; accent:
```
--ds-color-olive-400: oklch(52% 0.08 115)   /* === --ds-accent === */
--ds-accent-hover: var(--ds-color-olive-500)
--ds-accent-soft:  var(--ds-color-olive-100)
```
Semantic (each has a `-bg` tint): success `oklch(55% 0.1 145)`,
warning `oklch(65% 0.1 85)`, error `oklch(50% 0.14 30)`, info `oklch(55% 0.08 240)`.
Dark (`[data-theme="dark"]`): base `oklch(15% 0.008 75)`, body `oklch(84% 0.008 72)`,
accent `oklch(57% 0.065 115)`.

## Typography
```
--ds-font-display: "Iowan Old Style","Charter",Georgia,"Noto Serif SC",serif
--ds-font-body / --ds-font-ui: "Noto Sans SC",-apple-system,system-ui,sans-serif
--ds-font-mono: "JetBrains Mono","IBM Plex Mono",monospace
```
Scale (rem): caption .75 · body-sm .875 · body 1 · body-lg 1.125 · lead 1.25 ·
h4 1.5 · h3 1.875 · h2 2.25 · h1 3 · display 3.75 · hero 4.5.
- Headings: display family + `--ds-leading-tight` (1.1) + `--ds-tracking-tight` (-0.01em).
- Body: line-height 1.55, measure 65–75 chars (~540px / 72ch).
- CJK/Latin mix: body tracking 0.03em, heading 0.06em; full-width CJK punctuation.

## Spacing / radius / shadow / motion
- Spacing: 4px base, `--ds-space-1..32` (4→128px).
- Radius: sm 2 · md 4 · lg 8 · xl 12 · 2xl 16 · full. Core 8–16px.
- Shadow: `--ds-shadow-xs..2xl`.
- Motion: duration `--ds-duration-150..500`; ease `--ds-ease-out: cubic-bezier(.16,1,.3,1)`,
  `--ds-ease-spring`. Always honor `prefers-reduced-motion: reduce`.

## Component class catalog

### Layout
- **基础布局**: `ds-wrapper` `ds-section` (`--alt`/`--tight`) `ds-stack` (`--sm`/`--lg`) `ds-cluster` (`--center`) `ds-prose` `ds-flex-row`
- **网格系统**: `ds-grid-2` `ds-grid-3` `ds-grid-4` `ds-grid-6` `ds-grid-icons` `ds-feature-grid`
- **区块元素**: `ds-section-head` (`--center`) `ds-section-header`
- **间距工具**: `ds-mt-*` `ds-mb-*` `ds-pt-0` `ds-gap-16` `ds-mx-auto` `ds-items-center` `ds-justify-start`
- **间距展示**: `ds-spacing-vis` `ds-spacing-block` `ds-radius-vis` `ds-shadow-vis`

### Buttons & Interactive
- **按钮**: `ds-btn` + `--primary`/`--secondary`/`--ghost` + `--sm`/`--lg`
- **图标按钮**: `ds-icon-btn`
- **复制按钮**: `ds-copy-btn` (`--light`)

### Cards & Surfaces
- **卡片**: `ds-card` + `--hoverable`/`--flat`
- **玻璃卡片**: `ds-glass-card` (`--sm`/`--lg`) `ds-glass-meta` `ds-glass-demo-bg`
- **组件预览**: `ds-component-preview` `ds-component-group` `ds-component-label`

### Forms
- **基础表单**: `ds-input` (`--error`) `ds-label` `ds-hint` `ds-select` `ds-checkbox` `ds-radio` `ds-toggle` (`--track`/`--thumb`)
- **扩展表单**: `ds-form-input` `ds-form-textarea` `ds-form-select` `ds-form-row` `ds-form-group` `ds-form-label` `ds-form-checkbox` `ds-form-hint` (`--error`) `ds-form-submit` `ds-form-required`

### Feedback
- **徽章**: `ds-badge` (`--default`/`--accent`/`--success`/`--warning`/`--error`)
- **警告框**: `ds-alert` (`--info`/`--success`/`--warning`/`--error`) `ds-alert-icon` `ds-alert-title`
- **通知**: `ds-toast` (`--error`/`--success`/`--warning`) `ds-toast-group` `ds-toast-icon` `ds-toast-text` `ds-toast-close`

### Navigation
- **导航栏**: `ds-navbar` (`--scrolled`) `ds-navbar-inner` `ds-navbar-brand` `ds-navbar-links` `ds-navbar-link` (`--active`) `ds-navbar-actions` `ds-navbar-cta` `ds-navbar-icon-link`
- **移动端菜单**: `ds-mnav-trigger` `ds-mnav-trigger-bar` `ds-mnav-backdrop`
- **页面导航**: `ds-pagenav` (`--rail`/`--hidden`) `ds-pagenav-disclosure` `ds-pagenav-summary` `ds-pagenav-chevron` `ds-pagenav-list` `ds-pagenav-link` (`--active`) `ds-pagenav-num` `ds-pagenav-text`
- **标签页**: `ds-tabs` `ds-tab` (`--active`) `ds-tab-content` (`--active`)
- **面包屑**: `ds-breadcrumb` `ds-breadcrumb-current` `ds-breadcrumb-sep`
- **分页**: `ds-pagination` `ds-page-btn` (`--active`)
- **侧边导航**: `ds-nav` `ds-nav-item` (`--active`) `ds-nav-icon` `ds-nav-section-label`
- **霜冻导航**: `ds-frosted-nav`
- **主题切换**: `ds-theme-toggle-btn` (`--fixed`)

### Data Display
- **表格**: `ds-table` `ds-table-wrap` `ds-table-mini` `ds-table-mini-row`
- **进度条**: `ds-progress` `ds-progress-bar` `ds-progress-fill` `ds-progress-label`
- **头像**: `ds-avatar` (`--sm`/`--lg`)
- **芯片/标签**: `ds-chip` (`--active`) `ds-chip-remove`
- **骨架屏**: `ds-skeleton`
- **色卡**: `ds-swatch` `ds-swatch-color` `ds-swatch-info` `ds-swatch-name` `ds-swatch-value`
- **类型标签**: `ds-type-label` `ds-type-label-meta`

### Overlay & Glass
- **遮罩层**: `ds-overlay-sample` `ds-overlay-bg` `ds-overlay-layer` `ds-overlay-strong` `ds-overlay-light` `ds-overlay-label`
- **模态框**: `ds-modal` `ds-modal-header` `ds-modal-body` `ds-modal-footer` `ds-modal-close`
- **工具提示**: `ds-tooltip-demo` `ds-tooltip-bubble`
- **下拉菜单**: `ds-dropdown` `ds-dropdown-item` `ds-dropdown-divider`

### Typography
- **标题**: `ds-display` `ds-hero` `ds-h1` `ds-h2` `ds-h3` `ds-h4` `ds-h5` `ds-subtitle`
- **正文**: `ds-lead` `ds-caption` `ds-eyebrow` `ds-serif` `ds-mono` `ds-meta` `ds-cover`
- **中文排版**: `ds-text-cjk` `ds-text-cjk-heading` `ds-text-mixed` `ds-text-indent` `ds-hanging-punctuation` `ds-text-emphasis` `ds-text-highlight`
- **引用**: `ds-quote-cjk` `ds-no-orphan` `ds-num-unit`
- **工具**: `ds-text-center` `ds-text-muted` `ds-text-accent` `ds-text-balance` `ds-text-pretty` `ds-inline-code` `ds-body-sm`

### Article TOC
- **目录**: `ds-toc` `ds-toc-article` `ds-toc-article-title` `ds-toc-list` `ds-toc-link` (`--active`/`--h3`) `ds-toc-indicator` `ds-toc-badge` `ds-toc-grid` `ds-toc-item` `ds-toc-num`

### Timeline
- **时间线**: `ds-timeline` `ds-timeline-item` `ds-timeline-dot` `ds-timeline-content` `ds-timeline-date` `ds-timeline-title` `ds-timeline-tag`

### Date / Calendar
- **日期组**: `ds-date-group` `ds-date-wrap` `ds-date-input` `ds-date-icon` `ds-date-calendar`
- **日历**: `ds-cal-header` `ds-cal-nav` `ds-cal-month-year` `ds-cal-month` `ds-cal-year` `ds-cal-weekdays` `ds-cal-grid-new` `ds-cal-day` `ds-cal-today` `ds-cal-selected` `ds-cal-muted` `ds-cal-weekend` `ds-cal-weekend-col` `ds-cal-footer` `ds-cal-btn` (`--primary`)

### Slider
- **滑块**: `ds-slider-group` `ds-slider-label-row` `ds-slider-value` `ds-slider-track-wrap` `ds-slider-track` `ds-slider-fill` `ds-slider` `ds-slider-labels`

### Accordion
- **手风琴**: `ds-accordion` `ds-accordion-item` `ds-accordion-header` `ds-accordion-arrow` `ds-accordion-content`

### Code Block
- **代码**: `ds-code` `ds-code-bar` `ds-code-lang`

### Brand / Logo
- **Logo**: `ds-logo` (`--lg`) `ds-logo-mark` `ds-logo-text` `ds-logo-word` `ds-logo-sub` `ds-logo-hero` `ds-logo-draw`
- **品牌预览**: `ds-brand-preview` (`--paper`/`--ink`)

### Site Shell
- **英雄区**: `ds-hero-section` `ds-hero-inner` `ds-hero-badge` `ds-hero-title` `ds-hero-lead` `ds-hero-actions` `ds-hero-meta` `ds-hero-mark-wrap` `ds-gradient-text`
- **数据统计**: `ds-stat-grid` `ds-stat` `ds-stat-num` `ds-stat-label`
- **步骤列表**: `ds-steps` `ds-step` `ds-step-num` `ds-step-body`
- **兼容徽章**: `ds-compat-grid` `ds-compat-item` `ds-cta-h2`
- **特性卡片**: `ds-feature-card` `ds-feature-ico`
- **下载卡片**: `ds-dl-grid` (`--two-rows`) `ds-dl-card` `ds-dl-top` `ds-dl-ico` `ds-dl-meta` `ds-dl-actions`
- **文档布局**: `ds-docs` `ds-docs-aside` `ds-docs-main` `ds-doc-block`
- **提示卡片**: `ds-prompt` `ds-prompt-head` `ds-prompt-title` `ds-prompt-body` `ds-prompt-foot`
- **富页脚**: `ds-footer-rich` `ds-footer-cols` `ds-footer-brand` `ds-footer-col-heading` `ds-footer-links` `ds-footer-bottom`

### Motion & Animation
- **滚动揭示**: `ds-reveal` (`--left`/`--right`/`--scale`, stagger via inline `--d`)
- **连续动效**: `ds-anim-float` `ds-anim-spin-slow` `ds-anim-pulse` `ds-anim-fade-in` `ds-anim-rise` `ds-anim-glow-breathe`

### Gravitas & Glow (dark-mode accent)
- **发光效果**: `ds-glow-border` `ds-aura` `ds-surface-glow` `ds-heading-glow`

### Decorative
- **边缘装饰**: `ds-edge-decor` (`--tl`/`--tr`/`--bl`/`--br`)
- **背景斑点**: `ds-bg-blob` (`--1`/`--2`/`--3`)

### Accessibility
- **无障碍**: `ds-sr-only` `ds-skip` `#ds-main`

## Output expectations
- Produce complete, runnable HTML fragments assuming `styles.css` (and optional
  `scripts.js`) are linked.
- If the host has no stylesheet, include a minimal `<style>` but still use OKLch
  and equivalent token values.
- Use semantic structure (`header/main/section/nav/footer`) with correct heading order.
- Default to light theme and guarantee the same markup works under `[data-theme="dark"]`.
- When unsure, favor the more restrained, more whitespace, more editorial option.

## Example: token-driven card
```html
<article class="ds-card ds-card--hoverable">
  <span class="ds-badge ds-badge--accent">新</span>
  <h4 class="ds-serif ds-mt-3">橄榄园笔记</h4>
  <p class="ds-text-muted">使用令牌的卡片，悬停浮起，深浅主题自适配。</p>
  <a class="ds-btn ds-btn--primary ds-mt-4" href="#">阅读全文</a>
</article>
```

## Reference
- Website: https://edic.cgartlab.com/
- Usage docs: https://edic.cgartlab.com/docs.html
- Structured tokens: https://edic.cgartlab.com/tokens.json
