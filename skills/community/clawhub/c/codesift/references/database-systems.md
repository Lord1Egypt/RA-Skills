# Database and storage review

Use with SKILL.md and patterns.md. Determine the actual engine, version, workload,
schema, statistics, transaction boundaries and durability requirements first.

## Plans and fast paths

Read EXPLAIN for the real query and parameters. Use EXPLAIN ANALYZE only where
executing the statement is appropriate; it executes the query, including writes.

An existing index plus a sequential scan is not automatically a defect.
Small tables, low selectivity, ordering, statistics and cost settings can justify
that plan. Establish an unsuitable choice on the target workload and measure its
impact. Do not classify severity from plan keywords.

For a custom engine, trace binding, planning, dispatch and execution. Exercise
equivalent supported input variants and compare results. SQLite rowid aliases
are SQLite semantics, not a generic SQL-standard guarantee: table kind, declared
type, shadowing and documented exceptions matter.

## Persistence and transactions

Before changing fsync/sync_all/sync_data or batching, establish:

- What successful commit promises across process and power failures.
- Journal/WAL mode, synchronous setting and filesystem assumptions.
- Whether statements are separate transactions or one explicit transaction.
- Isolation, visibility, crash recovery and cancellation behavior.

Sync count per row is a measurement, not a verdict. Reducing sync can change the
durability contract. Do not equate SQLite commits with exactly one fsync across
all modes. Test failure/recovery semantics in disposable data, never user data.

## Integration and redundant work

Investigate query amplification/N+1, unnecessary connections, metadata rebuilds,
and repeated parsing on important paths. Show query/call counts and response-time
contributions. A small bounded loop or intentionally fresh metadata can be appropriate.
A cache requires an invalidation and consistency contract, not just faster reads.

## Unused paths and gates

Trace whether indexes, cache layers, recovery code and backend adapters are
reachable under supported configurations. Lack of normal-traffic coverage does
not make recovery code dead. Check feature/backend selection and fallback behavior.

For storage checks, identify the invariant and consequence: checksum, version,
schema compatibility, transaction ownership or flush completion. Check that
failure stops or rolls back the relevant mutation. Do not remove a second check
that protects a different trust boundary or a state changed since the first check.

## Comparative measurements

Use the same dataset, query sequence/seed, result validation, transaction sizes,
durability/isolation settings and connection reuse. Prepare data and compile
outside steady-state timing. Measure startup separately if it is the question.
Report repeated samples, warm/cold-cache conditions and workload sizes.

A loop launching one process per query measures process startup as well as the
database. Do not call its ratio an engine-only improvement. Framework benchmark
suite runtime and an individual query latency are different metrics.

## Primary sources

Checked 2026-11-03:

- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html):
  plan choices, small-table scans and actual execution.
- [SQLite rowids and primary keys](https://www.sqlite.org/lang_createtable.html#rowid):
  exact alias rules and exceptions.
- [SQLite synchronous](https://www.sqlite.org/pragma.html#pragma_synchronous):
  journal-mode-dependent durability behavior.
