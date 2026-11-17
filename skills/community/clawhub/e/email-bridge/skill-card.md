## Description:

Email Bridge helps AI assistants manage email with real-time notifications, smart categorization, verification code extraction, HTML content sanitization, and support for Gmail, QQ Mail, and NetEase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanchan720](https://clawhub.ai/user/ryanchan720)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Email Bridge to connect personal mail accounts to an AI assistant for local email sync, recent-message review, verification code extraction, outgoing email, and new-email notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials and OAuth tokens are stored locally and can be reused if ~/.email-bridge is exposed.

Mitigation: Protect ~/.email-bridge, avoid sharing authorization codes in chat or command-line config, and revoke or rotate mail tokens when no longer needed.

Risk: The skill can cache full mailbox contents locally.

Mitigation: Review local storage before installation and remove ~/.email-bridge when decommissioning the skill.

Risk: New-email notifications can send email-derived data, including verification codes, into the assistant.

Mitigation: Disable include_verification_codes or OpenClaw notifications when this data should not enter the assistant context.

Risk: The skill can send email through configured accounts.

Mitigation: Review configured accounts and outgoing messages before relying on the skill for send workflows.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ryanchan720/skills/email-bridge)
- [Project homepage](https://github.com/ryanchan720/email-bridge)
- [Gmail setup guide](references/gmail-setup.md)
- [Gmail readonly OAuth scope](https://www.googleapis.com/auth/gmail.readonly)
- [QQ Mail authorization code guide](https://service.mail.qq.com/detail/0/75)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sanitized email summaries, verification codes, links, and account configuration guidance depending on user settings.]

## Skill Version(s):

0.6.3 (source: server release evidence, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
