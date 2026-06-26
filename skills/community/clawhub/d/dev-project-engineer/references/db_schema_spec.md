# Database Schema Specification Template

This section of the Implementation Plan covers all database changes. It is used by the BE Developer for implementation and by the engineer for architecture reference.

## ID Convention

All database items use the prefix `DB-` followed by a sequential number: DB-001, DB-002, etc.

---

## DB-S1: New Tables

For each new table:

```
DB-001: [table_name]
SRS Requirement(s): [SRS-XXX]
Purpose: [what this table stores and why]

Columns:
  | Column        | Type          | Nullable | Default      | Constraints          | Notes                    |
  |---------------|---------------|----------|--------------|----------------------|--------------------------|
  | id            | UUID / SERIAL | No       | gen_random() | PRIMARY KEY          |                          |
  | [column]      | [type]        | [Y/N]    | [default]    | [UNIQUE, FK, CHECK]  | [explanation if needed]  |
  | created_at    | TIMESTAMP     | No       | NOW()        |                      |                          |
  | updated_at    | TIMESTAMP     | No       | NOW()        |                      | Auto-update on change    |

Indexes:
  - idx_[table]_[column] ON [column(s)] — [why this index exists, e.g., "frequently queried by user_id"]
  - UNIQUE idx_[table]_[column] ON [column] — [if needed]

Foreign Keys:
  - [column] → [other_table].[column] ON DELETE [CASCADE | SET NULL | RESTRICT]
```

### Column Type Guidance

Use types appropriate to the database engine. Common mappings:
- Identifiers: UUID (preferred) or SERIAL/BIGSERIAL
- Strings: VARCHAR(n) for bounded, TEXT for unbounded
- Numbers: INTEGER, BIGINT, DECIMAL(p,s) for money/precision
- Booleans: BOOLEAN
- Dates: TIMESTAMP WITH TIME ZONE for all datetime values
- JSON: JSONB (Postgres) or JSON — use sparingly, prefer normalized columns
- Enums: Use a CHECK constraint on VARCHAR rather than DB-level ENUM types (easier to migrate)

## DB-S2: Altered Tables

For each existing table that needs modification:

```
DB-010: Alter [table_name]
SRS Requirement(s): [SRS-XXX]
Reason: [why this table needs changes]

Changes:
  - ADD COLUMN [column_name] [type] [nullable] [default] — [reason]
  - ALTER COLUMN [column_name] SET TYPE [new_type] — [reason, migration concern]
  - DROP COLUMN [column_name] — [reason, confirm no dependencies]
  - ADD INDEX idx_[name] ON [column(s)] — [reason]
  - ADD FOREIGN KEY [column] → [table].[column] — [reason]

Migration Concerns:
  - [Will this lock the table? For how long?]
  - [Is there existing data that needs backfilling?]
  - [Is there a risk of data loss?]
  - [Does this require a multi-step migration? Describe the steps.]
```

## DB-S3: Foreign Key Relationships

Provide a relationship map showing how tables connect:

```
users
  └── 1:N → orders (orders.user_id → users.id)
  └── 1:N → addresses (addresses.user_id → users.id)
  └── 1:1 → profiles (profiles.user_id → users.id)

orders
  └── N:1 → users (orders.user_id → users.id)
  └── 1:N → order_items (order_items.order_id → orders.id)
  └── N:1 → addresses (orders.shipping_address_id → addresses.id)

order_items
  └── N:1 → orders (order_items.order_id → orders.id)
  └── N:1 → products (order_items.product_id → products.id)
```

For each relationship, specify the ON DELETE behavior and why:
- **CASCADE:** Child records are deleted when parent is deleted (use for tightly coupled data like order → order_items)
- **SET NULL:** Foreign key is set to NULL (use when child can exist without parent)
- **RESTRICT:** Prevent deletion of parent while children exist (use for data integrity, e.g., can't delete a user with active orders)

## DB-S4: Seed Data

If the application requires initial data to function:

```
Table: [table_name]
Seed Data:
  - [describe the records needed — e.g., "default admin user", "initial role types", "system configuration values"]
  - [do not include actual credentials — note that these will be set via environment variables]
Purpose: [why this seed data is required — e.g., "application requires at least one admin to function"]
```

## DB-S5: Migration Script Guidance

The engineer does not produce the full migration script — that's the dev's job. But the engineer specifies what the migration must accomplish:

```
Migration: DB-M-001 — [descriptive name]
Applies: DB-001, DB-002 [which schema items this migration covers]
Steps:
  1. Create [table] with columns as specified in DB-001
  2. Create [table] with columns as specified in DB-002
  3. Add foreign key from [table.column] to [table.column]
  4. Create indexes as specified
  5. Insert seed data if defined

Rollback:
  1. Drop [table] (reverse order of creation)
  2. Remove foreign keys first if cross-table

Ordering Note: [any sequencing requirements — e.g., "users table must exist before orders table due to FK dependency"]
```

For ALTER migrations on production tables with data:

```
Migration: DB-M-005 — [descriptive name]
Applies: DB-010 [alter spec]
Steps:
  1. Add new column with default value (non-locking)
  2. Backfill existing rows with [logic]
  3. Add NOT NULL constraint after backfill (if required)
  4. Add index after data is populated

Downtime Required: [Yes/No — if yes, estimated duration]
Data Risk: [describe any risk of data loss and how to mitigate]
```

## DB-S6: Performance Considerations

```
High-Volume Tables: [tables expected to grow large — note expected row counts]
Query Patterns:
  - [table]: Frequently queried by [column(s)] — ensure index covers this
  - [table]: Frequently joined with [other_table] — ensure FK is indexed
  - [table]: Full-text search needed on [column(s)] — consider GIN index or search engine
Archival: [any tables that should have data retention/archival strategy]
```
