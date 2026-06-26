# Theming Reference

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [CSS Custom Properties Strategy](#css-custom-properties-strategy)
3. [Dark Mode Implementation](#dark-mode-implementation)
4. [React ThemeProvider](#react-themeprovider)
5. [Vue 3 Theme System](#vue-3-theme-system)
6. [Runtime Theme Switching](#runtime-theme-switching)
7. [Tailwind CSS Integration](#tailwind-css-integration)

---

## Architecture Overview

The theming system has three layers:

```
Layer 1: Primitive Tokens    → Raw values (hex colors, px sizes)
Layer 2: Semantic Tokens     → Intent-based CSS variables (light/dark variants)
Layer 3: Component Tokens    → Component-scoped overrides (optional)
```

**The rule:** Components only reference **semantic tokens**. Switching a theme only requires swapping the semantic layer — components need zero changes.

```
Light theme:  --ds-color-surface = #ffffff
Dark theme:   --ds-color-surface = #0f172a

<Card> always uses: background: var(--ds-color-surface)
```

---

## CSS Custom Properties Strategy

### Primitive + Semantic Separation

```css
/* packages/tokens/dist/tokens.css */

/* ─── Primitives (global, never change) ─── */
:root {
  --ds-blue-50:  #eff6ff;
  --ds-blue-500: #3b82f6;
  --ds-blue-600: #2563eb;
  --ds-blue-700: #1d4ed8;
  --ds-gray-50:  #f9fafb;
  --ds-gray-100: #f3f4f6;
  --ds-gray-900: #111827;
  --ds-white:    #ffffff;
  --ds-black:    #000000;
}

/* ─── Light Theme (default) ─── */
:root,
[data-theme="light"] {
  /* Surfaces */
  --ds-color-bg-base:     var(--ds-white);
  --ds-color-bg-subtle:   var(--ds-gray-50);
  --ds-color-bg-muted:    var(--ds-gray-100);

  /* Text */
  --ds-color-text-primary:   var(--ds-gray-900);
  --ds-color-text-secondary: #4b5563;    /* gray-600 */
  --ds-color-text-disabled:  #9ca3af;   /* gray-400 */
  --ds-color-text-inverse:   var(--ds-white);

  /* Interactive */
  --ds-color-primary:         var(--ds-blue-600);
  --ds-color-primary-hover:   var(--ds-blue-700);
  --ds-color-primary-active:  var(--ds-blue-700);
  --ds-color-primary-subtle:  var(--ds-blue-50);
  --ds-color-primary-text:    var(--ds-white);

  /* Borders */
  --ds-color-border-default: #e5e7eb;  /* gray-200 */
  --ds-color-border-strong:  #9ca3af;  /* gray-400 */

  /* Feedback */
  --ds-color-error:    #dc2626;
  --ds-color-warning:  #d97706;
  --ds-color-success:  #16a34a;
  --ds-color-info:     var(--ds-blue-600);

  /* Shadows */
  --ds-shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --ds-shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --ds-shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* ─── Dark Theme ─── */
[data-theme="dark"] {
  /* Surfaces */
  --ds-color-bg-base:     #0f172a;   /* slate-900 */
  --ds-color-bg-subtle:   #1e293b;   /* slate-800 */
  --ds-color-bg-muted:    #334155;   /* slate-700 */

  /* Text */
  --ds-color-text-primary:   #f1f5f9;   /* slate-100 */
  --ds-color-text-secondary: #94a3b8;   /* slate-400 */
  --ds-color-text-disabled:  #475569;   /* slate-600 */
  --ds-color-text-inverse:   #0f172a;

  /* Interactive */
  --ds-color-primary:         var(--ds-blue-500);  /* lighter in dark mode */
  --ds-color-primary-hover:   var(--ds-blue-600);
  --ds-color-primary-active:  var(--ds-blue-700);
  --ds-color-primary-subtle:  #1e3a8a;   /* blue-900 */
  --ds-color-primary-text:    var(--ds-white);

  /* Borders */
  --ds-color-border-default: #334155;  /* slate-700 */
  --ds-color-border-strong:  #475569;  /* slate-600 */

  /* Shadows (stronger in dark mode) */
  --ds-shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.4);
  --ds-shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
  --ds-shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4);
}
```

---

## Dark Mode Implementation

### Strategy Options

| Strategy | How it works | Pros | Cons |
|---|---|---|---|
| **Media query** | `@media (prefers-color-scheme: dark)` | Auto, no JS | Can't override user choice |
| **Data attribute** | `[data-theme="dark"]` on `<html>` | Full control, user preference | Requires JS |
| **Class-based** | `.dark` on `<html>` (Tailwind style) | Familiar, works with Tailwind | Coupling to class names |

**Recommended: data attribute** — gives user control while respecting system preference.

### Implementation

```ts
// packages/utils/src/theme.ts

type Theme = 'light' | 'dark' | 'system';

const STORAGE_KEY = 'ds-theme';

function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme: 'light' | 'dark') {
  document.documentElement.setAttribute('data-theme', theme);
  document.documentElement.style.colorScheme = theme;
}

export function initTheme() {
  const saved = localStorage.getItem(STORAGE_KEY) as Theme | null;
  const resolved = saved === 'dark' || saved === 'light'
    ? saved
    : getSystemTheme();
  applyTheme(resolved);
  return resolved;
}

export function setTheme(theme: Theme) {
  localStorage.setItem(STORAGE_KEY, theme);
  const resolved = theme === 'system' ? getSystemTheme() : theme;
  applyTheme(resolved);
}

// Watch for system preference changes
export function watchSystemTheme(onChange: (theme: 'light' | 'dark') => void) {
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  mq.addEventListener('change', (e) => onChange(e.matches ? 'dark' : 'light'));
}
```

---

## React ThemeProvider

```tsx
// packages/themes/src/ThemeProvider.tsx
import * as React from 'react';
import { initTheme, setTheme, watchSystemTheme } from '@myds/utils/theme';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextValue {
  theme: Theme;
  resolvedTheme: 'light' | 'dark';
  setTheme: (theme: Theme) => void;
}

const ThemeContext = React.createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = React.useState<Theme>('system');
  const [resolvedTheme, setResolvedTheme] = React.useState<'light' | 'dark'>('light');

  React.useEffect(() => {
    const resolved = initTheme();
    setResolvedTheme(resolved);

    watchSystemTheme((systemTheme) => {
      const saved = localStorage.getItem('ds-theme') as Theme;
      if (!saved || saved === 'system') {
        setResolvedTheme(systemTheme);
      }
    });
  }, []);

  const handleSetTheme = React.useCallback((newTheme: Theme) => {
    setThemeState(newTheme);
    setTheme(newTheme);
    setResolvedTheme(newTheme === 'system'
      ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      : newTheme
    );
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme: handleSetTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = React.useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
}
```

### Theme Toggle Component

```tsx
export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  return (
    <button
      onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
      aria-label={`Switch to ${resolvedTheme === 'dark' ? 'light' : 'dark'} mode`}
    >
      {resolvedTheme === 'dark' ? '☀️' : '🌙'}
    </button>
  );
}
```

---

## Vue 3 Theme System

```ts
// composables/useTheme.ts
import { ref, watchEffect } from 'vue';

type Theme = 'light' | 'dark' | 'system';

const theme = ref<Theme>('system');
const resolvedTheme = ref<'light' | 'dark'>('light');

function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

watchEffect(() => {
  const resolved = theme.value === 'system' ? getSystemTheme() : theme.value;
  resolvedTheme.value = resolved;
  document.documentElement.setAttribute('data-theme', resolved);
  document.documentElement.style.colorScheme = resolved;
});

export function useTheme() {
  return { theme, resolvedTheme };
}
```

**Provide at app root:**

```ts
// main.ts
import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

// Initialize theme before mount
const saved = localStorage.getItem('ds-theme');
document.documentElement.setAttribute(
  'data-theme',
  saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
);

app.mount('#app');
```

---

## Runtime Theme Switching

### No Flash of Wrong Theme (FWOT)

Add to `<head>` before any JS bundles:

```html
<script>
  (function() {
    var theme = localStorage.getItem('ds-theme');
    var dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var resolved = theme === 'dark' || (!theme && dark) ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', resolved);
    document.documentElement.style.colorScheme = resolved;
  })();
</script>
```

This runs synchronously, preventing the flash before React/Vue hydrates.

---

## Tailwind CSS Integration

If using Tailwind, configure it to use your CSS variables:

```js
// tailwind.config.js
module.exports = {
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--ds-color-primary)',
          hover: 'var(--ds-color-primary-hover)',
          subtle: 'var(--ds-color-primary-subtle)',
        },
        bg: {
          base: 'var(--ds-color-bg-base)',
          subtle: 'var(--ds-color-bg-subtle)',
        },
        text: {
          primary: 'var(--ds-color-text-primary)',
          secondary: 'var(--ds-color-text-secondary)',
        },
        border: {
          default: 'var(--ds-color-border-default)',
        },
      },
    },
  },
};
```
