# Directus TypeScript Patterns

## Table of Contents
1. [Schema Definition](#schema-definition)
2. [Relation Types](#relation-types)
3. [Singleton Collections](#singleton-collections)
4. [Extending Core Collections](#extending-core-collections)
5. [Automatic Type Generation](#automatic-type-generation)
6. [Utility Types & Helpers](#utility-types--helpers)
7. [Typed SDK Requests](#typed-sdk-requests)
8. [Working with JavaScript (Non-TS)](#working-with-javascript-non-ts)

---

## Schema Definition

The SDK's type system revolves around a root schema interface that maps collection names to their item types. This is the single source of truth for all type checking and autocompletion.

```typescript
// src/lib/schema.ts

// Root schema — provided to createDirectus<Schema>()
export interface Schema {
  // Regular collections are ARRAYS
  posts: Post[];
  categories: Category[];
  authors: Author[];
  tags: Tag[];

  // Junction collections (for M2M) are also arrays
  posts_tags: PostTag[];

  // Singletons are SINGULAR types (not arrays)
  global_settings: GlobalSettings;

  // Custom fields on core collections are singular
  directus_users: CustomUser;
}

export interface Post {
  id: number;
  status: 'draft' | 'published' | 'archived';
  title: string;
  slug: string;
  content: string;
  excerpt: string | null;
  cover_image: string | null;           // file UUID
  date_created: string;                  // ISO 8601
  date_updated: string | null;
  // Relations — use union type: foreign key OR populated object
  author: number | Author;
  category: number | Category;
  tags: number[] | PostTag[];
}

export interface Author {
  id: number;
  name: string;
  bio: string | null;
  avatar: string | null;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string | null;
}

export interface Tag {
  id: number;
  name: string;
  slug: string;
}

// Junction table for posts <-> tags (M2M)
export interface PostTag {
  id: number;
  posts_id: number | Post;
  tags_id: number | Tag;
}

export interface GlobalSettings {
  site_title: string;
  description: string;
  logo: string | null;
  social_links: Record<string, string>;
}

// Extend core DirectusUser type
export interface CustomUser {
  department: string;
  phone: string | null;
}
```

### Why Union Types for Relations?

Relational fields return either the raw foreign key (a number or string) or the fully populated object, depending on whether you included that relation in your `fields` query. The union type `number | Author` handles both cases:

```typescript
const post = await client.request(readItem('posts', 1));
// post.author is `number` (just the ID)

const post = await client.request(readItem('posts', 1, {
  fields: ['*', { author: ['name'] }],
}));
// post.author is `Author` (populated object)
```

---

## Relation Types

### Many-to-One (M2O)
A post belongs to one category. The `category` field stores the foreign key.
```typescript
interface Post {
  category: number | Category;
}
```

### One-to-Many (O2M)
A category has many posts. Represented as an array on the "one" side:
```typescript
interface Category {
  id: number;
  name: string;
  posts: number[] | Post[];  // O2M — array of IDs or populated items
}
```

### Many-to-Many (M2M)
Posts and tags, linked through a junction collection:
```typescript
// In the schema root:
export interface Schema {
  posts: Post[];
  tags: Tag[];
  posts_tags: PostTag[];  // junction MUST be listed
}

interface Post {
  tags: number[] | PostTag[];  // references the junction
}

interface PostTag {
  id: number;
  posts_id: number | Post;
  tags_id: number | Tag;
}
```

Fetching M2M data:
```typescript
const posts = await client.request(readItems('posts', {
  fields: ['title', { tags: [{ tags_id: ['name', 'slug'] }] }],
}));

// Access: posts[0].tags[0].tags_id.name
```

### Many-to-Any (M2A)
Used for page builder / block patterns where a field can reference items from multiple collections:
```typescript
interface Page {
  id: number;
  title: string;
  blocks: PageBlock[];
}

interface PageBlock {
  id: number;
  collection: string;          // which collection this block comes from
  item: BlockHero | BlockText | BlockGallery;
  sort: number;
}

interface BlockHero {
  headline: string;
  content: string;
  image: string | null;
}

interface BlockText {
  body: string;
}

interface BlockGallery {
  title: string;
  images: string[];
}
```

---

## Singleton Collections

Singletons store exactly one item — used for global settings, homepage content, etc. Define them as a singular type (not an array) in the schema:

```typescript
export interface Schema {
  global_settings: GlobalSettings;  // singular = singleton
  posts: Post[];                     // array = regular collection
}
```

Read/update singletons with dedicated functions:
```typescript
import { readSingleton, updateSingleton } from '@directus/sdk';

const settings = await client.request(readSingleton('global_settings'));
await client.request(updateSingleton('global_settings', {
  site_title: 'New Title',
}));
```

---

## Extending Core Collections

Directus has built-in system collections (`directus_users`, `directus_files`, etc.). If you add custom fields to these, include them in your schema:

```typescript
export interface Schema {
  // Your custom fields on directus_users (singular type)
  directus_users: CustomUser;
}

interface CustomUser {
  // Only YOUR custom fields go here — Directus provides the rest
  department: string;
  employee_id: string;
  phone: string | null;
}
```

---

## Automatic Type Generation

Rather than writing types by hand, you can generate them from a running Directus instance.

### Using directus-typescript-gen
```bash
npx directus-typescript-gen \
  --host http://localhost:8055 \
  --email admin@example.com \
  --password your-password \
  --outFile src/lib/schema.d.ts
```

This produces a complete schema file matching your current data model.

### Using the Directus CMS Starter's Built-In Script
The official Astro CMS starter includes a type generation script:
```bash
pnpm run generate:types
```
This requires an admin token with permission to read system collections like `directus_fields`.

### Manual Approach via OpenAPI Spec
Export your OpenAPI spec from Directus (`GET /server/specs/oas`) and use it to derive types manually or with tools like `openapi-typescript`.

---

## Utility Types & Helpers

### Extract Item Type from Schema
```typescript
// Get the item type for a collection
type PostItem = Schema['posts'] extends (infer T)[] ? T : never;
// Result: Post
```

### Narrowing Relational Fields
After fetching with populated relations, narrow the type:
```typescript
function isPopulated<T>(value: number | T): value is T {
  return typeof value === 'object' && value !== null;
}

const post = await client.request(readItem('posts', 1, {
  fields: ['*', { author: ['name'] }],
}));

if (isPopulated(post.author)) {
  console.log(post.author.name); // TypeScript knows it's Author
}
```

### Creating Reusable Query Helpers
```typescript
// src/lib/queries.ts
import { readItems, readItem } from '@directus/sdk';
import directus from './directus';

export async function getPublishedPosts(limit = 20) {
  return directus.request(readItems('posts', {
    fields: ['id', 'slug', 'title', 'excerpt', 'date_created', 'cover_image',
      { author: ['name', 'avatar'] }],
    filter: { status: { _eq: 'published' } },
    sort: ['-date_created'],
    limit,
  }));
}

export async function getPostBySlug(slug: string) {
  const results = await directus.request(readItems('posts', {
    fields: ['*', { author: ['name', 'avatar'] }, { tags: [{ tags_id: ['name', 'slug'] }] }],
    filter: { slug: { _eq: slug }, status: { _eq: 'published' } },
    limit: 1,
  }));
  return results[0] ?? null;
}
```

---

## Typed SDK Requests

### Type Inference on Responses
The SDK infers return types based on your schema and the `fields` parameter. When you specify fields, the return type is narrowed:

```typescript
// Returns full Post type
const post = await client.request(readItem('posts', 1));

// Returns only { id: number; title: string }
const post = await client.request(readItem('posts', 1, {
  fields: ['id', 'title'],
}));
```

### Typing Custom Endpoints
When calling custom API endpoints, you can specify the return type:
```typescript
const result = await client.request<{ total: number; average: number }>(() => ({
  path: '/custom/stats',
  method: 'GET',
}));
```

---

## Working with JavaScript (Non-TS)

If you're not using TypeScript, the SDK still works — you just won't get type checking or autocompletion.

### JavaScript Setup
```javascript
// src/lib/directus.js
import { createDirectus, rest, staticToken } from '@directus/sdk';

const directus = createDirectus(process.env.DIRECTUS_URL)
  .with(staticToken(process.env.DIRECTUS_TOKEN))
  .with(rest());

export default directus;
```

### JavaScript CRUD
```javascript
import { readItems, createItem, updateItem, deleteItem } from '@directus/sdk';
import directus from './directus.js';

// Read
const posts = await directus.request(readItems('posts', {
  fields: ['id', 'title'],
  filter: { status: { _eq: 'published' } },
}));

// Create
const newPost = await directus.request(createItem('posts', {
  title: 'New Post',
  content: 'Hello world',
  status: 'draft',
}));

// Update
await directus.request(updateItem('posts', newPost.id, {
  status: 'published',
}));

// Delete
await directus.request(deleteItem('posts', newPost.id));
```

### JSDoc Type Hints (Optional)
You can add type hints in JS files without full TypeScript:
```javascript
/**
 * @typedef {Object} Post
 * @property {number} id
 * @property {string} title
 * @property {string} slug
 * @property {string} content
 * @property {'draft'|'published'|'archived'} status
 */

/** @type {import('@directus/sdk').DirectusClient} */
const directus = createDirectus('https://example.com').with(rest());
```
