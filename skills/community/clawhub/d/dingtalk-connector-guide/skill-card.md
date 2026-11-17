## Description:

Guides Chinese enterprise users and DingTalk developers through configuring an OpenClaw DingTalk bot connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise administrators use this skill as guidance for creating a DingTalk internal app, configuring bot message delivery, granting DingTalk permissions, and connecting OpenClaw to group chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide may lead administrators to grant broad DingTalk company chat, directory, and member-read permissions.

Mitigation: Grant only the DingTalk permissions needed for the selected features, avoid directory and member scopes unless required, and test first in one group.

Risk: The setup requires protecting DingTalk AppSecret credentials and a public webhook endpoint.

Mitigation: Store AppSecret securely, validate and monitor webhook traffic, configure allowed_chats before rollout, and rotate credentials when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/dingtalk-connector-guide)
- [DingTalk Open Platform](https://open.dingtalk.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with command and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance only; no executable code is shipped in the artifact.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
