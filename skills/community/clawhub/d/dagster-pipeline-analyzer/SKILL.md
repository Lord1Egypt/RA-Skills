---
name: cm-dagster-pipeline-analyzer
description: Analyze Dagster pipelines and software-defined assets for quality, scheduling, partitioning, IO managers, resource configuration, and observability. Checks asset dependencies, freshness policies, group structure, sensor/schedule configuration, and operational best practices. Use when asked to review Dagster code, audit asset graphs, check Dagster best practices, analyze partition strategies, review IO managers, or optimize Dagster deployments. Triggers on "dagster", "software-defined assets", "dagster assets", "dagster pipeline", "dagster schedule", "dagster sensor", "dagster partition", "io manager", "dagster resources", "dagster ops", "dagster jobs", "asset graph".
metadata:
  tags: ["dagster", "data-engineering", "orchestration", "pipeline", "assets", "partitioning", "scheduling", "data-platform", "etl", "observability"]
---

# Dagster Pipeline Analyzer

Analyze Dagster software-defined assets and pipelines for quality, reliability, and operational excellence. Reviews asset dependency graphs, freshness policies, partitioning strategies, IO managers, resources, sensors/schedules, and observability gaps. Acts as a senior data platform engineer auditing your Dagster deployment.

## Usage

**Basic:** `Analyze the Dagster project in /path/to/dagster/`
**Focused:** `Check asset freshness policies` | `Analyze partition strategies` | `Review IO manager configuration` | `Find assets without observability metadata`

## How It Works

### Step 1: Discover Dagster Definitions

```bash
find /path/to/project -name "definitions.py" -o -name "repository.py"
find /path/to/project -name "*.py" -path "*/assets/*"
find /path/to/project -name "*.py" -path "*/sensors/*" -o -path "*/schedules/*"
cat /path/to/project/dagster.yaml /path/to/project/workspace.yaml 2>/dev/null
```

Parses @asset, @multi_asset, @op, @graph, @job, ConfigurableResource, ConfigurableIOManager, @schedule, @sensor, and partition definitions.

### Step 2: Audit Asset Graph Structure

```
Asset Graph: 34 assets, 5 groups (raw, staging, warehouse, analytics, ml)
Max depth: 7 | External assets: 3 | Source assets: 4

  [source] s3_raw_events -> raw_events -> cleaned_events
    -> event_aggregates -> daily_metrics -> churn_features -> churn_model

  FAIL: "orphan_transform" has no downstream consumers
    Last materialized 49 days ago. Remove or document purpose.

  FAIL: "daily_metrics" depends on 6 upstream assets — fragile bottleneck
    If any upstream fails, materialization blocked.
    RECOMMEND: Add retry logic or partial materialization support

  FAIL: No @asset_check defined for any asset
    RECOMMEND: Add row count, null checks, freshness, schema validation
```

### Step 3: Review Freshness Policies

```
  Assets WITH freshness policy: 8/34 (24%)

  FAIL: "daily_revenue" — no freshness policy on business-critical metric
    FIX: FreshnessPolicy(maximum_lag_minutes=120)

  FAIL: Freshness SLA cascade violation:
    "event_aggregates" has 60-min freshness
    but upstream "cleaned_events" takes ~20 min to materialize
    Effective budget: 10 min. Actual avg: 25 min. SLA violated regularly.
    FIX: Relax to 90 min or speed up materialization

  WARN: "user_segments" has 1440-min (24h) freshness
    but downstream "real_time_recommendations" expects fresh data
    FIX: Tighten to maximum_lag_minutes=60
```

### Step 4: Analyze Partitioning

```
  "raw_events": DailyPartitionsDefinition — PASS, matches data pattern
  "event_aggregates": MonthlyPartitionsDefinition
    WARN: Upstream is daily — verify TimeWindowPartitionMapping
  "ml_features": Unpartitioned, processes 2M+ rows every run (45 min)
    FAIL: Add DailyPartitionsDefinition for incremental processing (~3 min/partition)

  FAIL: No BackfillPolicy on any partitioned asset
    Risk: Accidental backfill of 486 partitions = 486 concurrent runs
    FIX: BackfillPolicy(max_partitions_per_run=10)
```

### Step 5: Review IO Managers

```
  Configured: "io_manager" (Filesystem), "warehouse_io" (Snowflake), "s3_io" (S3Pickle)

  FAIL: Default is FilesystemIOManager — data lost on pod restart
    FIX: Set default to S3/GCS/database-backed store

  FAIL: S3PickleIOManager — not portable, security risk (arbitrary code exec)
    FIX: Switch to S3ParquetIOManager for schema enforcement + compression

  WARN: No return type annotations — IO manager cannot validate schema
    FIX: @asset def daily_metrics(...) -> pd.DataFrame:

  Coverage: warehouse_io 35%, s3_io 24%, filesystem 41% (concern)
```

### Step 6: Audit Resources

```
  FAIL: snowflake_password="..." in definitions.py line 42
    FIX: Use EnvVar("SNOWFLAKE_PASSWORD")

  FAIL: Resource "spark" defined but never used — remove it

  WARN: Resource "dbt" has hardcoded project path
    FIX: Use EnvVar or relative path

  WARN: No resource-level health checks at startup
```

### Step 7: Review Schedules and Sensors

```
  FAIL: "daily_etl" uses cron but assets have DailyPartitionsDefinition
    FIX: build_schedule_from_partitions() for auto-alignment

  FAIL: "s3_file_sensor" polls every 30s — high API cost, rate limit risk
    FIX: minimum_interval_seconds=300 or SQS/SNS event-driven

  FAIL: "freshness_sensor" has no error handling — crashes sensor daemon
    FIX: Wrap in try/except, return SkipReason on failure

  WARN: 14 assets have no automation — manual-only materialization
  WARN: No @asset_sensor for cross-job dependency coordination
```

### Step 8: Check Observability

```
  FAIL: 22/34 assets have no description
  FAIL: No MaterializeResult metadata (no row counts, schema, quality)
    FIX: yield MaterializeResult(metadata={"row_count": len(df), ...})
  FAIL: No asset checks defined
  WARN: No code_version on any asset — always re-materializes
  WARN: No owners defined — alerts not routable

  Coverage: descriptions 35%, freshness 24%, code_version 0%,
            checks 0%, metadata 15%, owners 0%
```

### Step 9: Final Report

```
# Dagster Pipeline Analysis Report

## Overall Health Score: 51/100
  Asset graph: 7/10       Freshness: 4/10       Partitioning: 5/10
  IO managers: 4/10       Resources: 5/10       Schedules/sensors: 5/10
  Observability: 3/10     Security: 4/10        Documentation: 3/10

## Critical Issues
  1. Credentials hardcoded in definitions.py
  2. Default IO manager is local filesystem — data loss risk
  3. Pickle serialization — security + portability risk
  4. No asset checks — data quality issues undetected
  5. No backfill safety — accidental mass materialization risk

## High Priority
  6. 76% assets have no freshness policy
  7. S3 sensor polling every 30s
  8. No materialization metadata
  9. Freshness SLA cascade violation
  10. 14 assets with no automation
```

## Output

- **Asset graph visualization** with dependency depth, bottlenecks, orphans
- **Freshness analysis** with SLA cascade validation
- **Partition audit** covering strategy review and backfill safety
- **IO manager review** for serialization, durability, consistency
- **Resource/schedule/sensor audit** with security and config checks
- **Observability gaps** for metadata, checks, documentation coverage
- **Health score** 0-100 with per-category breakdown and remediation code

## Tips for Best Results

- Point the agent at your Dagster project root directory
- Include dagster.yaml and workspace.yaml for deployment context
- Provide Dagster version for version-appropriate recommendations
- Run before major asset graph changes or quarterly as a health check
