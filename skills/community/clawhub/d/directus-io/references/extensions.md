# Directus Extensions

## Table of Contents
1. [Extension Types Overview](#extension-types-overview)
2. [Creating Extensions](#creating-extensions)
3. [Custom Endpoints](#custom-endpoints)
4. [Event Hooks](#event-hooks)
5. [Custom Operations](#custom-operations)
6. [App Extensions (Interfaces, Displays, Layouts, Modules, Panels)](#app-extensions)
7. [Bundles](#bundles)
8. [The Sandbox](#the-sandbox)
9. [Development Workflow](#development-workflow)

---

## Extension Types Overview

| Type | Category | Purpose |
|---|---|---|
| **Endpoints** | API | Register custom REST routes |
| **Hooks** | API | Run code on lifecycle/database events |
| **Operations** | API | Custom operations for use in Flows |
| **Interfaces** | App | Custom form inputs in the editor |
| **Displays** | App | Custom value renderers throughout the Data Studio |
| **Layouts** | App | Custom list/grid views for collection pages |
| **Modules** | App | Custom top-level pages in the Data Studio sidebar |
| **Panels** | App | Custom widgets for Insights dashboards |
| **Themes** | App | Custom visual themes for the Data Studio |
| **Bundles** | Both | Package multiple extensions together |

---

## Creating Extensions

### Scaffold an Extension
```bash
npx create-directus-extension@latest
```

You'll be prompted for:
- Extension type (endpoint, hook, interface, etc.)
- Name
- Language (JavaScript or TypeScript)

This creates a directory with:
```
my-extension/
├── src/
│   └── index.ts (or index.js)
├── package.json
└── tsconfig.json (if TypeScript)
```

### Build and Install
```bash
cd my-extension
npm install
npm run build
```

Copy the built extension to your Directus project's `extensions/` directory. The structure depends on how you're running Directus:

**Docker:**
```yaml
volumes:
  - ./extensions:/directus/extensions
```

**Self-hosted:**
Place in the `extensions/` directory at the root of your Directus project.

### Auto-Reload in Development
Set `EXTENSIONS_AUTO_RELOAD=true` in your Directus `.env` to automatically reload extensions when files change.

---

## Custom Endpoints

Endpoints add new API routes to your Directus instance. They are Express.js route handlers.

### Basic Endpoint
```typescript
// src/index.ts
import { defineEndpoint } from '@directus/extensions-sdk';

export default defineEndpoint((router, context) => {
  const { services, getSchema } = context;

  router.get('/', async (req, res) => {
    res.json({ message: 'Hello from custom endpoint!' });
  });

  router.get('/posts-count', async (req, res, next) => {
    try {
      const { ItemsService } = services;
      const schema = await getSchema();

      const postsService = new ItemsService('posts', {
        schema,
        accountability: req.accountability,
      });

      const posts = await postsService.readByQuery({
        aggregate: { count: '*' },
      });

      res.json({ count: posts[0].count });
    } catch (error) {
      next(error);
    }
  });
});
```

This endpoint is available at `/my-extension/` and `/my-extension/posts-count`.

### Endpoint with Custom ID
```typescript
export default {
  id: 'my-api',
  handler: (router, context) => {
    router.get('/', (req, res) => res.send('Available at /my-api'));
    router.post('/process', async (req, res, next) => {
      try {
        // process req.body
        res.json({ success: true });
      } catch (error) {
        next(error);
      }
    });
  },
};
```

### Context Object
The `context` parameter provides:

| Property | Description |
|---|---|
| `services` | All Directus service classes (ItemsService, FilesService, UsersService, etc.) |
| `getSchema` | Async function returning the current database schema |
| `database` | Knex database instance |
| `env` | Environment variables |
| `logger` | Pino logger instance |
| `emitter` | Event emitter for triggering hooks |

### Error Handling
Always use `next(error)` to pass errors to Directus's error handler:
```typescript
import { createError, ForbiddenError } from '@directus/errors';

const MyError = createError('MY_ERROR', 'Something went wrong.', 400);

router.get('/protected', async (req, res, next) => {
  if (!req.accountability?.user) {
    return next(new ForbiddenError());
  }
  // ...
});
```

---

## Event Hooks

Hooks run code when events occur — database operations, application lifecycle, or schedules.

### Basic Hook
```typescript
import { defineHook } from '@directus/extensions-sdk';

export default defineHook(({ filter, action, init, schedule, embed }) => {
  // FILTER: runs BEFORE event, can modify payload or reject
  filter('items.create', async (payload, meta, context) => {
    // Modify the payload before it's saved
    if (meta.collection === 'posts') {
      payload.slug = payload.title.toLowerCase().replace(/\s+/g, '-');
    }
    return payload;
  });

  // ACTION: runs AFTER event, for side effects
  action('items.create', async (meta, context) => {
    if (meta.collection === 'posts') {
      console.log(`Post created with ID: ${meta.key}`);
    }
  });

  // INIT: runs during Directus startup
  init('app.after', async () => {
    console.log('Directus is ready!');
  });

  // SCHEDULE: runs on a CRON schedule
  schedule('0 * * * *', async () => {
    console.log('Hourly task running...');
  });

  // EMBED: inject HTML into Data Studio
  embed('head', '<style>body { --primary: #ff6600; }</style>');
});
```

### Filter Events
Filters are synchronous and blocking. They can modify data or throw errors:

| Event | Description |
|---|---|
| `items.create` | Before item creation |
| `items.update` | Before item update |
| `items.delete` | Before item deletion |
| `items.query` | Before reading items |
| `<collection>.items.create` | Collection-specific events |
| `request.not_found` | When a route isn't found |
| `request.error` | When a request errors |

```typescript
filter('items.create', async (payload, meta, context) => {
  const { collection, accountability } = meta;
  const { database, schema } = context;

  if (collection === 'posts' && !payload.title) {
    throw new Error('Title is required');
  }

  return payload; // must return the (possibly modified) payload
});
```

### Action Events
Actions are asynchronous and non-blocking:

| Event | Description |
|---|---|
| `items.create` | After item creation |
| `items.update` | After item update |
| `items.delete` | After item deletion |
| `items.sort` | After items are sorted |
| `server.start` | After server starts |
| `server.stop` | Before server stops |
| `auth.login` | After user logs in |
| `auth.logout` | After user logs out |
| `files.upload` | After file upload |

```typescript
action('items.update', async (meta, context) => {
  const { collection, keys, payload } = meta;
  const { services, getSchema } = context;

  if (collection === 'posts' && payload.status === 'published') {
    // Send notification, sync to external service, etc.
    const { MailService } = services;
    const schema = await getSchema();
    const mailService = new MailService({ schema });

    await mailService.send({
      to: 'editor@example.com',
      subject: 'New post published',
      text: `Post ${keys[0]} has been published.`,
    });
  }
});
```

### Important Warnings
- Do NOT emit the same event you're handling inside a hook — this creates infinite loops
- Filter hooks on `items.query` / read events can severely impact performance if they do database reads
- System collections use unprefixed names: `users.create` (not `directus_users.create`)
- The `files` collection does not emit create/update events on file upload — use `files.upload` action instead
- The `collections` and `fields` system collections do not emit read events
- The `relations` collection does not emit delete events

---

## Custom Operations

Operations are custom steps usable within Directus Flows.

### Define an Operation
```typescript
// src/index.ts
import { defineOperationApi, defineOperationApp } from '@directus/extensions-sdk';

// API side — the logic
export const api = defineOperationApi({
  id: 'my-operation',
  handler: async (options, context) => {
    const { text, uppercase } = options;
    const result = uppercase ? text.toUpperCase() : text;
    return { processed: result };
  },
});

// App side — the UI in the Flow editor
export const app = defineOperationApp({
  id: 'my-operation',
  name: 'My Custom Operation',
  icon: 'bolt',
  description: 'Processes text',
  overview: ({ text }) => [
    { label: 'Text', text: text || 'Not configured' },
  ],
  options: [
    {
      field: 'text',
      name: 'Text Input',
      type: 'string',
      meta: { interface: 'input', width: 'full' },
    },
    {
      field: 'uppercase',
      name: 'Uppercase',
      type: 'boolean',
      meta: { interface: 'boolean', width: 'half' },
      schema: { default_value: false },
    },
  ],
});
```

---

## App Extensions

### Interfaces
Custom form inputs used in the item editor.

```typescript
import { defineInterface } from '@directus/extensions-sdk';

export default defineInterface({
  id: 'my-color-picker',
  name: 'Color Picker',
  icon: 'palette',
  description: 'A custom color input',
  component: MyColorPicker,        // Vue component
  types: ['string'],                // Directus field types this works with
  options: [                        // Configuration options
    {
      field: 'presets',
      name: 'Preset Colors',
      type: 'json',
      meta: { interface: 'tags' },
    },
  ],
});
```

### Displays
Render a value anywhere items are shown (tables, cards, etc.).

```typescript
import { defineDisplay } from '@directus/extensions-sdk';

export default defineDisplay({
  id: 'my-badge',
  name: 'Status Badge',
  icon: 'flag',
  description: 'Shows status as a colored badge',
  component: MyBadge,
  types: ['string'],
  options: [],
});
```

### Layouts
Custom views for collection list pages.

### Modules
Top-level pages in the Data Studio navigation sidebar.

### Panels
Dashboard widgets for the Insights module.

---

## Bundles

Bundles package multiple extensions into a single installable unit:

```json
// package.json
{
  "name": "my-directus-bundle",
  "directus:bundle": {
    "entries": [
      { "type": "endpoint", "name": "my-endpoint", "source": "src/endpoint/index.ts" },
      { "type": "hook", "name": "my-hook", "source": "src/hook/index.ts" },
      { "type": "interface", "name": "my-interface", "source": "src/interface/index.ts" }
    ]
  }
}
```

---

## The Sandbox

Directus runs API extensions (hooks, endpoints, operations) inside an isolated VM sandbox for security. This means:

- Extensions can't access the file system directly
- Extensions can't require arbitrary Node.js modules
- Extensions use the `@directus/extensions-sdk` to access services
- The sandbox provides controlled access to the Directus API

If you need to bypass the sandbox (for specific packages or functionality), you can disable it for specific extensions in Directus configuration — but this is not recommended for production.

---

## Development Workflow

### Recommended Setup

1. **Docker Compose** for Directus with mounted `extensions/` volume
2. **Extension development** in a separate directory with `npm run dev` for hot-reloading
3. **`EXTENSIONS_AUTO_RELOAD=true`** in Directus env for auto-detection of changes

### Docker Compose for Extension Dev
```yaml
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
      SECRET: 'change-me'
      ADMIN_EMAIL: 'admin@example.com'
      ADMIN_PASSWORD: 'password'
      DB_CLIENT: 'sqlite3'
      DB_FILENAME: '/directus/database/data.db'
      EXTENSIONS_AUTO_RELOAD: 'true'
```

### Build & Test Loop
```bash
# In your extension directory
npm run build          # Build once
npm run dev            # Watch mode (auto-rebuild on changes)

# Directus auto-reloads the extension if EXTENSIONS_AUTO_RELOAD=true
```

### Debugging
- Use `context.logger.info()` or `context.logger.error()` in API extensions
- Use `console.log` in Run Script operations (visible in server logs)
- Check Docker logs: `docker compose logs -f directus`
- For app extensions, use Vue DevTools in the browser
