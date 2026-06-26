# Components

## Table of Contents
1. [Built-in components overview](#built-in)
2. [Using components in MDX](#mdx-usage)
3. [Using components in Markdoc](#markdoc-usage)
4. [Built-in component catalog](#catalog)
5. [Custom components](#custom)
6. [Overriding Starlight components](#overriding)
7. [Common component pitfalls](#pitfalls)

---

## 1. Built-in components overview {#built-in}

Starlight ships with a set of UI components designed for documentation. Import them from `@astrojs/starlight/components` in `.mdx` files.

These components only work in `.mdx` files (not plain `.md`). If you need components, rename your file from `.md` to `.mdx`.

## 2. Using components in MDX {#mdx-usage}

Import and use like JSX:

```mdx
---
title: My Page
---

import { Tabs, TabItem } from '@astrojs/starlight/components';

<Tabs>
  <TabItem label="npm">npm install my-package</TabItem>
  <TabItem label="pnpm">pnpm add my-package</TabItem>
  <TabItem label="yarn">yarn add my-package</TabItem>
</Tabs>
```

You can also import your own custom components:

```mdx
import CustomCard from '../../components/CustomCard.astro';

<CustomCard title="Hello">
  This is custom content.
</CustomCard>
```

## 3. Using components in Markdoc {#markdoc-usage}

If using Markdoc (`.mdoc` files) with the Starlight Markdoc preset, built-in components are available without imports using `{% %}` tag syntax:

```markdoc
{% card title="Stars" icon="star" %}
Sirius, Vega, Betelgeuse
{% /card %}
```

## 4. Built-in component catalog {#catalog}

### Tabs

Multi-tab content blocks:

```mdx
import { Tabs, TabItem } from '@astrojs/starlight/components';

<Tabs>
  <TabItem label="Stars">Sirius, Vega</TabItem>
  <TabItem label="Planets">Jupiter, Saturn</TabItem>
</Tabs>
```

Synchronized tabs (tabs with the same `syncKey` switch together):
```mdx
<Tabs syncKey="pkg">
  <TabItem label="npm">npm run build</TabItem>
  <TabItem label="pnpm">pnpm build</TabItem>
</Tabs>

<!-- Later on the same page, these stay synced: -->
<Tabs syncKey="pkg">
  <TabItem label="npm">npm run dev</TabItem>
  <TabItem label="pnpm">pnpm dev</TabItem>
</Tabs>
```

### Cards

```mdx
import { Card, CardGrid } from '@astrojs/starlight/components';

<CardGrid>
  <Card title="Feature One" icon="rocket">
    Description of feature one.
  </Card>
  <Card title="Feature Two" icon="star">
    Description of feature two.
  </Card>
</CardGrid>
```

### Link Cards

Cards that are clickable links:

```mdx
import { LinkCard } from '@astrojs/starlight/components';

<LinkCard
  title="Getting Started"
  description="Learn the basics."
  href="/getting-started/"
/>
```

### Asides

Callout boxes. Can also be created with `:::note` syntax in plain Markdown.

```mdx
import { Aside } from '@astrojs/starlight/components';

<Aside type="tip" title="Did you know?">
  You can use components in MDX!
</Aside>
```

Types: `note`, `tip`, `caution`, `danger`.

### Steps

Numbered step-by-step instructions:

```mdx
import { Steps } from '@astrojs/starlight/components';

<Steps>
1. Install the package
   ```bash
   npm install my-package
   ```

2. Configure your project
   Edit `config.js` with your settings.

3. Deploy
   Push to your hosting provider.
</Steps>
```

### Code

Enhanced code blocks with Expressive Code features:

```mdx
import { Code } from '@astrojs/starlight/components';

export const exampleCode = `const greeting = 'Hello';
console.log(greeting);`;

<Code code={exampleCode} lang="js" title="example.js" />
```

Useful when you need to pass dynamic code from variables.

### File Tree

Visual file/folder structure:

```mdx
import { FileTree } from '@astrojs/starlight/components';

<FileTree>
- src/
  - content/
    - docs/
      - index.md
      - **getting-started.md** (highlighted)
  - components/
- astro.config.mjs
- package.json
</FileTree>
```

Bold items with `**name**`. Add comments with parentheses.

### Icons

```mdx
import { Icon } from '@astrojs/starlight/components';

<Icon name="star" size="1.5rem" />
```

See the icons reference for available names: https://starlight.astro.build/reference/icons/

### Link Buttons

```mdx
import { LinkButton } from '@astrojs/starlight/components';

<LinkButton href="/getting-started/" variant="primary" icon="right-arrow">
  Get Started
</LinkButton>
```

Variants: `primary`, `secondary`, `minimal`.

### Badges

```mdx
import { Badge } from '@astrojs/starlight/components';

<Badge text="New" variant="tip" />
<Badge text="Deprecated" variant="caution" />
```

Variants: `note`, `tip`, `caution`, `danger`, `success`, `default`.

## 5. Custom components {#custom}

### Creating an Astro component for docs

```astro
<!-- src/components/DocsCallout.astro -->
---
interface Props {
  type?: 'info' | 'warning';
  title: string;
}

const { type = 'info', title } = Astro.props;
---

<div class={`callout callout-${type}`}>
  <h3>{title}</h3>
  <slot />
</div>

<style>
  .callout {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
  }
  .callout-info { background: var(--sl-color-blue-low); }
  .callout-warning { background: var(--sl-color-orange-low); }
</style>
```

Use in MDX:
```mdx
import DocsCallout from '../../components/DocsCallout.astro';

<DocsCallout title="Important" type="warning">
  Don't forget to configure your base path!
</DocsCallout>
```

### Interactive components (React, Vue, Svelte, etc.)

For components that need client-side JavaScript, you need a `client:*` directive:

```mdx
import Counter from '../../components/Counter.jsx';

{/* Static — rendered at build time only, no interactivity */}
<Counter />

{/* Interactive — hydrated on the client */}
<Counter client:load />
```

Client directives:
- `client:load` — Hydrate immediately on page load (most common)
- `client:idle` — Hydrate when browser is idle
- `client:visible` — Hydrate when component scrolls into view
- `client:media` — Hydrate when a CSS media query matches
- `client:only="react"` — Skip server rendering, client only

### The `not-content` class

Starlight applies default content styles (margins, typography) to everything inside a doc page. If your component's layout conflicts:

```html
<div class="not-content">
  <!-- Your component's custom layout here -->
  <p>Not affected by Starlight content styles.</p>
</div>
```

## 6. Overriding Starlight components {#overriding}

You can replace any built-in Starlight component with your own:

```js
// astro.config.mjs
starlight({
  components: {
    // Replace the default header
    Header: './src/components/MyHeader.astro',
    // Replace social links
    SocialLinks: './src/components/MySocialLinks.astro',
    // Replace the theme toggle
    ThemeSelect: './src/components/MyThemeSelect.astro',
  },
})
```

Full list of overridable components: https://starlight.astro.build/reference/overrides/

To extend (not fully replace) a built-in component, import and wrap the original:

```astro
---
// src/components/MyHeader.astro
import type { Props } from '@astrojs/starlight/props';
import Default from '@astrojs/starlight/components/Header.astro';
---

<div class="my-header-wrapper">
  <Default {...Astro.props}><slot /></Default>
  <div class="custom-banner">Announcement here</div>
</div>
```

## 7. Common component pitfalls {#pitfalls}

**Problem: "Cannot use import statement" or import errors**
- You're trying to import in a `.md` file. Rename it to `.mdx`.

**Problem: Component renders but has no interactivity**
- Missing `client:load` (or another client directive). Without it, framework components render as static HTML.

**Problem: Component doesn't match Starlight's theme**
- Use Starlight's CSS custom properties (`var(--sl-color-*)`) instead of hardcoded colors.
- Check dark mode: use `[data-theme='dark']` selectors or Starlight's `--sl-color-*` which auto-switch.

**Problem: Hydration mismatch warnings**
- Ensure your interactive component produces the same HTML on server and client.
- Avoid `window` or `document` references during server rendering. Use `client:only="react"` for client-only components.

**Problem: Component layout breaks inside docs**
- Add `class="not-content"` to the wrapper element to opt out of Starlight's content typography styles.

**Problem: MDX component not found at runtime**
- Check the import path. Relative paths (`../../components/...`) are relative to the MDX file's location.
- Ensure the component file actually exports a default export (for Astro components, this is automatic).
