# EDIC Component HTML Examples
# 高频复合组件 HTML 结构示例

> This file is loaded on demand when complex component structure is needed.
> All examples assume `styles.css` and `scripts.js` are linked.

---

## 1. Glass Card (`ds-glass-card`)

The glass card requires a colored background parent (`ds-glass-demo-bg`) to show the
backdrop-filter effect. `ds-glass-meta` lives **inside** `ds-glass-card` as the footer row.

```html
<!-- ✅ Correct: colored parent + card + inner meta -->
<div class="ds-glass-demo-bg">
  <div class="ds-glass-card">
    <span class="ds-badge ds-badge--accent">新</span>
    <h4>橄榄园笔记</h4>
    <p>玻璃卡片需要彩色背景父容器才能显示毛玻璃效果。</p>
    <div class="ds-glass-meta">
      <span class="ds-caption ds-text-muted">2026-06</span>
      <button class="ds-btn ds-btn--ghost">阅读全文</button>
    </div>
  </div>
</div>

<!-- ❌ Wrong: ds-glass-card placed directly on a plain white page —
     backdrop-filter has nothing to blur, card looks like a plain white box -->
```

Size modifiers: add `ds-glass-card--sm` (padding 1rem) or `ds-glass-card--lg` (padding 2rem).

---

## 2. Docs Layout (`ds-docs`)

Two-column layout: fixed sidebar left, scrollable main right.
`ds-docs-aside` holds `ds-pagenav`; `ds-docs-main` holds `ds-prose` content.

```html
<div class="ds-docs">
  <aside class="ds-docs-aside">
    <nav class="ds-pagenav" aria-label="页面导航">
      <details class="ds-pagenav-disclosure" open>
        <summary class="ds-pagenav-summary">
          <span class="ds-pagenav-chevron">▶</span> 目录
        </summary>
        <ol class="ds-pagenav-list">
          <li>
            <a href="#section-1" class="ds-pagenav-link ds-pagenav-link--active">
              <span class="ds-pagenav-num">01</span>
              <span class="ds-pagenav-text">介绍</span>
            </a>
          </li>
          <li>
            <a href="#section-2" class="ds-pagenav-link">
              <span class="ds-pagenav-num">02</span>
              <span class="ds-pagenav-text">安装</span>
            </a>
          </li>
        </ol>
      </details>
    </nav>
  </aside>

  <main class="ds-docs-main ds-prose" id="ds-main">
    <section id="section-1">
      <h1>介绍</h1>
      <p>正文内容区域，自动控制行宽在 65–75 字符。</p>
    </section>
    <section id="section-2">
      <h2>安装</h2>
      <p>引入 <code>styles.css</code> 即可。</p>
    </section>
  </main>
</div>
```

---

## 3. Navbar (`ds-navbar`)

The navbar uses a `::before` pseudo-element for the frosted glass background —
**do not add `background` directly on `.ds-navbar`**. JS adds `--scrolled` on scroll.

```html
<nav class="ds-navbar" role="navigation" aria-label="主导航">
  <div class="ds-navbar-inner">
    <!-- Brand -->
    <a href="/" class="ds-navbar-brand">
      <svg width="24" height="24" aria-hidden="true"><!-- logo mark --></svg>
      EDIC
    </a>

    <!-- Links (hidden on mobile; shown via mnav-panel JS) -->
    <div class="ds-navbar-links" id="mnav-panel">
      <a href="/" class="ds-navbar-link ds-navbar-link--active" aria-current="page">首页</a>
      <a href="/docs.html" class="ds-navbar-link">文档</a>
      <a href="/downloads.html" class="ds-navbar-link">下载</a>
    </div>

    <!-- Actions -->
    <div class="ds-navbar-actions">
      <a href="https://github.com/cgartlab/edic-design-system"
         class="ds-navbar-icon-link" aria-label="GitHub 仓库" target="_blank" rel="noopener">
        <svg width="20" height="20" aria-hidden="true"><!-- github icon --></svg>
      </a>
      <button class="ds-theme-toggle-btn" aria-label="切换主题" data-theme-mode="system">
        <svg width="18" height="18" aria-hidden="true"><!-- theme icon --></svg>
      </button>
      <a href="/downloads.html" class="ds-navbar-cta">下载</a>

      <!-- Mobile hamburger trigger -->
      <button class="ds-mnav-trigger" aria-label="打开菜单" aria-expanded="false"
              aria-controls="mnav-panel">
        <span class="ds-mnav-trigger-bar"></span>
        <span class="ds-mnav-trigger-bar"></span>
        <span class="ds-mnav-trigger-bar"></span>
      </button>
    </div>
  </div>
</nav>
<!-- Mobile backdrop (injected by scripts.js, shown when menu opens) -->
<div class="ds-mnav-backdrop" aria-hidden="true"></div>
```

---

## 4. Toast Notifications (`ds-toast-group`)

Toasts are **appended to `ds-toast-group` via JS** — do not hard-code individual toasts
in static HTML unless for preview purposes. The group lives near the bottom of `<body>`.

```html
<!-- Place once near </body> -->
<div class="ds-toast-group" role="status" aria-live="polite" aria-atomic="false"></div>

<!-- JS to trigger a toast -->
<script>
function showToast(message, type = '') {
  const group = document.querySelector('.ds-toast-group');
  const toast = document.createElement('div');
  toast.className = `ds-toast${type ? ' ds-toast--' + type : ''}`;
  toast.innerHTML = `
    <svg class="ds-toast-icon" width="18" height="18" aria-hidden="true">
      <use href="#icon-check-circle"></use>
    </svg>
    <span class="ds-toast-text">${message}</span>
    <button class="ds-toast-close" aria-label="关闭通知">×</button>
  `;
  group.prepend(toast);
  // Auto-dismiss after 4 s
  setTimeout(() => {
    toast.classList.add('ds-toast-dismissing');
    toast.addEventListener('transitionend', () => toast.remove(), { once: true });
  }, 4000);
  toast.querySelector('.ds-toast-close').addEventListener('click', () => {
    toast.classList.add('ds-toast-dismissing');
    toast.addEventListener('transitionend', () => toast.remove(), { once: true });
  });
}
</script>

<!-- Static preview (for docs / screenshots only) -->
<div class="ds-toast-group">
  <div class="ds-toast ds-toast--success">
    <svg class="ds-toast-icon" width="18" height="18" aria-hidden="true"><use href="#icon-check-circle"></use></svg>
    <span class="ds-toast-text">已保存成功</span>
    <button class="ds-toast-close" aria-label="关闭">×</button>
  </div>
  <div class="ds-toast ds-toast--error">
    <svg class="ds-toast-icon" width="18" height="18" aria-hidden="true"><use href="#icon-alert-circle"></use></svg>
    <span class="ds-toast-text">上传失败，请重试</span>
    <button class="ds-toast-close" aria-label="关闭">×</button>
  </div>
</div>
```

---

## 5. Accordion (`ds-accordion`)

JS from `scripts.js` toggles the `open` class on `ds-accordion-item`.
`ds-accordion-content` is `display:none` by default; `display:block` when parent has `.open`.

```html
<div class="ds-accordion">
  <!-- Item 1: open by default -->
  <div class="ds-accordion-item open">
    <div class="ds-accordion-header"
         role="button" tabindex="0"
         aria-expanded="true"
         aria-controls="acc-panel-1">
      <span>EDIC 是否需要构建工具？</span>
      <svg class="ds-accordion-arrow" width="18" height="18"
           viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
           aria-hidden="true">
        <polyline points="6 9 12 15 18 9"/>
      </svg>
    </div>
    <div class="ds-accordion-content" id="acc-panel-1" aria-hidden="false">
      不需要。纯静态 CSS + JS，复制文件引入即可。
    </div>
  </div>

  <!-- Item 2: collapsed -->
  <div class="ds-accordion-item">
    <div class="ds-accordion-header"
         role="button" tabindex="0"
         aria-expanded="false"
         aria-controls="acc-panel-2">
      <span>支持 React / Vue 吗？</span>
      <svg class="ds-accordion-arrow" width="18" height="18"
           viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
           aria-hidden="true">
        <polyline points="6 9 12 15 18 9"/>
      </svg>
    </div>
    <div class="ds-accordion-content" id="acc-panel-2" aria-hidden="true">
      可以。在框架入口引入 <code>styles.css</code>，组件写法与普通 HTML 一致。
    </div>
  </div>
</div>
```

---

## 6. Modal (`ds-modal`)

Modal requires an **overlay wrapper** to provide the dimmed backdrop.
Use `ds-overlay-layer` as the parent — it is `position:fixed`, covers the viewport,
and already provides `display:flex` + centering. Focus trap and `Esc` handling must be added via JS.

```html
<!-- Overlay backdrop: ds-overlay-layer = position:fixed + flex centering -->
<div class="ds-overlay-layer" id="modal-overlay" role="dialog"
     aria-modal="true" aria-labelledby="modal-title">

  <div class="ds-modal">
    <div class="ds-modal-header">
      <h2 id="modal-title" style="font-family:var(--ds-font-display);
          font-size:var(--ds-text-h4);">确认删除</h2>
      <button class="ds-modal-close" aria-label="关闭弹窗">×</button>
    </div>

    <div class="ds-modal-body">
      删除「草稿-03」？此操作无法撤销。
    </div>

    <div class="ds-modal-footer">
      <button class="ds-btn ds-btn--ghost" id="modal-cancel">取消</button>
      <button class="ds-btn ds-btn--primary"
              style="background:var(--ds-color-error);
                     border-color:var(--ds-color-error);">删除</button>
    </div>
  </div>
</div>

<script>
// Minimal: close on cancel / backdrop click / Esc
const overlay = document.getElementById('modal-overlay');
document.getElementById('modal-cancel').addEventListener('click',
  () => overlay.style.display = 'none');
overlay.addEventListener('click', e => { if (e.target === overlay) overlay.style.display = 'none'; });
document.addEventListener('keydown', e => { if (e.key === 'Escape') overlay.style.display = 'none'; });
</script>
```

---

## 7. Tabs (`ds-tabs` + `ds-tab-content`)

`ds-tab--active` on the button and `ds-tab-content--active` on the panel must be toggled
together. JS from `scripts.js` handles this automatically when the markup is correct.

```html
<!-- Tab bar -->
<div class="ds-tabs" role="tablist" aria-label="内容分类">
  <button class="ds-tab ds-tab--active"
          role="tab" aria-selected="true" aria-controls="tab-panel-1" id="tab-1">
    概览
  </button>
  <button class="ds-tab"
          role="tab" aria-selected="false" aria-controls="tab-panel-2" id="tab-2">
    用法
  </button>
  <button class="ds-tab"
          role="tab" aria-selected="false" aria-controls="tab-panel-3" id="tab-3">
    代码
  </button>
</div>

<!-- Tab panels (only the active one is visible) -->
<div class="ds-tab-content ds-tab-content--active"
     id="tab-panel-1" role="tabpanel" aria-labelledby="tab-1">
  <p>概览内容</p>
</div>
<div class="ds-tab-content"
     id="tab-panel-2" role="tabpanel" aria-labelledby="tab-2" hidden>
  <p>用法内容</p>
</div>
<div class="ds-tab-content"
     id="tab-panel-3" role="tabpanel" aria-labelledby="tab-3" hidden>
  <pre><code class="language-html">&lt;div class="ds-tabs"&gt;...&lt;/div&gt;</code></pre>
</div>
```

---

## 8. Dropdown (`ds-dropdown`)

Dropdown requires a **`position:relative` parent wrapper** and JS to toggle visibility.
It is not a `<select>` — it is a styled floating panel.

```html
<!-- Wrapper provides the positioning context -->
<div style="position:relative; display:inline-block;">
  <button class="ds-btn ds-btn--secondary" id="dd-trigger"
          aria-haspopup="true" aria-expanded="false" aria-controls="dd-menu">
    操作
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" aria-hidden="true">
      <polyline points="6 9 12 15 18 9"/>
    </svg>
  </button>

  <div class="ds-dropdown" id="dd-menu" role="menu"
       style="display:none; position:absolute; top:calc(100% + var(--ds-space-1)); right:0; z-index:var(--ds-z-dropdown);">
    <div class="ds-dropdown-item" role="menuitem">
      <svg width="16" height="16" aria-hidden="true"><use href="#icon-edit"></use></svg>
      编辑
    </div>
    <div class="ds-dropdown-item" role="menuitem">
      <svg width="16" height="16" aria-hidden="true"><use href="#icon-copy"></use></svg>
      复制链接
    </div>
    <div class="ds-dropdown-divider" role="separator"></div>
    <div class="ds-dropdown-item" role="menuitem"
         style="color:var(--ds-color-error);">
      <svg width="16" height="16" aria-hidden="true"><use href="#icon-trash"></use></svg>
      删除
    </div>
  </div>
</div>

<script>
const trigger = document.getElementById('dd-trigger');
const menu = document.getElementById('dd-menu');
trigger.addEventListener('click', () => {
  const open = menu.style.display !== 'none';
  menu.style.display = open ? 'none' : 'block';
  trigger.setAttribute('aria-expanded', String(!open));
});
document.addEventListener('click', e => {
  if (!trigger.contains(e.target) && !menu.contains(e.target)) {
    menu.style.display = 'none';
    trigger.setAttribute('aria-expanded', 'false');
  }
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    menu.style.display = 'none';
    trigger.setAttribute('aria-expanded', 'false');
    trigger.focus();
  }
});
</script>
```
