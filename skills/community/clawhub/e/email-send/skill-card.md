## Description:

Send a quick email via SMTP using `msmtp` without opening a full mail client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send short SMTP email messages from an agent workflow using `msmtp`, including basic headers, CC/BCC recipients, and attachment-oriented guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email bodies, recipients, CC/BCC fields, and attachments may disclose information externally.

Mitigation: Review message content, recipient lists, attachment paths, and data sensitivity before sending email.

Risk: SMTP credentials are required in the environment.

Mitigation: Use scoped SMTP credentials through an approved secret-management path and avoid exposing credential values in prompts, logs, or generated commands.

Risk: Attachment behavior is not fully described by the artifact.

Mitigation: Review any attachment command before execution and test with non-sensitive files before sending real attachments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/email-send)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires `msmtp` and configured `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, and `SMTP_PASS` environment variables.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
