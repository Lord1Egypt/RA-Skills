---
name: aws-health
description: Check health of AWS EC2 instances and ECS clusters/services. Reports running/stopped counts, CPU/memory metrics, and unhealthy tasks. Use when the user asks about AWS instance health, ECS status, or infra monitoring.
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: AWS_ACCESS_KEY_ID
    requires:
      env:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION
      bins:
        - node
    install:
      - kind: node
        package: tsx
        bins: [tsx]
    envVars:
      - name: AWS_ACCESS_KEY_ID
        required: true
        description: AWS access key with read-only EC2/ECS/CloudWatch permissions.
      - name: AWS_SECRET_ACCESS_KEY
        required: true
        description: AWS secret access key.
      - name: AWS_REGION
        required: true
        description: AWS region to query (e.g. ap-south-1).
      - name: AWS_SESSION_TOKEN
        required: false
        description: Optional session token for temporary credentials (assumed roles).
---

# AWS Health Skill

Use this skill when the user asks any of the following:
- "What's the health of my AWS instances?"
- "How are my ECS services doing?"
- "Are all my EC2 instances running?"
- "Show me AWS status" / "Check my infra"
- "Any unhealthy tasks in ECS?"
- "What's the CPU on my instances?"

## How to invoke

Run the health check script using the `exec` tool:

```bash
cd {baseDir} && npx tsx scripts/aws-health.ts
```

To check only EC2:
```bash
cd {baseDir} && npx tsx scripts/aws-health.ts --only ec2
```

To check only ECS:
```bash
cd {baseDir} && npx tsx scripts/aws-health.ts --only ecs
```

To check a specific ECS cluster:
```bash
cd {baseDir} && npx tsx scripts/aws-health.ts --only ecs --cluster my-cluster-name
```

## Output format

The script prints a structured health report. Present it to the user as-is — it is already formatted for chat readability. If any service is UNHEALTHY or STOPPED unexpectedly, highlight that clearly to the user and suggest next steps (check logs, restart task, etc).

## Error handling

- `CredentialsProviderError`: env vars are missing or wrong — tell user to check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
- `AccessDeniedException`: the IAM user lacks permissions — tell user to attach the `ReadOnlyAccess` or custom policy (see README.md).
- `ResourceNotFoundException`: the cluster name doesn't exist — ask user to confirm cluster name.
- Network timeout: likely a VPC/firewall issue if running self-hosted — suggest checking connectivity.
