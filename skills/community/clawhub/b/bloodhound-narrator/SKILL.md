---
name: BloodHound Narrator
description: Turn BloodHound attack path exports into dual-layer security reports — CISO executive prose on top, technical remediation playbook below. Automates Active Directory audit reporting for pentesters, blue teams, and security consultants. Supports DCSync, Kerberoasting, AD CS abuse (ESC1/3/4/6/7/9/10/13, Golden Certificate), resource-based constrained delegation, shadow credentials, LAPS and gMSA password reads, ACL abuse, GPO takeover, and lateral movement paths. Pure local PowerShell — no API calls, no data leaves your machine. Air-gap compatible.
version: 1.0.2
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

**Detected attack patterns:** DCSync and directory replication rights, Kerberoasting, unconstrained delegation, resource-based constrained delegation (RBCD), shadow credentials (AddKeyCredentialLink), LAPS and gMSA password reads, AD CS escalation (ESC1, ESC3, ESC4, ESC6a/b, ESC7, ESC9a/b, ESC10a/b, ESC13, Golden Certificate, CA management rights, PKI template flag writes), GenericAll / WriteDacl / WriteOwner / GenericWrite / AllExtendedRights ACL abuse, GPO takeover, lateral movement chains (AdminTo + HasSession + CanPSRemote / ExecuteDCOM / SQLAdmin), Tier 0 boundary violations, stale service account passwords, and sensitive data exposure paths.

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

Two synthetic exports are included for validation:

- `{baseDir}/tests/synthetic-bloodhound.json` — 5 classic paths (3 Critical, 2 High)
- `{baseDir}/tests/synthetic-adcs.json` — AD CS, RBCD, shadow credential, and schema-drift cases

Both contain fabricated data only. Neither reflects a real environment.

## Severity Scoring Model

Scoring is additive: every factor a path matches contributes points, so a
Kerberoastable account that also reaches Tier 0 with a stale password stacks all
three signals rather than collapsing to one category. The total is capped at 100.

### Path-level factors

| Factor | Points |
|--------|--------|
| Terminates at Tier 0 core (DA, EA, Administrators, DCs, Schema/Key Admins) | +40 |
| Terminates at a privileged operator group (Account/Backup/Server/Print Operators, DnsAdmins) | +30 |
| Unconstrained delegation anywhere in path | +20 |
| Sensitive data keyword in a node description | +15 |
| Kerberoastable source account | +10 |
| Kerberoastable account mid-path | +6 |
| Short path (1-2 hops) | +10 |
| Medium path (3 hops) | +5 |
| Lateral movement chain (AdminTo + HasSession) | +5 |
| Stale source password (>365 days) | +5 |

### Edge weights

Edge scoring is table-driven; the full table lives in
`scripts/lib/SeverityClassifier.txt` under `$Script:EdgeWeights`. The Tier 0
column is an additional bonus applied when the edge target is a Tier 0 object.

| Edge | Base | +Tier 0 |
|------|------|---------|
| DCSync / GetChangesAll / GetChanges | 30 / 25 / 20 | — |
| GenericAll, WriteDacl, Owns | 15 | +15 |
| AllExtendedRights, WriteOwner | 12 | +18 |
| GenericWrite, AddMember, ForceChangePassword, WriteAccountRestrictions | 10 | +10 to +15 |
| AddKeyCredentialLink (shadow credentials) | 20 | +10 |
| AllowedToAct / AddAllowedToAct (RBCD) | 20 | +10 |
| AllowedToDelegate (constrained delegation) | 10 | +10 |
| ReadLAPSPassword / SyncLAPSPassword / ReadGMSAPassword | 15 | — |
| GoldenCert | 40 | — |
| ADCSESC1 / ESC3 / ESC4 / ESC6a / ESC6b / ESC7 | 35 | — |
| ADCSESC9a/b, ESC10a/b, ESC13 | 30 | — |
| ManageCA / ManageCertificates | 25 / 20 | — |
| WritePKIEnrollmentFlag, WritePKINameFlag, DelegatedEnrollmentAgent | 20 | — |
| SQLAdmin, WriteSPN | 8 | — |
| CanPSRemote, ExecuteDCOM, AddSelf, GpLink, Enroll | 5 | +5 (GpLink) |
| AdminTo, HasSession, CanRDP | 3 | — |
| MemberOf, Contains, and AD CS structural edges | 0 (ignored) | — |

**Thresholds:** Critical >= 50 | High >= 30 | Medium >= 15 | Low < 15

### Unknown edges

Edge labels that are neither weighted nor explicitly ignored are collected and
reported through a warning at the end of the run, and are retrievable via
`Get-UnknownEdgeLabels`. This matters because BloodHound adds edge types between
releases: without it, a newer export would score unrecognised edges as zero and
silently understate severity.

### Scope note on AD CS

ESC1, ESC3, ESC4, ESC6, ESC7, ESC9, ESC10 and ESC13 are detected from the
composite `ADCSESC*` edges emitted by BloodHound CE. Techniques that BloodHound
does not model as a composite edge — notably ESC2, ESC5, ESC8 (NTLM relay to web
enrollment) and ESC11 — are **not** detected here. Use Certipy or a dedicated AD CS
audit for those; this skill reports what is present in the graph it is given.

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
