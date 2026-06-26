# EMR On EKS Job Run Management Guide

## Overview

EMR on EKS submits Spark workloads to Kubernetes via the `emr-containers` API. Jobs run as Kubernetes pods in the namespace associated with the virtual cluster.

## Available Operations

All operations are available via `@tool` functions in `scripts/on_eks/emr_on_eks_cli.py`.

## Job Submission

### 1. Submit Spark Job

Submit a Spark job (JAR or PySpark script) via `sparkSubmitJobDriver`:

```python
submit_eks_spark_job(
    entry_point="s3://bucket/scripts/my_job.py",
    virtual_cluster_id="abc123def456",              # optional, falls back to config
    name="my-spark-job",                             # optional
    execution_role_arn="arn:aws:iam::123:role/emr",  # optional, falls back to config
    release_label="emr-7.1.0-latest",               # optional
    entry_point_args=["--input", "s3://data/"],      # optional
    spark_submit_params="--conf spark.executor.instances=10 --conf spark.executor.memory=4G",  # optional
    conf={"spark.dynamicAllocation.enabled": "true"},# optional (applicationConfiguration)
    s3_log_uri="s3://bucket/logs/",                  # optional
    is_sync=False,                                    # wait for completion
    timeout=600                                       # max wait seconds
)
```

**Returns:** Job run dict with keys: `id`, `name`, `arn`, `virtual_cluster_id`, `state`, `state_details`, `created_at`, `finished_at`, `execution_role_arn`, `release_label`.

### 2. Submit Spark SQL

Submit a Spark SQL query via `sparkSqlJobDriver`:

```python
submit_eks_spark_sql(
    sql_entry_point="s3://bucket/queries/my_query.sql",
    virtual_cluster_id="abc123def456",
    name="my-sql-job",
    release_label="emr-7.1.0-latest",
    spark_sql_params="--conf spark.sql.shuffle.partitions=100",
    s3_log_uri="s3://bucket/logs/",
    is_sync=False,
    timeout=600
)
```

## Job Lifecycle

### Describe Job Run

```python
describe_eks_job_run(
    job_run_id="xyz789",
    virtual_cluster_id="abc123def456"               # optional, falls back to config
)
```

**Returns:** Detailed dict with keys: `id`, `name`, `virtual_cluster_id`, `arn`, `state`, `state_details`, `failure_reason`, `created_at`, `created_by`, `finished_at`, `execution_role_arn`, `release_label`, `job_driver`, `configuration_overrides`, `tags`.

### List Job Runs

```python
list_eks_job_runs(
    virtual_cluster_id="abc123def456",               # optional
    states=["RUNNING", "COMPLETED"],                  # optional
    max_results=50                                     # optional
)
```

### Cancel Job Run

```python
cancel_eks_job_run(
    job_run_id="xyz789",
    virtual_cluster_id="abc123def456"
)
```

**Returns:** `{"id": "...", "virtual_cluster_id": "...", "status": "cancel_requested"}`

## Job Logs

### Get Job Log from S3

```python
get_eks_job_log(
    job_run_id="xyz789",
    virtual_cluster_id="abc123def456",
    log_type="stderr",       # stderr (default) or stdout
    max_lines=200,
    mask_secrets=True
)
```

**S3 log path structure:**
```
s3://{log_uri}/{virtual_cluster_id}/jobs/{job_run_id}/containers/
    spark-{id}/
        spark-{id}-driver/
            stdout.gz
            stderr.gz
        spark-{id}-exec-1/
            stdout.gz
            stderr.gz
```

> The exact container path is discovered automatically via S3 listing.

## Job Run States

```
PENDING → SUBMITTED → RUNNING → COMPLETED
                              → FAILED
                              → CANCEL_PENDING → CANCELLED
```

Terminal states: `COMPLETED`, `FAILED`, `CANCELLED`

### Failure Reasons

| Reason | Description |
|---|---|
| `INTERNAL_ERROR` | AWS internal error |
| `USER_ERROR` | Error in user code or configuration |
| `VALIDATION_ERROR` | Invalid request parameters |
| `CLUSTER_UNAVAILABLE` | EKS cluster is unavailable |

## Monitoring Configuration

When submitting jobs, configure logging via:

- **S3**: Set `s3_log_uri` parameter — logs written to S3 in gzip format
- **CloudWatch**: Set `cloudwatch_log_group` parameter — logs streamed to CloudWatch

## Configuration

| Environment Variable | Description | Required |
|---|---|---|
| `AWS_REGION` | AWS region | No (default: us-east-1) |
| `EMR_EKS_VIRTUAL_CLUSTER_ID` | Default virtual cluster ID | No (pass per-call) |
| `EMR_EKS_EXEC_ROLE_ARN` | Default execution role ARN | Yes (for job submission) |
| `EMR_SERVERLESS_S3_LOG_URI` | S3 log URI for log retrieval | No (needed for logs) |
