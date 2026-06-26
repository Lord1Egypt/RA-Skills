# Database Design

Schema design, migrations, indexes, and the SQL vs. NoSQL decision.

## SQL vs. NoSQL — how to decide

**Default to Postgres.** It handles relational data, JSON, full-text search, geospatial, and even some vector workloads. Most "we need NoSQL" arguments evaporate under scrutiny.

Pick NoSQL when:
- **Document store (MongoDB, Firestore)**: data is genuinely document-shaped and you don't need joins. Examples: user-generated content with wildly varying shapes, event logs, session data.
- **Key-value (Redis, DynamoDB)**: you know the exact access pattern (key → value), need very low latency, and willingly trade query flexibility for it. Great for caches, sessions, rate limiters, job queues.
- **Wide-column (Cassandra, ScyllaDB)**: you have write-heavy time-series at massive scale and well-known access patterns.
- **Graph (Neo4j)**: your queries are fundamentally about traversing relationships many hops deep (social graphs, knowledge graphs, fraud detection).

"We might need to scale" is not a reason to reach for NoSQL. Postgres on a single box handles tens of thousands of QPS for most workloads. Scale when it's a real problem.

## Relational schema design principles

1. **Name tables as plural nouns**: `users`, `orders`, `order_items`. Name columns as snake_case singular: `user_id`, `created_at`.
2. **Primary keys**: use UUIDs for anything exposed to the outside (URLs, API responses). Use bigint auto-increment for internal-only tables if you prefer. Don't use natural keys (email, username) as primary keys — they change.
3. **Foreign keys**: always define them, even if you're using an ORM. They enforce referential integrity at the DB level.
4. **Timestamps**: `created_at` and `updated_at` on every table. Use `TIMESTAMPTZ` in Postgres (timezone-aware), not `TIMESTAMP`.
5. **Soft deletes**: add `deleted_at TIMESTAMPTZ NULL` when you need to preserve history. Be consistent — either all tables or none.
6. **Enums**: Postgres native enums are fine for truly fixed sets (role types, statuses). For anything that might grow, use a reference table or a `CHECK` constraint on a `TEXT` column — altering an enum requires migrations.
7. **JSON columns**: use `JSONB` in Postgres for flexible/metadata fields, but don't make your whole schema JSON. If a field is queried or filtered on, it deserves to be a column with an index.
8. **NULL means "unknown" or "not applicable"**. Don't use it as "false" or "empty string" — it's a different thing and breaks queries.

## Indexing — the single biggest perf lever

Rules of thumb:
- Every foreign key needs an index. Most ORMs don't create these automatically.
- Every column that appears in a `WHERE`, `ORDER BY`, or `JOIN` predicate on a hot query path needs an index.
- Composite indexes: the order matters. Put the most selective / most-filtered column first.
- Adding an index has a cost — slower writes, more disk. Don't add indexes speculatively.
- Run `EXPLAIN ANALYZE` on your slow queries. The plan tells you exactly what's happening.

A common mistake: the ORM generates a query that's not using any of your indexes. Check. Don't trust.

## Migrations

Every schema change goes through a migration file. Never edit the DB by hand in any environment above local dev.

### Tooling
- **Prisma** (Node): `prisma migrate dev` / `prisma migrate deploy`
- **Drizzle** (Node): `drizzle-kit generate` / `drizzle-kit migrate`
- **Alembic** (Python/SQLAlchemy): `alembic revision --autogenerate` / `alembic upgrade head`
- **Django**: `makemigrations` / `migrate`
- **Go**: `golang-migrate` or `goose`
- **Rails**: built-in migrations

### Migration safety in production

The golden rule: **all migrations must be backward-compatible with the currently-deployed app code**, because there's always a window during deploy where old and new code both run.

Safe patterns:
- Add a new nullable column → backfill in a background job → make NOT NULL in a second migration (after old code is gone).
- Rename a column → create a new column, dual-write from the app, backfill, migrate reads, drop the old column. Multiple deploys.
- Drop a column → stop writing from the app first, ship that, then drop in a later migration.

Dangerous patterns that block or lock tables on Postgres:
- `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT <value>` on large tables (rewrites the whole table on older Postgres versions; fast on Postgres 11+).
- Adding an index on a large table without `CONCURRENTLY`.
- Long-running queries that hold locks (transactions on DDL statements).

For large production tables, always use `CREATE INDEX CONCURRENTLY`. Most ORM migration tools default to the blocking version — override explicitly.

## Common schemas for common domains

### Multi-tenant SaaS
Three approaches, pick by isolation needs:
1. **Shared schema + tenant_id column on every table.** Simplest. What most SaaS apps use. Requires discipline — every query must filter by tenant.
2. **Schema-per-tenant** (Postgres schemas). Stronger isolation, moderate complexity, doesn't scale to 10,000s of tenants.
3. **Database-per-tenant**. Strongest isolation. Only for a handful of enterprise tenants or regulated industries.

Enforce tenant scoping at the ORM/repo layer, not in individual queries — one forgotten `WHERE tenant_id = ...` is a data leak.

### Users + auth
```sql
users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  email_verified_at TIMESTAMPTZ,
  password_hash TEXT,              -- NULL if only OAuth
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
)

sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  token_hash TEXT UNIQUE NOT NULL, -- never store raw tokens
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
)

-- if supporting OAuth providers
oauth_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  provider TEXT NOT NULL,          -- 'google', 'github', etc.
  provider_account_id TEXT NOT NULL,
  UNIQUE (provider, provider_account_id)
)
```

### Orders / e-commerce
```sql
orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  status TEXT NOT NULL,           -- 'pending', 'paid', 'shipped', ...
  total_cents INTEGER NOT NULL,   -- never store money as float
  currency CHAR(3) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
)

order_items (
  id UUID PRIMARY KEY,
  order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price_cents INTEGER NOT NULL  -- snapshot, not a join
)
```

Always snapshot prices at order time. The product's price may change; the order's historical price must not.

### Audit / event log
```sql
audit_log (
  id BIGSERIAL PRIMARY KEY,
  actor_id UUID,                   -- who did it
  action TEXT NOT NULL,            -- 'user.created', 'order.refunded'
  target_type TEXT NOT NULL,
  target_id TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
)
CREATE INDEX ON audit_log (actor_id, created_at DESC);
CREATE INDEX ON audit_log (target_type, target_id, created_at DESC);
```

Audit logs are append-only. No updates, no deletes. Eventually archive to cold storage.

## Money and time — get these right early

### Money
- Store in the smallest unit (cents, satoshis) as an integer. NEVER as float.
- Always store the currency.
- Round only at display time, using the currency's rules.

### Time
- Store in UTC (`TIMESTAMPTZ` in Postgres). Convert at display.
- Store user-preferred timezone as a separate column when you need it ("Send daily digest at 9am THEIR time").
- Dates (not times) are different — "birthday" is a `DATE`, not a `TIMESTAMPTZ`.

## NoSQL (MongoDB) specifics

When you have chosen MongoDB deliberately:

- **Design around access patterns.** Embed what you always read together, reference what you read separately. Don't "3NF" your documents.
- **Indexes matter just as much.** Always index query fields. `db.collection.explain()` is your friend.
- **Don't use MongoDB transactions as the happy path.** They work but are the fallback, not the primary design. If you need transactions everywhere, you probably wanted SQL.
- **Validation with JSON Schema**. MongoDB supports schema validation; use it. Schemaless doesn't mean "no schema," it means "the schema lives in your app code and you should document it."

## Connection pooling

For any serverful deployment, connection pooling is mandatory:
- Postgres: PgBouncer in transaction mode, or a connection pool built into your ORM (Prisma, SQLAlchemy).
- In serverless (Vercel, AWS Lambda), use a pooling proxy — PgBouncer, Neon's built-in pooler, Supabase's pooler, AWS RDS Proxy. Direct connections from serverless rapidly exhaust the DB.

## Backups

- Enable automated daily backups on the managed DB.
- Enable point-in-time recovery (PITR) for production.
- Test restore at least quarterly. An unverified backup is not a backup — prove the restore path works before you need it.
