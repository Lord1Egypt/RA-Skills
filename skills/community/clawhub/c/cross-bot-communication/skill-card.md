## Description:

Helps an agent reason about Telegram bot-to-bot communication by scanning accessible groups or channels, checking route conditions, and selecting an honest communication path when possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate Telegram bots that may share groups or channels, verify whether communication conditions are met, and present alternatives when a route is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to map Telegram groups, channels, bot ownership, and admin status that it can access, which can expose relationship data without clear consent or deletion controls.

Mitigation: Require explicit per-scan consent, restrict discovery to named chats or bots, and define how relationship data can be reviewed and deleted.

Risk: Automatic route selection could send messages through an unintended group or channel.

Mitigation: Confirm each outbound message route before use and report unavailable routes honestly instead of attempting unsupported communication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adminlove520/skills/cross-bot-communication)
- [Publisher Profile](https://clawhub.ai/user/adminlove520)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Telegram group, channel, admin-status, and fallback-route checks before an agent sends messages.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
