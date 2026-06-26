[English](README.md) | [中文](README_CN.md)

# AWS Best Practice Research Skill

An agent skill that researches, compiles, and optionally assesses AWS service best practices against official documentation.

## Problem Statement

When configuring AWS services for production, engineers need to verify their setup against dozens of best-practice recommendations scattered across AWS documentation, Well-Architected Lenses, Security Hub controls, re:Post articles, and blog posts. Manually gathering and cross-referencing these sources is time-consuming and error-prone.

## What This Skill Does

1. **Research** — Searches official AWS documentation via [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) to find best practices for any AWS service.
2. **Compile** — Organizes findings into a categorized checklist table with 5 mandatory categories, source annotations, and priority levels.
3. **Assessment (optional)** — If the user provides AWS credentials and resource identifiers, runs AWS CLI commands to check a live resource against the compiled checklist and generates an assessment report with PASS/FAIL/WARN/N/A status per item.

## Prerequisites

| Dependency | Required For | Notes |
|-----------|-------------|-------|
| [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) | Checklist compilation (Steps 1-7) | Provides `aws___search_documentation`, `aws___read_documentation`, `aws___recommend` tools |
| AWS CLI (`aws`) | Live assessment only (Step 8) | Must be configured with read access to the target service |
| jq | Live assessment only (Step 8) | For parsing JSON output from AWS CLI commands |
| AWS credentials + region + resource ID | Live assessment only (Step 8) | Can be provided via env vars, profile, or credential file |

## Workflow Overview

```
Step 1: Identify target AWS service and assessment scope
         ↓
Step 2: Search documentation (5 sequential queries)
         ↓
Step 3: Read key documentation pages (3-5 pages)
         ↓
Step 4: Extract and categorize check items
         ↓
Step 5: Compile source annotations
         ↓
Step 6: Generate checklist output (5-category table, saved to local .md file)
         ↓
Step 7: Offer next steps
         ↓
Step 8: Live resource assessment (optional, only if credentials provided)
         ├── 8.1 Prepare environment
         ├── 8.2 Collect resource configuration
         ├── 8.3 Map configuration to checklist
         ├── 8.4 Generate assessment report (saved to local .md file)
         └── 8.5 Offer remediation
```

## Checklist Categories

Every generated checklist contains these 5 categories:

| # | Category | Example Items |
|---|----------|---------------|
| 1 | **High Availability Architecture** | Cluster mode, replication, Multi-AZ, AZ distribution, node types |
| 2 | **Disaster Recovery** | Backups, retention policies, RPO/RTO, cross-region replication |
| 3 | **Failover Planning** | Test Failover API, FIS testing, client timeout config, SNS notifications |
| 4 | **Security Configuration** | Encryption at-rest/in-transit, authentication, subnet groups, KMS |
| 5 | **Others** | Auto upgrade, monitoring, reserved memory, connection pooling, cost tags |

Each check item includes: ID (with embedded priority), name, description, source annotation, and priority level (High/Medium/Low).

## Check Item ID Format

```
{Category}-{Number}-{Priority}

Examples:
  HA-01-hi   → High Availability, item 1, High priority
  DR-02-md   → Disaster Recovery, item 2, Medium priority
  SEC-03-lo  → Security Configuration, item 3, Low priority
  OT-05-md   → Others, item 5, Medium priority
```

## Source Annotations

| Abbreviation | Source |
|--------------|--------|
| `WA-REL` / `WA-RELn` | Well-Architected Lens — Reliability Pillar |
| `WA-SEC` / `WA-SECn` | Well-Architected Lens — Security Pillar |
| `WA-PE` / `WA-PEn` | Well-Architected Lens — Performance Efficiency Pillar |
| `WA-OE` / `WA-OEn` | Well-Architected Lens — Operational Excellence Pillar |
| `WA-CO` | Well-Architected Lens — Cost Optimization Pillar |
| `Security Hub [{Service}.N]` | AWS Security Hub CSPM control |
| `re:Post` | AWS re:Post knowledge center article |
| `Official Docs` | Service user guide |
| `AWS Blog` | AWS official blog post |
| `Whitepaper` | AWS whitepaper |

## Assessment Status Definitions

When performing a live assessment, each check item receives one of these statuses:

| Status | Meaning |
|--------|---------|
| PASS | Resource configuration meets or exceeds the recommendation |
| FAIL | Resource configuration does not meet the recommendation |
| WARN | Cannot be fully verified from infrastructure alone, or partially meets |
| N/A | Check does not apply to this resource |

## Supported Services

The skill works with **any AWS service** that has documentation indexed by aws-knowledge-mcp-server. Pre-built assessment command mappings exist for:

- **ElastiCache Redis / Valkey** — Full CLI command set and check-item-to-field mapping
- **Amazon RDS / Aurora** — Primary describe commands
- **Amazon MSK** — Cluster and configuration commands
- **Amazon DynamoDB** — Table, backup, and global table commands
- **Amazon EKS** — Cluster, nodegroup, addon, access entries, and upgrade insights commands (infrastructure-level only; see Scope Boundary below)

Other services are supported for checklist compilation; live assessment commands are derived from the service's AWS CLI reference.

## Scope Boundary for Container / Orchestration Platforms

When the target service is a **container or orchestration platform** (EKS, ECS, Fargate, App Runner, Elastic Beanstalk), this skill focuses **exclusively on the AWS infrastructure layer** — items verifiable through AWS APIs (`aws eks`, `aws ecs`, `aws ec2`, `aws iam`, etc.).

Check items that require `kubectl`, ECS Exec, or any in-cluster / in-task inspection are **out of scope** and belong to a dedicated workload-level assessment skill.

### EKS Example: In Scope vs Out of Scope

| In Scope (AWS API verifiable) | Out of Scope (requires kubectl / workload context) |
|-------------------------------|-----------------------------------------------------|
| Control plane config (K8s version, API endpoint access, logging) | Pod Disruption Budgets (PDB) |
| Node group config (instance types, scaling, AMI, AZ distribution) | Topology Spread Constraints |
| Cluster networking (VPC, subnets, security groups) | Liveness / readiness / startup probes |
| Add-on presence and versions | Container resource requests / limits |
| Secrets envelope encryption (KMS) | Pod securityContext (runAsNonRoot, capabilities) |
| Authentication mode and Access Entries | Pod Security Admission (PSA) namespace labels |
| Control plane audit logging | Network Policies (K8s resource level) |
| Cluster deletion protection | Pod graceful termination (terminationGracePeriodSeconds) |
| OIDC provider configuration (for IRSA) | OPA Gatekeeper / Kyverno policies |
| GuardDuty EKS protection | Service mesh (mTLS) configuration |

The generated checklist includes a **Scope Notice** at the end directing users to a workload-level skill for the items that are out of scope.

## Directory Structure

```
aws-bestpractice-research/
├── SKILL.md                              # Main skill definition (agent instructions)
├── README.md                             # This file (PRD / user documentation)
└── references/
    ├── search-queries.md                 # 5 search query templates + page reading priority
    ├── output-template.md                # Checklist output format specification
    ├── assessment-workflow.md              # Per-service assessment commands and field mappings
    └── assessment-output-template.md       # Assessment report format specification
```

## Usage Examples

**Checklist only:**
```
"帮我查找 ElastiCache Redis 的最佳实践"
"What are the best practices for Amazon MSK?"
"Compile a HA/DR/security checklist for Aurora PostgreSQL"
```

**Checklist + live assessment:**
```
"Check my ElastiCache Redis cluster my-redis-cluster in us-west-2"
"评估一下我的 RDS 实例，region 是 ap-southeast-1，实例 ID 是 prod-db-01"
"Assess my DynamoDB table orders-table against best practices"
```

## Key Design Decisions

1. **Sequential MCP requests** — All documentation searches and page reads are executed one at a time to avoid rate limiting from aws-knowledge-mcp-server. This is slower but reliable.

2. **5-category structure** — Every checklist uses the same 5 categories regardless of service, providing a consistent assessment framework across different AWS services.

3. **Embedded priority in ID** — The `-hi`/`-md`/`-lo` suffix in check IDs allows quick visual scanning without needing to read the Priority column.

4. **Optional live assessment** — The checklist is a complete, standalone deliverable. Live assessment is only triggered when the user explicitly provides credentials and resource identifiers. The skill never blocks on missing credentials.

5. **Language respect** — All output follows the language of the user's conversation (English, Chinese, etc.).

6. **Infrastructure-only scope for container platforms** — For services like EKS and ECS, this skill strictly limits its scope to what AWS APIs can verify. Workload-level concerns (pods, tasks, containers) require different tools (`kubectl`, ECS Exec) and application context that this skill does not assume access to.

## Limitations

- Depends on aws-knowledge-mcp-server availability; if the MCP server is not configured, the skill cannot run.
- Rate limits on the MCP server mean documentation gathering takes ~30-60 seconds for 5 queries + 3-5 page reads.
- Live assessment requires read-only IAM permissions for the target service; write permissions are never needed.
- Assessment field mappings are pre-built for a limited set of services; other services derive assessment commands dynamically.
- Client-side configurations (connection pooling, retry logic, timeouts) can only be flagged as WARN during live assessment since they require application-level verification.
- For container/orchestration platforms (EKS, ECS), this skill only covers infrastructure-level best practices. Workload-level items (PDB, topology constraints, probes, resource limits, pod security) require a dedicated workload assessment skill with `kubectl` access.
