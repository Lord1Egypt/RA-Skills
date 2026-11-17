## Description:

Sends the same notification through email with Himalaya and iMessage with BlueBubbles using shared markdown formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to prepare and send a single notification across email and iMessage, with consistent formatting and per-channel success or failure reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted notification content could exploit the documented shell heredoc pattern and execute local commands.

Mitigation: Review and fix the email send workflow before routine use; pass message content through a safer API or temporary file path instead of interpolating untrusted text into shell input.

Risk: Crafted subject or message content could create unintended email headers or alter delivered notification content.

Mitigation: Validate recipient, subject, and body fields and use the mail client's structured message options when available.

Risk: The skill sends message content to configured email and iMessage services.

Mitigation: Use it only with trusted message text and intended recipients, and confirm channel configuration before sending.

## Reference(s):

- [Channel Configuration](references/channels.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/cross-channel-notify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with shell command examples and channel-specific message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a full markdown email body and a compact iMessage body truncated to 2000 characters.]

## Skill Version(s):

9.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
