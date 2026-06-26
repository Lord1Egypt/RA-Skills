# Content Collections & Data Fetching

## Table of Contents
1. [Content collections overview](#overview)
2. [Defining collections](#defining)
3. [Querying collections](#querying)
4. [Data fetching patterns](#data-fetching)
5. [Dynamic routes with data](#dynamic-routes)
6. [Common problems](#problems)

---

## Content collections overview

Content collections are Astro's system for organizing and validating structured content (blog posts, docs, products, etc.). They live in `src/content/` and use Zod schemas for type safety.

Why use them instead of raw markdown in `/src/pages`:
- Schema validation catches content errors at build time
- TypeScript types are auto-generated from schemas
- Query APIs for filtering, sorting, pagination
- Separates content from presentation

---

## Defining collections

### Directory structure
```
src/content/
├── config.ts          # Schema definitions (REQUIRED)
├── blog/
│   ├── first-post.md
│   ├── second-post.mdx
│   └── third-post.md
├── authors/
│   ├── alice.json
│   └── bob.json
└── products/
    └── widget.yaml
```

### Schema definition
```ts
// src/content/config.ts
import { defineCollection, z, reference } from 'astro:content';

const blog = defineCollection({
  type: 'content', // Markdown/MDX (has a body to render)
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(), // Coerces string to Date
    updatedDate: z.coerce.date().optional(),
    author: reference('authors'), // Reference to another collection
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    image: z.string().optional(),
  }),
});

const authors = defineCollection({
  type: 'data', // JSON/YAML (structured data, no body)
  schema: z.object({
    name: z.string(),
    email: z.string().email(),
    avatar: z.string().url(),
    bio: z.string().optional(),
  }),
});

export const collections = { blog, authors };
```

### Content file format
```md
---
title: "My First Post"
description: "An introduction to Astro"
publishDate: 2024-01-15
author: alice
tags: ["astro", "webdev"]
draft: false
---

# Hello World

This is the body content rendered as HTML.
```

---

## Querying collections

```astro
---
import { getCollection, getEntry } from 'astro:content';

// Get all published posts, sorted by date
const posts = (await getCollection('blog', ({ data }) => {
  return !data.draft; // Filter out drafts
})).sort((a, b) =>
  b.data.publishDate.valueOf() - a.data.publishDate.valueOf()
);

// Get a single entry by slug
const post = await getEntry('blog', 'first-post');

// Resolve a reference
const author = await getEntry(post.data.author);

// Render content to HTML
const { Content, headings } = await post.render();
---

<h1>{post.data.title}</h1>
<p>By {author.data.name}</p>
<Content />
```

### Useful query patterns

**Pagination**:
```astro
---
const allPosts = await getCollection('blog');
const pageSize = 10;
const page = Number(Astro.params.page) || 1;
const totalPages = Math.ceil(allPosts.length / pageSize);
const posts = allPosts.slice((page - 1) * pageSize, page * pageSize);
---
```

**Filter by tag**:
```astro
---
const tag = Astro.params.tag;
const posts = await getCollection('blog', ({ data }) =>
  data.tags.includes(tag)
);
---
```

**Group by year**:
```ts
const postsByYear = posts.reduce((acc, post) => {
  const year = post.data.publishDate.getFullYear();
  (acc[year] ||= []).push(post);
  return acc;
}, {} as Record<number, typeof posts>);
```

---

## Data fetching patterns

### SSG: Fetch at build time

In static mode, all fetching happens during the build. Data is baked into HTML.

```astro
---
// This runs at BUILD TIME, not in the browser
const res = await fetch('https://api.example.com/products');
const products = await res.json();
---

{products.map(p => <ProductCard product={p} />)}
```

**Important**: API rate limits can bite you during builds. If you have 1000 pages each fetching from an API, that's 1000 requests during build.

Mitigations:
- Batch API calls where possible
- Use content collections for local data
- Cache API responses during build (Astro caches `fetch` by default in SSG)

### SSR: Fetch at request time

In SSR mode, fetching happens on every request.

```astro
---
// This runs on EVERY REQUEST
const query = Astro.url.searchParams.get('q') || '';
const res = await fetch(`https://api.example.com/search?q=${query}`);
const results = await res.json();
---

<SearchResults results={results} />
```

### Fetch in API endpoints

```ts
// src/pages/api/products.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ url }) => {
  const category = url.searchParams.get('category');
  const products = await db.getProducts({ category });

  return new Response(JSON.stringify(products), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, s-maxage=120',
    },
  });
};
```

### Client-side fetching from islands

For interactive data loading (search, infinite scroll), fetch from within the island:

```vue
<script setup>
import { ref, onMounted } from 'vue';

const data = ref(null);
const loading = ref(true);

onMounted(async () => {
  const res = await fetch('/api/products');
  data.value = await res.json();
  loading.value = false;
});
</script>
```

---

## Dynamic routes with data

### SSG dynamic routes
Must provide all paths at build time:

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<Layout title={post.data.title}>
  <Content />
</Layout>
```

### SSR dynamic routes
Read params at request time:

```astro
---
// src/pages/blog/[slug].astro (SSR)
import { getEntry } from 'astro:content';

const { slug } = Astro.params;
const post = await getEntry('blog', slug);

if (!post) {
  return Astro.redirect('/404');
}

const { Content } = await post.render();
---
```

### Catch-all routes
```astro
---
// src/pages/[...path].astro
const { path } = Astro.params;
// path = "a/b/c" for URL /a/b/c
---
```

---

## Common problems

### "Collection not found"
- Check that `src/content/config.ts` exists and exports the collection
- Make sure the collection name in `getCollection('name')` matches the folder name
- Run `astro sync` to regenerate types after changing schemas

### Schema validation errors
```
[ERROR] blog/my-post.md: "publishDate" Expected date, received string
```
Fix: Use `z.coerce.date()` instead of `z.date()` for frontmatter dates.

### Content not updating
- Content collections are cached. Restart the dev server after structural changes
- Run `astro sync` after modifying `config.ts`

### Slow builds with large collections
- Avoid fetching external data inside `getStaticPaths()` if possible
- Use pagination to limit pages generated per build
- Consider switching data-heavy pages to SSR

### MDX components not rendering
- Make sure `@astrojs/mdx` is installed and in `astro.config.mjs`
- Import components in the MDX file or pass them via the layout

### Reference resolution
```ts
// Get the referenced entry
const author = await getEntry(post.data.author);
// author.data.name, author.data.email, etc.
```
References only store the collection name and slug. You must call `getEntry()` to resolve them.
