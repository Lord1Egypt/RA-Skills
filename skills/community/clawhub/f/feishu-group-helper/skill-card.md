## Description:

Manage Feishu group information, record join and leave events, look up active groups by name, and send messages to selected groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panmenglin](https://clawhub.ai/user/panmenglin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a local registry of Feishu groups for an agent, confirm active group membership, and prepare or send messages to the correct group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can be configured to read or overwrite arbitrary local JSON files.

Mitigation: Constrain the group registry path to the agent workspace before broader use.

Risk: The skill can send messages to Feishu groups using bot permissions.

Mitigation: Require user confirmation before sending messages to groups.

Risk: The skill stores group metadata locally.

Mitigation: Provide a way to review and delete stored group records.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [ClawHub skill page](https://clawhub.ai/panmenglin/skills/feishu-group-helper)
- [Publisher profile](https://clawhub.ai/user/panmenglin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript code examples and Feishu permission references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference or update a workspace-local JSON group registry and may require Feishu message-sending permissions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
