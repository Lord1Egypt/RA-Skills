# AWS Redshift Skills

An AI agent skill for managing AWS Redshift across two deployment modes: **Redshift Provisioned** and **Redshift Serverless**, plus a shared **Data API** for SQL execution.

This is not a standalone CLI tool. It is a skill designed for AI agent platforms like [OpenCode](https://github.com/opencode-ai/opencode), [Claude Code](https://code.claude.com), [OpenClaw](https://openclaw.ai), [Cursor](https://cursor.com), and [40+ more](https://github.com/vercel-labs/skills#supported-agents), enabling AI assistants to manage Redshift clusters, workgroups, run SQL queries, and move data through natural language.

> **SKILL.md** is the LLM-facing skill descriptor. This README is for humans.

## Features

**33 @tool functions** covering two Redshift deployment modes plus the Data API:

| Mode | Tools | Capabilities |
|------|-------|-------------|
| **Redshift Provisioned** | 12 | Cluster management (list/describe/create/delete/resize/pause/resume/reboot), snapshot management (create/describe/restore/delete) |
| **Redshift Serverless** | 9 | Workgroup management (list/get/create/update/delete), namespace management (list/get/create/delete) |
| **Redshift Data API** | 12 | SQL execution (single/batch, sync/async), results with pagination, statement lifecycle (describe/list/cancel), metadata (databases/schemas/tables/columns), COPY from S3, UNLOAD to S3 |

Additional features:

- AWS credentials resolved via boto3 default credential chain — no keys stored or logged
- Automatic secret masking in all output
- All environment variables are optional, validated at point of use
- Works with both provisioned cluster-identifier + db-user auth AND serverless workgroup-name + secrets-manager auth

## Project Structure

```
aws-redshift-skills/
├── SKILL.md                                    # AI agent skill descriptor (LLM-facing)
├── README.md                                   # English README (this file)
├── pyproject.toml                              # Project metadata
├── .clawhubignore                              # ClawHub publish exclusions
├── scripts/
│   ├── config/
│   │   └── redshift_config.py                  # Unified config (both modes + Data API)
│   ├── client/
│   │   └── boto_client.py                      # boto3 client factory
│   ├── provisioned/
│   │   ├── redshift_provisioned_cli.py         # @tool entry point (12 tools)
│   │   ├── clusters.py                         # Cluster management
│   │   └── snapshots.py                        # Snapshot management
│   ├── serverless/
│   │   ├── redshift_serverless_cli.py          # @tool entry point (9 tools)
│   │   ├── workgroups.py                       # Workgroup management
│   │   └── namespaces.py                       # Namespace management
│   └── data_api/
│       ├── redshift_data_cli.py                # @tool entry point (12 tools)
│       └── queries.py                          # SQL execution, results, metadata
├── references/
│   ├── provisioned/
│   │   ├── cluster_guide.md                    # Cluster lifecycle guide
│   │   └── snapshot_guide.md                   # Snapshot management guide
│   ├── serverless/
│   │   ├── workgroup_guide.md                  # Workgroup management guide
│   │   └── namespace_guide.md                  # Namespace management guide
│   └── data_api/
│       └── query_guide.md                      # SQL execution via Data API guide
├── examples/
│   ├── run_sql.py                              # Execute SQL query example
│   ├── manage_cluster.py                       # Cluster operations demo
│   ├── manage_serverless.py                    # Serverless operations demo
│   └── copy_unload.py                          # COPY/UNLOAD demo
└── tests/                                      # Unit tests (40+ tests)
    ├── conftest.py
    ├── test_config.py
    ├── test_clusters.py
    ├── test_snapshots.py
    ├── test_workgroups.py
    ├── test_namespaces.py
    └── test_queries.py
```

## Installation

### Option 1: Install via npx skills (Recommended)

[skills](https://github.com/vercel-labs/skills) is the open agent skills installer supporting [40+ AI agent platforms](https://github.com/vercel-labs/skills#supported-agents) (OpenCode, Claude Code, OpenClaw, Cursor, Codex, etc.):

```bash
npx skills add danjin/aws-redshift-skills
```

Target specific agent platforms:

```bash
# Install to Claude Code
npx skills add danjin/aws-redshift-skills -a claude-code

# Install to OpenClaw
npx skills add danjin/aws-redshift-skills -a openclaw

# Install to OpenCode
npx skills add danjin/aws-redshift-skills -a opencode

# Install to all detected agents
npx skills add danjin/aws-redshift-skills --all
```

### Option 2: Install via ClawHub

[ClawHub](https://clawhub.ai) is the skill registry for OpenClaw:

```bash
npx clawhub@latest install aws-redshift-skills
```

### Option 3: Manual install via Git

```bash
# Clone the repository
git clone https://github.com/danjin/aws-redshift-skills.git

# Symlink into the skills directory (Claude Code example)
ln -s "$(pwd)/aws-redshift-skills" ~/.claude/skills/aws-redshift-skills
```

### Dependencies

Ensure boto3 is installed in your Python environment:

```bash
pip install boto3>=1.26.0
```

## Environment Variables

All environment variables are optional. They are validated at the point of use.

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `REDSHIFT_CLUSTER_ID` | Provisioned cluster identifier | — |
| `REDSHIFT_DATABASE` | Database name | `dev` |
| `REDSHIFT_DB_USER` | Database user (provisioned mode) | — |
| `REDSHIFT_WORKGROUP_NAME` | Serverless workgroup name | — |
| `REDSHIFT_NAMESPACE_NAME` | Serverless namespace name | — |
| `REDSHIFT_IAM_ROLE_ARN` | IAM role for COPY/UNLOAD | — |
| `REDSHIFT_S3_LOG_URI` | S3 path for logs/results | — |
| `REDSHIFT_SECRET_ARN` | Secrets Manager ARN for auth | — |
| `REDSHIFT_SKILL_CONFIG` | Optional config file path (KEY=VALUE) | — |

Config priority: environment variable > config file > built-in default.

## Usage Examples

### Provisioned Cluster Management

```python
import sys
sys.path.append("/path/to/aws-redshift-skills")

from scripts.provisioned.redshift_provisioned_cli import (
    list_clusters,
    describe_cluster,
    create_cluster,
    pause_cluster,
    resume_cluster,
)

# List all clusters
clusters = list_clusters()

# Describe a specific cluster
detail = describe_cluster(cluster_id="my-cluster")

# Create a new cluster
new_cluster = create_cluster(
    cluster_id="analytics-cluster",
    node_type="ra3.xlplus",
    number_of_nodes=2,
    master_username="admin",
    master_password="MySecurePass123!",
)

# Pause to save costs
pause_cluster(cluster_id="analytics-cluster")
```

### Serverless Management

```python
from scripts.serverless.redshift_serverless_cli import (
    list_workgroups,
    create_namespace,
    create_workgroup,
)

# List workgroups
workgroups = list_workgroups()

# Create namespace and workgroup
ns = create_namespace(namespace_name="analytics-ns", db_name="analytics")
wg = create_workgroup(
    workgroup_name="analytics-wg",
    namespace_name="analytics-ns",
    base_capacity=32,
)
```

### SQL Execution via Data API

```python
from scripts.data_api.redshift_data_cli import (
    execute_sql,
    get_statement_result,
    list_tables,
    execute_copy,
)

# Execute a query (sync)
result = execute_sql(sql="SELECT * FROM sales LIMIT 10", is_sync=True)

# Get results
if result["status"] == "FINISHED":
    data = get_statement_result(statement_id=result["id"])
    print(data["columns"])
    print(data["rows"])

# List tables
tables = list_tables(schema_pattern="public")

# COPY data from S3
execute_copy(
    table="sales",
    s3_path="s3://my-bucket/data/sales/",
    data_format="PARQUET",
)
```

## Key Redshift Details

- **Provisioned node types**: ra3.xlplus, ra3.4xlarge, ra3.16xlarge, dc2.large, dc2.8xlarge, ds2.xlarge, ds2.8xlarge
- **Serverless RPU**: 8–512 RPU (Redshift Processing Units), increments of 8
- **Data API auth**: Supports cluster-identifier + db-user OR workgroup-name + secrets-manager
- **Key features**: Zero-ETL, streaming ingestion, COPY JOB, materialized views, datasharing, federated queries, ML (CREATE MODEL), Spectrum (external tables)

## License

MIT License
