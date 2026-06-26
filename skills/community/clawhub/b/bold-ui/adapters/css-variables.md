# CSS Variables Adapter

Transform bold-ui design tokens into CSS custom properties and component styles. This adapter works for plain HTML/CSS projects, CSS Modules, or any project that uses vanilla CSS.

## Detection

You're in a CSS Variables project if:
- No Tailwind config found
- No CSS-in-JS framework detected
- `.css` files are the primary styling method
- Or the user explicitly requests plain CSS output

## Token Translation

### Design Token → CSS Custom Properties

Generate a `theme.css` file with all tokens as CSS custom properties:

```css
/* ===== Bold UI Theme: Modern Clean ===== */

:root {
  /* --- Colors --- */
  --bui-color-primary: #6366F1;
  --bui-color-primary-light: #818CF8;
  --bui-color-primary-dark: #4F46E5;
  --bui-color-secondary: #EC4899;
  --bui-color-secondary-light: #F472B6;
  --bui-color-secondary-dark: #DB2777;

  --bui-color-background: #F8FAFC;
  --bui-color-surface: #FFFFFF;
  --bui-color-elevated: #FFFFFF;

  --bui-color-text-primary: #0F172A;
  --bui-color-text-secondary: #475569;
  --bui-color-text-muted: #94A3B8;

  --bui-color-border: #E2E8F0;
  --bui-color-focus: var(--bui-color-primary);

  --bui-color-success: #10B981;
  --bui-color-warning: #F59E0B;
  --bui-color-error: #EF4444;
  --bui-color-info: #3B82F6;

  /* --- Typography --- */
  --bui-font-heading: 'Inter', 'SF Pro Display', -apple-system, sans-serif;
  --bui-font-body: 'Inter', 'SF Pro Text', -apple-system, sans-serif;
  --bui-font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --bui-text-xs: 0.75rem;
  --bui-text-sm: 0.875rem;
  --bui-text-base: 1rem;
  --bui-text-lg: 1.125rem;
  --bui-text-xl: 1.25rem;
  --bui-text-2xl: 1.5rem;
  --bui-text-3xl: 1.875rem;
  --bui-text-4xl: 2.25rem;

  --bui-font-normal: 400;
  --bui-font-medium: 500;
  --bui-font-semibold: 600;
  --bui-font-bold: 700;

  /* --- Spacing --- */
  --bui-space-0: 0;
  --bui-space-1: 0.25rem;
  --bui-space-2: 0.5rem;
  --bui-space-3: 0.75rem;
  --bui-space-4: 1rem;
  --bui-space-5: 1.25rem;
  --bui-space-6: 1.5rem;
  --bui-space-8: 2rem;
  --bui-space-10: 2.5rem;
  --bui-space-12: 3rem;
  --bui-space-16: 4rem;
  --bui-space-20: 5rem;

  /* --- Border Radius --- */
  --bui-radius-none: 0;
  --bui-radius-sm: 0.25rem;
  --bui-radius-md: 0.5rem;
  --bui-radius-lg: 0.75rem;
  --bui-radius-xl: 1rem;
  --bui-radius-full: 9999px;

  /* --- Shadows --- */
  --bui-shadow-none: none;
  --bui-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --bui-shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  --bui-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
  --bui-shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.04);

  /* --- Motion --- */
  --bui-duration-fast: 150ms;
  --bui-duration-normal: 200ms;
  --bui-duration-slow: 300ms;
  --bui-duration-gradual: 500ms;

  --bui-ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --bui-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --bui-ease-out: cubic-bezier(0, 0, 0.2, 1);
  --bui-ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* --- Decorations --- */
  --bui-gradient-primary: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
  --bui-gradient-subtle: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
  --bui-backdrop-blur: blur(8px);
}

/* Dark mode support — generate when user needs dark mode */
/* @media (prefers-color-scheme: dark) { ... } */
```

**Naming convention**: `--bui-<category>-<name>`. Use `nv` prefix to namespace and avoid conflicts with existing CSS.

### Import in project

Add to the main HTML or CSS entry point:

```html
<link rel="stylesheet" href="/theme.css">
```

Or in CSS:
```css
@import './theme.css';
```

## Component Generation

### Level 1: Theme Only

Generate only `theme.css` with CSS custom properties. Provide a brief usage guide comment at the top.

### Level 2: Base Components

Generate `components.css` with styled base components:

```css
/* ===== Bold UI Components: Modern Clean ===== */

/* --- Button --- */
.bui-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--bui-space-2);
  padding: var(--bui-space-2) var(--bui-space-4);
  font-family: var(--bui-font-body);
  font-size: var(--bui-text-sm);
  font-weight: var(--bui-font-medium);
  color: white;
  background: var(--bui-gradient-primary);
  border: none;
  border-radius: var(--bui-radius-md);
  box-shadow: var(--bui-shadow-sm);
  cursor: pointer;
  transition: transform var(--bui-duration-fast) var(--bui-ease-out),
              box-shadow var(--bui-duration-fast) var(--bui-ease-out);
}

.bui-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--bui-shadow-md);
}

.bui-btn:focus-visible {
  outline: 2px solid var(--bui-color-primary);
  outline-offset: 2px;
}

.bui-btn--secondary {
  background: var(--bui-color-surface);
  color: var(--bui-color-text-primary);
  border: 1px solid var(--bui-color-border);
}

.bui-btn--danger {
  background: var(--bui-color-error);
}

/* Sizes */
.bui-btn--sm { padding: var(--bui-space-1) var(--bui-space-3); font-size: var(--bui-text-xs); }
.bui-btn--lg { padding: var(--bui-space-3) var(--bui-space-6); font-size: var(--bui-text-base); }

/* --- Card --- */
.bui-card {
  background: var(--bui-color-surface);
  border: 1px solid var(--bui-color-border);
  border-radius: var(--bui-radius-lg);
  box-shadow: var(--bui-shadow-sm);
  padding: var(--bui-space-6);
  transition: transform var(--bui-duration-fast) var(--bui-ease-out),
              box-shadow var(--bui-duration-fast) var(--bui-ease-out);
}

.bui-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--bui-shadow-md);
}

/* --- Input --- */
.bui-input {
  width: 100%;
  padding: var(--bui-space-2) var(--bui-space-3);
  font-family: var(--bui-font-body);
  font-size: var(--bui-text-sm);
  color: var(--bui-color-text-primary);
  background: var(--bui-color-surface);
  border: 1px solid var(--bui-color-border);
  border-radius: var(--bui-radius-md);
  transition: border-color var(--bui-duration-fast) var(--bui-ease-out),
              box-shadow var(--bui-duration-fast) var(--bui-ease-out);
}

.bui-input::placeholder {
  color: var(--bui-color-text-muted);
}

.bui-input:focus {
  outline: none;
  border-color: var(--bui-color-primary);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.4); /* primary with 40% opacity */
}

/* --- Badge --- */
.bui-badge {
  display: inline-flex;
  align-items: center;
  padding: var(--bui-space-0-5) var(--bui-space-2-5);
  font-size: var(--bui-text-xs);
  font-weight: var(--bui-font-medium);
  border-radius: var(--bui-radius-full);
}

.bui-badge--success { background: rgba(16, 185, 129, 0.1); color: var(--bui-color-success); }
.bui-badge--warning { background: rgba(245, 158, 11, 0.1); color: var(--bui-color-warning); }
.bui-badge--error   { background: rgba(239, 68, 68, 0.1); color: var(--bui-color-error); }
.bui-badge--info    { background: rgba(59, 130, 246, 0.1); color: var(--bui-color-info); }

/* --- Modal --- */
.bui-modal-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: var(--bui-backdrop-blur);
  z-index: 50;
}

.bui-modal {
  background: var(--bui-color-surface);
  border-radius: var(--bui-radius-xl);
  box-shadow: var(--bui-shadow-xl);
  padding: var(--bui-space-6);
  max-width: 32rem;
  width: 90%;
  animation: bui-modal-in var(--bui-duration-normal) var(--bui-ease-out);
}

@keyframes bui-modal-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

### Level 3: Page Layouts

Generate `layout.css` with page-level layout patterns:

```css
/* Navigation */
.bui-nav { ... }
.bui-nav__brand { ... }
.bui-nav__links { ... }

/* Hero */
.bui-hero { ... }
.bui-hero__title { ... }
.bui-hero__subtitle { ... }

/* Footer */
.bui-footer { ... }

/* Container */
.bui-container {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--bui-space-4);
}

@media (min-width: 768px) {
  .bui-container { padding: 0 var(--bui-space-6); }
}

@media (min-width: 1024px) {
  .bui-container { padding: 0 var(--bui-space-8); }
}
```

## Integration Notes

- **Namespace everything**: Use the `nv-` prefix to avoid conflicts with existing CSS classes.
- **Don't reset globals**: Avoid applying styles to bare HTML elements (`body`, `a`, `h1`). Use class selectors only.
- **Respect existing styles**: If the project already has a CSS reset or base styles, work alongside them.
- **Font loading**: Include a Google Fonts or font-face declaration comment so the user knows to add the font.
- **Icons**: If the Iconify API is unavailable, fall back to `data/icon-fallback.json` for SVG path data, or use CSS-drawn/Unicode icons as a last resort.

## Icon Integration with CSS

Fetch icons from **Iconify** (free, no API key needed). Map the template's icon source to the corresponding Iconify prefix:

| Template source | Iconify prefix | Example URL |
|----------------|---------------|-------------|
| lucide         | `lucide`       | `https://api.iconify.design/lucide/search.svg` |
| phosphor       | `ph`           | `https://api.iconify.design/ph/magnifying-glass.svg` |
| heroicons      | `heroicons-outline` / `heroicons-solid` | `https://api.iconify.design/heroicons-outline/search.svg` |
| feather        | `feather`      | `https://api.iconify.design/feather/search.svg` |
| tabler         | `tabler`       | `https://api.iconify.design/tabler/search.svg` |

```
# Fetch icon SVG from Iconify
curl -s "https://api.iconify.design/lucide/search.svg?height=24"
```

Embed the returned SVG inline with the `nv-icon` class:

```html
<!-- Inline SVG from API response — allows currentColor inheritance -->
<svg class="bui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z M21 21l-4.35-4.35"/>
</svg>
```

```css
.bui-icon {
  width: 1.25rem;   /* matches template icon size 20px */
  height: 1.25rem;
  color: var(--bui-color-text-secondary);
  transition: color var(--bui-duration-fast) var(--bui-ease-out);
}

.bui-btn:hover .bui-icon {
  color: currentColor;
}
```
