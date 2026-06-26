# AZ Availability: Power Interruption — Scenario Guide

## Contents

- Scope
- Service-Scoped Sub-Action Pruning (Blast Radius Control)
  - Pruning Rules
  - Sub-Action to Service Mapping
  - Dependency Rules Between Sub-Actions
  - Examples
  - Impact on Tagging, Permissions, and Dashboard
- Default Experiment Duration
- Official Documentation (Required Reading)
- Design Decision: One Stack Per AZ
- Resource Tagging Strategy (Lambda Custom Resource + tag key/value table)
- FIS Experiment Role — Required Permissions
- Service-Linked Role (ARC Zonal Autoshift)
- Pause Instance Launches — Default: Remove
- Limitations
- Additional Sub-Action Details (S3 Express, ARC Zonal Autoshift timing)
- Custom Resource Lambda — Tagging Logic (cfn-response callback, ASG two-step)
- Quick Reference: CFN Stack Contents

## Scope

This guide applies when the user requests an **AZ Availability: Power Interruption**
scenario from the FIS Scenario Library. It covers the unique requirements of this
scenario that differ from custom single-action FIS experiments.

**This scenario includes 10 sub-actions:** Stop-Instances, Stop-ASG-Instances,
Pause-Instance-Launches, Pause-ASG-Scaling, Pause-Network-Connectivity, Failover-RDS,
Pause-ElastiCache, Start-ARC-Zonal-Autoshift, Pause-EBS-IO (`aws:ebs:pause-volume-io`),
and Disrupt-S3-Express-One-Zone.

**MANDATORY:** Complete all steps in this guide before generating configuration files
for this scenario.

## Service-Scoped Sub-Action Pruning (Blast Radius Control)

**CRITICAL: When the user mentions specific services, include ONLY the sub-actions
relevant to those services. Do NOT include the full 10 sub-actions by default.**

This prevents unintended impact on other business applications running in the same AZ.

### Pruning Rules

1. **User mentions specific services** → include ONLY sub-actions for those services
   plus the mandatory infrastructure sub-actions (Network Connectivity, ARC Zonal
   Autoshift). Remove all others.
2. **User says "all services" or does not specify** → include all 10 sub-actions
   (full AZ power interruption simulation).
3. **Always ask the user to confirm the final sub-action list** before generating files.

### Sub-Action to Service Mapping

| Sub-Action | Service Keyword(s) | Action ID |
|---|---|---|
| Stop-Instances | EC2, instance | `aws:ec2:stop-instances` |
| Stop-ASG-Instances | EC2, ASG, Auto Scaling | `aws:ec2:stop-instances` (ASG target) |
| Pause-ASG-Scaling | ASG, Auto Scaling | `aws:ec2:asg-insufficient-instance-capacity-error` |
| Pause-Network-Connectivity | Network, Subnet, VPC | `aws:network:disrupt-connectivity` |
| Failover-RDS | RDS, Aurora, database | `aws:rds:failover-db-cluster` |
| Pause-ElastiCache | ElastiCache, Redis, cache | `aws:elasticache:replicationgroup-interrupt-az-power` |
| Pause-EBS-IO | EBS, volume, disk | `aws:ebs:pause-volume-io` |
| Disrupt-S3-Express-One-Zone | S3, S3 Express | `aws:network:disrupt-connectivity` (S3 Express target) |
| Start-ARC-Zonal-Autoshift | ARC, Zonal Autoshift | `aws:arc:start-zonal-autoshift` |
| Pause-Instance-Launches | *(removed by default — see "Pause Instance Launches" section)* | `aws:ec2:api-insufficient-instance-capacity-error` |

### Dependency Rules Between Sub-Actions

Some sub-actions have implicit dependencies. When including a service, also include
its dependent sub-actions:

| If User Mentions | Must Also Include | Reason |
|---|---|---|
| EC2 instances (standalone) | Stop-Instances | Direct EC2 impact |
| EC2 instances (ASG-managed) | Stop-ASG-Instances + Pause-ASG-Scaling | Stop instances AND prevent ASG from replacing them in the impaired AZ |
| ASG / Auto Scaling | Stop-ASG-Instances + Pause-ASG-Scaling | Both are needed: stop existing + prevent new launches |
| RDS / Aurora | Failover-RDS | Direct RDS impact |
| ElastiCache / Redis | Pause-ElastiCache | Direct ElastiCache impact |
| EBS / volume | Pause-EBS-IO | Direct EBS impact |
| S3 Express | Disrupt-S3-Express-One-Zone + Pause-Network-Connectivity | S3 Express disruption requires subnet network disruption |
| Network / Subnet | Pause-Network-Connectivity | Direct network impact |

**Mandatory infrastructure sub-action** (always included unless user explicitly
excludes it):
- **Pause-Network-Connectivity** — simulates AZ-level network isolation; without it,
  resources in the impaired AZ can still communicate, which is unrealistic

**Conditional infrastructure sub-action** (include only when applicable):
- **Start-ARC-Zonal-Autoshift** — simulates AWS's automatic traffic shift response.
  **Only include if the user's environment has resources with zonal autoshift enabled
  (e.g., ALB, NLB with zonal autoshift configured).** If the user does not mention
  ARC or zonal autoshift, and the environment has no such resources, omit this action.

**Exception:** If the user explicitly says they only want to test a single service
(e.g., "only test RDS failover") and does NOT want network disruption, respect their
request and omit the infrastructure sub-actions. Confirm this with the user.

### Examples

| User Request | Included Sub-Actions | Excluded |
|---|---|---|
| "测试 AZ 断电对 RDS 的影响" | Failover-RDS, Pause-Network-Connectivity | EC2, ASG, ElastiCache, EBS, S3 Express, ARC Autoshift |
| "test AZ failure for EC2 and RDS" | Stop-Instances, Stop-ASG-Instances, Pause-ASG-Scaling, Failover-RDS, Pause-Network-Connectivity | ElastiCache, EBS, S3 Express, ARC Autoshift |
| "AZ 断电对 ElastiCache 的影响" | Pause-ElastiCache, Pause-Network-Connectivity | EC2, ASG, RDS, EBS, S3 Express, ARC Autoshift |
| "full AZ power interruption" | All 10 sub-actions (minus Pause-Instance-Launches per default) | None |
| "只测试 RDS 故障转移，不需要网络中断" | Failover-RDS | All others including network |

### Impact on Tagging, Permissions, and Dashboard

When sub-actions are pruned:
- **Tagging Lambda:** Only tag resources for the included sub-actions. Remove unused
  tag values from the Lambda parameters.
- **FIS Experiment Role:** Only attach managed policies for the included services.
  Remove inline permissions for excluded services.
- **CloudWatch Dashboard:** Only include metric widgets for the included services.
- **CFN template size:** Significantly smaller with fewer sub-actions.

## Default Experiment Duration

**Default duration: `PT10M` (10 minutes) for all sub-actions.**

Unless the user explicitly specifies a different duration, use `PT10M` as the default
for the overall experiment and all sub-actions. The original AWS documentation template
uses `PT30M` (30 minutes), but 10 minutes is sufficient for most validation scenarios
and reduces the blast radius window.

**Duration parameter locations:**
- Each sub-action's `parameters.duration` field
- ARC Zonal Autoshift's `startAfter` timing should scale proportionally:
  - At PT30M default: ARC starts at minute 5, runs for 25 minutes
  - At PT10M default: ARC starts at minute 2, runs for 8 minutes
  - Formula: `startAfter = duration × (5/30)`, rounded to nearest minute

If the user specifies a custom duration, apply it consistently to all sub-actions
and adjust ARC timing proportionally.

## Official Documentation (Required Reading)

Before generating any configuration files, you **MUST** call `aws___read_documentation`
to read the AZ Power Interruption scenario page and extract the JSON experiment template:

```
aws___read_documentation:
  url: https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-availability-scenario.html
  max_length: 30000
```

This page is the **authoritative source** for the correct multi-action template structure,
including all sub-actions, target definitions, parameter values, and action ordering.
Do NOT attempt to construct the experiment template from memory or from
`aws fis list-actions` alone.

**IMPORTANT:** The documentation template includes a `logConfiguration` field with only
`logSchemaVersion: 2` but no log destination. This is incomplete and will cause a CFN
error: `"Must specify at least one log destination in logConfiguration"`. **Remove the
entire `logConfiguration` field** from the experiment template when generating the CFN
template.

## Design Decision: One Stack Per AZ

AZ Power Interruption experiment templates have the **target AZ hardcoded** in multiple
locations — target filters (`Placement.AvailabilityZone`), action parameters
(`availabilityZoneIdentifiers`), and target parameters (`writerAvailabilityZoneIdentifiers`,
`availabilityZoneIdentifier`). Changing the target AZ requires recreating the experiment
template.

**Chosen approach:** Create one CFN Stack per AZ. To test a different AZ, delete the
current Stack and deploy a new one with the new AZ parameter. This is the simplest
approach — AZ failure experiments are not run frequently enough to justify maintaining
multiple templates simultaneously.

**Stack naming convention:** `fis-az-power-int-{AZ_SUFFIX}-{RANDOM_SUFFIX}`
- Example: `fis-az-power-int-2a-a3x7k2`, `fis-az-power-int-2b-b8y2m1`

## Resource Tagging Strategy

### Why Tags Are Needed

AZ Power Interruption uses **tag-based target selection** for resource types that do
not support `resourceArns` (ASG, ElastiCache) and optionally for others. Each sub-action
looks for a specific tag key/value pair on target resources.

### Tagging via CFN Custom Resource (Lambda)

Tags are applied by a **Lambda-backed Custom Resource within the same CFN Stack** as
the experiment template. This approach:

- Requires **zero additional permissions on the EC2 Instance Profile** — all tagging
  is done by the Lambda role, created through the CFN Service Role
- Ties tag lifecycle to the Stack — delete Stack removes tags automatically
- Is deployed in a single `aws cloudformation deploy` command

### Tag Key/Value Table

All sub-actions share the same tag key `AzImpairmentPower`. The value identifies which
sub-action targets the resource:

| Resource Type | Tag Value | Applied To |
|---|---|---|
| EC2 Instance (standalone) | `StopInstances` | Instances in target AZ |
| EC2 Instance (ASG-managed) | `IceAsg` | ASG instances in target AZ |
| Auto Scaling Group | `IceAsg` | ASGs with instances in target AZ |
| Subnet | `DisruptSubnet` | Subnets in target AZ |
| RDS Cluster | `DisruptRds` | Aurora clusters with writer in target AZ |
| ElastiCache Replication Group | `ElasticacheImpact` | Replication groups with nodes in target AZ |
| EBS Volume | `ApiPauseVolume` | Volumes attached to instances in target AZ (only volumes with `DeleteOnTermination: false`) |
| ARC Autoshift Resources | `RecoverAutoshiftResources` | Resources with zonal autoshift enabled |

### AZ Filtering Is Not Done by Tags

A critical design point: **tags do NOT distinguish AZ — the experiment template does.**

All three AZs' resources can carry the same tag values simultaneously. The experiment
template's internal AZ filters and parameters determine which resources are actually
affected:

| Target Type | AZ Selection Mechanism |
|---|---|
| EC2 Instance | `filters[].path: Placement.AvailabilityZone` |
| Subnet | `filters[].path: AvailabilityZone` |
| ASG | `parameters.availabilityZoneIdentifiers` in action |
| RDS Cluster | `parameters.writerAvailabilityZoneIdentifiers` in target |
| ElastiCache | `parameters.availabilityZoneIdentifier` in target |
| EBS Volume | `parameters.availabilityZoneIdentifier` in target + `filters[].path: Attachments.DeleteOnTermination` = `false` |

This means: if you later want to test a different AZ, **tags do not need updating** —
only the experiment template (i.e., the CFN Stack) needs to be recreated.

### ASG Tag Propagation

When tagging an ASG, set `PropagateAtLaunch: true`. This ensures:

- Existing instances launched by the ASG inherit the tag
- **New instances launched during or after the experiment** (e.g., ASG scaling in a
  healthy AZ to compensate for stopped instances) also get the tag automatically
- No need to track individual instance IDs

Since AZ filtering is done by the experiment template (not tags), ASG-launched instances
in healthy AZs will carry the tag but will **not** be affected by the experiment.

## FIS Experiment Role — Required Permissions

The FIS Experiment Role permissions are defined in the **Permissions** section of the
[AZ Power Interruption documentation](https://docs.aws.amazon.com/fis/latest/userguide/az-availability-scenario.html).
The agent MUST extract the full IAM policy JSON from that page (already required in
the Official Documentation step above).

To reduce policy size, use **AWS managed policies** for well-covered areas and an
**inline policy** for the remainder:

| Managed Policy | Covers |
|---|---|
| `AWSFaultInjectionSimulatorEC2Access` | Stop/Start instances, KMS grants for encrypted EBS, SSM commands |
| `AWSFaultInjectionSimulatorNetworkAccess` | Network ACL creation/deletion/replacement for connectivity disruption |
| `AWSFaultInjectionSimulatorRDSAccess` | RDS cluster failover, instance reboot, tag-based target resolution |

Permissions NOT covered by managed policies (ElastiCache, EBS pause-io, InjectApiError,
ASG describe, logs, tag resolution) must be added as an inline policy. Extract these
directly from the documentation's Permissions JSON — do NOT hardcode from this guide.

## Service-Linked Role

The ARC Zonal Autoshift recovery action requires the service-linked role
`AWSServiceRoleForZonalAutoshiftPracticeRun`. This role is **created automatically**
when an experiment template with the AZ Power Interruption scenario is created via
Console, CLI, or SDK. No manual creation is needed, but the CFN Service Role must have
`iam:CreateServiceLinkedRole` permission.

## Pause Instance Launches — Default: Remove

The `Pause-Instance-Launches` action (`aws:ec2:api-insufficient-instance-capacity-error`)
and its `IAM-role` target should be **removed from the experiment template by default**.

**Why:**
- This action targets IAM Roles that call `RunInstances`/`CreateFleet`/`StartInstances`
- FIS does **not** accept service-linked roles (e.g., `AWSServiceRoleForAutoScaling`) as
  targets — attempting to use one will fail
- An empty `resourceArns` array also fails CFN validation: `"You must specify resource
  ARNs, resource tags, or resource parameters for target IAM-role"`
- `Pause-ASG-Scaling` (`aws:ec2:asg-insufficient-instance-capacity-error`) already
  blocks ASG from launching instances in the target AZ at the ASG control plane level,
  so `Pause-Instance-Launches` is redundant for ASG-managed instances

**When to add it back:** Only if the user has **custom (non-service-linked) IAM Roles**
that call `RunInstances` outside of ASG — e.g., automation scripts, CI/CD pipelines,
Lambda functions. In that case, provide those Role ARNs in `resourceArns`.

## Limitations

| Limitation | Detail |
|---|---|
| No stop conditions by default | Scenario template has no built-in stop conditions — you MUST add CloudWatch Alarms |
| Fargate not supported | EKS Pods on Fargate and ECS Tasks on Fargate are not affected |
| RDS Multi-AZ with 2 readable standby not supported | Instances terminate but capacity re-provisions immediately in affected AZ |
| S3 Express One Zone | Only affects directory buckets co-located in the target AZ |
| EBS volume filter | Only targets volumes with `DeleteOnTermination: false` by default; selection mode is `COUNT(1)` (one volume) |

## Additional Sub-Action Details

### Disrupt S3 Express One Zone

This is a separate action using `aws:network:disrupt-connectivity` (same action ID as
Pause Network Connectivity but with different scope). It disrupts connectivity between
subnets and S3 Express One Zone directory buckets in the affected AZ. It reuses the
Subnet target with tag `AzImpairmentPower: DisruptSubnet` — no additional tagging is
needed beyond what Pause Network Connectivity requires.

### ARC Zonal Autoshift Timing

The `aws:arc:start-zonal-autoshift` action simulates real-world ARC behavior where
AWS detects the impairment and shifts traffic after the event.

**Timing scales proportionally with experiment duration:**

| Experiment Duration | ARC startAfter | ARC runs for |
|---|---|---|
| PT10M (default) | ~2 minutes | ~8 minutes |
| PT30M (AWS doc default) | ~5 minutes | ~25 minutes |
| Custom | duration × (5/30), rounded to nearest minute | remaining time |

**Only include this action if the user's environment has resources with zonal
autoshift enabled.** If omitted, the experiment still tests AZ failure impact
on the specified services — it just won't simulate the ARC traffic shift response.

## Custom Resource Lambda — Tagging Logic

The Lambda receives target resource identifiers as input parameters and applies
`AzImpairmentPower` tags. Key behaviors:

| Event Type | Action |
|---|---|
| Create | Apply tags to all specified resources |
| Update | Remove tags from old resources (via `OldResourceProperties`), apply to new |
| Delete | Remove all `AzImpairmentPower` tags from resources |

### cfn-response Callback (CRITICAL — prevents CFN hanging)

**The Lambda MUST send a cfn-response callback in ALL code paths (success AND
failure).** If the Lambda exits without sending a response, CloudFormation will
hang for up to 1 hour waiting for the callback, then fail with timeout.

Requirements:
1. **Lambda code MUST be inline using `ZipFile` property** in the CFN template.
   The `cfnresponse` module is **only available with `ZipFile` inline code** —
   it is NOT available for Lambda code stored in S3 buckets. If the code is in S3,
   you must manually send an HTTP PUT to the `ResponseURL`.
2. **Python import must be exactly `import cfnresponse`** — no other variant
   (e.g., `from cfnresponse import send`) works. CloudFormation only injects the
   module when it sees this exact import statement.
3. **Wrap ALL logic in try/except** — on ANY exception, send `cfnresponse.FAILED`
   with the error message, then return. If the exception is not caught, no response
   is sent and CFN hangs.
4. **Set Lambda Timeout to at least 60 seconds** (default 3s is too short for
   multiple API calls). In the CFN template: `Timeout: 60`
5. On success, send `cfnresponse.SUCCESS`

**Skeleton (Python, ZipFile inline):**
```python
import json
import boto3
import cfnresponse

def handler(event, context):
    try:
        # ... tagging logic ...
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        print(f"ERROR: {e}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Error": str(e)})
```

**Common causes of CFN Custom Resource hanging (1 hour timeout):**

| Cause | Symptom | Fix |
|---|---|---|
| Unhandled exception | Lambda logs show traceback, no cfn-response sent | Wrap ALL logic in try/except, always call cfnresponse.send |
| Lambda timeout too short | Logs show "Task timed out after 3.00 seconds" | Set `Timeout: 60` in CFN template |
| Code not inline (`ZipFile`) | `ModuleNotFoundError: No module named 'cfnresponse'` | Use `ZipFile` property for Lambda code, not S3 |
| Wrong import syntax | `ImportError` on `from cfnresponse import ...` | Use exactly `import cfnresponse` |
| Lambda in VPC without NAT | Lambda runs but cannot reach CFN callback URL | Do NOT place this Lambda in a VPC, or add NAT/VPC Endpoint |

### Resource Discovery

The Lambda receives explicit resource IDs/names as CFN parameters. It does NOT
auto-discover resources. The prepare skill's resource discovery step (Step 2 in
SKILL.md) identifies target resources and passes them as parameters.

### ASG Tagging (Two-Step — CRITICAL)

1. Tag the ASG itself via `autoscaling:CreateOrUpdateTags` with `PropagateAtLaunch: true`
   (ensures future instances also get tagged)
2. **Also tag existing EC2 instances in the ASG** — query instances via
   `autoscaling:DescribeAutoScalingGroups` to get current instance IDs, then apply
   the `AzImpairmentPower: IceAsg` tag directly via `ec2:CreateTags`. Without this
   step, Stop-ASG-Instances will be skipped because existing instances lack the
   required tag (`PropagateAtLaunch` only applies to newly launched instances).

Similarly, on Delete event, the Lambda must remove the tag from both the ASG and
its current instances.

**Lambda Role permissions** (minimum):

| Permission | Resource Scope |
|---|---|
| `ec2:CreateTags` / `ec2:DeleteTags` | `arn:aws:ec2:*:*:instance/*`, `arn:aws:ec2:*:*:subnet/*`, `arn:aws:ec2:*:*:volume/*` |
| `autoscaling:CreateOrUpdateTags` / `autoscaling:DeleteTags` | `*` |
| `autoscaling:DescribeAutoScalingGroups` | `*` |
| `rds:AddTagsToResource` / `rds:RemoveTagsFromResource` | `arn:aws:rds:*:*:cluster:*` |
| `elasticache:AddTagsToResource` / `elasticache:RemoveTagsFromResource` | `arn:aws:elasticache:*:*:replicationgroup:*` |

## Quick Reference: CFN Stack Contents

A complete AZ Power Interruption CFN Stack contains:

| Resource | Type | Purpose |
|---|---|---|
| FIS Experiment Role | `AWS::IAM::Role` | 3 managed policies + inline policy |
| FIS Experiment Template | `AWS::FIS::ExperimentTemplate` | The experiment definition |
| CloudWatch Dashboard | `AWS::CloudWatch::Dashboard` | Monitoring during experiment |
| Tagging Lambda Role | `AWS::IAM::Role` | Permissions for tagging resources |
| Tagging Lambda Function | `AWS::Lambda::Function` | Applies/removes resource tags |
| Tagging Custom Resource | `Custom::FISAZPowerTags` | Triggers Lambda on Stack lifecycle |
| CloudWatch Alarm (optional) | `AWS::CloudWatch::Alarm` | Stop condition, only if user requests |
