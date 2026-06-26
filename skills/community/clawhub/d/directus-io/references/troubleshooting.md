# Directus Troubleshooting

## Table of Contents
1. [Installation & Startup Issues](#installation--startup-issues)
2. [Authentication & Token Errors](#authentication--token-errors)
3. [CORS & Network Errors](#cors--network-errors)
4. [SDK Errors](#sdk-errors)
5. [Docker Issues](#docker-issues)
6. [Database Issues](#database-issues)
7. [File Upload & Asset Issues](#file-upload--asset-issues)
8. [Extension Issues](#extension-issues)
9. [Performance Issues](#performance-issues)
10. [Migration & Upgrade Issues](#migration--upgrade-issues)
11. [Flow & Automation Issues](#flow--automation-issues)
12. [Framework Integration Issues](#framework-integration-issues)

---

## Installation & Startup Issues

### "SECRET must be set" Error
Directus requires a `SECRET` environment variable for encryption.
```env
SECRET="a-random-string-at-least-32-characters-long"
```
Generate one: `openssl rand -hex 32`

### "Port 8055 already in use"
Another process is using the port. Either stop it or change Directus's port:
```env
PORT=8056
```

### Directus Hangs on Startup
Common causes:
- Database connection failing — verify `DB_HOST`, `DB_PORT`, credentials
- Redis connection failing (if cache enabled) — verify `CACHE_REDIS` URL
- For Docker: ensure database service is healthy before Directus starts (use `depends_on` with health checks)

### "Cannot find module" Errors
After upgrading Directus or Node.js:
```bash
rm -rf node_modules
npm install
```

For Docker, pull the latest image:
```bash
docker compose pull
docker compose up -d
```

---

## Authentication & Token Errors

### "Invalid token" Error
Causes and fixes:
- **Token expired**: Access tokens have a short TTL. Refresh with `await client.refresh()` or re-login
- **Token not saved**: After generating a static token in the Data Studio, you MUST click Save on the user profile
- **Wrong token type**: Static tokens go in `staticToken()`, login tokens are managed by `authentication()`
- **SECRET changed**: If you change the `SECRET` env var, all existing tokens are invalidated

### "Forbidden" / 403 Error
The authenticated user (or Public role) doesn't have permission for the requested action.

Checklist:
1. Check **Settings → Access Policies** for the relevant role
2. Verify the collection has the needed CRUD permissions
3. Check for item-level permission rules that might filter out the item
4. If using the Public role, ensure read access is explicitly granted
5. For file access, ensure the Public role has read access to `directus_files`

### Login Returns "Invalid credentials"
- Verify email and password
- Check if the user exists and is active (not suspended)
- External auth provider users cannot use email/password login — they must use their provider's flow
- The `requestPasswordReset` endpoint throws a Forbidden error for external auth provider users

### Session/Cookie Auth Not Working
For SSR frameworks using cookie auth:
- `credentials: 'include'` must be set on both `authentication()` and `rest()`:
  ```typescript
  const client = createDirectus(url)
    .with(authentication('session', { credentials: 'include' }))
    .with(rest({ credentials: 'include' }));
  ```
- Ensure `CORS_CREDENTIALS=true` in Directus
- Cookies require matching domains or proper `SameSite` configuration

---

## CORS & Network Errors

### "Access-Control-Allow-Origin" Errors
Enable and configure CORS in Directus:
```env
CORS_ENABLED=true
CORS_ORIGIN=http://localhost:4321,https://your-site.com
CORS_METHODS=GET,POST,PATCH,DELETE
CORS_ALLOWED_HEADERS=Content-Type,Authorization
CORS_CREDENTIALS=true
```

Common mistakes:
- Using `CORS_ORIGIN=*` with `CORS_CREDENTIALS=true` — browsers reject this. List specific origins instead
- Forgetting to include both `http://localhost:PORT` for dev and production URL
- Missing `CORS_CREDENTIALS=true` when using cookie/session auth

### "Mixed Content" Errors
Browser blocks HTTP requests from HTTPS pages. Ensure both your frontend and Directus use HTTPS in production.

### Fetch Failures in SSG Build
During static build (e.g., `astro build`), your Directus server must be running and reachable. Verify `DIRECTUS_URL` in `.env` is correct and the server is up.

---

## SDK Errors

### "No URL provided" / "Request failed"
Ensure you're passing a valid URL to `createDirectus()`:
```typescript
// Wrong — missing protocol
const client = createDirectus('directus.example.com');

// Correct
const client = createDirectus('https://directus.example.com');
```

### "readItems is not a function" / Import Errors
Ensure you're importing from `@directus/sdk`, not an old SDK version:
```typescript
// Correct (SDK v13+)
import { createDirectus, rest, readItems } from '@directus/sdk';

// Wrong (old SDK)
import { Directus } from '@directus/sdk';
```

### TypeScript Type Errors with SDK
- Provide a Schema generic: `createDirectus<MySchema>(url)`
- Ensure your schema interface uses arrays for regular collections and singular types for singletons
- Relational fields should use union types: `number | RelatedType`
- After upgrading the SDK, check for breaking changes in type definitions

### "Cannot read property of undefined" on Response
The response might be empty or the collection name might be wrong. Always handle null:
```typescript
const posts = await client.request(readItems('posts'));
// posts could be an empty array — check length before accessing [0]
```

---

## Docker Issues

### Container Crashes on Startup
Check logs first:
```bash
docker compose logs directus
```

Common causes:
- Database not ready yet — add a health check:
  ```yaml
  database:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U directus"]
      interval: 5s
      timeout: 5s
      retries: 5

  directus:
    depends_on:
      database:
        condition: service_healthy
  ```
- Incorrect volume mounts — ensure paths exist on the host
- Incompatible env vars — check for typos

### Volumes / Permissions Errors
If Directus can't write to mounted volumes:
```bash
# Fix permissions (Linux/Mac)
sudo chown -R 1000:1000 ./uploads ./database ./extensions
```

Or in docker-compose:
```yaml
directus:
  user: "1000:1000"
```

### Extensions Not Loading in Docker
Ensure the extensions volume mount is correct:
```yaml
volumes:
  - ./extensions:/directus/extensions
```

And that built extensions (with `dist/` or `index.js`) are in the right structure:
```
extensions/
└── my-extension/
    ├── package.json
    └── dist/
        └── index.js
```

### Upgrading Directus in Docker
```bash
docker compose pull
docker compose down
docker compose up -d
```

Always snapshot your schema before upgrading:
```bash
# Before upgrade
docker compose exec directus npx directus schema snapshot /directus/snapshot.yaml
```

---

## Database Issues

### "Relation already exists" on Setup
If you're reusing a database that already has Directus tables, either:
- Use a fresh database
- Or run migrations: `npx directus database migrate:latest`

### Slow Queries
- Add database indexes for fields you frequently filter/sort on
- Use `fields` parameter to limit returned data
- Use `limit` to avoid fetching entire collections
- Enable caching: `CACHE_ENABLED=true`
- For PostgreSQL, run `ANALYZE` periodically

### Connection Pool Exhaustion
If you see "too many connections" errors:
```env
DB_POOL__MIN=0
DB_POOL__MAX=10
```

---

## File Upload & Asset Issues

### "Payload too large" on Upload
Increase the max payload size:
```env
MAX_PAYLOAD_SIZE="100mb"
```

For Docker with a reverse proxy, also configure the proxy's max body size (e.g., `client_max_body_size 100m;` in nginx).

### Assets Return 403
Ensure the accessing role has read permission on `directus_files`. For public access:
1. **Settings → Access Policies → Public**
2. Enable Read on `directus_files`

### Image Transformations Not Working
- Check `ASSETS_TRANSFORM` env var — must be `"all"` or `"presets"`
- Verify Sharp is installed (included in Docker image, may need manual install for npm setups)
- Very large images may exceed `ASSETS_TRANSFORM_IMAGE_MAX_DIMENSION`

---

## Extension Issues

### Extension Not Appearing
1. Verify the extension is built: check for `dist/index.js`
2. Verify directory structure: `extensions/{extension-name}/package.json`
3. Check `package.json` has correct `directus:extension` metadata
4. Restart Directus (or enable `EXTENSIONS_AUTO_RELOAD=true`)
5. Check logs for extension loading errors

### "Route doesn't exist" for Custom Endpoints
- Endpoints are available at `/{extension-name}/` (the directory name or custom `id`)
- Ensure the extension exported correctly — `export default` for the handler
- Check that the extension built successfully without errors
- Verify Express route paths are correct (leading slash matters)

### Hooks Not Firing
- Verify event names: `items.create` not `item.create`
- Collection-specific events: use `posts.items.create` or check `meta.collection` inside a generic handler
- Filter hooks must `return` the payload — forgetting this silently drops the data
- Check that the hook is registered in the correct lifecycle phase

---

## Performance Issues

### Slow API Responses
1. **Enable caching**: `CACHE_ENABLED=true` with Redis
2. **Limit fields**: Always specify `fields` in queries instead of returning everything
3. **Use pagination**: Never fetch unbounded result sets
4. **Add database indexes**: For frequently filtered/sorted fields
5. **Optimize relations**: Don't deeply nest relational queries if you don't need the data

### High Memory Usage
- Directus with Sharp (image processing) can use significant memory
- Set `ASSETS_TRANSFORM_IMAGE_MAX_DIMENSION` to limit max image size
- Use Redis for caching instead of in-memory
- For Docker, set memory limits:
  ```yaml
  directus:
    deploy:
      resources:
        limits:
          memory: 512M
  ```

### Slow Builds (SSG)
If `astro build` is slow due to many API calls:
- Reduce the number of collections/items fetched at build time
- Use incremental builds where supported
- Consider hybrid (SSR for dynamic pages, SSG for static)
- Cache Directus responses during build

---

## Migration & Upgrade Issues

### Breaking Changes Between Versions
Always check the [Directus release notes](https://github.com/directus/directus/releases) before upgrading. Major areas of change:
- SDK import paths and function signatures
- Environment variable names
- Database migration requirements
- Extension API changes

### Schema Migration Conflicts
If `schema apply` fails:
1. Take a fresh snapshot of the target
2. Compare manually with the source snapshot
3. Resolve conflicts in collection/field definitions
4. Apply incrementally if needed

### Data Loss Prevention
- Always back up your database before upgrading
- Test upgrades in a staging environment first
- Schema snapshots don't include content — back up your database separately

---

## Flow & Automation Issues

### Flow Not Triggering
- Check the flow's status is "Active"
- For Event Hooks: verify the correct scope (items.create, items.update) and collection are selected
- For Schedules: verify CRON syntax is correct
- For Webhooks: test the URL with curl
- For Manual: ensure the collection is selected in the trigger config

### Operations Failing Silently
- Check server logs: `docker compose logs directus`
- Use a "Log to Console" operation between steps to debug the data chain
- Web Request failures: check response status codes, verify URLs and headers
- Template variables: ensure they match exactly (e.g., `{{ operation_key.field }}`)

### Data Chain Variables Not Resolving
- Operation keys are case-sensitive
- Use `{{ $trigger }}` for trigger data, `{{ operation_key }}` for operation output
- Array access: `{{ operation_key[0].field }}`
- Check that the previous operation actually returned data

---

## Framework Integration Issues

### Astro: "getStaticPaths() requires at least one entry"
Your Directus query returned zero items. Causes:
- Collection is empty
- Filter excludes all items (e.g., nothing is "published")
- Public role doesn't have read access
- Token is invalid or missing

Handle gracefully:
```typescript
export async function getStaticPaths() {
  try {
    const pages = await directus.request(readItems('pages'));
    if (!pages.length) return [{ params: { slug: '404' }, props: {} }];
    return pages.map(p => ({ params: { slug: p.slug }, props: p }));
  } catch (error) {
    console.error('Failed to fetch pages:', error);
    return [{ params: { slug: '404' }, props: {} }];
  }
}
```

### Astro: Content Not Updating After Directus Changes
For SSG sites, you need to rebuild after content changes. Options:
- Set up a Directus Flow to trigger a deploy webhook on publish
- Use SSR mode (`output: 'server'`) for always-fresh content
- Use hybrid mode and mark content pages as SSR

### Next.js / Nuxt: ISR Cache Not Invalidating
Use `revalidate` (Next.js) or Directus webhooks to trigger revalidation:
```typescript
// Next.js API route for on-demand revalidation
export async function POST(request: Request) {
  const body = await request.json();
  revalidatePath(`/blog/${body.slug}`);
  return Response.json({ revalidated: true });
}
```

### Environment Variables Not Available
- In Astro: prefix with nothing (just use `import.meta.env.DIRECTUS_URL`)
- In Next.js: prefix with `NEXT_PUBLIC_` for client-side, no prefix for server-side
- In Nuxt: use `runtimeConfig` in `nuxt.config.ts`
- In plain Node.js: use `process.env.DIRECTUS_URL`
- Check `.env` file is in the project root and the dev server was restarted after changes

### "fetch is not defined" in Node.js
The Directus SDK uses `fetch` internally. Node.js 18+ includes it natively. For older versions:
```bash
npm install undici
```
Or use Node.js 18+.
