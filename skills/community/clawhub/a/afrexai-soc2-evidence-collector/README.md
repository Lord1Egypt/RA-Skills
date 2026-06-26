# SOC2 Evidence Collector

Automate evidence gathering for SOC2 Type I and Type II audits across all 5 Trust Service Criteria.

## What It Does

- Generates a complete evidence matrix covering Security (CC), Availability, Processing Integrity, Confidentiality, and Privacy criteria
- Creates automated collection scripts for AWS, GitHub, and IdP platforms
- Identifies evidence gaps with remediation steps
- Builds an evidence collection schedule so nothing is missed

## Quick Start

Tell your AI agent:
> "I need to prepare for a SOC2 Type II audit. We're on AWS with GitHub for CI/CD. Security and Availability are in scope."

The skill will generate:
1. A tailored evidence checklist with 50+ control points
2. Shell scripts to pull evidence from AWS, GitHub, and your IdP
3. A gap analysis showing what's missing
4. A collection schedule (daily/weekly/monthly/quarterly cadence)

## Who It's For

- **Startups preparing for their first SOC2 audit**
- **Engineering teams** who own compliance evidence collection
- **Compliance managers** who want automation over spreadsheets
- **Audit firms** looking to streamline client evidence requests

## Trust Service Criteria Covered

| Criteria | Controls | Automation |
|----------|----------|------------|
| CC (Security) | CC1-CC9, 40+ evidence items | AWS IAM, CloudTrail, VPC, S3 encryption |
| Availability | SLAs, capacity, redundancy | Uptime monitoring, auto-scaling configs |
| Processing Integrity | Validation, QA, reconciliation | CI/CD pipeline evidence |
| Confidentiality | Classification, DLP, retention | Policy version tracking |
| Privacy | Consent, DSRs, PIAs | Consent logs, DSR ticket tracking |

## Installation

```bash
clawhub install afrexai-soc2-evidence-collector
```

## Built by AfrexAI

For managed SOC2 compliance with AI agents handling continuous evidence collection and auditor coordination, visit [afrexai.com](https://afrexai.com).
