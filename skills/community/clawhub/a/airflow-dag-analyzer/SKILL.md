---
name: cm-airflow-dag-analyzer
description: Analyze Apache Airflow DAG definitions for quality, reliability, and operational best practices. Checks task dependencies, SLA compliance, retry policies, resource allocation, sensor timeouts, trigger rules, pool usage, and DAG complexity. Use when asked to review Airflow DAGs, audit DAG quality, check Airflow best practices, analyze task dependencies, optimize DAG performance, review Airflow configuration, or troubleshoot DAG failures. Triggers on "airflow", "DAG", "airflow dag", "dag review", "airflow audit", "task dependencies", "airflow best practices", "dag quality", "airflow optimization", "dag analysis", "airflow troubleshoot", "dag performance".
metadata:
  tags: ["airflow", "data-engineering", "orchestration", "dag", "pipeline", "scheduling", "etl", "data-pipeline", "workflow", "reliability"]
---

# Airflow DAG Analyzer

Analyze Apache Airflow DAG definitions for quality, reliability, and operational excellence. Reviews task dependencies, retry policies, SLA configurations, resource allocation, sensor patterns, error handling, and DAG structure. Acts as a senior data platform engineer auditing your Airflow deployment.

## Usage

Invoke this skill when you need to review Airflow DAGs for quality issues, optimize performance, or ensure operational best practices.

**Basic invocation:**
> Analyze the Airflow DAGs in /path/to/dags/
> Review this DAG file for best practices
> Check DAG quality for production readiness

**Focused analysis:**
> Check retry policies across all DAGs
> Find DAGs without SLA configurations
> Analyze task dependency structure for bottlenecks
> Review sensor configurations for timeout risks

The agent reads DAG Python files, parses task definitions, and produces a comprehensive quality report.

## How It Works

### Step 1: Discover and Parse DAG Files

The agent locates and reads all DAG definitions:

```bash
# Find all DAG files
find /path/to/dags/ -name "*.py" -type f

# Identify which files contain DAG definitions
grep -rl "DAG\|@dag" /path/to/dags/ --include="*.py"

# Check for dynamic DAG generation
grep -rn "globals()\|create_dag\|dag_factory\|generate_dag" /path/to/dags/ --include="*.py"
```

The agent parses each DAG file to extract:
- **DAG ID and description**
- **Schedule interval** (cron expression or preset)
- **Default arguments** (default_args dict)
- **Task definitions** (operators, task IDs, dependencies)
- **Task group structure** (TaskGroups for logical grouping)
- **Callbacks** (on_failure, on_success, on_retry, SLA miss)
- **Tags and owners** for organizational metadata
- **Imports and custom operators** for dependency analysis

### Step 2: Audit DAG-Level Configuration

The agent checks each DAG's top-level configuration:

**Schedule configuration:**

```python
# GOOD: Explicit schedule with catchup disabled
dag = DAG(
    dag_id="etl_daily_orders",
    schedule_interval="0 6 * * *",
    catchup=False,
    start_date=datetime(2026, 1, 1),
    tags=["etl", "orders", "production"],
)

# PROBLEMS the agent detects:
```

```
FAIL: dag_id="etl_daily_orders"
  catchup=True (default) — will backfill all dates from start_date
  RISK: Accidental mass backfill on deploy, resource exhaustion
  FIX: Set catchup=False unless intentional backfill is needed

FAIL: dag_id="report_generator"
  start_date=datetime.now() — dynamic start_date
  RISK: Start date changes on every scheduler restart, breaks idempotency
  FIX: Use a fixed date: start_date=datetime(2026, 1, 1)

WARN: dag_id="data_sync"
  No schedule_interval defined — DAG defaults to daily
  FIX: Explicitly set schedule_interval (even if daily)

FAIL: dag_id="ml_training"
  max_active_runs=None (unlimited)
  RISK: Overlapping runs cause resource contention and data corruption
  FIX: Set max_active_runs=1 for data pipelines

WARN: dag_id="analytics_refresh"
  No tags defined
  FIX: Add tags for filtering in the UI: tags=["analytics", "production"]

WARN: dag_id="customer_export"
  No doc_md or description
  FIX: Add DAG documentation for operators and on-call engineers
```

**Default arguments audit:**

```python
# The agent checks default_args for completeness:
default_args = {
    "owner": "data-team",               # WHO: Required for accountability
    "depends_on_past": False,            # DEPENDENCY: Usually False for resilience
    "email": ["data-team@company.com"],  # ALERTS: Team email for notifications
    "email_on_failure": True,            # ALERTS: Must be True for production
    "email_on_retry": False,             # ALERTS: Usually False (too noisy)
    "retries": 3,                        # RESILIENCE: Required for production
    "retry_delay": timedelta(minutes=5), # RESILIENCE: Required with retries
    "retry_exponential_backoff": True,   # RESILIENCE: Prevents thundering herd
    "max_retry_delay": timedelta(minutes=60),
    "execution_timeout": timedelta(hours=2),  # SAFETY: Prevents hanging tasks
    "sla": timedelta(hours=4),           # SLA: When should we be concerned
    "on_failure_callback": alert_slack,  # ALERTS: Custom alerting
}
```

```
Default Args Audit: etl_daily_orders

  FAIL: No "retries" defined — tasks will not retry on transient failures
        Production DAGs should have retries >= 2
  
  FAIL: No "execution_timeout" — tasks can hang indefinitely
        Risk: Zombie tasks consuming worker slots for hours/days
        Recommend: Set based on expected duration + buffer (2x typical)

  FAIL: No "on_failure_callback" — team not notified on failures
        Recommend: Add Slack/PagerDuty callback for production DAGs

  WARN: No "sla" defined — no SLA tracking
        Recommend: Set SLA based on business requirements

  WARN: "owner" = "airflow" (default) — no ownership attribution
        Recommend: Set to team or individual responsible for the DAG

  PASS: "depends_on_past" = False — good for resilience
  PASS: "email_on_failure" = True — email alerts configured
```

### Step 3: Analyze Task Dependencies and DAG Structure

The agent maps the dependency graph and checks for structural issues:

```
DAG Structure Analysis: etl_daily_orders

  Tasks: 14
  Max depth: 6 (levels of sequential dependencies)
  Max width: 4 (maximum parallel tasks at any level)
  Critical path: extract -> validate -> transform -> aggregate -> load -> notify
  Critical path duration: estimated 45 min (sum of median task durations)

  Dependency Graph:
    extract_orders ─┐
    extract_items  ─┤
    extract_users  ─┴─> validate_data ─> transform ─> aggregate ─┐
                                                                    ├─> load_warehouse
    extract_config ────────────────────────────────────────────────┘
                                                                    └─> load_cache
    load_warehouse ─┐
    load_cache     ─┴─> run_tests ─> notify_complete
```

**Structural checks:**

```
FAIL: Task "transform" has 3 upstream dependencies but creates a bottleneck
  All downstream tasks wait for transform to complete
  RECOMMEND: Split transform into independent sub-tasks that can run in parallel:
    transform_orders, transform_items, transform_users

FAIL: Linear chain of 6 tasks where 3 could run in parallel
  extract -> validate -> transform -> test -> load -> notify
  RECOMMEND: Parallelize extract tasks, parallelize test + load where possible

WARN: Task "extract_config" has no downstream dependencies
  This task runs but nothing depends on its output
  Is this intentional? May be a dead task.

WARN: DAG has 14 tasks — approaching complexity threshold
  RECOMMEND: Consider using TaskGroups to organize related tasks

FAIL: Circular dependency risk detected in dynamic task generation
  Loop generates tasks but dependency chain references previous iteration
  RISK: Can create circular dependency at runtime depending on data
```

**Fan-out / fan-in analysis:**

```
Fan-out at "validate_data": 1 -> 4 tasks
  OK: Reasonable parallelism

Fan-in at "load_warehouse": 4 -> 1 tasks
  WARN: Single point of failure — if any upstream fails, load fails
  Consider: Use trigger_rule="none_failed_min_one_success" if partial loads acceptable
```

### Step 4: Review Retry and Error Handling Policies

The agent evaluates resilience configuration:

```
Retry Policy Analysis:

  Task: extract_api_data
    retries: 0    <-- FAIL: API calls should always retry
    Recommend: retries=3, retry_delay=timedelta(minutes=2),
               retry_exponential_backoff=True

  Task: load_to_warehouse
    retries: 5, retry_delay: 1 minute
    WARN: 5 retries * 1 min = only 5 min total retry window
    For warehouse operations, recommend:
      retries=3, retry_delay=timedelta(minutes=5),
      retry_exponential_backoff=True,
      max_retry_delay=timedelta(minutes=30)
    This gives ~35 min retry window for transient warehouse issues

  Task: send_email_report
    retries: 10, retry_delay: 10 seconds
    WARN: Aggressive retry on email — may trigger rate limits
    Recommend: retries=3, retry_delay=timedelta(minutes=1)
```

**Trigger rule analysis:**

```
  Task: run_quality_checks
    trigger_rule: "all_success" (default)
    OK: Quality checks should only run if all data loaded

  Task: send_failure_alert
    trigger_rule: "all_success" (default)
    FAIL: Alert task should fire on failure
    FIX: trigger_rule="one_failed" or "all_done"

  Task: cleanup_temp_files
    trigger_rule: "all_success"
    WARN: Cleanup won't run if upstream fails — temp files accumulate
    FIX: trigger_rule="all_done" — cleanup should always run
```

### Step 5: Audit Sensor Configurations

Sensors are a common source of production issues. The agent checks each sensor:

```
Sensor Analysis:

  FAIL: ExternalTaskSensor("wait_for_upstream_dag")
    mode="poke" (default), poke_interval=60s, timeout=3600s
    PROBLEM: Poke mode holds a worker slot while waiting
    At 60s interval for up to 1 hour = 1 worker slot blocked
    FIX: mode="reschedule" — releases worker between pokes

  FAIL: S3KeySensor("wait_for_file")
    timeout=7200s (2 hours), no explicit timeout action
    PROBLEM: If file never arrives, sensor blocks for 2 hours then fails
    FIX: Add soft_fail=True to skip downstream tasks gracefully
    OR: Add on_failure_callback to alert when file is late

  WARN: SqlSensor("check_data_ready")
    poke_interval=30s
    PROBLEM: Polling database every 30s for extended periods
    FIX: Increase poke_interval to 300s, use mode="reschedule"

  WARN: HttpSensor("wait_for_api")
    No exponential_backoff=True
    RISK: Fixed-interval polling may hit rate limits
    FIX: Add exponential_backoff=True
```

**Sensor best practices checklist:**

| Setting | Recommended | Why |
|---------|-------------|-----|
| `mode` | `"reschedule"` | Releases worker slot between pokes |
| `timeout` | Set explicitly | Prevents indefinite waits |
| `poke_interval` | 300s+ for external deps | Reduces load on external systems |
| `soft_fail` | `True` for optional deps | Prevents blocking entire DAG |
| `exponential_backoff` | `True` for APIs | Prevents rate limiting |

### Step 6: Check Resource Allocation

The agent reviews resource configuration:

```
Resource Analysis:

  WARN: No pool assignments detected
    All 14 tasks run in default pool (128 slots)
    RISK: This DAG competes with all other DAGs for worker slots
    RECOMMEND: Assign pools for resource-intensive tasks:
      - "api_pool" (limit=5) for API extraction tasks
      - "warehouse_pool" (limit=10) for database operations

  WARN: Task "heavy_transform" has no resource constraints
    KubernetesPodOperator without resource requests/limits
    RISK: Can consume unlimited cluster resources
    FIX: Add resources=k8s.V1ResourceRequirements(
           requests={"memory": "2Gi", "cpu": "1"},
           limits={"memory": "4Gi", "cpu": "2"}
         )

  WARN: No priority_weight set on critical path tasks
    All tasks have equal priority (default=1)
    RECOMMEND: Set higher priority_weight for critical path tasks
    to ensure they're scheduled first when workers are constrained
```

### Step 7: Validate Operator Usage

The agent checks that operators are used correctly:

```
Operator Analysis:

  FAIL: BashOperator with inline script (15 lines)
    Task: "complex_transformation"
    PROBLEM: Complex logic in BashOperator is hard to test and maintain
    FIX: Move to PythonOperator or a standalone script

  FAIL: PythonOperator calling subprocess.run()
    Task: "run_spark_job"
    PROBLEM: Bypasses Airflow's operator framework
    FIX: Use SparkSubmitOperator or BashOperator for CLI commands

  WARN: BranchPythonOperator without join task
    Task: "check_data_quality"
    Branches to "process_good_data" or "handle_bad_data"
    But no downstream join — one branch's downstream tasks are skipped
    RECOMMEND: Add a join task with trigger_rule="none_failed_min_one_success"

  WARN: Multiple ShortCircuitOperator in sequence
    Tasks: "check_weekday", "check_data_exists", "check_flag"
    PROBLEM: Unclear which condition caused the circuit to break
    FIX: Combine conditions or add logging to each operator

  FAIL: Using SubDagOperator
    Task: "process_subtasks"
    SubDagOperator is DEPRECATED and causes deadlocks
    FIX: Replace with TaskGroup (Airflow 2.0+)
```

### Step 8: Review SLA and Monitoring Configuration

The agent checks operational visibility:

```
SLA Configuration:

  FAIL: 8 of 12 production DAGs have no SLA defined
    DAGs without SLA: etl_orders, etl_users, report_daily, ...
    RISK: Data pipeline delays go unnoticed until stakeholders complain

  WARN: DAG "etl_critical" has SLA=6 hours, schedule=daily
    SLA allows data to be 6+ hours late before alert
    RECOMMEND: Tighten to 2 hours based on downstream consumer requirements

  FAIL: No sla_miss_callback defined for any DAG
    Email-only SLA alerts are often missed
    RECOMMEND: Add callback for Slack/PagerDuty integration

Monitoring Gaps:
  FAIL: No task-level execution_timeout on 23 tasks
    Risk: Zombie tasks silently consume resources
  
  WARN: No Airflow metrics exported (statsd/prometheus)
    Recommend: Enable statsd metrics for:
      - scheduler.heartbeat
      - dag_processing.total_parse_time
      - executor.open_slots
      - task_instance.duration
```

### Step 9: Check Idempotency and Data Safety

The agent evaluates whether DAGs are safe to re-run:

```
Idempotency Analysis:

  FAIL: Task "load_orders" uses INSERT without UPSERT logic
    Re-running this task will create duplicate rows
    FIX: Use INSERT ... ON CONFLICT DO UPDATE (PostgreSQL)
    OR: Use MERGE statement (Snowflake/BigQuery)
    OR: Use DELETE+INSERT pattern within a transaction

  FAIL: Task "export_to_s3" writes to fixed S3 key
    s3://bucket/exports/orders.csv
    Re-running overwrites without versioning
    FIX: Use execution_date in path:
      s3://bucket/exports/orders/{{ ds }}/orders.csv

  WARN: Task "send_notification" has no idempotency check
    Re-running sends duplicate Slack messages
    RECOMMEND: Add check for already-sent notification for this execution_date

  PASS: Task "create_report" uses execution_date in output path
    Safe to re-run — produces same output for same execution_date
```

### Step 10: Produce the Analysis Report

The agent generates a comprehensive report:

```
# Airflow DAG Analysis Report
# DAGs Directory: /opt/airflow/dags/ | Date: April 30, 2026

## Overview
  Total DAGs: 12
  Total tasks: 87
  Production DAGs: 9
  Development DAGs: 3

## Overall Health Score: 58/100

## Category Scores
  DAG Configuration:    6/10  (catchup, schedule, max_active_runs)
  Default Args:         4/10  (retries, timeouts, callbacks)
  Task Dependencies:    7/10  (DAG structure, bottlenecks)
  Retry Policies:       5/10  (missing retries, bad intervals)
  Sensor Config:        4/10  (poke mode, no timeouts)
  Resource Allocation:  5/10  (no pools, no limits)
  Operator Usage:       6/10  (deprecated operators, misuse)
  SLA & Monitoring:     3/10  (missing SLAs, no callbacks)
  Idempotency:          5/10  (duplicate risk on re-run)
  Code Quality:         7/10  (imports, structure, DRY)

## Critical Issues (Production Risk)
  1. 8 DAGs have catchup=True — risk of accidental mass backfill
  2. 23 tasks have no execution_timeout — zombie task risk
  3. SubDagOperator in use — deprecated, causes deadlocks
  4. 4 sensors using poke mode — blocking worker slots
  5. No SLA monitoring on critical data pipelines

## High Priority
  6. No retry policies on API-dependent tasks
  7. No pools configured — resource contention risk
  8. INSERT without upsert — duplicate data on re-runs
  9. No failure callbacks — team not alerted on failures

## Recommendations Summary
  Estimated effort: 3-5 days for critical + high priority fixes
  Expected improvement: 58 -> 82 health score
  Risk reduction: Eliminates 4 classes of production incidents
```

## Output

The agent produces:

- **Health score**: 0-100 overall DAG quality rating
- **Category scores**: granular ratings for each quality dimension
- **Critical issues**: problems that pose immediate production risk
- **Per-DAG analysis**: configuration audit for each DAG
- **Per-task findings**: specific task-level issues with fix recommendations
- **Dependency visualization**: text-based DAG structure with bottleneck annotations
- **Remediation code**: exact Python code to fix each issue
- **Priority matrix**: issues ranked by risk and effort

## Scope Options

| Scope | What It Covers |
|-------|---------------|
| **Full** (default) | All DAGs, all checks |
| **Single DAG** | Deep analysis of one DAG file |
| **Category** | One check category across all DAGs (e.g., only retry policies) |
| **Production only** | Only DAGs tagged as production |
| **Changed** | Only DAG files changed in current git branch |

## Airflow Version Support

The agent adapts its recommendations based on the Airflow version detected:

| Feature | Airflow 1.x | Airflow 2.x |
|---------|-------------|-------------|
| TaskGroups | N/A (use SubDagOperator) | Recommended over SubDag |
| TaskFlow API | N/A | Recommended for Python tasks |
| Timetables | N/A | Recommended over cron strings for complex schedules |
| Dynamic Task Mapping | N/A | Recommended for variable task counts |
| Dataset-driven scheduling | N/A | Recommended for event-driven pipelines (2.4+) |

## Tips for Best Results

- Point the agent at your actual DAGs directory for a real audit
- Provide Airflow version info for version-appropriate recommendations
- Include custom operators and utility modules in the scan path
- For the most thorough analysis, also share Airflow configuration (airflow.cfg) so the agent can cross-reference pool sizes, executor type, and parallelism settings
- Run this analysis before major DAG deployments or as a quarterly health check
- Combine with log analysis to correlate code issues with actual failure patterns
