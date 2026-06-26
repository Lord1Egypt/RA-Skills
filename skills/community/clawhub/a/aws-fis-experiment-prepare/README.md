[English](README.md) | [中文](README_CN.md)

# AWS FIS Experiment Prepare

An agent skill that generates all configuration files needed to run an AWS FIS (Fault Injection Service) experiment, then **deploys via CloudFormation with self-healing iteration** until the stack succeeds.

## Problem Statement

Preparing an AWS FIS experiment manually involves several error-prone, tedious steps:

- **Resource-action compatibility is non-obvious** — e.g., `aws:rds:failover-db-cluster` requires an Aurora cluster (`aws:rds:cluster`), not a standalone RDS instance. Mismatches are only discovered at experiment start time, wasting all prior setup effort.
- **Multiple files must be generated and kept consistent** — experiment template JSON, IAM policy, CloudFormation template, CloudWatch alarms, and dashboard all reference the same resource ARNs and parameters.
- **CloudFormation deployments frequently fail** — property validation errors, IAM propagation delays, and region-specific resource limitations require iterative debugging that is slow and frustrating to do manually.
- **Scenario Library scenarios are complex** — composite scenarios (e.g., AZ Power Interruption) orchestrate multiple sub-actions with specific tag requirements and target types that are easy to misconfigure.
- **Scenario Library templates cannot be generated via API** — unlike custom single FIS actions, the 4 Scenario Library scenarios have no CLI/API command to auto-generate their experiment templates. The JSON template must be extracted from AWS documentation.

## What This Skill Does

1. **Identifies the scenario** — Determines whether the user wants a Scenario Library pre-built scenario (AZ Power Interruption, AZ Application Slowdown, etc.) or a custom single FIS action.
2. **Reads Scenario Library documentation** — For Scenario Library scenarios, reads the AWS documentation page to extract the JSON experiment template (these cannot be generated via API). The documentation URLs are:
   - [AZ Power Interruption](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-availability-scenario.html)
   - [AZ Application Slowdown](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-application-slowdown-scenario.html)
   - [Cross-AZ Traffic Slowdown](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-az-traffic-slowdown-scenario.html)
   - [Cross-Region Connectivity](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-region-scenario.html)
3. **Discovers target resources** — Queries the user's actual AWS resources and collects target identifiers. For ElastiCache cluster-mode-enabled replication groups, detects shard primary/replica distribution via CloudWatch `IsMaster` metric (since `CurrentRole` returns null for cluster-mode-enabled).
4. **Validates compatibility** — Inspects actual resources via AWS CLI (e.g., `describe-db-instances`, `describe-db-clusters`) and cross-checks against FIS action `resourceType` requirements before generating any files.
5. **Determines monitoring configuration** — Defaults to `source: "none"` (no stop condition alarm). Only creates CloudWatch alarms if the user explicitly provides one. Generates a comprehensive CloudWatch dashboard with per-service availability, performance, and error/latency metrics.
6. **Reads CFN resource documentation** — Before generating the CFN template, reads the `AWS::FIS::ExperimentTemplate` CloudFormation documentation to ensure the template uses the current property schema.
7. **Generates configuration files** — Produces a self-contained directory with 2 files: CFN template and README.
8. **Deploys with self-healing** — Deploys the CFN template, and if deployment fails, automatically analyzes errors, fixes the template, deletes the failed stack, and retries (up to 5 times).
9. **Renames directory with template ID** — After successful deployment, appends the experiment template ID to the output directory name (e.g., `2026-04-11-pod-net-pktloss-payment-redis-EXT1a2b3c4d5e6f7/`) for easy identification.

## Supported Scenarios

### Scenario Library (Composite, Multi-Action)

| Scenario | Key Sub-Actions |
|---|---|
| AZ Availability: Power Interruption | EC2 stop, RDS failover, ElastiCache AZ power, EBS pause, network disruption |
| AZ: Application Slowdown | Pod network latency, EBS latency, network disruption |
| Cross-AZ: Traffic Slowdown | Cross-AZ network latency/packet-loss |
| Cross-Region: Connectivity | Cross-region network disruption |
| EC2 Stress | Instance failure, CPU, memory, disk, network latency |
| EKS Stress | Pod delete, CPU, disk, memory, network latency |
| EBS Latency | Sustained, increasing, intermittent, decreasing |

### Custom FIS Actions (Single Action)

Any valid FIS action ID, e.g.:
- `aws:rds:failover-db-cluster`
- `aws:ec2:stop-instances`
- `aws:elasticache:replicationgroup-interrupt-az-power`
- `aws:eks:pod-network-latency`

### Service-Specific Guides (SSM Automation for Services Without Native FIS Actions)

For AWS services that have **no native FIS action**, the skill uses `aws:ssm:start-automation-execution` to invoke an SSM Automation runbook that calls the target service's API directly. Both the SSM Automation document and the FIS experiment template are deployed in a single CFN stack.

Currently supported:
- **Amazon MSK** — `kafka:RebootBroker` to test Kafka consumer/producer resilience. See `references/msk-guide.md`.
- **Amazon ElastiCache** (primary node reboot) — `elasticache:RebootCacheCluster` to test Redis/Valkey connection pool and retry logic resilience. See `references/elasticache-redis-guide.md`.
- **Amazon ElastiCache** (replication group failover) — `elasticache:TestFailover` to trigger automatic failover on a specific shard, promoting a replica to primary. Supports both cluster-mode-disabled and cluster-mode-enabled. See `references/elasticache-redis-guide.md`.

Additional services (Redshift, Neptune, OpenSearch, MemoryDB, etc.) can be added following the same pattern — the `ssm-auto-<service>-<operation>` slug naming and two-role IAM design are documented in `references/slug-conventions.md` and `references/msk-guide.md`.

## Output Directory Structure

```
./{yyyy-mm-dd-HH-MM-SS}-{scenario-slug}-{target-slug}[-{context-slug}]-{TEMPLATE_ID}/
├── README.md                          # Experiment overview and execution instructions
└── cfn-template.yaml                  # All-in-one CloudFormation template
```

The optional `{context-slug}` distinguishes experiments with the same scenario and target
but different downstream services (e.g., `redis`, `msk`). Used for network fault injection
actions (latency, packet-loss, blackhole-port).

The `{TEMPLATE_ID}` is the FIS experiment template ID (e.g., `EXT1a2b3c4d5e6f7`), appended
after successful CFN deployment for easy identification.

Scenario slugs use standard abbreviations (e.g., `pod-net-pktloss`, `az-power-int`,
`ec-rg-az-power`) to keep CFN stack names and resource names concise. See
`references/slug-conventions.md` for the full abbreviation table and naming rules.

## Resource-Action Compatibility Validation

A critical differentiator of this skill: it validates resource compatibility **before** generating any files.

| FIS Action | Required resourceType | Incompatible With |
|---|---|---|
| `aws:rds:failover-db-cluster` | `aws:rds:cluster` | Standalone RDS instances (non-Aurora) |
| `aws:rds:reboot-db-instances` | `aws:rds:db` | Aurora clusters (use failover instead) |
| `aws:elasticache:replicationgroup-interrupt-az-power` | `aws:elasticache:replicationgroup` | Standalone ElastiCache nodes |
| `aws:ec2:stop-instances` | `aws:ec2:instance` | Spot instances (may terminate instead) |
| `aws:eks:pod-network-latency` | `aws:eks:pod` | Clusters without required addon |

When incompatible, the skill explains the mismatch and suggests alternatives.

## Self-Healing CFN Deployment

After generating files, the skill immediately deploys the CloudFormation template:

1. **Permission pre-check** — Inspects the caller's IAM policy for a `cloudformation:RoleArn` condition on CreateStack/UpdateStack/DeleteStack. If found, extracts the required CFN Service Role ARN and adds `--role-arn` to all subsequent CFN commands. If no condition is found, uses IAM policy simulation (`simulate-principal-policy`) to verify the caller has CloudFormation permissions — stops early with guidance if permissions are missing.
2. **Validate** — `aws cloudformation validate-template`
3. **Deploy** — `aws cloudformation deploy --capabilities CAPABILITY_NAMED_IAM` (with `--role-arn` if required)
4. **On failure** — Extract error from stack events, analyze root cause, fix template, delete failed stack, retry
5. **Max 5 retries** — Reports failure with all attempted fixes if still failing
6. **On success** — Updates local files with real ARNs from stack outputs

## Prerequisites

- **AWS CLI** (`aws`) — Resource discovery, FIS action validation, CFN deployment. Must have permissions for FIS, IAM, CloudWatch, CloudFormation.
- [**aws-knowledge-mcp-server**](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) — Scenario Library documentation research (`aws___search_documentation`, `aws___read_documentation`)
- **jq** — JSON processing (required by scripts in `scripts/`)

**EKS Pod fault injection prerequisites:**
- EKS cluster authentication mode must be **`API_AND_CONFIG_MAP`** or **`API`**
  - Check with: `aws eks describe-cluster --name {CLUSTER} --query 'cluster.accessConfig.authenticationMode'`
  - If mode is `CONFIG_MAP` only, the user must update the cluster to `API_AND_CONFIG_MAP` first
- K8s RBAC resources (ServiceAccount, Role, RoleBinding) are **automatically managed** via a Lambda-backed CFN Custom Resource — no manual `kubectl apply` is required
- The CFN template includes a Lambda function that performs idempotent creation of K8s RBAC resources (checks if they exist before creating). The Lambda uses `botocore.signers.RequestSigner` with `x-k8s-aws-id` header for EKS token generation — this is required for EKS API server authentication (plain `sts_client.generate_presigned_url` lacks this header and results in 401 Unauthorized). The `ensure_resource` helper includes logging and error checking to prevent silent failures.
- RBAC resources use **fixed standardized names** (`fis-sa`, `fis-experiment-role`, `fis-experiment-role-binding`) shared across all FIS experiments in the same namespace
- RBAC resources are **not deleted** when a stack is removed — they are shared and may be used by other experiments
- **MANDATORY:** When using any `aws:eks:pod-*` action, you MUST follow `references/eks-pod-action-guide.md`

### Create a CloudFormation Service Role

This skill deploys CloudFormation stacks that create IAM roles, CloudWatch resources, and FIS experiment templates. Instead of using your own broad permissions, create a dedicated CloudFormation service role to limit the blast radius.

See the setup guide: https://panlm.github.io/others/cfn-service-role-for-fis-experiment-setup-guide/

Then pass `--role-arn` when deploying stacks:

```bash
aws cloudformation deploy \
  --template-file cfn-template.yaml \
  --stack-name <stack-name> \
  --role-arn arn:aws:iam::<account-id>:role/CloudFormationFISServiceRole \
  --capabilities CAPABILITY_NAMED_IAM \
  --region <region>
```

> **Benefit:** Your calling identity only needs `cloudformation:*` and `iam:PassRole` permissions. All resource creation is delegated to the service role, limiting the blast radius.

## Workflow Overview

```
Step 1: Identify scenario + region
         ↓
Step 2: Discover target resources
         ├── Scenario Library → MUST read AWS documentation first (JSON templates not available via API)
         └── Custom FIS action → query via `aws fis get-action`
         ↓
Step 2.5: EKS Pod action setup (if applicable)
         └── CFN template auto-includes Lambda + Custom Resource for K8s RBAC management
         ↓
Step 3: Validate resource-action compatibility [CRITICAL GATE]
         ├── Compatible → proceed
         └── Incompatible → suggest alternative → user confirms or abort
         ↓
Step 4: Determine monitoring config (stop conditions + dashboard metrics)
         ↓
Step 5: Generate configuration files in output directory (README.md + cfn-template.yaml)
         ↓
Step 5.5: CFN permission pre-check (detect cloudformation:RoleArn condition)
         ↓
Step 6: Deploy CFN template with self-healing loop (up to 5 retries)
         ├── ExperimentName includes random suffix → all physical resource names globally unique
         ├── On success → update local files with real ARNs
         └── On failure → report error with all attempted fixes
         ↓
Step 7: Rename output directory (append experiment template ID for easy identification)
```

## Usage Examples

```
"Prepare an AZ Power Interruption experiment for us-east-1a"
"Create FIS experiment for aws:rds:failover-db-cluster targeting my Aurora cluster"
"准备 FIS 实验，测试 AZ 断电对 EKS 和 RDS 的影响"
"测试 AZ 断电对 RDS 的影响"
"Generate chaos experiment config for EC2 CPU stress"
"Set up fault injection test for ElastiCache failover in ap-southeast-1"
"test AZ failure impact on EC2 and ElastiCache only"
"Reboot MSK broker to test Kafka consumer resilience"
"准备 MSK broker 重启的故障注入实验"
"Test ElastiCache Redis failover in us-west-2a"
"Reboot Redis primary node to test connection pool resilience"
"准备 ElastiCache Redis 主节点重启的实验"
"Test failover on ElastiCache replication group shard 0001"
"准备 ElastiCache 复制组主备切换实验"
```

## Key Design Decisions

1. **Validate before generating.** Resource-action compatibility is checked before any files are produced. This avoids the common anti-pattern of generating a full configuration, deploying a stack, and only discovering the mismatch at experiment start.

2. **Scenario Library templates come from documentation.** The 4 Scenario Library scenarios (AZ Power Interruption, AZ Application Slowdown, Cross-AZ Traffic Slowdown, Cross-Region Connectivity) cannot be generated via FIS API. The skill reads the official AWS documentation pages to extract the JSON experiment template as the authoritative source for the correct multi-action template structure.

3. **Self-healing deployment loop.** CFN errors are analyzed and fixed automatically rather than reported to the user. The goal is a working, deployed experiment template — not just files that might work.

4. **All-in-one CFN template.** The `cfn-template.yaml` contains IAM role, alarms, dashboard, and experiment template. A single `cloudformation deploy` produces everything needed.

5. **Local files stay in sync.** After successful deployment, `README.md` is updated with real ARNs and stack outputs, so the directory is an accurate record of the deployed experiment.

6. **Never starts the experiment.** This skill only prepares and deploys infrastructure. Starting the actual experiment is handled by [aws-fis-experiment-execute](../aws-fis-experiment-execute/) or manually by the user.

7. **Directory name includes experiment template ID.** After successful deployment, the output directory is renamed to append the experiment template ID (e.g., `EXT1a2b3c4d5e6f7`), making it easy to identify which directory corresponds to which experiment.

8. **EKS RBAC via CFN Custom Resource.** K8s RBAC resources (ServiceAccount, Role, RoleBinding) for EKS Pod actions are managed automatically by a Lambda-backed CFN Custom Resource. Uses fixed standardized names (`fis-sa`, `fis-experiment-role`, `fis-experiment-role-binding`) shared across all experiments in the same namespace. Lambda performs idempotent creation (skip if exists) and does NOT delete RBAC on stack removal, since other experiments may still depend on them. The Lambda uses `botocore.signers.RequestSigner` with `x-k8s-aws-id` header for EKS bearer token generation, which is required for proper EKS API server authentication.

9. **Naming convention prevents collisions.** `ExperimentName` includes a 6-character random suffix, making all CFN physical resource names (IAM Role, Dashboard, Alarm) globally unique. An optional `context-slug` in directory and resource names distinguishes experiments with the same scenario and target but different downstream services (e.g., `payment-redis` vs `payment-msk` for network fault injection).

10. **AZ Power Interruption: one Stack per AZ, shared tags.** The target AZ is hardcoded in multiple locations within the experiment template (filters, action parameters). To test a different AZ, delete the Stack and deploy a new one. Resource tags (`AzImpairmentPower`) do NOT distinguish AZ — the experiment template's internal AZ filters handle that. Tags are applied by a Lambda-backed Custom Resource within the same CFN Stack, requiring zero extra permissions on the EC2 Instance Profile. See `references/az-power-interruption-guide.md` for full details.

11. **Service-scoped sub-action pruning for AZ Power Interruption.** When the user mentions specific services (e.g., "test AZ failure for RDS"), only the relevant sub-actions are included in the experiment template — not the full 10 sub-actions. This prevents unintended impact on other business applications in the same AZ. Mandatory infrastructure sub-actions (Network Connectivity, ARC Zonal Autoshift) are always included unless explicitly excluded by the user. The agent confirms the final sub-action list with the user before generating files.

12. **Default experiment duration is 10 minutes.** All experiment scenarios and sub-actions default to `PT10M` unless the user specifies otherwise. This is shorter than the AWS documentation default of `PT30M` but sufficient for most validation scenarios, and reduces the blast radius window. Time-dependent parameters (e.g., ARC Zonal Autoshift timing) scale proportionally.

13. **Service-specific guides for services without native FIS actions.** Amazon MSK has no native FIS action, so the skill uses `aws:ssm:start-automation-execution` to invoke an SSM Automation runbook that calls `kafka:RebootBroker` directly. This requires a two-role IAM pattern: the FIS Experiment Role (trusts `fis.amazonaws.com`) passes an SSM Automation Role (trusts `ssm.amazonaws.com`) that has the MSK API permissions. Both the SSM document and the FIS experiment template are deployed in a single CFN stack. See `references/msk-guide.md` for full details. Additional services (Redshift, Neptune, OpenSearch, etc.) can be added as separate service-specific guides following the same pattern.

14. **Pre-experiment shard role detection for Redis clusters.** For ElastiCache cluster-mode-enabled replication groups, `describe-replication-groups` returns `CurrentRole` as null. The skill uses CloudWatch `IsMaster` metric to detect each node's role and records the shard distribution as a pre-experiment baseline. This enables the README to include precise expected behavior — e.g., which shards will experience primary failover in the target AZ vs. which only lose replicas.

## Directory Structure

```
aws-fis-experiment-prepare/
├── SKILL.md                              # Main skill definition (agent instructions)
├── README.md                             # This file (English)
├── README_CN.md                          # Chinese version
├── references/
│   ├── output-format.md                  # Directory layout, slug naming, README template
│   ├── cfn-base-template.md              # CFN skeleton (Parameters, IAM Role, Dashboard, FIS Template, Outputs)
│   ├── slug-conventions.md               # Scenario/context slug abbreviations, resource naming, length budget
│   ├── eks-pod-action-guide.md           # EKS Pod action guide (Lambda + Custom Resource for K8s RBAC, auth mode, memory stress calculation)
│   ├── az-power-interruption-guide.md    # AZ Power Interruption scenario guide (tagging, permissions, design decisions)
│   ├── elasticache-redis-guide.md        # ElastiCache Redis/Valkey guide (native AZ power action + primary node reboot + replication group failover via SSM)
│   └── msk-guide.md                      # Amazon MSK FIS experiment guide (broker reboot via SSM Automation)
└── scripts/
    ├── precheck-cfn-permissions.sh       # Detects required CFN service role
    ├── deploy-with-retry.sh              # Validate + deploy + delete-on-failure
    └── rename-output-dir.sh              # Appends FIS template ID to directory name
```

## Limitations

- Depends on AWS CLI access with sufficient permissions (FIS, IAM, CloudWatch, CloudFormation).
- Scenario Library documentation is read at execution time; newly added scenarios require re-running.
- Self-healing loop handles common CFN errors but may not resolve permission or account-level limits.
- Composite scenarios require resources to be pre-tagged with scenario-specific tags (e.g., `AzImpairmentPower: StopInstances`).
- Sequential MCP calls for documentation research take ~10-20 seconds.

## Related Skills

- [aws-service-chaos-research](../aws-service-chaos-research/) — Research chaos testing scenarios for any AWS service (run before this skill)
- [aws-fis-experiment-execute](../aws-fis-experiment-execute/) — Deploy and run the prepared experiment (run after this skill)
- [eks-workload-best-practice-assessment](../eks-workload-best-practice-assessment/) — Assess EKS workload configurations
