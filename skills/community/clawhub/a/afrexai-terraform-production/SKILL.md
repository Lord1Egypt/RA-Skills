---
name: Terraform & Infrastructure as Code Production Engineering
description: Complete Terraform & IaC production methodology — project structure, module design, state management, multi-environment deployment, security hardening, testing, CI/CD pipelines, cost optimization, and drift management. Use when designing infrastructure, writing Terraform, reviewing IaC, or managing cloud environments.
---

# Terraform & Infrastructure as Code Production Engineering

Complete 14-phase system for production-grade infrastructure as code. Zero dependencies — works with any cloud provider and any Terraform version.

---

## Phase 1: Quick Health Check

Run this 8-signal triage on any Terraform project:

| # | Signal | ✅ Healthy | 🔴 Fix Now |
|---|--------|-----------|-----------|
| 1 | Remote state backend | S3/GCS/Azure Blob with locking | Local state or no locking |
| 2 | State encryption | Encrypted at rest + restricted access | Plain state, wide access |
| 3 | Module pinning | All modules version-pinned | Unpinned or `ref=main` |
| 4 | Provider pinning | `required_providers` with `~>` constraints | No version constraints |
| 5 | Separate environments | Isolated state per env (dev/staging/prod) | Shared state or workspaces-as-envs |
| 6 | Plan before apply | CI runs `plan`, human approves, CI runs `apply` | Local `apply` without review |
| 7 | Secrets management | No secrets in `.tf` files; vault/SSM/secrets manager | Hardcoded secrets anywhere |
| 8 | Drift detection | Scheduled drift checks (weekly minimum) | No drift monitoring |

**Score: /16** (2 per signal). Below 10 = stop and fix foundations first.

---

## Phase 2: Project Structure

### Recommended Layout

```
infrastructure/
├── modules/                    # Reusable modules (internal registry)
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   └── README.md
│   ├── compute/
│   ├── database/
│   └── monitoring/
├── environments/               # Environment-specific configs
│   ├── dev/
│   │   ├── main.tf            # Module calls with dev params
│   │   ├── backend.tf         # Dev state backend
│   │   ├── terraform.tfvars   # Dev variable values
│   │   └── versions.tf
│   ├── staging/
│   └── prod/
├── global/                     # Shared resources (IAM, DNS, etc.)
│   ├── iam/
│   ├── dns/
│   └── networking/
├── scripts/                    # Helper scripts (import, migration)
├── policies/                   # OPA/Sentinel policies
└── .github/workflows/          # CI/CD pipelines
```

### 7 Architecture Rules

1. **One module = one responsibility** — networking module doesn't create compute
2. **Environments are thin** — they call modules with different parameters, not duplicate code
3. **State isolation** — separate state file per environment AND per logical group (networking vs compute)
4. **No hardcoded values in modules** — everything is a variable with sensible defaults
5. **Outputs are your API** — if another module/team needs a value, it's an output
6. **README per module** — inputs, outputs, usage example, dependencies
7. **`.terraform.lock.hcl` committed** — reproducible provider versions

### File Naming Convention

| File | Purpose |
|------|---------|
| `main.tf` | Primary resource definitions |
| `variables.tf` | All input variables |
| `outputs.tf` | All outputs |
| `versions.tf` | `terraform` and `required_providers` blocks |
| `backend.tf` | State backend configuration |
| `locals.tf` | Local values and computed expressions |
| `data.tf` | Data sources |
| `providers.tf` | Provider configuration (if complex) |

---

## Phase 3: State Management

### Remote Backend Setup (AWS Example)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "environments/prod/networking/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    kms_key_id     = "alias/terraform-state"
  }
}
```

### State Key Strategy

```
{org}/{environment}/{component}/terraform.tfstate
```

Examples:
- `acme/prod/networking/terraform.tfstate`
- `acme/prod/compute/terraform.tfstate`
- `acme/global/iam/terraform.tfstate`

### State Operations Safety Rules

| Operation | Risk | Safe Approach |
|-----------|------|---------------|
| `terraform state mv` | Medium | Plan after to verify no changes |
| `terraform state rm` | High | Only to adopt resource elsewhere |
| `terraform import` | Medium | Write config first, import, plan to verify |
| `terraform state pull` | Low | For inspection only |
| `terraform state push` | CRITICAL | Almost never — breaks consistency |
| `moved` block | Low | Preferred over `state mv` — in config, reviewable |

### 6 State Rules

1. **Never edit state JSON manually** — use CLI commands only
2. **Never share state across environments** — separate backends per env
3. **Always enable locking** — DynamoDB (AWS), Cloud Storage (GCP), Blob lease (Azure)
4. **Enable versioning on state bucket** — rollback capability
5. **Restrict state access** — only CI/CD service accounts, not developers
6. **State contains secrets** — treat state files as sensitive; encrypt at rest + in transit

---

## Phase 4: Module Design

### Module Interface Template

```hcl
# variables.tf — Module inputs
variable "name" {
  description = "Name prefix for all resources"
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,28}[a-z0-9]$", var.name))
    error_message = "Name must be 4-30 chars, lowercase alphanumeric + hyphens."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "tags" {
  description = "Common tags applied to all resources"
  type        = map(string)
  default     = {}
}
```

```hcl
# outputs.tf — Module contract
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}
```

### Module Composition Pattern

```hcl
# environments/prod/main.tf
module "networking" {
  source      = "../../modules/networking"
  name        = "prod"
  environment = "prod"
  vpc_cidr    = "10.0.0.0/16"
  azs         = ["us-east-1a", "us-east-1b", "us-east-1c"]
  tags        = local.common_tags
}

module "compute" {
  source             = "../../modules/compute"
  name               = "prod"
  environment        = "prod"
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  instance_type      = "t3.large"
  min_size           = 3
  max_size           = 10
  tags               = local.common_tags
}
```

### 8 Module Design Rules

1. **Expose what's needed, hide what's not** — minimal variable surface
2. **Use `for_each` over `count`** — stable resource addressing
3. **Validate inputs** — `validation` blocks catch errors at plan time
4. **Default to secure** — encryption on, public access off, least privilege
5. **Version everything** — semver for modules, `~>` for providers
6. **No provider config in modules** — providers configured in root only
7. **Use `moved` blocks for refactoring** — not `state mv`
8. **Test with examples** — `examples/` directory with working configurations

---

## Phase 5: Multi-Environment Strategy

### Environment Comparison

| Aspect | Dev | Staging | Prod |
|--------|-----|---------|------|
| Instance sizes | Small/micro | Match prod types | Right-sized |
| Replica count | 1 | 2 | 3+ (HA) |
| Multi-AZ | Optional | Yes | Yes |
| Backup retention | 1 day | 7 days | 30+ days |
| Monitoring | Basic | Full | Full + PagerDuty |
| Auto-scaling | Off | On | On |
| WAF/Shield | Off | On | On + Advanced |
| State access | Dev team | DevOps | DevOps only |

### Variable Hierarchy Pattern

```hcl
# modules/compute/variables.tf
variable "instance_type" {
  type    = string
  default = "t3.micro"  # Safe default
}

variable "min_size" {
  type    = number
  default = 1
}

variable "enable_deletion_protection" {
  type    = bool
  default = true  # Safe default — must explicitly disable for dev
}
```

```hcl
# environments/dev/terraform.tfvars
instance_type              = "t3.micro"
min_size                   = 1
enable_deletion_protection = false

# environments/prod/terraform.tfvars
instance_type              = "t3.large"
min_size                   = 3
enable_deletion_protection = true
```

### Promotion Strategy

```
dev → staging → prod
 │       │        │
 │       │        └─ Manual approval required
 │       └─ Auto-apply after plan review
 └─ Auto-apply on merge to dev branch
```

---

## Phase 6: Security Hardening

### 15-Point Security Checklist

**P0 — Mandatory:**
- [ ] No secrets in `.tf` files, `.tfvars`, or state (use vault/SSM/secrets manager)
- [ ] State backend encrypted at rest with customer-managed keys
- [ ] State access restricted to CI/CD service accounts only
- [ ] `prevent_destroy` on critical resources (databases, S3 with data)
- [ ] Provider credentials via environment variables or OIDC, never in config
- [ ] `.gitignore` includes `*.tfvars` with secrets, `.terraform/`, `*.tfstate*`

**P1 — Required:**
- [ ] OIDC for CI/CD auth (no long-lived access keys)
- [ ] Least-privilege IAM for Terraform service account
- [ ] Security group rules explicit (no `0.0.0.0/0` ingress except ALB on 443)
- [ ] Encryption enabled on all data stores (RDS, S3, EBS, ElastiCache)
- [ ] VPC flow logs enabled
- [ ] CloudTrail/audit logging for all API calls

**P2 — Recommended:**
- [ ] OPA/Sentinel policies enforced in CI
- [ ] `tfsec` or `checkov` in CI pipeline
- [ ] Separate AWS accounts per environment (AWS Organizations)

### Secrets Management Decision Tree

```
Need a secret in Terraform?
├── Runtime secret (app needs at runtime)
│   └── Use AWS Secrets Manager / HashiCorp Vault
│       └── Reference via data source, pass ARN to app
├── Terraform-time secret (provider needs it)
│   └── Environment variable (TF_VAR_xxx) or OIDC
└── Generated secret (Terraform creates it)
    └── random_password resource → store in Secrets Manager
        └── Mark output as sensitive = true
```

### OIDC Authentication (GitHub Actions → AWS)

```hcl
# No access keys needed
data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_role" "terraform_ci" {
  name = "terraform-ci"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Federated = data.aws_iam_openid_connect_provider.github.arn }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:org/infra:*"
        }
      }
    }]
  })
}
```

---

## Phase 7: Testing Strategy

### 4-Level Test Pyramid

| Level | Tool | What It Tests | When |
|-------|------|---------------|------|
| **Static** | `terraform validate`, `tflint`, `tfsec`, `checkov` | Syntax, best practices, security | Every commit |
| **Plan** | `terraform plan` + policy checks | Expected changes, no surprises | Every PR |
| **Contract** | `terratest` / `tftest` (TF 1.6+) | Module inputs/outputs, behavior | PR + nightly |
| **Integration** | `terratest` with real cloud | Actual infrastructure works | Nightly/weekly |

### Native Terraform Test (TF 1.6+)

```hcl
# tests/networking.tftest.hcl
run "creates_vpc_with_correct_cidr" {
  command = plan

  variables {
    name        = "test"
    environment = "dev"
    vpc_cidr    = "10.0.0.0/16"
    azs         = ["us-east-1a"]
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR doesn't match input"
  }

  assert {
    condition     = aws_vpc.main.enable_dns_hostnames == true
    error_message = "DNS hostnames should be enabled"
  }
}

run "rejects_invalid_environment" {
  command = plan
  expect_failures = [var.environment]

  variables {
    name        = "test"
    environment = "invalid"
    vpc_cidr    = "10.0.0.0/16"
    azs         = ["us-east-1a"]
  }
}
```

### Static Analysis CI Step

```yaml
- name: Terraform Lint & Security
  run: |
    terraform fmt -check -recursive
    terraform validate
    tflint --recursive
    tfsec .
    checkov -d . --framework terraform
```

### 7 Testing Rules

1. **Static analysis on every commit** — catches 80% of issues for free
2. **Plan review on every PR** — humans approve infrastructure changes
3. **Native tests for modules** — `terraform test` is built-in, use it
4. **Integration tests destroy after** — `defer cleanup` to avoid orphaned resources
5. **Test in isolated account** — never test against production state
6. **Pin test dependencies** — terratest Go modules, provider versions
7. **Cost estimation in CI** — `infracost` to catch expensive surprises

---

## Phase 8: CI/CD Pipeline

### GitHub Actions Pipeline

```yaml
name: Terraform
on:
  pull_request:
    paths: ['infrastructure/**']
  push:
    branches: [main]
    paths: ['infrastructure/**']

permissions:
  id-token: write    # OIDC
  contents: read
  pull-requests: write  # PR comments

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.7.x"
      - run: terraform fmt -check -recursive
      - run: terraform init -backend=false
      - run: terraform validate
      - run: tflint --recursive
      - run: tfsec . --soft-fail

  plan:
    needs: validate
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::role/terraform-ci
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
      - working-directory: infrastructure/environments/${{ matrix.environment }}
        run: |
          terraform init
          terraform plan -out=tfplan -no-color
      - uses: actions/upload-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}/tfplan

  apply:
    if: github.ref == 'refs/heads/main'
    needs: plan
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    strategy:
      matrix:
        environment: [dev, staging, prod]
      max-parallel: 1  # Sequential: dev → staging → prod
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::role/terraform-ci
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
      - uses: actions/download-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}
      - working-directory: infrastructure/environments/${{ matrix.environment }}
        run: terraform apply tfplan
```

### CI/CD Rules

1. **Never `apply` from local machines** — CI/CD only
2. **Plan artifact = apply input** — same plan that was reviewed gets applied
3. **Sequential environment promotion** — dev → staging → prod, not parallel
4. **Production requires approval** — GitHub Environment protection rules
5. **Drift detection on schedule** — weekly `plan` to detect manual changes
6. **Cost estimation on PR** — Infracost or similar

---

## Phase 9: Resource Patterns

### Tagging Strategy

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Team        = var.team
    CostCenter  = var.cost_center
    Repository  = "github.com/org/infrastructure"
  }
}

# Apply to all resources
resource "aws_instance" "app" {
  # ...
  tags = merge(local.common_tags, {
    Name = "${var.name}-app"
    Role = "application"
  })
}
```

### Naming Convention

```
{project}-{environment}-{component}-{qualifier}
```

Examples: `acme-prod-vpc-main`, `acme-staging-rds-primary`, `acme-prod-alb-api`

### Common Patterns

**Conditional Resource Creation:**
```hcl
resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.environment == "prod" ? 1 : 0
  # Only create alarms in prod
}
```

**Dynamic Blocks:**
```hcl
resource "aws_security_group" "app" {
  name   = "${var.name}-app"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidrs
      description = ingress.value.description
    }
  }
}
```

**Data Source for Cross-Stack References:**
```hcl
# Instead of hardcoding VPC ID
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "company-terraform-state"
    key    = "environments/prod/networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use: data.terraform_remote_state.networking.outputs.vpc_id
```

---

## Phase 10: Drift Management

### Drift Detection Schedule

```yaml
# .github/workflows/drift-detection.yml
name: Drift Detection
on:
  schedule:
    - cron: '0 8 * * 1'  # Weekly Monday 8 AM UTC

jobs:
  detect:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::role/terraform-ci
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
      - working-directory: infrastructure/environments/${{ matrix.environment }}
        run: |
          terraform init
          terraform plan -detailed-exitcode -no-color 2>&1 | tee plan.txt
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "::warning::Drift detected in ${{ matrix.environment }}"
            # Send Slack alert
          fi
```

### Drift Response Playbook

| Drift Type | Response |
|-----------|----------|
| Manual console change (cosmetic) | Import or update config to match |
| Manual console change (critical) | Investigate who/why, then align |
| Auto-scaling / ASG changes | Expected — use `ignore_changes` for dynamic attributes |
| AWS service updates | Update provider version, review changelog |
| Security group modified manually | 🚨 Security incident — investigate immediately |

### `ignore_changes` Decision Guide

Use `ignore_changes` ONLY for:
- Attributes modified by the application at runtime (e.g., ASG desired count)
- Tags managed by external systems (e.g., AWS Backup tags)
- Attributes that drift due to API behavior (e.g., default security group rules)

**Never `ignore_changes` for:**
- Security configurations
- Network rules
- IAM policies
- Encryption settings

---

## Phase 11: Cost Optimization

### Infracost in CI

```yaml
- name: Infracost
  run: |
    infracost breakdown --path infrastructure/environments/prod/ \
      --format json --out-file infracost.json
    infracost output --path infracost.json --format github-comment \
      --out-file comment.md
    # Post as PR comment
```

### Cost Optimization Checklist

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| Reserved Instances / Savings Plans | 30-60% | Annual commitment for stable workloads |
| Right-sizing | 20-40% | Monitor CPU/memory, downsize over-provisioned |
| Spot/Preemptible for non-critical | 60-90% | Batch jobs, dev environments |
| S3 lifecycle policies | 20-50% storage | Transition to IA → Glacier → delete |
| NAT Gateway alternatives | $30-100/mo per GW | NAT instances for dev, VPC endpoints |
| Dev environment scheduling | 60-70% | Destroy nights/weekends, recreate on demand |
| Unused resource cleanup | Variable | Tag with TTL, auto-delete untagged after 7 days |

### Tagging for Cost Allocation

Required cost tags (enforce via policy):
- `CostCenter` — maps to business unit
- `Environment` — dev/staging/prod
- `Project` — which project owns this
- `Team` — responsible team
- `ManagedBy` — terraform/manual/other

---

## Phase 12: Advanced Patterns

### Terragrunt for DRY Environments

When you have 5+ environments with identical module structures, Terragrunt eliminates repetition:

```hcl
# terragrunt.hcl (root)
remote_state {
  backend = "s3"
  generate = { path = "backend.tf", if_exists = "overwrite_terragrunt" }
  config = {
    bucket         = "company-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### Import Block (TF 1.5+)

```hcl
# Declarative import — reviewable in PR
import {
  to = aws_s3_bucket.existing
  id = "my-existing-bucket"
}

resource "aws_s3_bucket" "existing" {
  bucket = "my-existing-bucket"
  # Write config to match existing resource
}
```

### Provider Aliases for Multi-Region

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu"
  region = "eu-west-1"
}

module "eu_networking" {
  source = "../../modules/networking"
  providers = { aws = aws.eu }
  # ...
}
```

### `moved` Block for Refactoring

```hcl
# Rename without destroy+create
moved {
  from = aws_instance.app
  to   = aws_instance.application
}

# Move into module
moved {
  from = aws_instance.app
  to   = module.compute.aws_instance.app
}
```

---

## Phase 13: Disaster Recovery & Migration

### State Recovery

```bash
# Enable versioning on state bucket (BEFORE you need it)
aws s3api put-bucket-versioning \
  --bucket company-terraform-state \
  --versioning-configuration Status=Enabled

# List state versions
aws s3api list-object-versions \
  --bucket company-terraform-state \
  --prefix environments/prod/networking/terraform.tfstate

# Restore previous version
aws s3api get-object \
  --bucket company-terraform-state \
  --key environments/prod/networking/terraform.tfstate \
  --version-id "versionId123" \
  restored-state.tfstate
```

### Migration Checklist (Moving Between Backends)

1. [ ] `terraform state pull > backup.tfstate` — backup current state
2. [ ] Update `backend.tf` with new backend config
3. [ ] `terraform init -migrate-state` — Terraform copies state
4. [ ] `terraform plan` — verify no changes (state matches)
5. [ ] Test apply on non-critical resource
6. [ ] Delete old state after verification period (7 days)

### Breaking Changes Protocol

When upgrading major Terraform or provider versions:
1. Read changelog for breaking changes
2. Test upgrade in dev first
3. Update `.terraform.lock.hcl`
4. Run `terraform plan` in all environments
5. Apply dev → staging → prod with 24h gaps

---

## Phase 14: Quality Scoring

### 100-Point Terraform Quality Rubric

| Dimension | Weight | Score Range |
|-----------|--------|-------------|
| State management | 20% | 0-20 |
| Security posture | 20% | 0-20 |
| Module design | 15% | 0-15 |
| Testing coverage | 15% | 0-15 |
| CI/CD automation | 10% | 0-10 |
| Documentation | 10% | 0-10 |
| Cost governance | 5% | 0-5 |
| Drift management | 5% | 0-5 |

**Scoring Guide:**
- **90-100**: Production-grade, fully automated, battle-tested
- **70-89**: Solid foundation, some gaps to address
- **50-69**: Functional but risky — prioritize security and state management
- **Below 50**: Stop deploying and fix fundamentals

### 10 Terraform Commandments

1. **Remote state with locking or don't start**
2. **Never hardcode secrets — not in code, not in state if avoidable**
3. **Plan is sacred — review every plan, apply only reviewed plans**
4. **Modules are contracts — version them, test them, document them**
5. **Environments are isolated — separate state, separate accounts ideally**
6. **`for_each` over `count` — stable addressing saves you**
7. **CI/CD applies, humans don't — no local `terraform apply` in prod**
8. **Tag everything — cost allocation, ownership, lifecycle**
9. **Drift is a bug — detect it weekly, fix it immediately**
10. **Upgrade deliberately — test in dev, read changelogs, lock versions**

### 10 Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Local state for team projects | State conflicts, data loss | Remote backend day 1 |
| Secrets in `.tfvars` committed to git | Credential exposure | Use vault/SSM + env vars |
| `count` for optional resources | Index shift on removal | `for_each` with conditional map |
| Monolithic state file | Slow plans, blast radius | Split by component (networking/compute/data) |
| No `prevent_destroy` on data stores | Accidental database deletion | Lifecycle rule on stateful resources |
| Unpinned module versions | Breaking changes on init | Pin with `?ref=v1.2.3` or `version = "~> 1.2"` |
| `terraform apply -auto-approve` in prod | Unreviewed changes | Plan artifact → human review → apply |
| Using workspaces as environments | Shared state, shared blast radius | Separate directories + backends per env |
| No cost estimation in CI | $10K surprise bills | Infracost or similar on every PR |
| Manual changes "just this once" | Permanent drift | Always go through code, even for emergencies |

---

## Natural Language Commands

- "Review this Terraform code" → Run Phase 1 health check + static analysis recommendations
- "Design infrastructure for [service]" → Phase 2 structure + Phase 4 module design
- "Set up remote state" → Phase 3 backend configuration
- "Create a module for [resource]" → Phase 4 module template with variables/outputs
- "Compare environments" → Phase 5 environment matrix
- "Security audit my Terraform" → Phase 6 security checklist
- "Add tests to this module" → Phase 7 native test examples
- "Set up CI/CD for Terraform" → Phase 8 GitHub Actions pipeline
- "Check for drift" → Phase 10 drift detection setup
- "Estimate infrastructure costs" → Phase 11 Infracost integration
- "Migrate state to new backend" → Phase 13 migration checklist
- "Score this Terraform project" → Phase 14 quality rubric

---

## ⚡ Level Up

This skill covers Terraform methodology and best practices. For industry-specific infrastructure patterns:

- **SaaS Infrastructure** → [AfrexAI SaaS Context Pack ($47)](https://afrexai-cto.github.io/context-packs/)
- **Fintech Compliance Infrastructure** → [AfrexAI Fintech Context Pack ($47)](https://afrexai-cto.github.io/context-packs/)
- **Healthcare HIPAA Infrastructure** → [AfrexAI Healthcare Context Pack ($47)](https://afrexai-cto.github.io/context-packs/)

## 🔗 More Free Skills by AfrexAI

- `clawhub install afrexai-devops-engine` — Complete DevOps & Platform Engineering
- `clawhub install afrexai-cybersecurity-engine` — Security Hardening & Compliance
- `clawhub install afrexai-system-architect` — System Architecture Decision Frameworks
- `clawhub install afrexai-api-architect` — API Design & Lifecycle Management
- `clawhub install afrexai-cicd-engineering` — CI/CD Pipeline Engineering

Browse all AfrexAI skills: [clawhub.com](https://clawhub.com) → Search "afrexai"

Storefront: [afrexai-cto.github.io/context-packs](https://afrexai-cto.github.io/context-packs/)
