## Description:

Web interface for agent email communication that supports inbox viewing, draft creation and editing, and sending through Gmail/Gog CLI integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up webmail access for agent inboxes, compose and send non-bot emails, and manage drafts through Roundcube or a custom Gmail/Gog CLI interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples could expose a Gmail inbox and sending capability without sufficient protection.

Mitigation: Require authentication, bind the interface locally or place it behind HTTPS, disable debug mode, add CSRF protection, and keep Gmail secrets outside versioned or image-baked configuration.

Risk: Email transport configuration can weaken connection security if certificate validation is disabled.

Mitigation: Keep certificate validation enabled for IMAP and SMTP connections unless a reviewer approves a controlled exception.

## Reference(s):

- [Roundcube](https://roundcube.net)
- [Gmail IMAP configuration](https://support.google.com/mail/answer/7126229)
- [Gog CLI](https://github.com/openclaw/gog)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell, PHP, Python, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup steps, configuration snippets, security guidance, testing checklist, and fallback implementation options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
