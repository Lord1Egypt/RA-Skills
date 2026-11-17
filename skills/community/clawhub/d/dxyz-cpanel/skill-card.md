## Description:

Manage cPanel hosting accounts via API for version 134.0.11 and compatible versions, including account management, DNS zones, email accounts, databases, file operations, SSL certificates, backups, and bandwidth monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picodozbotdoz](https://clawhub.ai/user/picodozbotdoz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hosting administrators use this skill to operate cPanel and WHM servers through API calls and helper scripts for account, DNS, email, database, SSL, file, backup, and monitoring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue high-impact hosting administration commands, including account, DNS, database, and restore operations.

Mitigation: Require explicit human confirmation for destructive or restorative actions before running generated commands or helper scripts.

Risk: API credentials may be exposed or over-scoped if stored in plaintext configuration or broad WHM tokens.

Mitigation: Use narrowly scoped, revocable API tokens and prefer environment or secret-manager storage over plaintext config files.

Risk: Bundled helper scripts are flagged by security guidance for URL encoding, HTTPS enforcement, and create_account.sh sourcing issues.

Mitigation: Review and fix the helper scripts before using them against a real hosting environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/picodozbotdoz/skills/dxyz-cpanel)
- [cPanel API Reference](references/api-reference.md)
- [cPanel Error Codes Reference](references/error-codes.md)
- [cPanel Quick Reference Card](references/quick-reference.md)
- [cPanel Version 134.0.11 Changes](references/version-134-changes.md)
- [cPanel API Documentation](https://api.docs.cpanel.net/)
- [cPanel 134 Release Notes](https://docs.cpanel.net/release-notes/134-release-notes/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API call examples and helper-script invocations that require operator review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
