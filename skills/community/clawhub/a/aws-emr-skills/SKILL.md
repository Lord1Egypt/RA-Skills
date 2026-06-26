---
name: aws-emr-skills
description: |
  AWS EMR interaction skill for managing EMR Serverless, EMR on EC2, and EMR on EKS.
  Submit and manage Spark, Hive, and PySpark jobs across all three EMR deployment modes.
  Use this skill when the user mentions EMR, Spark, Hive, Serverless, big data jobs,
  submit job, query job status, get job logs, cancel job, EMR cluster, EMR step,
  virtual cluster, EKS, or similar keywords.
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - AWS_REGION
      bins:
        - python3
    primaryEnv: AWS_REGION
    emoji: "⚡"
    homepage: https://github.com/yhyyz/aws-emr-skills
---

# AWS EMR Skills

A Python skill for interacting with AWS EMR across three deployment modes: **EMR Serverless**, **EMR on EC2**, and **EMR on EKS**. Submit Spark and Hive jobs, manage clusters and applications, monitor job status, and retrieve logs.

## When to Use (Trigger Phrases)

Invoke this skill when the user mentions:
```
"Submit a Spark job on EMR"
"List EMR Serverless applications"
"Add a step to my EMR cluster"
"Get EMR job logs"
"Check EMR job status"
"Cancel running EMR job"
"List EMR clusters"
"Create an EMR on EKS virtual cluster"
"Submit PySpark to EMR Serverless"
"Get step logs from EMR cluster"
```
Any request involving EMR Serverless applications/jobs, EMR on EC2 clusters/steps, or EMR on EKS virtual clusters/job runs.

## Feature List

### EMR Serverless
- **Applications**: List, describe, start, stop EMR Serverless applications
- **Job Submission**: Submit Spark SQL, Spark JAR, PySpark, and Hive jobs (sync/async)
- **Job Lifecycle**: Get status, cancel, list job runs
- **Results**: Retrieve SQL query results from S3
- **Logs**: Get driver stdout/stderr logs with secret masking

### EMR on EC2
- **Clusters**: List, describe, terminate EMR clusters
- **Step Submission**: Add Spark, PySpark, and Hive steps via command-runner.jar
- **Step Lifecycle**: List, describe, cancel steps
- **Logs**: Get step logs (stderr, stdout, controller, syslog) from S3

### EMR on EKS
- **Virtual Clusters**: List, describe, create, delete virtual clusters
- **Job Submission**: Submit Spark and Spark SQL jobs to EKS
- **Job Lifecycle**: Describe, list, cancel job runs
- **Logs**: Get job logs from S3

## Initial Setup

1. **Python 3.8+** with `boto3>=1.26.0`:
   ```bash
   pip install boto3>=1.26.0
   ```

2. **AWS credentials** via boto3 default chain (env vars, config files, IAM roles).

3. **Environment variables** (all optional, validated at point of use):
   ```bash
   export AWS_REGION="us-east-1"

   # EMR Serverless
   export EMR_SERVERLESS_APP_ID="00abcdef12345678"
   export EMR_SERVERLESS_EXEC_ROLE_ARN="arn:aws:iam::123456789:role/emr-role"
   export EMR_SERVERLESS_S3_LOG_URI="s3://my-bucket/emr-logs/"

   # EMR on EC2
   export EMR_CLUSTER_ID="j-XXXXXXXXXXXXX"

   # EMR on EKS
   export EMR_EKS_VIRTUAL_CLUSTER_ID="abc123def456"
   export EMR_EKS_EXEC_ROLE_ARN="arn:aws:iam::123456789:role/emr-eks-role"
   ```

## How to Manage EMR

### 1. EMR Serverless

Fully managed serverless Spark/Hive execution. No infrastructure to manage.

- **Application management**: `scripts/on_serverless/emr_serverless_cli.py` — 14 @tool functions
- **Detailed guide**: `references/emr_serverless/application_guide.md` — Application lifecycle
- **Detailed guide**: `references/emr_serverless/job_guide.md` — Job submission, results, logs

### 2. EMR on EC2

Traditional EMR clusters on EC2 instances. Submit work as Steps.

- **Cluster & step management**: `scripts/on_ec2/emr_on_ec2_cli.py` — 10 @tool functions
- **Detailed guide**: `references/emr_on_ec2/cluster_guide.md` — Cluster lifecycle
- **Detailed guide**: `references/emr_on_ec2/step_guide.md` — Step submission, logs

### 3. EMR on EKS

Spark workloads on Amazon EKS via the emr-containers API.

- **Virtual cluster & job management**: `scripts/on_eks/emr_on_eks_cli.py` — 10 @tool functions
- **Detailed guide**: `references/emr_on_eks/virtual_cluster_guide.md` — Virtual cluster lifecycle
- **Detailed guide**: `references/emr_on_eks/job_run_guide.md` — Job submission, logs

## Available Scripts

| Script | Description |
|---|---|
| `scripts/on_serverless/emr_serverless_cli.py` | EMR Serverless @tool functions (14 tools) |
| `scripts/on_ec2/emr_on_ec2_cli.py` | EMR on EC2 @tool functions (10 tools) |
| `scripts/on_eks/emr_on_eks_cli.py` | EMR on EKS @tool functions (10 tools) |
| `scripts/config/emr_config.py` | Unified configuration management |
| `scripts/client/boto_client.py` | boto3 client factory |

## References

| Document | Description |
|---|---|
| `references/emr_serverless/application_guide.md` | EMR Serverless application management guide |
| `references/emr_serverless/job_guide.md` | EMR Serverless job submission and management guide |
| `references/emr_on_ec2/cluster_guide.md` | EMR on EC2 cluster management guide |
| `references/emr_on_ec2/step_guide.md` | EMR on EC2 step submission and management guide |
| `references/emr_on_eks/virtual_cluster_guide.md` | EMR on EKS virtual cluster management guide |
| `references/emr_on_eks/job_run_guide.md` | EMR on EKS job run management guide |

## Requirements

- When writing temporary files (scripts, notes, etc.), place them in the `./tmp` folder.
- When importing scripts packages, add the skill root to path: `sys.path.append(${emr_skill_root})`
- AWS credentials are handled by boto3's default credential chain — never pass access keys directly.
- All configuration environment variables are optional and validated at the point of use.

## Data Privacy & Trust

- **No credential storage**: AWS credentials are resolved via boto3 default chain. No keys are stored or logged.
- **Secret masking**: Log retrieval functions automatically mask potential AWS credentials in output.
- **Read-only by default**: Most operations are read-only queries. Write operations (job submission, cluster termination) require explicit user action.

## External Endpoints

This skill connects to:
- AWS EMR Serverless API (`emr-serverless.{region}.amazonaws.com`)
- AWS EMR API (`elasticmapreduce.{region}.amazonaws.com`)
- AWS EMR Containers API (`emr-containers.{region}.amazonaws.com`)
- AWS S3 API (`s3.{region}.amazonaws.com`) — for log and result retrieval
