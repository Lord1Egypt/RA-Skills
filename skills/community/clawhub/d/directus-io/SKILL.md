---
name: directus_io
description: Use this skill for anything involving Directus — the open-source headless CMS and backend-as-a-service. Triggers include setting up Directus (Docker, Cloud, self-hosted), using the Directus JavaScript/TypeScript SDK, integrating Directus with frontend frameworks (especially Astro, but also Next.js, Nuxt, SvelteKit), building Directus Flows and automations, generating content with AI via Directus Automate, building custom extensions (hooks, endpoints, interfaces, layouts, modules, operations), data modeling and collections, access control and permissions, file management, real-time subscriptions, REST and GraphQL API usage, troubleshooting Directus errors, and any mention of 'Directus', 'directus.io', '@directus/sdk', 'Directus Cloud', 'Directus Flows', 'Directus Automate', or 'Data Studio'. Also trigger when users mention headless CMS integration with Astro/TypeScript and Directus is a likely fit, or when they ask about CMS-powered content pipelines, dynamic page generation from a CMS, or automating content workflows with a headless backend.
---

# Directus Skill

Directus is an open-source headless CMS and backend-as-a-service that wraps any SQL database with instant REST and GraphQL APIs, plus a no-code Data Studio for content management. It's built with Node.js and Vue.js, supports PostgreSQL, MySQL, SQLite, MariaDB, MS-SQL, OracleDB, and CockroachDB, and is fully extensible.

## How to Use This Skill

This skill is organized into focused reference files. Read the relevant reference before answering:

| Topic | Reference File | When to Read |
|---|---|---|
| **SDK & API Basics** | `references/sdk-and-api.md` | Any question about the JS/TS SDK, REST API, GraphQL, authentication, CRUD operations, filtering, or real-time subscriptions |
| **Astro Integration** | `references/astro-integration.md` | Integrating Directus with Astro — fetching data, dynamic routes, SSG/SSR, live preview, authentication, visual editing |
| **TypeScript Patterns** | `references/typescript-patterns.md` | Schema typing, type generation, advanced generics, type-safe SDK usage |
| **Flows & Automation** | `references/flows-and-automation.md` | Directus Flows, triggers, operations, scheduled tasks, AI content generation, webhook integrations |
| **Extensions** | `references/extensions.md` | Custom endpoints, hooks, interfaces, layouts, displays, modules, operations, panels, themes |
| **Data Modeling & Admin** | `references/data-modeling.md` | Collections, fields, relations (M2O, O2M, M2M, M2A), singletons, permissions, roles, file management, environment config |
| **Troubleshooting** | `references/troubleshooting.md` | Common errors, debugging, CORS issues, Docker problems, migration headaches, performance tips |

**Always read the relevant reference file before generating code or instructions.** For complex questions spanning multiple topics, read multiple references.

## Quick-Reference Essentials

These are the most common patterns you'll need. For anything beyond these basics, consult the reference files.

### Install the SDK
```bash
npm install @directus/sdk
```

### Create a Client (TypeScript)
```typescript
import { createDirectus, rest, staticToken } from '@directus/sdk';

// Define your schema for type safety
interface MySchema {
  posts: Post[];
  categories: Category[];
  global: GlobalSettings; // singleton (not an array)
}

interface Post {
  id: number;
  title: string;
  content: string;
  status: string;
  category: number | Category;
}

interface Category {
  id: number;
  name: string;
}

interface GlobalSettings {
  site_title: string;
  description: string;
}

const client = createDirectus<MySchema>('https://your-directus-url.com')
  .with(staticToken('your-token'))
  .with(rest());
```

### Read Items
```typescript
import { readItems, readItem, readSingleton } from '@directus/sdk';

// Get all posts
const posts = await client.request(readItems('posts'));

// Get one post with relational data
const post = await client.request(readItem('posts', 1, {
  fields: ['*', { category: ['name'] }],
}));

// Get singleton
const global = await client.request(readSingleton('global'));
```

### Astro Quick Setup
```typescript
// src/lib/directus.ts
import { createDirectus, rest } from '@directus/sdk';
const directus = createDirectus(import.meta.env.DIRECTUS_URL).with(rest());
export default directus;
```

### Docker Quick Start
```yaml
# docker-compose.yml
services:
  directus:
    image: directus/directus:latest
    ports:
      - 8055:8055
    volumes:
      - ./database:/directus/database
      - ./uploads:/directus/uploads
      - ./extensions:/directus/extensions
    environment:
      SECRET: 'your-random-secret'
      ADMIN_EMAIL: 'admin@example.com'
      ADMIN_PASSWORD: 'your-password'
      DB_CLIENT: 'sqlite3'
      DB_FILENAME: '/directus/database/data.db'
      WEBSOCKETS_ENABLED: 'true'
```

## Key Concepts to Remember

- **Composable Client**: The SDK client starts empty — you add features with `.with(rest())`, `.with(authentication())`, `.with(realtime())`, `.with(staticToken())`.
- **Schema Typing**: Always define a TypeScript schema interface for type-safe SDK usage. Regular collections are arrays, singletons are singular types.
- **Access Policies**: New collections are private by default. You must configure public read access or use authentication tokens.
- **Directus Assets**: Images/files are served at `{DIRECTUS_URL}/assets/{file-id}` with optional transformation query params like `?width=500&format=webp`.
- **Flows vs Extensions**: Flows are no-code automations configured in the Data Studio. Extensions are code-based additions (hooks, endpoints, etc.) that extend Directus itself.
- **Environment Variables**: Directus is heavily configured via env vars — `DB_CLIENT`, `SECRET`, `CORS_ENABLED`, `AUTH_PROVIDERS`, etc.
