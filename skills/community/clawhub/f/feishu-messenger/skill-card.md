## Description:

Feishu Messenger helps an agent send Feishu text messages, images, and files to individual users or group chats using OpenClaw messaging commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanl754](https://clawhub.ai/user/hanl754)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent send Feishu notifications, screenshots, logs, reports, and other selected workspace files to known Feishu recipients. It is useful for operational updates and file handoff workflows where recipient IDs and outbound content are reviewed before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages or files may be sent to the wrong Feishu recipient if the target ID is incorrect.

Mitigation: Confirm the open_id or chat_id before sending, and test bulk sends with one recipient first.

Risk: Screenshots, logs, documents, or reports may contain secrets, personal data, customer data, or internal details.

Mitigation: Review and redact selected content before sending it through Feishu.

Risk: Media sends may fail or behave unexpectedly when absolute paths or home-directory paths are used.

Mitigation: Copy files into the OpenClaw workspace and use relative media paths such as ./file.ext.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanl754/skills/feishu-messenger)
- [Feishu Open Platform](https://open.feishu.cn/)
- [OpenClaw message documentation](https://docs.openclaw.ai/tools/message)
- [Feishu message API](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional Python subprocess snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Feishu through OpenClaw and may include user-selected relative media paths.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
