---
name: fe-cli-astro
description: >
  Scaffold a static site / content site project. Supports Astro, Gatsby (React), and VitePress (Vue).
  For blogs, documentation sites, portfolios, landing pages with SSG/SSR.
  Triggered as a sub-skill of fe-cli when user wants Astro/Gatsby/建站/博客/文档站/VitePress project.
---

# fe-cli-astro — Static Site Scaffolding

## Workflow

### Step 1: Gather Options

1. **Framework**: Astro / Gatsby (React) / VitePress (Vue)
2. **UI Integration** (Astro only): React / Vue / Svelte / Preact / None (Astro components only)
3. **Styling**: Tailwind CSS / shadcn/ui (Astro+React) / 纯 SCSS
4. **Content**: MDX (Astro/Gatsby) / Markdown (all) / CMS integration (Contentful/Sanity) / None
5. **i18n**: Yes / No
6. **Deployment**: Vercel (default) / Netlify / Cloudflare Pages
7. **Project name**: string

**Quick guide:**
- **Blog / portfolio / content site** → Astro (islands architecture, partial hydration, fast)
- **React-heavy content site** → Gatsby (GraphQL data layer, rich plugin ecosystem)
- **Vue documentation site** → VitePress (Vue-powered static site, markdown-first)

### Step 2: Scaffold

**Astro:**
```
bun create astro@latest <project-name>
```
Interactive prompt: template (blog/docs/portfolio/empty), TypeScript, install dependencies.

Or with flags:
```
bunx create-astro <project-name> --template blog --typescript strict --install
```

**Gatsby:**
```
bunx gatsby new <project-name>
```

**VitePress:**
```
mkdir <project-name> && cd <project-name>
bun init
bun add -D vitepress vue
mkdir docs && echo '# Hello VitePress' > docs/index.md
```

### Step 3: Install Additional Dependencies

| Selection | Packages |
|---|---|
| **Astro** | |
| Tailwind CSS | `@astrojs/tailwind tailwindcss` (Astro 4+) or `tailwindcss @tailwindcss/vite` |
| React integration | `@astrojs/react react react-dom` |
| Vue integration | `@astrojs/vue vue` |
| MDX | `@astrojs/mdx` |
| i18n | `astro-i18next` / manual routing |
| shadcn/ui | `bun add -d shadcn && bunx shadcn init`（固定版本，if React integration）+ `lucide-react` |
| **Gatsby** | |
| Tailwind CSS | `tailwindcss postcss autoprefixer` + `gatsby-plugin-postcss` |
| MDX | `gatsby-plugin-mdx @mdx-js/react` |
| CMS | `gatsby-source-contentful` / `gatsby-source-sanity` |
| **VitePress** | |
| Tailwind CSS | `tailwindcss @tailwindcss/vite` |
| Vue components | `vue` (already included) |
| Search | `vitepress-plugin-search` / Algolia |

### Step 4: Project Structure

**Astro:**
```
project-name/
├── src/
│   ├── components/
│   │   ├── BaseHead.astro       # <head> meta tags, fonts, styles
│   │   ├── Header.astro         # Navigation header
│   │   ├── Footer.astro         # Site footer
│   │   └── Card.astro           # Content card component
│   ├── content/
│   │   ├── config.ts            # Content collection schema
│   │   └── blog/                # Blog posts (MDX/Markdown)
│   │       └── first-post.mdx
│   ├── layouts/
│   │   ├── BaseLayout.astro     # Page layout wrapper
│   │   └── BlogPost.astro       # Blog post layout
│   ├── pages/
│   │   ├── index.astro          # Home page
│   │   ├── about.astro          # About page
│   │   └── blog/
│   │       ├── index.astro      # Blog listing
│   │       └── [...slug].astro  # Dynamic blog post
│   └── styles/
│       └── global.scss          # Global styles
├── public/                      # Static assets
├── astro.config.mjs             # Astro configuration
├── tsconfig.json
└── package.json
```

**Gatsby:**
```
project-name/
├── src/
│   ├── components/
│   ├── pages/
│   │   ├── index.tsx
│   │   └── blog.tsx
│   ├── templates/
│   │   └── blog-post.tsx        # GraphQL template
│   └── styles/
├── gatsby-config.ts             # Plugins & metadata
├── gatsby-node.ts               # Programmatic page creation
└── package.json
```

**VitePress:**
```
project-name/
├── docs/
│   ├── .vitepress/
│   │   ├── config.ts            # VitePress config (nav, sidebar, theme)
│   │   └── theme/
│   │       └── index.ts         # Custom theme extensions
│   ├── index.md                 # Home page
│   ├── guide/                   # Guide pages
│   │   ├── getting-started.md
│   │   └── configuration.md
│   └── blog/                    # Blog pages
│       └── first-post.md
├── package.json
└── tsconfig.json
```

### Step 5: Key Templates

**`astro.config.mjs`:**
```javascript
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';        // if React integration
import mdx from '@astrojs/mdx';            // if MDX
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    react(),     // if selected
    mdx(),       // if selected
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
```

**`src/content/config.ts`** (Astro content collections):
```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { blog };
```

**`docs/.vitepress/config.ts`** (VitePress):
```typescript
import { defineConfig } from 'vitepress';

export default defineConfig({
  title: 'My Docs',
  description: 'Documentation site',
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Blog', link: '/blog/' },
    ],
    sidebar: {
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/getting-started' },
            { text: 'Configuration', link: '/guide/configuration' },
          ],
        },
      ],
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-org/your-repo' },
    ],
  },
});
```

### Step 6: Final Setup

```bash
cd <project-name>
bun install
bun dev      # Astro: http://localhost:4321 | VitePress: http://localhost:5173
```

**Deployment:**

Vercel (recommended, zero-config):
```bash
bun add -g vercel
vercel
```

Netlify:
```bash
bun add -g netlify-cli
netlify deploy --prod
```

Cloudflare Pages:
```bash
bunx wrangler pages deploy dist/
```

Astro adapter for SSR (if needed):
```
bun add @astrojs/vercel    # or @astrojs/netlify / @astrojs/cloudflare
```
Then add to `astro.config.mjs`: `output: 'server'` + adapter import.

Announce: Static site ready, framework, content setup, deploy target.
