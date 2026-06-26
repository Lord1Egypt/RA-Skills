# Directus + Astro Integration Guide

## Table of Contents
1. [Project Setup](#project-setup)
2. [Directus Client Configuration](#directus-client-configuration)
3. [Fetching & Displaying Data](#fetching--displaying-data)
4. [Dynamic Routes & Pages](#dynamic-routes--pages)
5. [Blog with Relational Data](#blog-with-relational-data)
6. [Images & Assets](#images--assets)
7. [Live Preview](#live-preview)
8. [Authentication in Astro](#authentication-in-astro)
9. [SSR vs SSG Considerations](#ssr-vs-ssg-considerations)
10. [Dynamic Blocks / Page Builder](#dynamic-blocks--page-builder)
11. [Real-Time with Astro](#real-time-with-astro)
12. [Multilingual Content](#multilingual-content)
13. [Deployment & Build Hooks](#deployment--build-hooks)

---

## Project Setup

### Create Astro Project
```bash
npm create astro@latest my-site
cd my-site
npm install @directus/sdk
```

### Environment Variables
Create `.env` in the project root:
```env
DIRECTUS_URL=https://your-directus-project.directus.app
DIRECTUS_TOKEN=your-static-token
```

For TypeScript projects, add types in `src/env.d.ts`:
```typescript
/// <reference types="astro/client" />
interface ImportMetaEnv {
  readonly DIRECTUS_URL: string;
  readonly DIRECTUS_TOKEN: string;
}
```

---

## Directus Client Configuration

Create `src/lib/directus.ts`:

### Public-Only Access (SSG)
```typescript
import { createDirectus, rest } from '@directus/sdk';

// Import your schema types
import type { Schema } from './schema';

const directus = createDirectus<Schema>(import.meta.env.DIRECTUS_URL)
  .with(rest());

export default directus;
```

### Token-Based Access (SSG/SSR)
```typescript
import { createDirectus, rest, staticToken } from '@directus/sdk';
import type { Schema } from './schema';

const directus = createDirectus<Schema>(import.meta.env.DIRECTUS_URL)
  .with(staticToken(import.meta.env.DIRECTUS_TOKEN))
  .with(rest());

export default directus;
```

### Authenticated Access (SSR Only)
```typescript
import { createDirectus, rest, authentication } from '@directus/sdk';
import type { Schema } from './schema';

const directus = createDirectus<Schema>(import.meta.env.DIRECTUS_URL)
  .with(authentication('cookie'))
  .with(rest());

export default directus;
```

---

## Fetching & Displaying Data

### Basic Page with Singleton Data
```astro
---
// src/pages/index.astro
import Layout from '../layouts/Layout.astro';
import directus from '../lib/directus';
import { readSingleton } from '@directus/sdk';

const global = await directus.request(readSingleton('global'));
---

<Layout title={global.site_title}>
  <h1>{global.site_title}</h1>
  <p>{global.description}</p>
</Layout>
```

### List Page
```astro
---
// src/pages/blog/index.astro
import Layout from '../../layouts/Layout.astro';
import directus from '../../lib/directus';
import { readItems } from '@directus/sdk';

const posts = await directus.request(readItems('posts', {
  fields: ['id', 'slug', 'title', 'excerpt', 'date_created', 'cover_image'],
  filter: { status: { _eq: 'published' } },
  sort: ['-date_created'],
  limit: 20,
}));
---

<Layout title="Blog">
  <h1>Blog</h1>
  <ul>
    {posts.map((post) => (
      <li>
        <a href={`/blog/${post.slug}`}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
          <time>{new Date(post.date_created).toLocaleDateString()}</time>
        </a>
      </li>
    ))}
  </ul>
</Layout>
```

---

## Dynamic Routes & Pages

### Static Generation (SSG) — `[slug].astro`
```astro
---
// src/pages/[slug].astro
import Layout from '../layouts/Layout.astro';
import directus from '../lib/directus';
import { readItems } from '@directus/sdk';

export async function getStaticPaths() {
  const pages = await directus.request(readItems('pages', {
    fields: ['slug', 'title', 'content'],
    filter: { status: { _eq: 'published' } },
  }));

  return pages.map((page) => ({
    params: { slug: page.slug },
    props: page,
  }));
}

const page = Astro.props;
---

<Layout title={page.title}>
  <h1>{page.title}</h1>
  <div set:html={page.content} />
</Layout>
```

### Blog Post with Relational Author
```astro
---
// src/pages/blog/[slug].astro
import Layout from '../../layouts/Layout.astro';
import directus from '../../lib/directus';
import { readItems } from '@directus/sdk';

export async function getStaticPaths() {
  const posts = await directus.request(readItems('posts', {
    fields: [
      'slug', 'title', 'content', 'date_created', 'cover_image',
      { author: ['name', 'avatar'] },
    ],
    filter: { status: { _eq: 'published' } },
  }));

  return posts.map((post) => ({
    params: { slug: post.slug },
    props: post,
  }));
}

const post = Astro.props;
const DIRECTUS_URL = import.meta.env.DIRECTUS_URL;
---

<Layout title={post.title}>
  {post.cover_image && (
    <img
      src={`${DIRECTUS_URL}/assets/${post.cover_image}?width=1200&format=webp`}
      alt={post.title}
    />
  )}
  <h1>{post.title}</h1>
  {typeof post.author === 'object' && post.author && (
    <p>By {post.author.name}</p>
  )}
  <time>{new Date(post.date_created).toLocaleDateString()}</time>
  <article set:html={post.content} />
</Layout>
```

### SSR Dynamic Route (No getStaticPaths)
For SSR mode (`output: 'server'` in astro.config), you don't need `getStaticPaths`:
```astro
---
// src/pages/blog/[slug].astro (SSR mode)
import directus from '../../lib/directus';
import { readItems } from '@directus/sdk';

const { slug } = Astro.params;

const posts = await directus.request(readItems('posts', {
  fields: ['*', { author: ['name'] }],
  filter: { slug: { _eq: slug }, status: { _eq: 'published' } },
  limit: 1,
}));

if (!posts.length) return Astro.redirect('/404');
const post = posts[0];
---
```

---

## Blog with Relational Data

### Many-to-Many Tags
Directus M2M relations use a junction collection (e.g., `posts_tags`).

```astro
---
const posts = await directus.request(readItems('posts', {
  fields: [
    'id', 'title', 'slug',
    { tags: [{ tags_id: ['name', 'slug'] }] },
  ],
  filter: { status: { _eq: 'published' } },
}));
---

{posts.map((post) => (
  <article>
    <h2>{post.title}</h2>
    <div class="tags">
      {post.tags?.map((junction) => (
        <span>{junction.tags_id.name}</span>
      ))}
    </div>
  </article>
))}
```

### Filter by Tag
```astro
---
// src/pages/tags/[tag].astro
export async function getStaticPaths() {
  const tags = await directus.request(readItems('tags', {
    fields: ['slug', 'name'],
  }));

  return tags.map((tag) => ({
    params: { tag: tag.slug },
    props: { tag },
  }));
}

const { tag } = Astro.props;

const posts = await directus.request(readItems('posts', {
  fields: ['slug', 'title'],
  filter: {
    tags: {
      tags_id: { slug: { _eq: tag.slug } },
    },
  },
}));
---
```

---

## Images & Assets

### Rendering Directus Images
```astro
---
const DIRECTUS_URL = import.meta.env.DIRECTUS_URL;
---

<!-- Basic image -->
<img src={`${DIRECTUS_URL}/assets/${imageId}`} alt="Description" />

<!-- With transformations -->
<img
  src={`${DIRECTUS_URL}/assets/${imageId}?width=800&height=450&fit=cover&format=webp&quality=80`}
  alt="Description"
  width="800"
  height="450"
  loading="lazy"
/>
```

### Responsive Image Helper
```typescript
// src/lib/image.ts
const DIRECTUS_URL = import.meta.env.DIRECTUS_URL;

export function getImageUrl(
  id: string,
  options?: { width?: number; height?: number; fit?: string; format?: string; quality?: number }
) {
  const params = new URLSearchParams();
  if (options?.width) params.set('width', String(options.width));
  if (options?.height) params.set('height', String(options.height));
  if (options?.fit) params.set('fit', options.fit);
  if (options?.format) params.set('format', options.format);
  if (options?.quality) params.set('quality', String(options.quality));

  const query = params.toString();
  return `${DIRECTUS_URL}/assets/${id}${query ? `?${query}` : ''}`;
}
```

---

## Live Preview

### Directus Config
In Settings → Data Model → your collection, enable Live Preview with URL pattern:
```
http://localhost:4321/{slug}?preview=true
```

### Astro Config (requires SSR)
```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'server',
});
```

### Preview-Aware Page
```astro
---
// src/pages/blog/[slug].astro
import directus from '../../lib/directus';
import { readItems, withToken } from '@directus/sdk';

const { slug } = Astro.params;
const preview = Astro.url.searchParams.get('preview') === 'true';
const token = Astro.url.searchParams.get('token');

let filter: any = {
  slug: { _eq: slug },
};

// In preview mode, don't filter by status
if (!preview) {
  filter.status = { _eq: 'published' };
}

let request = readItems('posts', {
  fields: ['*'],
  filter,
  limit: 1,
});

// Use token for draft content access
const posts = token
  ? await directus.request(withToken(token, request))
  : await directus.request(request);

if (!posts.length) return Astro.redirect('/404');
const post = posts[0];
---
```

### Visual Editing Support
Install the visual editing library for real-time field editing:
```bash
npm install @directus/visual-editing
```

---

## Authentication in Astro

### SSR Login Flow
```astro
---
// src/pages/login.astro
import directus from '../lib/directus';

if (Astro.request.method === 'POST') {
  const formData = await Astro.request.formData();
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;

  try {
    const result = await directus.login(email, password);
    // Store tokens in cookies
    Astro.cookies.set('access_token', result.access_token, {
      httpOnly: true,
      secure: true,
      path: '/',
      maxAge: 60 * 15, // 15 minutes
    });
    Astro.cookies.set('refresh_token', result.refresh_token, {
      httpOnly: true,
      secure: true,
      path: '/',
      maxAge: 60 * 60 * 24 * 7, // 7 days
    });
    return Astro.redirect('/dashboard');
  } catch (e) {
    // handle error
  }
}
---

<form method="POST">
  <input type="email" name="email" required />
  <input type="password" name="password" required />
  <button type="submit">Login</button>
</form>
```

### Protected Routes via Middleware
```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';
import { createDirectus, rest, withToken, readMe } from '@directus/sdk';

export const onRequest = defineMiddleware(async (context, next) => {
  const protectedPaths = ['/dashboard', '/profile'];
  const isProtected = protectedPaths.some(p => context.url.pathname.startsWith(p));

  if (!isProtected) return next();

  const token = context.cookies.get('access_token')?.value;
  if (!token) return context.redirect('/login');

  try {
    const client = createDirectus(import.meta.env.DIRECTUS_URL).with(rest());
    const user = await client.request(withToken(token, readMe()));
    context.locals.user = user;
    return next();
  } catch {
    return context.redirect('/login');
  }
});
```

---

## SSR vs SSG Considerations

| Feature | SSG (Static) | SSR (Server) |
|---|---|---|
| Config | `output: 'static'` (default) | `output: 'server'` |
| Data freshness | Build-time only | Every request |
| Dynamic routes | Requires `getStaticPaths()` | Uses `Astro.params` directly |
| Auth / login flows | Not supported | Supported |
| Live preview | Not supported | Supported |
| Hosting | Any static host | Node.js server, serverless, or edge |
| Build hooks | Rebuild on content change | Not needed |

### Hybrid Mode
Astro supports `output: 'hybrid'` where pages default to static but individual pages can opt into SSR:
```astro
---
// This specific page renders on the server
export const prerender = false;
---
```

---

## Dynamic Blocks / Page Builder

Directus Many-to-Any (M2A) relationships enable page-builder patterns where pages contain ordered blocks of different types.

### Data Model
- Collection `pages`: slug, title
- Collection `block_hero`: headline, content, image, buttons (JSON)
- Collection `block_richtext`: content (WYSIWYG)
- Collection `block_gallery`: title, images (M2M to directus_files)
- Junction: `pages_blocks` (M2A linking pages → various block collections)

### Astro Implementation
```astro
---
// src/pages/[slug].astro
import directus from '../lib/directus';
import { readItems } from '@directus/sdk';
import Hero from '../components/blocks/Hero.astro';
import RichText from '../components/blocks/RichText.astro';
import Gallery from '../components/blocks/Gallery.astro';

export async function getStaticPaths() {
  const pages = await directus.request(readItems('pages', {
    fields: [
      'slug', 'title',
      {
        blocks: [
          'id', 'collection', 'sort',
          { item: { block_hero: ['headline', 'content', 'image', 'buttons'] } },
          { item: { block_richtext: ['content'] } },
          { item: { block_gallery: ['title', { images: [{ directus_files_id: ['id', 'title'] }] }] } },
        ],
      },
    ],
  }));

  return pages.map((page) => ({
    params: { slug: page.slug },
    props: page,
  }));
}

const page = Astro.props;

const blockComponents: Record<string, any> = {
  block_hero: Hero,
  block_richtext: RichText,
  block_gallery: Gallery,
};
---

<h1>{page.title}</h1>
{page.blocks
  ?.sort((a, b) => a.sort - b.sort)
  .map((block) => {
    const Component = blockComponents[block.collection];
    return Component ? <Component item={block.item} /> : null;
  })}
```

---

## Real-Time with Astro

Real-time features require client-side JavaScript. Use an Astro island:

```astro
---
// src/pages/live.astro
import LiveFeed from '../components/LiveFeed';
---

<LiveFeed client:only="react" />
```

```tsx
// src/components/LiveFeed.tsx (React island)
import { useEffect, useState } from 'react';
import { createDirectus, realtime } from '@directus/sdk';

export default function LiveFeed() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const client = createDirectus('https://directus.example.com')
      .with(realtime({ authMode: 'public' }));

    async function connect() {
      await client.connect();
      const { subscription } = await client.subscribe('messages', {
        query: { fields: ['id', 'text', 'date_created'] },
      });

      for await (const msg of subscription) {
        if (msg.event !== 'init') {
          setMessages(prev => [...prev, ...msg.data]);
        }
      }
    }

    connect();
  }, []);

  return (
    <ul>
      {messages.map((m) => <li key={m.id}>{m.text}</li>)}
    </ul>
  );
}
```

---

## Multilingual Content

Directus handles translations via a translations interface that creates a junction collection.

### Fetching Translated Content
```astro
---
const posts = await directus.request(readItems('posts', {
  fields: ['id', 'slug', { translations: ['title', 'content', 'languages_code'] }],
  deep: {
    translations: {
      _filter: { languages_code: { _eq: 'en-US' } },
    },
  },
}));
---

{posts.map((post) => {
  const t = post.translations?.[0];
  return t ? <h2>{t.title}</h2> : null;
})}
```

---

## Deployment & Build Hooks

### Triggering Astro Rebuilds on Content Change
Use Directus Flows to send a webhook when content is published:

1. Create a Flow with an Event Hook trigger on `items.create` / `items.update` for your content collections
2. Add a Condition operation to check `{{ $trigger.payload.status }}` equals `published`
3. Add a Web Request operation to POST to your hosting provider's deploy hook:
   - **Netlify**: `https://api.netlify.com/build_hooks/{hook-id}`
   - **Vercel**: `https://api.vercel.com/v1/integrations/deploy/{hook-id}`
   - **Cloudflare Pages**: Use their deploy hook URL

### CORS Configuration
If your Astro frontend and Directus backend are on different domains, configure CORS in Directus:
```env
CORS_ENABLED=true
CORS_ORIGIN=https://your-astro-site.com
CORS_METHODS=GET,POST,PATCH,DELETE
CORS_ALLOWED_HEADERS=Content-Type,Authorization
```

For local development:
```env
CORS_ENABLED=true
CORS_ORIGIN=http://localhost:4321
```
