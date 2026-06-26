# Project Setup & Structure

## Table of Contents
1. [Scaffolding a new project](#scaffolding)
2. [Adding Starlight to an existing Astro project](#manual-setup)
3. [Project structure anatomy](#project-structure)
4. [astro.config.mjs deep dive](#config)
5. [Content collections setup](#content-collections)
6. [Updating Starlight](#updating)

---

## 1. Scaffolding a new project {#scaffolding}

The fastest way to start:

```bash
# npm
npm create astro@latest -- --template starlight

# pnpm
pnpm create astro --template starlight

# yarn
yarn create astro --template starlight
```

For Starlight + Tailwind pre-configured:
```bash
npm create astro@latest -- --template starlight/tailwind
```

After scaffolding, start the dev server:
```bash
cd my-docs
npm run dev
```

## 2. Adding Starlight to an existing Astro project {#manual-setup}

Install the integration:
```bash
npx astro add starlight
```

This does three things:
- Installs `@astrojs/starlight`
- Adds the integration to `astro.config.mjs`
- Creates `src/content/docs/` with a starter page
- Creates `src/content.config.ts` with the docs collection

If the CLI doesn't do everything, manually:

1. Install: `npm install @astrojs/starlight`
2. Add to config (see section 4 below)
3. Create `src/content/docs/index.md` with a title in frontmatter
4. Create `src/content.config.ts` (see section 5 below)

## 3. Project structure anatomy {#project-structure}

```
my-docs/
├── astro.config.mjs          # Main config — Starlight lives here
├── src/
│   ├── content/
│   │   └── docs/              # ALL doc pages go here (file-based routing)
│   │       ├── index.mdx      # → yoursite.com/
│   │       ├── guides/
│   │       │   ├── intro.md   # → yoursite.com/guides/intro/
│   │       │   └── setup.md   # → yoursite.com/guides/setup/
│   │       └── reference/
│   │           └── api.md     # → yoursite.com/reference/api/
│   ├── content.config.ts      # Content collection schema definition
│   ├── assets/                # Optimized images (imported in content)
│   ├── styles/                # Custom CSS files
│   ├── components/            # Custom Astro/React/etc. components
│   └── pages/                 # Custom non-Starlight pages (optional)
├── public/                    # Static assets served as-is (favicon, robots.txt)
└── package.json
```

Key rules:
- **`src/content/docs/`** is where ALL documentation pages live. Subdirectories become URL path segments.
- **`src/assets/`** is for images you want Astro to optimize. Reference them in content with `~/assets/image.png`.
- **`public/`** is for files served verbatim (favicon, CNAME, etc.). Reference them with absolute paths like `/favicon.svg`.
- **`src/pages/`** is optional — use it for custom pages that don't follow Starlight's layout.

## 4. astro.config.mjs deep dive {#config}

Full annotated example:

```js
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  // IMPORTANT for subpath deployments:
  site: 'https://example.com',
  // base: '/docs/',  // Uncomment ONLY if hosting at a subpath

  integrations: [
    starlight({
      // REQUIRED — your site's title
      title: 'My Docs',

      // Optional — meta description
      description: 'Documentation for my awesome project',

      // Sidebar configuration (see sidebar-and-content.md for details)
      sidebar: [
        {
          label: 'Guides',
          items: [
            { slug: 'guides/intro' },
            { slug: 'guides/setup' },
          ],
        },
        {
          label: 'Reference',
          autogenerate: { directory: 'reference' },
        },
      ],

      // Social links in the header
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/...' },
      ],

      // Edit page links
      editLink: {
        baseUrl: 'https://github.com/your-org/your-repo/edit/main/',
      },

      // Custom CSS (see styling-and-theming.md)
      customCss: [
        './src/styles/custom.css',
      ],

      // Logo
      logo: {
        src: './src/assets/logo.svg',
        // Or separate dark/light: { light: '...', dark: '...' }
      },

      // Table of contents config
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },

      // Show last updated date (requires git history)
      lastUpdated: true,

      // Pagination (prev/next links)
      pagination: true,

      // Favicon
      favicon: '/favicon.svg',

      // Head tags (analytics, etc.)
      head: [
        {
          tag: 'script',
          attrs: { src: 'https://analytics.example.com/script.js', defer: true },
        },
      ],

      // Search — true by default (Pagefind)
      // Set false to disable, or pass PagefindOptions object
      pagefind: true,

      // Expressive Code (syntax highlighting) config
      expressiveCode: {
        // themes: ['dracula', 'github-light'],
        styleOverrides: { borderRadius: '0.5rem' },
      },

      // Component overrides
      // components: {
      //   SocialLinks: './src/components/MySocialLinks.astro',
      // },

      // Plugins
      // plugins: [myPlugin()],
    }),
  ],
});
```

### Key config properties

| Property | Type | Default | Purpose |
|---|---|---|---|
| `title` | `string` | (required) | Site title in nav bar and metadata |
| `description` | `string` | — | Default meta description |
| `sidebar` | `SidebarItem[]` | auto from filesystem | Navigation structure |
| `customCss` | `string[]` | `[]` | CSS file paths to include |
| `logo` | `LogoConfig` | — | Site logo |
| `social` | `SocialLink[]` | — | Header social icons |
| `editLink` | `{ baseUrl: string }` | — | "Edit this page" links |
| `tableOfContents` | `false \| { min, max }` | `{ min: 2, max: 3 }` | Right-side ToC |
| `lastUpdated` | `boolean` | `false` | Show git-based last updated |
| `pagefind` | `boolean \| PagefindOptions` | `true` | Search configuration |
| `expressiveCode` | `boolean \| object` | `true` | Code block highlighting |
| `head` | `HeadConfig[]` | `[]` | Custom `<head>` tags |
| `locales` | `object` | — | i18n setup |
| `prerender` | `boolean` | `true` | Static vs SSR rendering |
| `components` | `Record<string, string>` | — | Override built-in components |

## 5. Content collections setup {#content-collections}

Starlight requires a content collection for docs. The config file:

```ts
// src/content.config.ts
import { defineCollection } from 'astro:content';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
  // Optional — for multilingual UI translations:
  i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
```

You can extend the schema with custom frontmatter fields:
```ts
import { docsSchema } from '@astrojs/starlight/schema';
import { z } from 'astro:content';

schema: docsSchema({
  extend: z.object({
    category: z.string().optional(),
    difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
  }),
}),
```

## 6. Updating Starlight {#updating}

Use the Astro upgrade tool:
```bash
npx @astrojs/upgrade
```

This updates Starlight and all Astro packages together, handling peer dependency coordination.

Check the changelog for breaking changes: https://github.com/withastro/starlight/blob/main/packages/starlight/CHANGELOG.md
