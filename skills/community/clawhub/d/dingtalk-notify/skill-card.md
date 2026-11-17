## Description:

Sends DingTalk work notifications and files to a specified user, with commands for connectivity testing, retrying failed sends, checking status, and switching DingTalk bot models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m646pxhjf4-dot](https://clawhub.ai/user/m646pxhjf4-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for DingTalk work notification commands that send messages or files, test connectivity, retry failed sends, and check delivery status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send arbitrary notification content or files through DingTalk to a fixed external user ID.

Mitigation: Review each proposed send command, confirm the recipient and file path, and use only with trusted DingTalk helper scripts.

Risk: The referenced DingTalk helper scripts and OAuth token handling are outside the reviewed skill package.

Mitigation: Audit the local helper scripts and token storage before enabling the skill in a shared or production agent environment.

Risk: Notification send records may include message or file metadata outside the skill package.

Mitigation: Confirm retention, access controls, and data handling for local notification logs before sending sensitive content.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that send DingTalk messages or files through local helper scripts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
