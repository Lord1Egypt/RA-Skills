# Other-Engine Differences (defaults beyond PostgreSQL)

| Concern | MySQL 8 | SQLite | MongoDB |
|---|---|---|---|
| Primary key | `BIGINT AUTO_INCREMENT` or `CHAR(36)` UUID | `INTEGER PRIMARY KEY AUTOINCREMENT` | `_id: ObjectId` |
| Strings | start with `VARCHAR(255)` (MySQL TEXT columns cannot be indexed without a prefix default) | `TEXT` | string |
| Time | `DATETIME` (store UTC; convert in the application) | `TEXT` ISO-8601 or unix epoch int | date |
| Money | `DECIMAL(12,2)` | `NUMERIC` / integer cents | use Decimal128; never double |
| Boolean | `TINYINT(1)` (MySQL has no true boolean) | `INTEGER` 0/1 | bool |
| Enum | `ENUM(...)` (or VARCHAR+CHECK) | `TEXT + CHECK` | no schema; application-level validation |
| Foreign keys | InnoDB supports them; must be declared explicitly | requires `PRAGMA foreign_keys=ON` | maintained manually (or lookup pattern) |
| Indexing FK columns | MySQL auto-indexes FKs | manual | manual |
| Migration conventions | raw SQL / Alembic | raw SQL / Drizzle | mongoose migrations |

## Supabase (= PostgreSQL + conventions)

- Manage DDL through the Supabase migrations directory, not dashboard clicks
- RLS: for public-facing projects, `ENABLE ROW LEVEL SECURITY` on every table by default; write policies explicitly
- `auth.users` is a reserved table; link business user tables via `user_id uuid references auth.users(id)`; when the primary key isn't named `id`, mind the Supabase client conventions
