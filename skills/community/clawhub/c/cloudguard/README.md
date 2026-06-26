# CloudGuard

<p align="center">
  <img src="https://img.shields.io/badge/patterns-90-blue" alt="90 patterns">
  <img src="https://img.shields.io/badge/categories-6-purple" alt="6 categories">
  <img src="https://img.shields.io/badge/license-COMMERCIAL-orange" alt="Commercial License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find the cloud misconfigurations your IaC is hiding. Fix them before they go live.</h3>

<p align="center">
  <a href="https://cloudguard.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#check-categories">Categories</a> &middot;
  <a href="https://cloudguard.pages.dev/#pricing">Pricing</a>
</p>

---

## Your cloud infrastructure has misconfigurations. Dangerous ones.

Studies show that over 70% of cloud breaches stem from misconfigured infrastructure. Public S3 buckets leaking customer data. Security groups open to 0.0.0.0/0 on port 22. IAM policies with `*:*` wildcard permissions. EBS volumes without encryption at rest. CloudTrail disabled in production. Terraform files deploying resources with no VPC isolation.

A single misconfiguration can expose your entire cloud environment. Attackers scan for open ports and public buckets continuously. Compliance auditors flag these issues in every review.

**CloudGuard finds the misconfigurations before they reach production.** Pre-commit hooks. Local scanning. 90 patterns across 6 security categories. Severity-graded scoring with actionable remediation. Zero data leaves your machine.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install cloudguard

# 2. Scan your infrastructure code
cloudguard scan

# 3. Install pre-commit hooks (Pro)
cloudguard hooks install
```

That's it. Every commit touching IaC files is now scanned for cloud security issues before it lands.

## What It Does

### Scan IaC files for cloud misconfigurations
One command to scan any Terraform, CloudFormation, Kubernetes, or Docker configuration. 90 regex patterns detect security issues across storage, IAM, networking, encryption, logging, and compliance.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged IaC file. If critical or high-severity misconfigurations are detected, the commit is blocked with clear remediation guidance.

### Generate cloud security reports
Produce markdown reports with severity breakdowns, category analysis, and remediation priority. Ideal for security reviews, compliance audits, and team presentations.

### Category-focused auditing
Run scans targeting specific categories (S3, IAM, Networking, Encryption, Logging, Configuration) for focused compliance checks.

### Multiple output formats
Generate results as plain text, structured JSON for CI/CD pipelines, or HTML reports for stakeholder sharing.

## How It Compares

| Feature | CloudGuard | tfsec ($0) | checkov ($0) | tflint ($0) | kics ($0) | terrascan ($0) |
|---------|:----------:|:----------:|:------------:|:-----------:|:---------:|:--------------:|
| 90 security patterns | Yes | ~300 | ~1000 | ~100 | ~2000 | ~500 |
| S3/Storage security | Yes | Yes | Yes | Limited | Yes | Yes |
| IAM analysis | Yes | Yes | Yes | No | Yes | Yes |
| Network security | Yes | Yes | Yes | Limited | Yes | Yes |
| Encryption checks | Yes | Yes | Yes | No | Yes | Yes |
| Logging/monitoring | Yes | Yes | Yes | No | Yes | Yes |
| Compliance checks | Yes | Yes | Yes | No | Yes | Yes |
| Pre-commit hooks | Yes | Yes | Yes | Yes | Yes | No |
| Zero config scan | Yes | Yes | Yes | Config needed | Yes | Config needed |
| Offline license | Yes | N/A | N/A | N/A | N/A | N/A |
| Local-only (no cloud) | Yes | Yes | Yes | Yes | Yes | Yes |
| Zero telemetry | Yes | Yes | Opt-out | Yes | Yes | Yes |
| No binary deps | Yes | Go binary | Python | Go binary | Go binary | Go binary |
| Score & grades | Yes | No | No | No | No | No |
| ClawHub integration | Yes | No | No | No | No | No |
| Price (individual) | Free/$19/mo | Free | Free | Free | Free | Free |

## Check Categories

CloudGuard detects 90 cloud security patterns across 6 categories:

### S3 / Storage Security (15 patterns)

| Check | Severity | Description |
|-------|----------|-------------|
| Public ACL on S3 bucket | Critical | S3 bucket with `acl = "public-read"` or `acl = "public-read-write"` |
| Missing server-side encryption | Critical | S3 bucket without `server_side_encryption_configuration` block |
| Missing bucket versioning | High | S3 bucket without versioning enabled |
| Overly permissive bucket policy | Critical | Bucket policy with `Principal: "*"` allowing public access |
| Missing access logging | Medium | S3 bucket without access logging configured |
| No lifecycle rules | Low | S3 bucket without lifecycle rules for cost and data management |
| Missing block public access | Critical | S3 bucket without `block_public_acls` and related settings |
| CloudFront without HTTPS | High | CloudFront distribution without viewer protocol HTTPS-only |
| EFS without encryption | High | EFS file system created without encryption at rest |
| Unencrypted DynamoDB | High | DynamoDB table without server-side encryption |
| Public access in bucket policy | Critical | Bucket policy allowing `s3:GetObject` to all principals |
| Missing S3 Object Lock | Medium | S3 bucket without object lock for immutability |
| S3 bucket without MFA delete | Medium | S3 bucket without MFA delete protection |
| Missing cross-region replication | Low | S3 bucket without cross-region replication for DR |
| S3 transfer acceleration disabled | Low | S3 bucket without transfer acceleration |

### IM / IAM & Permissions (15 patterns)

| Check | Severity | Description |
|-------|----------|-------------|
| Wildcard IAM action | Critical | IAM policy with `Action: "*"` granting all permissions |
| AdministratorAccess policy | Critical | IAM role or user attached to `AdministratorAccess` managed policy |
| Overly broad assume role | High | AssumeRole policy with `Principal: "*"` |
| IAM user with inline policy | High | IAM user with inline policy instead of managed policy |
| Missing MFA condition | High | IAM policy missing `aws:MultiFactorAuthPresent` condition |
| Root account access key | Critical | Root account with active access keys |
| Wildcard resource in policy | High | IAM policy with `Resource: "*"` |
| PassRole with wildcard | Critical | `iam:PassRole` on `Resource: "*"` |
| Missing permission boundary | Medium | IAM role without permission boundary |
| No password policy | Medium | AWS account without IAM password policy |
| Cross-account trust too broad | High | Cross-account trust with overly broad principal |
| Missing deny statement | Medium | IAM policy without explicit deny for sensitive actions |
| Lambda with admin role | Critical | Lambda function with AdministratorAccess role |
| User with console and API | Medium | IAM user with both console access and API keys |
| Group without policy | Low | IAM group defined without any attached policies |

### NW / Network Security (15 patterns)

| Check | Severity | Description |
|-------|----------|-------------|
| Security group open to world | Critical | Ingress rule with `cidr_blocks = ["0.0.0.0/0"]` |
| SSH open to internet | Critical | Port 22 open to `0.0.0.0/0` |
| RDP open to internet | Critical | Port 3389 open to `0.0.0.0/0` |
| Database port exposed | High | Port 3306/5432/27017 open to `0.0.0.0/0` |
| All ports open | Critical | Security group with `from_port = 0, to_port = 65535` |
| Missing VPC configuration | High | Resource deployed without VPC/subnet specification |
| No network ACL | Medium | Subnet without associated network ACL |
| Public subnet without NAT | High | Public subnet routing directly to IGW without NAT gateway |
| Default VPC in use | Medium | Resources deployed in the default VPC |
| Missing egress restriction | Medium | Security group with unrestricted egress (`0.0.0.0/0`) |
| IPv6 open to world | High | Security group with `::/0` ingress rule |
| No VPC flow logs | High | VPC without flow logs enabled |
| Elasticsearch public access | Critical | Elasticsearch domain with public access enabled |
| Redis/ElastiCache exposed | High | ElastiCache cluster without subnet group in VPC |
| Load balancer HTTP only | High | Load balancer listener on HTTP without HTTPS redirect |

### EN / Encryption (15 patterns)

| Check | Severity | Description |
|-------|----------|-------------|
| Unencrypted EBS volume | Critical | EBS volume with `encrypted = false` |
| Missing KMS key rotation | High | KMS key without `enable_key_rotation = true` |
| RDS without encryption | Critical | RDS instance with `storage_encrypted = false` |
| Missing SSL/TLS certificate | High | Resource without SSL/TLS configuration |
| No transit encryption | High | ElastiCache without `transit_encryption_enabled` |
| Weak TLS version | High | Resource configured with TLS 1.0 or 1.1 |
| S3 bucket without SSE | Critical | S3 bucket missing `server_side_encryption_configuration` |
| Redshift without encryption | Critical | Redshift cluster with `encrypted = false` |
| SQS without encryption | Medium | SQS queue without `kms_master_key_id` |
| SNS without encryption | Medium | SNS topic without `kms_master_key_id` |
| CloudWatch logs unencrypted | Medium | CloudWatch log group without `kms_key_id` |
| EBS default encryption off | High | AWS account without EBS default encryption enabled |
| Aurora without encryption | Critical | Aurora cluster with `storage_encrypted = false` |
| Kinesis without encryption | Medium | Kinesis stream without `encryption_type = "KMS"` |
| Secrets Manager no CMK | Low | Secrets Manager secret without customer-managed KMS key |

### LG / Logging & Monitoring (15 patterns)

| Check | Severity | Description |
|-------|----------|-------------|
| Missing CloudTrail | Critical | AWS account or region without CloudTrail enabled |
| CloudTrail not multi-region | High | CloudTrail trail with `is_multi_region_trail = false` |
| No VPC flow logs | High | VPC without flow logs for network monitoring |
| GuardDuty disabled | High | AWS account without GuardDuty enabled |
| Missing CloudWatch alarms | Medium | No CloudWatch alarms for critical metrics |
| No SNS notification topic | Medium | Missing SNS topic for security notifications |
| S3 access logging disabled | Medium | S3 bucket without server access logging |
| ALB access logs disabled | Medium | Application Load Balancer without access logging |
| RDS audit logging off | High | RDS instance without audit logging enabled |
| Lambda no log group | Medium | Lambda function without CloudWatch log group |
| Config recorder disabled | High | AWS Config recorder not enabled |
| CloudTrail log validation off | High | CloudTrail without log file validation |
| No metric filters | Medium | CloudWatch without metric filters for security events |
| EKS audit logging off | High | EKS cluster without audit logging to CloudWatch |
| Missing access analyzer | Low | IAM Access Analyzer not configured in region |

### CF / Configuration & Compliance (15 patterns)

| Check | Severity | Description |
|-------|----------|-------------|
| Missing resource tags | Medium | Cloud resource without required tags (Name, Environment, Owner) |
| Hardcoded AWS region | Medium | Terraform with hardcoded region string instead of variable |
| Hardcoded AMI ID | Medium | EC2 instance with hardcoded AMI ID |
| Missing backup configuration | High | RDS/DynamoDB without backup retention configured |
| No deletion protection | Medium | RDS/DynamoDB without deletion protection |
| Hardcoded availability zone | Low | Resource with hardcoded AZ instead of data source |
| Missing auto-scaling | Medium | EC2/ECS without auto-scaling configuration |
| No multi-AZ deployment | High | RDS without `multi_az = true` for high availability |
| Terraform backend insecure | High | Terraform backend without encryption or locking |
| Missing health checks | Medium | Load balancer target group without health checks |
| Resource naming non-standard | Low | Resources without consistent naming convention |
| Outdated provider version | Medium | Terraform provider without version constraint |
| No lifecycle prevent destroy | Low | Critical resources without `prevent_destroy` lifecycle rule |
| Missing outputs | Low | Terraform module without outputs for key resources |
| Hardcoded account ID | Medium | AWS account ID hardcoded instead of using data source |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| Security patterns | 30 | 60 | 90 (all) |
| 6 check categories | Yes | Yes | Yes |
| Score & grading | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Security reports | | Yes | Yes |
| Deep audit mode | | Yes | Yes |
| JSON output | | | Yes |
| HTML output | | | Yes |
| Category filtering | | | Yes |
| CI/CD integration | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "cloudguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/examples/**"],
          "ignoreChecks": [],
          "reportFormat": "text",
          "categories": ["S3", "IM", "NW", "EN", "LG", "CF"]
        }
      }
    }
  }
}
```

## Ecosystem

CloudGuard is part of the ClawHub code quality suite:

- **[SecretScan](https://secretscan.pages.dev)** -- Hardcoded secrets & credential leak detection
- **[EnvGuard](https://envguard.pages.dev)** -- Environment variable safety checking
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[DeadCode](https://deadcode.pages.dev)** -- Dead code and unused export detection
- **[PerfGuard](https://perfguard.pages.dev)** -- Performance regression detection
- **[GitPulse](https://gitpulse.pages.dev)** -- Git workflow analytics
- **[DocSync](https://docsync.pages.dev)** -- Documentation drift detection
- **[MigrateSafe](https://migratesafe.pages.dev)** -- Database migration safety checking
- **[LicenseGuard](https://licenseguard.pages.dev)** -- License compliance scanning
- **[CloudGuard](https://cloudguard.pages.dev)** -- Cloud infrastructure & IaC security scanning

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies beyond bash and grep

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Add or improve patterns in `scripts/patterns.sh`
4. Ensure all regex patterns are valid POSIX ERE (`grep -E` compatible)
5. Test patterns against sample IaC files
6. Submit a pull request

### Adding New Patterns

Each pattern follows the format:
```
REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
```

- **REGEX**: POSIX Extended Regular Expression compatible with `grep -E`
- **SEVERITY**: `critical`, `high`, `medium`, or `low`
- **CHECK_ID**: Category prefix + sequential number (e.g., `S3-016`)
- **DESCRIPTION**: Clear explanation of the security issue
- **RECOMMENDATION**: Actionable fix guidance

### Pattern Guidelines

- Use `[[:space:]]` instead of `\s` for POSIX compatibility
- Avoid Perl-only features (`\d`, `\w`, `\b`, etc.)
- Test with `grep -E "pattern" testfile.tf` before submitting
- Include both Terraform and CloudFormation variants where applicable
- Assign realistic severities based on actual security impact

## License

COMMERCIAL -- See https://cloudguard.pages.dev/license for terms.

Free tier available for individual use. Pro and Team licenses available at https://cloudguard.pages.dev/pricing.
