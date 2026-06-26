---
name: BloodHound Narrator
description: Turn BloodHound attack path exports into dual-layer security reports — CISO executive prose on top, technical remediation playbook below. Automates Active Directory audit reporting for pentesters, blue teams, and security consultants. Supports DCSync, Kerberoasting, unconstrained delegation, ACL abuse, GPO takeover, and lateral movement paths. Pure local PowerShell — no API calls, no data leaves your machine. Air-gap compatible.
version: 1.0.0
license: MIT-0
bins:
  - pwsh
---

# BloodHound Narrator

Turn BloodHound attack paths into boardroom-ready security reports — entirely offline.

Built for **pentesters**, **blue teams**, and **AD security consultants** who need to translate BloodHound graph output into actionable deliverables without spending hours writing prose.

BloodHound Narrator ingests Cypher export JSON, scores each attack path on a weighted severity model, and produces a **dual-layer Markdown report**:

1. **CISO / Executive Layer** — severity summary table, per-path business risk narrative, impact statements written in non-technical language that management and board members can act on.
2. **Technical Remediation Appendix** — step-by-step hardening playbook with PowerShell commands, Event IDs to monitor, and remediation guidance per finding.

**Detected attack patterns:** DCSync, Kerberoasting, unconstrained delegation, GenericAll / WriteDacl / WriteOwner ACL abuse, GPO takeover, lateral movement chains (AdminTo + HasSession), Tier 0 boundary violations, stale service account passwords, and sensitive data exposure paths.

No API keys. No network calls. No data exfiltration risk. Air-gap compatible. Works in regulated, classified, and OT environments.

## Setup

Install PowerShell (if not already present):

```bash
# macOS
brew install powershell/tap/powershell

# Linux (Ubuntu/Debian)
sudo apt-get install -y powershell

# Windows — already included
```

No environment variables or credentials required.

## Usage

```bash
# Generate a full report (all severities)
bash {baseDir}/scripts/bh-narrator.sh -InputFile "path/to/bloodhound-export.json"

# Only include Critical and High findings
bash {baseDir}/scripts/bh-narrator.sh -InputFile "path/to/export.json" -MinSeverity High

# Specify output path
bash {baseDir}/scripts/bh-narrator.sh -InputFile "path/to/export.json" -OutputFile "report.md"

# Pipe classified objects for further processing
bash {baseDir}/scripts/bh-narrator.sh -InputFile "path/to/export.json" -PassThru
```

## Run the test suite

```bash
bash {baseDir}/tests/run-tests.sh
```

A synthetic BloodHound export with 5 attack paths (3 Critical, 2 High) is included at `{baseDir}/tests/synthetic-bloodhound.json` for validation.

## Severity Scoring Model

| Factor | Points | Example |
|--------|--------|---------|
| Tier 0 target (DA, EA, DC) | +40 | Path ends at Domain Admins |
| DCSync edge | +30 | Replication rights on DC |
| GenericAll/WriteDacl/Owns on Tier 0 | +30 | GenericAll on Domain Admins group |
| Unconstrained delegation in path | +20 | TGT cached on delegation host |
| GenericAll/WriteDacl/Owns (non-Tier 0) | +15 | WriteDacl on OU |
| Sensitive data keywords in path | +15 | Target description contains "PII" or "financial" |
| Kerberoastable source | +10 | Source account has SPN set |
| Short path (1-2 hops) | +10 | Direct GenericAll to DA |
| Lateral movement chain | +10 | AdminTo + HasSession combo |
| Medium path (3 hops) | +5 | Three-hop escalation |
| Stale password (>365 days) | +5 | Service account never rotated |

**Thresholds:** Critical >= 50 | High >= 30 | Medium >= 15 | Low < 15

## Report Output

The generated Markdown report includes:

- Header with domain name, collection date, BloodHound version
- Executive summary with severity distribution table
- Per-path findings with attack chain, business risk bullets, and impact statement
- Technical remediation appendix with numbered steps per finding (DCSync removal, gMSA migration, delegation hardening, tier isolation, GPO lockdown, etc.)

## Who Is This For

- **Pentesters** delivering AD audit reports to clients — skip the manual write-up, generate the narrative from your BloodHound data
- **Blue team / SOC analysts** triaging BloodHound findings after a security assessment
- **Security consultants** who need client-ready deliverables fast
- **CISOs and security managers** who want attack path reports they can actually read without a graph database
- **Purple teams** documenting offensive findings for defensive remediation

## Use Cases

- Post-pentest AD audit reporting
- Quarterly Active Directory security health checks
- Incident response — rapid attack path analysis after a compromise
- Compliance reporting (ISO 27001, NIS2, LPM, SOC2) requiring documented AD risk assessments
- Training and awareness — show management what "3 hops to Domain Admin" actually means
