---
name: ask-the-data
description: >
  Part of the Overpowered skill suite.
  Answer reproducible questions from structured data files such as Excel, CSV, JSON, TSV, or Parquet by discovering useful inputs, reading data dictionaries, loading durable relations when helpful, inspecting schema, querying only what is needed, and returning traceable results. Use when the answer is in tabular/structured files rather than prose documents.
compatibility: >
  Best with a structured-data/DuckDB capability. Designed to compose with a lower-level `structured-data-duckdb` skill when present; can use equivalent local tabular tools otherwise.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "1-knowledge"
  version: "0.1.0"
---

# Overpowered / Ask the Data

## Promise

**Drop structured files in a project and ask questions. Return answers that can be traced back to the data and query logic.**

## Preferred implementation

If a `structured-data-duckdb` skill is available, delegate workbook inspection, table selection, ingestion, schema inspection, sampling, and DuckDB operations to it. Do not duplicate its low-level mechanics.

## Input conventions

These are helpful, not mandatory:

```text
data/                  structured source files and dictionaries
TASK.md                recurring questions or analysis objectives
*.xlsx *.csv *.json *.parquet *.tsv
```

Data dictionaries may be Markdown, Word, PDF, Excel, JSON, or other readable artifacts. Use them to resolve business meaning, not merely column names.

## Project reference

Read `references/project-conventions.md` when the project has multiple data files, dictionaries, recurring questions, or would benefit from persistent DuckDB state.

## Procedure

1. Discover relevant structured files and nearby dictionaries.
2. Read dictionaries first when column semantics or codes are non-obvious.
3. Inspect schemas/sheets before loading everything.
4. Load only useful relations into DuckDB or the available structured-data engine; persist when repeated questioning is likely.
5. Inspect schema and representative samples before writing analytical queries.
6. Translate the user's question into explicit filters, joins, aggregations, and definitions.
7. Execute the minimal reproducible query.
8. Validate suspicious results with counts, uniqueness checks, null checks, or targeted samples.
9. Return the answer with provenance sufficient to reproduce it.

## Output contract

```text
Answer
[direct answer]

Evidence
- source files / tables
- business definitions used
- filters / assumptions
- query or concise query summary
- validation checks
```

Show full SQL when it improves reproducibility; otherwise keep it concise and offer/store it as an artifact when the harness supports files.

## Gotchas

- Do not guess sheet meaning from names when dictionaries exist.
- Do not load every workbook tab by default.
- Do not silently coerce identifiers, dates, currencies, units, or codes.
- Do not claim a business definition from a column name alone.
- Distinguish “no matching rows” from “data unavailable or not loaded.”

## Composition

- Ambiguous business meaning → `know-enough` or inspect dictionaries.
- Conflicting definitions/sources → `reconcile`.
- Comparing snapshots → `what-changed`.
- Before a strong completion claim → `completion-audit`.

## Stop condition

Stop when the user's question is answered from a reproducible query and material data-quality caveats are explicit.
