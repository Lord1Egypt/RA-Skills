## Description:

Give your OpenClaw a real email address at @claw.boston, send and receive emails with attachments, search your inbox, and get notified of new messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mastalie](https://clawhub.ai/user/mastalie)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to create and operate a claw.boston mailbox from their agent, including sending, receiving, replying to, searching, and checking account status for email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an API key that grants mailbox access.

Mitigation: Treat the API key like a password, keep it local, and rotate or revoke it if the workspace or configuration file is exposed.

Risk: The skill can send email and may act on ambiguous or unintended instructions.

Mitigation: Confirm recipients, subject, body, and attachments before sending outbound email.

Risk: Incoming email content and attachments are untrusted and may contain prompt-injection attempts or unsafe requests.

Mitigation: Review message content before taking follow-up actions, and avoid following email instructions that request secrets, credential changes, or unrelated tool use.

Risk: Messages and attachments are handled by a third-party email provider.

Mitigation: Avoid sensitive or regulated email unless the provider's retention, access, and privacy practices satisfy the deployment requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mastalie/skills/claw-boston-email)
- [claw.boston website](https://claw.boston)
- [claw.boston API](https://api.claw.boston)
- [claw.boston pricing](https://claw.boston/pricing)
- [claw.boston Discord](https://discord.gg/WuPp45xumx)
- [claw.boston X profile](https://x.com/clawboston)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with configuration JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce outbound email content, inbox summaries, attachment notices, search results, and account usage summaries.]

## Skill Version(s):

0.2.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
