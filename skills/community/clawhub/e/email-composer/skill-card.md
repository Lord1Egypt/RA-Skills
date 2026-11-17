## Description:

Email writer and sender for OpenClaw. Use when user needs to draft, reply, or send emails via browser. Supports Gmail, Outlook, QQ Mail, 163 Mail. Requires OpenClaw v2026.3.22+ with browser access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to draft, reply to, and send email through a logged-in browser session across supported webmail providers. It is intended for composing individual messages in Gmail, Outlook, QQ Mail, 163 Mail, or 126 Mail with user-provided recipient, subject, content, tone, and language details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email from a live logged-in account without a required final approval step.

Mitigation: Use draft-only workflows where possible and manually review the recipient, subject, account, and full message body before sending.

Risk: The skill operates inside browser sessions for logged-in email accounts.

Mitigation: Use it only with accounts where browser automation is acceptable and avoid use with sensitive accounts unless the user explicitly accepts that access pattern.

Risk: Attacker-provided or untrusted HTML may affect messages handled by the skill.

Mitigation: Avoid pasting untrusted HTML or attacker-provided content into email content processed by the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/email-composer)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Email draft text with browser automation guidance and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw v2026.3.22+ with browser access; no required bins or environment variables are listed in server metadata.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
