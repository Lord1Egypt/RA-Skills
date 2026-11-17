## Description:

Enables authenticated interaction with Slack for sending, editing, deleting, reacting to, and managing messages and pins via a secure bot token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rk905](https://clawhub.ai/user/rk905)

### License/Terms of Use:


## Use Case:

Employees, external collaborators, and developers use this skill to let an agent perform authorized Slack workspace actions such as sending messages, managing reactions and pins, reading recent channel history, and looking up member or emoji information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped or personal Slack token could expose or modify workspace content beyond the intended use.

Mitigation: Install with a dedicated Slack bot token, grant only the listed scopes and channels needed, and do not use personal user tokens or broad workspace permissions.

Risk: Send, edit, pin, unpin, or delete actions can change visible Slack content.

Mitigation: Confirm channel IDs, message IDs, and message text before executing any content-changing action, and require explicit approval before deleting messages.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [JSON action payloads and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Slack Bot User OAuth token stored in SLACK_BOT_TOKEN and operates only within the bot token's granted workspace permissions.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
