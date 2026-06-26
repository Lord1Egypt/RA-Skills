# Scenario Slug & Naming Conventions

Defines the standard abbreviations for `SCENARIO_SLUG` and `CONTEXT_SLUG` used
in output directory names, CFN stack names, and physical resource names.

## Contents

- Scenario Slug Abbreviation Table
- Abbreviation Rules for Unlisted Actions
- Context Slug Guidance
- CFN Physical Resource Naming
- Name Length Budget
- ExperimentName Composition

## Scenario Slug Abbreviation Table

Standard abbreviations for `SCENARIO_SLUG`. Keeps resource names short while
remaining readable. **Max 18 characters.**

| Scenario / Action | SCENARIO_SLUG | Len |
|---|---|---|
| AZ Power Interruption | `az-power-int` | 13 |
| AZ Application Slowdown | `az-app-slow` | 11 |
| Cross-AZ Traffic Slowdown | `xaz-traffic-slow` | 17 |
| Cross-Region Connectivity | `xregion-conn` | 12 |
| `aws:eks:pod-network-latency` | `pod-net-latency` | 15 |
| `aws:eks:pod-network-packet-loss` | `pod-net-pktloss` | 15 |
| `aws:eks:pod-network-blackhole-port` | `pod-net-blackhole` | 17 |
| `aws:eks:pod-delete` | `pod-delete` | 10 |
| `aws:eks:pod-cpu-stress` | `pod-cpu-stress` | 14 |
| `aws:eks:pod-memory-stress` | `pod-mem-stress` | 14 |
| `aws:eks:pod-io-stress` | `pod-io-stress` | 13 |
| `aws:ec2:stop-instances` | `ec2-stop` | 8 |
| EC2 CPU stress | `ec2-cpu-stress` | 14 |
| `aws:rds:failover-db-cluster` | `rds-failover` | 12 |
| `aws:rds:reboot-db-instances` | `rds-reboot` | 10 |
| `aws:elasticache:replicationgroup-interrupt-az-power` | `ec-rg-az-power` | 14 |
| `aws:ebs:pause-io` | `ebs-pause-io` | 12 |
| `aws:ssm:send-command` | `ssm-cmd` | 7 |
| `aws:ssm:start-automation-execution` (MSK reboot) | `ssm-auto-msk-reboot` | 20 |
| `aws:ssm:start-automation-execution` (ElastiCache reboot) | `ssm-auto-ec-reboot` | 19 |
| `aws:ssm:start-automation-execution` (ElastiCache failover) | `ssm-auto-ec-failover` | 21 |

## Abbreviation Rules for Unlisted Actions

When a scenario is not in the table above, build the slug using these
abbreviations:

| Full Word | Abbreviation |
|---|---|
| `network` | `net` |
| `packet-loss` | `pktloss` |
| `memory` | `mem` |
| `cross-az` | `xaz` |
| `cross-region` | `xregion` |
| `interruption` | `int` |
| `slowdown` | `slow` |
| `connectivity` | `conn` |
| `application` | `app` |
| `replicationgroup` | `rg` |
| `elasticache` | `ec` |

**Additional rules:**

- EKS pod actions: keep the `pod-` prefix, drop `eks-`
  (e.g., `pod-net-pktloss`, not `eks-net-pktloss`).
- SSM Automation actions: use the `ssm-auto-` prefix + service abbreviation +
  operation (e.g., `ssm-auto-msk-reboot`, `ssm-auto-ec-reboot`).
- Service abbreviations for future additions: `redshift` -> `rs`,
  `neptune` -> `np`, `opensearch` -> `os`, `memorydb` -> `memdb`.
- Target max 18 characters.

## Context Slug Guidance

| Action Type | CONTEXT_SLUG Source | Example |
|---|---|---|
| `aws:eks:pod-network-latency` | Downstream service name (from port/endpoint/user description) | `redis`, `msk`, `rds` |
| `aws:eks:pod-network-packet-loss` | Same as above | `redis`, `dynamodb` |
| `aws:eks:pod-network-blackhole-port` | Same as above | `kafka`, `elasticache` |
| `aws:eks:pod-delete` | Omit (no directional context) | *(empty)* |
| `aws:eks:pod-cpu-stress` | Omit | *(empty)* |
| `aws:eks:pod-memory-stress` | Omit | *(empty)* |
| Non-EKS actions | Omit unless the user specifies a distinguishing purpose | *(empty)* |

Extract the downstream service context from the user's description. Examples:

- "payment pod 到 redis 的丢包" -> `CONTEXT_SLUG=redis`
- "payment pod 到 msk 的网络延迟" -> `CONTEXT_SLUG=msk`

## CFN Physical Resource Naming

Resources with generous name limits (128-256 chars) use `ExperimentName` for
readability. Resources with tight limits (64 chars) use `RandomSuffix` with a
fixed prefix.

| Resource | Naming Pattern | Example | AWS Limit |
|---|---|---|---|
| CFN Stack | `fis-{ExperimentName}` | `fis-pod-net-pktloss-payment-redis-a3x7k2` | 128 |
| IAM Role (FIS) | `fis-role-{RandomSuffix}` | `fis-role-a3x7k2` | 64 |
| Dashboard | `fis-{ExperimentName}` | `fis-pod-net-pktloss-payment-redis-a3x7k2` | 256 |
| Alarm | `fis-stop-{ExperimentName}` | `fis-stop-pod-net-pktloss-payment-redis-a3x7k2` | 255 |
| Lambda Role | `fis-lambda-role-{RandomSuffix}` | `fis-lambda-role-a3x7k2` | 64 |
| Lambda Function | `fis-rbac-{RandomSuffix}` | `fis-rbac-a3x7k2` | 64 |

## Name Length Budget

| Resource | Pattern | Max Length | AWS Limit | Safe? |
|---|---|---|---|---|
| CFN Stack | `fis-` (4) + ExperimentName (max 57) | 61 | 128 | Yes |
| IAM Role | `fis-role-` (9) + RandomSuffix (6) | 15 | 64 | Yes |
| Dashboard | `fis-` (4) + ExperimentName (max 57) | 61 | 256 | Yes |
| Alarm | `fis-stop-` (9) + ExperimentName (max 57) | 66 | 255 | Yes |
| Lambda Role | `fis-lambda-role-` (16) + RandomSuffix (6) | 22 | 64 | Yes |
| Lambda Function | `fis-rbac-` (9) + RandomSuffix (6) | 15 | 64 | Yes |

All resources with a 64-char AWS limit (IAM roles, Lambda functions) use
`RandomSuffix` only — always safe regardless of slug lengths. Resources with
generous limits (128-256 chars) use `ExperimentName` for readability.

## ExperimentName Composition

```
# Without context slug:
ExperimentName = {SCENARIO_SLUG}-{TARGET_SLUG}-{RANDOM_SUFFIX}

# With context slug:
ExperimentName = {SCENARIO_SLUG}-{TARGET_SLUG}-{CONTEXT_SLUG}-{RANDOM_SUFFIX}
```

**Example mappings:**

| Experiment | Output Directory (initial) | Stack Name |
|---|---|---|
| payment pod -> redis packet-loss | `2026-04-11-10-30-00-pod-net-pktloss-payment-redis` | `fis-pod-net-pktloss-payment-redis-a3x7k2` |
| payment pod -> msk packet-loss | `2026-04-11-10-30-05-pod-net-pktloss-payment-msk` | `fis-pod-net-pktloss-payment-msk-b8y2m1` |
| payment pod delete | `2026-04-11-10-30-10-pod-delete-payment` | `fis-pod-delete-payment-c4z9n3` |
| AZ power interruption | `2026-04-11-10-30-15-az-power-int-my-cluster` | `fis-az-power-int-my-cluster-d5w1p7` |

After successful CFN deployment, directories are renamed to append the
experiment template ID (e.g., `...-payment-redis-EXT1a2b3c4d5e6f7`).
