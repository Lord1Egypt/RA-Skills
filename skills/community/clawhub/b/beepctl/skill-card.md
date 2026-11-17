## Description:

Use when sending messages, searching chats, or managing conversations across messaging platforms (Telegram, WhatsApp, Slack, iMessage, etc.) via Beeper Desktop API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blqke](https://clawhub.ai/user/blqke)

### License/Terms of Use:


## Use Case:

External users and developers use beepctl to let an agent inspect Beeper-connected accounts and chats, search messages, manage conversations, and prepare or send messages through the Beeper Desktop API. Message-sending actions should be confirmed by the user before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an unpinned global CLI package.

Mitigation: Install only after deciding that the beepctl npm package is trusted for the target environment.

Risk: The skill can access private messages, attachments, and a Beeper API token across connected messaging services.

Mitigation: Use narrow chat and account filters for searches, avoid token-reveal commands unless necessary, and limit agent access to contexts where message data exposure is acceptable.

Risk: The skill can send messages or change chats through the Beeper Desktop API.

Mitigation: Require explicit confirmation before sending messages or modifying chats, including a clear recipient and message preview.

Risk: Attachment downloads can write files to user-selected paths.

Mitigation: Choose safe destination paths before downloading attachments and review requested paths before execution.

## Reference(s):

- [beepctl ClawHub Skill](https://clawhub.ai/blqke/skills/beepctl)
- [beepctl GitHub Repository](https://github.com/blqke/beepctl)
- [Beeper Desktop API](https://developers.beeper.com/desktop-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the beepctl CLI and access to the user's Beeper Desktop API context.]

## Skill Version(s):

0.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
