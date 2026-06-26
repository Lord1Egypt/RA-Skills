---
name: cloud-tagging-enforcer
description: Enforce cloud resource tagging policies for cost allocation, compliance, and governance across AWS/GCP/Azure
---

# Cloud Tagging Enforcer

Scan cloud infrastructure for missing, incorrect, or non-compliant resource tags. This skill teaches an AI agent to audit tagging across AWS, GCP, and Azure, define and validate tagging schemas, generate compliance reports, and produce remediation scripts that bring resources into policy compliance.

Use when: "check cloud tags", "untagged resources", "tagging policy", "cost allocation tags", "tag compliance", "enforce tags", "missing tags", "tag governance", "remediate tags"

## Commands

### 1. `scan` -- Find untagged or non-compliant resources

Discover all resources that violate the tagging policy by having missing, empty, or incorrectly formatted tags.

#### Step 1: Define the expected tagging schema

Before scanning, establish what "compliant" means. Load the policy or define defaults.

```bash
# Check if a tagging policy file exists in the repo
rg -l "tagging.policy|tag.schema|required.tags" . -g '*.{json,yaml,yml,toml}'

# If no policy exists, use a sensible default for cost allocation and governance
cat <<'POLICY'
required_tags:
  - key: "Environment"
    allowed_values: ["production", "staging", "development", "sandbox"]
  - key: "Owner"
    pattern: "^[a-z]+@[a-z]+\\.[a-z]+$"
  - key: "Team"
    allowed_values: []  # any non-empty value
  - key: "CostCenter"
    pattern: "^CC-[0-9]{4}$"
  - key: "Project"
    allowed_values: []  # any non-empty value
  - key: "ManagedBy"
    allowed_values: ["terraform", "cloudformation", "pulumi", "manual"]
POLICY
```

#### Step 2: Scan AWS resources

```bash
# AWS: Find all resources missing required tags using Resource Groups Tagging API
# This is the most efficient API -- covers 50+ resource types in one call
aws resourcegroupstaggingapi get-resources \
  --no-paginate \
  --output json | python3 -c "
import sys, json

required_keys = ['Environment', 'Owner', 'Team', 'CostCenter', 'Project']
data = json.load(sys.stdin)
violations = []

for resource in data.get('ResourceTagMappingList', []):
    arn = resource['ResourceARN']
    tags = {t['Key']: t['Value'] for t in resource.get('Tags', [])}
    missing = [k for k in required_keys if k not in tags]
    empty = [k for k in required_keys if k in tags and not tags[k].strip()]

    if missing or empty:
        violations.append({
            'arn': arn,
            'missing_tags': missing,
            'empty_tags': empty,
            'existing_tags': tags
        })

print(f'Total resources scanned: {len(data.get(\"ResourceTagMappingList\", []))}')
print(f'Non-compliant resources: {len(violations)}')
print()
for v in violations[:20]:
    svc = v['arn'].split(':')[2]
    print(f'  {svc}: {v[\"arn\"]}')
    if v['missing_tags']:
        print(f'    MISSING: {v[\"missing_tags\"]}')
    if v['empty_tags']:
        print(f'    EMPTY:   {v[\"empty_tags\"]}')
    print()
if len(violations) > 20:
    print(f'  ... and {len(violations) - 20} more')
"

# AWS: Find EC2 instances specifically without the Environment tag
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[?!not_null(Tags[?Key==`Environment`].Value | [0])].{ID:InstanceId,Name:Tags[?Key==`Name`]|[0].Value,Type:InstanceType}' \
  --output table

# AWS: Find untagged S3 buckets
for bucket in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  tags=$(aws s3api get-bucket-tagging --bucket "$bucket" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
keys = [t['Key'] for t in data.get('TagSet', [])]
print(','.join(keys))
" 2>/dev/null)
  if [ -z "$tags" ]; then
    echo "UNTAGGED: s3://$bucket"
  fi
done
```

#### Step 3: Scan GCP resources

```bash
# GCP: Find instances without required labels
gcloud compute instances list --format=json | python3 -c "
import sys, json

required_labels = ['environment', 'owner', 'team', 'cost-center', 'project']
instances = json.load(sys.stdin)
for inst in instances:
    labels = inst.get('labels', {})
    missing = [l for l in required_labels if l not in labels]
    if missing:
        zone = inst['zone'].split('/')[-1]
        print(f'NON-COMPLIANT: {inst[\"name\"]} ({zone})')
        print(f'  Missing labels: {missing}')
"

# GCP: Scan all project resources using Cloud Asset Inventory
gcloud asset search-all-resources \
  --scope="projects/$GCP_PROJECT" \
  --query="NOT labels:environment" \
  --format="table(name.basename(), assetType, labels)"
```

#### Step 4: Scan Azure resources

```bash
# Azure: Find resources without required tags
az resource list --query "[?tags.Environment==null || tags.Owner==null].{Name:name,Type:type,RG:resourceGroup,Tags:tags}" --output table

# Azure: Get a compliance percentage by resource group
az resource list --output json | python3 -c "
import sys, json
from collections import defaultdict

required = ['Environment', 'Owner', 'Team', 'CostCenter']
resources = json.load(sys.stdin)
rg_stats = defaultdict(lambda: {'total': 0, 'compliant': 0})

for r in resources:
    rg = r.get('resourceGroup', 'unknown')
    tags = r.get('tags') or {}
    rg_stats[rg]['total'] += 1
    missing = [k for k in required if k not in tags]
    if not missing:
        rg_stats[rg]['compliant'] += 1

for rg, stats in sorted(rg_stats.items()):
    pct = (stats['compliant'] / stats['total'] * 100) if stats['total'] > 0 else 0
    status = 'PASS' if pct == 100 else 'FAIL'
    print(f'{rg:<30} {stats[\"total\"]:>6} {stats[\"compliant\"]:>10} {pct:>6.1f}% {status}')
"
```

#### Report template

```
## Cloud Tagging Compliance Report

**Date:** YYYY-MM-DD
**Cloud:** AWS / GCP / Azure
**Account/Project:** account-id / project-name
**Policy:** 5 required tags (Environment, Owner, Team, CostCenter, Project)

### Summary
- Total resources scanned: 847
- Fully compliant: 612 (72.3%)
- Non-compliant: 235 (27.7%)
- Completely untagged: 43 (5.1%)

### Non-compliance by service
- EC2 instances: 23 / 89 non-compliant (25.8%)
- S3 buckets: 8 / 34 non-compliant (23.5%)
- RDS instances: 2 / 12 non-compliant (16.7%)
- Lambda functions: 45 / 120 non-compliant (37.5%)

### Most common missing tags
1. CostCenter -- missing on 180 resources
2. Owner -- missing on 95 resources
3. Team -- missing on 67 resources

### Estimated unattributable monthly cost
- Resources without CostCenter: $12,400/mo
- Resources without Owner: $8,200/mo (overlap with above)
```

---

### 2. `policy` -- Define and validate a tagging schema

Create a formal tagging policy document and validate existing tags against it.

#### Step 1: Generate a tagging policy from current usage

```bash
# Discover all tag keys currently in use (AWS)
aws resourcegroupstaggingapi get-tag-keys --output json | python3 -c "
import sys, json
data = json.load(sys.stdin)
keys = sorted(data.get('TagKeys', []))
print(f'Found {len(keys)} unique tag keys:')
for k in keys:
    print(f'  - {k}')
"

# Discover tag value patterns for each key
for key in Environment Owner Team CostCenter; do
  echo "=== $key ==="
  aws resourcegroupstaggingapi get-tag-values --key "$key" --output text | sort | uniq -c | sort -rn | head -10
done
```

#### Step 2: Detect tag value drift and inconsistencies

Tag drift is when the same concept has multiple spellings: "prod" vs "production" vs "Production". This silently breaks cost allocation and IAM policies.

```bash
aws resourcegroupstaggingapi get-tag-values --key "Environment" --output json | python3 -c "
import sys, json

data = json.load(sys.stdin)
values = data.get('TagValues', [])
normalized = {}
for v in values:
    norm = v.lower().strip().replace('-', '').replace('_', '')
    if norm not in normalized:
        normalized[norm] = []
    normalized[norm].append(v)

print('Tag value inconsistencies for Environment:')
for norm, variants in normalized.items():
    if len(variants) > 1:
        print(f'  DRIFT: {variants} -- standardize to one value')
    else:
        print(f'  OK:    {variants[0]}')
"
```

#### Step 3: Generate preventive enforcement policies

Preventive controls stop non-compliant resources from being created. This is stronger than detective controls (scanning after the fact).

```python
# Generate an AWS SCP that denies resource creation without required tags
import json

scp = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyEC2WithoutRequiredTags",
            "Effect": "Deny",
            "Action": ["ec2:RunInstances"],
            "Resource": ["arn:aws:ec2:*:*:instance/*", "arn:aws:ec2:*:*:volume/*"],
            "Condition": {
                "Null": {
                    "aws:RequestTag/Environment": "true",
                    "aws:RequestTag/Owner": "true",
                    "aws:RequestTag/Team": "true"
                }
            }
        },
        {
            "Sid": "DenyRDSWithoutRequiredTags",
            "Effect": "Deny",
            "Action": ["rds:CreateDBInstance", "rds:CreateDBCluster"],
            "Resource": ["*"],
            "Condition": {
                "Null": {
                    "aws:RequestTag/Environment": "true",
                    "aws:RequestTag/Owner": "true"
                }
            }
        },
        {
            "Sid": "DenyS3WithoutRequiredTags",
            "Effect": "Deny",
            "Action": ["s3:CreateBucket"],
            "Resource": ["*"],
            "Condition": {
                "Null": {
                    "aws:RequestTag/Environment": "true",
                    "aws:RequestTag/Owner": "true"
                }
            }
        }
    ]
}
print(json.dumps(scp, indent=2))
```

```bash
# Generate a Terraform default_tags block for the AWS provider
cat <<'TF'
provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      Owner       = var.team_email
      Team        = var.team_name
      CostCenter  = var.cost_center
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}
TF
```

#### Step 4: Validate tag values against the schema

```python
import re, json

schema = {
    "Environment": {"allowed": ["production", "staging", "development", "sandbox"]},
    "Owner": {"pattern": r"^[a-z.]+@[a-z]+\.[a-z]+$"},
    "Team": {"required": True},  # any non-empty value
    "CostCenter": {"pattern": r"^CC-[0-9]{4}$"},
    "Project": {"required": True},
}

def validate_tags(tags: dict, schema: dict) -> list:
    """Return list of violations for a set of tags."""
    violations = []
    for key, rules in schema.items():
        value = tags.get(key, "")
        if not value:
            violations.append(f"MISSING: {key}")
            continue
        if "allowed" in rules and value not in rules["allowed"]:
            violations.append(f"INVALID VALUE: {key}={value} (allowed: {rules['allowed']})")
        if "pattern" in rules and not re.match(rules["pattern"], value):
            violations.append(f"BAD FORMAT: {key}={value} (expected: {rules['pattern']})")
    return violations

# Example usage
test_tags = {"Environment": "prod", "Owner": "jdoe", "CostCenter": "1234"}
for v in validate_tags(test_tags, schema):
    print(f"  {v}")
# Output:
#   INVALID VALUE: Environment=prod (allowed: ['production', ...])
#   BAD FORMAT: Owner=jdoe (expected: ^[a-z.]+@[a-z]+\.[a-z]+$)
#   BAD FORMAT: CostCenter=1234 (expected: ^CC-[0-9]{4}$)
#   MISSING: Team
#   MISSING: Project
```

#### Report template

```
## Tagging Policy Definition

### Required Tags (all resources)
| Tag Key | Allowed Values | Pattern | Purpose |
|---------|----------------|---------|---------|
| Environment | production, staging, development, sandbox | - | Cost allocation, access control |
| Owner | - | email format | Accountability |
| Team | any non-empty | - | Org mapping |
| CostCenter | - | CC-NNNN | Finance allocation |
| Project | any non-empty | - | Project tracking |

### Enforcement Mechanisms
- **Preventive:** SCP denies resource creation without required tags
- **Detective:** Daily scan via this skill, alerts to Slack/PagerDuty
- **Corrective:** Auto-remediation scripts apply placeholder values

### Tag Value Drift Detected
- Environment: "prod" vs "production" (12 resources affected)
- Team: "Platform" vs "platform-team" (8 resources affected)
```

---

### 3. `enforce` -- Generate remediation scripts

Produce executable scripts that add missing tags to non-compliant resources.

#### Step 1: Generate AWS bulk remediation

```bash
# Generate a remediation script for all non-compliant resources
aws resourcegroupstaggingapi get-resources --no-paginate --output json | python3 -c "
import sys, json

required = {
    'Environment': 'NEEDS-CLASSIFICATION',
    'Owner': 'NEEDS-OWNER',
    'Team': 'NEEDS-TEAM',
    'CostCenter': 'CC-0000',
    'Project': 'NEEDS-PROJECT'
}
data = json.load(sys.stdin)
commands = []

for resource in data.get('ResourceTagMappingList', []):
    arn = resource['ResourceARN']
    tags = {t['Key']: t['Value'] for t in resource.get('Tags', [])}
    missing = {k: v for k, v in required.items() if k not in tags}

    if missing:
        tags_json = json.dumps(missing)
        commands.append(f'aws resourcegroupstaggingapi tag-resources --resource-arn-list \"{arn}\" --tags \'{tags_json}\'')

print('#!/bin/bash')
print('# Auto-generated tagging remediation script')
print(f'# {len(commands)} resources to remediate')
print('# Review before running -- placeholder values (NEEDS-*) must be replaced by owners')
print('set -euo pipefail')
print()
for i, cmd in enumerate(commands):
    print(f'echo \"[{i+1}/{len(commands)}] Tagging resource...\"')
    print(cmd)
    print('sleep 0.2  # rate limiting')
    print()
"
```

#### Step 2: Generate Terraform tag fixes

For resources managed by Terraform, fix the source of truth rather than patching live.

```bash
# Find Terraform resource blocks missing tags
rg -l 'resource "aws_' . -g '*.tf' | while read tf_file; do
  python3 -c "
import re

with open('$tf_file') as f:
    content = f.read()

blocks = re.finditer(r'resource\s+\"(aws_\w+)\"\s+\"(\w+)\"\s*\{', content)
for match in blocks:
    rtype, rname = match.group(1), match.group(2)
    # Find the block end by counting braces
    start = match.end()
    depth = 1
    pos = start
    while depth > 0 and pos < len(content):
        if content[pos] == '{': depth += 1
        elif content[pos] == '}': depth -= 1
        pos += 1
    block = content[start:pos]
    if 'tags' not in block:
        print(f'MISSING tags in $tf_file: {rtype}.{rname}')
"
done
```

#### Step 3: Generate GCP label remediation

```bash
# GCP: Produce gcloud commands to set missing labels
gcloud compute instances list --format=json | python3 -c "
import sys, json

required = {'environment': 'needs-classification', 'owner': 'needs-owner', 'team': 'needs-team', 'cost-center': 'cc-0000'}
instances = json.load(sys.stdin)

print('#!/bin/bash')
print('# GCP label remediation script')
print('set -euo pipefail')
for inst in instances:
    labels = inst.get('labels', {})
    missing = {k: v for k, v in required.items() if k not in labels}
    if missing:
        zone = inst['zone'].split('/')[-1]
        label_str = ','.join(f'{k}={v}' for k, v in missing.items())
        print(f'gcloud compute instances update {inst[\"name\"]} --zone={zone} --update-labels={label_str}')
"
```

#### Step 4: Dry-run validation

Always validate before applying. Compare pre- and post-remediation compliance.

```bash
# Pre-remediation compliance count
echo "=== Pre-remediation compliance ==="
aws resourcegroupstaggingapi get-resources --no-paginate --output json | python3 -c "
import sys, json
required_keys = ['Environment', 'Owner', 'Team', 'CostCenter', 'Project']
data = json.load(sys.stdin)
total = len(data.get('ResourceTagMappingList', []))
compliant = sum(1 for r in data.get('ResourceTagMappingList', [])
                if all(k in {t['Key'] for t in r.get('Tags', [])} for k in required_keys))
print(f'Total: {total}, Compliant: {compliant} ({compliant/total*100:.1f}%)')
print(f'Non-compliant: {total - compliant} ({(total-compliant)/total*100:.1f}%)')
"

# After remediation, re-run the same check to confirm improvement
```

#### Report template

```
## Tagging Remediation Report

**Date:** YYYY-MM-DD
**Scope:** AWS account 123456789012
**Mode:** Dry run / Applied

### Remediation Summary
- Resources targeted: 235
- Tags added: 580 (across 5 required keys)
- Resources now compliant: 235 / 235

### Remediation breakdown
| Tag Key | Resources Fixed | Default Value Applied |
|---------|----------------|----------------------|
| Environment | 45 | NEEDS-CLASSIFICATION |
| Owner | 95 | NEEDS-OWNER |
| Team | 67 | NEEDS-TEAM |
| CostCenter | 180 | CC-0000 |
| Project | 193 | NEEDS-PROJECT |

### Next steps
1. Resource owners must replace placeholder values (NEEDS-*) within 7 days
2. SCP enforcement activates in 14 days -- non-compliant creates will be denied
3. Re-scan scheduled for YYYY-MM-DD to verify owner updates
4. Escalate any resources still carrying NEEDS-* after deadline
```
