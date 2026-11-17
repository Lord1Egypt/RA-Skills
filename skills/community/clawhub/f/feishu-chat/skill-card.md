## Description:

Feishu (Lark) group chat messaging guide for OpenClaw, covering Raw/Card message modes, @ mention formatting, and group member management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heimo-he](https://clawhub.ai/user/heimo-he)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide OpenClaw agents when sending Feishu or Lark group messages, choosing between raw and card rendering, formatting @ mentions, and managing known group member identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's examples can be used to send messages to real Feishu groups, including @everyone when workspace permissions allow it.

Mitigation: Confirm the target group, recipient scope, and message content before sending, and reserve @everyone for cases approved by the workspace.

Risk: Saved Feishu member identifiers and bot App IDs can expose workspace-specific routing details.

Mitigation: Store member IDs only in appropriate workspace memory or configuration locations and avoid sharing them outside the intended group context.

Risk: Using both direct replies and the message tool for the same content can produce duplicate group messages.

Mitigation: Choose one sending method per message: use the message tool for raw plain text and direct replies for card-formatted Markdown.

## Reference(s):

- [Feishu Developer Console](https://open.feishu.cn/app)
- [ClawHub skill page](https://clawhub.ai/heimo-he/skills/feishu-chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command, YAML, and message-format examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu chat IDs, member IDs, App IDs, renderMode settings, and @ mention syntax supplied by the user or workspace.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
