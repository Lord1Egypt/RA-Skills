## Description:

Draft and send emails via browser automation. Supports Gmail, Outlook, QQ Mail, 163 Mail. Requires OpenClaw v2026.3.22+ with browser access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft new emails, compose replies, and send them through a logged-in browser session after confirming recipient, subject, content, tone, and login state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can control a logged-in webmail session and send email content or attachments to external mail providers.

Mitigation: Require explicit user review of the recipient, thread, subject, body, and attachments before any send action, and avoid sensitive content unless the privacy wording is corrected.

Risk: Safety gaps around automatic sending and message handling could cause email to be sent before the final target and content are verified.

Mitigation: Prefer plain-text insertion followed by a final confirmation after the target email address and message body are resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/email-writer)
- [Publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [Text, Guidance, Browser automation actions]

**Output Format:** [Plain-text email content with browser automation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw v2026.3.22+ with browser access and a logged-in webmail session; no batch or encrypted email support.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
