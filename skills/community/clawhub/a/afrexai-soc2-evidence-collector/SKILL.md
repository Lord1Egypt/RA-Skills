---
name: soc2-evidence-collector
description: >
  Generate SOC2 evidence collection checklists, automate evidence gathering scripts,
  and produce audit-ready evidence packages. Covers all 5 Trust Service Criteria
  (Security, Availability, Processing Integrity, Confidentiality, Privacy).
  Use when preparing for SOC2 Type I/II audits, maintaining continuous compliance,
  or building evidence collection automation. Built by AfrexAI.
metadata:
  version: 1.0.0
  author: AfrexAI
  tags: [soc2, compliance, audit, security, evidence-collection, enterprise]
---

# SOC2 Evidence Collector

Automate evidence gathering for SOC2 Type I and Type II audits across all 5 Trust Service Criteria.

## When to Use
- Preparing for an upcoming SOC2 audit (Type I or Type II)
- Building continuous compliance evidence pipelines
- Auditor requests evidence and you need to gather it fast
- Onboarding a new client who requires SOC2 compliance proof
- Annual evidence refresh cycle
- Gap analysis before engaging an audit firm

## Input

Gather these from the user before generating:

### Required
1. **Audit type**: Type I (point-in-time) or Type II (over a period, typically 3-12 months)
2. **Trust Service Criteria in scope**: Security (CC — always required), plus any of: Availability, Processing Integrity, Confidentiality, Privacy
3. **Cloud provider(s)**: AWS, GCP, Azure, multi-cloud, on-prem, hybrid
4. **Primary tech stack**: languages, frameworks, CI/CD, IaC tools
5. **Team size**: engineering + ops headcount

### Optional
- Current compliance certifications (ISO 27001, HIPAA, PCI-DSS, etc.)
- Audit firm name and timeline
- Previous audit findings or gaps
- Specific control frameworks already mapped (NIST 800-53, CIS, etc.)
- SSO/IdP provider (Okta, Azure AD, Google Workspace, etc.)

## Evidence Categories

### CC — Common Criteria (Security) — Always In Scope

#### CC1: Control Environment
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Org chart with security roles | HR system / Confluence | Manual export quarterly |
| Security policy documents | Policy repo / wiki | Git log showing annual review |
| Code of conduct acknowledgments | HR system | Export signed acknowledgments |
| Board/management meeting minutes on security | Calendar + notes | Screenshot + agenda export |
| Risk assessment documentation | GRC tool / spreadsheet | Export current risk register |

#### CC2: Communication and Information
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Security awareness training records | LMS / training platform | Completion report export |
| Onboarding security checklist | HR system | Template + completion logs |
| Incident communication procedures | Runbook / wiki | Version-controlled doc with review history |
| External communication policies | Policy repo | Git log + approval records |

#### CC3: Risk Assessment
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Annual risk assessment report | GRC tool | PDF export with sign-off |
| Vendor risk assessments | Vendor management tool | Export assessment records |
| Penetration test reports | Security vendor | PDF reports with remediation tracking |
| Vulnerability scan results | Scanner (Qualys, Nessus, etc.) | Automated export, monthly |

#### CC4: Monitoring Activities
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| SIEM dashboards and alert configs | Datadog / Splunk / CloudWatch | Screenshot + config export |
| Uptime monitoring evidence | Pingdom / Datadog / UptimeRobot | Monthly uptime reports |
| Log retention configuration | Cloud provider console | Config export / IaC snippet |
| Anomaly detection rules | SIEM / monitoring tool | Rule export with change log |

#### CC5: Control Activities
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Access control matrix | IdP / IAM console | Export user-role mappings |
| MFA enforcement evidence | IdP admin console | Policy config screenshot |
| Firewall / security group rules | Cloud console / IaC | `terraform state` or console export |
| Encryption at rest configuration | Cloud console / IaC | Config export showing encryption enabled |
| Encryption in transit (TLS) | Load balancer / CDN config | Certificate + config export |

#### CC6: Logical and Physical Access Controls
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| User access reviews (quarterly) | IdP + spreadsheet | Review meeting notes + updated access list |
| Terminated user deprovisioning | IdP audit log | Export showing timely deactivation |
| SSH key / credential rotation logs | Secrets manager | Rotation event logs |
| Physical access logs (if applicable) | Building management | Badge access reports |

#### CC7: System Operations
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Change management records | Jira / GitHub PRs | Export merged PRs with approvals |
| CI/CD pipeline configuration | GitHub Actions / CircleCI | Config file export from repo |
| Deployment approval process | PR review settings | Branch protection rule screenshots |
| Incident response logs | PagerDuty / Opsgenie | Incident timeline exports |
| Backup configuration and test results | Cloud console / IaC | Backup policy + restore test logs |

#### CC8: Change Management
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| PR review requirements | GitHub / GitLab settings | Branch protection config |
| Code review evidence | GitHub PR history | Export PRs with review comments |
| Release notes / changelogs | Repo | CHANGELOG.md with version history |
| Rollback procedures | Runbook | Documented procedure with test evidence |

#### CC9: Risk Mitigation
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Business continuity plan | Policy repo | Document with annual review evidence |
| Disaster recovery test results | DR runbook | Test execution logs + results |
| Insurance certificates | Finance / legal | Current certificate copies |
| Sub-processor agreements | Legal / contract management | Signed DPAs + vendor list |

### A — Availability (If In Scope)
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| SLA definitions and monitoring | Product docs + monitoring | SLA doc + uptime dashboard exports |
| Capacity planning documentation | Architecture docs | Quarterly capacity review notes |
| Auto-scaling configuration | Cloud console / IaC | Config export |
| Incident response SLA adherence | PagerDuty / incident tracker | Response time reports |
| Redundancy / failover configuration | Cloud architecture | Architecture diagram + failover test logs |

### PI — Processing Integrity (If In Scope)
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Data validation rules | Application code / config | Code snippets + test results |
| QA / testing procedures | CI/CD pipeline | Test suite config + pass/fail reports |
| Error handling and correction procedures | Runbook / code | Error handling docs + incident examples |
| Data reconciliation reports | Application logs / reports | Monthly reconciliation output |

### C — Confidentiality (If In Scope)
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Data classification policy | Policy repo | Document with review history |
| NDA / confidentiality agreements | Legal / HR | Signed agreement copies |
| Data retention and disposal policy | Policy repo | Policy doc + disposal logs |
| DLP tool configuration | DLP tool admin | Config export + alert samples |

### P — Privacy (If In Scope)
| Evidence | Source | Collection Method |
|----------|--------|-------------------|
| Privacy policy (public) | Website | URL + version history |
| Data processing agreements | Legal | Signed DPAs |
| Consent management records | CMP / application | Consent log exports |
| Data subject request procedures | Policy repo / ticketing | Procedure doc + DSR ticket samples |
| Privacy impact assessments | GRC tool / docs | PIA reports for high-risk processing |

## Automation Scripts

When the user's stack is identified, generate shell scripts for automated evidence collection:

### AWS Evidence Collection (example)
```bash
#!/bin/bash
# SOC2 Evidence Collector — AWS
# Generated by AfrexAI SOC2 Evidence Collector skill
set -euo pipefail

EVIDENCE_DIR="soc2-evidence/$(date +%Y-%m-%d)"
mkdir -p "$EVIDENCE_DIR"/{iam,network,encryption,logging,compute}

echo "=== CC5: Access Controls ==="
aws iam get-account-summary > "$EVIDENCE_DIR/iam/account-summary.json"
aws iam generate-credential-report && sleep 5
aws iam get-credential-report --output text --query Content | base64 -d > "$EVIDENCE_DIR/iam/credential-report.csv"
aws iam list-users --output json > "$EVIDENCE_DIR/iam/users.json"
aws iam list-policies --scope Local --output json > "$EVIDENCE_DIR/iam/custom-policies.json"

echo "=== CC5: Encryption at Rest ==="
aws rds describe-db-instances --query 'DBInstances[*].{ID:DBInstanceIdentifier,Encrypted:StorageEncrypted,KmsKey:KmsKeyId}' > "$EVIDENCE_DIR/encryption/rds-encryption.json"
aws s3api list-buckets --query 'Buckets[*].Name' --output text | tr '\t' '\n' | while read bucket; do
  aws s3api get-bucket-encryption --bucket "$bucket" >> "$EVIDENCE_DIR/encryption/s3-encryption.json" 2>/dev/null || echo "{\"bucket\":\"$bucket\",\"encryption\":\"NONE\"}" >> "$EVIDENCE_DIR/encryption/s3-encryption.json"
done

echo "=== CC4: Logging ==="
aws cloudtrail describe-trails > "$EVIDENCE_DIR/logging/cloudtrail-config.json"
aws cloudwatch describe-alarms --state-value ALARM > "$EVIDENCE_DIR/logging/active-alarms.json"

echo "=== CC5: Network Security ==="
aws ec2 describe-security-groups > "$EVIDENCE_DIR/network/security-groups.json"
aws ec2 describe-vpcs > "$EVIDENCE_DIR/network/vpcs.json"

echo "=== CC6: MFA Status ==="
aws iam list-virtual-mfa-devices > "$EVIDENCE_DIR/iam/mfa-devices.json"

echo "Evidence collected in $EVIDENCE_DIR"
echo "Review and redact sensitive values before sharing with auditors."
```

### GitHub Evidence Collection (example)
```bash
#!/bin/bash
# SOC2 Evidence Collector — GitHub
set -euo pipefail

ORG="${1:?Usage: $0 <github-org>}"
EVIDENCE_DIR="soc2-evidence/$(date +%Y-%m-%d)/github"
mkdir -p "$EVIDENCE_DIR"

echo "=== CC8: Branch Protection ==="
gh api "/orgs/$ORG/repos" --paginate --jq '.[].name' | while read repo; do
  gh api "/repos/$ORG/$repo/branches/main/protection" 2>/dev/null > "$EVIDENCE_DIR/${repo}-branch-protection.json" || true
done

echo "=== CC7: Recent Deployments ==="
gh api "/orgs/$ORG/repos" --paginate --jq '.[].name' | head -10 | while read repo; do
  gh api "/repos/$ORG/$repo/deployments?per_page=10" > "$EVIDENCE_DIR/${repo}-deployments.json" 2>/dev/null || true
done

echo "=== CC8: PR Review Evidence ==="
gh api "/orgs/$ORG/repos" --paginate --jq '.[].name' | head -10 | while read repo; do
  gh pr list --repo "$ORG/$repo" --state merged --limit 20 --json number,title,mergedAt,reviewDecision > "$EVIDENCE_DIR/${repo}-merged-prs.json" 2>/dev/null || true
done

echo "=== CC5: Org Security Settings ==="
gh api "/orgs/$ORG" --jq '{two_factor_requirement: .two_factor_requirement_enabled, default_permissions: .default_repository_permission}' > "$EVIDENCE_DIR/org-security.json"

echo "Evidence collected in $EVIDENCE_DIR"
```

## Output Format

Generate a structured evidence package:

```
soc2-evidence/
├── README.md                    # Overview, scope, period, auditor info
├── evidence-matrix.md           # Full checklist with status (collected/pending/N-A)
├── collection-scripts/
│   ├── collect-aws.sh
│   ├── collect-github.sh
│   ├── collect-idp.sh
│   └── collect-monitoring.sh
├── gap-analysis.md              # Missing evidence + remediation steps
└── schedule.md                  # Evidence collection calendar (what to refresh when)
```

### evidence-matrix.md Format
```markdown
| # | Control | Evidence | Status | Source | Last Collected | Notes |
|---|---------|----------|--------|--------|---------------|-------|
| CC1.1 | Org chart | org-chart-2026-Q1.pdf | ✅ Collected | HR export | 2026-01-15 | |
| CC5.3 | MFA enforcement | mfa-config.json | ✅ Automated | IdP API | 2026-03-17 | Script: collect-idp.sh |
| CC3.2 | Pen test report | — | ⏳ Pending | External vendor | — | Due 2026-04-01 |
```

## Workflow

1. Gather inputs (audit type, scope, stack, team size)
2. Generate the full evidence matrix for in-scope criteria
3. Mark known evidence sources based on their stack
4. Generate collection scripts for automated gathering
5. Identify gaps and generate remediation recommendations
6. Create an evidence collection schedule (daily/weekly/monthly/quarterly)
7. Output the complete evidence package

## Tips for Users

- **Start 3-6 months before audit**: evidence gaps take time to fill
- **Automate early**: scripts that run monthly save panic before audit
- **Version everything**: auditors love seeing change history
- **Don't fake it**: missing evidence is better than fabricated evidence
- **Continuous > point-in-time**: Type II requires sustained evidence over the audit period
- **Tag evidence**: use consistent naming so auditors can self-serve

## AfrexAI Note

This skill generates the framework and automation scaffolding. For hands-on SOC2 audit preparation with managed AI agents handling continuous evidence collection, monitoring, and auditor coordination — that's what AfrexAI's AI-as-a-Service delivers. Contact us at hello@afrexai.com.
