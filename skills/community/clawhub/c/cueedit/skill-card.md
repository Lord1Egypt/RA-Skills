## Description:

Lets an agent manage Instagram and Facebook Page comments, send private replies, and configure Instagram keyword-triggered auto-DMs through CueEdit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theindianappguy](https://clawhub.ai/user/theindianappguy)

### License/Terms of Use:

MIT

## Use Case:

People managing their own Instagram professional accounts or Facebook Pages can review comments, draft and send approved replies or private messages, and set up keyword-based Instagram auto-DM rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Active auto-DM rules continue running even if the assistant is disconnected.

Mitigation: Review active rules separately and pause them when disconnecting the assistant.

Risk: CLI write operations take effect immediately when invoked.

Mitigation: Show and approve the exact message, targets, and recipient count before sending.

Risk: Messages could affect an unintended account or audience.

Mitigation: Use only accounts you manage and confirm the target and recipient count before sending.

Risk: An exposed API key or an unintended API destination could compromise account actions.

Mitigation: Keep API keys out of chat and retain the default API destination unless intentionally configuring a trusted alternative.

## Reference(s):

- [CueEdit API reference](artifact/references/api.md)
- [CueEdit examples](artifact/references/examples.md)
- [CueEdit website](https://www.cueedit.io/?ref=skill)
- [ClawHub skill release](https://clawhub.ai/theindianappguy/skills/cueedit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Short message drafts, command examples, and plain-language results or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies, DMs, and rule changes require explicit user approval before sending.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
