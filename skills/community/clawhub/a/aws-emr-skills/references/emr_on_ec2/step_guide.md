# EMR On EC2 Step Management Guide

## Overview

Steps are units of work submitted to an EMR cluster. Each step runs a Hadoop job (Spark, Hive, custom JAR, etc.) via the `command-runner.jar` mechanism.

## Available Operations

All operations are available via `@tool` functions in `scripts/on_ec2/emr_on_ec2_cli.py`.

## Step Submission

### 1. Add Spark Step (JAR or PySpark)

Submit a Spark job via `spark-submit`:

```python
add_spark_step(
    cluster_id="j-XXXXXXXXXXXXX",
    entry_point="s3://bucket/jars/my-app.jar",  # JAR or PySpark script
    main_class="com.example.Main",                # required for JAR, omit for PySpark
    args=["arg1", "arg2"],                         # optional
    name="My Spark Job",                           # optional
    conf={"spark.executor.memory": "4g"},          # optional
    deploy_mode="cluster",                         # cluster (default) or client
    action_on_failure="CONTINUE"                   # CONTINUE | CANCEL_AND_WAIT | TERMINATE_CLUSTER
)
```

**Returns:** `{"step_id": "s-XXXXX", "cluster_id": "j-XXXXX", "name": "..."}`

Internally builds: `command-runner.jar` + `['spark-submit', '--deploy-mode', 'cluster', '--class', 'com.example.Main', '--conf', 'k=v', 's3://...', 'arg1', 'arg2']`

### 2. Add PySpark Step

Convenience function for PySpark scripts:

```python
add_pyspark_step(
    cluster_id="j-XXXXXXXXXXXXX",
    script="s3://bucket/scripts/my_job.py",
    args=["--input", "s3://bucket/data"],          # optional
    name="My PySpark Job",                          # optional
    py_files="s3://bucket/libs/utils.zip",         # optional
    conf={"spark.executor.cores": "2"},            # optional
    action_on_failure="CONTINUE"
)
```

### 3. Add Hive Step

```python
add_hive_step(
    cluster_id="j-XXXXXXXXXXXXX",
    script_s3_uri="s3://bucket/scripts/query.q",   # Hive script on S3
    # OR
    query="SELECT COUNT(*) FROM my_table",          # inline query
    name="My Hive Job",                             # optional
    args=["-d", "INPUT=s3://bucket/data/"],         # optional Hive variables
    action_on_failure="CONTINUE"
)
```

> Provide either `script_s3_uri` or `query`, not both.

## Step Lifecycle

### List Steps

```python
list_emr_steps(
    cluster_id="j-XXXXXXXXXXXXX",
    states=["RUNNING", "PENDING"],                  # optional
    max_results=50                                   # optional
)
```

**Returns:** List of step dicts with keys: `id`, `name`, `state`, `action_on_failure`, `jar`, `args`, `created_at`, `started_at`, `ended_at`, `failure_reason`, `failure_message`, `failure_log_file`.

### Describe Step

```python
describe_emr_step(cluster_id="j-XXXXX", step_id="s-XXXXX")
```

### Cancel Steps

```python
cancel_emr_steps(
    cluster_id="j-XXXXXXXXXXXXX",
    step_ids=["s-XXXXX", "s-YYYYY"],
    cancel_option="SEND_INTERRUPT"                  # or TERMINATE_PROCESS
)
```

**Returns:** List of `{"step_id": "...", "status": "SUBMITTED|FAILED", "reason": "..."}`

> `SEND_INTERRUPT`: Sends an interrupt signal (graceful). `TERMINATE_PROCESS`: Kills the process immediately.

## Step Logs

### Get Step Log

```python
get_emr_step_log(
    cluster_id="j-XXXXX",
    step_id="s-XXXXX",
    log_type="stderr",      # stderr (default), stdout, controller, syslog
    max_lines=200,           # optional
    mask_secrets=True        # optional, masks AWS credentials
)
```

**Log path structure in S3:**
```
s3://{log_uri}/{cluster_id}/steps/{step_id}/
├── controller.gz     # Step controller log
├── stderr.gz         # Standard error ⭐ (main debug log)
├── stdout.gz         # Standard output
└── syslog.gz         # System log
```

The `log_uri` is automatically fetched from the cluster's configuration.

## Step States

```
PENDING → RUNNING → COMPLETED / FAILED / CANCELLED / INTERRUPTED
              ↘ CANCEL_PENDING → CANCELLED
```

Terminal states: `COMPLETED`, `FAILED`, `CANCELLED`, `INTERRUPTED`

## ActionOnFailure Options

| Value | Behavior |
|---|---|
| `CONTINUE` | Continue executing next steps |
| `CANCEL_AND_WAIT` | Cancel remaining steps, cluster enters WAITING |
| `TERMINATE_CLUSTER` | Terminate the entire cluster |

## Configuration

| Environment Variable | Description | Required |
|---|---|---|
| `AWS_REGION` | AWS region | No (default: us-east-1) |
| `EMR_CLUSTER_ID` | Default cluster ID | No (pass per-call) |
