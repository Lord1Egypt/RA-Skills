# Directus Data Modeling & Administration

## Table of Contents
1. [Collections & Fields](#collections--fields)
2. [Relations](#relations)
3. [Permissions & Access Control](#permissions--access-control)
4. [File Management](#file-management)
5. [Environment Configuration](#environment-configuration)
6. [Installation & Deployment](#installation--deployment)
7. [Schema Migration](#schema-migration)

---

## Collections & Fields

### Creating Collections
Collections map to database tables. Create them in the Data Studio under **Settings → Data Model** or via API.

**Common field types:**
| Type | Description | Use Case |
|---|---|---|
| `string` | Short text (varchar) | Titles, names, slugs |
| `text` | Long text | Descriptions, excerpts |
| `integer` | Whole number | IDs, counts |
| `float` / `decimal` | Decimal number | Prices, percentages |
| `boolean` | True/false | Toggles, flags |
| `datetime` | Date and time | Publish dates, timestamps |
| `date` | Date only | Birthdays, event dates |
| `time` | Time only | Schedules |
| `json` | JSON object | Structured data, settings |
| `uuid` | UUID string | Primary keys |
| `hash` | Hashed string | Passwords |
| `csv` | Comma-separated values | Simple lists |

### Interface Types
Interfaces control how fields appear in the editor:
- `input` — standard text input
- `input-rich-text-html` — WYSIWYG editor (stores HTML)
- `input-rich-text-md` — Markdown editor
- `input-code` — Code editor with syntax highlighting
- `select-dropdown` — Dropdown select
- `select-multiple-checkbox` — Checkboxes
- `boolean` — Toggle switch
- `datetime` — Date/time picker
- `file-image` — Image upload
- `file` — File upload
- `tags` — Tag input
- `slider` — Range slider
- `map` — Map coordinate picker
- `translations` — Multilingual content interface

### System Fields
Directus can automatically manage these optional fields:
- `status` — workflow status (draft, published, archived)
- `sort` — manual sort order
- `date_created` — auto-set on creation
- `date_updated` — auto-set on update
- `user_created` — auto-set to creating user
- `user_updated` — auto-set to updating user

### Singleton Collections
A singleton has exactly one item — used for global settings, homepage content, etc. Enable in collection settings: **Singleton → Treat as a single object**.

---

## Relations

### Many-to-One (M2O)
The most common relation. A foreign key field on the "many" side points to the "one" side.

**Example:** Each `post` belongs to one `category`.
- Field `category` on `posts` collection → references `categories.id`
- In the editor, shows as a dropdown or drawer selector

### One-to-Many (O2M)
The reverse of M2O. Displayed on the "one" side as a list of related items.

**Example:** A `category` has many `posts`.
- Configure as an O2M alias field on `categories` → references `posts.category`
- No new database column — it reads the existing M2O relation in reverse

### Many-to-Many (M2M)
Requires a junction collection with two foreign keys.

**Example:** `posts` and `tags` linked via `posts_tags`.
- Junction collection `posts_tags`:
  - `posts_id` → M2O to `posts`
  - `tags_id` → M2O to `tags`
- Directus auto-creates the junction if you set up M2M in the Data Model UI

### Many-to-Any (M2A)
A polymorphic relation where items can reference rows from multiple collections. Used for page builders and block-based content.

**Example:** A `page` has `blocks` that can be heroes, text sections, galleries, etc.
- Junction collection `pages_blocks`:
  - `pages_id` → M2O to `pages`
  - `collection` → string (which collection the item comes from)
  - `item` → string (the ID of the related item)
  - `sort` → integer (ordering)

### Translations
A special M2M pattern for multilingual content. Directus provides a dedicated translations interface that creates:
- A `languages` collection
- A junction collection (e.g., `posts_translations`) with fields for each translated field plus a `languages_code` foreign key

---

## Permissions & Access Control

### Concepts
- **Roles** — groups of users (e.g., Admin, Editor, Viewer)
- **Policies** — sets of permissions attached to a role
- **Permissions** — CRUD access per collection, optionally with field-level and item-level rules
- **Access Policies** — found in Settings → Access Policies

### Default State
New collections are completely private. No role (including Public) has any access until you grant it.

### Public Role
The Public role controls what unauthenticated users can access. For a public-facing site:
1. Go to **Settings → Access Policies → Public**
2. For each collection you want publicly readable, enable **Read** access
3. Optionally restrict which fields are visible

### Field-Level Permissions
Control which fields a role can read or write:
```
Role: Editor
Collection: posts
Create: ✅ (title, content, excerpt, status=draft only)
Read: ✅ (all fields)
Update: ✅ (title, content, excerpt — but NOT status)
Delete: ❌
```

### Item-Level Permissions (Custom Rules)
Restrict access to specific items based on field values:
```
Role: Author
Collection: posts
Read: Custom → user_created equals $CURRENT_USER
Update: Custom → user_created equals $CURRENT_USER
```

### Available Variables in Permission Rules
- `$CURRENT_USER` — the authenticated user's ID
- `$CURRENT_ROLE` — the authenticated user's role UUID
- `$NOW` — current timestamp

### Admin Role
Users with the admin role bypass all permission checks. There is always at least one admin user.

---

## File Management

### Storage Adapters
Directus supports multiple storage backends:

```env
# Local filesystem (default)
STORAGE_LOCATIONS="local"
STORAGE_LOCAL_ROOT="./uploads"

# Amazon S3
STORAGE_LOCATIONS="s3"
STORAGE_S3_KEY="your-access-key"
STORAGE_S3_SECRET="your-secret-key"
STORAGE_S3_BUCKET="your-bucket"
STORAGE_S3_REGION="us-east-1"

# Google Cloud Storage
STORAGE_LOCATIONS="gcs"
STORAGE_GCS_KEY_FILENAME="./service-account.json"
STORAGE_GCS_BUCKET="your-bucket"

# Cloudflare R2
STORAGE_LOCATIONS="s3"
STORAGE_S3_KEY="your-r2-key"
STORAGE_S3_SECRET="your-r2-secret"
STORAGE_S3_BUCKET="your-bucket"
STORAGE_S3_ENDPOINT="https://{account-id}.r2.cloudflarestorage.com"
STORAGE_S3_REGION="auto"
```

### Image Transformations
Directus automatically serves transformed images via query parameters:
```
GET /assets/{file-id}?width=300&height=200&fit=cover&format=webp&quality=80
```

Transformation presets can be configured to limit allowed transformations:
```env
ASSETS_TRANSFORM="presets"
ASSETS_TRANSFORM_IMAGE_MAX_DIMENSION="4096"
```

---

## Environment Configuration

### Essential Variables

```env
# Security (REQUIRED)
SECRET="a-long-random-string"

# Database
DB_CLIENT="pg"                    # pg, mysql, sqlite3, mssql, oracledb, cockroachdb
DB_HOST="localhost"
DB_PORT="5432"
DB_DATABASE="directus"
DB_USER="directus"
DB_PASSWORD="password"

# For SQLite
DB_CLIENT="sqlite3"
DB_FILENAME="./database.db"

# Admin User (first run only)
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="secure-password"
ADMIN_TOKEN="optional-static-token"

# Server
HOST="0.0.0.0"
PORT="8055"
PUBLIC_URL="https://your-directus-domain.com"

# CORS
CORS_ENABLED="true"
CORS_ORIGIN="https://your-frontend.com"
CORS_METHODS="GET,POST,PATCH,DELETE"

# WebSockets
WEBSOCKETS_ENABLED="true"

# Email
EMAIL_TRANSPORT="smtp"
EMAIL_SMTP_HOST="smtp.example.com"
EMAIL_SMTP_PORT="587"
EMAIL_SMTP_USER="user"
EMAIL_SMTP_PASSWORD="password"
EMAIL_FROM="noreply@example.com"

# Cache
CACHE_ENABLED="true"
CACHE_STORE="redis"
CACHE_REDIS="redis://localhost:6379"
CACHE_TTL="5m"

# Rate Limiting
RATE_LIMITER_ENABLED="true"
RATE_LIMITER_STORE="redis"
RATE_LIMITER_POINTS="50"
RATE_LIMITER_DURATION="1"

# Extensions
EXTENSIONS_PATH="./extensions"
EXTENSIONS_AUTO_RELOAD="false"

# Logging
LOG_LEVEL="info"                  # fatal, error, warn, info, debug, trace
LOG_STYLE="pretty"                # pretty, raw
```

---

## Installation & Deployment

### Docker (Recommended)
```yaml
# docker-compose.yml
services:
  database:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: directus
      POSTGRES_PASSWORD: directus
      POSTGRES_DB: directus

  cache:
    image: redis:7

  directus:
    image: directus/directus:latest
    ports:
      - 8055:8055
    volumes:
      - ./uploads:/directus/uploads
      - ./extensions:/directus/extensions
    depends_on:
      - database
      - cache
    environment:
      SECRET: 'change-this-to-a-random-value'
      ADMIN_EMAIL: 'admin@example.com'
      ADMIN_PASSWORD: 'your-password'

      DB_CLIENT: 'pg'
      DB_HOST: 'database'
      DB_PORT: '5432'
      DB_DATABASE: 'directus'
      DB_USER: 'directus'
      DB_PASSWORD: 'directus'

      CACHE_ENABLED: 'true'
      CACHE_STORE: 'redis'
      CACHE_REDIS: 'redis://cache:6379'

      WEBSOCKETS_ENABLED: 'true'

volumes:
  pgdata:
```

### npm (Self-Hosted)
```bash
npx create-directus-project my-project
cd my-project
npx directus start
```

### Directus Cloud
Sign up at directus.io/cloud — managed hosting from $15/month with auto-scaling, CDN, and backups.

### One-Click Deploy
- **Railway**: One-click deploy with PostgreSQL, Redis, and S3 storage
- **DigitalOcean**: App Platform deployment
- **Render**: Web service deployment

---

## Schema Migration

Directus supports schema snapshots and diffs for migrating data models between environments.

### Export Schema Snapshot
```bash
# CLI
npx directus schema snapshot ./snapshot.yaml

# API
GET /schema/snapshot
```

### Apply Schema to Another Instance
```bash
# Generate a diff
npx directus schema diff ./snapshot.yaml

# Apply the diff
npx directus schema apply ./snapshot.yaml
```

### API-Based Migration
```typescript
// Export from source
const snapshot = await fetch('https://source.directus.app/schema/snapshot', {
  headers: { Authorization: 'Bearer admin-token' },
}).then(r => r.json());

// Diff against target
const diff = await fetch('https://target.directus.app/schema/diff', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer admin-token',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(snapshot),
}).then(r => r.json());

// Apply diff to target
await fetch('https://target.directus.app/schema/apply', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer admin-token',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(diff),
});
```

### Best Practices
- Always snapshot before upgrading Directus versions
- Use schema migration in CI/CD pipelines to keep staging and production in sync
- Schema snapshots include collections, fields, and relations — not content data
- For content migration, use the API to export/import items
