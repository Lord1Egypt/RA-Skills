English | [中文](README.md)

# AWS EMR Skills

An AI agent skill for managing AWS EMR across three deployment modes: **EMR Serverless**, **EMR on EC2**, and **EMR on EKS**.

This is not a standalone CLI tool. It is a skill designed for AI agent platforms like [OpenCode](https://github.com/opencode-ai/opencode), [Claude Code](https://code.claude.com), [OpenClaw](https://openclaw.ai), [Cursor](https://cursor.com), and [40+ more](https://github.com/vercel-labs/skills#supported-agents), enabling AI assistants to manage EMR clusters, submit Spark/Hive jobs, and retrieve logs through natural language.

> **SKILL.md** is the LLM-facing skill descriptor. This README is for humans.

## Features

**32 @tool functions** covering three EMR deployment modes:

| Mode | Tools | Capabilities |
|------|-------|-------------|
| **EMR Serverless** | 14 | Application management (list/describe/start/stop), job submission (Spark SQL/JAR/PySpark/Hive, sync/async), job status, cancel, logs, SQL result retrieval |
| **EMR on EC2** | 10 | Cluster management (list/describe/terminate), step submission (Spark/PySpark/Hive), step status, cancel, log retrieval |
| **EMR on EKS** | 8 | Virtual cluster management (list/describe/create/delete), job submission (Spark/Spark SQL), job status, cancel, log retrieval |

Additional features:

- AWS credentials resolved via boto3 default credential chain — no keys stored or logged
- Automatic secret masking in log output
- All environment variables are optional, validated at point of use

## Project Structure

```
aws-emr-skills/
├── SKILL.md                                    # AI agent skill descriptor (LLM-facing)
├── README.md                                   # 中文说明
├── README_EN.md                                # English README (this file)
├── pyproject.toml                              # Project metadata
├── .clawhubignore                              # ClawHub publish exclusions
├── scripts/
│   ├── config/
│   │   └── emr_config.py                       # Unified config (all 3 modes)
│   ├── client/
│   │   └── boto_client.py                      # boto3 client factory
│   ├── on_serverless/
│   │   ├── emr_serverless_cli.py               # @tool entry point (14 tools)
│   │   ├── applications.py                     # Application management
│   │   └── jobs.py                             # Job management
│   ├── on_ec2/
│   │   ├── emr_on_ec2_cli.py                   # @tool entry point (10 tools)
│   │   ├── clusters.py                         # Cluster management
│   │   └── steps.py                            # Step management
│   └── on_eks/
│       ├── emr_on_eks_cli.py                   # @tool entry point (8 tools)
│       ├── virtual_clusters.py                 # Virtual cluster management
│       └── job_runs.py                         # Job run management
├── references/
│   ├── emr_serverless/
│   │   ├── application_guide.md                # Application lifecycle guide
│   │   └── job_guide.md                        # Job submission & logs guide
│   ├── emr_on_ec2/
│   │   ├── cluster_guide.md                    # Cluster management guide
│   │   └── step_guide.md                       # Step submission & logs guide
│   └── emr_on_eks/
│       ├── virtual_cluster_guide.md            # Virtual cluster management guide
│       └── job_run_guide.md                    # Job submission & logs guide
├── examples/                                   # Example scripts (Serverless)
│   ├── sql_job.py
│   ├── pyspark_job.py
│   ├── jar_job.py
│   ├── hive_job.py
│   └── manage_demo.py
└── tests/                                      # Unit tests (49 tests)
    ├── test_applications.py                    # Serverless application tests
    ├── test_jobs.py / test_jobs_*.py           # Serverless job tests
    ├── test_ec2_clusters.py                    # EC2 cluster tests
    ├── test_ec2_steps.py                       # EC2 step tests
    ├── test_eks_virtual_clusters.py            # EKS virtual cluster tests
    └── test_eks_job_runs.py                    # EKS job run tests
```

## Installation

### Option 1: Install via npx skills (Recommended)

[skills](https://github.com/vercel-labs/skills) is the open agent skills installer supporting [40+ AI agent platforms](https://github.com/vercel-labs/skills#supported-agents) (OpenCode, Claude Code, OpenClaw, Cursor, Codex, etc.):

```bash
npx skills add yhyyz/aws-emr-skills
```

Target specific agent platforms:

```bash
# Install to Claude Code
npx skills add yhyyz/aws-emr-skills -a claude-code

# Install to OpenClaw
npx skills add yhyyz/aws-emr-skills -a openclaw

# Install to OpenCode
npx skills add yhyyz/aws-emr-skills -a opencode

# Install to all detected agents
npx skills add yhyyz/aws-emr-skills --all
```

### Option 2: Install via ClawHub

[ClawHub](https://clawhub.ai) is the skill registry for OpenClaw:

```bash
npx clawhub@latest install aws-emr-skills
```

### Option 3: Manual install via Git

```bash
# Clone the repository
git clone https://github.com/yhyyz/aws-emr-skills.git

# Symlink into the skills directory (Claude Code example)
ln -s "$(pwd)/aws-emr-skills" ~/.claude/skills/aws-emr-skills
```

### Dependencies

Ensure boto3 is installed in your Python environment:

```bash
pip install "boto3>=1.26.0"
```

Requires **Python 3.8+**.

## Configuration

All environment variables are optional. AWS credentials are resolved via the boto3 default credential chain (env vars → `~/.aws/config` → IAM Role).

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `EMR_SERVERLESS_APP_ID` | Serverless application ID | — |
| `EMR_SERVERLESS_EXEC_ROLE_ARN` | Serverless execution role ARN | — |
| `EMR_SERVERLESS_S3_LOG_URI` | Serverless log S3 path | — |
| `EMR_CLUSTER_ID` | EC2 cluster ID | — |
| `EMR_EKS_VIRTUAL_CLUSTER_ID` | EKS virtual cluster ID | — |
| `EMR_EKS_EXEC_ROLE_ARN` | EKS execution role ARN | — |

Priority: **Environment variables > Config file > Built-in defaults**

## Usage Examples

After installation, trigger the skill with natural language in your AI assistant:

```
"List all EMR Serverless applications"
"Submit a Spark SQL job to EMR Serverless"
"Check the status of EMR cluster j-XXXXX"
"Add a PySpark step to my EMR cluster"
"Cancel the running EMR job"
"Get EMR step logs"
"Create an EMR on EKS virtual cluster"
"Submit a PySpark job to EMR Serverless, script at s3://my-bucket/scripts/etl.py"
```

The AI assistant will automatically recognize intent and invoke the corresponding tool functions.

## Development & Testing

```bash
# Run all tests (49 unit tests)
pytest tests/ -v

# Run tests for a specific module
pytest tests/test_applications.py -v        # Serverless applications
pytest tests/test_ec2_clusters.py -v         # EC2 clusters
pytest tests/test_eks_virtual_clusters.py -v # EKS virtual clusters
```

## License

MIT License
