## Description:

GCP compliance evidence collection for auditclaw-grc. 12 read-only checks across Cloud Storage, firewall, IAM, logging, KMS, DNS, BigQuery, Compute, and Cloud SQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailnike](https://clawhub.ai/user/mailnike)

### License/Terms of Use:


## Use Case:

Developers and security or compliance teams use this skill to collect automated GCP project evidence for AuditClaw GRC. It checks storage, firewall, IAM, logging, KMS, DNS, BigQuery, Compute, and Cloud SQL controls and stores results in the local GRC evidence database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs broad read visibility across a target GCP project to collect compliance evidence.

Mitigation: Use a tightly scoped custom role or the documented read-only roles only for projects where this visibility is approved.

Risk: Service account JSON keys can become long-lived credentials if generated for the integration.

Mitigation: Prefer keyless authentication where possible; otherwise keep JSON keys out of repositories, restrict file permissions, rotate them, and revoke them when no longer needed.

Risk: The local GRC SQLite database stores compliance evidence that may include sensitive cloud configuration details.

Mitigation: Protect the local database path, limit access to authorized users, and handle exported evidence as sensitive compliance data.

## Reference(s):

- [AuditClaw GCP ClawHub Page](https://clawhub.ai/mailnike/skills/auditclaw-gcp)
- [AuditClaw Homepage](https://www.auditclaw.ai)
- [GCP IAM Roles](artifact/scripts/gcp-roles.json)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs read-only GCP checks and writes automated evidence records to a local AuditClaw GRC SQLite database.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
