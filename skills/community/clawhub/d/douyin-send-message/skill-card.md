## Description:

在抖音网页版发送私信消息，当用户想发送抖音私信、提醒续火花、或者提到“抖音发消息”、“发抖音私信”或“douyin send message”时触发，并支持独立使用或配合人物关系管理技能使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvin-dean](https://clawhub.ai/user/calvin-dean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send Douyin Web private messages to a specified contact, either from a directly supplied Douyin nickname or after resolving a nickname through a relationship-management skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate through a live logged-in Douyin account and send a private message without an explicit final confirmation step.

Mitigation: Require manual confirmation of the sending account, recipient, and exact message content immediately before dispatch.

Risk: The bundled script hard-codes a local browser profile path and writes screenshots that may expose private messages or account state.

Mitigation: Replace local profile paths before use, avoid running the bundled script as-is, and disable or securely handle screenshots containing private conversation data.

Risk: The workflow may suggest dynamically installing a related relationship-management skill.

Mitigation: Prefer a manually supplied Douyin display name or verify and pin any related dependency before installation.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/calvin-dean/skills/douyin-send-message)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown instructions with inline JavaScript and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Douyin Web session and manual confirmation before sending messages.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
