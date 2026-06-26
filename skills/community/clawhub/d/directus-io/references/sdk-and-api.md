# Directus SDK & API Reference

## Table of Contents
1. [SDK Setup & Composables](#sdk-setup--composables)
2. [Authentication](#authentication)
3. [CRUD Operations](#crud-operations)
4. [Filtering, Sorting & Pagination](#filtering-sorting--pagination)
5. [Relational Data & Fields](#relational-data--fields)
6. [File Management](#file-management)
7. [Real-Time Subscriptions](#real-time-subscriptions)
8. [GraphQL Usage](#graphql-usage)
9. [Raw REST API](#raw-rest-api)

---

## SDK Setup & Composables

The Directus SDK (`@directus/sdk`) uses a composable architecture. The client starts empty and gains features through `.with()`:

```bash
npm install @directus/sdk
```

### Available Composables

| Composable | Purpose |
|---|---|
| `rest()` | Enables REST API requests via `client.request()` |
| `graphql()` | Enables GraphQL queries via `client.query()` |
| `authentication(mode)` | Manages login/logout/refresh. Modes: `'json'`, `'session'`, `'cookie'` |
| `staticToken(token)` | Sets a fixed access token for all requests |
| `realtime(options)` | Enables WebSocket subscriptions |

### Client Creation Patterns

**Public (no auth):**
```typescript
import { createDirectus, rest } from '@directus/sdk';

const client = createDirectus<Schema>('https://directus.example.com')
  .with(rest());
```

**Static token (API key):**
```typescript
import { createDirectus, rest, staticToken } from '@directus/sdk';

const client = createDirectus<Schema>('https://directus.example.com')
  .with(staticToken('my-api-token'))
  .with(rest());
```

**Session-based auth (for SSR apps like Astro in server mode):**
```typescript
import { createDirectus, rest, authentication } from '@directus/sdk';

const client = createDirectus<Schema>('https://directus.example.com')
  .with(authentication('cookie'))
  .with(rest());
```

**JSON auth (for SPAs):**
```typescript
import { createDirectus, rest, authentication } from '@directus/sdk';

const client = createDirectus<Schema>('https://directus.example.com')
  .with(authentication('json'))
  .with(rest());
```

### Per-Request Token Override
```typescript
import { withToken, readItems } from '@directus/sdk';

const result = await client.request(
  withToken('temporary-token', readItems('posts'))
);
```

---

## Authentication

### Login / Logout / Refresh
```typescript
// Login (requires authentication() composable)
await client.login('email@example.com', 'password');

// Refresh tokens
await client.refresh();

// Logout
await client.logout();

// Get current user
import { readMe } from '@directus/sdk';
const me = await client.request(readMe());
```

### Generate Static Token
In the Directus Data Studio: Users → select user → Token field → Generate → Save. Use this token with `staticToken()` or in API headers as `Authorization: Bearer <token>`.

### SSO / External Auth
Directus supports OAuth2, OpenID Connect, LDAP, and SAML. Configure via environment variables:
```env
AUTH_PROVIDERS="google"
AUTH_GOOGLE_DRIVER="openid"
AUTH_GOOGLE_CLIENT_ID="your-client-id"
AUTH_GOOGLE_CLIENT_SECRET="your-client-secret"
AUTH_GOOGLE_ISSUER_URL="https://accounts.google.com/.well-known/openid-configuration"
AUTH_GOOGLE_REDIRECT_ALLOW_LIST="http://localhost:3000/auth/callback"
```

---

## CRUD Operations

All operations use `client.request(operationFunction())`.

### Create
```typescript
import { createItem, createItems } from '@directus/sdk';

// Single item
const newPost = await client.request(createItem('posts', {
  title: 'Hello World',
  content: '<p>My first post</p>',
  status: 'published',
}));

// Multiple items
const newPosts = await client.request(createItems('posts', [
  { title: 'Post A', status: 'draft' },
  { title: 'Post B', status: 'draft' },
]));
```

### Read
```typescript
import { readItems, readItem, readSingleton } from '@directus/sdk';

// All items (with query)
const posts = await client.request(readItems('posts', {
  fields: ['id', 'title', 'status'],
  filter: { status: { _eq: 'published' } },
  sort: ['-date_created'],
  limit: 10,
}));

// Single item by ID
const post = await client.request(readItem('posts', 42));

// Singleton collection (e.g., global settings)
const settings = await client.request(readSingleton('global'));
```

### Update
```typescript
import { updateItem, updateItems, updateSingleton } from '@directus/sdk';

// Single item
await client.request(updateItem('posts', 42, {
  title: 'Updated Title',
}));

// Multiple items by query
await client.request(updateItems('posts', {
  filter: { status: { _eq: 'draft' } },
  limit: -1,
}, {
  status: 'archived',
}));

// Singleton
await client.request(updateSingleton('global', {
  site_title: 'New Site Title',
}));
```

### Delete
```typescript
import { deleteItem, deleteItems } from '@directus/sdk';

// Single
await client.request(deleteItem('posts', 42));

// Multiple
await client.request(deleteItems('posts', [1, 2, 3]));
```

---

## Filtering, Sorting & Pagination

### Filter Operators

| Operator | Meaning |
|---|---|
| `_eq` | Equals |
| `_neq` | Not equals |
| `_gt`, `_gte` | Greater than (or equal) |
| `_lt`, `_lte` | Less than (or equal) |
| `_in` | In array |
| `_nin` | Not in array |
| `_contains` | String contains (case-sensitive) |
| `_icontains` | String contains (case-insensitive) |
| `_starts_with` | String starts with |
| `_ends_with` | String ends with |
| `_null` | Is null |
| `_nnull` | Is not null |
| `_between` | Between two values |
| `_empty` | Is empty (null or '') |
| `_nempty` | Is not empty |

### Compound Filters
```typescript
const results = await client.request(readItems('posts', {
  filter: {
    _and: [
      { status: { _eq: 'published' } },
      {
        _or: [
          { category: { _eq: 'news' } },
          { featured: { _eq: true } },
        ],
      },
    ],
  },
}));
```

### Filtering Relational Fields
```typescript
const results = await client.request(readItems('posts', {
  filter: {
    author: {
      name: { _eq: 'John' },
    },
  },
}));
```

### Sorting
```typescript
// Ascending
const sorted = await client.request(readItems('posts', {
  sort: ['title'],
}));

// Descending (prefix with -)
const sortedDesc = await client.request(readItems('posts', {
  sort: ['-date_created'],
}));

// Multiple sort fields
const multiSort = await client.request(readItems('posts', {
  sort: ['-featured', 'title'],
}));
```

### Pagination
```typescript
// Offset-based
const page2 = await client.request(readItems('posts', {
  limit: 10,
  offset: 10,
}));

// Get total count with items
const withCount = await client.request(readItems('posts', {
  limit: 10,
  offset: 0,
  meta: ['total_count', 'filter_count'],
}));
```

### Search
```typescript
const results = await client.request(readItems('posts', {
  search: 'keyword',
}));
```

---

## Relational Data & Fields

### Selecting Specific Fields
```typescript
// Flat fields
const posts = await client.request(readItems('posts', {
  fields: ['id', 'title'],
}));

// Wildcard (all top-level fields)
const posts = await client.request(readItems('posts', {
  fields: ['*'],
}));

// Nested relational fields
const posts = await client.request(readItems('posts', {
  fields: ['id', 'title', { author: ['name', 'avatar'] }],
}));

// Deep nested
const posts = await client.request(readItems('posts', {
  fields: [
    'id',
    'title',
    { author: ['name', { role: ['name'] }] },
    { tags: [{ tags_id: ['name', 'slug'] }] },
  ],
}));
```

### Aggregation
```typescript
import { aggregate } from '@directus/sdk';

const stats = await client.request(aggregate('posts', {
  aggregate: { count: '*' },
  groupBy: ['status'],
}));
```

---

## File Management

### Upload a File
```typescript
import { uploadFiles } from '@directus/sdk';

const formData = new FormData();
formData.append('file', fileBlob, 'photo.jpg');

const result = await client.request(uploadFiles(formData));
```

### Import a File by URL
```typescript
import { importFile } from '@directus/sdk';

const result = await client.request(importFile('https://example.com/photo.jpg'));
```

### Access File URLs
Files are served at: `{DIRECTUS_URL}/assets/{file-id}`

**Transformations via query params:**
```
/assets/{id}?width=300&height=200&fit=cover&format=webp&quality=80
```

| Param | Values |
|---|---|
| `width` | Pixel width |
| `height` | Pixel height |
| `fit` | `cover`, `contain`, `inside`, `outside` |
| `format` | `jpg`, `png`, `webp`, `avif`, `tiff` |
| `quality` | 1–100 |
| `withoutEnlargement` | `true` to prevent upscaling |

---

## Real-Time Subscriptions

Requires `WEBSOCKETS_ENABLED=true` in Directus config.

```typescript
import { createDirectus, realtime, authentication } from '@directus/sdk';

const client = createDirectus<Schema>('https://directus.example.com')
  .with(authentication())
  .with(realtime());

await client.connect();
await client.login('email@example.com', 'password');

// Subscribe to collection changes
const { subscription, unsubscribe } = await client.subscribe('posts', {
  query: { fields: ['id', 'title', 'status'] },
});

for await (const message of subscription) {
  console.log('Change:', message);
}
```

### Real-Time with Public Access
```typescript
const client = createDirectus<Schema>('https://directus.example.com')
  .with(realtime({ authMode: 'public' }));

await client.connect();
```

---

## GraphQL Usage

```typescript
import { createDirectus, graphql } from '@directus/sdk';

const client = createDirectus<Schema>('https://directus.example.com')
  .with(graphql());

const result = await client.query<{ posts: Post[] }>(`
  query {
    posts(filter: { status: { _eq: "published" } }) {
      id
      title
      content
    }
  }
`);
```

GraphQL endpoints:
- User collections: `POST /graphql`
- System collections: `POST /graphql/system`

---

## Raw REST API

When the SDK doesn't cover your use case, make custom requests:

```typescript
const result = await client.request(() => ({
  path: '/custom/my-endpoint',
  method: 'GET',
}));

// With body
const result = await client.request(() => ({
  path: '/custom/my-endpoint',
  method: 'POST',
  body: JSON.stringify({ key: 'value' }),
  headers: { 'Content-Type': 'application/json' },
}));
```

### REST Endpoints Reference

| Resource | Endpoint |
|---|---|
| Items | `GET/POST/PATCH/DELETE /items/{collection}` |
| Single Item | `GET/PATCH/DELETE /items/{collection}/{id}` |
| Singleton | `GET/PATCH /items/{collection}` |
| Files | `GET/POST /files` |
| Assets | `GET /assets/{id}` |
| Users | `GET/POST/PATCH/DELETE /users` |
| Auth | `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout` |
| Flows | `GET/POST/PATCH/DELETE /flows` |
| Activity | `GET /activity` |
| Schema | `GET /schema/snapshot`, `POST /schema/diff`, `POST /schema/apply` |
