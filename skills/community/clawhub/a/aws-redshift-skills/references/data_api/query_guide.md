# Redshift Data API Query Guide

## Overview

The Redshift Data API enables you to execute SQL statements without managing database connections. It supports both Redshift Provisioned and Serverless, and is ideal for AI agents, Lambda functions, and other serverless workloads.

## Authentication Modes

### Provisioned Cluster
```
ClusterIdentifier + DbUser  (temporary credentials)
ClusterIdentifier + SecretArn  (Secrets Manager)
```

### Serverless Workgroup
```
WorkgroupName  (uses IAM identity)
WorkgroupName + SecretArn  (Secrets Manager)
```

## SQL Execution

### Async (Default)
1. Call `execute_sql()` → returns statement ID immediately
2. Poll `describe_statement()` to check status
3. When FINISHED, call `get_statement_result()` to retrieve data

### Sync (with polling)
1. Call `execute_sql(is_sync=True)` → waits until completion
2. Returns full statement details including status

### Batch Execution
- Execute multiple SQL statements atomically
- All statements succeed or all fail
- Useful for DDL sequences or multi-step transformations

## Statement Lifecycle

```
SUBMITTED → PICKED → STARTED → FINISHED
                              → FAILED
                              → ABORTED (cancelled)
```

## Result Retrieval

- Results are paginated (default page size varies)
- Use `next_token` to iterate through pages
- Column metadata includes name, type, and label
- Field values are typed (string, long, double, boolean, null)

## COPY Command

Load data from S3 into Redshift:

```sql
COPY tablename FROM 's3://bucket/prefix/'
IAM_ROLE 'arn:aws:iam::123456789:role/redshift-role'
FORMAT AS PARQUET;
```

Supported formats: CSV, JSON, PARQUET, AVRO, ORC

### COPY Options
- `IGNOREHEADER n` — Skip header rows (CSV)
- `DELIMITER ','` — Field delimiter (CSV)
- `GZIP` / `BZIP2` / `LZOP` / `ZSTD` — Compressed files
- `COMPUPDATE ON` — Automatic compression encoding
- `STATUPDATE ON` — Automatic statistics update
- `MAXERROR n` — Maximum errors before failing

## UNLOAD Command

Export query results to S3:

```sql
UNLOAD ('SELECT * FROM sales WHERE year=2026')
TO 's3://bucket/output/'
IAM_ROLE 'arn:aws:iam::123456789:role/redshift-role'
FORMAT AS PARQUET
HEADER
PARALLEL ON;
```

Supported output formats: CSV, JSON, PARQUET

### UNLOAD Options
- `HEADER` — Include column headers (CSV/JSON)
- `PARALLEL ON/OFF` — Parallel file output
- `MAXFILESIZE n` — Maximum output file size
- `ALLOWOVERWRITE` — Overwrite existing files
- `ADDQUOTES` — Enclose strings in quotes (CSV)

## Metadata Operations

- **list_databases** — List all databases
- **list_schemas** — List schemas (supports LIKE patterns)
- **list_tables** — List tables (supports LIKE patterns)
- **describe_table** — Get column definitions

## Limits and Quotas

- Maximum SQL statement length: 100 KB
- Maximum result set size: 100 MB
- Statement timeout: 24 hours (default)
- Maximum active statements: 200
- Batch statement limit: 40 SQL statements per batch

## Best Practices

1. Use async execution for long-running queries
2. Set appropriate timeouts for sync execution
3. Use named statements for tracking
4. Paginate large result sets
5. Use PARQUET format for COPY/UNLOAD (best performance)
6. Use COPY with manifests for exact file control
7. Monitor statement history with list_statements
8. Cancel runaway queries promptly
