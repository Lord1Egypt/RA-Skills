# Rails Money And State Checks

The Rails-specific money and state checks, and the findings that are usually block-merge.

## Rails-specific money and state checks

- **Migrations and defaults.** A new NOT NULL column without a default
  breaks existing rows. A new column with a default silently changes the
  meaning of existing queries.
- **Counter caches.** Updated in the same transaction as the row, or they
  drift. Check that a rollback does not leave the counter wrong.
- **Validations vs database constraints.** A model-level validation can be
  bypassed by `update_column`, `update_all`, or `insert_all`. Check whether
  any code path does that on a validated field.
- **Scopes and default ordering.** A scope with `default_scope` or an
  implicit ordering that the query does not expect will produce different
  results in a test than in production, once the data set grows.
- **Serialization and caching.** A cached fragment that includes a
  permission-dependent value will serve one user's data to another.
- **Enums.** A string column with a value outside the enum raises on write.
  A renamed enum value is a data migration, not just a code change.

---
