# EMR Serverless Job Management Guide

## Overview

EMR Serverless supports submitting Spark SQL, Spark JAR, PySpark, and Hive jobs. Jobs run on a fully managed serverless infrastructure — no cluster management required.

## Available Operations

All operations are available via `@tool` functions in `scripts/on_serverless/emr_serverless_cli.py`.

## Job Submission

### 1. Submit Spark SQL

Submit a SQL query via an embedded PySpark runner script that auto-uploads to S3.

```python
submit_spark_sql(
    sql="SELECT * FROM my_table LIMIT 10",
    application_id="00abcdef12345678",    # optional, falls back to config
    task_name="my-sql-job",               # optional
    conf={"spark.executor.memory": "4g"}, # optional
    is_sync=True,                          # wait for completion
    timeout=300.0                          # max wait seconds
)
```

**Returns:** Job run info dict with keys: `job_run_id`, `name`, `state`, `application_id`, etc.

After a successful SQL job, retrieve results with `get_job_result(job_run_id)`.

### 2. Submit Spark JAR

```python
submit_spark_jar(
    jar="s3://my-bucket/jars/my-app.jar",
    main_class="com.example.MainClass",
    main_args=["arg1", "arg2"],            # optional
    application_id="00abcdef12345678",     # optional
    task_name="my-jar-job",                # optional
    conf={"spark.executor.cores": "2"},    # optional
    is_sync=True,
    timeout=300.0
)
```

### 3. Submit PySpark

```python
submit_pyspark(
    script="s3://my-bucket/scripts/job.py",
    args=["--input", "s3://bucket/data"],  # optional
    application_id="00abcdef12345678",     # optional
    task_name="my-pyspark-job",            # optional
    conf={},                                # optional
    is_sync=True,
    timeout=300.0
)
```

### 4. Submit Hive Query

```python
submit_hive_query(
    query="SELECT COUNT(*) FROM my_table",
    application_id="00abcdef12345678",     # optional
    task_name="my-hive-job",               # optional
    parameters="--hivevar key=value",      # optional
    is_sync=True,
    timeout=300.0
)
```

## Job Lifecycle

### Get Job Run Status

```python
get_job_run(job_run_id="00abcdef12345678", application_id="...")
```

**Returns:** Detailed dict with keys: `job_run_id`, `name`, `state`, `state_details`, `application_id`, `arn`, `release_label`, `created_by`, `created_at`, `updated_at`, `started_at`, `ended_at`, `execution_role`, `total_execution_duration_seconds`.

### Cancel Job Run

```python
cancel_job_run(job_run_id="00abcdef12345678", application_id="...")
```

**Returns:** `{"job_run_id": "...", "cancelled": true}`

### List Job Runs

```python
list_job_runs(
    application_id="00abcdef12345678",
    states=["RUNNING", "SUCCESS"],         # optional
    max_results=50                          # optional, default 50
)
```

## Results and Logs

### Get SQL Results

Only for Spark SQL jobs that completed successfully:

```python
get_job_result(job_run_id="00abcdef12345678", application_id="...")
```

**Returns:** `{"columns": [...], "rows": [...], "row_count": N}`

### Get Driver Logs

```python
# stdout
get_driver_log(job_run_id="...", application_id="...", max_lines=100, mask_secrets=True)

# stderr
get_stderr_log(job_run_id="...", application_id="...", max_lines=100, mask_secrets=True)
```

Logs are read from S3 at path: `{s3_log_uri}/applications/{app_id}/jobs/{job_run_id}/SPARK_DRIVER/{stdout|stderr}.gz`

## Job States

```
SUBMITTED → PENDING → SCHEDULED → RUNNING → SUCCESS / FAILED / CANCELLED
```

Terminal states: `SUCCESS`, `FAILED`, `CANCELLED`

## Configuration

| Environment Variable | Description | Required |
|---|---|---|
| `AWS_REGION` | AWS region | No (default: us-east-1) |
| `EMR_SERVERLESS_APP_ID` | Default application ID | No (pass per-call) |
| `EMR_SERVERLESS_EXEC_ROLE_ARN` | Execution role ARN | Yes (for job submission) |
| `EMR_SERVERLESS_S3_LOG_URI` | S3 log URI (e.g., `s3://bucket/logs/`) | No (needed for logs/results) |
