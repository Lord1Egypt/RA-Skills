---
name: testing-policy
description: Persistence-heavy changes should be validated against a real database
type: working-style
---

When changing queries, migrations, or persistence-sensitive code, prefer tests that touch a real database over mock-only coverage.

Why:
The team has been burned by mock-based tests passing while a production migration or SQL behavior failed.

How to apply:
If the work touches schema, query generation, or transactions, add or run integration coverage before declaring the change safe.
