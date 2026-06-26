---
name: Drizzle
description: Build type-safe database queries with Drizzle ORM patterns.
metadata: {"clawdbot":{"emoji":"💧","requires":{"bins":["npx"]},"os":["linux","darwin","win32"]}}
---

## Schema Definition
- Export every table from schema file — queries fail silently if table isn't exported
- Use `$inferSelect` for query return types, `$inferInsert` for insert input — they differ (select has defaults filled, insert has optionals)
- Define `relations()` in a separate call, not inline with table — Drizzle separates schema from relations

## Query Syntax Traps
- Conditions use functions, not objects: `where: eq(users.id, 5)` not `where: { id: 5 }` — Prisma syntax doesn't work
- Combine conditions with `and()` / `or()`: `where: and(eq(users.active, true), gt(users.age, 18))`
- `db.query.users.findMany()` for relational queries with `with:`, `db.select().from(users)` for SQL-like — mixing them causes type errors

## Migrations
- `drizzle-kit push` is dev-only (destructive) — production needs `drizzle-kit generate` then `drizzle-kit migrate`
- Schema changes require regenerating migrations — editing generated SQL breaks the migration hash
- Set `strict: true` in drizzle.config.ts to catch schema drift before it hits production

## Driver-Specific
- PostgreSQL: use `pgTable`, imports from `drizzle-orm/pg-core`
- MySQL: use `mysqlTable`, imports from `drizzle-orm/mysql-core`  
- SQLite: use `sqliteTable`, imports from `drizzle-orm/sqlite-core`
- Mixing imports across drivers compiles but fails at runtime with cryptic errors

## Performance
- Wrap multi-query operations in `db.transaction(async (tx) => {})` — Drizzle doesn't auto-batch
- Use `.prepare()` for queries executed repeatedly — skips query building overhead
- Add `.limit()` to every `findMany()` / `select()` — no default limit means full table scans

## Common Mistakes
- Forgetting `await` on queries returns a Promise, not results — TypeScript doesn't catch this if you ignore the return
- `returning()` is required to get inserted/updated rows back — without it you get `{ rowCount }` only
- JSON columns: PostgreSQL uses `jsonb()`, MySQL uses `json()` — wrong function = wrong serialization
