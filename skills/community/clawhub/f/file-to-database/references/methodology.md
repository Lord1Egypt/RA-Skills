# Database Design Methodology (pluggable)

> This file is the methodological core of file-to-database-skill. Replace this file to switch the entire design style.
> The current version is adapted from Cursor community best practices (staged loop + query-driven indexing).

## Core Principles

1. **Constraints live in the database, not the application layer** — data rules that exist only in application code will sooner or later be broken by the next script or a manual fix. NOT NULL, UNIQUE, CHECK, and foreign keys (with an explicit ON DELETE) must land in the DDL.
2. **Indexes are derived from queries, not from a checklist** — every frequent query should be able to name "which index serves me"; an index with no query behind it is a liability.
3. **Every stage leaves a checkable artifact** — correctness rests on tests and EXPLAIN, not on a human reading generated SQL.
4. **Normalization is the default; denormalization is the exception** — start from 3NF; denormalize only for a named query, and record it in a comment.

## Information you must obtain before modeling (ask for each missing item; never guess)

- Target engine and version (default PostgreSQL 18)
- Natural-language description of entities and relationships (data files themselves can partially substitute)
- The 5–10 most important/frequent queries (including filters and sort orders)
- Data volume and growth (rows per year), read/write ratio
- Multi-tenancy? Retention policy? PII / deletion requests / audit requirements?
- The migration tool in use (Prisma / Drizzle / Alembic / raw SQL)

## Type Selection Rules (PostgreSQL defaults)

| Scenario | Choice |
|---|---|
| Primary key | `bigint generated always as identity` or `uuid DEFAULT uuidv7()` (uuid only for distributed writes) |
| Strings | `text` (not varchar(n), unless there is a real business cap) |
| Timestamps | always `timestamptz` |
| Money | `numeric` (never float) |
| Booleans | `boolean`; never int 0/1 as a substitute |
| Enumerations | start with `text + CHECK (col IN (...))`; consider an enum type only once values are stable |

Other engines: see `references/other-engines.md`.

## File → Table Mapping Rules

1. One data file maps to one table by default; table name = file name (plural, snake_case)
2. Wide-table split triggers (split only when one holds; note the split in the ERD):
   - A 1:N embedded structure exists (e.g. a column holding JSON arrays) → split into a child table
   - A transitive dependency unrelated to the primary key exists → split out the columns violating 3NF
   - The same entity's information repeats across multiple files → merge into one table
3. N:M relationships must use an explicit junction table; comma-separated columns are forbidden
4. "Display order"/"row number" columns in source files that have no business meaning → drop (note it in the delivery report)

## Foreign-Key Adjudication (output by detect_relations.py; adjudicate per these rules)

- High confidence (≥0.8): name match (`user_id` ↔ `users.id`) and 100% value-set containment → adopt directly
- Medium confidence (0.5–0.8): value-set containment but name mismatch → list the evidence and ask the user
- Low confidence (<0.5): name similarity only → ignore; mention it in the report
- One-to-one: FK column is also UNIQUE → annotate 1:1

## Index Derivation Procedure

For each frequent query:
1. Find the filter columns, sort columns, and JOIN columns
2. Name an index for it (composite index column order = equality columns first, range columns after)
3. Index every foreign-key column used in JOINs or cascades — Postgres does not do this automatically
4. Do not duplicate coverage already provided by UNIQUE or primary keys

## Constraint Testing (run all of these when a database is available)

Write one negative test per business rule: insert a row that should be rejected and assert the database errors.
A constraint that has never been tested = a constraint nobody knows works.

## Migration Strategy

Expand-and-contract: add new columns/tables (expand) → dual-write and migrate data (migrate) → drop old columns (contract).
Every migration must ship with a rollback script.

## Ask-Checkpoint Pattern (ask only at branch points; act directly elsewhere)

Principles: do not ask about anything deterministically derivable from the data (asking looks dumb); always ask about semantic ambiguity (wrong guesses cost the most rework); always ask about business requirements (they are invisible in the data). When asking, bring evidence and offer multiple choice — never open-ended questions.

```
files → type detection → full-scan profiling        (uncontroversial, don't ask)
    → [Checkpoint 1] ambiguity confirmation          with evidence: "3 user_id values
         │                                            don't exist in users — dirty
         ▼                                            data, or dangling refs allowed?"
    FK/entity inference → three-tier verdicts (adopt directly / ask_user listed / ignore)
    → [Checkpoint 2] requirements confirmation       frequent queries, retention, PII
         ▼
    modeling → DDL → verification                     (uncontroversial, don't ask)
```

- **Checkpoint 1 (after profiling)**: mixed-type columns, overlong-text truncation, encoding anomalies, dangling FK values, duplicate entities across files — each with sample values and statistical evidence, offering 2–3 options.
- **Checkpoint 2 (before modeling)**: the items in the "information you must obtain" list that the data itself cannot answer.
- The two checkpoints may be merged into a single interaction but must not be skipped; if the user does not answer, proceed with the methodology defaults and mark "adopted by default, unconfirmed" in the report.

## Final Checklist (tick every item before delivery)

- [ ] Every table has a primary key; every column has an explicit type
- [ ] All business rules are encoded as constraints, and every constraint has a negative test
- [ ] Every frequent query has a matching index, confirmed by EXPLAIN
- [ ] Every foreign key has an explicit ON DELETE policy with a stated reason
- [ ] ERD and DDL agree (tables, columns, relationships all aligned)
- [ ] The seed script runs through on an empty database in one pass
- [ ] All timestamps are timestamptz; all money is numeric
- [ ] Every denormalized spot has a comment naming the query it serves
