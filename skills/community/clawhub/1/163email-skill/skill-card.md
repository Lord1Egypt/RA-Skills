## Description:

Sends plain text email through the 163 SMTP service with configurable recipients, subject, and body content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubindashen](https://clawhub.ai/user/liubindashen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to send notification emails from a configured 163 mail account by CLI or Python import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses mail credentials to authenticate to the configured SMTP service.

Mitigation: Use a dedicated SMTP authorization code rather than a primary account password, and scope the account to the intended automation workflow.

Risk: Recipients, subjects, and message bodies are sent to the SMTP provider.

Mitigation: Avoid sending secrets or regulated data unless the account, recipients, and provider use are approved for that content.

Risk: An agent with access to this skill can send real emails from the configured account.

Mitigation: Install only in workflows where outbound email is intended, and review recipients and message content before execution when user approval is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liubindashen/skills/163email-skill)
- [Publisher profile](https://clawhub.ai/user/liubindashen)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration]

**Output Format:** [Plain text email content, CLI output, and Python Boolean return values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAW_EMAIL and CLAW_EMAIL_AUTH environment variables; uses smtp.163.com:465 by default.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
