# EMR On EC2 Cluster Management Guide

## Overview

EMR on EC2 provides traditional Hadoop/Spark clusters running on Amazon EC2 instances. You manage cluster lifecycle (create, monitor, terminate) and submit work as Steps.

## Available Operations

All operations are available via `@tool` functions in `scripts/on_ec2/emr_on_ec2_cli.py`.

### 1. List Clusters

```python
list_emr_clusters(
    states=["RUNNING", "WAITING"],         # optional
    max_results=50                          # optional
)
```

**Parameters:**
- `states` (optional): Filter by state. Valid values: `STARTING`, `BOOTSTRAPPING`, `RUNNING`, `WAITING`, `TERMINATING`, `TERMINATED`, `TERMINATED_WITH_ERRORS`.
- `max_results` (optional): Maximum clusters to return (default: 50).

**Returns:** List of cluster dicts with keys: `id`, `name`, `state`, `state_change_reason`, `created_at`, `ready_at`, `ended_at`, `normalized_instance_hours`, `cluster_arn`.

### 2. Describe Cluster

```python
describe_emr_cluster(cluster_id="j-XXXXXXXXXXXXX")
```

**Returns:** Detailed dict with keys: `id`, `name`, `state`, `state_details`, `log_uri`, `release_label`, `applications`, `service_role`, `master_public_dns`, `ec2_instance_attributes`, `step_concurrency_level`, `auto_terminate`, `termination_protected`, `cluster_arn`, `tags`.

### 3. Terminate Clusters

```python
terminate_emr_clusters(cluster_ids=["j-XXXXX", "j-YYYYY"])
```

**Returns:** `{"cluster_ids": [...], "status": "termination_requested"}`

> **Note:** Termination is asynchronous. The cluster may take 1-5 minutes to fully terminate.

## Cluster States

```
STARTING → BOOTSTRAPPING → RUNNING → WAITING → TERMINATING → TERMINATED / TERMINATED_WITH_ERRORS
```

- `RUNNING`: Cluster is executing Steps.
- `WAITING`: Cluster is idle, waiting for new Steps (only when `KeepJobFlowAliveWhenNoSteps=True`).
- `TERMINATED_WITH_ERRORS`: Cluster terminated due to an error.

## Configuration

| Environment Variable | Description | Required |
|---|---|---|
| `AWS_REGION` | AWS region | No (default: us-east-1) |
| `EMR_CLUSTER_ID` | Default cluster ID | No (pass per-call) |

AWS credentials are resolved via boto3 default credential chain.

## Notes

- Cluster creation (`run_job_flow`) is not exposed as a tool function due to its complexity. Use the AWS Console or CLI for cluster creation, then use this skill for step management and monitoring.
- For log access, ensure the cluster was created with a `LogUri` pointing to an S3 bucket you have read access to.
