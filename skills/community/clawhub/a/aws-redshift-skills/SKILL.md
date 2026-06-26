---
name: aws-redshift-skills
description: |
  AWS Redshift interaction skill for managing Redshift Provisioned, Redshift Serverless,
  and executing SQL queries via the Redshift Data API.
  Manage clusters, workgroups, namespaces, snapshots, and run SQL statements.
  Use this skill when the user mentions Redshift, data warehouse, Redshift cluster,
  Redshift Serverless, workgroup, namespace, COPY, UNLOAD, Redshift query,
  Redshift Data API, or similar keywords.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AWS_REGION
      bins:
        - python3
    primaryEnv: AWS_REGION
    emoji: "🔴"
    homepage: https://github.com/danjin/aws-redshift-skills
---

# AWS Redshift Skills

A Python skill for interacting with AWS Redshift across two deployment modes: **Redshift Provisioned** and **Redshift Serverless**, plus a shared **Data API** for SQL execution.

## When to Use (Trigger Phrases)

Invoke this skill when the user mentions:
```
"List Redshift clusters"
"Create a Redshift cluster"
"Pause my Redshift cluster"
"List Redshift Serverless workgroups"
"Create a namespace"
"Run a SQL query on Redshift"
"Execute COPY from S3 to Redshift"
"UNLOAD data to S3"
"Check query status"
"List tables in Redshift"
"Describe Redshift table columns"
"Resize my Redshift cluster"
```
Any request involving Redshift Provisioned clusters/snapshots, Redshift Serverless workgroups/namespaces, or Data API SQL execution.

## Feature List

### Redshift Provisioned
- **Clusters**: List, describe, create, delete, resize, pause, resume, reboot clusters
- **Snapshots**: Create, describe, restore from, delete snapshots

### Redshift Serverless
- **Workgroups**: List, get, create, update, delete workgroups (RPU configuration)
- **Namespaces**: List, get, create, delete namespaces (database configuration)

### Redshift Data API
- **SQL Execution**: Execute single or batch SQL statements (async or sync with polling)
- **Results**: Get query results with pagination
- **Lifecycle**: Describe statement status, list recent statements, cancel running queries
- **Metadata**: List databases, schemas, tables; describe table columns
- **Data Movement**: COPY from S3, UNLOAD to S3

## Initial Setup

1. **Python 3.8+** with `boto3>=1.26.0`:
   ```bash
   pip install boto3>=1.26.0
   ```

2. **AWS credentials** via boto3 default chain (env vars, config files, IAM roles).

3. **Environment variables** (all optional, validated at point of use):
   ```bash
   export AWS_REGION="us-east-1"

   # Redshift Provisioned
   export REDSHIFT_CLUSTER_ID="my-cluster"
   export REDSHIFT_DATABASE="dev"
   export REDSHIFT_DB_USER="admin"

   # Redshift Serverless
   export REDSHIFT_WORKGROUP_NAME="my-workgroup"
   export REDSHIFT_NAMESPACE_NAME="my-namespace"

   # Shared
   export REDSHIFT_IAM_ROLE_ARN="arn:aws:iam::123456789:role/redshift-role"
   export REDSHIFT_S3_LOG_URI="s3://my-bucket/redshift-logs/"
   export REDSHIFT_SECRET_ARN="arn:aws:secretsmanager:us-east-1:123456789:secret:my-secret"
   ```

## How to Manage Redshift

### 1. Redshift Provisioned

Traditional Redshift provisioned clusters with dedicated compute nodes.

- **Cluster & snapshot management**: `scripts/provisioned/redshift_provisioned_cli.py` — 12 @tool functions
- **Detailed guide**: `references/provisioned/cluster_guide.md` — Cluster lifecycle, node types, resize
- **Detailed guide**: `references/provisioned/snapshot_guide.md` — Snapshot create/restore/share

### 2. Redshift Serverless

Fully managed serverless data warehouse with automatic scaling.

- **Workgroup & namespace management**: `scripts/serverless/redshift_serverless_cli.py` — 9 @tool functions
- **Detailed guide**: `references/serverless/workgroup_guide.md` — Workgroup management
- **Detailed guide**: `references/serverless/namespace_guide.md` — Namespace management

### 3. Redshift Data API

SQL execution via the Data API. Works with both Provisioned and Serverless.

- **Query execution & metadata**: `scripts/data_api/redshift_data_cli.py` — 12 @tool functions
- **Detailed guide**: `references/data_api/query_guide.md` — SQL execution, COPY/UNLOAD

## Available Scripts

| Script | Description |
|---|---|
| `scripts/provisioned/redshift_provisioned_cli.py` | Redshift Provisioned @tool functions (12 tools) |
| `scripts/serverless/redshift_serverless_cli.py` | Redshift Serverless @tool functions (9 tools) |
| `scripts/data_api/redshift_data_cli.py` | Redshift Data API @tool functions (12 tools) |
| `scripts/config/redshift_config.py` | Unified configuration management |
| `scripts/client/boto_client.py` | boto3 client factory |

## References

| Document | Description |
|---|---|
| `references/provisioned/cluster_guide.md` | Redshift Provisioned cluster management guide |
| `references/provisioned/snapshot_guide.md` | Redshift snapshot management guide |
| `references/serverless/workgroup_guide.md` | Redshift Serverless workgroup management guide |
| `references/serverless/namespace_guide.md` | Redshift Serverless namespace management guide |
| `references/data_api/query_guide.md` | Redshift Data API SQL execution guide |

## Requirements

- When writing temporary files (scripts, notes, etc.), place them in the `./tmp` folder.
- When importing scripts packages, add the skill root to path: `sys.path.append(${redshift_skill_root})`
- AWS credentials are handled by boto3's default credential chain — never pass access keys directly.
- All configuration environment variables are optional and validated at the point of use.

## Data Privacy & Trust

- **No credential storage**: AWS credentials are resolved via boto3 default chain. No keys are stored or logged.
- **Secret masking**: All functions automatically mask potential AWS credentials in output.
- **Read-only by default**: Most operations are read-only queries. Write operations (cluster creation, deletion) require explicit user action.

## External Endpoints

This skill connects to:
- AWS Redshift API (`redshift.{region}.amazonaws.com`)
- AWS Redshift Serverless API (`redshift-serverless.{region}.amazonaws.com`)
- AWS Redshift Data API (`redshift-data.{region}.amazonaws.com`)
- AWS S3 API (`s3.{region}.amazonaws.com`) — for COPY/UNLOAD operations
