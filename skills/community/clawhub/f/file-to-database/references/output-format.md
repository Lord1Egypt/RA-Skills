# Deliverable Output Format

file-to-database-skill produces a standard set of deliverables on every run, laid out as follows:

```
output/
├── schema.sql          # DDL (tables, constraints, indexes)
├── erd.md              # Mermaid ERD
├── seed.py             # imports data from source files (or seed.sql)
├── migrations/
│   └── 001_init.up.sql / 001_init.down.sql
└── report.md           # modeling report (see below)
```

## schema.sql requirements

- File-header comment: generation time, target engine, source-file list
- One section per table; the table comment states the source file
- Every index annotated with the query it serves: `-- serves Q3: SELECT ... WHERE user_id = ? ORDER BY created_at`
- Every foreign key annotated with the reason for its ON DELETE choice
- Every denormalized column must carry a comment naming the query it serves

## erd.md requirements

Mermaid `erDiagram`, with cardinality and FK columns annotated between entities.

## report.md template

```markdown
# Database Modeling Report

## Input
- Source files: … (row counts, sampling notes)

## Decision Record
| # | Decision | Basis (methodology clause) |
|---|----------|----------------------------|

## Open Questions (asked / pending)
- …

## Foreign-Key Adjudication
(the three tiers from detect_relations.py: adopt / ask_user / ignore)

## Verification Results
- Constraint negative tests: X/X passed
- EXPLAIN index hits: Q1 ✓ Q2 ✓ …
- Or: no database environment; manual walkthrough per the checklist completed
```
