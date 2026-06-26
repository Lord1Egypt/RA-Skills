# Output Format Reference

Defines the directory layout and README.md template that this skill produces.
All placeholders use `{CURLY_BRACES}` notation.

## Contents

- Directory Layout
- Slug Naming Rules (scenario-slug, target-slug, context-slug)
- README.md Template

## Directory Layout

```
./{yyyy-mm-dd-HH-MM-SS}-{scenario-slug}-{target-slug}[-{context-slug}]-{TEMPLATE_ID}/
├── README.md
└── cfn-template.yaml
```

## Slug Naming Rules

**scenario-slug:**
- Look up the abbreviation table in `references/slug-conventions.md`.
- Lowercase, hyphens only, max 18 characters.
- Examples: `az-power-int`, `az-app-slow`, `rds-failover`, `ec2-cpu-stress`,
  `xaz-traffic-slow`, `pod-net-pktloss`.

**target-slug:**
- Primary target resource identifier (cluster name, instance ID, replication
  group ID, etc.).
- Lowercase, hyphens only, truncated to max 20 characters.
- Examples: `my-aurora-cluster`, `prod-redis-rg`, `i-0abc123def`.
- For AZ-level scenarios with multiple targets, use the most representative
  resource.

**context-slug (optional):**
- Downstream service or purpose that distinguishes experiments sharing the same
  scenario + target.
- Lowercase, hyphens only, truncated to max 10 characters.
- Applies to network fault-injection actions (latency, packet-loss,
  blackhole-port) to identify the downstream service (e.g., `redis`, `msk`,
  `dynamo`).
- Omit for non-directional actions (pod-delete, cpu-stress, memory-stress, etc.).

## README.md Template

**Key placeholders to replace after CFN deployment:**

| Placeholder | Meaning |
|---|---|
| `{STACK_NAME}` | Actual deployed CloudFormation stack name (e.g., `fis-az-power-int-my-cluster-a3x7k2`) |
| `{TEMPLATE_ID}` | FIS experiment template ID from stack outputs |
| `{DASHBOARD_URL}` | CloudWatch dashboard URL from stack outputs |

**IMPORTANT:** After successful CFN deployment, replace every `{STACK_NAME}`
placeholder with the real stack name. Do NOT leave generic placeholders in the
final output — users need the exact stack name for cleanup commands.

````markdown
# FIS Experiment: {Scenario Name}

**Directory:** {OUTPUT_DIR_FULL_PATH}
**Region:** {REGION}
**Target AZ:** {AZ_ID} (if applicable)
**Created:** {TIMESTAMP}
**CFN Stack:** {STACK_NAME}
**Estimated Duration:** {DURATION}

## Overview

{1-3 sentence description of what this experiment does}

## Affected Resources

| Resource Type | Identifier | Impact |
|---|---|---|
| {type} | {id/tag} | {what happens to it} |

## Files in This Directory

| File | Purpose |
|---|---|
| `cfn-template.yaml` | All-in-one CloudFormation template (IAM Role, FIS Template, Dashboard, Alarms) |

## How to Execute

**Note:** The CFN stack was already deployed by the prepare skill. Use the stack
outputs directly.

```bash
# Stack name (already deployed by prepare skill):
# {STACK_NAME}

# If you need to redeploy:
aws cloudformation deploy \
  --template-file cfn-template.yaml \
  --stack-name {STACK_NAME} \
  --capabilities CAPABILITY_NAMED_IAM \
  --region {REGION} \
  ${CFN_ROLE_ARN:+--role-arn ${CFN_ROLE_ARN}}

# After stack creation, start the experiment:
TEMPLATE_ID=$(aws cloudformation describe-stacks \
  --stack-name {STACK_NAME} \
  --query 'Stacks[0].Outputs[?OutputKey==`ExperimentTemplateId`].OutputValue' \
  --output text --region {REGION})

aws fis start-experiment \
  --experiment-template-id $TEMPLATE_ID \
  --region {REGION}
```

## Monitoring During Experiment

- **CloudWatch Dashboard:** View the dashboard deployed by the CFN stack in the
  CloudWatch console.
- **Experiment Status:**
  `aws fis get-experiment --id {EXPERIMENT_ID} --region {REGION}`

## Cleanup

```bash
# Delete the entire stack (removes IAM role, alarms, dashboard, and all other resources):
aws cloudformation delete-stack --stack-name {STACK_NAME} --region {REGION} \
  ${CFN_ROLE_ARN:+--role-arn ${CFN_ROLE_ARN}}

# Wait for deletion to complete:
aws cloudformation wait stack-delete-complete --stack-name {STACK_NAME} --region {REGION}
```

## CFN Deployment Status

- **Stack Name:** {STACK_NAME}
- **Status:** {DEPLOYMENT_STATUS}
- **Experiment Template ID:** {TEMPLATE_ID}
- **CloudWatch Dashboard URL:** {DASHBOARD_URL}

## Next Step

To start the experiment:
- Use aws-fis-experiment-execute skill, OR
- Manually: `aws fis start-experiment --experiment-template-id {TEMPLATE_ID} --region {REGION}`
````
