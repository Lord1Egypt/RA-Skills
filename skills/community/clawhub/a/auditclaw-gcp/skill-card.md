## Description: <br>
GCP compliance evidence collection for auditclaw-grc across Cloud Storage, firewall, IAM, logging, KMS, DNS, BigQuery, Compute, and Cloud SQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailnike](https://clawhub.ai/user/mailnike) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Cloud security, compliance, and GRC teams use this skill to collect read-only GCP configuration evidence and store automated findings for AuditClaw GRC workflows. It supports project-level checks for storage, firewall, IAM, logging, KMS, DNS, BigQuery, Compute Engine, and Cloud SQL controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires GCP authentication and may guide users toward long-lived service account JSON credentials. <br>
Mitigation: Prefer keyless or short-lived GCP authentication where possible, restrict the service account to the smallest read-only scope needed, store any JSON key outside the repo with tight file permissions, rotate and monitor it, and revoke it when scanning is complete. <br>
Risk: The skill reads cloud configuration across multiple GCP services and stores findings in a local GRC database. <br>
Mitigation: Review the setup before installing, use read-only roles, verify the target GCP project, and limit database access to users who should see compliance evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mailnike/auditclaw-gcp) <br>
- [AuditClaw homepage](https://www.auditclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes automated GCP evidence records to an AuditClaw GRC SQLite database when run with configured credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
