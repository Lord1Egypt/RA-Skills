# Styling & Theming

## Table of Contents
1. [Custom CSS basics](#custom-css)
2. [Starlight CSS custom properties](#css-props)
3. [Cascade layers](#cascade-layers)
4. [Tailwind CSS integration](#tailwind)
5. [Dark mode](#dark-mode)
6. [Expressive Code (syntax highlighting)](#expressive-code)
7. [Common styling pitfalls](#pitfalls)

---

## 1. Custom CSS basics {#custom-css}

Add custom styles by creating a CSS file and registering it in config:

```css
/* src/styles/custom.css */
:root {
  --sl-content-width: 50rem;
  --sl-text-5xl: 3.5rem;
}
```

```js
// astro.config.mjs
starlight({
  customCss: ['./src/styles/custom.css'],
})
```

You can list multiple CSS files. They're loaded in order, so later files override earlier ones.

You can also import npm packages:
```js
customCss: ['./src/styles/custom.css', '@fontsource/inter'],
```

## 2. Starlight CSS custom properties {#css-props}

Starlight exposes a comprehensive set of CSS custom properties for theming. Override them in your custom CSS.

### Color tokens

The two main color scales are **accent** (links, highlights) and **gray** (backgrounds, text, borders). Each has shades from 50 (lightest) to 950 (darkest).

```css
:root {
  /* Accent colors */
  --sl-color-accent-low: #1a1a4e;
  --sl-color-accent: #4f46e5;
  --sl-color-accent-high: #c7d2fe;

  /* You can also override individual Hue/Chroma values */
  --sl-hue-accent: 234;
  --sl-hue-gray: 240;
}
```

### Typography tokens

```css
:root {
  --sl-font: 'Inter', sans-serif;
  --sl-font-mono: 'JetBrains Mono', monospace;
  --sl-text-xs: 0.75rem;
  --sl-text-sm: 0.875rem;
  --sl-text-base: 1rem;
  --sl-text-lg: 1.125rem;
  --sl-text-xl: 1.25rem;
  --sl-text-2xl: 1.5rem;
  --sl-text-3xl: 1.875rem;
  --sl-text-4xl: 2.25rem;
  --sl-text-5xl: 3rem;
  --sl-text-6xl: 3.75rem;
}
```

### Layout tokens

```css
:root {
  --sl-content-width: 40rem;        /* Max width of content area */
  --sl-sidebar-width: 18.75rem;     /* Sidebar width */
  --sl-content-pad-x: 1rem;         /* Horizontal padding */
  --sl-nav-height: 3.5rem;          /* Top nav bar height */
}
```

Full list of properties: https://github.com/withastro/starlight/blob/main/packages/starlight/style/props.css

### Targeting dark mode

```css
:root[data-theme='dark'] {
  --sl-color-accent-low: #1e1b4b;
  --sl-color-accent: #818cf8;
}

:root[data-theme='light'] {
  --sl-color-accent-low: #eef2ff;
  --sl-color-accent: #4f46e5;
}
```

## 3. Cascade layers {#cascade-layers}

Starlight uses CSS cascade layers internally. Custom unlayered CSS automatically overrides Starlight defaults (because unlayered CSS beats layered CSS).

If you use layers in your own CSS, define the order explicitly:

```css
@layer my-reset, starlight, my-overrides;
```

- `my-reset` — applied before Starlight (Starlight can still override it)
- `starlight` — Starlight's own styles
- `my-overrides` — your overrides that always win

## 4. Tailwind CSS integration {#tailwind}

### New project with Tailwind

```bash
npm create astro@latest -- --template starlight/tailwind
```

### Adding Tailwind to existing Starlight project

1. Add Tailwind:
```bash
npx astro add tailwind
```

2. Install compatibility package:
```bash
npm install @astrojs/starlight-tailwind
```

3. Replace `src/styles/global.css` contents:
```css
@layer base, starlight, theme, components, utilities;
@import '@astrojs/starlight-tailwind';
@import 'tailwindcss/theme.css' layer(theme);
@import 'tailwindcss/utilities.css' layer(utilities);
```

4. Update `astro.config.mjs`:
```js
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Docs',
      customCss: ['./src/styles/global.css'],  // Must be first!
    }),
  ],
  vite: { plugins: [tailwindcss()] },
});
```

### Customizing Tailwind theme for Starlight

In `src/styles/global.css`, use `@theme` to override Starlight's colors:

```css
@layer base, starlight, theme, components, utilities;
@import '@astrojs/starlight-tailwind';
@import 'tailwindcss/theme.css' layer(theme);
@import 'tailwindcss/utilities.css' layer(utilities);

@theme {
  --font-sans: 'Inter';
  --font-mono: 'JetBrains Mono';

  /* Accent colors — indigo is closest to Starlight defaults */
  --color-accent-50: var(--color-indigo-50);
  --color-accent-100: var(--color-indigo-100);
  /* ... through 950 */

  /* Gray scale — zinc is closest to Starlight defaults */
  --color-gray-50: var(--color-zinc-50);
  --color-gray-100: var(--color-zinc-100);
  /* ... through 950 */
}
```

### Common Tailwind + Starlight conflicts

**Problem: Tailwind resets fight Starlight typography**
- The `@astrojs/starlight-tailwind` package handles this. Without it, Tailwind's Preflight reset removes Starlight's content styling.

**Problem: Tailwind classes don't work in .md/.mdx content**
- Tailwind utility classes work in Astro components. In Markdown content, Starlight applies its own content styles. Use `customCss` or custom components instead.

**Problem: Dark mode classes conflict**
- The Starlight Tailwind compatibility CSS configures `dark:` variants to sync with Starlight's theme switcher. Don't try to configure `darkMode` separately in Tailwind.

## 5. Dark mode {#dark-mode}

Starlight supports light/dark mode out of the box with a toggle in the header.

### Customizing dark mode colors

```css
:root[data-theme='dark'] {
  --sl-color-bg: #0f172a;
  --sl-color-bg-nav: #1e293b;
}

:root[data-theme='light'] {
  --sl-color-bg: #ffffff;
  --sl-color-bg-nav: #f8fafc;
}
```

### Disabling dark mode

There's no single config flag. You can hide the toggle by overriding the `ThemeSelect` component:

```js
// astro.config.mjs
starlight({
  components: {
    ThemeSelect: './src/components/EmptyThemeSelect.astro',
  },
})
```

```astro
<!-- src/components/EmptyThemeSelect.astro -->
<!-- Empty component — no theme toggle rendered -->
```

Then force a theme in CSS:
```css
:root { color-scheme: light; }
```

## 6. Expressive Code (syntax highlighting) {#expressive-code}

Starlight uses Expressive Code for code blocks. Enabled by default.

### Configuration

```js
starlight({
  expressiveCode: {
    themes: ['dracula', 'github-light'],
    styleOverrides: {
      borderRadius: '0.5rem',
      codeFontFamily: 'JetBrains Mono, monospace',
    },
    // Sync with Starlight's dark mode toggle
    useStarlightDarkModeSwitch: true,
    // Use Starlight's UI colors for code block chrome
    useStarlightUiThemeColors: true,
  },
})
```

### Disabling Expressive Code

```js
starlight({
  expressiveCode: false,
})
```

### Code block features in Markdown

Title: ````js title="config.js"````
Line highlighting: ````js {2-3}````
Insertions: ````js ins={3}````
Deletions: ````js del={1}````
Line numbers: Enabled via theme or config
File name tab: ````js title="src/index.js"````

## 7. Common styling pitfalls {#pitfalls}

**Problem: Custom CSS doesn't take effect**
- Check that the file path in `customCss` is correct (relative to project root).
- If using layers, ensure your layer order puts your overrides after `starlight`.
- Use browser devtools to check specificity conflicts.

**Problem: Fonts not loading**
- Install the font package: `npm install @fontsource/inter`
- Add to `customCss`: `customCss: ['@fontsource/inter', './src/styles/custom.css']`
- Set the font in CSS: `--sl-font: 'Inter', sans-serif;`

**Problem: Content area too narrow/wide**
- Override `--sl-content-width` in your custom CSS.

**Problem: Tailwind styles overriding Starlight in unexpected ways**
- Make sure `@astrojs/starlight-tailwind` is installed and imported.
- The global.css file must be listed first in `customCss`.
- Don't configure `darkMode` in Tailwind separately.
