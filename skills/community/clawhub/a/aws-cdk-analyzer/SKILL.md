---
name: aws-cdk-analyzer
description: Analyze AWS CDK applications for best practices, security, cost optimization, and deployment safety — covers construct patterns, IAM policies, and CloudFormation output.
metadata:
  tags: ["aws", "cdk", "infrastructure", "cloud", "security", "iac"]
---

# AWS CDK Analyzer

Analyze AWS CDK applications for best practices, security vulnerabilities, cost optimization, and deployment safety. Reviews construct patterns, IAM policies, resource configurations, and synthesized CloudFormation output. Use when reviewing CDK code, preparing for production deployments, or auditing existing infrastructure.

## Usage

```
"Analyze my CDK app for security issues"
"Review the IAM policies in my CDK stacks"
"Check my CDK code for cost optimization opportunities"
"Audit the CDK constructs for best practices"
"Verify deployment safety for this CDK change"
```

## How It Works

### 1. Project Discovery

Map the CDK application structure:

```bash
# Detect CDK version and language
cat package.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for key in ['aws-cdk-lib', 'aws-cdk', '@aws-cdk/core']:
    ver = d.get('dependencies', {}).get(key) or d.get('devDependencies', {}).get(key)
    if ver: print(f'CDK: {key}@{ver}')
"

# Find all stack definitions
grep -rn "extends Stack\|new Stack\|class.*Stack" lib/ bin/ src/ 2>/dev/null
# Find all construct files
find lib/ src/ -name "*.ts" -o -name "*.py" | head -30
```

### 2. Security Audit

**IAM Policy Analysis:**
- Detect wildcard permissions (`*` actions or resources)
- Find overly permissive policies (AdministratorAccess, PowerUserAccess)
- Check for missing condition keys on sensitive actions
- Verify least-privilege principle
- Identify cross-account access without proper trust boundaries

**Network Security:**
- Security groups with `0.0.0.0/0` ingress on sensitive ports
- Public subnets for resources that should be private
- Missing VPC endpoints for AWS services
- Unencrypted data in transit (HTTP listeners, unencrypted connections)

**Data Protection:**
- S3 buckets without encryption, versioning, or access logging
- RDS instances without encryption at rest
- DynamoDB tables without point-in-time recovery
- Missing KMS key rotation
- Secrets hardcoded in CDK code instead of using Secrets Manager

**Compliance:**
- CloudTrail logging enabled
- VPC Flow Logs configured
- Config rules for compliance monitoring
- Backup plans for critical resources

### 3. Cost Analysis

- Oversized instances (can downsize based on typical patterns)
- Missing auto-scaling configurations
- On-Demand instances that could use Reserved/Spot
- NAT Gateway costs (consider VPC endpoints instead)
- Unused Elastic IPs
- CloudWatch log retention too long
- Missing S3 lifecycle policies

### 4. Best Practices

**Construct patterns:**
- L1 constructs (CfnXxx) used where L2/L3 exists — prefer higher-level
- Missing removal policies on stateful resources (RDS, S3, DynamoDB)
- Using default construct IDs that generate poor CloudFormation logical IDs
- Stack dependencies and cross-stack references
- Proper use of aspects for cross-cutting concerns

**Code quality:**
- Hardcoded values that should be parameters or context
- Missing stack tags for cost allocation
- Environment-specific config not separated from construct logic
- Missing stack descriptions
- Construct scope and naming conventions

**Deployment safety:**
- Resources that would be replaced on update (data loss risk)
- Missing stack policies to prevent accidental deletion
- No rollback configuration
- Insufficient CloudFormation change set review

### 5. Synthesize & Verify

```bash
# Synth and check output
npx cdk synth --quiet 2>&1
# Check for drift
npx cdk diff 2>&1
# Verify no sensitive data in CloudFormation template
grep -i "password\|secret\|key\|token" cdk.out/*.template.json
```

### 6. Migration Recommendations

- CDK v1 to v2 migration paths
- Feature flag recommendations
- Construct library updates
- Breaking change detection

## Output

```
## AWS CDK Analysis — MyApp (3 stacks)

### 🔴 Critical (4)
1. **Wildcard IAM permission** — lib/api-stack.ts:45
   `PolicyStatement({ actions: ['s3:*'], resources: ['*'] })`
   → Scope to specific bucket ARN and required actions only

2. **Public RDS instance** — lib/database-stack.ts:23
   `publiclyAccessible: true` on production database
   → Move to private subnet, access via bastion or VPN

3. **Hardcoded secret** — lib/api-stack.ts:78
   Database password in CDK code: `password: 'prod_db_pass123'`
   → Use `secretsmanager.Secret.fromSecretNameV2()`

4. **No removal policy on S3 bucket** — lib/storage-stack.ts:15
   Default DESTROY policy will delete all data on stack deletion
   → Add `removalPolicy: RemovalPolicy.RETAIN`

### 🟡 Warnings (6)
5. **Oversized Lambda** — 1024MB allocated, avg usage 128MB
6. **NAT Gateway** — $32/mo, could use VPC endpoints ($7/mo)
7. **CloudWatch logs** — no retention set (infinite, $0.50/GB/mo)
8. **Missing tags** — 3 stacks without cost allocation tags
9. **L1 construct used** — CfnBucket where s3.Bucket available
10. **No auto-scaling** — ECS service with fixed task count

### 💰 Cost Optimization
| Resource | Current | Optimized | Monthly Savings |
|----------|---------|-----------|-----------------|
| NAT Gateway | $32 | VPC Endpoints $7 | $25 |
| Lambda memory | 1024MB | 256MB | ~$8 |
| CW Logs retention | ∞ | 30 days | ~$15 |
| RDS instance | db.r5.xlarge | db.r5.large | $180 |
| **Total** | | | **~$228/mo** |

### ✅ Good Practices
- Proper stack separation (API, Database, Storage)
- VPC with proper subnet tiers
- CloudFront distribution with WAF
- Parameter Store for non-secret config
```
