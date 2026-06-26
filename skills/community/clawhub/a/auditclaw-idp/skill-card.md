## Description: <br>
Identity provider compliance checks for auditclaw-grc across Google Workspace MFA, admin audit, inactive users, passwords, and Okta MFA, password policy, inactive users, and session policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailnike](https://clawhub.ai/user/mailnike) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Security, compliance, and GRC teams use this skill to collect identity-provider evidence from Google Workspace and Okta and store findings for AuditClaw GRC workflows. It supports checks for MFA coverage, administrator posture, inactive accounts, password policy, and session policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests sensitive identity-provider access, including Google Workspace domain-wide delegation and Okta token permissions. <br>
Mitigation: Confirm the exact Google and Okta permissions before installation, use least-privileged read-only accounts or tokens, and avoid granting the Google admin.reports.audit.readonly scope unless the publisher explains why it is needed. <br>
Risk: The local GRC SQLite database may contain user emails, MFA status, admin status, login activity, and policy findings. <br>
Mitigation: Protect the local database with appropriate filesystem permissions, encryption or endpoint controls, and retention practices aligned to the organization's identity-data policy. <br>
Risk: Okta API tokens inherit the permissions of the administrator who creates them. <br>
Mitigation: Create a dedicated read-only admin or scoped token where available, rotate it regularly, and revoke it when the skill is no longer in use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mailnike/auditclaw-idp) <br>
- [AuditClaw Homepage](https://www.auditclaw.ai) <br>
- [AuditClaw IDP Source Link](https://github.com/avansaber/auditclaw-idp) <br>
- [AuditClaw GRC](https://github.com/avansaber/auditclaw-grc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON evidence] <br>
**Output Format:** [Markdown with inline shell commands and JSON evidence written to a local SQLite-backed GRC evidence store] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and optional Google Workspace or Okta credentials for provider-specific checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
