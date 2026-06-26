# Live Assessment Workflow

This document describes how to assess a live AWS resource against the compiled best-practice
checklist. The assessment is optional — only run when the user provides credentials, region,
and resource identifiers.

## General Flow

```
1. Prepare environment (source credentials, verify access)
2. Collect resource configuration (parallel AWS CLI calls)
3. Map each check item to actual config → PASS / FAIL / WARN / N/A
4. Generate assessment report
5. Offer remediation guidance
```

## Per-Service Assessment Commands

### ElastiCache Redis / Valkey

**Primary commands** (run in parallel):

```bash
# Replication group overview (topology, Multi-AZ, failover, encryption, auth)
aws elasticache describe-replication-groups \
  --replication-group-id {REPL_GROUP_ID} \
  --region {REGION} --output json

# Node-level details (engine version, node type, AZ, parameter group, subnet group)
aws elasticache describe-cache-clusters \
  --show-cache-node-info \
  --region {REGION} --output json

# Subnet group details (VPC, AZs, custom vs default)
aws elasticache describe-cache-subnet-groups \
  --cache-subnet-group-name {SUBNET_GROUP_NAME} \
  --region {REGION} --output json

# Key parameter values (reserved-memory-percent, slowlog, rename-commands, maxmemory-policy, timeout)
aws elasticache describe-cache-parameters \
  --cache-parameter-group-name {PARAM_GROUP_NAME} \
  --region {REGION} --output json

# Resource tags
aws elasticache list-tags-for-resource \
  --resource-name {REPL_GROUP_ARN} \
  --region {REGION} --output json

# Existing snapshots / backups
aws elasticache describe-snapshots \
  --replication-group-id {REPL_GROUP_ID} \
  --region {REGION} --output json

# Recent events (failover, maintenance, etc.)
aws elasticache describe-events \
  --source-type replication-group \
  --duration 10080 \
  --region {REGION} --output json
```

**Optional / secondary commands**:

```bash
# Check SNS notification subscriptions related to ElastiCache
aws sns list-subscriptions --region {REGION} --output json

# Check if Global Datastore is configured
aws elasticache describe-global-replication-groups --region {REGION} --output json
```

**How to extract replication-group-id if user only provides cluster name**:

If the user gives a cache cluster ID instead of a replication group ID, first describe the
cluster and read `ReplicationGroupId` from the response.

### Check Item Mapping for ElastiCache Redis

Below is the mapping from checklist IDs to AWS CLI response fields:

| Check ID | CLI Response Field | Pass Condition |
|----------|-------------------|----------------|
| HA-01 | `ClusterEnabled` | `true` |
| HA-02 | Count of `NodeGroupMembers` per `NodeGroup` | `>= 3` (1 primary + 2 replicas) |
| HA-03 | Count of `NodeGroups` | `>= 3` |
| HA-04 | `AutomaticFailover` + `MultiAZ` | Both `"enabled"` |
| HA-05 | Distinct AZs across all `NodeGroupMembers` | `>= 2`, ideally `>= 3` |
| HA-06 | `CacheNodeType` | Contains `r6g`, `r7g`, `m6g`, `m7g` (Graviton) |
| DR-01 | `SnapshotRetentionLimit` | `>= 1` (recommend `>= 7`) |
| DR-04 | Parameter `reserved-memory-percent` | `>= 25` |
| SEC-01 | `AtRestEncryptionEnabled` | `true` |
| SEC-02 | `TransitEncryptionEnabled` | `true` |
| SEC-03 | `AuthTokenEnabled` or RBAC user groups | Either `true` or RBAC configured |
| SEC-04 | `CacheSubnetGroupName` | Not `"default"` |
| SEC-07 | Parameter `rename-commands` | Not empty (for Redis < 6.0); or RBAC with `-@dangerous` |
| SEC-09 | RBAC enabled | Check if user groups are assigned |
| OT-01 | `AutoMinorVersionUpgrade` | `true` |
| OT-03 | Parameter `rename-commands` | Expensive commands renamed/blocked |
| OT-04 | `LogDeliveryConfigurations` | Not empty (slow log published to CloudWatch/Kinesis) |
| OT-13 | `TagList` | Not empty |

Items not in this table (e.g., FP-02 client timeout, OT-05 connection pooling) are client-side
configurations and should be marked as **WARN** with a note that they require application-level
verification.

### Amazon RDS / Aurora

**Primary commands** (run in parallel):

```bash
aws rds describe-db-instances --db-instance-identifier {DB_ID} --region {REGION} --output json
aws rds describe-db-clusters --db-cluster-identifier {CLUSTER_ID} --region {REGION} --output json
aws rds describe-db-subnet-groups --db-subnet-group-name {SUBNET_GROUP} --region {REGION} --output json
aws rds describe-db-parameter-groups --region {REGION} --output json
aws rds list-tags-for-resource --resource-name {DB_ARN} --region {REGION} --output json
aws rds describe-db-snapshots --db-instance-identifier {DB_ID} --region {REGION} --output json
aws rds describe-events --source-type db-instance --duration 10080 --region {REGION} --output json
```

### Amazon MSK

```bash
aws kafka describe-cluster --cluster-arn {CLUSTER_ARN} --region {REGION} --output json
aws kafka list-configurations --region {REGION} --output json
aws kafka describe-configuration --arn {CONFIG_ARN} --region {REGION} --output json
aws kafka list-tags-for-resource --resource-arn {CLUSTER_ARN} --region {REGION} --output json
```

### Amazon DynamoDB

```bash
aws dynamodb describe-table --table-name {TABLE_NAME} --region {REGION} --output json
aws dynamodb describe-continuous-backups --table-name {TABLE_NAME} --region {REGION} --output json
aws dynamodb list-tags-of-resource --resource-arn {TABLE_ARN} --region {REGION} --output json
aws dynamodb describe-global-table --global-table-name {TABLE_NAME} --region {REGION} --output json
```

### Amazon EKS

**Scope**: This assessment covers **AWS infrastructure-level configuration only**. All commands use
the AWS API (`aws eks`, `aws ec2`, `aws iam`). Do NOT use `kubectl` or inspect Kubernetes-internal
resources (Pods, Deployments, PDBs, NetworkPolicies, etc.) — those require a dedicated
workload-level assessment with cluster credentials and application context.

**Primary commands** (run in parallel):

```bash
aws eks describe-cluster --name {CLUSTER_NAME} --region {REGION} --output json
aws eks list-nodegroups --cluster-name {CLUSTER_NAME} --region {REGION} --output json
aws eks describe-nodegroup --cluster-name {CLUSTER_NAME} --nodegroup-name {NG_NAME} --region {REGION} --output json
aws eks list-addons --cluster-name {CLUSTER_NAME} --region {REGION} --output json
```

**Optional / secondary commands** (for deeper infra-level checks):

```bash
# Describe each installed addon's version and configuration
aws eks describe-addon --cluster-name {CLUSTER_NAME} --addon-name {ADDON_NAME} --region {REGION} --output json

# Check OIDC provider for IRSA support
aws iam list-open-id-connect-providers --region {REGION} --output json

# List access entries (for API auth mode clusters)
aws eks list-access-entries --cluster-name {CLUSTER_NAME} --region {REGION} --output json

# Check upgrade insights
aws eks list-insights --cluster-name {CLUSTER_NAME} --region {REGION} --output json
```

## Handling Errors

- **AccessDenied**: Report which command failed and what IAM permission is needed. Continue
  checking other items.
- **ResourceNotFound**: Verify the resource identifier with the user. The resource may have
  been deleted or the name may be wrong.
- **Expired credentials**: Prompt the user to refresh credentials and retry.
- **Region mismatch**: If a describe command returns empty, confirm the correct region with the user.

## Assessment Status Definitions

| Status | When to use |
|--------|-------------|
| **PASS** | The actual configuration meets or exceeds the documented recommendation. Include the actual value in the finding. |
| **FAIL** | The actual configuration does not meet the recommendation. Include both the expected and actual values. |
| **WARN** | The check cannot be fully verified from infrastructure-level API calls (e.g., client-side settings like connection pooling, retry logic), or the configuration partially meets the recommendation. |
| **N/A** | The check does not apply to this specific resource configuration or the user's stated requirements (e.g., Global Datastore when cross-region DR is not needed). |
