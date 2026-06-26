---
name: db-migrate
description: "Database migration manager. Detects ORM/migration tool in use, generates migrations, handles rollbacks, creates seed scripts, diffs schemas between environments, backs up databases, and supports zero-downtime patterns. Use when the user says 'database migration', 'migrate', 'schema change', 'seed data', 'rollback', 'add a column', 'rename column', 'drop table', 'backfill', 'schema diff', or 'backup database'. Supports Prisma, Drizzle, Knex, TypeORM, Alembic, Django, raw SQL. Works with Postgres, MySQL, SQLite."
required-tools:
  - Bash
security-notes: |
  This skill requires database CLI tools (prisma, drizzle-kit, knex, alembic, django manage.py, psql, mysql, sqlite3) to be installed locally.
  Database credentials are read from the project's existing environment files (.env, .env.local) — this skill NEVER asks for or stores credentials directly.
  All destructive operations (DROP, DELETE, rollback) require explicit user confirmation before execution.
  Production database operations always create a backup first.
  This skill does NOT connect to remote databases unless the user's existing configuration already points to one.
---

# Database Migration Manager

Detect. Generate. Migrate. Roll back. Zero downtime.

## Phase 1: Detect Migration Tool

Scan the project to identify the ORM/migration tool in use. Check in this order:

| Signal | Tool |
|--------|------|
| `prisma/schema.prisma` or `schema.prisma` in root | **Prisma** |
| `drizzle.config.ts` or `drizzle.config.js` or `drizzle/` dir | **Drizzle** |
| `knexfile.js` or `knexfile.ts` | **Knex** |
| `ormconfig.json` or `data-source.ts` with `TypeORM` import | **TypeORM** |
| `alembic.ini` or `alembic/` directory | **Alembic** |
| `manage.py` with Django imports | **Django** |
| `migrations/` dir with raw `.sql` files, no ORM config | **Raw SQL** |

If no tool is detected, ask the user which they want to use. If starting fresh, recommend Drizzle for TypeScript projects, Alembic for Python, Django migrations for Django apps.

Read the existing migration history to understand current schema state before doing anything.

## Phase 2: Determine the Operation

Classify what the user needs:

| Operation | Description |
|-----------|-------------|
| **generate** | Create a new migration from schema changes |
| **run** | Apply pending migrations |
| **rollback** | Revert the last migration or to a specific point |
| **seed** | Create or run seed data scripts |
| **diff** | Compare schemas between environments |
| **backup** | Back up the database before migrating |
| **zero-downtime** | Multi-step migration for production safety |

If the user's request implies multiple operations (e.g., "migrate production safely"), chain them: backup -> diff -> generate -> run.

## Phase 3: Execute by Tool

### Prisma

```bash
# Generate migration from schema changes
npx prisma migrate dev --name <migration_name>

# Apply in production (no interactive prompts)
npx prisma migrate deploy

# Reset database (dev only — destroys data)
npx prisma migrate reset

# Check migration status
npx prisma migrate status

# Generate client after schema change
npx prisma generate

# Seed data
npx prisma db seed

# Pull schema from existing database
npx prisma db pull

# Push schema without migration file (dev only)
npx prisma db push
```

**Prisma rollback**: Prisma has no built-in rollback command. To roll back:
1. Create a new migration that reverses the changes
2. Or restore from backup
3. For failed migrations: `npx prisma migrate resolve --rolled-back <migration_name>`

**Prisma seed setup**: Ensure `package.json` has:
```json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

### Drizzle

```bash
# Generate migration from schema changes
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push schema directly (dev only — destructive)
npx drizzle-kit push

# Pull schema from existing database
npx drizzle-kit pull

# Open Drizzle Studio (visual browser)
npx drizzle-kit studio

# Check current state
npx drizzle-kit check
```

**Drizzle rollback**: Drizzle generates SQL files. To roll back:
1. Write a new migration that reverses changes
2. Or delete the migration file and re-push (dev only)
3. For production: always use generated SQL files, never `push`

**Drizzle seed**: Create a `seed.ts` file and run with `tsx drizzle/seed.ts` or add a script to `package.json`.

### Knex

```bash
# Create a new migration file
npx knex migrate:make <migration_name>

# Run pending migrations
npx knex migrate:latest

# Rollback last batch
npx knex migrate:rollback

# Rollback all migrations
npx knex migrate:rollback --all

# Check migration status
npx knex migrate:status

# Run seed files
npx knex seed:run

# Create a new seed file
npx knex seed:make <seed_name>
```

**Knex migration template**:
```js
exports.up = function(knex) {
  return knex.schema.createTable('table_name', (table) => {
    table.increments('id').primary();
    table.timestamps(true, true);
  });
};

exports.down = function(knex) {
  return knex.schema.dropTable('table_name');
};
```

### TypeORM

```bash
# Generate migration from entity changes
npx typeorm migration:generate -d src/data-source.ts src/migrations/<MigrationName>

# Create empty migration
npx typeorm migration:create src/migrations/<MigrationName>

# Run pending migrations
npx typeorm migration:run -d src/data-source.ts

# Revert last migration
npx typeorm migration:revert -d src/data-source.ts

# Show migrations and status
npx typeorm migration:show -d src/data-source.ts
```

### Alembic (Python/SQLAlchemy)

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of change"

# Create empty migration
alembic revision -m "description of change"

# Apply all pending migrations
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Rollback one step
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Show current revision
alembic current

# Show migration history
alembic history

# Show all branch heads
alembic heads
```

### Django

```bash
# Generate migrations from model changes
python3 manage.py makemigrations

# Generate for specific app
python3 manage.py makemigrations <app_name>

# Apply all pending migrations
python3 manage.py migrate

# Apply specific app migration
python3 manage.py migrate <app_name> <migration_number>

# Rollback to specific migration
python3 manage.py migrate <app_name> <migration_number>

# Rollback all migrations for an app
python3 manage.py migrate <app_name> zero

# Show migration status
python3 manage.py showmigrations

# Generate SQL without applying
python3 manage.py sqlmigrate <app_name> <migration_number>

# Create empty migration
python3 manage.py makemigrations --empty <app_name>
```

### Raw SQL

When no ORM is detected and the project uses raw SQL:

1. Create a `migrations/` directory if it doesn't exist
2. Name files with timestamp prefix: `YYYYMMDDHHMMSS_description.sql`
3. Each migration file should have `-- UP` and `-- DOWN` sections
4. Track applied migrations in a `_migrations` table

**Raw SQL migration template**:
```sql
-- UP
CREATE TABLE IF NOT EXISTS example (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- DOWN
DROP TABLE IF EXISTS example;
```

**Migration tracking table**:
```sql
CREATE TABLE IF NOT EXISTS _migrations (
  id SERIAL PRIMARY KEY,
  filename VARCHAR(255) NOT NULL UNIQUE,
  applied_at TIMESTAMP DEFAULT NOW()
);
```

## Phase 4: Database Backup

**Always back up before running migrations in production.** Offer to back up before any destructive operation.

### Postgres
```bash
# Full database dump (compressed)
pg_dump -Fc -f backup_$(date +%Y%m%d_%H%M%S).dump $DATABASE_URL

# Schema only
pg_dump --schema-only -f schema_$(date +%Y%m%d_%H%M%S).sql $DATABASE_URL

# Specific tables
pg_dump -t table_name -f table_backup.dump $DATABASE_URL

# Restore from dump
pg_restore -d $DATABASE_URL backup.dump

# Restore from SQL
psql $DATABASE_URL < backup.sql

# Roles and global objects (needed for full restore)
pg_dumpall --globals-only -f globals.sql
```

### MySQL
```bash
# Full database dump
mysqldump -u $DB_USER -p $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql

# Schema only
mysqldump -u $DB_USER -p --no-data $DB_NAME > schema_$(date +%Y%m%d_%H%M%S).sql

# Specific tables
mysqldump -u $DB_USER -p $DB_NAME table_name > table_backup.sql

# Restore
mysql -u $DB_USER -p $DB_NAME < backup.sql

# With single-transaction for InnoDB (no locks)
mysqldump --single-transaction -u $DB_USER -p $DB_NAME > backup.sql
```

### SQLite
```bash
# Copy the database file (simplest backup)
cp database.db backup_$(date +%Y%m%d_%H%M%S).db

# SQL dump
sqlite3 database.db .dump > backup_$(date +%Y%m%d_%H%M%S).sql

# With WAL mode — must copy both files
cp database.db backup.db && cp database.db-wal backup.db-wal 2>/dev/null

# Online backup (safe while db is in use)
sqlite3 database.db "VACUUM INTO 'backup_$(date +%Y%m%d_%H%M%S).db';"

# Restore from SQL dump
sqlite3 new_database.db < backup.sql
```

## Phase 5: Schema Diff Between Environments

Compare schemas to detect drift between environments.

### Prisma
```bash
# Pull remote schema and compare
npx prisma db pull  # updates schema.prisma from database
git diff prisma/schema.prisma  # see what changed vs. committed schema
```

### Drizzle
```bash
# Check for schema drift
npx drizzle-kit check

# Pull current DB schema
npx drizzle-kit pull
# Then diff generated files against your source schema
```

### Generic SQL Diff (Postgres)
```bash
# Dump schemas from both environments
pg_dump --schema-only -f staging_schema.sql $STAGING_DATABASE_URL
pg_dump --schema-only -f production_schema.sql $PRODUCTION_DATABASE_URL

# Diff them
diff staging_schema.sql production_schema.sql
```

### Generic SQL Diff (MySQL)
```bash
mysqldump --no-data -u $USER -p $STAGING_DB > staging_schema.sql
mysqldump --no-data -u $USER -p $PROD_DB > production_schema.sql
diff staging_schema.sql production_schema.sql
```

For richer diffs, use `migra` (Postgres):
```bash
pip install migra
migra $STAGING_DATABASE_URL $PRODUCTION_DATABASE_URL --unsafe
# Outputs ALTER statements needed to sync staging -> production
```

## Phase 6: Seed Data

When creating seed scripts, follow these principles:

1. **Idempotent**: Seeds must be safe to run multiple times (use upserts or check-before-insert)
2. **Environment-aware**: Different seed data for dev vs. staging vs. production
3. **Realistic**: Use realistic data shapes, not lorem ipsum
4. **Referential integrity**: Insert in dependency order (users before posts, etc.)
5. **Deterministic**: Use fixed IDs or consistent generation for reproducibility

### Seed Script Structure

```typescript
// seed.ts pattern (Prisma/Drizzle/Knex)
async function seed() {
  console.log('Seeding database...');

  // 1. Clear existing data (dev only)
  if (process.env.NODE_ENV !== 'production') {
    await clearTables();
  }

  // 2. Insert in dependency order
  const users = await seedUsers();
  const projects = await seedProjects(users);
  await seedTasks(projects, users);

  console.log('Seeding complete.');
}

seed()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
```

### Python Seed Pattern (Alembic/Django)

```python
# For Alembic: create a data migration
# alembic revision -m "seed initial data"

def upgrade():
    op.execute("""
        INSERT INTO users (email, name) VALUES
        ('admin@example.com', 'Admin')
        ON CONFLICT (email) DO NOTHING;
    """)

def downgrade():
    op.execute("DELETE FROM users WHERE email = 'admin@example.com';")
```

```python
# For Django: management command
# python3 manage.py seed
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.get_or_create(
            email='admin@example.com',
            defaults={'name': 'Admin'}
        )
```

## Phase 7: Zero-Downtime Migrations

Use the **expand-contract pattern** for any schema change that could break running application code. This is mandatory for production deployments with rolling updates or blue-green deploys.

### When to Use Zero-Downtime Patterns

| Change | Safe Without Pattern? | Zero-Downtime Required? |
|--------|----------------------|------------------------|
| Add nullable column | Yes | No |
| Add column with default | Yes (Postgres 11+, MySQL 8.0.12+) | No |
| Add NOT NULL column | No | Yes |
| Rename column | No | Yes |
| Change column type | No | Yes |
| Drop column | No | Yes |
| Add index | Depends on size | Use CONCURRENTLY |
| Add foreign key | No (locks table) | Yes |

### The Expand-Contract Pattern

**Step 1: Expand** (Deploy migration + new code that writes to both)
```sql
-- Add new column, nullable, no constraint yet
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);
```

**Step 2: Backfill** (Run as background job, batch processing)
```sql
-- Process in batches to avoid locks
UPDATE users
SET display_name = name
WHERE display_name IS NULL
AND id BETWEEN $start AND $end;
-- Run in batches of 1000-5000 rows
-- Sleep 100-500ms between batches
-- Monitor replication lag
```

**Step 3: Contract** (Deploy code that only reads from new column)
```sql
-- Now safe to add constraint
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;

-- After bake period (24-72 hours), drop old column
ALTER TABLE users DROP COLUMN name;
```

### Safe Index Creation

```sql
-- Postgres: CREATE INDEX CONCURRENTLY (no table lock)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
-- Note: Cannot run inside a transaction

-- MySQL: Online DDL (InnoDB)
ALTER TABLE users ADD INDEX idx_email (email), ALGORITHM=INPLACE, LOCK=NONE;
```

### Safe Foreign Key Addition (Postgres)

```sql
-- Step 1: Add constraint as NOT VALID (no full table scan)
ALTER TABLE posts
ADD CONSTRAINT fk_posts_user
FOREIGN KEY (user_id) REFERENCES users(id)
NOT VALID;

-- Step 2: Validate in background (no lock on writes)
ALTER TABLE posts VALIDATE CONSTRAINT fk_posts_user;
```

### Rename Column Pattern

Never rename directly. Instead:
1. Add new column
2. Deploy code that writes to both old and new
3. Backfill new column from old
4. Deploy code that reads from new column only
5. Drop old column after bake period

### Multi-Deploy Migration Checklist

For any breaking schema change, split across multiple deploys:

- [ ] **Deploy 1**: Add new column/table (expand)
- [ ] **Deploy 2**: Update writes to populate both old and new
- [ ] **Deploy 3**: Backfill existing data
- [ ] **Deploy 4**: Switch reads to new column/table
- [ ] **Deploy 5**: Stop writing to old column
- [ ] **Deploy 6**: Drop old column/table (contract) — after bake period

## Safety Rules

1. **Never run `migrate reset`, `push`, or `db push` in production** — these are dev-only commands
2. **Always back up before migrating production** — offer this proactively
3. **Never drop columns or tables without confirming with the user** — even if the schema change implies it
4. **Review generated SQL before applying** — auto-generated migrations can be destructive
5. **Test migrations on a staging copy of production data** — operations that take milliseconds on dev can lock for minutes on large tables
6. **Monitor during production migrations** — watch replication lag, CPU, lock contention
7. **Keep migrations small and focused** — one concern per migration file
8. **Never skip the down/rollback function** — every up needs a corresponding down
9. **Use transactions where supported** — Postgres DDL is transactional, MySQL is not (most DDL auto-commits)
10. **Check for active connections before dropping** — `SELECT * FROM pg_stat_activity WHERE datname = 'dbname';`

## Error Recovery

If a migration fails mid-way:

1. **Check migration status** — which migrations applied, which failed
2. **Do NOT re-run blindly** — understand what partially applied
3. **For Prisma**: `npx prisma migrate resolve --rolled-back <name>` to mark as rolled back
4. **For Alembic**: `alembic stamp <last_good_revision>` to reset tracking
5. **For Django**: Fix the issue, then `python3 manage.py migrate` again (Django tracks per-migration)
6. **For Knex**: Check `knex_migrations` table, manually remove failed entry if needed
7. **Restore from backup** if the database is in an inconsistent state

## Environment Variable Detection

Read database connection from the project's environment:

| Variable | Common In |
|----------|-----------|
| `DATABASE_URL` | Prisma, Drizzle, general |
| `DB_HOST` + `DB_PORT` + `DB_NAME` + `DB_USER` + `DB_PASSWORD` | Knex, TypeORM, raw |
| `SQLALCHEMY_DATABASE_URI` | Alembic/Flask |
| `DATABASES` in `settings.py` | Django |
| `POSTGRES_URL` or `POSTGRES_PRISMA_URL` | Vercel Postgres |
| `TURSO_DATABASE_URL` + `TURSO_AUTH_TOKEN` | Turso/LibSQL |

Check `.env`, `.env.local`, `.env.development`, and `.env.production` for these values. Never log or display connection strings — they contain credentials.
