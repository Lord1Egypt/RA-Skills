## Description:

令牌管理中心 helps agents manage third-party API tokens, account passwords, and SSH keys with categorization, expiry reminders, password generation, encrypted backups, usage statistics, audit logs, and explicit-confirmation credential capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to store, retrieve, list, migrate, back up, and audit local API tokens, passwords, and keys during ClawHub/OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive credentials saved by this skill may be readable by code running as the same local user.

Mitigation: Use it only for low-risk local notes or temporary credentials, and rotate any deleted or exposed credentials at the provider.

Risk: The skill presents vault-like security features, but the security evidence says it should not be treated as a hardened password manager.

Mitigation: Use a managed secret store or dedicated password manager for high-value or production credentials.

Risk: Credential-like text can be detected from conversation content and saved after confirmation.

Mitigation: Review detected values before saving and avoid pasting credentials that do not need to be stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luis1213899/skills/creds-vault)
- [Publisher profile](https://clawhub.ai/user/luis1213899)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples and local JSON-backed credential records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local secrets.json, secrets.audit.log, encrypted backups, and lock files under the user's OpenClaw workspace.]

## Skill Version(s):

2.1.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
