## Description:

Email Pro Optimized helps agents manage QQ Mail, Gmail, and Outlook accounts through IMAP/SMTP and OAuth 2.0, including listing accounts, checking, searching, fetching, analyzing, and sending email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q012315](https://clawhub.ai/user/q012315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate email workflows across QQ Mail, Gmail, and Outlook, including mailbox checks, search, message fetches, analysis, and outbound email with optional attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships exposed Outlook OAuth credentials.

Mitigation: Remove the bundled secret, use your own OAuth application credentials, and rotate or revoke any exposed credential before authorization.

Risk: The skill can send email and attachments from configured accounts.

Mitigation: Review OAuth scopes and verify every recipient, subject, body, and attachment before running send commands.

Risk: Credential and OAuth token files under ~/.openclaw/credentials are sensitive.

Mitigation: Limit access to credential files, keep token files out of shared workspaces, and review account entries before use.

Risk: Developer scripts can publish code or copy files into another workspace.

Mitigation: Avoid or delete auto-push.py and sync-updates.py unless their target paths and repository actions have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/q012315/skills/email-pro-optimized)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Gmail API profile endpoint](https://www.googleapis.com/gmail/v1/users/me/profile)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, requests, and user-controlled mail or OAuth credentials; email query commands return structured JSON.]

## Skill Version(s):

2.2.0 (source: server release metadata; artifact/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
