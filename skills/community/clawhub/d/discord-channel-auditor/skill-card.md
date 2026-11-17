## Description:

Audit and auto-update a Discord server guide channel. Compares a reference guide message against actual channels, detects new/renamed/deleted/moved channels, and posts an updated guide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npfaerber](https://clawhub.ai/user/npfaerber)

### License/Terms of Use:


## Use Case:

External community managers and server operators use this skill to keep a Discord guide channel aligned with the current channel list after channels are created, renamed, moved, or deleted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently delete and repost Discord guide-channel messages when the bot has broad message-management permissions.

Mitigation: Restrict Manage Messages permission to the guide channel, store created message IDs, verify bot authorship, skip pinned or user-authored messages, log planned changes, and require confirmation or dry-run review before scheduled updates mutate content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/npfaerber/skills/discord-channel-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guide content and concise status guidance for Discord message updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue Discord channel listing, read, send, delete, and edit operations through OpenClaw's configured message tool.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
