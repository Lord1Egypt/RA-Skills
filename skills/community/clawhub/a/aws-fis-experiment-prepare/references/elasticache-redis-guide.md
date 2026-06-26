# ElastiCache Redis/Valkey — FIS Experiment Guide

## Contents

- Scope
- Supported Fault Scenarios (Decision Table)
- Scenario 1: AZ Power Interruption (Native FIS Action)
  - Action Details
  - Target Selection
  - IAM Permissions
  - Dashboard Metrics
- Scenario 2: Primary Node Reboot (SSM Automation)
  - Critical Limitation
  - Architecture Overview
  - SSM Automation Runbook
  - IAM Design — Two-Role Pattern
  - Discovery: Identify Primary Node
  - CFN Template Integration
  - Scenario Slug
- Scenario 3: Replication Group Failover (SSM Automation)
  - Architecture Overview
  - SSM Automation Runbook
  - IAM Design — Two-Role Pattern
  - Discovery: Identify Node Group
  - CFN Template Integration
  - Scenario Slug
- Resource Discovery
- Compatibility Validation
- Common Mistakes
- Key Constraints

## Scope

This guide covers FIS experiment preparation for **Amazon ElastiCache** with
Redis or Valkey engines. Use it when the user wants to:

- Simulate AZ-level power interruption affecting ElastiCache nodes
- Reboot the primary node to test application connection resilience
- Trigger automatic failover on a specific replication group (shard)
- Test failover behavior and connection pool recovery

**Do NOT use this guide when:**
- The fault is network-level between application pods and ElastiCache — use
  `aws:eks:pod-network-*` or `aws:network:disrupt-connectivity` instead
- ElastiCache is one service among many in a broader AZ power interruption
  scenario — use `references/az-power-interruption-guide.md` (which already
  includes ElastiCache as a sub-action)

## Supported Fault Scenarios (Decision Table)

| User Intent | FIS Action | Guide Section |
|---|---|---|
| AZ-level power interruption (failover + blocked replacements) | `aws:elasticache:replicationgroup-interrupt-az-power` (native) | Scenario 1 |
| Reboot primary node (test reconnection and retry logic) | `aws:ssm:start-automation-execution` (SSM Automation) | Scenario 2 |
| Failover a single replication group / shard (primary-to-replica promotion) | `aws:ssm:start-automation-execution` (SSM Automation) | Scenario 3 |
| Network latency or packet loss between app and Redis | `aws:eks:pod-network-latency` / `aws:eks:pod-network-packet-loss` | `references/eks-pod-action-guide.md` |

If the user's intent is ambiguous, ask which fault type they want before
proceeding.

## Scenario 1: AZ Power Interruption (Native FIS Action)

### Action Details

| Field | Value |
|---|---|
| Action ID | `aws:elasticache:replicationgroup-interrupt-az-power` |
| Resource Type | `aws:elasticache:replicationgroup` |
| Engines | Redis, Valkey |
| Prerequisite | Multi-AZ enabled on the replication group |
| Not Supported | ElastiCache Serverless |

**Behavior:** Interrupts power to nodes in the specified AZ. When the primary
node is in the target AZ, the replica with the least replication lag is promoted
to primary. Read replica replacements in the target AZ are **blocked for the
entire duration** of the action, so the replication group operates at reduced
capacity. Only one AZ per replication group can be impacted at a time.

**Parameters:**
- `duration` — PT1M to PT12H (default: `PT10M`)

**Target parameters:**
- `availabilityZoneIdentifier` — the AZ containing the node(s) to impair

**Note:** This action was renamed from `aws:elasticache:interrupt-cluster-az-power`
to `aws:elasticache:replicationgroup-interrupt-az-power`. Always use the new name.

### Target Selection

ElastiCache replication groups **do NOT support `resourceArns`** — you MUST use
`resourceTags`. This is a known platform limitation already documented in the
main SKILL.md.

```yaml
Targets:
  ElastiCacheTarget:
    ResourceType: aws:elasticache:replicationgroup
    ResourceTags:
      - Key: '{TAG_KEY}'
        Value: '{TAG_VALUE}'
    Parameters:
      availabilityZoneIdentifier: '{TARGET_AZ}'
    SelectionMode: ALL
```

**IMPORTANT:** Neither `resourceArns` nor `filters` are supported for this
resource type. Only `resourceTags` combined with
`Parameters.availabilityZoneIdentifier` works.

### IAM Permissions

**No AWS managed policy exists for ElastiCache FIS actions.** Attach an inline
policy to the FIS Experiment Role:

```yaml
- Sid: ElastiCacheActions
  Effect: Allow
  Action:
    - elasticache:InterruptClusterAzPower
    - elasticache:DescribeReplicationGroups
  Resource: '*'
- Sid: TagResolution
  Effect: Allow
  Action:
    - tag:GetResources
  Resource: '*'
```

### Dashboard Metrics

| Widget | Metrics | Dimension |
|---|---|---|
| Replication & Availability | `ReplicationLag`, `IsPrimary` | `ReplicationGroupId`, `CacheClusterId` |
| Performance | `EngineCPUUtilization`, `CurrConnections`, `NewConnections` | `CacheClusterId` |
| Cache Efficiency | `CacheHitRate`, `Evictions`, `CurrItems` | `CacheClusterId` |

**Namespace:** `AWS/ElastiCache`

## Scenario 2: Primary Node Reboot (SSM Automation)

ElastiCache has **no native FIS action for single-node reboot**. Instead, use
`aws:ssm:start-automation-execution` to run an SSM Automation runbook that calls
`elasticache:RebootCacheCluster`.

**Use case:** Validate application connection pool resilience and retry logic
during a brief primary node reboot (typically 1-3 minutes recovery). This is
less disruptive than AZ power interruption — only the targeted node reboots,
and replica replacements are NOT blocked.

**Reference:** Based on
[aws-samples/fis-template-library/elasticache-redis-primary-node-reboot](https://github.com/aws-samples/fis-template-library/tree/main/elasticache-redis-primary-node-reboot),
adapted to the single-CFN-stack pattern used by this skill.

---

### CRITICAL LIMITATION

> **`RebootCacheCluster` is NOT supported on cluster-mode-enabled clusters.**
>
> This API works **only** with cluster mode **disabled** (Memcached, Valkey,
> and Redis OSS). If the user's replication group has `ClusterEnabled: true`,
> the reboot call will fail.
>
> **Alternatives when cluster mode is enabled:**
> - Use **Scenario 1** (AZ power interruption) — it supports both cluster modes
> - Use network-level fault injection (`aws:eks:pod-network-*`)
>
> **How to check:** Run `aws elasticache describe-replication-groups` and
> inspect the `ClusterEnabled` field. It must be `false` for Scenario 2.

---

### Architecture Overview

```
FIS Experiment Template
  └── Action: aws:ssm:start-automation-execution
        ├── documentArn: arn:aws:ssm:{REGION}:{ACCOUNT_ID}:document/{DOC_NAME}
        ├── documentParameters: {"CacheClusterId":"...","AutomationAssumeRoleArn":"..."}
        └── maxDuration: PT15M
              │
              v
SSM Automation Runbook (schema 0.3)
  ├── Step 1: RebootPrimaryNode     (aws:executeAwsApi -> elasticache:RebootCacheCluster)
  └── Step 2: WaitForNodeAvailable  (aws:waitForAwsResourceProperty -> elasticache:DescribeCacheClusters)
```

### SSM Automation Runbook

Schema version **0.3** is required for all Automation documents.

```yaml
description: 'FIS: Reboot ElastiCache primary node to test client resilience'
schemaVersion: '0.3'
assumeRole: '{{ AutomationAssumeRoleArn }}'
parameters:
  AutomationAssumeRoleArn:
    type: String
    description: IAM Role ARN for SSM Automation to assume
  CacheClusterId:
    type: String
    description: CacheClusterId of the primary node to reboot
mainSteps:
  - name: RebootPrimaryNode
    action: aws:executeAwsApi
    inputs:
      Service: elasticache
      Api: RebootCacheCluster
      CacheClusterId: '{{ CacheClusterId }}'
      CacheNodeIdsToReboot:
        - '0001'
    outputs:
      - Name: CacheClusterId
        Selector: $.CacheCluster.CacheClusterId
        Type: String

  - name: WaitForNodeAvailable
    action: aws:waitForAwsResourceProperty
    timeoutSeconds: 600
    inputs:
      Service: elasticache
      Api: DescribeCacheClusters
      CacheClusterId: '{{ CacheClusterId }}'
      PropertySelector: $.CacheClusters[0].CacheClusterStatus
      DesiredValues:
        - available
```

### IAM Design — Two-Role Pattern

Same pattern as `references/msk-guide.md`:

| Role | Trusted By | Purpose | Permissions |
|---|---|---|---|
| FIS Experiment Role | `fis.amazonaws.com` | FIS starts SSM Automation | `AWSFaultInjectionSimulatorSSMAccess` + `iam:PassRole` for SSM Automation Role |
| SSM Automation Role | `ssm.amazonaws.com` | SSM calls `elasticache:RebootCacheCluster` | `elasticache:RebootCacheCluster`, `elasticache:DescribeCacheClusters` |

**SSM Automation Role inline policy:**

```json
{
  "Effect": "Allow",
  "Action": [
    "elasticache:RebootCacheCluster",
    "elasticache:DescribeCacheClusters"
  ],
  "Resource": "*"
}
```

**FIS Experiment Role additions** (beyond the managed policy):

```yaml
- Sid: PassRoleToSSM
  Effect: Allow
  Action: iam:PassRole
  Resource: !GetAtt SSMAutomationRole.Arn
  Condition:
    StringEquals:
      iam:PassedToService: ssm.amazonaws.com
```

### Discovery: Identify Primary Node

The prepare skill must identify the primary node's `CacheClusterId` before
generating the template.

**Cluster mode disabled** — `CurrentRole` is available directly:

```bash
aws elasticache describe-replication-groups \
  --replication-group-id {RG_ID} \
  --query 'ReplicationGroups[0].NodeGroups[].NodeGroupMembers[].[CacheClusterId,CurrentRole,PreferredAvailabilityZone]' \
  --output table
# Pick the node where CurrentRole == "primary"
```

If the user does not know the replication group ID, list all replication groups:

```bash
aws elasticache describe-replication-groups \
  --query 'ReplicationGroups[].{Id:ReplicationGroupId,Status:Status,MultiAZ:MultiAZ,ClusterEnabled:ClusterEnabled}' \
  --output table
```

### Shard Role Detection for Cluster-Mode-Enabled

**Problem:** `describe-replication-groups` returns `CurrentRole` as **null**
for cluster-mode-enabled clusters. This is AWS expected behavior.

**Solution:** Use CloudWatch `IsMaster` metric to determine each node's role:
- `IsMaster` = `1.0` → Primary
- `IsMaster` = `0.0` → Replica

**Method:**
1. Get all member clusters and their AZ/Shard mapping from
   `describe-replication-groups` → `NodeGroups[].NodeGroupMembers[]`
2. For each `CacheClusterId`, query CloudWatch `IsMaster` metric using
   `get-metric-data` with `Period=60` and retrieve only the **most recent single
   datapoint** (e.g., last 5 minutes, take the latest value). Do NOT use
   `Average` over a longer window — after a failover the role flips from 1→0
   or 0→1, and averaging would produce misleading intermediate values like 0.5.
   (namespace `AWS/ElastiCache`, dimensions `CacheClusterId` + `CacheNodeId=0001`)
3. Build a shard distribution table: Shard → Node → AZ → Role

**When to run:** Always run this detection for **cluster-mode-enabled**
replication groups (both Scenario 1 and Scenario 2 validation). Record the
result as a pre-experiment baseline.

**Why it matters for FIS experiments:**
- **Scenario 1 (AZ power):** Knowing which AZ holds each shard's primary
  predicts how many failovers the experiment will trigger
- **Scenario 2 validation:** Confirms the cluster is cluster-mode-enabled
  and should be redirected to Scenario 1

### Pre-Experiment Shard Distribution Report

For **any** ElastiCache Redis/Valkey experiment targeting a cluster-mode-enabled
replication group, record the shard distribution in the output README. Include:

- Each shard's slot range
- Each node's CacheClusterId, AZ, and role (Primary/Replica)
- For AZ-scoped experiments: which shards have their primary in the target AZ
  (these will failover) vs. which only lose replicas

This baseline enables the README's "Expected Behavior" section to state
precisely: "Shard 0001 primary is in us-west-2a — expect failover to
us-west-2b replica. Shard 0002 only loses a replica — no failover."

### CFN Template Integration

#### SSM Document Resource

```yaml
SSMAutomationDocument:
  Type: AWS::SSM::Document
  Properties:
    DocumentType: Automation
    DocumentFormat: YAML
    Name: !Sub 'fis-${ExperimentName}-runbook'
    Content:
      description: 'FIS: Reboot ElastiCache primary node to test client resilience'
      schemaVersion: '0.3'
      assumeRole: '{{ AutomationAssumeRoleArn }}'
      parameters:
        AutomationAssumeRoleArn:
          type: String
          description: IAM Role ARN
        CacheClusterId:
          type: String
          description: CacheClusterId of the primary node to reboot
      mainSteps:
        - name: RebootPrimaryNode
          action: aws:executeAwsApi
          inputs:
            Service: elasticache
            Api: RebootCacheCluster
            CacheClusterId: '{{ CacheClusterId }}'
            CacheNodeIdsToReboot:
              - '0001'
          outputs:
            - Name: CacheClusterId
              Selector: $.CacheCluster.CacheClusterId
              Type: String
        - name: WaitForNodeAvailable
          action: aws:waitForAwsResourceProperty
          timeoutSeconds: 600
          inputs:
            Service: elasticache
            Api: DescribeCacheClusters
            CacheClusterId: '{{ CacheClusterId }}'
            PropertySelector: $.CacheClusters[0].CacheClusterStatus
            DesiredValues:
              - available

SSMAutomationRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: !Sub 'fis-ssm-auto-role-${RandomSuffix}'
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: ssm.amazonaws.com
          Action: sts:AssumeRole
    Policies:
      - PolicyName: ElastiCacheApiAccess
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Sid: ElastiCacheReboot
              Effect: Allow
              Action:
                - elasticache:RebootCacheCluster
                - elasticache:DescribeCacheClusters
              Resource: '*'
```

#### FIS Experiment Template Action

```yaml
FISExperimentTemplate:
  Type: AWS::FIS::ExperimentTemplate
  DependsOn:
    - FISExperimentRole
    - SSMAutomationDocument
  Properties:
    Description: !Sub 'FIS: ${ExperimentName}'
    RoleArn: !GetAtt FISExperimentRole.Arn
    StopConditions:
      - Source: 'none'
    Tags:
      Name: !Ref ExperimentName
    Targets: {}
    Actions:
      RebootPrimaryNode:
        ActionId: aws:ssm:start-automation-execution
        Parameters:
          documentArn: !Sub 'arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:document/fis-${ExperimentName}-runbook'
          documentParameters: !Sub >-
            {"AutomationAssumeRoleArn":"${SSMAutomationRole.Arn}",
             "CacheClusterId":"{PRIMARY_CACHE_CLUSTER_ID}"}
          maxDuration: 'PT15M'
```

### Scenario Slug

| Scenario | SCENARIO_SLUG | Example Stack Name |
|---|---|---|
| ElastiCache AZ power interruption | `ec-rg-az-power` | `fis-ec-rg-az-power-my-rg-a3x7k2` |
| ElastiCache primary node reboot | `ssm-auto-ec-reboot` | `fis-ssm-auto-ec-reboot-my-rg-a3x7k2` |
| ElastiCache replication group failover | `ssm-auto-ec-failover` | `fis-ssm-auto-ec-failover-my-rg-a3x7k2` |

## Scenario 3: Replication Group Failover (SSM Automation)

ElastiCache has **no native FIS action for triggering automatic failover on a
single replication group (shard)**. Instead, use
`aws:ssm:start-automation-execution` to run an SSM Automation runbook that calls
`elasticache:TestFailover`.

**Use case:** Validate application failover handling when the primary node of a
specific shard is promoted to a replica in a different AZ. This simulates a
real failover event — the current primary becomes a replica and a replica is
promoted to the new primary. More realistic than a reboot (Scenario 2) because
the endpoint topology actually changes.

**Key differences from Scenario 2 (Reboot):**

| Aspect | Scenario 2 (Reboot) | Scenario 3 (TestFailover) |
|---|---|---|
| API | `RebootCacheCluster` | `TestFailover` |
| Effect | Primary node restarts, same node stays primary | Replica promoted to primary, old primary becomes replica |
| Cluster mode | Disabled only | Both disabled and enabled |
| Parameters | `CacheClusterId` | `ReplicationGroupId` + `NodeGroupId` |
| Recovery | Node reboots and returns to `available` | Failover completes, roles swap |

**Reference:** Based on the
[ElastiCache TestFailover API](https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_TestFailover.html).

---

### Architecture Overview

Same architecture as Scenario 2 (FIS → SSM Automation → ElastiCache API).
Differences:

- **Step 1:** `elasticache:TestFailover` (instead of `RebootCacheCluster`)
- **Step 2:** waits on `DescribeReplicationGroups` status (instead of
  `DescribeCacheClusters`)
- **documentParameters:** `ReplicationGroupId` + `NodeGroupId` (instead of
  `CacheClusterId`)

### SSM Automation Runbook

Schema version **0.3** is required for all Automation documents.

```yaml
description: 'FIS: Test automatic failover on ElastiCache replication group'
schemaVersion: '0.3'
assumeRole: '{{ AutomationAssumeRoleArn }}'
parameters:
  AutomationAssumeRoleArn:
    type: String
    description: IAM Role ARN for SSM Automation to assume
  ReplicationGroupId:
    type: String
    description: Replication group ID to trigger failover on
  NodeGroupId:
    type: String
    description: >-
      Node group (shard) ID to failover. For cluster-mode-disabled,
      this is always '0001'. For cluster-mode-enabled, specify the
      target shard ID (e.g., '0001', '0002').
mainSteps:
  - name: TestFailover
    action: aws:executeAwsApi
    inputs:
      Service: elasticache
      Api: TestFailover
      ReplicationGroupId: '{{ ReplicationGroupId }}'
      NodeGroupId: '{{ NodeGroupId }}'
    outputs:
      - Name: ReplicationGroupId
        Selector: $.ReplicationGroup.ReplicationGroupId
        Type: String

  - name: WaitForReplicationGroupAvailable
    action: aws:waitForAwsResourceProperty
    timeoutSeconds: 600
    inputs:
      Service: elasticache
      Api: DescribeReplicationGroups
      ReplicationGroupId: '{{ ReplicationGroupId }}'
      PropertySelector: $.ReplicationGroups[0].Status
      DesiredValues:
        - available
```

### IAM Design — Two-Role Pattern

Same two-role pattern as Scenario 2 (FIS Experiment Role + SSM Automation
Role). FIS Experiment Role `iam:PassRole` block is identical. Only the SSM
Automation Role permissions differ:

```json
{
  "Effect": "Allow",
  "Action": [
    "elasticache:TestFailover",
    "elasticache:DescribeReplicationGroups"
  ],
  "Resource": "*"
}
```

### Discovery: Identify Node Group

Use the same `describe-replication-groups` commands from Scenario 2's
"Discovery: Identify Primary Node" section to inspect the replication group.

The target parameter is `NodeGroupId` (not `CacheClusterId`):

- **Cluster mode disabled** — always `0001` (only one node group).
- **Cluster mode enabled** — list shards via
  `NodeGroups[].NodeGroupId` and ask the user which shard to target.
  Use the "Shard Role Detection for Cluster-Mode-Enabled" method from
  Scenario 2 if `CurrentRole` is null.

### CFN Template Integration

**SSM Document and SSM Automation Role:** Follow the same CFN pattern as
Scenario 2. Use the runbook from the "SSM Automation Runbook" section above
as `AWS::SSM::Document.Content`, and create the `SSMAutomationRole` with the
permissions from the "IAM Design — Two-Role Pattern" section above.

#### FIS Experiment Template Action

```yaml
FISExperimentTemplate:
  Type: AWS::FIS::ExperimentTemplate
  DependsOn:
    - FISExperimentRole
    - SSMAutomationDocument
  Properties:
    Description: !Sub 'FIS: ${ExperimentName}'
    RoleArn: !GetAtt FISExperimentRole.Arn
    StopConditions:
      - Source: 'none'
    Tags:
      Name: !Ref ExperimentName
    Targets: {}
    Actions:
      TestFailover:
        ActionId: aws:ssm:start-automation-execution
        Parameters:
          documentArn: !Sub 'arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:document/fis-${ExperimentName}-runbook'
          documentParameters: !Sub >-
            {"AutomationAssumeRoleArn":"${SSMAutomationRole.Arn}",
             "ReplicationGroupId":"{REPLICATION_GROUP_ID}",
             "NodeGroupId":"{NODE_GROUP_ID}"}
          maxDuration: 'PT15M'
```

### Scenario Slug

See the consolidated slug table in Scenario 2's Scenario Slug section.

## Resource Discovery

### Describe Replication Group

```bash
aws elasticache describe-replication-groups \
  --replication-group-id {RG_ID} \
  --region {TARGET_REGION}
```

**Key fields to check:**
- `Status` — must be `available`
- `MultiAZ` — must be `enabled` (required for AZ power interruption)
- `AutomaticFailover` — must be `enabled` (required for both scenarios)
- `ClusterEnabled` — `true` = cluster mode enabled, `false` = cluster mode disabled
- `NodeGroups[].NodeGroupMembers[]` — node details, roles, and AZs

### List Tags

```bash
aws elasticache list-tags-for-resource \
  --resource-name "arn:aws:elasticache:{REGION}:{ACCOUNT_ID}:replicationgroup:{RG_ID}"
```

## Compatibility Validation

| Check | Requirement | How to Detect | Impact |
|---|---|---|---|
| Multi-AZ | Enabled | `MultiAZ: enabled` in describe output | AZ power action requires Multi-AZ |
| Automatic Failover | Enabled | `AutomaticFailover: enabled` | Both scenarios need automatic failover for proper recovery |
| Engine | Redis or Valkey | `Engine` field — must NOT be `memcached` | Memcached does not support replication groups |
| Deployment | Non-serverless | Verify the replication group exists (serverless uses a different API) | AZ power action does not support serverless |
| Cluster Mode (Scenario 1) | Disabled or Enabled | `ClusterEnabled` field | Both modes are supported for AZ power interruption |
| Cluster Mode (Scenario 2) | **Disabled only** | `ClusterEnabled` must be `false` | **`RebootCacheCluster` is NOT supported on cluster-mode-enabled clusters.** If `ClusterEnabled: true`, use Scenario 1 instead |
| Cluster Mode (Scenario 3) | Disabled or Enabled | `ClusterEnabled` field | Both modes are supported for `TestFailover` |
| Automatic Failover (Scenario 3) | **Enabled** | `AutomaticFailover: enabled` | `TestFailover` requires automatic failover to be enabled |

**If incompatible:** Explain the specific mismatch and suggest alternatives:
- Standalone ElastiCache (no replication group) — must create a replication
  group with Multi-AZ before running FIS experiments
- Memcached — not supported for replication group actions; consider Redis/Valkey
  or test at the network level
- Cluster mode enabled + user wants primary node reboot —
  `RebootCacheCluster` is not supported; recommend Scenario 1 (AZ power
  interruption) or network-level fault injection (`aws:eks:pod-network-*`)

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using `resourceArns` for ElastiCache targets | Replication groups only support `resourceTags` — never use `resourceArns` |
| Targeting Serverless ElastiCache | Not supported by `replicationgroup-interrupt-az-power`. Serverless handles failover behind a managed proxy |
| Using old action ID `aws:elasticache:interrupt-cluster-az-power` | Use the renamed `aws:elasticache:replicationgroup-interrupt-az-power` |
| Forgetting `tag:GetResources` permission | Required for tag-based target resolution |
| Not checking `AutomaticFailover` status | Both scenarios require `AutomaticFailover: enabled`. Without it, failover does not occur |
| Assuming `CacheNodeIdsToReboot` varies | For single-node reboot, the node ID is always `0001` |
| Rebooting a replica instead of the primary | Discover the primary node's `CacheClusterId` at prepare time using `CurrentRole == "primary"` (cluster mode disabled) or CloudWatch `IsMaster` metric (cluster mode enabled). If the primary changes before execution, the reboot still validates connection resilience — just on a different node |
| Using `CurrentRole` on cluster-mode-enabled | `CurrentRole` returns null for cluster-mode-enabled clusters. Use CloudWatch `IsMaster` metric instead |
| Skipping shard distribution baseline | For cluster-mode-enabled, always record shard roles before the experiment. Without the baseline, you cannot determine which shards experienced failover |
| Attempting reboot on a cluster-mode-enabled replication group | `RebootCacheCluster` is NOT supported on cluster-mode-enabled clusters. Check `ClusterEnabled` first. Use Scenario 1 (AZ power) or Scenario 3 (TestFailover) instead |
| Using FIS Experiment Role as SSM Automation `assumeRole` | Same as MSK — the FIS role trusts `fis.amazonaws.com`, not `ssm.amazonaws.com`. Create a dedicated SSM Automation Role |
| Using wrong `NodeGroupId` for `TestFailover` | For cluster-mode-disabled, `NodeGroupId` is always `0001`. For cluster-mode-enabled, discover available shard IDs via `describe-replication-groups` → `NodeGroups[].NodeGroupId` |
| Calling `TestFailover` multiple times concurrently on the same replication group (cluster-mode-enabled) | The first node replacement must complete before a subsequent call. Check for failover events via `DescribeEvents` or wait for the replication group to return to `available` |
| Exceeding `TestFailover` rate limit | Up to 15 node groups per rolling 24-hour period. Plan experiments accordingly |

## Key Constraints

| Constraint | Detail |
|---|---|
| Target resolution | Only `resourceTags` — not `resourceArns` or `filters` |
| AZ limit | One AZ per replication group can be impacted at a time |
| Reboot recovery time | Primary node reboot typically takes 1-3 minutes to return to `available` |
| SSM document naming | Max 128 characters. Follow the `fis-{ExperimentName}-runbook` convention |
| `documentParameters` format | Must be a JSON string, not a JSON object |
| `CacheNodeIdsToReboot` | Always `["0001"]` for single-node reboot |
| Cluster mode (Scenario 1) | Both cluster-mode-enabled and cluster-mode-disabled are supported |
| Cluster mode (Scenario 2) | **Cluster mode disabled ONLY.** `RebootCacheCluster` is not supported on cluster-mode-enabled clusters. Use Scenario 1 or Scenario 3 instead |
| Cluster mode (Scenario 3) | Both cluster-mode-enabled and cluster-mode-disabled are supported |
| `TestFailover` rate limit | Up to 15 node groups per rolling 24-hour period per account |
| `TestFailover` sequential constraint | For cluster-mode-enabled, the first node replacement must complete before a subsequent `TestFailover` call on a different shard in the same replication group |
| `NodeGroupId` format | 1-4 digit numeric string (pattern: `\d+`). Always `0001` for cluster-mode-disabled |
| Rollback | All three scenarios are self-recovering. AZ power: replicas resume when the action ends. Reboot: the node comes back online automatically. TestFailover: roles swap completes, new primary accepts writes |
