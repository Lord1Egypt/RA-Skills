## Description:

Feishu IM helps an agent prepare Feishu OpenAPI calls for sending messages, creating and managing chats, updating chat surfaces, and handling IM-related operational tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyyao2222-eng](https://clawhub.ai/user/sunnyyao2222-eng)

### License/Terms of Use:


## Use Case:

Developers and workplace automation operators use this skill to construct Feishu IM requests for messaging, group creation, membership updates, message recall, urgent notifications, announcements, tabs, widgets, feed cards, and related chat configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad workplace messaging and group-management actions, including private messages, bulk sends, recalls, membership changes, and persistent chat configuration updates.

Mitigation: Require explicit human approval before executing private messages, bulk sends, message recalls, membership changes, urgent notifications, or chat configuration changes.

Risk: A deployed agent may receive Feishu permissions that allow it to message users, create or modify chats, add members, and update chat surfaces.

Mitigation: Scope Feishu app permissions and accessible users or chats to the minimum required for the intended workflow.

## Reference(s):

- [Feishu IM OpenAPI Base](https://open.feishu.cn/open-apis/im/v1)
- [ClawHub Skill Page](https://clawhub.ai/sunnyyao2222-eng/skills/feishu-im)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON, configuration]

**Output Format:** [Markdown guidance with Feishu endpoint examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu tenant access tokens and appropriate IM permissions before API calls can succeed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
