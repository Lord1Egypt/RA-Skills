## Description:

Identity provider compliance checks for auditclaw-grc. 8 read-only checks across Google Workspace (MFA, admin audit, inactive users, passwords) and Okta (MFA, password policy, inactive users, session policy).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailnike](https://clawhub.ai/user/mailnike)

### License/Terms of Use:

MIT

## Use Case:

Developers and security or GRC teams use this skill to collect Google Workspace and Okta identity-provider compliance evidence for AuditClaw GRC. It supports MFA, administrator, inactive-user, password, and session-policy checks and records results for audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can expose highly privileged Google Workspace and Okta access.

Mitigation: Use dedicated least-privilege Google Workspace and Okta service identities, remove the unused Google audit-report scope, and grant only the read permissions needed for configured checks.

Risk: Identity-provider tokens and tenant configuration could be misused if exposed or pointed at the wrong tenant.

Mitigation: Restrict OKTA_ORG_URL to the exact tenant, store tokens outside shared logs or prompts, and rotate Google and Okta credentials on a regular schedule.

Risk: The local GRC database stores identifiable user security-posture data.

Mitigation: Protect ~/.openclaw/grc/compliance.sqlite with local access controls, encrypted backups where applicable, and retention aligned to the organization's audit policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mailnike/skills/auditclaw-idp)
- [AuditClaw homepage](https://www.auditclaw.ai)
- [AuditClaw GRC](https://github.com/avansaber/auditclaw-grc)
- [Declared source repository](https://github.com/avansaber/auditclaw-idp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs configured provider checks and stores automated evidence records in the local AuditClaw GRC SQLite database.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
